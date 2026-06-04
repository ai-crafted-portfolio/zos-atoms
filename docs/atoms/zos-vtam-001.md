---
id: ZOS-VTAM-001
title: VTAM (SNA Network Communication)
status: stable
last_reviewed: 2026-06-02
authors: [agent]
rag_verified: partially
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

書籍 (BK_MF_001 / BK_ZOS_TECH_001) 蒸留の補強観点として、VTAM は「**OS が通信セッションを資産として持つ**」設計の代表例として理解しておくと本質が分かる。TCP/IP では各アプリが socket を保持して通信を完結させるが、VTAM では VTAM アドレス空間が LU 状態 / session 状態 / route 状態を集中管理する。これにより、アプリが落ちても VTAM レイヤでは session が生き残れる、複数アプリ間で session を委譲できる、などの可用性メリットがあるが、**「アプリ起動 = VTAM ACT」「アプリ停止 = VTAM INACT」が独立コマンド** という独特の運用文化を生んでいる。Linux 系の「アプリと socket は一体」の感覚で運用しようとすると、INACT 漏れで session が残置されたまま再ACT で衝突する事故が起こる。

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

書籍 (BK_ZOS_TECH_001 / BK_ZOS_TECH_002) 蒸留の mechanism 補強: MODETAB は session 特性 (RU sizes / pacing / class of service) を定義するアセンブラテーブルで、**SE で送信側と受信側で完全一致しないと BIND がリジェクトされる**。新規 APPL を構築する時、MODETAB の DEF を忘れて default の `ISTNORM` を使うと、性能が出ない / 大量データで segment 化が頻発する事象が起きる。**業務特性 (3270 対話か、大容量バルクか、CPI-C か) に応じた MODETAB を選定** し、両側で一致確認をするのが構築 SOP。APPC では VTAM の MODENAME と CICS/IMS の MODE 定義がリンクするため、3 層で名前と特性を揃える必要がある。

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

書籍 (BK_MF_001 / BK_ZOS_TECH_001) 蒸留の代表的な落とし穴 (概要):
- **APPLID 重複**: 同一 Sysplex 内で APPLID が衝突すると後勝ち / session 衝突。`APPLID` の命名規約 (`SYSnnnAPP` 等) をサイト全体で固定する。
- **MODETAB / LOGMODE 不一致**: 送受信側 LOGMODE 不一致で BIND リジェクト、`IST663I BIND FAILED` が出る。両側の LOGMODE entry を `D NET,ID=mode,TYPE=LOGON` で確認。
- **CDRSC キャッシュ古い**: cross-domain で接続先 APPL の状態キャッシュが古いまま、相手 LPAR の再起動を VTAM が認識せず `IST663I SENSE=08570003`。`V NET,INACT,ID=cdrsc` → `V NET,ACT,ID=cdrsc` で強制リフレッシュ。
- **EE トンネル MTU 過大**: Enterprise Extender (EE = SNA over IP) のトンネル MTU が物理 MTU を超えると断片化、`IST1856I` で性能劣化。EE の `IPMSGSIZ` を物理 MTU - 28 程度に絞る。
- **VTAM trace のディスク食い潰し**: `F NET,TRACE,TYPE=BUF,...` で trace を仕掛けたまま忘れると、SYS1.TRACE 系のデータセットを食い潰して OS まで落ちる。trace は時間制限 + 自動停止コマンドとセットで運用。

## 6. examples

詳細は `examples.md`。

書籍 (BK_ZOS_TECH_001) 蒸留の代表的な VTAMLST 設計パターン:

```
* APPL major node 例 (CICS application)
CICSP01  VBUILD TYPE=APPL
CICSP01  APPL  ACBNAME=CICSP01,                                        X
               AUTH=(ACQ,PASS,VPACE),                                  X
               EAS=200,                                                X
               PARSESS=YES,                                            X
               MODETAB=ISTINCLM,                                       X
               DLOGMOD=SCS,                                            X
               SONSCIP=NO,                                             X
               VPACING=2

* Switched major node 例 (3270 端末)
SW3270   VBUILD TYPE=SWNET,MAXGRP=10,MAXNO=10
PU3270   PU    ADDR=01,IDBLK=017,IDNUM=12345,                          X
               PUTYPE=2,USSTAB=USSTBL,LOGAPPL=CICSP01
LU3270A  LU    LOCADDR=02
LU3270B  LU    LOCADDR=03

* MODETAB 抜粋 (Assembler macro)
SCS      MODEENT LOGMODE=SCS,                                          X
               FMPROF=X'03',TSPROF=X'03',                              X
               PRIPROT=X'B1',SECPROT=X'90',COMPROT=X'3080',            X
               RUSIZES=X'8585',                                        X
               PSERVIC=X'01000000E100000000000000'
```

## 7. decision_axes

詳細は `decision-axes/` 配下。

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_TECH_001) から VTAM major node 設計の運用知識を概念蒸留 (ADR-0109)。書籍は概念補助。
