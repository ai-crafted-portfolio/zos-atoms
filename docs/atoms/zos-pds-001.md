---
id: ZOS-PDS-001
title: 区分データセット（PDS / PDSE）
status: stable
last_reviewed: 2026-05-09
---


# ZOS-PDS-001: 区分データセット（PDS / PDSE）

## 1. purpose（なぜ存在するか）

PDS（Partitioned Data Set）は「**1 つのデータセットの中に複数の独立メンバ**」を持てる構造。Linux で言えば「ディレクトリ + 配下の小ファイル」を 1 つの実体にまとめたもの、ただし階層は 1 段だけ。

なぜ必要か: ロードモジュール（実行可能形式）を 1 つずつ別データセットにすると、カタログエントリが爆発する（数千〜数万個）。BIND された COBOL/PL/I プログラムは 1 個 = 1 メンバとして PDS に格納する事で、カタログ負荷を 1/100 以下にできる。**JCL ライブラリ・PROC ライブラリ・SYSLIB（コンパイル include 用）など、メインフレームの「ライブラリ」と呼ばれるものは大半が PDS**。

PDSE（Extended）は PDS の現代版。古い PDS の致命的欠陥（圧縮再編成必要、並行更新不可、ディレクトリ部の上限）を解決した別実装。新規はほぼ PDSE 一択だが、**旧プログラム互換性問題**で完全移行できない事例が現場に残る。

## 2. mechanism（どう動くか）

### PDS（古典）

- 先頭部に **ディレクトリ**（メンバ名 → 相対トラック・ブロック番号の対応表）
- メンバ更新時:
  - 同サイズ以下なら原位置上書き
  - サイズ増 or 名前変更 → 末尾に新コピー、旧領域は **「死んだ領域」として残る**
  - 死んだ領域の累積 → **IEBCOPY で圧縮再編成必要**
- ディレクトリブロック数は **DEFINE 時固定**（`SPACE=(CYL,(10,5,20))` の 3 つ目 20）。これを使い切ると `B14` ABEND

### PDSE

- ディレクトリは **HFS の inode 風** の動的構造
- 削除時に空き領域 **自動回収**
- **並行更新可能**
- **プログラム オブジェクト**格納可、これは PDSE 必須機能
- 但し **古いユーティリティ（特に SMP/E 配布の古い IBM）が PDSE で誤動作**するリスク残存

両者の見分け: `LISTCAT ENT(...) ALL` で `DSNTYPE=LIBRARY` なら PDSE。

## 3. prerequisites（理解の前提）

- データセット概念（→ [ZOS-DATASET-001](zos-dataset-001.md)）
- DASD のシリンダ・トラック構造（→ [ZOS-DASD-001](zos-dasd-001.md)）
- メンバ名規約（1〜8 文字、英数字 + `@#$`）

## 4. relations（他アトムとの繋がり）

- `depends_on`: [ZOS-DATASET-001](zos-dataset-001.md)
- `specialized_by`: なし
- `contrasts_with`: [ZOS-USS-001](zos-uss-001.md)（POSIX ディレクトリ）
- `used_by`: [ZOS-JCL-001](zos-jcl-001.md) (JCL ライブラリ), [ZOS-CICS-001](zos-cics-001.md) (LOAD ライブラリ), [ZOS-DB2-001](zos-db2-001.md) (DBRM ライブラリ)

## 5. pitfalls（実装・運用での落とし穴）

- **PDS ディレクトリブロック枯渇**: `SPACE=(CYL,(10,5,20))` の 20 は固定枠。プロジェクトが大きくなって 25 メンバ目を追加したら `B14-08` ABEND（ディレクトリ満杯）。**増やすには再 DEFINE + 全メンバコピーが必要**。新規はディレクトリ多めに（200 とか）取っておく事。PDSE なら自動拡張。
- **PDS の死領域で容量誤認**: 100 シリンダ取った PDS のメンバ削除を繰り返すうちに、`LISTC` では 60 シリンダ使用と出るが、実際には死領域含めて 95 シリンダ消費。**圧縮 (IEBCOPY) しないと容量見積もりが狂う**。週次ジョブで圧縮を回す運用が必要。
- **PDSE で古いユーティリティ ABEND**: 古い IEBUPDTE（プロダクト ID 5752-CC1）系で PDSE のメンバを更新すると `IEC036I` 等の謎エラー。最新ユーティリティに置き換えれば直るが、保守用 JCL でひっそり古い物が混じってる事案多い。**PDSE 移行プロジェクトの 90% はこのトラップ調査に費やされる**。
- **ロードモジュール（PDS）と Program Object（PDSE）の互換性**: 古いロードモジュール（PDS）は PDSE にコピーすると program object 形式に変換されない。`AMASPZAP`, `IEBCOPY COPYMOD` 等で意図的に変換、忘れると新しいリンケージ機能（DLL Re-entrancy 等）が利かない。
- **メンバ名 8 文字制限**: 1〜8 文字、`A`-`Z`, `0`-`9`, `@`, `#`, `$` のみ、先頭は数字不可。9 文字目を切る運用ルールを作らないと、複数チームでメンバ名衝突。**プロジェクト・サブシステムで先頭 2〜3 文字を予約する**運用が定石。
- **ALIAS メンバの管理**: PDS/PDSE では「メンバ A は B の alias」という同一実体への複数名指しが可能。alias を消す時に主メンバを消してしまい全 alias が消える事故あり。

## 6. examples（具体例）

```jcl
//* PDS 新規作成（ディレクトリ 50 ブロック）
//PDS01 DD DSN=USER.PROD.PROCLIB,DISP=(NEW,CATLG),
//         SPACE=(CYL,(20,5,50)),
//         DCB=(RECFM=FB,LRECL=80,BLKSIZE=27920,DSORG=PO),
//         UNIT=SYSDA

//* PDSE 新規作成
//PDSE01 DD DSN=USER.PROD.LOAD,DISP=(NEW,CATLG),
//          SPACE=(CYL,(50,10)),
//          DSNTYPE=LIBRARY,
//          DCB=(RECFM=U,BLKSIZE=32760,DSORG=PO),
//          UNIT=SYSDA

//* メンバ参照
//SYSIN DD DSN=USER.PROD.PROCLIB(MYJOB),DISP=SHR
```

```jcl
//* IEBCOPY で圧縮
//STEP01 EXEC PGM=IEBCOPY
//SYSPRINT DD SYSOUT=*
//SYSUT1   DD DSN=USER.PROD.PDS,DISP=OLD
```

## 7. decision_axes（採否を分ける判断軸）

- **PDS vs PDSE**: 新規ライブラリは PDSE 一択。**旧プログラム互換性が必要な箇所**（古いベンダー ISV ツール群、SMP/E 配布の古い HOLD ファイル）だけ PDS 残置。判断は「ツール群が PDSE で動くか確認」が前提、確認せず一律 PDSE にすると半月後にバグ発見、というのが起こる。
- **PDS 既定ディレクトリブロック数**: 想定メンバ数 + 50% を取る目安。100 メンバ予定なら 150 ブロック。**「絶対に増えない」と確信できない限り多めに取る**。PDSE なら関係ない。
- **ロードライブラリの分割**: 1 つの巨大 PDSE に全プログラム vs サブシステム別 PDSE。**サブシステム + 環境 (PROD/TEST/DEV)** で分割が中庸案。
- **IEBCOPY 圧縮頻度（PDS のみ）**: 更新頻度の高い PDS は週次圧縮が標準。**圧縮中は OPEN 不可なので業務時間外実施**。
- **メンバ名命名規約**: プロジェクト 2 文字 + 機能 3 文字 + 連番 3 文字 等。**「自由に付けて良い」とすると 1 年で衝突**。先頭 prefix 予約 + 検索しやすい命名規則が運用の前提条件。
