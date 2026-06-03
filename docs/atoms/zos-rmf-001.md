---
title: ZOS-RMF-001
description: Mon I / II / III、`ERBRMFPP`、PR/SM partition data、Spreadsheet Reporter
tags:
  - Monitor
  - Storage-Monitor
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
