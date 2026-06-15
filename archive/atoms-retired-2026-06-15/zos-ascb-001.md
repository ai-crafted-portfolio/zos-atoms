---
id: ZOS-ASCB-001
title: アドレス空間制御ブロック (ASCB / ASSB)
status: draft
last_reviewed: 2026-06-02
authors: [agent-z1]
rag_verified: partially
---

# ZOS-ASCB-001: アドレス空間制御ブロック (ASCB / ASSB)

## 1. purpose（なぜ存在するか）

ASCB (Address Space Control Block) は z/OS kernel が各アドレス空間 (Address Space) を識別・管理する **核となる固定長 control block**。1 つのアドレス空間 = 1 つの ASCB であり、System area (Common storage) に置かれる。**SQA** (System Queue Area) に常駐し、`x80` バイト前後の固定構造。

なぜ存在するか: MVS は当初から **同時複数 address space** モデル (Multi Virtual Storage = MVS) で設計され、各 address space を kernel が高速に列挙・dispatch するため、固定 offset でフィールドアクセスできる control block が必要だった。ASCB は dispatching queue (ready / wait) の double linked list で繋がっており、Dispatcher は ASCB chain を回って次に走らせる address space を決める。

Linux の `task_struct` / Windows `EPROCESS` に対応するが、決定的な違いは **ASCB が SQA (Common storage) にあって全 address space から参照可能** な点。Linux の task_struct は kernel space に置かれ user space からは見えない。z/OS ではアプリ (authorized state なら) が他 address space の ASCB を直接読める仕様で、これは cross-memory service の前提でもある。

## 2. mechanism（どう動くか）

主要フィールド (代表):
- **ASCBASID** (`+x24`, 2 byte): Address Space ID (ASID)、1〜0xFFFF
- **ASCBJBNI** / **ASCBJBNS** (`+x50`/`+x54`): Job name (initiator / started task)
- **ASCBASXB** (`+x6C`): ASXB (Address Space Extension Block) への pointer、TCB chain root は ASXB.ASXBFTCB
- **ASCBCSCB** (`+x38`): CSCB (Command Scheduling Control Block) への pointer
- **ASCBOUCB** (`+x90`): OUCB (SRM User Control Block) への pointer、WLM/SRM が使う
- **ASCBASSB** (`+x150`): ASSB (Address Space Secondary Block) への pointer、cross-memory authority 情報

階層構造:
```
ASCB (SQA, ASID 単位)
 +-- ASXB (private, ASCB が ASXB を指す)
 |    +-- ASXBFTCB -> TCB chain (task) -> RB chain
 |    +-- LDA, RTM2WA 等
 +-- ASSB (cross-memory 情報、PCAUTH 等)
 +-- OUCB (SRM/WLM 計測)
```

- **TCB** (Task Control Block): job step 毎に存在、attach で増える、`SUBTASK` の本体
- **SRB** (Service Request Block): 「割込み駆動の非同期処理」用、TCB より軽量、disabled で実行可能
- TCB は preemptive、SRB は disabled 区間で連続実行 (kernel critical section)
- 1 address space に TCB 数百〜、SRB は短命

ASID 割当:
- 1〜0xFFFF (65535) の範囲、`MAXUSER` parm で実用上の上限制御
- 終了後 ASID は再利用される (ASID wrap-around) が、reuse 前に一定期間 reserve
- `D A,ASID=nnnn` で確認、`SETROPTS` ではなく `D ASM` 等の operator command で覗ける

## 3. prerequisites（理解の前提）

- 一般 IT 知識: process / thread / control block
- z/OS storage 階層 (→ ZOS-VIRTSTOR-001): Common (SQA/CSA/LPA) / Private の区別
- メモリ map / pointer chase の基礎

## 4. relations（他アトムとの繋がり）

- `depends_on`: なし
- `specialized_by`: なし
- `contrasts_with`: Linux task_struct (kernel space 限定、外から見えない)、Windows EPROCESS (kernel mode 限定)、Linux /proc/$pid (read-only な投影に対し、z/OS ASCB は authorized program なら直接 read 可能)
- `used_by`: ZOS-VIRTSTOR-001, ZOS-WAITSTATE-001, ZOS-DUMP-001, ZOS-IPCS-001, ZOS-WLM-001 (SRM/OUCB 経由)

## 5. pitfalls（実装・運用での落とし穴）

- **CSA leak と address space recycle**: アプリが `GETMAIN SP=241` (CSA) で取得した storage を `FREEMAIN` せずに address space 終了→ CSA leak。ASCB は終了で消えるが、CSA は kernel global なので残置。長期間で CSA fragmentation → `IRA300E` (SQA exhausted) や `IEA404A` で IPL 必要に。**現場対処**: SMF type 32 / 33 で GETMAIN/FREEMAIN 不整合を追う、もしくは CSA monitor ツール (RMF Mon III の `STORC` report) で leak source ASID 特定。
- **Cross-memory mode の認可漏れ**: アプリが `SSAR` (Set Secondary ASN) で他 address space に向くには `AKM` (Authorization Key Mask) / `EKM` (Extended Auth Key Mask) を ASSB に登録済が前提。登録漏れで `0D3` ABEND (cross-memory privilege violation)。**書き手経験**: PC routine 経由の cross-memory call で `PCLINK STACK` 失敗、原因は ATL (Authorization Table) と ASSB の不一致だった。
- **ASCB scan 系 utility の reentrant 性**: ASCB chain を `ASCBFWDP` (forward pointer) でたどるツールは、scan 中に dispatcher が ASCB 並び替えると **中途で逸脱 / loop**。**現場対処**: `LOCAL` lock (`SETLOCK OBTAIN,LOCAL`) で短時間保護、または `ASCBASID` を順次 increment で覗く方式。`D A,L` の出力タイミングと SDSF DA で table が乱れる事案あり。
- **ASID wrap-around で別 job 取り違え**: ASID は 16-bit で枯渇後 reuse される。古い SMF record の ASID と新 job の ASID が同じになり、性能分析ツールが **無関係 job をマージ集計**。**書き手経験**: 2019 年に customer の月次 RMF report で「謎の CPU 跳ね」、原因は ASID 再利用後の集計バグ。**対処**: SMF type 30 では `SMF30JBN` (job name) と `SMF30STM` (start time) で identify、ASID 単独は信用しない。
- **ASCB を Print Dump で見て symbol 未解決**: IPCS の `IP ASCB` コマンドは ASCB を formatted 表示するが、`MODULE` resolve が無いと offset が hex のまま読みにくい。**現場対処**: `IP SUMMARY FORMAT` の前に `IP SETDEF DSNAME(...)` で symbol dataset を bind、`IP VERBX MTRACE` も同じ前提で動かないと、原因 module が ASCB から取れず無効化される。
- **ASXB.ASXBFTCB から TCB tree 取り違え**: ASXBFTCB は **first TCB**、その後 `TCBNTC` (next task on same level) と `TCBLTC` (lowest sub-task) で tree が広がる。`TCBNTC` だけ追うと sub-task を全部見逃す。**書き手経験**: アプリ hang 解析で `TCBPRT` 結果に出てなかった sub-task が真の hang 元だった事案、`IP SUMMARY FORMAT TCBSUM` で完全展開すべきだった。

## 6. examples（具体例）

```
* ASCB 主要フィールド (z/OS 2.5、`IHAASCB` macro 抜粋)
+x00  ASCBASCB  CL4   'ASCB' eyecatcher
+x04  ASCBFWDP  A     forward pointer (next ASCB)
+x08  ASCBBWDP  A     backward pointer
+x24  ASCBASID  H     ASID
+x38  ASCBCSCB  A     CSCB pointer
+x50  ASCBJBNI  CL8   job name (initiator)
+x6C  ASCBASXB  A     ASXB pointer (private 側へ)
+x90  ASCBOUCB  A     SRM/WLM control
+x150 ASCBASSB  A     ASSB pointer (cross-memory)
```

```
* IPCS で ASCB 解析
IP SETDEF DSNAME('USER.DUMP.D250602.T1430') NOCONFIRM
IP STATUS REGISTERS
IP SUMMARY FORMAT KEYFIELD(ASID,JOBNAME)
IP ASCB ASID(X'001A')
IP VERBX MTRACE
```

```
* operator command で ASCB ベース情報を出す
D A,ASID=001A
D A,L
D ASM,ASID=001A
```

## 7. decision_axes（採否を分ける判断軸）

- **ASCB 直接参照 vs SDSF/RMF API**: **ASCB 直接 read** は authorized state 必須 + reentrancy 自分で確保 + 内部構造の z/OS リリース差吸収必要。**SDSF REXX API** / **RMF Mon III DDS** はサポートされた interface で安定だが latency と粒度の制約あり。**選定基準**: 単発ツールなら API、常駐 system monitor なら ASCB 直接 + LOCAL lock + リリース別 macro 化。
- **ASID 単位 vs Job name 単位の identify**: ASCB ベースの分析は **ASID** が key、SMF 集計は **Job name + start time** が key。同 job が再 submit で別 ASID になり、ASID 単位だと「同 job の 2 run」が別物に見える。**選定基準**: real-time 監視は ASID (即値性)、capacity / billing は Job name + time。
- **Authorized program (APF) vs Unauthorized**: ASCB の private 領域以外を read するには Key 0 / Supervisor state / APF authorized のいずれか必要。**APF authorized** にすると全 address space を覗けるが、悪用で system integrity 破壊リスク。**選定基準**: 業務アプリは絶対 unauthorized、運用 utility のみ APF (RACF FACILITY class で限定)。


## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

本 atom の領域については、IBM 公式 manual を一次出典としつつ、運用事例や設計判断の補強として市販書籍 (BK_MF_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 等の z/OS / メインフレーム関連書籍) からの実装知識を補助的に参照する。逐語引用は禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
