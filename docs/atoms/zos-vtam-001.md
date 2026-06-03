---
title: ZOS-VTAM-001
description: APPL / LU / Mode table、SNA セッション、cross-domain、APPN/HPR
tags:
  - Network
  - Security-Network
---
# ZOS-VTAM-001: VTAM (SNA Network Communication)

## 1. purpose（なぜ存在するか）

VTAM (Virtual Telecommunications Access Method) は、SNA (Systems Network Architecture) ネットワーク全体を z/OS から制御するアクセスメソッド。1974 年に SNA と共に登場、**TCP/IP 普及後も「死なずに」残り続けている** のは、CICS / IMS / TSO 等の業務子システムが SNA 上の LU (Logical Unit) 概念をプロトコル契約として組み込んだ歴史的経緯による。

現在の VTAM (z/OS では Communications Server SNA Services と呼称) は、**(a) 純粋な SNA レガシー (LU0/1/2/3 端末, LU 6.2 APPC)** と **(b) APPN/HPR (Advanced Peer-to-Peer Networking / High Performance Routing)** と **(c) EE (Enterprise Extender、別アトム ZOS-EE-001)** という 3 つの世代を並存させる。新規構築では EE が主、subarea SNA は既存サイトの保守継続が大半。

Linux / クラウドとの対比:
- Linux: SNA emulation (古い Hercules + linuxsna 等) は概念実証レベル、業務用途では成立しない
- TCP/IP: connection-oriented という意味では SNA session と似るが、SNA は **「session を OS の access method が保持する」** モデル (TCP/IP は socket を application が持つ)
- Cloud: 完全に SNA は存在しない、レガシー連携は AT-TLS + IBM HTTP Server / MQ bridge / EE で IP 化が前提

CICS が「**APPLID で identify される VTAM application**」として VTAMLST に登録され、SNA session を張る相手 (3270 端末 / 他 CICS region / IMS) と LU-LU session を交わす。**「CICS が動かない」障害の半分は VTAM 側 (APPL inactive / MODETAB 不整合 / 通信 path 切断)** という現場感覚は今でも有効。

## 2. mechanism（どう動くか）

### Subarea SNA (古典)
- SSCP (System Services Control Point): VTAM が SSCP として subarea network 全体を管理
- PU (Physical Unit) / LU (Logical Unit): 端末や通信路を表す
- APPL: アプリケーション (CICS, IMS, TSO 等) を VTAM 上の LU として登録
- VTAM 起動 = SSCP 起動 + 定義された LU / PU を ACT (activate)

### APPN / HPR
- APPN: dynamic な network topology、Network Node (NN) / End Node (EN) / Border Node 概念
- HPR: APPN 上の高速 routing、RTP (Rapid Transport Protocol) でセッション継続性確保
- HPR は EE (SNA over IP) でも使われる

### VTAMLST PDS
- `SYS1.VTAMLST` (or PROD.VTAMLST) PDS に **MAJNODE definitions** が入る
- ATCSTRxx member: VTAM 起動 parm
- ATCCONxx member: 初期 activate 対象 MAJNODE 列挙
- 各 MAJNODE: APPL major node / Local Non-SNA major node / Switched major node / Cross-domain resource (CDRSC) major node / Cross-domain resource manager (CDRM)
- MODETAB: session 特性 (RU size / pacing / class of service) のテーブル

### LU-LU session の流れ
1. VTAM START → ACT APPL,ID=CICSP01 → APPLID `CICSP01` が active
2. 端末側 LU から CICS APPL に session 要求 → VTAM の SSCP がメディエート
3. BIND RU で session 特性ネゴ → CICS が accept (`LOGON` exit で USERID 検査)
4. 業務開始、終了時 UNBIND

### Cross-domain
- 別 z/OS LPAR 上の APPL (例 CICSA → CICSB) とは Cross-Domain Resource (CDRSC) 経由
- CDRM 同士が SSCP-SSCP session を張って APPL を見えるようにする
- ADJSSCP table で SSCP-SSCP のルーティング規則

### コマンド
- `D NET,APPLS` (active APPL 一覧)
- `D NET,ID=CICSP01,E` (APPL 詳細)
- `V NET,INACT,ID=CICSP01` (停止)
- `V NET,ACT,ID=CICSP01` (起動)
- `D NET,SESSIONS,LU1=CICSP01` (session 一覧)
- `D NET,MAJNODES` (active MAJNODE 一覧)

## 3. prerequisites

- ZOS-CICS-001 / ZOS-IMS-001 (VTAM の主要顧客)
- 一般 IT 知識: SNA architecture の概略 (PU/LU/SSCP)、connection-oriented 通信モデル
- ZOS-CONSOLE-001 (VTAM コマンドは MVS console から発行)

## 4. relations

- `depends_on`: なし (VTAM は OS 機能としての位置付け、起動は通常 STC)
- `specialized_by`: ZOS-EE-001 (EE は VTAM の延長で IP 上の SNA)
- `contrasts_with`: TCP/IP (ZOS-TCPIP-001), Linux SNA emulation (実用ではない)
- `used_by`: ZOS-CICS-001 (CICS region は VTAM APPL), ZOS-IMS-001 (IMS DC は VTAM APPL), ZOS-CONSOLE-001 (SMCS は VTAM 経由), ZOS-WAS-001 (legacy WAS で SNA session を持つケース)

## 5. pitfalls

詳細は `pitfalls/` 配下。

## 6. examples

詳細は `examples.md`。

## 7. decision_axes

詳細は `decision-axes/` 配下。
