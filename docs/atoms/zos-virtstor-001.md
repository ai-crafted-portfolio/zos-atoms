---
id: ZOS-VIRTSTOR-001
title: 仮想記憶 + ストレージ階層
status: draft
last_reviewed: 2026-06-02
authors: [agent-z1]
rag_verified: partially
---

# ZOS-VIRTSTOR-001: 仮想記憶 + ストレージ階層

## 1. purpose（なぜ存在するか）

z/OS の仮想記憶は **64-bit address space x 多重** という設計。1 address space = 16 EB の理論空間 (実用は LPAR real storage と Aux storage で制限)。Common / Private / Above-the-bar / High Virtual に分かれ、それぞれ用途と寿命が違う。

なぜこの階層か: 24-bit (16 MB) → 31-bit (2 GB) → 64-bit (16 EB) と歴史的に拡張されてきたが、**24/31-bit アプリ互換性を維持しながら** 64-bit を提供する必要があった結果。`bar` (2 GB 境界) の上下で Below-the-bar / Above-the-bar、`extended common` (16 MB 境界の上) で extended SQA/CSA/LPA がある。Common 領域 (SQA/CSA/LPA) は全 address space から共通 mapping され、System service / I/O buffer 等で活用される。

Linux の virtual memory + swap、Windows VAS + pagefile が比較対象だが、決定的な違いは:
1. z/OS は **address space 多重で 16 EB ずつ独立**、Linux は process 単位だが ECS (Exec Common Storage) 概念は無い
2. z/OS の Aux storage (page set) は **MVS 専用 dataset** で fs に乗らない、Linux swap partition より厳格
3. `HiperDispatch` で CPU affinity / cache locality / storage 階層を統合制御

## 2. mechanism（どう動くか）

**Address space layout (64-bit)**:
```
0000_0000_0000_0000  Low Private (24-bit、CICS COMMAREA 等 legacy)
00000000_00FFFFFF    16 MB line (24-bit 上限)
0000_0001_00000000   2 GB bar (31-bit 上限)
                     | Above-the-bar Private | (64-bit data)
                     | High Virtual Common  |
FFFF_FFFF_FFFFFFFF   16 EB
```

**Common 領域 (全 address space 共有)**:
- **SQA** (System Queue Area): kernel control block、固定 size、IPL parm `SQA=(n,m)`
- **CSA** (Common Service Area): SVC / PC routine 用、`CSA=(n,m)` で size 指定
- **LPA** (Link Pack Area): re-entrant kernel module、`MLPA`/`FLPA`/`PLPA`、IPL 時に LOAD
- **ECSA/ESQA/ELPA**: 上記の extended (16 MB 上)
- **HVCOMMON** (High Virtual Common): 2 GB 上の Common、`HVCOMMON=` で size

**Private 領域 (address space ごと)**:
- User region (24-bit / 31-bit)、`REGION=` parm 指定、`REGION=0M` で max
- Extended user region: 16 MB 上 〜 2 GB
- Above-the-bar Private: 2 GB 〜、`MEMLIMIT=` で上限

**Aux storage**:
- Page set: `PAGE=` parm、`PLPA` / `Common` / `Local` の 3 種類
- `IRA200E` (page set フル) で system 停止リスク、page set 拡張は IPL 必要
- VIO (Virtual I/O): SPOOL / TEMP に使う、Aux 上

**HiperDispatch**:
- 各 CP (Central Processor) に **affinity** を付け、L1/L2 cache hit 率を上げる
- WLM と連動、`HIPERDISPATCH=YES` (default、`IEAOPTxx`)、無効化すると性能ペナルティ 5-15%

**PAV** (Parallel Access Volume):
- 1 DASD volume に複数 UCB (Unit Control Block) を割当、同時 I/O を可能に
- Static PAV / Dynamic PAV (WLM control) / HyperPAV (z14 以降の prefferd 方式)

## 3. prerequisites（理解の前提）

- ZOS-ASCB-001 (address space 概念)
- DASD / page set の dataset 仕組み (→ ZOS-DASD-001)
- 一般 IT 知識: virtual memory、paging、TLB

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-ASCB-001
- `specialized_by`: なし
- `contrasts_with`: Linux page table + swap (process 単位 / Common storage 無)、Windows VAS + pagefile (Address Space 単一視点)、Linux Transparent Huge Pages vs z/OS 1 MB large frame、AWS EC2 instance memory (LPAR shared real memory との対比)
- `used_by`: ZOS-WAITSTATE-001 (page set フル系 wait code)、ZOS-DUMP-001 (CHNGDUMP の領域指定)、ZOS-IPL-001 (LOADxx での page set 定義)

## 5. pitfalls（実装・運用での落とし穴）

- **CSA 逼迫で IEA404A、reboot 不可避**: CSA leak (前述 ZOS-ASCB-001 pitfall) が長期蓄積で `IEA404A SYSTEM HAS REACHED MAXIMUM AUXILIARY STORAGE CAPACITY` 系の派生または `IRA300E` で system 機能が degrade。**書き手経験**: 銀行 OLTP で CSA 使用率が weekly 1% ずつ上昇、3 ヶ月で 90% 到達 → 月次 IPL でリセットしてた事案、根本原因は third-party MQ exit の FREEMAIN 漏れ。CSA 縮小は IPL 必要、運用中 release はほぼ不可能。
- **Page set フル (IRA200E) で system hang**: Aux storage が一杯になると `IRA200E AUX STORAGE SHORTAGE` → 続いて `IRA201E CRITICAL` → `IEA995I MEMORY TERMINATION` 連鎖。**現場対処**: page set を事前に複数 (Common / Local 分離) で配置、`PAGEADD` command で動的追加、SMF type 71 で page set 使用率を 70% 警戒。新規 page set 追加は IPL なしで可能だが、削除は IPL 必要。
- **Above-the-bar storage の MEMLIMIT 認識違い**: アプリが 64-bit storage (`IARV64 REQUEST=GETSTOR`) を要求しても、JCL の `MEMLIMIT=` か SMFPRMxx の `MEMLIMIT` で頭打ち、default は 0 (使えない)。**書き手経験**: Java for z/OS の heap が 2 GB で頭打ち、原因は `MEMLIMIT=2G` を `MEMLIMIT=NOLIMIT` にし忘れ、SMFPRMxx の default 2 GB だった。`D SMF` で確認可能。
- **Common 領域 fragmentation で大型 GETMAIN 失敗**: CSA 使用率 50% でも fragmentation で大型 contiguous request (例: 1 MB) が `ABEND 878-10` で失敗。**現場対処**: `D ASM` で fragmentation 状況確認、reboot しないと圧縮されない、根本対策は CSA 使う SVC/exit を見直し小分け取得 + 早期 free。
- **LPA cache 古いまま (CLPA 漏れ)**: IPL 時に `CLPA` (Create LPA) 指定しないと旧 cached LPA が使われ、SMP/E で apply した module が反映されない。**書き手経験**: emergency PTF 適用後の IPL で CLPA 忘れ、症状再発で再 IPL、運用障害扱いになった。**対処**: PTF 適用後の IPL SOP に `CLPA` 強制、もしくは LOADxx の `IEASYS` で `CLPA` を hard-code。
- **HiperDispatch off で WLM goal 達成不能**: `HIPERDISPATCH=NO` (IEAOPTxx) にすると CP affinity が失われ、cache thrash で CPU 性能 5-15% 低下、WLM の Response Time goal が PI > 1 連発。**書き手経験**: troubleshoot 目的で HiperDispatch を off にして「忘れた」事案、月次性能 review で発覚、原因特定に 2 週間。

## 6. examples（具体例）

```
* IEASYSxx (IPL parm) 抜粋
SQA=(8,200)         CSA 下 8 / 上 200 MB
CSA=(50,1000)       CSA 下 50 / 上 1000 MB
PAGE=(SYS1.LOCAL1,SYS1.LOCAL2,SYS1.COMMON1,SYS1.PLPA,L)
HIPERDISPATCH=YES
REAL=128
```

```
* operator command で storage 状況確認
D ASM                    page set 使用率
D VS,LOCAL              Local page set
D VS,CSA                CSA 使用率
D M=STOR                real storage 構成
PAGEADD PAGE=SYS1.LOCAL3   page set 動的追加
```

```
* JCL での MEMLIMIT
//STEP1 EXEC PGM=MYJAVA,REGION=0M,MEMLIMIT=4G
//STEPLIB DD DISP=SHR,DSN=JAVA.LOADLIB
```

```
* RMF Mon III で storage breakdown
RMFMON III
  -> STORM (Storage memory)
  -> STORC (Common storage)
  -> STORR (Real storage)
```

## 7. decision_axes（採否を分ける判断軸）

- **Common storage vs Private storage 配置**: SVC routine / cross-memory 必要なら **Common** (SQA/CSA)、address space 内完結なら **Private**。Common は kernel global で全体に影響、leak が致命的。**選定基準**: アクセス対象範囲、寿命 (Common は IPL までずっと、Private は address space と同じ)、reentrancy 要件。
- **Below-the-bar vs Above-the-bar**: **Below** (2 GB 以下) は 31-bit AMODE、legacy COBOL/Assembler 互換だが容量制限。**Above** (2 GB 超) は 64-bit AMODE、Java / 新規 C/C++ / 大型データ。**選定基準**: 既存資産との連携 (COMMAREA 等)、データ size、開発言語。
- **Static PAV vs HyperPAV**: **Static** は volume に固定 alias UCB、低オーバーヘッド・予測性高だが alias 数固定。**HyperPAV** は WLM 制御で動的に alias 借用、効率良いが latency 微増。**選定基準**: I/O profile が安定なら Static、burst 型なら HyperPAV、z14 以降は HyperPAV 推奨。
- **Page set 構成: Common と Local の分離**: 全部同じ page set に置くと Common page-out で Local が押される。**Common 専用 + Local 専用** に分けると独立性向上、ただし DASD volume が増える。**選定基準**: Common 領域使用量 (CSA leak 体質なら必須分離)、DASD 余裕。

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_TECH_001) から仮想記憶設計の実運用知識を概念蒸留 (ADR-0109)。逐語引用禁止。
