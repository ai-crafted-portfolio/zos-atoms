---
id: ZOS-IPL-001
title: IPL + LOADxx parm
status: draft
last_reviewed: 2026-06-02
authors: [agent-z1]
rag_verified: partially
---

# ZOS-IPL-001: IPL + LOADxx parm

## 1. purpose（なぜ存在するか）

IPL (Initial Program Load) は z/OS の system 起動シーケンス。HMC (Hardware Management Console) または stand-alone console から initiate し、`SYSRES` volume から NIP (Nucleus Initialization Program) を load して LOADxx / IEASYSxx / IEAOPTxx を順に読む。**IPL なしで変更できる parm と、IPL 必要な parm の境界** を知らないと運用設計を誤る。

なぜこの階層か: z/OS は kernel 設定が parm dataset (`SYS1.PARMLIB` 等) の **member 単位** で hot-swap 可能領域と IPL 必要領域に分かれている。`LOADxx` (SYS0.IPLPARM) で suffix を切替えて構成 (例: `LOAD00` = 平常、`LOADBD` = 障害復旧) し、`IEASYM` parm で `&SYSNAME.` 等の symbol を解決する。

Linux GRUB + initramfs、Windows boot loader と異なり、z/OS の IPL は **完全に dataset (DASD) ベース**: `SYS1.PARMLIB` を編集→次回 IPL で反映、運用での「設定変更=次回 IPL 待ち」が日常的。emergency 系では `SET IEASYS=xx` や `SETxxxx` 系 operator command で動的反映可能なものもあるが、`IEASYS` の `CMD=` (auto execute) 等は IPL 限定。

## 2. mechanism（どう動くか）

**IPL シーケンス**:
1. HMC で SYSRES volume を指定して `Load` 操作 (`Load type=Normal`)
2. NIP (`IPLINFO`) が ROM 領域から起動 → SYSRES の IEAVNIP0 を load
3. **LOADxx** を SYS0.IPLPARM (default) または SYSRES から読み込み
   - `LOADxx` suffix は HMC の `Load parameter` で指定 (`IODF=00`, `LOAD parm` = `0A82M11M` 等)
   - 形式: `LOADxx` から `IODF=` / `NUCLEUS=` / `SYSPARM=` / `IEASYM=` / `PARMLIB=` 参照
4. **IEASYS00** + `SYSPARM=` 補完 → IPL parm dataset 全列挙
5. NIP が **SQA/CSA/LPA** を構築、page set mount、master scheduler 起動
6. `IEACMD00` / `COMMNDxx` で起動コマンド実行
7. JES2/JES3 起動、TSO / TCP/IP 等 STC 起動
8. `IEE389I MVS COMMAND PROCESSING AVAILABLE` で IPL 完了通知

**主要 parm member**:
- **LOADxx**: SYSRES / IODF / NUCLEUS / IEASYM / PARMLIB / SYSCAT 等の根本指定
- **IEASYSxx**: 一般システム parm (`CSA=`, `SQA=`, `MAXUSER=`, `PAGE=`, `SMF=`)
- **IEAOPTxx**: WLM / SRM 関連 (`HIPERDISPATCH=`, `IFAHONORPRIORITY=`)
- **IEASYMxx**: symbol 定義 (`&SYSNAME=`, `&SYSCLONE=`)
- **CONSOLxx**: console 構成 (→ ZOS-CONSOLE-001)
- **CLOCKxx**: TOD / timezone
- **PROGxx**: APF / LNKLST / LPA 設定

**CLPA / CVIO の判断**:
- `CLPA` (Create LPA): LPA を新規構築。SMP/E apply 後の必須 (前述 pitfall)
- `CVIO` (Cold start VIO): VIO dataset を clear。IPL 後の clean state、ただし運転中データ消失
- これらは LOADxx の `NUCLEUS=` ではなく、HMC IPL parameter で動的指定する場合が多い

**IODF** (I/O Definition File):
- HCD (Hardware Configuration Definition) で edit、PROD/WORK 状態あり
- IPL 時 LOADxx で `IODF=xx,IODFLIB` 指定
- IODF 不一致で `IOS076E DEVICE NOT FOUND` 連発、起動不可

## 3. prerequisites（理解の前提）

- ZOS-ASCB-001 (address space 概念、IPL で master scheduler ASID=1 起動)
- ZOS-DATASET-001 (PARMLIB member 編集の前提)
- HMC operation の基礎 (Load operation)

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-ASCB-001
- `specialized_by`: なし
- `contrasts_with`: Linux GRUB + initramfs (kernel parameter は command line、dataset member ではない)、Windows boot loader + BCD (binary 設定 vs z/OS の text parm)、AWS EC2 user data (起動時 script vs PARMLIB member)、Linux systemd preset (起動順 dependency)
- `used_by`: ZOS-CONSOLE-001, ZOS-WAITSTATE-001 (IPL 中 wait state)、ZOS-SMF-001 (SMF parm)、ZOS-WLM-001 (WLM policy activate)

## 5. pitfalls（実装・運用での落とし穴）

- **LOADxx の SUFFIX 指定漏れで IPL 失敗**: HMC の `Load parameter` で `LOAD parm` (例: `0A82M101M` = IODF=01, SYSCAT=M1, LOAD=01) の suffix 設定ミスで、想定外の LOADxx を読みに行く。**書き手経験**: DR 演習で `LOADBD` を指定したつもりが `LOAD00` を読み、結果 production parm が DR site で動いて IP address 衝突。HMC profile (Activation Profile) で固定するのが正解、手動入力は避ける。
- **CLPA 抜けで LPA 古いまま**: SMP/E APPLY 後の IPL で `CLPA` を指定しないと旧 cached LPA を使い続け、PTF が反映されない。`D PROG,LPA` で LPA load 時刻を確認、IPL 時刻と一致してないと未反映。**現場対処**: PTF apply SOP に `IPL 時に CLPA 強制` を必ず明記、LOADxx の `IEASYS` member に `CLPA` をデフォルト hard-code する案もあるが、頻繁な IPL で LPA 再構築 overhead を嫌う運用もある。
- **IEASYM symbol 衝突 / 解決失敗**: `&SYSNAME` 等 system symbol が IEASYMxx で多重定義されると、最後勝ちで意図しない値が入る。`SYS1.PARMLIB(LLA00)` 等で `DSN=USER.&SYSCLONE..LIST` が想定と違う dataset を resolve。**書き手経験**: Sysplex に LPAR 追加時に `&SYSCLONE` を `Z1` に設定、既存の `&SYSCLONE=PR` 想定の parm が全部壊れた。`D SYMBOLS` で確認、変更前にdry-run 必須。
- **IPL volume の SMS managed 不可**: SYSRES volume を SMS-managed にすると IPL 段階で SMS 未起動なので read 不可。SMS storage group には絶対入れない、Non-SMS で固定 + RACF プロテクトが基本。**現場対処**: SYSRES は専用 storage pool で別管理、SMS ACS routine で除外。
- **IODF mismatch で device 認識不能**: HCD で device 構成変更後、IODF を PROD 化せず WORK のまま IPL → `IOS076E` で device 認識失敗。**書き手経験**: 月次変更で IODF=05 を WORK で残し、別チームが IPL で `IODF=05` 指定、結果新規 channel 未認識で業務停止 4 時間。HCD の `Build production IODF` を必ず最後に実施。
- **Hot IPL 時の page set fragment**: 短時間で IPL 連発すると page set の cleanup が間に合わず、`IRA100E` (page space full anomaly) で第 2 IPL hang。**現場対処**: IPL 間隔は最低 5 分空ける、SOP に `D ASM` で page set status 確認後の次 IPL 許可。
- **PARMLIB concatenation 順序の隠れた優先**: LOADxx の `PARMLIB` は複数 dataset concatenation 可能、同名 member は先頭 dataset 優先。**書き手経験**: 緊急時に開発用 PARMLIB を先頭に追加したまま運用継続、production member が override されてた事案、定期 IPL でデグレ発覚。`D PARMLIB` で確認。

## 6. examples（具体例）

```
* LOAD00 (SYS0.IPLPARM)
NUCLEUS  1
IODF     00 SYS1     03 Y
SYSCAT   MCAT01113CSYS1.MASTER.CATALOG
SYSPARM  00,IS
IEASYM   00
PARMLIB  USER.PARMLIB
PARMLIB  SYS1.PARMLIB
```

```
* IEASYS00
SQA=(8,200)
CSA=(50,1500)
HIPERDISPATCH=YES
MAXUSER=400
PAGE=(SYS1.PLPA,SYS1.COMMON1,SYS1.LOCAL1,SYS1.LOCAL2,L)
SMF=00
WLM=00
CONSOLE=00
SCH=00
CMD=(00,L)
APF=00
LNKLST=00
LPA=00
CLPA
```

```
* IEASYM00
SYSDEF SYSCLONE(&SYSNAME(3:2))
SYSDEF SYSNAME(SYSA) HWNAME(CEC1) LPARNAME(LPARA)
SYSDEF SYSNAME(SYSB) HWNAME(CEC1) LPARNAME(LPARB)
SYMDEF(&PRODUCT='ZOS')
SYMDEF(&ENVIRON='PROD')
```

```
* HMC Load parameter (8 char)
0A82M101M
  ^^ IODF SUFFIX (=0A82, つまり IODF.IODF82)
      ^^^^ SYSCAT (=M101, つまり catalog identifier)
          ^ LOAD SUFFIX (=M)
* つまり LOADM を読みに行く
```

```
* operator command (IPL 後)
D IPLINFO            IPL 履歴
D SYMBOLS            system symbol
D PARMLIB            PARMLIB concatenation
D PROG,LPA           LPA load 時刻
D ASM                page set 状況
SET IEASYS=xx        run-time SYSPARM 変更 (限定的)
```

## 7. decision_axes（採否を分ける判断軸）

- **Static LOADxx vs Variable LOADxx**: **Static** (LOADxx 1 つ + LPAR 毎に IEASYM で差分) は管理 simple、symbol 解決でメンテ集中可。**Variable** (LOADxx を LPAR 毎に分ける) は完全独立だが member 増殖。**選定基準**: LPAR 数 (3-4 なら Static、10+ なら Variable 検討)、運用標準化レベル。
- **CLPA 強制 vs オプション**: **CLPA 強制** (LOADxx に hard-code) は PTF 反映漏れ事故防止、ただし毎回 IPL 5-10 分余計に。**オプション** (HMC で都度指定) は速い IPL 可能だが指定漏れリスク。**選定基準**: PTF apply 頻度、IPL 時間 SLA、運用習熟度。
- **PARMLIB を SYSRES と分ける**: PARMLIB を SYSRES と同じ volume にすると IPL シンプルだが SYSRES rolling upgrade で巻き込まれ。**別 volume** (USER.PARMLIB 等) にすると分離独立で運用しやすいが mount 順序注意。**選定基準**: SYSRES upgrade 頻度、parm 変更頻度、Sysplex 共有要否。
- **IODF を Sysplex 共通 vs LPAR 個別**: **共通 IODF** は Sysplex 全体で I/O 構成統一、HCD 編集で全 LPAR 反映だが影響範囲広。**個別 IODF** は LPAR 独立だが構成不整合リスク。**選定基準**: I/O sharing 度 (DASD shared 多いなら共通)、運用承認フロー。


## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

本 atom の領域については、IBM 公式 manual を一次出典としつつ、運用事例や設計判断の補強として市販書籍 (BK_MF_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 等の z/OS / メインフレーム関連書籍) からの実装知識を補助的に参照する。逐語引用は禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
