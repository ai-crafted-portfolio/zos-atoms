---
id: ZOS-RMF-001
title: RMF (Resource Measurement Facility)
status: draft
last_reviewed: 2026-06-02
authors: [agent-z4]
rag_verified: false
---

# ZOS-RMF-001: RMF (Resource Measurement Facility)

## 1. purpose（なぜ存在するか）

RMF は z/OS の **計測 + 性能分析の中核基盤**。CPU / Storage / DASD / Channel / CF / WLM 達成度を **3 経路 (Monitor I / II / III)** で収集し、SMF type 70-79 として永続化 + リアルタイム可視化。

ZOS-SMF-001 が「計測ログの汎用基盤」なら、RMF は **SMF type 70-78 を生成する側 + 集計可視化する側**。

Linux 対比: `sar` / `dstat` / `iostat` / Performance Monitor を Sysplex + PR/SM 全体で統合した感じ。

## 2. mechanism（どう動くか）

- **Monitor I**: 15 分 interval、SMF type 70-78 出力
- **Monitor II**: snapshot 系、ISPF / SDSF query、SMF type 79
- **Monitor III**: 1-100 秒粒度、sliding window、VSAM linear buffer
- **Postprocessor (ERBRMFPP)**: SMF 読んで CPU / WLM / CF / Cache report
- **DDS (GPMSERVE)**: HTTPS REST、Grafana / Splunk から query
- **Sysplex Data Server**: 集約 query

## 3. prerequisites（理解の前提）

- ZOS-SMF-001, ZOS-WLM-001, ZOS-PARALLELSYSPLEX-001

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-SMF-001, ZOS-WLM-001, ZOS-PARALLELSYSPLEX-001
- `specialized_by`: なし
- `contrasts_with`: LINUX-SAR-001 (未作成), WIN-PERFMON-001 (未作成)
- `used_by`: ZOS-CAPCALC-001, ZOS-WLM-001, ZOS-OPERLOG-001, ZOS-IRD-001

## 5. pitfalls（実装・運用での落とし穴）

- Mon III 起動漏れで real-time data 空
- RMF Distributed Data Server (DDS) 認可漏れ
- SMF type 70-78 と RMF report の不一致
- PR/SM partition data の time skew
- Mon III VSAM buffer 不足で sliding window 短縮

## 6. examples（具体例）

[examples.md](./examples.md) 参照。STC 起動 / Mon II snapshot / Postprocessor JCL / DDS REST / Workflow Exception を収録。

## 7. decision_axes（採否を分ける判断軸）

- RMF Postprocessor vs DDS REST vs vendor analytics (OMEGAMON/MainView)
- Mon III interval (1 秒 vs 10 秒 vs 100 秒)
- Sysplex Data Server で集約 vs LPAR ごと独立
- Mon III data の SMF 永続化 ON/OFF


## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

本 atom の領域については、IBM 公式 manual を一次出典としつつ、運用事例や設計判断の補強として市販書籍 (BK_MF_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 等の z/OS / メインフレーム関連書籍) からの実装知識を補助的に参照する。逐語引用は禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
