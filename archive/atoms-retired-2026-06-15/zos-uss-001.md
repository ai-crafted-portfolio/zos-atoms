---
id: ZOS-USS-001
title: UNIX System Services（HFS / zFS）
status: stable
last_reviewed: 2026-05-09
authors: [agent]
rag_verified: partially
---

# ZOS-USS-001: UNIX System Services

## 1. purpose（なぜ存在するか）

USS（UNIX System Services、旧名 OpenEdition MVS）は **z/OS 内蔵の POSIX 互換 UNIX サブシステム**。z/OS の伝統的な MVS データセット世界（→ ZOS-DATASET-001）の **隣に**、Linux/Unix 風のファイルシステム + シェル + 標準 C ランタイムを並列稼動させる。

なぜ必要か:
1. **オープンソース移植**: Java / Python / Apache HTTP / OpenSSH / Git 等を z/OS に動かしたいが、これらは POSIX 前提で書かれてる。USS が無いと動かない
2. **TCP/IP / Web サーバ**: HTTP サーバ、SFTP、cron 系処理は USS で動かす
3. **DevOps / モダン開発**: Git, Maven, Gradle, Liberty Profile 等
4. **z/OS UNIX シェル経由のスクリプト**: bash 風の自動化を z/OS 上で

「z/OS 内に Linux サブシステムが同居」という構図。**MVS データセットと USS ファイルは別物だが、相互参照可能**。

Linux/Windows と何が違うか:
- Linux: ファイルシステムが OS の中心、UNIX 唯一
- z/OS: MVS データセット（中心） + USS ファイル（別系統）の 2 系統、共存。**「どっち使うか」を毎回考える設計**

書籍 (BK_MF_001 / BK_ZOS_BASIC_001 / BK_KORN_001) 蒸留の補強観点として、USS は **「POSIX 互換層であって POSIX 完全実装ではない」** という前提を強く意識する必要がある。Linux 由来の OSS ツールチェーン (autotools / cmake / Python 拡張モジュール / Git hook 等) が、ファイル属性・改行・エンコーディング・signal 動作・fork 性能のいずれかで微妙に挙動が違って、ビルドが失敗するか、動作するが結果が違うパターンがある。**「Linux で動いた」を即「USS で動く」と読み替えない**、検証フェーズで実機テストを通す前提でプロジェクト計画を組むのが安全。

## 2. mechanism（どう動くか）

### ファイルシステム
- **HFS** (Hierarchical File System): 旧式
- **zFS** (z/OS File System): 新式、マルチユーザ並行アクセス対応
- 物理実体は VSAM LDS。USS から見ると `/u/user01/file.txt`、MVS から見ると `OMVS.USER01.ZFS` 等
- マウント: `BPXPRMxx` parmlib メンバで定義、または動的 `MOUNT FILESYSTEM(...) TYPE(ZFS) MOUNTPOINT(...)`

### プロセス・シェル
- USS シェル: `/bin/sh` (Korn Shell + extensions) と bash
- ユーザは RACF と OMVS segment（UID/GID）が両方必要
- TSO から `OMVS` コマンド、または ssh 直接

### MVS データセット連携
- USS から MVS DSN: `cat "//USER.PROD.PS"` 構文
- MVS から USS ファイル: JCL の `PATH=` 指定 (`//DD1 DD PATH='/u/x/file'`)
- **EBCDIC vs ASCII**: MVS は EBCDIC、USS も伝統 EBCDIC、しかし zFS の text タグ機能で per-file ASCII 可能
- file tag (chtag) で「このファイルは ISO8859-1」と OS に教えると、自動変換 enable

書籍 (BK_KORN_001 / BK_ZOS_TECH_002) 蒸留の mechanism 補強: USS のシェルは伝統的に **Korn シェル (ksh) 互換** を中核として位置付けられており、bash も導入できるが、z/OS native スクリプトは ksh で書く慣習が長い。これは z/OS の Job 投入や ISPF 連携で起動される自動スクリプトが、長年 ksh で書かれて運用に組み込まれているため。ksh のパラメータ展開 (`${var:-default}`, `${var##pattern}` 等) や `print -r` での raw 出力、`integer` 型変数などは bash と挙動が異なる場面があり、**Linux bash スクリプトをそのまま USS ksh に持ち込むと微妙に挙動が変わる**。プロジェクトのスクリプト言語標準を bash か ksh かで先に決めると、後の保守コストが下がる。

## 3. prerequisites（理解の前提）

- データセット概念（→ ZOS-DATASET-001）
- VSAM（→ ZOS-VSAM-001）— zFS/HFS 実体
- RACF（→ ZOS-RACF-001）— USS ユーザは OMVS segment 必須
- 一般 IT 知識: POSIX、Unix シェル、ファイル権限 (rwx)

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-DATASET-001, ZOS-VSAM-001, ZOS-RACF-001
- `specialized_by`: なし
- `contrasts_with`: ZOS-DATASET-001（POSIX vs MVS native）, ZOS-TSO-001
- `used_by`: なし（最終消費側）

## 5. pitfalls（実装・運用での落とし穴）

- **EBCDIC / ASCII 自動変換の罠**: USS のテキストファイルは伝統的 EBCDIC、しかし Java JAR / Python source / Git リポジトリは ASCII (UTF-8)。`chtag` 設定無しで `cat` するとバイナリ表示、`chtag -t -c ISO8859-1 file.py` で「これは ASCII text」と OS に教えれば自動変換 OK。**chtag 漏れで Java ビルドが意味不明エラー**は新人の通る道。
- **改行コード LF vs CRLF**: Linux 移植プロジェクトで Git pull したファイルが LF だったり CRLF だったり。USS は LF が標準だが、bash スクリプトの shebang (`#!/bin/sh`) が CRLF だと **`/bin/sh^M: not found`** で起動失敗、原因が見えない。`dos2unix` か `sed -i 's/\r$//'`。
- **OMVS segment 無しの RACF ID で USS ログイン不可**: TSO は使えるが USS には入れない。`ALTUSER USER01 OMVS(UID(1001) HOME('/u/user01') PROGRAM('/bin/sh'))` が必要。**「全社員に USS 開放」と決めて OMVS segment 一括追加**しないと現場で詰む。
- **zFS 容量自動拡張に上限**: zFS はデフォルト 4PB 拡張可だが、auto extension が設定されてないとフルでマウント時 IO エラー。**`AGGRGROW` パラメータで auto extension on**、設定漏れで深夜に zFS フルしてアプリ停止。
- **MVS DSN と USS path の混在 JCL**: 1 つの JCL で `DD DSN=USER.X` と `DD PATH='/u/x/y'` を両方使うのは可能だが、デバッグが地獄。**バッチ処理は MVS DSN で統一、USS 必要なら別ステップでファイル変換**が運用ルール。
- **USS でのプロセス TSO 同居**: TSO セッションから OMVS シェル入って `vi` 使うと、3270 端末上で表示が崩れる事案あり。**TSO 上 OMVS は緊急用**、本格的に使うなら ssh で z/OS につないで TERM=xterm。
- **HFS から zFS 移行漏れ**: 旧 HFS を放置するとサポート切れ + 性能劣化。`bpxwmigf` で移行可能だが、**移行前後でアクセス権ビットの扱いが微妙に変わる**事例あり、テスト環境で全アプリ動作確認必要。
- **APF 認可と USS sticky bit の混同 (BK_ZOS_TECH_002 蒸留)**: USS 実行ファイルに sticky bit (`chmod +t`) を立てると、その実行ファイルは APF authorized library 経由で動く扱いになる。これを知らずに通常のスクリプトに sticky bit を立てると **意図せずシステム権限で動作する** セキュリティリスク。`extattr +a` も同様。**APF 認可の意味を理解せずに sticky bit/extattr を扱わない** が原則。
- **fork() の性能劣化 (BK_MF_001 / BK_KORN_001 蒸留)**: USS の fork() は Linux と比べて重い (内部で BPXAS Initiator 起動が必要)。シェルスクリプトで `for` ループ内で `awk` や `sed` を呼ぶような書き方をすると、Linux と比べて 10-100 倍遅くなる事例あり。**fork-heavy なスクリプトは Linux→USS 移植時に書き直す必要**、awk/perl/python で 1 プロセス完結に変更するのが定石。
- **EBCDIC 配下の sort の崩壊**: USS の `sort` コマンドは EBCDIC 順で並べるが、これは ASCII 順と全く違う (数字より英字が先に来る等)。**Linux で動いた `sort | uniq` が USS で意図と違う順序になる**罠。`LC_ALL=C` 指定や `iconv` 経由で ASCII 化してから sort する回避策が必要。
- **autoconvert(yes) の意図せぬ副作用**: BPXPRMxx で `AUTOCVT(ALL)` を指定すると、tag 付きファイルが自動変換されるが、**バイナリファイルに誤って tag を付けた瞬間に破壊される**。Git pull したファイル群に一括で `chtag -R` するのは危険、テキストかバイナリかを分別してから tag を付ける。

## 6. examples（具体例）

```bash
# OMVS シェルから
$ pwd
/u/user01
$ ls -la
$ cat "//'USER.PROD.SALES'"

# chtag で text encoding 設定
$ chtag -t -c ISO8859-1 myscript.sh
$ chtag -p myscript.sh
t ISO8859-1   T=on  myscript.sh

# zFS マウント
$ mount -t zfs -o aggrgrow=yes -f OMVS.U.USER01.ZFS /u/user01
```

```jcl
//STEP01 EXEC PGM=BPXBATCH
//STDPARM DD *
SH /u/user01/myscript.sh arg1 arg2
//STDOUT  DD SYSOUT=*
//STDERR  DD SYSOUT=*
```

```parmlib
*  BPXPRMxx 例
   FILESYSTYPE TYPE(ZFS) ENTRYPOINT(IOEFSCM)
   MAXPROCSYS(2000)
   MAXPROCUSER(500)
   MAXFILEPROC(1000)
   ROOT FILESYSTEM('OMVS.ROOT.ZFS') TYPE(ZFS) MODE(RDWR)
   MOUNT FILESYSTEM('OMVS.ETC.ZFS')   TYPE(ZFS) MOUNTPOINT('/etc')
```

書籍 (BK_KORN_001) 蒸留の ksh パラメータ展開実例: USS 自動スクリプトで頻出するイディオム。Linux bash と動作差がある書き方を意識的に避けると保守性が上がる。

```bash
# デフォルト値展開 (ksh / bash 共通)
: ${LOG_DIR:=/u/ops/logs}

# 末尾拡張子削除 (ksh / bash 共通)
base=${file%.txt}

# CP / 改行コード判定をして処理分岐 (USS 特有)
typeset -i tag_count
tag_count=$(chtag -p "$file" | grep -c 'untagged')
if (( tag_count > 0 )); then
   chtag -t -c IBM-1047 "$file"
fi

# JCL から呼ばれる時は stdout を SYSPRINT に
print -r -- "PROCESS START $(date +%Y%m%d-%H%M%S)"
```

## 7. decision_axes（採否を分ける判断軸）

- **HFS vs zFS**: 新規は zFS 一択（HFS は IBM サポート停止予定）。既存 HFS は順次 zFS へ移行、移行コスト大だが避けられない。**「サポート切れた後で慌てる」のは最悪**、計画移行が原則。
- **USS vs MVS データセットで「データはどっちに置く」**: COBOL/PL/I バッチが扱うデータは MVS データセット。Java/Python/REST 系が扱うデータは USS ファイル。**両方使うシステムは ETL でデータ橋渡し**、混在をアプリ層で意識させない。
- **USS シェルで書くか REXX で書くか**: 自動化スクリプトを USS bash で書くか TSO REXX で書くか。**USS で OSS ツールを使う場合は bash**、TSO/MVS 操作中心なら REXX。
- **USS から MVS への移行 / 共存戦略**: モダン化の文脈で「全部 USS に寄せる」誘惑があるが、レガシー COBOL/CICS/IMS は MVS native のまま。**「橋渡し API + 双方共存」が現実解**、強引な統合は失敗事例多し。
- **chtag 自動化**: Git や Maven 経由で大量ソースを取り込む時、`autoconvert(yes)` 設定や `chtag -R` でディレクトリ全体に再帰タグ付けが必要。**プロジェクト初期に chtag 戦略を決める**、後付けはバグの温床。
- **OMVS segment 配布**: 全 RACF ユーザに UID/GID を発行する自動運用ジョブが必要。**社員番号 → UID 一意マッピング** + `BPX.NEXT.USER` プロファイル併用。


## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

本 atom の領域については、IBM 公式 manual を一次出典としつつ、運用事例や設計判断の補強として市販書籍 (BK_MF_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 等の z/OS / メインフレーム関連書籍) からの実装知識を補助的に参照する。逐語引用は禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
