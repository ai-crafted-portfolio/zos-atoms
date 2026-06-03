---
title: ZOS-NETVIEW-001
description: NetView automation、SOA、CLISTs、event correlation、CNMNETOP
tags:
  - Monitor
  - Storage-Monitor
---
# ZOS-NETVIEW-001: NetView + automation

## 1. purpose（なぜ存在するか）

NetView for z/OS は **メッセージ駆動の自動運用 + 中央オペレーション基盤**。WTO/WTOR、SNMP trap、OPERLOG msg を受信し、automation table (AT) + CLIST / REXX で event-driven response を実装。

ZOS-CONSOLE-001 が msg 発生側、ZOS-OPERLOG-001 が永続化側なら、本アトムは **action を起こす層**。

Linux 対比: Nagios/Zabbix + Ansible runbook を z/OS 内で統合した感じ。SA z/OS は NetView 上の application layer で subsystem dependency を宣言的に扱う。

## 2. mechanism（どう動くか）

- **NetView STC**: CNMPROC 起動
- **DSIPARM**: parmlib 相当の dataset
- **automation table (AT)**: msgid pattern → EXEC CLIST
- **CLIST / REXX**: action 実装
- **MPF**: msg を NetView に AUTOMATE flag で route
- **SA z/OS**: subsystem 起動順 / 障害時 restart の policy DB
- **CNMNETOP**: operator login task
- **DSI6DST**: cross-domain task

## 3. prerequisites（理解の前提）

- ZOS-CONSOLE-001, ZOS-OPERLOG-001

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-CONSOLE-001, ZOS-OPERLOG-001
- `specialized_by`: なし
- `contrasts_with`: NAGIOS-PLUGIN-001 (未作成), SPLUNK-ALERT-001 (未作成)
- `used_by`: ZOS-ARM-001, ZOS-HSM-001, ZOS-CICS-001, ZOS-IMS-001, ZOS-DB2-001, ZOS-RMF-001

## 5. pitfalls（実装・運用での落とし穴）

- Automation table 反映漏れで msg 抑制動かず
- CLIST ループ暴走で NetView 内 task 詰まる
- NetView outdated に対する OMEGAMON 代替検討漏れ
- Cross-domain message routing 漏れで遠隔 alert 不達
- MPF SUPPRESS で重要 msg が NetView に届かない

## 6. examples（具体例）

[examples.md](./examples.md) 参照。AT / CLIST(REXX) / MPFLSTxx / CNMNETOP cmd / SA policy DB を収録。

## 7. decision_axes（採否を分ける判断軸）

- NetView 維持 vs OMEGAMON/MainView 全面移行 vs modern AIOps
- Automation table (AT) vs CLIST/REXX vs SA z/OS policy DB
- Cross-domain = SNA APPN/EE vs IP REST 経路
- Automation 配置 = NetView 一極 vs SA z/OS policy DB vs ARM 連携の責任分担
