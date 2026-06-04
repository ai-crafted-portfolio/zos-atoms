---
id: ZOS-DATASET-001
title: データセット
status: stable
last_reviewed: 2026-05-09
authors: [agent]
rag_verified: true
---

# ZOS-DATASET-001: データセット

## 1. purpose（なぜ存在するか）

z/OS では「ファイル」ではなく「データセット」を扱う。これは **メインフレームが入出力性能を最大化するために、ストレージを物理的なブロック単位で管理し、アクセス方式（順次・直接・索引）を OS レベルで明示する設計を取った結果**。Windows / Linux のような「全部バイトストリーム、解釈はアプリ任せ」と真逆の哲学。だから「データセット」という別名詞が要る。

別の言い方をすると、Linux では `cat /etc/passwd` も `cat /var/log/messages` も同じ「バイト列」として扱える（解釈は read 側）が、z/OS では「これは固定長 80 バイト × 順次」「これはキー長 12 のキー付き索引」と OS にタグを貼ってアロケートする。アプリ起動時に OS は当該タグを読み、アクセスメソッド（QSAM, BSAM, VSAM, BPAM 等）を bind する。**型の遅延束縛ではなく早期束縛**。

この哲学のメリットは I/O 効率（ブロック整数倍で割り当てるためチャネルが暴走しない）。デメリットは柔軟性低下（後から RECFM を変えるには REPRO/COPY で別データセット作るしか無い）。

書籍 (BK_MF_001 / BK_ZOS_BASIC_001) 蒸留の補強観点として、データセットの設計時点では **「アクセス形態を物理レイアウトに固定する」** という前提を理解しておく。Linux で言うと「ファイル作成時に B-tree か LSM か Heap かを宣言してから write を始める」ようなもので、後から検索パターンが変わっても物理構造は容易に変えられない。アプリ寿命 20-40 年を前提とする業務システムでは、この「最初の選択を間違えると一生引きずる」性質を踏まえて、想定アクセスパターンを丁寧に洗い出してから DSORG/RECFM を決める文化がある。

## 2. mechanism（どう動くか）

- DASD（直接アクセス記憶装置）上に **トラック / シリンダ / ボリューム** 単位でアロケート（→ ZOS-DASD-001）
- 各データセットには **DSORG**（編成種別: PS=順次, PO=区分, VS=VSAM, DA=直接 等）と **RECFM**（レコード形式: F/V/U + B/A）が金属プレートのように固定で付く
- アプリが `OPEN` する時、OS はカタログ参照（→ ZOS-CATALOG-001）→ ボリューム特定 → DEB（Data Extent Block）構築 → アクセス方式の I/O ルーチンを bind
- ファイル名（DSN）は **44 文字制限** + ドット階層（例: `USER.PROD.DATA`）。各レベル 1〜8 文字、英数字 + `@#$`、先頭文字制限あり
- 実体は VTOC（Volume Table Of Contents）に format-1 DSCB として登録される
- 「カタログされた」状態とは、ICF カタログにエントリがあり、DSN だけで OS がボリューム名を引けること。逆は `VOL=SER=xxx` 指定が必要

書籍 (BK_ZOS_TECH_001) 蒸留での追加 mechanism: BLKSIZE は物理 I/O 効率に直結し、**1 トラック (CKD で約 56KB) の整数分数を意識した値が伝統的に選ばれてきた** (27920 = 半トラック、4096 = 4KB block 等)。System Determined Blocksize の機能が出てからは多くの新規データセットで意識不要になったが、特定ツールが BLKSIZE を bind 時点でハードコードしている事例があり、**「自動だから安全」と思い込むと特定ステップだけ性能異常になる**。物理層を完全に隠蔽できないのが z/OS データセット設計の特徴。

## 3. prerequisites（理解の前提）

- DASD の物理構造（CKD = Count-Key-Data フォーマット） — `ZOS-DASD-001`
- カタログの 2 層構造（マスター + ユーザカタログ） — `ZOS-CATALOG-001`
- TSO/JCL での DSN 指定方法
- 一般 IT 知識: ストレージのブロック概念、ファイル名空間

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-DASD-001, ZOS-CATALOG-001
- `specialized_by`: ZOS-PDS-001, ZOS-VSAM-001, ZOS-GDG-001
- `contrasts_with`: ZOS-USS-001（POSIX ファイルとの対比）, （未作成）LINUX-FILE-001
- `used_by`: ZOS-JCL-001 (DD), ZOS-RACF-001 (保護対象), ZOS-SMF-001 (出力先), ZOS-SMS-001 (ストレージポリシ), ZOS-RECOVERY-001 (HSM/dss), ZOS-SORT-001 (ソート対象), ZOS-DUMP-001 (DSN= 出力先)

## 5. pitfalls（実装・運用での落とし穴）

- **DSORG 不一致で OPEN 失敗**: アプリが PS 想定で書いてるのに JCL で PO を渡すと `IEC141I 013-20` ABEND。多くの初心者が引き継ぎ JCL の修正で踏む頻発エラー。原因究明には JOBLOG の IEC141I の reason code（02/0C/14/20 等）を見る必要あり。
- **拡張限界 (EAS/EAV)**: 古いデータセットは 65,535 トラック上限。Extended Address Space 未対応プログラムは EAV ボリューム（54GB 超）で `IGD308I 17 06` ABEND。古い ENTERPRISE COBOL（V3 以前）でビルドされた load module が引っかかる。再 BIND 必要。
- **共有違反**: `DISP=SHR` で書いてはいけないのに書く → 破損。`DISP=OLD` を恒常的に使うと、別ジョブと同時実行になった瞬間 `SE37` か待ち合いで dead lock。
- **44 文字制限を忘れる**: ジョブ自動生成系で DSN を組み立てる時、prefix 拡張で 44 文字超えてジョブが ABEND `IEFC005I PROCEDURE (DSN OVER 44 CHARACTERS)`。HLQ.MID.PROD.SUBSYS.DAILY.YYYYMMDD.DETAIL 等やるとすぐ枯れる。
- **RECFM=U（不定長）の罠**: load module / object module 等以外で U を使うと後段ツール（DFSORT, ICETOOL, IDCAMS REPRO）がほぼ全滅。テキストデータで U を使う初心者の誘惑があるが絶対やらせない。
- **未カタログ DSN の幽霊化**: `DISP=(NEW,KEEP)` で作ったがカタログしてないデータセットを忘れる事例。VTOC には残るがカタログに無いので `LISTCAT` で見つからず、容量だけ食い続ける。年に 1 回 VTOC 全件 vs カタログ全件の差分洗い出しが必要。
- **SPACE の primary 大きすぎで割り当て失敗 (BK_MF_001 蒸留)**: `SPACE=(CYL,(500,50))` のように primary を過大に取ると、ボリューム上に連続空き領域が無くて `IEF257I` で割当失敗。「リスクヘッジで大きめに」がかえって悪手になるケース。**primary は実必要量の 1.2〜1.5 倍、secondary を多めに取って 2 次拡張に任せる設計**が安全。
- **DSN HLQ と RACF プロファイルの不整合**: 新規 DSN の HLQ がどの RACF generic profile にも引っかからない場合、UACC(NONE) ではなく **「保護無し」** という最悪状態になる事例。SETROPTS PROTECTALL(WARNING|FAILURES) を入れる運用が一般的だが、長寿サイトで設定がブレている事もあり、新規 HLQ 作る時は RACF プロファイル整備を同時実施が原則。
- **RLSE 指定漏れで巨大な空き領域がそのまま残る**: `SPACE=(...,RLSE)` を付け忘れると、ジョブ終了後も未使用領域がデータセットに張り付いたまま。DASD 利用率レポートで「使ってないのに大きい DSN」が積み上がる主因。月次の HSM ML2 移送や IDCAMS DEFINE 時の見直しで RLSE を入れる SOP が必要。

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

書籍 (BK_MF_001) 蒸留の実例: 本番運用での DSN 命名規約は、HLQ から末尾まで「環境 / システム / サブシステム / 業務 / 種別 / 世代」の階層に意味を持たせる慣習が定着している。例えば `PROD.SALES.DLY.AGGR.OUT.G0050V00` のように、ジョブ ID や役割がレベルで読み取れる構造。命名規約を最初に固めると、その後の RACF generic profile、HSM 移送ルール、SMS データクラス割当が全部効率化される。逆に **HLQ 設計を後回しにしてアドホックに命名すると、3 年後に運用ルール整備で苦労する**。

## 7. decision_axes（採否を分ける判断軸）

- **PS vs PDS vs VSAM**: 単一ファイル更新なら PS（オーバーヘッド最小、ツール対応が一番厚い）。複数小ファイルをまとめたい・メンバ単位 BIND したい場合 PDS(E)（だが圧縮再編成コストあり、PDSE は並行更新可だが旧プログラム互換性で躓く）。検索性能要件があるなら VSAM（だが CISIZE/CASIZE のチューニング知識必須、初期構築コスト大、ツールの一部が VSAM 非対応）。RDB ならそもそも Db2。
- **古典 PDS vs PDSE**: PDSE は圧縮再編成不要・並行更新可・ロードモジュールはほぼ PDSE 一択。だが **古いユーティリティが PDSE で誤動作**（IEBUPDTE 等）するため、長寿サイトで完全移行できない事例あり。新規は PDSE、既存は移行コストとリスクで判定。
- **DSORG=PS で BLKSIZE 自動 vs 明示**: System Determined Blocksize（BLKSIZE=0）は安全だが、特定ツールが「BLKSIZE が 0 以外の特定値」を期待するケースあり（古い C 言語ランタイム等）。ツール側の前提を読む必要あり、自動が常に正解ではない。
- **SMS 管理 vs 非管理**: SMS 配下なら DATACLAS / STORCLAS / MGMTCLAS で集中管理可、ボリューム指定不要。だが SMS ACS ルーチン設計次第で意図しないボリュームに落ちる事故あり。非管理だと VOL=SER=xxx を JCL で都度指定、規模が大きくなると地獄。新規サイトはほぼ SMS 必須。


## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

本 atom の領域については、IBM 公式 manual を一次出典としつつ、運用事例や設計判断の補強として市販書籍 (BK_MF_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 等の z/OS / メインフレーム関連書籍) からの実装知識を補助的に参照する。逐語引用は禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
