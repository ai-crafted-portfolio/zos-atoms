---
title: ZOS-EE-001
description: EE node、IPNET、HPR (High Performance Routing)、APPN backbone
tags:
  - Network
  - Security-Network
---
# ZOS-EE-001: Enterprise Extender (SNA over IP)

## 1. purpose（なぜ存在するか）

Enterprise Extender (EE) は、**SNA session を IP network 上で運ぶための encapsulation 機構**。物理層に SNA 専用設備 (SDLC, Token Ring, FDDI 等の古い hardware) を持たず、既存の IP backbone をそのまま使って CICS / IMS の SNA session を到達させる。

歴史的経緯: 1990 年代後半、企業 backbone が IP 化される中で、SNA 専用 link を持ち続けるコストが許容されなくなった。Cisco の SNASw (SNA Switching Services) や IBM の AnyNet 等の競合があったが、EE が標準化 (RFC 2353 → IBM Communications Server 実装) で生き残った。**現代では Subarea SNA → APPN/HPR → EE が新規構築の標準経路**。

技術的本質: EE は APPN/HPR の上に乗る、APPN routing で「IP の隣接 EE node」が見えるトポロジ、HPR の RTP がエンドツーエンドの session を運ぶ。SNA session の品質を IP 上で保つために QoS (DSCP marking) と HPR の adaptive rate-based congestion control が組み合わさる。

Linux / クラウドとの対比:
- Linux: SNA emulation 自体が業務用途で成立しない、EE 相当を Linux で受ける手段はほぼ無い
- Cloud / AWS: SNA を Cloud に持ち込めない、Direct Connect 経由でオンプレ z/OS との EE 通信が成立する場合は EE 自体は z/OS 側で完結
- z/OS EE: 標準実装、VTAM + TCP/IP stack の協調、UDP 12000-12004 ポートを 5 段階優先度で使い分け

EE は「**既存 SNA アプリ (CICS / IMS / TSO) を改修せずに IP backbone へ乗せる**」延命戦略の中核。新規開発 = TCP/IP 直接、レガシー連携 = EE で繋ぐ、の役割分担。

## 2. mechanism（どう動くか）

### UDP ポート使い分け (5 段階優先度)
- 12000: LDLC (Logical Data Link Control) signaling
- 12001: Network priority (制御 traffic)
- 12002: High priority (interactive session)
- 12003: Medium priority
- 12004: Low priority (batch transfer)
- 各 UDP packet は DSCP marking で QoS 連動

### Connection 構造
- z/OS 側で `VBUILD TYPE=XCA` (External Communications Adapter) で IP interface を SNA から見せる
- EE 用 PORT を `MEDIUM=HPRIP` 指定で TCP/IP stack に紐付け
- 接続先 (隣接 EE node) を `VBUILD TYPE=SWNET` で switched major node として定義、IP address を入れる
- BIND 経路で IP 上に HPR pipe が確立、SNA session がその上を流れる

### APPN との関係
- EE node は APPN の End Node (EN) または Network Node (NN) として APPN topology に参加
- APPN routing で EE node 間が "隣接" に見える
- APPN session の確立で BIND が EE 上の HPR pipe に乗る

### HPR (High Performance Routing) と path switch
- HPR の RTP (Rapid Transport Protocol) は session を path 独立に保つ
- network 経路の片方が落ちても RTP が代替 path に切替えて session 継続 (path switch)
- 過敏すぎる path switch は逆に session 不安定の原因

## 3. prerequisites

- ZOS-VTAM-001 (EE は VTAM 機能の延長)
- ZOS-TCPIP-001 (UDP transport 経路)
- ZOS-OSA-001 (物理 NIC)
- 一般 IT 知識: UDP socket, DSCP / QoS, APPN topology の概念

## 4. relations

- `depends_on`: ZOS-VTAM-001, ZOS-TCPIP-001
- `specialized_by`: なし
- `contrasts_with`: Cisco SNASw, IBM AnyNet (legacy), TN3270 (terminal access の代替経路)
- `used_by`: ZOS-CICS-001 (Distributed CICS の DPL / function shipping), ZOS-IMS-001 (IMS MSC), ZOS-WAS-001 (legacy WAS で SNA session を持つケース)

## 5. pitfalls

詳細は `pitfalls/` 配下。

## 6. examples

詳細は `examples.md`。

## 7. decision_axes

詳細は `decision-axes/` 配下。
