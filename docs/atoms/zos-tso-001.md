---
id: ZOS-TSO-001
title: TSO（対話シェル + ISPF）
status: stable
last_reviewed: 2026-05-09
---


# ZOS-TSO-001: TSO

## 1. purpose（なぜ存在するか）

TSO（Time Sharing Option）は z/OS の対話インタフェース。Linux で言う「ssh + bash」に相当するが、**対話＋全画面エディタ（ISPF）＋データセット参照** が一体化している。

JCL がバッチ実行（→ [ZOS-JCL-001](zos-jcl-001.md)）の世界なら、TSO は対話実行の世界。**両者で扱う「データセット」は同じ実体**だが、起動モデルが正反対。バッチは静的宣言、TSO は動的（プロンプトでコマンド連発）。

歴史的には MVS が batch 専用だった時代に、開発者向けに後付けされた対話モード。だから今も「TSO はオプション扱い」という名前のまま。実際にはこれ無しで運用できないので、全 z/OS サイトに必須。

ISPF は TSO 上で動く全画面エディタ + メニューシステム。**z/OS 開発者が起きてる時間の 80% は ISPF 画面を見てる**と言って過言ではない。

## 2. mechanism（どう動くか）

- TSO セッションは **アドレススペース** 1 つを占有。`LOGON USERID` で起動、`LOGOFF` で消える
- TSO コマンドは英語の動詞: `ALLOCATE`, `LISTC`, `RENAME`, `DELETE`, `EXEC`, `SUBMIT` 等
- **REXX**: TSO 上のスクリプト言語
- **CLIST**: REXX より古い、新規はほぼ書かない
- **ISPF**: `ISPF` コマンドで全画面メニューに切り替わる
  - `=3.4` のような shortcut で深い階層に直接ジャンプ
- **SDSF**: ISPF 上で動くスプール閲覧
- 端末は通常 3270 エミュレータ（PCOMM, TN3270 等）で接続

## 3. prerequisites（理解の前提）

- データセット概念（→ [ZOS-DATASET-001](zos-dataset-001.md)）
- JCL（→ [ZOS-JCL-001](zos-jcl-001.md)）
- 一般 IT 知識: シェルとエディタの分離（Unix の bash + vi）が ISPF では融合している

## 4. relations（他アトムとの繋がり）

- `depends_on`: [ZOS-DATASET-001](zos-dataset-001.md), [ZOS-JCL-001](zos-jcl-001.md)
- `specialized_by`: なし
- `contrasts_with`: [ZOS-JCL-001](zos-jcl-001.md)（対話 vs バッチ）, [ZOS-USS-001](zos-uss-001.md)（z/OS native vs POSIX）
- `used_by`: 全アトム（運用入口）

## 5. pitfalls（実装・運用での落とし穴）

- **3270 端末で日本語が文字化け**: PCOMM 等のコードページ設定が IBM-930 / IBM-939 に合ってないと、データセット内日本語が「@@@@」「\\\\」等になる。**コードページ統一が運用初期の落とし穴**、Windows 側で `ja-JP` 系設定でも 3270 ターミナルは EBCDIC 系を別途指定要。
- **ISPF EDIT で `MAX` 行超過**: ISPF 標準では編集対象データセットのレコード上限あり（既定 80MB 程度）。巨大ログファイルを EDIT で開くと「LARGE FORMAT FILE - VIEW ONLY」で編集不可。`BROWSE` で見る or 分割するしかない。
- **TSO セッション残置で REGION 占有**: LOGOFF 忘れた TSO セッションがアドレススペースを保持し続け、夜間バッチの REGION 不足を招く事案。サイト運用で「アイドル 30 分で自動 LOGOFF」設定があるが、有効になってない事もある。
- **REXX で `CALL ... ON ERROR` 抜け漏れ**: REXX のエラー処理は `SIGNAL ON ERROR` を明示しないと、TSO コマンド失敗時もスクリプトが平然と続行する。**バッチで使う REXX は必ず先頭で `SIGNAL ON ERROR`** が原則。
- **ALLOCATE で SHR/OLD の混乱**: `ALLOC F(MYDD) DA('USER.X') SHR` で SHR を付けないと OLD（排他）になり、別 TSO や JCL とロック衝突。`FREE` し忘れたまま LOGOFF せずに別セッションで `ALLOC` すると `dataset enqueued` で一見謎エラー。
- **ISPF EDIT のリカバリ未保存**: 突然回線切断（VPN・Citrix 等経由でよくある）で ISPF EDIT セッション死亡 → 編集中データ消失。**ISPF オプション 0 の Edit Recovery を「ON」**にしておくと自動保存されるが、デフォルト OFF のサイトもあり、知らない人が大事故。

## 6. examples（具体例）

```tso
LISTC LEVEL(USER.PROD)
LISTC ENT(USER.PROD.SALES) ALL
ALLOC F(SYSIN) DA('USER.JCL(MYJOB)') SHR
SUBMIT 'USER.JCL(MYJOB)'
RENAME 'USER.OLD' 'USER.NEW'
DELETE 'USER.X'
EXEC 'USER.REXX(MYSCR)' 'arg1 arg2'
```

ISPF パネル shortcut:
```
=3.4   DSLIST（最も使う）
=2     EDIT
=3.1   ライブラリ ユーティリティ
=SDSF  ジョブ出力
```

REXX 例:
```rexx
/* REXX */
SIGNAL ON ERROR
ADDRESS TSO
"ALLOC F(IN) DA('USER.PROD.IN') SHR"
"EXECIO * DISKR IN (FINIS STEM record."
DO i = 1 TO record.0
   SAY i": " record.i
END
"FREE F(IN)"
EXIT 0

ERROR:
   SAY 'TSO command failed RC='RC' line='SIGL
   EXIT 8
```

## 7. decision_axes（採否を分ける判断軸）

- **TSO 直接 vs ISPF 経由**: 単発コマンド（LISTC, RENAME 等）は TSO READY で直接打つのが速い。複数操作 / データセット閲覧 / JCL 編集は ISPF。**慣れた運用者は両方使い分ける**、初心者を ISPF 内に閉じ込めるのは速度低下。
- **REXX vs CLIST**: 新規 TSO スクリプトは REXX 一択。CLIST は古い文化。**既存 CLIST 資産を REXX に書換える価値があるかは別問題、動いてる物は触らない原則**。
- **ISPF Edit vs Browse vs View**: View は読み取り専用編集、Browse は表示のみ、Edit はフル編集。**生ログは Browse**（誤更新防止）、**作業ファイルは Edit**、**過去 JCL の参照は View**。
- **3270 ターミナル ソフト選定**: PCOMM (IBM 公式、有償)、TN3270 (OSS)、x3270 (Linux/Mac)。本番運用は PCOMM 推奨、開発は OSS で十分。**SSL/TLS 対応必須**。
- **ISPF Edit の数値制限を超える時**: 巨大ファイルは ISPF Edit 不可 → 切り出して編集 + 連結戻し。**この運用が必要になる規模はそもそも別ツール（バッチ加工）の方が筋良い**。
