---
id: ZOS-RRS-001
title: RRS (Resource Recovery Services)
status: stable
last_reviewed: 2026-06-02
authors: [agent]
rag_verified: partially
---

# ZOS-RRS-001: RRS (Resource Recovery Services)

## 1. purpose（なぜ存在するか）

RRS（Resource Recovery Services）は z/OS の **OS レベル two-phase commit coordinator**。Db2 / IMS / MQ / CICS / WebSphere 等の複数 Resource Manager（RM）にまたがる **分散トランザクション** を、OS が単一の URID（Unit of Recovery ID）で束ねて prepare / commit / backout する。subsystem 個別の TX coordinator では足りない領域を埋める。

Linux + XA でいう **TPM（Transaction Processing Monitor）** や **Tuxedo** に近いが、RRS は OS 組込みかつ **Sysplex 全体に伝播**（CF log stream 経由）し、kernel コンポーネントとして動作するので追加 middleware ライセンス不要。WebSphere on Linux で XA tx を回す場合、tx log を 各 EJB container が管理する分散モデルに対し、RRS は z/OS のあらゆる RM（Db2, IMS DBCTL, MQ, IBM File Manager, ICSF 等）が **同じ URID** で commit/backout を同期させる中央集権モデル。

なぜ OS 組込みか: メインフレームでは「OLTP（CICS）から Db2 + MQ + IMS DB を 1 つの business transaction で update」が日常業務で、それぞれが独立 commit すると **heuristic damage**（一部 commit / 一部 backout）で在庫不整合・二重請求等が即発生する。RM 個別 coordinator では cross-RM の prepare 同期ができない。RRS は OS が all-or-nothing を保証する。

## 2. mechanism（どう動くか）

### 中核オブジェクト
- **URID (Unit of Recovery ID)**: 16-byte 一意 ID。1 つの分散 tx に 1 つ割当。Sysplex 内で global unique。
- **Context**: 1 つ以上の URID を含む scope。アプリケーションが ATRBEG マクロで context 作成 → ATREND で commit/backout。
- **Resource Manager (RM)**: Db2 / IMS / MQ / CICS / WebSphere 等。RRS に **set-exit-information** で登録、prepare/commit/backout callback を提供。
- **Express UR vs Protected UR**: Express は単一 RM のみ（性能優先）、Protected は複数 RM + log（持続性優先）。

### Log stream 構造
- RRS は 5 つの log stream を **Coupling Facility logstream** または **DASD-only logstream**（LOG-MAINSTREAM）に書く:
  - `ATR.<gname>.MAIN.UR` — Main UR state
  - `ATR.<gname>.DELAYED.UR` — Indoubt UR の長期保管
  - `ATR.<gname>.RESTART` — restart 用
  - `ATR.<gname>.RM.DATA` — RM 情報
  - `ATR.<gname>.ARCHIVE` — 完了 UR archive（optional）
- log stream は IXCMIAPU / IXGINVNT で事前定義。CF 構造 (`LIST` type) 必須。

### 二相 commit 流れ
- アプリ ATRBEG → context 作成 → URID 発行
- アプリが Db2 + MQ を update（各 RM が RRS に「私はこの URID に参加してる」と申告）
- アプリ ATREND COMMIT → RRS が phase 1（prepare）を全 RM に送信
- 全 RM から OK 応答 → RRS が phase 2（commit）送信 → log stream に commit record
- どれか 1 つでも NG → RRS が backout 送信

### ATR メッセージ
- 起動時: `ATR132I` (RRS initialization complete)
- log stream 接続失敗: `ATR233I`
- URID indoubt: `ATR248I` (resource manager is unable to participate)
- 手動 RESOLVE 必要: `ATR240I`

### 起動 / 停止
- `S RRS,SUB=MSTR` で起動（subsystem 名 RRS 固定）。**Db2 / CICS より先に起動** が必須（依存）。
- `SETRRS CANCEL` で停止（業務停止前提）。

## 3. prerequisites（理解の前提）

- Coupling Facility / Parallel Sysplex — `ZOS-PARALLELSYSPLEX-001`
- Db2 trans / commit 概念 — `ZOS-DB2-001`
- log stream の概念（IXG / system logger）
- 一般 IT 知識: 2PC（two-phase commit）、heuristic damage、XA Transaction Manager

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-PARALLELSYSPLEX-001, ZOS-DB2-001
- `specialized_by`: なし
- `contrasts_with`: Linux XA + Tuxedo / WebLogic JTA, Microsoft DTC, Saga pattern (eventual consistency), Kubernetes Distributed Transactions
- `used_by`: ZOS-CICS-001（CICS tx 跨 Db2 + MQ）, ZOS-IMS-001（IMS DBCTL + Db2）, ZOS-MQ-001（MQ syncpoint 連携）, ZOS-WAS-001（WebSphere Liberty z/OS JTA 経由 RRS）

## 5. pitfalls（実装・運用での落とし穴）

- **RRS log stream 枯渇で URID 解決不能**: MAIN.UR / DELAYED.UR の log stream offload size 不足で **commit record が書けず**、URID 状態が log に残らない。新規 tx が `ATR233I` で reject、業務全停止。CF structure full → indoubt 大量発生 → 業務人員手作業で RESOLVE → 半日停止が典型。**log stream sizing は MAXBUFSIZE x4、HIGHOFFLOAD 80% / LOWOFFLOAD 60%、staging dataset サイズも本番ピーク x2 想定** が SOP。
- **Heuristic damage 後の手動 RESOLVE 忘れ**: ネットワーク障害等で RM が応答せず RRS が `ATR240I` を出して URID を indoubt 化、運用者が `DISPLAY RRS,UREXP` で確認しないと **半年放置で log stream 圧迫**。最悪、業務側で「在庫 -100」になってた事案。**indoubt URID は日次 monitor、`SETRRS RESOLVE` で COMMIT/BACKOUT 手動決断、決断根拠を SMF + 業務報告書に記録** が SOP。
- **RRS 起動順 (Db2/CICS より先) 漏れ**: IPL 後の subsystem 起動順序で RRS が Db2 / CICS より後だと、Db2 が「RRS unavailable」で RRSAF 接続を諦め、**以後 IPL 中の Db2 全 tx が RRS なしで動く**（local commit のみ）。気付かず 1 ヶ月運用したサイトあり。**COMMNDxx / IEACMD00 で RRS を Db2 起動より前に S RRS,SUB=MSTR**、起動順序を docs に明記。
- **Cross-sysplex RRS path 検証漏れ**: Sysplex A と Sysplex B で RM 跨ぐ tx は **RRS が両 Sysplex を意識しない**（RRS は単一 Sysplex scope）ため、cross-sysplex coordination は別途 CICS ISC / Db2 DRDA + XA で実現する必要。これを混同して RRS で global tx を組もうとして失敗するアーキ設計あり。**RRS scope = 単一 Sysplex** を設計初期に明文化。
- **Express UR vs Protected UR の選択ミス**: 単一 RM 内 tx を Protected で組むと **log stream に書く分性能 30〜50% 低下**、逆に複数 RM を Express で組むと **logger 死亡時に backout 不能**。**「複数 RM = Protected」「単一 RM = Express」を tx 設計時に明示**、アプリ実装者が選択肢を知らないとデフォルト（多くは Protected）で性能が出ない。
- **log stream offload dataset 不足で performance degradation**: log stream の staging dataset / offload dataset を SMS で動的拡張させず、固定 size で運用していると、ピーク時に offload が遅延 → log stream full → tx throttle。**SMS storage class で DSNTYPE=EXTREQ + EATTR=OPT、Volume Pool に余裕**。

## 6. examples（具体例）

```text
* log stream 定義例 (CF structure 経由)
* IXGINVNT 用 input
DEFINE LOGSTREAM NAME(ATR.PLEX1.MAIN.UR)
  STRUCTNAME(LOG_RRS_MAIN_1)
  LS_DATACLAS(SHARED)
  STG_DATACLAS(SHARED)
  HLQ(IXGLOGR) 
  LS_SIZE(2000)
  STG_SIZE(2000)
  HIGHOFFLOAD(80)
  LOWOFFLOAD(60)
```

```text
* RRS 起動
S RRS,SUB=MSTR

* 状態確認
D RRS
D RRS,UR,SUMMARY
D RRS,UR,DETAILED,URID=001A0000...

* indoubt UR 一覧
D RRS,UREXP

* 手動 RESOLVE (RM が応答不能 + 運用判断)
SETRRS RESOLVE,URID=001A0000...,ACTION=COMMIT
SETRRS RESOLVE,URID=001B0000...,ACTION=BACKOUT
```

```cobol
* COBOL アプリでの ATR マクロ利用イメージ
       CALL 'ATRBEG' USING CTX-TOKEN, ...
       EXEC SQL UPDATE ACCT SET BAL = BAL - 100 WHERE ID = :ID END-EXEC.
       CALL 'MQPUT'  USING ... QMGR-CONN ...
       CALL 'ATREND' USING CTX-TOKEN, COMMIT-OPT.
       IF RC NOT = 0 THEN
           CALL 'ATREND' USING CTX-TOKEN, BACKOUT-OPT.
```

## 7. decision_axes（採否を分ける判断軸）

- **RRS vs subsystem 個別 tx coordinator**: CICS 単体 tx は CICS が coordinator、Db2 単体 tx は Db2 が coordinator。**複数 RM 跨ぐ tx を組む瞬間に RRS 必須**。RRS なしで Db2 + MQ をアプリ側で「commit 順序工夫」しても heuristic damage は防げない。
- **Protected UR vs Express UR**: log stream に書く Protected はクラッシュ後の RM 整合保証、書かない Express は性能優先。**複数 RM = Protected 一択、単一 RM 短命 tx = Express、長命 tx で persistent state があれば Protected**。
- **CF log stream vs DASD-only log stream**: CF 経由は Sysplex 全 system で共有 + 高速、DASD-only は単一 LPAR 想定。**Sysplex 構成は CF 経由が原則**、DASD-only は test / 開発 LPAR のみ。
- **archive log stream 採否**: ARCHIVE log stream を取ると過去 URID の audit が可能、取らないと容量節約。**金融 / 公共では archive 取得 + IXGRPT1 で日次レポート、開発系は archive 無し** が住み分け。
- **subsystem 起動順 SOP**: RRS → Db2 → CICS → MQ の順が標準。**起動順設計を IEACMD00 / COMMNDxx に明示記載 + IPL 後の D RRS チェックを check list 化**、これがないと「Db2 が RRS なしで起動」事故が無症状で続く。
- **indoubt monitor 頻度**: 大規模 OLTP は **5 分間隔自動 monitor**（NetView automation で `D RRS,UREXP` 取得）、小規模は日次手動。**「indoubt があるのに気付かない」運用は heuristic damage を放置するのと等価**。

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_TECH_001) から RRS 2 phase commit 設計の運用知識を概念蒸留 (ADR-0109)。逐語引用禁止。
