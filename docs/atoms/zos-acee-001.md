---
title: ZOS-ACEE-001
description: ACEE 構造、SAF 認可検査経路、Surrogate / SUBMIT BY、TSO submit と batch ID 違い
tags:
  - Security
  - Security-Network
---
# ZOS-ACEE-001: ACEE / Address Space Identity

## 1. purpose（なぜ存在するか）

ACEE (Accessor Environment Element) は **「今、この address space は誰として動いているのか」を表現する 1 個の control block**。RACF / SAF の認可判定は、保護対象 (DATASET / RESOURCE) に対して「**この ACEE は許可されているか**」を問う形で行われる。ACEE が無ければ全ての SAF 検査は実行不能。

ACEE は単に USER ID だけでなく、所属グループ (current connect group)、属性 (SPECIAL / OPERATIONS / AUDITOR)、適用される securlabel、JES (job entry subsystem) 関連属性、ICRX (Identity Context Reference) 等を保持する。複雑に見えるが、要するに **「SAF 検査時の input package」** である。

Linux / Windows との対比:
- Linux: プロセスごとに `(real uid, effective uid, saved uid, supplementary groups, capabilities, SELinux context)` の組、`setuid` 等で動的変化
- Windows: プロセス / スレッドごとの access token (`HANDLE` from `OpenProcessToken`)、`ImpersonateLoggedOnUser` で一時 swap
- z/OS: address space ごとの ACEE (`ASXBSENV` 経由で chain)、TCB レベルの sub-ACEE もあり、**さらに別 ID で動かす場合は ACEE swap** (RACINIT/RACROUTE REQUEST=VERIFY ENVIR=CREATE)

特に **batch / started task で「別人で動かしたい」シナリオ (SUBMIT BY, SURROGAT, USER= JCL parm)** は ACEE 設計の中核トピック。「誰が誰の権限で動かしたか」が SMF type 80 にも記録される基盤。

## 2. mechanism（どう動くか）

### ACEE の場所
- Address space level: `ASXB` (Address Space Extension Block) → `ASXBSENV` が ACEE をポイント
- Task level: `TCB` → `TCBSENV` (TCB 個別 ACEE) があれば優先、無ければ address space level fallback
- Cross-memory: PC-ss 呼出時は、呼出先 address space の ACEE が使われる (FACILITY class の CSF.* 等の権限判定はここで効く)

### ACEE 作成経路
- **TSO LOGON**: TSO/E が `RACROUTE REQUEST=VERIFY` で password / phrase / certificate / MFA を検証 → ACEE 作成
- **JCL JOB statement の USER=**: JES (JES2/JES3) が初期化時に submitter ID で SURROGAT 検査 → ACEE 作成
- **Started task**: STARTED class / ICHRIN03 で「STC 名 → 実行 USER ID」マッピング → ACEE 作成
- **USS login (`telnetd` / OMVS shell)**: BPX (USS kernel) が SAF 経由 ACEE 作成
- **Application server (CICS / WAS)**: Server 内部で `RACROUTE REQUEST=VERIFY` を呼んで end user 用 sub-ACEE を thread に貼る

### ACEE swap (一時的別人化)
- `RACROUTE REQUEST=VERIFY ENVIR=CREATE` で別 ACEE を作る → 旧 ACEE 退避 → 操作 → `ENVIR=DELETE` で復帰
- アプリ層は CICS / IMS / Db2 がよく使う、authorized state (key 0-7 / supervisor) が必要

### SURROGAT 認可 (代理実行)
- `SURROGAT.SUBMIT.*` class profile で「USER01 は USER02 として SUBMIT 可」を許可
- 例: `RDEFINE SURROGAT USER02.SUBMIT UACC(NONE)` → `PERMIT USER02.SUBMIT CLASS(SURROGAT) ID(USER01) ACCESS(READ)`

### SAF 検査経路
- 保護対象アクセス時 (DATASET OPEN, transaction 起動, file 開く等) → `RACROUTE REQUEST=AUTH` 発行
- 引数の `ACEE=` が無ければ current ACEE (ASXBSENV / TCBSENV) を使う
- 戻り値 RC=0 (許可) / RC=4 (no profile) / RC=8 (不許可) / RC=12 (decision deferred)
- RC=8 時の reason code が「権限不足」「class inactive」「resource not defined」等を区別

## 3. prerequisites

- ZOS-RACF-001 (RACF 基礎)
- ZOS-SAF-001 (SAF callable services)
- ZOS-ASCB-001 (address space / TCB 構造、ASXB との関係)
- 一般 IT 知識: process credential / impersonation pattern

## 4. relations

- `depends_on`: ZOS-SAF-001, ZOS-RACF-001, ZOS-ASCB-001
- `specialized_by`: なし
- `contrasts_with`: Linux setuid + capabilities, Windows access token + impersonation, AWS STS AssumeRole
- `used_by`: ZOS-CICS-001 (BIND/Attach 時の transaction security と Surrogate), ZOS-IMS-001 (sign-on user の ACEE), ZOS-DB2-001 (thread の primary/secondary authid と ACEE), ZOS-FTP-001 (FTP server が end user ACEE を attach), ZOS-RRS-001 (URID 取得時の identity), ZOS-WAS-001 (servant region thread の ACEE)

## 5. pitfalls

詳細は `pitfalls/` 配下。

## 6. examples

詳細は `examples.md`。

## 7. decision_axes

詳細は `decision-axes/` 配下。
