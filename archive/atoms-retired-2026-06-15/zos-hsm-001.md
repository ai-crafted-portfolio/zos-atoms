---
id: ZOS-HSM-001
title: DFSMShsm + tape hierarchy
status: draft
last_reviewed: 2026-06-02
authors: [agent-z4]
rag_verified: false
---

# ZOS-HSM-001: DFSMShsm + tape hierarchy

## 1. purpose（なぜ存在するか）

DFSMShsm（**Data Facility Storage Management Subsystem - Hierarchical Storage Manager**、以下 HSM）は、z/OS の **ストレージライフサイクル自動管理基盤**。データセットを「使われている／使われなくなった」で **ML0 / ML1 / ML2** の 3 階層に自動降格・自動再昇格させ、高単価 DASD を高頻度データに集中させる。

ZOS-RECOVERY-001 が「バックアップ + DR の概観」を扱うのに対し、本アトムは **HSM 内部の運用詳細**（ARCCMD parameter / CDS 3 種 / Recall 経路 / ABARS aggregate） に踏み込む。

Linux / クラウド対比: AWS S3 の **lifecycle policy + Glacier transition** や、Linux のディスク階層化 (`lvmthin` + DRBD + tape) を **手で組み合わせる**。HSM の特異性は **SMS の ManagementClass と統合**されている点。

## 2. mechanism（どう動くか）

### 階層構造
- **ML0**: Primary、active DASD
- **ML1**: 別 DASD、compressed、SDSP で小データセット集約
- **ML2**: tape / VTL / Cloud Tape

### CDS 3 種類
- MCDS (Migration) / BCDS (Backup) / OCDS (Offline)、全 VSAM KSDS、JES journal で update 記録

### ARCCMD parm
- SETSYS / DEFINE / ADDVOL を SYS1.PARMLIB(ARCCMD00) で宣言

### ABARS
- 業務単位の dataset group を 1 aggregate として ABACKUP / ARECOVER

## 3. prerequisites（理解の前提）

- ZOS-SMS-001, ZOS-DATASET-001, ZOS-RECOVERY-001, ZOS-VSAM-001

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-SMS-001, ZOS-DATASET-001, ZOS-RECOVERY-001, ZOS-VSAM-001
- `specialized_by`: ZOS-TAPE-001
- `contrasts_with`: LINUX-LVMTHIN-001 (未作成), AWS-S3-LIFECYCLE-001 (未作成)
- `used_by`: ZOS-RECOVERY-001, ZOS-OPERLOG-001, ZOS-CAPCALC-001

## 5. pitfalls（実装・運用での落とし穴）

- CDS バックアップ忘れで ARC0040I HSM 全滅
- Recall storm でユーザ業務停止 (ARC0734I 大量)
- ML2 tape mount 待ちで批処理 hang
- Migrate2 優先度逆転で運用フロー破綻
- ABARS で aggregate 定義漏れ、災対 ARECOVER で欠損
- SDSP overflow で小データセット migrate 不能

## 6. examples（具体例）

[examples.md](./examples.md) 参照。ARCCMD parm / HMIGRATE / HRECALL / ABARS / CDS バックアップ JCL を収録。

## 7. decision_axes（採否を分ける判断軸）

- ML2 = 物理 tape vs VTL (TS7700) vs Cloud Tape
- ABARS aggregate vs DFSMSdss DUMP for DR
- Recall on OPEN vs プレ recall（バッチ事前準備）
- HSM 単一インスタンス vs HSMplex

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_TECH_001/002) から DFSMShsm 階層管理の実運用知識を概念蒸留 (ADR-0109)。書籍は概念補助。
