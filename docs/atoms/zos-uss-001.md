---
id: ZOS-USS-001
title: UNIX System Services（HFS / zFS）
status: stable
last_reviewed: 2026-05-09
---


# ZOS-USS-001: UNIX System Services

## 1. purpose（なぜ存在するか）

USS（UNIX System Services、旧名 OpenEdition MVS）は **z/OS 内蔵の POSIX 互換 UNIX サブシステム**。z/OS の伝統的な MVS データセット世界（→ [ZOS-DATASET-001](zos-dataset-001.md)）の **隣に**、Linux/Unix 風のファイルシステム + シェル + 標準 C ランタイムを並列稼動させる。

なぜ必要か:
1. **オープンソース移植**: Java / Python / Apache HTTP / OpenSSH / Git 等を z/OS に動かしたいが、これらは POSIX 前提で書かれてる。USS が無いと動かない
2. **TCP/IP / Web サーバ**: HTTP サーバ、SFTP、cron 系処理は USS で動かす
3. **DevOps / モダン開発**: Git, Maven, Gradle, Liberty Profile 等
4. **z/OS UNIX シェル経由のスクリプト**: bash 風の自動化を z/OS 上で

「z/OS 内に Linux サブシステムが同居」という構図。**MVS データセットと USS ファイルは別物だが、相互参照可能**。

Linux/Windows と何が違うか:
- Linux: ファイルシステムが OS の中心、UNIX 唯一
- z/OS: MVS データセット（中心） + USS ファイル（別系統）の 2 系統、共存。**「どっち使うか」を毎回考える設計**

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

## 3. prerequisites（理解の前提）

- データセット概念（→ [ZOS-DATASET-001](zos-dataset-001.md)）
- VSAM（→ [ZOS-VSAM-001](zos-vsam-001.md)）— zFS/HFS 実体
- RACF（→ [ZOS-RACF-001](zos-racf-001.md)）— USS ユーザは OMVS segment 必須
- 一般 IT 知識: POSIX、Unix シェル、ファイル権限 (rwx)

## 4. relations（他アトムとの繋がり）

- `depends_on`: [ZOS-DATASET-001](zos-dataset-001.md), [ZOS-VSAM-001](zos-vsam-001.md), [ZOS-RACF-001](zos-racf-001.md)
- `specialized_by`: なし
- `contrasts_with`: [ZOS-DATASET-001](zos-dataset-001.md)（POSIX vs MVS native）, [ZOS-TSO-001](zos-tso-001.md)
- `used_by`: なし（最終消費側）

## 5. pitfalls（実装・運用での落とし穴）

- **EBCDIC / ASCII 自動変換の罠**: USS のテキストファイルは伝統的 EBCDIC、しかし Java JAR / Python source / Git リポジトリは ASCII (UTF-8)。`chtag` 設定無しで `cat` するとバイナリ表示、`chtag -t -c ISO8859-1 file.py` で「これは ASCII text」と OS に教えれば自動変換 OK。**chtag 漏れで Java ビルドが意味不明エラー**は新人の通る道。
- **改行コード LF vs CRLF**: Linux 移植プロジェクトで Git pull したファイルが LF だったり CRLF だったり。USS は LF が標準だが、bash スクリプトの shebang (`#!/bin/sh`) が CRLF だと **`/bin/sh^M: not found`** で起動失敗、原因が見えない。`dos2unix` か `sed -i 's/\r$//'`。
- **OMVS segment 無しの RACF ID で USS ログイン不可**: TSO は使えるが USS には入れない。`ALTUSER USER01 OMVS(UID(1001) HOME('/u/user01') PROGRAM('/bin/sh'))` が必要。**「全社員に USS 開放」と決めて OMVS segment 一括追加**しないと現場で詰む。
- **zFS 容量自動拡張に上限**: zFS はデフォルト 4PB 拡張可だが、auto extension が設定されてないとフルでマウント時 IO エラー。**`AGGRGROW` パラメータで auto extension on**、設定漏れで深夜に zFS フルしてアプリ停止。
- **MVS DSN と USS path の混在 JCL**: 1 つの JCL で `DD DSN=USER.X` と `DD PATH='/u/x/y'` を両方使うのは可能だが、デバッグが地獄。**バッチ処理は MVS DSN で統一、USS 必要なら別ステップでファイル変換**が運用ルール。
- **USS でのプロセス TSO 同居**: TSO セッションから OMVS シェル入って `vi` 使うと、3270 端末上で表示が崩れる事案あり。**TSO 上 OMVS は緊急用**、本格的に使うなら ssh で z/OS につないで TERM=xterm。
- **HFS から zFS 移行漏れ**: 旧 HFS を放置するとサポート切れ + 性能劣化。`bpxwmigf` で移行可能だが、**移行前後でアクセス権ビットの扱いが微妙に変わる**事例あり、テスト環境で全アプリ動作確認必要。

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

## 7. decision_axes（採否を分ける判断軸）

- **HFS vs zFS**: 新規は zFS 一択（HFS は IBM サポート停止予定）。既存 HFS は順次 zFS へ移行、移行コスト大だが避けられない。**「サポート切れた後で慌てる」のは最悪**、計画移行が原則。
- **USS vs MVS データセットで「データはどっちに置く」**: COBOL/PL/I バッチが扱うデータは MVS データセット。Java/Python/REST 系が扱うデータは USS ファイル。**両方使うシステムは ETL でデータ橋渡し**、混在をアプリ層で意識させない。
- **USS シェルで書くか REXX で書くか**: 自動化スクリプトを USS bash で書くか TSO REXX で書くか。**USS で OSS ツールを使う場合は bash**、TSO/MVS 操作中心なら REXX。
- **USS から MVS への移行 / 共存戦略**: モダン化の文脈で「全部 USS に寄せる」誘惑があるが、レガシー COBOL/CICS/IMS は MVS native のまま。**「橋渡し API + 双方共存」が現実解**、強引な統合は失敗事例多し。
- **chtag 自動化**: Git や Maven 経由で大量ソースを取り込む時、`autoconvert(yes)` 設定や `chtag -R` でディレクトリ全体に再帰タグ付けが必要。**プロジェクト初期に chtag 戦略を決める**、後付けはバグの温床。
- **OMVS segment 配布**: 全 RACF ユーザに UID/GID を発行する自動運用ジョブが必要。**社員番号 → UID 一意マッピング** + `BPX.NEXT.USER` プロファイル併用。
