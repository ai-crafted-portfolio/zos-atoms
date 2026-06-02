---
id: ZOS-DATASET-001
title: データセット
status: stable
last_reviewed: 2026-05-09
---


# ZOS-DATASET-001: データセット

## 1. purpose（なぜ存在するか）

z/OS では「ファイル」ではなく「データセット」を扱う。これは **メインフレームが入出力性能を最大化するために、ストレージを物理的なブロック単位で管理し、アクセス方式（順次・直接・索引）を OS レベルで明示する設計を取った結果**。Windows / Linux のような「全部バイトストリーム、解釈はアプリ任せ」と真逆の哲学。だから「データセット」という別名詞が要る。

別の言い方をすると、Linux では `cat /etc/passwd` も `cat /var/log/messages` も同じ「バイト列」として扱える（解釈は read 側）が、z/OS では「これは固定長 80 バイト × 順次」「これはキー長 12 のキー付き索引」と OS にタグを貼ってアロケートする。アプリ起動時に OS は当該タグを読み、アクセスメソッド（QSAM, BSAM, VSAM, BPAM 等）を bind する。**型の遅延束縛ではなく早期束縛**。

この哲学のメリットは I/O 効率（ブロック整数倍で割り当てるためチャネルが暴走しない）。デメリットは柔軟性低下（後から RECFM を変えるには REPRO/COPY で別データセット作るしか無い）。

## 2. mechanism（どう動くか）

- DASD（直接アクセス記憶装置）上に **トラック / シリンダ / ボリューム** 単位でアロケート（→ [ZOS-DASD-001](zos-dasd-001.md)）
- 各データセットには **DSORG**（編成種別: PS=順次, PO=区分, VS=VSAM, DA=直接 等）と **RECFM**（レコード形式: F/V/U + B/A）が金属プレートのように固定で付く
- アプリが `OPEN` する時、OS はカタログ参照（→ [ZOS-CATALOG-001](zos-catalog-001.md)）→ ボリューム特定 → DEB（Data Extent Block）構築 → アクセス方式の I/O ルーチンを bind
- ファイル名（DSN）は **44 文字制限** + ドット階層（例: `USER.PROD.DATA`）。各レベル 1〜8 文字、英数字 + `@#$`、先頭文字制限あり
- 実体は VTOC（Volume Table Of Contents）に format-1 DSCB として登録される
- 「カタログされた」状態とは、ICF カタログにエントリがあり、DSN だけで OS がボリューム名を引けること。逆は `VOL=SER=xxx` 指定が必要

## 3. prerequisites（理解の前提）

- DASD の物理構造（CKD = Count-Key-Data フォーマット） — [ZOS-DASD-001](zos-dasd-001.md)
- カタログの 2 層構造（マスター + ユーザカタログ） — [ZOS-CATALOG-001](zos-catalog-001.md)
- TSO/JCL での DSN 指定方法
- 一般 IT 知識: ストレージのブロック概念、ファイル名空間

## 4. relations（他アトムとの繋がり）

- `depends_on`: [ZOS-DASD-001](zos-dasd-001.md), [ZOS-CATALOG-001](zos-catalog-001.md)
- `specialized_by`: [ZOS-PDS-001](zos-pds-001.md), [ZOS-VSAM-001](zos-vsam-001.md), [ZOS-GDG-001](zos-gdg-001.md)
- `contrasts_with`: [ZOS-USS-001](zos-uss-001.md)（POSIX ファイルとの対比）, （未作成）LINUX-FILE-001
- `used_by`: [ZOS-JCL-001](zos-jcl-001.md) (DD), [ZOS-RACF-001](zos-racf-001.md) (保護対象), [ZOS-SMF-001](zos-smf-001.md) (出力先), [ZOS-SMS-001](zos-sms-001.md) (ストレージポリシ), [ZOS-RECOVERY-001](zos-recovery-001.md) (HSM/dss), [ZOS-SORT-001](zos-sort-001.md) (ソート対象), [ZOS-DUMP-001](zos-dump-001.md) (DSN= 出力先)

## 5. pitfalls（実装・運用での落とし穴）

- **DSORG 不一致で OPEN 失敗**: アプリが PS 想定で書いてるのに JCL で PO を渡すと `IEC141I 013-20` ABEND。多くの初心者が引き継ぎ JCL の修正で踏む頻発エラー。原因究明には JOBLOG の IEC141I の reason code（02/0C/14/20 等）を見る必要あり。
- **拡張限界 (EAS/EAV)**: 古いデータセットは 65,535 トラック上限。Extended Address Space 未対応プログラムは EAV ボリューム（54GB 超）で `IGD308I 17 06` ABEND。古い ENTERPRISE COBOL（V3 以前）でビルドされた load module が引っかかる。再 BIND 必要。
- **共有違反**: `DISP=SHR` で書いてはいけないのに書く → 破損。`DISP=OLD` を恒常的に使うと、別ジョブと同時実行になった瞬間 `SE37` か待ち合いで dead lock。
- **44 文字制限を忘れる**: ジョブ自動生成系で DSN を組み立てる時、prefix 拡張で 44 文字超えてジョブが ABEND `IEFC005I PROCEDURE (DSN OVER 44 CHARACTERS)`。HLQ.MID.PROD.SUBSYS.DAILY.YYYYMMDD.DETAIL 等やるとすぐ枯れる。
- **RECFM=U（不定長）の罠**: load module / object module 等以外で U を使うと後段ツール（DFSORT, ICETOOL, IDCAMS REPRO）がほぼ全滅。テキストデータで U を使う初心者の誘惑があるが絶対やらせない。
- **未カタログ DSN の幽霊化**: `DISP=(NEW,KEEP)` で作ったがカタログしてないデータセットを忘れる事例。VTOC には残るがカタログに無いので `LISTCAT` で見つからず、容量だけ食い続ける。年に 1 回 VTOC 全件 vs カタログ全件の差分洗い出しが必要。

## 6. examples（具体例）

```jcl
//OUTDD DD DSN=USER.PROD.SALES,DISP=(NEW,CATLG,DELETE),
//      DCB=(DSORG=PS,RECFM=FB,LRECL=80,BLKSIZE=27920),
//      SPACE=(CYL,(10,5),RLSE),UNIT=SYSDA
```

- `DSN=...`: 44 文字以内必須
- `DISP=(NEW,CATLG,DELETE)`: 新規作成、正常終了でカタログ登録、異常終了で削除
- `DCB=...`: 編成 PS / 固定長ブロック / レコード長 80 / ブロック長 27920（半トラック整数倍）
- `SPACE=(CYL,(10,5),RLSE)`: 1 次 10 シリンダ + 2 次 5 シリンダ × 15 回拡張可
- `UNIT=SYSDA`: ストレージグループ汎用 DASD

```jcl
//* PDS 既存メンバを参照
//INDD  DD DSN=USER.PROD.PROCLIB(MYJOB),DISP=SHR
```

## 7. decision_axes（採否を分ける判断軸）

- **PS vs PDS vs VSAM**: 単一ファイル更新なら PS（オーバーヘッド最小、ツール対応が一番厚い）。複数小ファイルをまとめたい・メンバ単位 BIND したい場合 PDS(E)（だが圧縮再編成コストあり、PDSE は並行更新可だが旧プログラム互換性で躓く）。検索性能要件があるなら VSAM（だが CISIZE/CASIZE のチューニング知識必須、初期構築コスト大、ツールの一部が VSAM 非対応）。RDB ならそもそも Db2。
- **古典 PDS vs PDSE**: PDSE は圧縮再編成不要・並行更新可・ロードモジュールはほぼ PDSE 一択。だが **古いユーティリティが PDSE で誤動作**（IEBUPDTE 等）するため、長寿サイトで完全移行できない事例あり。新規は PDSE、既存は移行コストとリスクで判定。
- **DSORG=PS で BLKSIZE 自動 vs 明示**: System Determined Blocksize（BLKSIZE=0）は安全だが、特定ツールが「BLKSIZE が 0 以外の特定値」を期待するケースあり（古い C 言語ランタイム等）。ツール側の前提を読む必要あり、自動が常に正解ではない。
- **SMS 管理 vs 非管理**: SMS 配下なら DATACLAS / STORCLAS / MGMTCLAS で集中管理可、ボリューム指定不要。だが SMS ACS ルーチン設計次第で意図しないボリュームに落ちる事故あり。非管理だと VOL=SER=xxx を JCL で都度指定、規模が大きくなると地獄。新規サイトはほぼ SMS 必須。
