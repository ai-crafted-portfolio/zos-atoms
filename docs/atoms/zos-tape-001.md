---
id: ZOS-TAPE-001
title: Tape / VTL (TS7700, Cloud Tape)
status: draft
last_reviewed: 2026-06-02
authors: [agent-z4]
rag_verified: false
---

# ZOS-TAPE-001: Tape / VTL (TS7700, Cloud Tape)

## 1. purpose（なぜ存在するか）

z/OS の **テープ層**（物理テープ + VTL + Cloud Tape）は、HSM ML2 / バックアップ / 長期保管 / DR オフサイトの **物理 backbone**。本アトムは ZOS-HSM-001 から見たときの「ML2 物理層」を独立に切り出し、テープ volume の確保・配置・マウント運用・障害切り分けを扱う。

Linux / クラウド対比: Linux 世界では tape は **LTFS で file system 化** することが多く、AWS S3 Glacier が概念的に z/OS の Cloud Tape に近い。z/OS 側は **TMS (CA-1 / RMM / Control-M Tape) が必須**、これ無しの z/OS テープ運用は事実上不可能。

## 2. mechanism（どう動くか）

- VOLSER (6 文字英数) で識別、TMS DB が retention / 所有者を管理
- scratch / private pool 分離
- 業務単位 pool 分け
- TS7700 grid (2-4 site DASD-backed VTL)
- Cloud tier (TS7700 V8+ で AWS S3 / IBM COS backed)
- MOUNT: `IEC501A` mount 要請、`IEC502E` allocation 失敗

## 3. prerequisites（理解の前提）

- ZOS-DATASET-001, ZOS-DASD-001, ZOS-HSM-001, ZOS-JCL-001

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-DATASET-001, ZOS-DASD-001, ZOS-JCL-001
- `specialized_by`: なし
- `contrasts_with`: LINUX-LTFS-001 (未作成), AWS-S3-GLACIER-001 (未作成)
- `used_by`: ZOS-HSM-001, ZOS-RECOVERY-001, ZOS-OPERLOG-001, ZOS-FTP-001

## 5. pitfalls（実装・運用での落とし穴）

- Scratch pool 枯渇で MOUNT 待機
- TS7700 grid 障害で remote copy 停止
- Cloud tier latency 過小評価で recall SLA 違反
- VOLSER 重複で MEM mount 失敗
- TMS DB と OAM / catalog 不整合で「テープあるのに読めない」

## 6. examples（具体例）

[examples.md](./examples.md) 参照。書込み JCL / scratch report / TS7700 LI REQ / cloud tier 確認 / EJECT 等を収録。

## 7. decision_axes（採否を分ける判断軸）

- 物理 tape vs VTL (TS7700) vs Cloud Tape
- TMS = CA-1 vs RMM vs Control-M Tape
- Sync copy vs Deferred copy (TS7700 grid)
- Tape pool 細分化粒度（業務単位 vs 統合）

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_TECH_002) からテープ媒体運用の実運用知識を概念蒸留 (ADR-0109)。逐語引用禁止。
