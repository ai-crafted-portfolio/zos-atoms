---
id: ZOS-OSA-001
title: OSA-Express + FICON / OSM / Hipersockets
status: stable
last_reviewed: 2026-06-02
authors: [agent]
rag_verified: partially
---

# ZOS-OSA-001: OSA-Express + FICON / OSM / Hipersockets

## 1. purpose（なぜ存在するか）

OSA-Express は IBM Z の **ネットワーク・カード機能 (physical NIC)**。z/OS から見ると CHPID (Channel Path ID) として現れ、外部 LAN への接続経路となる。OSA は単一の hardware だが、複数の **CHPID type** をサポートし、z/OS / Linux on Z / z/VM 等から異なる用途で共用できる:

- **OSD (Queued Direct I/O, QDIO)**: 標準 IP 通信、IPAQENET / IPAQENET6 device 形式
- **OSE (non-QDIO)**: 古い OSA、新規構築では使わない
- **OSM (OSA for z/OSMF / Manage)**: HMC 経由の管理 LAN、z/OSMF / Hardware Management 用
- **OSX (OSA for zBX / Ensemble)**: 旧 ensemble 連携、現代ではほぼ使われない
- **OSC (OSA Integrated Console Controller)**: HMC 経由 console、SMCS と組み合わせ

加えて、メインフレーム内部の **Hipersockets (IQD CHPID type)** と **IQDIO (Internal Queued Direct I/O)** が論理 NIC として LPAR 間通信を提供 (memory copy のみ、physical wire 不要、低遅延)。さらに **FICON (Fiber Connection)** は I/O 用 channel (DASD / Tape) で、network ではないが OSA と並ぶ高速 channel として運用設計時に同列で扱う。

Linux / クラウドとの対比:
- Linux (x86): PCI NIC + SR-IOV、virtio-net、Linux network namespace で分離
- AWS: ENI (Elastic Network Interface)、SR-IOV ベースの enhanced networking
- z/OS / IBM Z: **OSA は channel として OS から見える**、CHPID + DEVICE + INTERFACE statement の 3 段で表現、複数 LPAR で同一 OSA port 共有可

OSA 関連障害の特徴: **「physical card 故障は稀、設定不整合と CHPID share の競合が大半」**。CHPID share で「OSA port shared 4 LPAR」運用時、1 LPAR の IPL で他 LPAR 影響、device busy で起動失敗、というシナリオが定番。

## 2. mechanism（どう動くか）

### CHPID と DEVICE
- HCD (Hardware Configuration Definition) で CHPID → CU → DEVICE の階層定義
- OSA-Express は 1 物理ポート = 1 CHPID、1 CHPID 配下に DATAPATH device (data 用) + LCS device (legacy) 等
- IOCDS (I/O Configuration Data Set) に書き込まれ、HMC で activate

### TCP/IP PROFILE.TCPIP 側
- `INTERFACE OSA01 DEFINE IPAQENET PORTNAME OSAPORT IPADDR ...` で z/OS TCP/IP stack と紐付け
- PORTNAME は HCD で定義した OSA port name と一致必須
- VLAN tag は `VLANID nn` で指定

### Hipersockets
- IQD CHPID type、memory-based、CPU 上の virtual L3 switch
- LPAR 間で「同一 IQD CHPID」を share すれば LPAR-LPAR 通信が memory copy で完結 (TCP segment 無し、超低遅延)
- IBM Z 内のみ、外部に出ない (Cloud との連携 / 他社製ハードと通信は不可)
- MTU を大きく (8KB / 32KB / 56KB) 取れる、ただし peer 同士で MTU 合わせる必要

### Shared OSA
- 1 OSA port を複数 LPAR で共有 (LPAR ごとに SHARE / DEDICATE 選択)
- 共有時は OSA 内部に LPAR ごとの queue を持つ、同時 IPL 競合あり
- VMAC (Virtual MAC) を LPAR ごとに割り振って外部スイッチからは別 NIC に見せる

### FICON
- I/O channel (DASD / Tape 接続)、本アトムでは network ではないが運用設計時に同列扱い
- FCB (Fiber Channel) over SAN、Director (Brocade / Cisco MDS) を介在
- Zoning で port 単位の到達性制御、Zoning 漏れで storage アクセス全停止

### OSM
- HMC から z/OSMF への管理 LAN 専用、CHPID type OSM
- OSM 未設定だと z/OSMF Hardware Management 系操作が動かない (LPAR profile 変更等)

## 3. prerequisites

- ZOS-TCPIP-001 (OSA は TCP/IP stack の物理層、INTERFACE で紐付ける)
- ZOS-IPL-001 (HCD / IOCDS 変更は IPL 計画と連動)
- 一般 IT 知識: Ethernet / VLAN / MAC / MTU, SAN zoning

## 4. relations

- `depends_on`: ZOS-TCPIP-001 (TCP/IP stack の物理層として被参照)
- `specialized_by`: なし
- `contrasts_with`: Linux PCI NIC, SR-IOV, AWS ENI, VMware vSwitch
- `used_by`: ZOS-TCPIP-001 (INTERFACE 定義経由), ZOS-CONSOLE-001 (OSC + SMCS), ZOS-ZOSMF-001 (OSM 経由 LPAR 操作)

## 5. pitfalls

詳細は `pitfalls/` 配下。

## 6. examples

詳細は `examples.md`。

## 7. decision_axes

詳細は `decision-axes/` 配下。

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_TECH_001) から OSA / CHPID 共有設計の運用知識を概念蒸留 (ADR-0109)。書籍は概念補助。
