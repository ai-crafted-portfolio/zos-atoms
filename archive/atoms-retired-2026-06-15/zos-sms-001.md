---
id: ZOS-SMS-001
title: SMS（System Managed Storage）
status: stable
last_reviewed: 2026-06-01
authors: [agent]
rag_verified: partially
---

# ZOS-SMS-001: SMS（System Managed Storage）

## 1. purpose（なぜ存在するか）

SMS は DASD のアロケーション（ボリューム選定・配置・サイズ・退避方針）を **JCL 側に書かせず、システム側ポリシで自動決定** する仕組み。「人間が DASD ボリューム名を JCL に直書き」の運用が、年代を経るとボリューム消滅・ボリューム移行・容量逼迫で崩壊するため、その層を z/OS が肩代わりする。

Linux なら mountpoint と filesystem を sysadmin が固定し、アプリは `/var/log/...` のような **論理パス** に書くだけで物理ボリュームを意識しない。SMS はその「論理 → 物理マッピング自動化」を z/OS のデータセット世界に持ち込んだ仕掛け。逆に言うと、SMS 以前の z/OS は **「アプリが VOL=SER=DISK01 を直接指定」していた** ということ。1980 年代までは普通だったが、何百ボリュームになると保守が成立しない。

SMS は ACS（Automatic Class Selection）ルーチンと呼ばれる **ポリシ言語** を導入し、DSN・JOBNAME・UNIT・SIZE 等を入力として 4 つのクラス（StorageClass / DataClass / ManagementClass / StorageGroup）に振り分ける。これで JCL は `UNIT=SYSDA,VOL=SER=...` を書かず、`DSN=USER.PROD.SALES` だけで適切な DASD グループに落ちる。

## 2. mechanism（どう動くか）

- SMS は **4 種のクラス** + **ACS ルーチン群** で構成される。
- **StorageClass (STORCLAS)**: パフォーマンス・可用性属性（SSD 配置・dual copy・PAV 利用）。「速いの遅いの」軸。
- **DataClass (DATACLAS)**: データセット属性（RECFM / LRECL / BLKSIZE / SPACE / DSNTYPE）。「JCL の DCB を肩代わり」軸。
- **ManagementClass (MGMTCLAS)**: バックアップ・退避・期限切れ削除の運用ポリシ。HSM 連携（→ ZOS-RECOVERY-001）。「捨てる残す軸」。
- **StorageGroup (STORGRP)**: 物理 DASD ボリュームの束。最終的な配置先。「どこに置くか」軸。
- **ACS ルーチン**: 4 クラスそれぞれに 1 本ずつあり、`FILTLIST` + `IF/THEN/SET` 風の言語で書く。アロケート要求の都度実行される。
- ACS の **判定順**: DataClass → StorageClass → ManagementClass → StorageGroup（StorageGroup は StorageClass が NULL でないと選ばれない）。
- **SCDS / ACDS / COMMDS**: SMS 設定本体（SCDS = Source Control Data Set）、稼働中複製（ACDS = Active Control Data Set）、シスプレックス通信用（COMMDS = Communication Data Set）の 3 種 VSAM。
- 設定変更は SCDS で編集 → `SETSMS SCDS(...)` で ACDS に反映 → シスプレックス全 LPAR に伝搬。

## 3. prerequisites（理解の前提）

- データセットの DSORG / RECFM / SPACE の意味 — `ZOS-DATASET-001`
- DASD ボリューム概念（VOL=SER） — `ZOS-DASD-001`
- カタログとの関係（SMS-managed は必ずカタログ） — `ZOS-CATALOG-001`
- 一般 IT 知識: ポリシ駆動ストレージ管理（Storage Class on Kubernetes 等と概念は近い）

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-DATASET-001, ZOS-DASD-001, ZOS-CATALOG-001
- `specialized_by`: なし
- `contrasts_with`: 「非 SMS（直接 VOL=SER 指定）」運用との対比
- `used_by`: ZOS-GDG-001（GDG base + SMS DataClass で世代生成）, ZOS-RECOVERY-001（HSM が ManagementClass 経由で migrate）, ZOS-VSAM-001（VSAM の CISIZE 等を DataClass で集中設定）

## 5. pitfalls（実装・運用での落とし穴）

- **ACS ルーチンの順序ミスで意図しない StorageGroup**: ACS は **先頭から順に IF 判定**し、最初に SET された値が採用される。「特殊ルール」を後ろに置くと、前段の包括ルールに食われて永遠に発火しない。「DSN starts with TEMP.* なら作業用 SG」ルールを末尾に置き、前段の `IF &DSN(1) = 'USER'` で全 USER.TEMP.* も general SG に落ちる事故。**例外は先に書く** が鉄則。
- **DataClass の SPACE 上書きが JCL より強い**: DataClass で `SPACE=(CYL,(10,5))` を強制している環境で、JCL に大きめの `SPACE=(CYL,(1000,100))` を書いても **DataClass 値が勝つ**（OVERRIDE 設定次第）。「容量が足りないのは JCL が悪い」と何時間も探した挙句、SMS DataClass で上限張られてた、というのが典型事故。
- **SCDS と ACDS の差分忘れ**: SCDS で編集して `VALIDATE` 通したのに `SETSMS SCDS(...)` を打ち忘れ、本番には反映されてない、または逆に SCDS 直前更新がない状態で `ACTIVATE SCDS` してロールバック不能になる。**変更は必ず SCDS 編集 → VALIDATE → ACTIVATE → ACDS バックアップ → 動作確認** の手順を踏む。
- **StorageGroup 容量逼迫の連鎖**: SG プール枯渇は、ACS が次の候補 SG を探す挙動を持つが、設定によっては **全 SG 横断で `IGD17273I` not enough space** で ABEND。SG 容量モニタを SMF type 42 or RMF で常時可視化していないと、夜間バッチが翌朝になる典型例。
- **GUARANTEED SPACE で空ボリューム喰い潰し**: StorageClass の `GUARANTEED SPACE=YES` を有効にしたデータセットは、SG 内全ボリュームに **空きを確保** しに行く（multivolume primary allocation）。これを大量に作ると、SG 全ボリュームのフラグメンテーション + 空きが見せ掛けで枯れる。本当に必要な VSAM の Primary key 領域だけ。
- **ACS ルーチンの `WRITE` でテスト印字垂れ流し**: ACS デバッグ時の `WRITE 'DEBUG: ' || &DSN` を本番に残すと、SMS LOG（または SYSLOG）に毎アロケート 1 行ずつ垂れ流れ、コンソール spool 逼迫の原因になる。本番デプロイ前 `WRITE` 全削除をチェックリスト化する。
- **SMS pool 移行時の Affinity 残骸**: ボリューム入れ替えで古いボリュームを `DRAIN` した後、`MIGRATE` で全データを別 SG に流したつもりが、Affinity（ボリューム名指定 catalog エントリ）が残っていて参照不能。catalog 側の REPRO / IDCAMS で affinity 解除する手当てが必要。

## 6. examples（具体例）

```jcl
//* SMS-managed の場合、JCL は UNIT/VOL を一切書かない
//OUT DD DSN=USER.PROD.SALES,DISP=(NEW,CATLG,DELETE),
//      DATACLAS=PRODFB80,STORCLAS=STDPERF,MGMTCLAS=STDBKUP,
//      SPACE=(CYL,(10,5))
```

```text
* ACS ルーチン (StorageClass 用) の抜粋
FILTLIST PROD_DSN INCLUDE('USER.PROD.**','PROD.**')
FILTLIST TEMP_DSN INCLUDE('**.TEMP.**','**.WORK.**')

IF &DSN = &TEMP_DSN THEN
  SET &STORCLAS = 'TEMPFAST'
ELSE IF &DSN = &PROD_DSN AND &SIZE > 1000000 THEN
  SET &STORCLAS = 'BIGPROD'
ELSE
  SET &STORCLAS = 'STDPERF'
```

```tso
/* SMS ステータス確認 */
D SMS,SG(ALL)
D SMS,STORCLAS(ALL)
D SMS,DSNAME(USER.PROD.SALES)
```

## 7. decision_axes（採否を分ける判断軸）

- **SMS-managed vs 非 SMS**: 現代の新規環境は SMS 必須。非 SMS は **JCL の VOL=SER 直書き運用** が残る古典系か、テスト用隔離ボリューム。新規アロケートで非 SMS を強行すると将来の HSM/DRP 統合で苦労する。
- **DataClass で DCB 強制 vs JCL で個別指定**: DataClass で集中設定する方が標準化しやすいが、特殊ツール（古い C ランタイム等）が独自 BLKSIZE を要求するとぶつかる。**運用標準は DataClass、例外データセットは JCL 明示**。
- **StorageClass の Tier 分け**: 「SSD/HDD」「dual copy 有無」「PAV 有無」「Cache 優先度」の組合せで Tier を作る。Tier を増やしすぎると ACS ルーチンが破綻、減らすと用途別最適化が効かない。**実運用 3〜5 Tier 程度** が現実解。
- **ACS ルーチンを REXX 風で書く vs 単純 IF 連結**: ACS 言語は REXX サブセット風で `DO/END/SELECT` も書けるが、保守性のため **可能な限り単純 IF/THEN 並びに留める**。複雑分岐を入れると ACS validate でも気付かない trace 困難なバグが入る。
- **SMS-managed VSAM vs 非 SMS VSAM**: VSAM は SMS 配下にした方が CI/CA 設計を DataClass で標準化できる。だが古い CICS file 等で `VOL=SER` を意識的に指定する伝統運用が残ると、混在による Catalog 整合性事故が起きる。**新規 VSAM は SMS、移行は段階的** が安全。

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_TECH_001/002) から SMS 自動クラス選択設計の実運用知識を概念蒸留 (ADR-0109)。書籍は概念補助。
