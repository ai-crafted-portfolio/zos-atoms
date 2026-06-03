---
title: ZOS-IPCS-001
description: dump 解析セッション、CBFORMAT、SUMMARY FORMAT、TCBPRT、SUMMARY KEYFIELD
tags:
  - Recovery
  - Recovery-Workload
---
# ZOS-IPCS-001: IPCS (Interactive Problem Control System)

## 1. purpose（なぜ存在するか）

IPCS（Interactive Problem Control System）は z/OS のダンプ解析 **対話セッション環境**。ZOS-DUMP-001 で採取された SVC dump / SYSMDUMP / Stand-alone dump（数百 MB 〜 数 GB のバイナリ）を読み込み、TCB ツリー・PSW・コントロールブロック・モジュール所属・recovery ログを subcommand で掘り下げる。ダンプ解析の **事実上唯一の正規ツール**。

Linux なら `gdb` + `crash`、Windows なら `WinDbg`、AIX なら `dbx` が対応するが、IPCS の特徴は (a) **dump dataset directory** という IPCS 自身が管理する dump カタログがあり、複数 dump を tag 付き管理できる、(b) **CBFORMAT** で z/OS のコントロールブロック（ASCB / TCB / RB / WEB / SDWA 等）を **名前解決して構造表示** できる（生 hex を読まずに済む）、(c) **VERBX exit routine** で subsystem 専用解析（VERBX MTRACE / VERBX LOGDATA / VERBX CTRACE）を呼べる拡張機構、の 3 点。

IPCS なしで dump.bin を `od` 相当で読むのは現実的に不可能。これは MVS の OS 内部構造が **命名付き Mapping Macro**（IHA*, IEZ*, IRA* 等）で公開されており、IPCS がそれを使って構造化表示する設計に由来する。Linux の `crash` も似た方式（kernel debug info ベース）だが、ダンプ管理 directory・対話 subcommand 体系・VERBX 拡張は IPCS 独自。

## 2. mechanism（どう動くか）

### セッション構造
- TSO 配下の対話セッション（`IPCS` コマンドで起動）または batch（`IKJEFT01` PGM 内 `IPCS NOPARM` + SYSIN）。
- **dump directory dataset**（IPCS profile で `IPCSDDIR` DD として割当て、`SETDEF DSNAME(...) NOCONFIRM` で active 化）に解析中ダンプを登録する。`DSNAME('USER.MYPROG.DUMP')` で読込・解析、addsel で別名 tag。

### 主要 subcommand
- **STATUS 系**: `STATUS REGS`（レジスタ）、`STATUS CPU`（PSW + CPU 状態）、`STATUS FAILDATA`（abend code / module / PSW @ failure summary）、`STATUS SYSTEM`（system 全体 summary）
- **SUMMARY 系**: `SUMMARY FORMAT`（全 TCB ツリー + RB chain）、`SUMMARY KEYFIELD`（指定 KEY フィールドで sort）、`SUMMARY REGISTERS`（TCB 毎の register dump）
- **CBFORMAT**: `CBFORMAT addr STRUCTURE(ASCB)` で ASCB を structured 表示。`CBSTAT addr STRUCTURE(TCB)` で要約。
- **LIST / FIND**: `LIST addr LENGTH(n)`（生 hex）、`FIND 'string' RANGE(...)`（hex / EBCDIC 検索）
- **WHERE**: アドレスからモジュール名解決（load map / SMF 30 / CSVQUERY）
- **VERBX**: subsystem 専用 exit。`VERBX LOGDATA`（logrec record トレース）、`VERBX MTRACE`（master trace）、`VERBX CTRACE COMP(SYSXCF)`（component trace）、`VERBX TRACE`（GTF trace）
- **IP RUNCHAIN**: `IP RUNCHAIN ASID(x'00A1')` で全 RB / TCB ウォーク

### Stand-alone dump (SADUMP) 特殊
- HMC から `STAND ALONE DUMP` で IPL 不能 / disabled wait 時に採取（OS 死亡時の最終手段）。
- 物理 DASD の dump dataset に書く（`AMDSADMP` で事前 dataset 作成）。
- IPCS で開く時は `IPCS BROWSE DSNAME('SADUMP.D20260601')` + `EVALDUMP`。**SVC dump と異なり「LPAR 全体」のスナップショット** なので CSA/SQA 含む全 system 領域が見える。

### Mapping Macro 解決経路
- IPCS は SYS1.MIGLIB / SYS1.MACLIB の **mapping macro**（IHAPSA, IHAASCB, IHATCB, ...）と SDWA dataset の load map から構造定義を取得。
- 古い z/OS リリースの dump を新リリース IPCS で開くと **mapping macro layout が違う** 場合があり、`CBFORMAT` が誤読する。**dump 採取 release と同 release の IPCS** が原則。

## 3. prerequisites（理解の前提）

- ダンプ採取の種別と仕組み — `ZOS-DUMP-001`
- ASCB / TCB / RB 等のアドレス空間制御ブロック構造（ZOS-ASCB-001 は Tier α 起案中、未完なら一般 IT 知識として TCB ≒ Linux task_struct と読替え可）
- TSO セッション操作 — `ZOS-TSO-001`
- データセット概念 — `ZOS-DATASET-001`
- 一般 IT 知識: hex dump 読解、レジスタ・PSW、スタックトレース概念

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-DUMP-001, ZOS-TSO-001, ZOS-DATASET-001
- `specialized_by`: なし（IPCS は単一ツール、subcommand で機能分岐）
- `contrasts_with`: Linux gdb + crash + addr2line, Windows WinDbg + symbol server, AIX dbx
- `used_by`: ZOS-CICS-001（CICS transaction dump 解析）, ZOS-IMS-001（IMS region dump 解析）, ZOS-DB2-001（DSNWDMP 経由の Db2 dump 解析）, ZOS-WAITSTATE-001（disabled wait + stand-alone dump 解析）

## 5. pitfalls（実装・運用での落とし穴）

- **dump directory 未設定で BLS18028I**: 新規 TSO ID で `IPCS` 起動して即 `DSNAME('USER.DUMP')` すると `BLS18028I I/O error on dump directory` で死亡。**IPCS 初回利用は `IPCS NOPARM` + `SETDEF DSNAME(...) NOCONFIRM` で directory 作成 + active 化、profile ALLOC で IPCSDDIR DD 永続化** が必須。組織で IPCS directory dataset 命名規則（`useridid.DDIR` 等）を決めて新人配布する SOP がない現場では初回 30 分が drown する。
- **WHERE がモジュール解決失敗で「Unresolved」連発**: ロードモジュールのリンクマップ（Linkage Editor SYSPRINT）と SMF 30 の MODULE LOAD レコードが揃ってないと、IPCS の `WHERE 8C0040` が "Unresolved" を返す。**load library 更新時にリンクマップを保存** + **CSVQUERY / LPA map の dump 採取時点スナップショット保存** が運用 SOP。これを怠った組織は半年後 dump 開いて「アドレス 8C0040 のモジュールは何か」が永久に分からない。
- **SUMMARY FORMAT 既定で重要 area 抜け**: `SUMMARY FORMAT` を引数なしで打つと **TCB ツリーは出るが SDWA / RTM2WA / WEB / SRB の詳細が出ない**。「ABEND した task は分かったが、recovery routine が何をやったか分からない」状態。**`SUMMARY FORMAT TCBERROR ALL` または `IP SUMM FORMAT JOBNAME(MYJOB) ALL`** で全領域明示が必須。
- **IPCS session 永続化忘れで profile 失う**: 解析途中で TSO logoff すると **dump directory の active 設定が消える**。次回 IPCS 起動で `STATUS FAILDATA` を打つと別 dump（前回 active のまま残ったもの）を見て嵌る。**`PROFILE` データセットで IPCSDDIR DD を永続化 + IPCS profile で `SETDEF` 自動実行** が SOP。
- **release mismatch で CBFORMAT が誤読**: z/OS 2.4 で採取した dump を z/OS 2.5 IPCS で開く（または逆）と、ASCB / TCB の field offset が違っていて `CBFORMAT addr STRUCTURE(ASCB)` が **正常表示に見えて値が全部ズレてる** 事故。検出が極めて困難（IPCS は warning を出さない）。**dump 採取時点の z/OS release を 必ず STATUS SYSTEM で確認 → 同 release の IPCS load library を使う**。
- **VERBX LOGDATA で logrec が空**: `VERBX LOGDATA` を打って「records found: 0」だと「障害無し」と誤解する人が多い。実際は **SVC dump の SDATA に logrec が含まれてない**（CHNGDUMP で SDATA から TRT/LOGREC が除外されていた）だけ。**logrec は別途 `IFCEREP1` または `OPERLOG` 経由で取得**、SVC dump の VERBX LOGDATA は補助。
- **batch IPCS の SYSIN 終了忘れ**: batch IPCS（IKJEFT01 経由）で SYSIN に subcommand を流すとき、最終行に `END` を入れ忘れると **IPCS が SYSIN 待ちのまま hang**、JCL が wait state（実際は input EOF 待ち）。**SYSIN 最終行は END で明示**。

## 6. examples（具体例）

```text
* TSO 対話 IPCS セッション起動 (初回)
TSO IPCS NOPARM
  SETDEF DSNAME('USER.DUMP.D20260602') NOCONFIRM
  STATUS SYSTEM
  STATUS FAILDATA
  STATUS REGS
  SUMMARY FORMAT JOBNAME(MYJOB) ALL
  WHERE 8C0040
  CBFORMAT 7F8E40 STRUCTURE(ASCB)
  IP RUNCHAIN ASID(X'00A1')
  VERBX LOGDATA
  END
```

```jcl
//* batch IPCS で dump 自動 summary (夜間 cron 用)
//IPCS    EXEC PGM=IKJEFT01,REGION=0M,DYNAMNBR=200
//IPCSDDIR DD DSN=OPS.IPCS.DDIR,DISP=SHR
//IPCSPRNT DD SYSOUT=*
//SYSPRINT DD SYSOUT=*
//SYSTSPRT DD SYSOUT=*
//SYSTSIN  DD *
  IPCS NOPARM
  SETDEF DSNAME('USER.DUMP.D20260602') NOCONFIRM
  STATUS FAILDATA
  SUMMARY FORMAT ALL
  END
/*
```

```text
* Stand-alone dump 解析 (HMC から SADUMP 採取 → IPCS で開く)
IPCS
  DSNAME('SADUMP.MVS01.D20260602')
  EVALDUMP
  STATUS SYSTEM
  STATUS WORKSHEET
  IP CBFORMAT 0 STRUCTURE(PSA)
  VERBX MTRACE
```

## 7. decision_axes（採否を分ける判断軸）

- **対話 (TSO) vs batch IPCS**: 障害発生直後の初動解析は **TSO 対話**（subcommand を手で打って掘る）、定型サマリ生成は **batch IPCS**（JCL に固定 subcommand 列）。**夜間障害監視で「STATUS FAILDATA + SUMMARY FORMAT + VERBX LOGDATA」を自動 SYSOUT 出力する batch IPCS 設定がある組織 vs ない組織** で初動の質が変わる。
- **SVC dump vs Stand-alone dump (SADUMP) の使い分け**: 個別 address space 障害は **SVC dump + IPCS**（DSDUMP COMM 経由）、LPAR 全体 disabled wait / hang は **SADUMP**（HMC から）。**「SVC dump で済むのに SADUMP 採る」運用は LPAR 停止時間 30〜60 分の loss、「SADUMP すべきなのに SVC dump で誤魔化す」運用は OS 内部状態が見えず根本原因不明** の二重リスク。
- **CBFORMAT 多用 vs LIST hex 直読**: `CBFORMAT STRUCTURE(...)` は構造化されて読みやすいが、release mismatch で誤読リスク。`LIST addr LENGTH(n)` は生 hex で確実だが mapping macro 知識が必要。**経験浅い解析者は CBFORMAT、ベテランは LIST + 自前 IHAMacro 参照** の住み分け。
- **IPCS dump directory 共有 vs 個人別**: チーム共有 directory なら過去事案再現がしやすいが、ファイル競合（add/delete 衝突）リスク。個人別なら独立だが過去事案にアクセス不可。**現代の標準: 個人 directory で解析、確定 dump は共有 archive directory に登録**。
- **mapping macro 自前管理 vs IBM 提供**: 古い z/OS release の dump 解析用に **当時の mapping macro library を保管** するか、最新だけ持つか。**長期保管要件（監査 / レビュー）がある組織は mapping macro library を release 毎に archive 必須**、これを怠ると 3 年前 dump が「読めるが意味が分からない」状態になる。
