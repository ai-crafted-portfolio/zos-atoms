---
id: ZOS-RECOVERY-001
title: バックアップ + DR（DFSMShsm / DFSMSdss / DRP）
status: stable
last_reviewed: 2026-06-01
---


# ZOS-RECOVERY-001: バックアップ + DR

## 1. purpose（なぜ存在するか）

z/OS のバックアップは **3 階層**: (a) **DFSMSdss** によるフルバックアップ / リストア、(b) **DFSMShsm** による多段ライフサイクル（active → migrate level 1 DASD → migrate level 2 tape/cloud）の自動管理、(c) **DR（Disaster Recovery）** としてのオフサイト退避 + 災対機リストア手順。

Linux / クラウドなら `rsync + tape`, `restic`, `S3 + Glacier` 等の組合せで階層化するが、z/OS では **HSM が SMS の ManagementClass と統合されており、データセット属性に「いつ migrate するか・どこに行くか」を貼って自動運用** できる。バックアップは別個ツールではなく **ストレージ管理の延長**。これが SMS 必須の理由でもある（→ [ZOS-SMS-001](zos-sms-001.md)）。

DR は別物。HSM の migrate / backup は「同一サイト内」のライフサイクルであり、サイト全焼に備えるには **HSM の ABACKUP（Aggregate Backup）** か **DFSMSdss DUMP のオフサイト輸送**、または **GDPS（Geographically Dispersed Parallel Sysplex）** によるリアルタイム同期が要る。HSM だけで DR を済ませようとして本番焼失で詰む事例が知られている。

## 2. mechanism（どう動くか）

### DFSMSdss
- バッチ utility（PGM=ADRDSSU）。データセット / ボリューム単位の **DUMP / RESTORE / COPY / DEFRAG**。
- 制御文 `DUMP DATASET(INCLUDE(USER.PROD.**)) OUTDDNAME(BACKUP)`
- 出力先は通常テープ / DASD 上の大型データセット。
- バックアップは **論理 (LOGICAL)** または **物理 (PHYSICAL)** モード。論理は DSN ベース（カタログ前提）、物理はトラックイメージ。

### DFSMShsm
- 常駐 STC（Started Task）として 24/7 動く。
- **3 階層**: Primary (active DASD) → ML1 (Migration Level 1, 別 DASD) → ML2 (Migration Level 2, tape / virtual tape / Cloud)。
- **migrate**: 未使用日数 (LAST_REFERENCED) や ManagementClass の MIGRATION ATTRIBUTES に従って自動降格。
- **recall**: 参照されると自動上昇（ML2 → ML1 → Primary）。`HRECALL` コマンドでも手動可能。
- **backup**: `HBACKDS dsname` でデータセット単位、`AUTOBACKUP` で日次。世代数（VERSIONS）保持。
- **ABARS (Aggregate Backup And Recovery Support)**: 業務単位の DSN グループをまとめてバックアップ + DR 用にオフサイト転送。`ABACKUP` / `ARECOVER`。
- **CDS（Control Data Set）**: HSM のメタデータ。MCDS / BCDS / OCDS の 3 VSAM。これが壊れると HSM が死ぬ。

### DR
- **Tier 1 (現代の標準)**: GDPS + PPRC / XRC でメトロ / グローバルにリアルタイム複製。RPO 数秒 / RTO 数十分。
- **Tier 2**: ABARS でオフサイトテープ輸送、災対機で ARECOVER。RPO 24h / RTO 数時間〜半日。
- **Tier 3**: DFSMSdss DUMP テープを宅配輸送、災対機で RESTORE。RPO 24h+ / RTO 1〜2 日。

## 3. prerequisites（理解の前提）

- データセット概念 — [ZOS-DATASET-001](zos-dataset-001.md)
- DASD ボリューム — [ZOS-DASD-001](zos-dasd-001.md)
- SMS の ManagementClass — [ZOS-SMS-001](zos-sms-001.md)
- カタログ（migrate 後は catalog が ML1/ML2 を指す） — [ZOS-CATALOG-001](zos-catalog-001.md)
- 一般 IT 知識: RPO / RTO の概念

## 4. relations（他アトムとの繋がり）

- `depends_on`: [ZOS-DATASET-001](zos-dataset-001.md), [ZOS-DASD-001](zos-dasd-001.md), [ZOS-SMS-001](zos-sms-001.md)
- `specialized_by`: なし（dss / hsm / GDPS は axis 内別ツール）
- `contrasts_with`: Linux の `rsync` / `restic` / クラウドオブジェクトストレージ tier 化, Windows VSS / Azure Backup
- `used_by`: [ZOS-GDG-001](zos-gdg-001.md)（GDS の世代別 migrate）, [ZOS-VSAM-001](zos-vsam-001.md)（VSAM の backup + RLS）, [ZOS-DB2-001](zos-db2-001.md)（Db2 image copy は別系統だが HSM tier に乗せる事例多い）

## 5. pitfalls（実装・運用での落とし穴）

- **Recall storm でユーザ業務停止**: 大量データセットが一斉に ML2 → Primary に recall されると、テープ I/O が詰まり全 recall 待ち。月初の集計ジョブが「半年眠った GDG 全世代」を `(0)〜(-180)` で参照、全部 ML2 から呼び戻して数時間停止、が典型事故。コンソールが `ARC0734I` (recall failed, retry pending) で埋まる。**recall 同時実行数（MAXRECALLTASKS）** を業務時間帯で絞る運用。
- **CDS バックアップ忘れで HSM 全滅**: MCDS / BCDS が壊れると、ML1/ML2 上のデータが「どこに何があるか」を HSM が知らなくなる。物理データは生きてるのに参照不能（`ARC0040I` CDS read error がコンソールに出続け、HSM STC が機能停止）。**CDS は日次 BACKUP（HSM 内自動 + DSS による 2 重保険）** が必須。
- **ABACKUP の Aggregate Definition が陳腐化**: 業務追加時に Aggregate Group 定義 (`AGGREGATE` PGM=ARCBJRNL) を更新し忘れ、新規業務が DR スコープ外。**月次 / 四半期で AGGREGATE 棚卸し** が運用 SOP。
- **migrate vs migrate2 の優先付け間違い**: ML1 (DASD) は速いが容量小、ML2 (tape) は遅いが容量大。ManagementClass で「ML1 で 7 日保持 → ML2 へ」が標準だが、巨大 GDG を ML1 で長期間保持して ML1 容量枯渇 + 新規 migrate 失敗（`ARC0184I` migrate failed - no space）→ Primary 枯渇（`IGD17273I` insufficient space）→ アロケート失敗の連鎖。**ML1 の使用率モニタが必須**。
- **DR テープのオフサイト戻し忘れ**: 災対演習でテープを取り寄せて、戻すのを忘れる。次の災害時にオフサイトに無い。**テープ受払表とロジ管理がインフラ部門の本気度のリトマス試験紙**。
- **DR 演習を「演習用システム」でしかやらない**: 「本番カタログを丸ごと災対機にリストアしてアプリ起動」を一度もやらないと、本番災害時に動かない。**少なくとも年 1 回、フル DR 演習** + 結果の RTO 実測。
- **SMF ログを HSM migrate して障害解析時に recall 嵐**: SMF dump データセットを ML2 に migrate しておくと、障害解析で過去 1 ヶ月分参照 → 全 ML2 recall。**SMF アーカイブは HSM 階層から除外** または別 ManagementClass で「migrate しない」運用。
- **ABEND リカバリと DR の混同**: 業務 ABEND の復旧（GDG 1 個 RESTORE）と「サイト全焼の災対」を同じ手順書に混ぜると、双方が機能しない。**手順書は別建て**、頻度別に検証も別。

## 6. examples（具体例）

```jcl
//* DFSMSdss DUMP（論理バックアップ）
//DUMP EXEC PGM=ADRDSSU
//SYSPRINT DD SYSOUT=*
//BACKUP   DD DSN=USER.BACKUP.D20260601,DISP=(NEW,CATLG),
//            SPACE=(CYL,(500,100)),UNIT=TAPE
//SYSIN    DD *
  DUMP DATASET(INCLUDE(USER.PROD.**)) -
       OUTDDNAME(BACKUP) -
       COMPRESS -
       OPTIMIZE(4) -
       TOLERATE(ENQF)
/*
```

```jcl
//* DFSMSdss RESTORE（単一データセット復旧）
//REST EXEC PGM=ADRDSSU
//SYSPRINT DD SYSOUT=*
//BACKUP   DD DSN=USER.BACKUP.D20260601,DISP=SHR,UNIT=TAPE
//SYSIN    DD *
  RESTORE DATASET(INCLUDE(USER.PROD.SALES)) -
          INDDNAME(BACKUP) -
          REPLACE
/*
```

```text
* HSM コマンド例
HMIGRATE 'USER.PROD.SALES.G0123V00'      /* 手動 migrate */
HRECALL  'USER.PROD.SALES.G0123V00'      /* 手動 recall */
HBACKDS  'USER.PROD.SALES.G0123V00'      /* バックアップ */
HSEND    LIST DSN('USER.PROD.SALES.**')  /* 状態確認 */

* ABACKUP
HSEND    ABACKUP AGGRGROUP(SALES_AGG)
HSEND    ARECOVER AGGRGROUP(SALES_AGG) DATE(2026,06,01)
```

## 7. decision_axes（採否を分ける判断軸）

- **dss DUMP vs HSM BACKUP**: dss は単発フル、HSM はライフサイクル統合。**業務システム全体は HSM、災対メディア化は dss + ABARS** のハイブリッドが標準。
- **ML1 (DASD) vs ML2 (tape) vs Cloud Tier**: 7 日未満は Primary、7〜30 日は ML1、それ以上は ML2 が古典。近年は ML2 をクラウドオブジェクト（TS7700 連携 / DS8900F + 物理タイアウト）に置く事例増。**RPO/RTO + 容量 + コストの 3 軸最適化**。
- **AUTOBACKUP vs 業務側 IMAGECOPY**: HSM の AUTOBACKUP は データセット単位、Db2 IMAGECOPY は表領域単位 + 整合性保証。**Db2 は IMAGECOPY、それ以外は HSM** が住み分け。
- **DR Tier 1 (GDPS) vs Tier 2 (ABARS) vs Tier 3 (テープ宅配)**: GDPS は導入コスト高 + 専用回線必須、Tier 2 はテープ I/O ベース、Tier 3 は最廉価。**事業継続要件（RTO / RPO）から逆算**して投資判断する。「DR が無い」サイトは皆無、「DR が機能してない」サイトは無数。
- **VERSIONS 数の設計**: HSM BACKUP の世代保持数。3 世代 = 3 日分、過剰だと容量、過小だと「2 日前の誤更新」リカバリ不能。**業務 RPO + 監査要件で決める**。
- **演習頻度**: 年 1 回フル DR 演習が標準（ISO 22301 等）、四半期で部分演習、月次でデータセット単位 RESTORE 訓練。**「やってない」は監査指摘事項**。
