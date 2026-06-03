---
title: ZOS-TCPIP-001
description: PROFILE.TCPIP、HOME / GATEWAY / PORT、Stack 内 TN3270/FTP/Telnet、`netstat`
tags:
  - Network
  - Security-Network
---
# ZOS-TCPIP-001: TCP/IP for z/OS

## 1. purpose（なぜ存在するか）

z/OS Communications Server の TCP/IP スタックは、メインフレーム上の **オープンプロトコルへの窓口**。SNA/VTAM が CICS/IMS のレガシー資産を担うのに対し、TCP/IP は (a) FTP / TN3270 / Telnet 等の伝統的 TCP アプリ、(b) HTTP/HTTPS (IBM HTTP Server, Liberty profile WAS), (c) AT-TLS / IPSec / SAF-protected resolver、(d) Policy Agent ベースの QoS / IDS / IP filtering を提供する。

歴史的経緯から **「VTAM とは別 STC、しかし VTAM とは強く連動」** (VTAM の IUTSAMEH device で SAMEHOST 通信、Sysplex Distributor は XCF 経由で他 LPAR 通信)、**1 LPAR で複数 TCP/IP stack を立てられる** (HOSTNAME / VIPA 単位で stack 分離)、という独自性がある。Linux のように 1 OS = 1 TCP/IP stack ではない。

Linux / クラウドとの対比:
- Linux: `/etc/network/interfaces` + systemd-networkd + nftables、1 OS = 1 stack、network namespace で分離
- AWS: VPC + Subnet + Security Group、stack は EC2 OS 内、CloudFormation でコード化
- z/OS TCP/IP: **PROFILE.TCPIP** 1 ファイルが stack 設定の中核、HOME / GATEWAY / PORT / VIPADYNAMIC / IPCONFIG が並ぶ、`netstat` + `D TCPIP,,NETSTAT,...` の二刀流

**「業務影響大の z/OS 障害」は近年は TCP/IP 起因が圧倒的に増えた**。理由は (a) AT-TLS 証明書期限切れ、(b) Sysplex Distributor VIPADYN 不整合、(c) Policy Agent 反映漏れ、(d) Resolver.cnf 順序間違い、(e) PORT 占有による start 失敗、等の **「設定ファイル系」障害が運用負荷の中心** だから。

## 2. mechanism（どう動くか）

### TCP/IP stack 起動
- STC として `S TCPIP` (or 個別 procname) で起動
- 参照 dataset 階層:
  - `//PROFILE   DD DISP=SHR,DSN=TCPIP.PROFILE.TCPIP`
  - `//SYSTCPD   DD DISP=SHR,DSN=TCPIP.TCPIP.DATA` (resolver)
  - SYS1.PARMLIB(BPXPRMxx) で OMVS が TCP/IP に依存

### PROFILE.TCPIP の主要 statement
- `HOSTNAME`: stack のホスト名
- `IPCONFIG`: IPv4 設定 (DATAGRAMFWD, IGNOREROUTERHELLO, SOURCEVIPA)
- `IPCONFIG6`: IPv6 設定
- `HOME`: ローカル IP アドレス + interface 名割当て
- `GATEWAY`: 静的ルーティング (古い形式)、新規は `BEGINROUTES` / `ENDROUTES`
- `PORT`: ポート割当て (`23 TCP TELNET` 等)、`JOBNAME` で予約
- `VIPADYNAMIC` / `VIPABACKUP`: Sysplex Distributor 動的 VIPA
- `INTERFACE`: 物理 NIC (OSA) との接続定義
- `START`: stack 起動時に自動起動する device

### 並列 stack
- 1 LPAR で `TCPIP` / `TCPIP2` / `TCPIP3` のように複数 stack 起動可
- 用途分離 (本番 / DR テスト / DMZ 系の分離)、ただし resolver 設定 + アプリの BIND 指定が複雑化

### Resolver (`TCPIP.DATA`)
- DNS lookup の設定、`TCPIPJOBNAME`, `NSINTERADDR`, `DOMAINORIGIN`, `DATASETPREFIX`
- アプリは `SYSTCPD` DD 経由 / 環境変数 `RESOLVER_CONFIG` 経由 / system-level default で参照
- 「resolver.conf が 3 つの場所で異なる定義」が運用事故の温床

### コマンド
- `D TCPIP,,STOR` (stack のストレージ使用)
- `D TCPIP,,NETSTAT,CONN` (active connection)
- `D TCPIP,,NETSTAT,HOME` (HOME 一覧)
- `D TCPIP,,NETSTAT,DEV` (device 一覧)
- `D TCPIP,,SYSPLEX,VIPADYN` (VIPADYNAMIC 状況)
- `V TCPIP,,OBEYFILE,DSN=TCPIP.PROFILE.UPDATE` (動的設定変更)
- `V TCPIP,,SYSPLEX,QUIESCE` (LPAR を Sysplex Distributor から除外)

### Sysplex Distributor
- 同 sysplex 内の複数 z/OS LPAR が同一 VIPA を共有 (active/active のロードバランサ)
- 1 LPAR が distributor 役 (DISTMETHOD で BASEWLM / SERVERWLM / ROUNDROBIN)
- XCF で stack 間通信、HEARTBEAT で障害検知

## 3. prerequisites

- ZOS-USS-001 (USS が TCP/IP に依存、起動順依存)
- 一般 IT 知識: TCP/IP basics (IP / port / route table)、DNS の lookup 経路、TLS handshake の基本
- ZOS-CONSOLE-001 (`D TCPIP` コマンドは MVS console から)

## 4. relations

- `depends_on`: ZOS-USS-001 (相互依存)
- `specialized_by`: ZOS-OSA-001 (物理層: OSA-Express / Hipersockets), ZOS-AT-TLS-001 (TLS 透過化), ZOS-EE-001 (SNA over IP), ZOS-FTP-001 (アプリ層)
- `contrasts_with`: Linux TCP/IP stack, AWS VPC + Subnet, Azure VNet
- `used_by`: ZOS-FTP-001, ZOS-AT-TLS-001, ZOS-EE-001, ZOS-ZOSMF-001 (web 経由), ZOS-WAS-001 (HTTP), ZOS-ANSIBLE-001 (SSH)

## 5. pitfalls

詳細は `pitfalls/` 配下。

## 6. examples

詳細は `examples.md`。

## 7. decision_axes

詳細は `decision-axes/` 配下。
