---
title: ZOS-OPERLOG-001
description: SYSLOG dataset、OPERLOG (Coupling Facility logstream)、検索方法 (SDSF LOG)、IXGCNF
tags:
  - Monitor
  - Storage-Monitor
---
# ZOS-OPERLOG-001: OPERLOG + SYSLOG + log stream

## 1. purpose（なぜ存在するか）

z/OS の **メッセージログ統合基盤**: SYSLOG (LPAR ローカル / JES SPOOL), OPERLOG (Sysplex 統合 / CF logstream), System Logger logstream (汎用 logging 基盤)。

ZOS-CONSOLE-001 が WTO 発生側なら、本アトムは **永続化 + 横断検索側**。

Linux 対比: journald + rsyslog + CloudWatch Logs に相当、ただし CF logstream で Sysplex 共有が OS 機能。

## 2. mechanism（どう動くか）

- **SYSLOG**: JES2/JES3 SPOOL data set、LPAR ローカル、$T LOG,SWITCH
- **OPERLOG**: System Logger の CF logstream、Sysplex 統合、SDSF `LOG O`
- **System Logger (IXGLOGR)**: CF logstream / DASD-only logstream、IXGCNFxx parmlib
- **HARDCOPY 設定**: CONSOLxx で DEVNUM(OPERLOG) 指定必要

## 3. prerequisites（理解の前提）

- ZOS-PARALLELSYSPLEX-001, ZOS-DATASET-001, ZOS-CONSOLE-001

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-PARALLELSYSPLEX-001, ZOS-DATASET-001, ZOS-CONSOLE-001
- `specialized_by`: なし
- `contrasts_with`: LINUX-JOURNALD-001 (未作成), AWS-CLOUDWATCH-LOGS-001 (未作成)
- `used_by`: ZOS-NETVIEW-001, ZOS-RRS-001, ZOS-DUMP-001, ZOS-HSM-001, ZOS-CICS-001

## 5. pitfalls（実装・運用での落とし穴）

- SYSLOG full で SWITCH 失敗、msg 紛失
- OPERLOG logstream stagger setting 不適切で signaling 偏重
- LOG offload 失敗で CF 構造逼迫
- SDSF LOG retrieve 時間範囲漏れで「msg が無い」誤判定
- CONSOLxx で HARDCOPY DEVNUM(OPERLOG) 漏れで OPERLOG 空

## 6. examples（具体例）

[examples.md](./examples.md) 参照。CONSOLxx / IXGCNF / CFRM policy / LOGR couple data set / SDSF / D LOGGER / IPCS MERGE を収録。

## 7. decision_axes（採否を分ける判断軸）

- OPERLOG vs SYSLOG (Sysplex 統合 vs LPAR ローカル)
- CF logstream vs DASD-only logstream
- SDSF LOG vs IPCS MERGE vs Splunk forwarder for cross-LPAR 検索
- Retention 設計 = OPERLOG logstream 単体 vs SMF Type 88 永続化 vs 外部 long-term
