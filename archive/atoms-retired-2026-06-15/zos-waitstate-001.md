---
id: ZOS-WAITSTATE-001
title: Wait state / loop / disabled wait
status: draft
last_reviewed: 2026-06-02
authors: [agent-z1]
rag_verified: partially
---

# ZOS-WAITSTATE-001: Wait state / loop / disabled wait

## 1. purpose（なぜ存在するか）

**Wait state** は z/OS kernel が回復不可能な error / 一時 hardware 待ちに陥った状態。**Disabled wait** (`PSW` の WAIT bit on + 全 interrupt disabled) は **system 全停止** を意味し、HMC 上に `Disabled wait state` 表示と code が出る。**Enabled loop** (CPU 暴走、interrupt は受ける) と **Disabled loop** (interrupt も受けない、PSW 進まない) も区別。

なぜこの概念が必要か: Linux kernel panic / Windows BSOD は「kernel 自体の破壊」を示すが、z/OS の wait state は更に細かく分類: **回復可能 wait** (recoverable resource 待ち、operator action で復旧)、**Disabled wait** (system integrity 喪失、IPL 必要) など。Wait state code (3 桁 hex + reason code) で原因即判定できる設計。

Linux kernel panic との対比: panic では即 reboot だが、z/OS は disabled wait で **system 停止** したまま **dump 採取可能** (stand-alone dump、SADMP)。これが PR/SM (LPAR hypervisor) と HMC の存在意義の一つで、failure 解析を完璧に残せる。

## 2. mechanism（どう動くか）

**PSW (Program Status Word)**:
- 16 byte (z/Architecture)、CPU の現状態 を表現
- WAIT bit (`bit 14`): on で wait state
- AMODE (`bit 31-32`): 24/31/64
- KEY (`bit 8-11`): storage key 0-15
- PROBLEM bit: supervisor vs problem state

**Disabled wait state**:
- PSW の wait bit on + interrupt disabled (System Mask の I/O / EXT bit off)
- PSW の `reason code` (右側 16-bit) に **wait state code** + 詳細
- 主要 code (3 桁 hex):
  - **064** (`x064`): page set フル系、Aux storage 不足
  - **071**: Recovery termination で disabled、SDWA 解析必要
  - **0A1**: master scheduler 起動失敗
  - **0A3**: NIP 段階 error (IPL 未完了)
  - **0B0**: I/O subsystem 致命的 error
  - **02D**: SVC dump 不能、その他

**Enabled loop**:
- WAIT bit off、PSW counter は進むが特定 address 範囲で循環
- I/O / EXT interrupt は受ける、operator command 可能
- `D PSW` (HMC) で確認、CPU 使用率 100% 一定

**Disabled loop**:
- WAIT bit off、PSW counter は進むが interrupt 全 disable
- system 完全 freeze、operator command 不能
- HMC `PSW restart` か stand-alone dump → re-IPL

**Stand-alone dump (SADMP)**:
- HMC から専用 SADMP DASD volume 起動
- 全 real storage + control block を DASD に保存
- IPCS で後解析、disabled wait の真因究明には必須
- 採取忘れで原因不明のまま再発するパターン非常に多い

**SPIN loop / Excessive Spin**:
- 複数 CP で同 lock を取り合い、終わらない状態
- `D XCF,STR=` 等で structure 状況、`IEE801D EXCESSIVE SPIN-LOOP CONDITION` msg

## 3. prerequisites（理解の前提）

- ZOS-ASCB-001 (TCB/SRB と PSW の関係)
- ZOS-VIRTSTOR-001 (Aux storage、page set 概念)
- ZOS-DUMP-001 (Stand-alone dump 採取)

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-ASCB-001, ZOS-VIRTSTOR-001, ZOS-DUMP-001
- `specialized_by`: なし
- `contrasts_with`: Linux kernel panic (即 reboot、dump は kdump で別 kernel 経由)、Windows BSOD (即 reboot、memory.dmp)、AWS EC2 hypervisor freeze (instance reboot 必要)、Linux soft lockup (CPU loop 検知 + watchdog reset)
- `used_by`: ZOS-IPCS-001 (stand-alone dump 解析)、ZOS-DUMP-001 (dump 採取設計)、ZOS-RECOVERY-001 (DR sequence)

## 5. pitfalls（実装・運用での落とし穴）

- **wait state 064 -> Page set フル、即対処不能**: Aux storage (page set) が 100% 使用 → kernel が paging 不能で disabled wait `x064`。IPL しないと復旧不能、SADMP 採取後 re-IPL。**現場対処**: 平常運用で `D ASM` 監視、80% 警戒 / 90% アラート、page set 動的追加 (PAGEADD) は 70% 前後で予防的に。**書き手経験**: 月次バッチで一時 dataset が VIO 占有 → Aux 急上昇 → wait 064 で銀行 OLTP 3 時間停止。
- **Recovery termination 中 loop で system 不安定**: RTM (Recovery Termination Manager) が ESTAE/ESPIE recovery 経路で loop、kernel state 半壊。disabled wait に陥らない代わりに work が動かない状態。**書き手経験**: third-party SVC が ESTAE 内で abend → 再 ESTAE → loop、`D A,L` で全 address space wait 状態が出るが操作不能、最終的に HMC restart で SADMP 採取。
- **Stand-alone dump 採取忘れで再現原因不明**: Disabled wait 発生時、operator が「とりあえず IPL」で復旧優先 → SADMP 採取せず → 翌週同じ wait 再発、解析不能。**現場対処**: 障害発生時の SOP に **SADMP 採取を強制**、IPL の前に必ず HMC SADMP 起動。これが守られないと永遠に root cause 不明。
- **PSW の AMODE 誤読**: PSW の bit 31-32 (AMODE) を旧 MVS 感覚で 24/31 だけで読むと、64-bit code が address `00000000_xxxxxxxx` に見えて混乱。**書き手経験**: Java 関連 disabled wait の解析で 64-bit AMODE 見落とし、address resolve 失敗で 4 時間ロス。**対処**: IPCS で `IP STATUS REGISTERS` で AMODE 表示確認、64-bit なら upper word も resolve。
- **Excessive spin で false positive operator action**: `IEE801D EXCESSIVE SPIN-LOOP CONDITION` で operator が `R nn,TERM` (address space 強制終了) 実行 → 巻き添えで critical work 死亡。**書き手経験**: WLM SRM の一時 spin に operator が反応、結果 DB2 主要 task が TERM で DB 破損。**対処**: `IEE801D` の reply は default 90 秒 wait、その間に `D A,L` で address space 影響範囲確認。
- **Disabled loop で HMC `PSW restart` 連発**: Disabled loop の対処で `PSW restart` (HMC) を連発すると、kernel state 不整合で disabled wait に転落。**対処**: `PSW restart` は 1 回までで判断、効かないなら SADMP → re-IPL。
- **wait 0A1 / 0A3 を区別せず operator action**: `0A1` (master scheduler 起動失敗) と `0A3` (NIP 段階 error) は対処違う: 0A1 は parm 系問題 (LOADxx/IEASYS)、0A3 は I/O 系 (SYSRES 認識失敗、IODF 問題)。混同で diagnostic 経路ずれ。**対処**: wait code を即引いて手順分岐、code 表を SOP に印刷。

## 6. examples（具体例）

```
* HMC operator workplace で Disabled wait 発生時
PSW: 070C0000 00000000 00000000 0000064  <- wait code 064
                                       ^^ wait state code (3 桁 hex)

* 解釈
- PSW bit 14 (WAIT) = 1
- PSW interrupt mask = 0 (disabled)
- wait code 064 = Aux storage exhausted -> page set フル
```

```
* SADMP 採取手順 (HMC)
1. HMC で対象 LPAR 選択
2. CPC > Recovery > Standalone dump
3. SADMP DASD volume (例: SADUMP) を Load
4. SADMP が自動で全 real storage を SYS1.SADMP データセットに保存
5. 完了後 normal IPL で system 再開
6. IPCS で SADMP を read:
   IP SETDEF DSNAME('SYS1.SADMP.D250602.T0430') NOCONFIRM
   IP STATUS REGISTERS         <- 障害時 PSW 表示
   IP SUMMARY FORMAT KEYFIELD(ASID,JOBNAME)
   IP VERBX MTRACE             <- master trace
   IP VERBX LOGDATA            <- LOGREC 直近
```

```
* Excessive spin 検知時の operator command
D A,L                          <- 全 address space CPU 状況
D U                            <- CPU 別 util
D XCF,STR=*                    <- CF structure 状況
DUMP COMM=(SPIN_DEBUG)         <- 全 system dump 開始
   R xx,JOBNAME=(*MASTER*),CONT
   R xx,SDATA=(CSA,RGN,LSQA,LPA,GRSQ,SUM,TRT),END
```

```
* SDSF / NetView で wait state msg trap
IF MSGID = 'IEE801D' THEN
   EXEC(CMD('D A,L; D U') ROUTE(ONE NETVIEW));
IF MSGID = 'IEE331A' THEN  <- disabled wait pre-message
   ALERT(SEV=CRITICAL);
```

## 7. decision_axes（採否を分ける判断軸）

- **SADMP vs SVC dump**: **SADMP** (stand-alone) は disabled wait / loop で kernel 不能時の唯一手段、HMC 経由で別 IPL 必要。**SVC dump** は kernel 動作中の任意 dump、運用中に取れる。**選定基準**: system 状態 (生きてるか否か)、dump 必要範囲 (全 real storage か特定 address space か)。
- **Disabled wait 時の IPL 優先 vs SADMP 優先**: 業務影響最小化なら IPL 即実施、根本原因究明なら SADMP 採取後 IPL。**選定基準**: 障害頻度 (初回 / 再発)、業務 SLA、解析チーム capability。**ルール**: 初回 disabled wait は SADMP 必須、再発 IPL も SADMP 推奨。
- **Enabled loop の介入: TERM vs CANCEL vs DUMP**: **TERM** は最強の強制終了、巻添えリスク。**CANCEL** は穏便な終了要求、loop 中だと効かないこと多い。**DUMP COMM=,jobname=** は dump 採取して継続、解析優先。**選定基準**: 影響範囲、原因究明 priority、運用時間帯。
- **Wait state code lookup の SOP**: code 表を operator 手元に常時、または NetView で `IEE801D` を trap して自動解説出力。**選定基準**: operator 経験度、運用時間 (深夜帯は SOP 必須)、automation 整備状況。

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_TECH_001) から disabled wait 解析の運用知識を概念蒸留 (ADR-0109)。書籍は概念補助。
