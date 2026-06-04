---
id: ZOS-SCHED-001
title: Batch scheduler (TWS / Control-M / OPC)
status: stable
last_reviewed: 2026-06-02
authors: [agent]
rag_verified: partially
---

# ZOS-SCHED-001: Batch scheduler (TWS / Control-M / OPC)

## 1. purpose（なぜ存在するか）

z/OS の **batch scheduler** は数千〜数万本の JCL Job を **依存関係 + 時刻 + リソース制約** に基づき自動投入する OLTP 終夜運用の中核。代表製品は **IBM TWS（Tivoli Workload Scheduler、旧 OPC）** と **BMC Control-M**、加えて CA / Broadcom Workload Automation 系。基本概念は OPC（Operations Planning and Control）時代から共通。

なぜ JES2/JES3 だけで足りないか: JES（Job Entry Subsystem、→ ZOS-JCL-001 周辺）は **JCL を spool に受け取り Initiator に渡す** 役割で、依存関係 / 時刻待ち / 失敗時 retry / 月次・週次の calendar 制御は持たない。「100 本の job を順番に流す」「先行 job が ABEND したら後続止める」「平日のみ走る」を JCL 内 COND= だけで書くのは限界。scheduler はその上位レイヤ。

Linux なら cron + Airflow / Apache NiFi、Kubernetes なら CronJob + Argo Workflows、AWS なら EventBridge + Step Functions が対応。メインフレーム scheduler の特徴は (a) **数万 job 規模を 1 日内に carry-forward して走らせる plan モデル**、(b) **業務 carrier calendar（祝日 / 半日営業 / 月末）** が複雑、(c) **大規模 batch window**（夜間 8 時間で全業務日次処理）の SLA 制約。

この atom は scheduler の基本概念（Application / Operation / dependency / carry-forward / plan モデル）+ 運用 pitfall を扱う。

## 2. mechanism（どう動くか）

### TWS (Tivoli Workload Scheduler) のオブジェクト
- **Application (TWS) / Job Group (Control-M)**: 業務単位の集合。例: "売上日次処理"
- **Operation (TWS) / Job (Control-M)**: 1 つの実行単位（JCL job 1 本に対応）
- **Dependency**: 先行 Operation 完了待ち（internal / external dependency）
- **Run Cycle / Calendar**: 「平日のみ」「月末」「営業日 + 月初 1 営業日」等の calendar 式
- **Workstation**: job が走る LPAR / 物理ノード（z/OS, Linux, Windows）

### Plan モデル
- **Long-term plan (LTP)**: 数週間〜数ヶ月先の Operation を calendar 展開した plan。
- **Current plan**: 当日（または当日 + 翌日）の plan。実行 status を保持。
- **Daily plan turnover**: 毎日 1 回、長期 plan から当日 plan を再展開（DPLAN-style）+ 未完了 operation を carry-forward。

### 主要 component
- **Controller / Tracker**: TWS の中央 controller（PIF 経由 plan 更新）と LPAR 内 tracker。
- **EQQUX exit**: TWS の event-driven exit。job ABEND / step end / dataset trigger 等。
- **Special resource**: 数値カウンタによる **同時実行制限**（DB2 max 5 件等）

### dependency 制御
- **Internal dependency**: 同 Application 内の Operation 間
- **External dependency**: 別 Application の Operation 待ち（cross-Application）
- **Dataset trigger**: dataset 作成 / DISP=KEEP 完了で次 Operation 起動
- **Manual hold / release**: 運用者が一時停止 / 解放

### 失敗時動作
- ABEND 発生 → TWS が job status `ERROR` → 自動 retry policy 有無 → 後続 operation hold（依存 propagation）→ NetView automation で alert
- 運用者対応: `RERUN`（同 job 再投入）、`COMPLETE`（強制完了扱い）、`HOLD`（依存先停止）

## 3. prerequisites（理解の前提）

- JCL — `ZOS-JCL-001`
- WLM — `ZOS-WLM-001`（job class → Service Class mapping）
- JES2/JES3 spool 概念
- 一般 IT 知識: cron、DAG、ジョブ依存、business calendar

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-JCL-001, ZOS-WLM-001
- `specialized_by`: なし（TWS / Control-M / OPC は同 atom 内 axis 比較）
- `contrasts_with`: Linux cron + Airflow + Apache NiFi, Kubernetes CronJob + Argo Workflows, AWS EventBridge + Step Functions, Windows Task Scheduler + SQL Agent
- `used_by`: ZOS-DB2-001（Db2 utility job 依存）, ZOS-CICS-001（CICS 起動 / 停止 batch）, ZOS-RECOVERY-001（HSM AUTOBACKUP の trigger）, ZOS-CAPCALC-001（batch window MSU 予測）

## 5. pitfalls（実装・運用での落とし穴）

- **Carry-forward でループ**: 完了しなかった Operation が翌日 plan に carry-forward されるが、後続 Operation も依存で carry → 累積で 3 日分の job が同日に走る → spool 逼迫 → 全業務遅延の連鎖。**carry-forward 不可（NO CARRY）を「日次必須完了」job に設定**、または carry 期限（48h）を policy 化。月末月初の事故源。
- **Spool 逼迫で JES2 SOS**: scheduler 投入の job が JES2 spool（SYSOUT + SYSIN）を埋め、`HASP050` SOS (Sub Optimal State) → 新規 job 投入不能 → scheduler retry storm → 完全 hang。**JES2 SPOOL 80% で alert + AUTO PURGE/INACTIVE SYSOUT**、scheduler 側で job 投入 throttle。
- **TWS DAILY plan 取込み漏れ**: 長期 plan の更新（新業務追加 / calendar 変更）後、`EQQDPLAN` が daily turnover で取り込む。turnover の前に plan が確定してないと **新業務が当日走らない** で気付かず翌朝発覚。**plan 変更は turnover の 4 時間前まで確定 + 取込み後の D PLAN で検証**。
- **依存先 Operation 削除で orphan**: 廃止業務の Application を削除しても、後続業務に **external dependency が残ったまま** だと依存先不在で永久 hold。**Application 削除 SOP に「dependency 検索 + 後続 cleanup」を必須**、TWS は `EQQDDEF` で全依存検索可能。
- **Special resource quota の dead lock**: 「Db2 utility 同時 5 件まで」の Special resource に対し、5 件全部が **互いに別 Special resource 待ち** だと dead lock。TWS は dead lock 検出機構が弱く、運用者が 30 分後に気付くまで全停止。**Special resource は単純で互いに独立、循環依存禁止**、monitor の `D LOCK` で 5 分間隔 check。
- **calendar の祝日定義漏れ**: 翌年の祝日が calendar dataset に登録されてないと、年末で **「営業日 = 全日 / 祝日 = なし」** 扱いになり、元日から異常起動。**年末 12 月に翌年 calendar 全件 review + テスト LPAR で long-term plan 再展開**、Golden Week / お盆 / 年末年始は特に注意。
- **scheduler controller 単一障害点**: TWS controller / Control-M EM が単一 LPAR のみで running、その LPAR 障害で全業務スケジュール停止 → 当日 batch 全滅。**Sysplex 構成で controller HA（standby + ARM cross-system restart）**、controller 自体を ARM element 化。
- **job 起動 LPAR の workload skew**: TWS で「どの LPAR で走らせるか」未指定 → JES2 共有 spool 経由で全 job が **同 LPAR** に集中。**LPAR 毎に job class を分散 + workstation 設定で明示 routing**、JES2 routing が偏ると 1 LPAR の CPU 100% + 他 LPAR 遊休。

## 6. examples（具体例）

```text
* TWS Application 定義例 (概念)
Application: SALES_DAILY
  Run Cycle: Weekdays + Excluding holidays
  Operations:
    01 SALES_EXTRACT (job=SALEEXT)
       Predecessors: (none)
       Successors: 02
       Special resource: DB2_UTIL (qty=1)
    02 SALES_TRANSFORM (job=SALETRN)
       Predecessors: 01
       Successors: 03
    03 SALES_LOAD (job=SALELOD)
       Predecessors: 02
       External dep: PROD_DB2_READY (from APP: DB2_HEALTHCHK)
       Carry-forward: YES
```

```text
* TWS 運用 command (TSO 経由)
TSO EQQYRPRC  -- バッチ Plan ユーティリティ
TSO EQQYHRPT  -- 失敗 Operation report
TSO EQQE6510  -- 当日 Plan 表示

* Operation 状態確認
D APPL,APPLID=SALES_DAILY
D OPER,OPNO=02,APPLID=SALES_DAILY

* 手動 RERUN / COMPLETE
F TWS,RERUN,APPLID=SALES_DAILY,OPNO=02
F TWS,COMPLETE,APPLID=SALES_DAILY,OPNO=02
```

```text
* Control-M Job 定義例 (概念、XML 抜粋)
<JOB JOBNAME="SALEEXT" APPLICATION="SALES_DAILY"
     MEMNAME="SALEEXT" SUB_APPLICATION="EXTRACT"
     SCHEDULING_ENVIRONMENT="WEEKDAYS"
     MAXRERUN="3" CYCLIC="N">
  <INCOND NAME="DB2_READY" ODATE="ODAT"/>
  <OUTCOND NAME="SALEEXT_DONE" ODATE="ODAT" SIGN="ADD"/>
  <QUANTITATIVE NAME="DB2_UTIL" QUANT="1"/>
</JOB>
```

```text
* Special resource (TWS) 定義
RESOURCE NAME=DB2_UTIL,QUANTITY=5
RESOURCE NAME=TAPE_MOUNT,QUANTITY=3
RESOURCE NAME=BATCH_WINDOW_LIMIT,QUANTITY=200

* 当日 quota 確認
D RES,NAME=DB2_UTIL
```

## 7. decision_axes（採否を分ける判断軸）

- **TWS vs Control-M vs OPC 残置**: TWS は IBM 純正で z/OS 統合が深い、Control-M はマルチプラットフォーム（z/OS + Linux + Windows + Cloud 混在）に強い、OPC は legacy（TWS の旧名）。**z/OS 単独 + IBM 一社契約 = TWS、ハイブリッド業務 = Control-M、新規導入は TWS or Control-M**、OPC 残置はサポート切れ目で TWS 移行。
- **DAILY plan turnover 時刻**: 標準は深夜 0:00 / 4:00 / 6:00。**業務日次の境界（営業日切替）** に合わせる、24 時間 OLTP は turnover 時の plan refresh で短時間停止リスク。
- **Special resource 設計**: 物理リソース（tape mount, MQ qmgr connection）と論理リソース（同時実行制限）の 2 系統。**物理は実 capacity、論理は SLA 設計値**、過小設定で thoughput 不足、過大で resource contention。
- **業務 calendar の粒度**: 「営業日」「月末」「四半期末」「年度末」の階層。**業務サイクル + 国別カレンダー（日本祝日 / 米国 holidays）+ 内部営業日カレンダーの 3 層管理**、Golden Week / Thanksgiving の独立 calendar 必須。
- **失敗時の自動 RERUN policy**: 全 job auto-retry vs 特定 job のみ auto-retry vs 全部手動。**冪等 job（idempotent）のみ auto-retry、副作用ある job は手動**、retry 3 回まで等の policy 化。
- **scheduler controller HA**: 単一 controller（運用簡素 + 障害時手動切替）vs HA + ARM cross-system restart（複雑 + 自動切替）。**業務 SLA 99.9% 以上 = HA 必須、24 時間 OLTP は controller 障害が全業務影響なので HA 一択**。
- **cross-platform 統合**: z/OS scheduler が Linux / Windows job も併せて管理する vs platform 毎 scheduler 分離。**業務フローが platform 跨ぐ場合 (z/OS 集計 → Linux ML → Windows 報告) は統合、独立業務は分離**、Control-M の優位領域。

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_TECH_002) からジョブスケジューラ設計の運用知識を概念蒸留 (ADR-0109)。逐語引用禁止。
