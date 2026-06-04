---
id: ZOS-RACF-PASSTICKET-001
title: RACF PassTicket (時刻同期型ワンタイム認証)
status: draft
last_reviewed: 2026-06-04
authors: [agent]
rag_verified: false
---

# ZOS-RACF-PASSTICKET-001: RACF PassTicket (時刻同期型ワンタイム認証)

## 1. purpose（なぜ存在するか）

**PassTicket** = RACF が提供する **時刻同期型ワンタイム認証トークン**。(USERID, APPL 名, time window) と secret key から 8 文字英数字へ決定論的に派生する。**用途は SSO/プロキシ認証**: AD/LDAP/WAS/Java Web 層が user を別系で認証済の前提で、平文パスワードを介さず RACF/CICS/IMS/Db2/TSO へ proxy login する。

Linux 対比は Kerberos AP-REQ (KDC 中央、5 分時刻同期), Windows は AD ticket, AWS は STS 一時 credential。**z/OS PassTicket は pre-shared key + 10 分窓 (発行±5 分) + APPL ごと別 key + ネット上は平文 (8 文字 login string)** という特殊位置。

## 2. mechanism（どう動くか）

- 払い出し: `R_GenSec` / `R_ticketserv` (callable `IRRSPK00` / `IRRSGS00`)、USERID + APPL → 8 文字 ticket
- 検証: 通常の `RACROUTE REQUEST=VERIFY PASSWORD=...` 経路で RACF が PassTicket か pwd か自動判別
- 鍵保管: `PTKTDATA <APPL>` profile の `SSIGNON(KEYMASKED(...))` (旧、XOR mask) または `SSIGNON(KEYENCRYPTED(...))` (推奨、ICSF master key 暗号化)
- APPL 名: TSO/TSOnnnn / CICS APPLID / IMS subsystem / Db2 SSID / カスタム
- 時刻窓 ±5 分、`APPLDATA('NO REPLAY')` で 1 回限り化
- 発行権限: `IRR.RTICKETSERV` FACILITY または `PTKTDATA.<APPL>` UPDATE

## 3. prerequisites（理解の前提）

- ZOS-RACF-001, ZOS-SAF-001, ZOS-ACEE-001, ZOS-ICSF-001
- 一般: TOTP / HOTP, Kerberos pre-shared key, SSO 概念

## 4. relations（他アトムとの繋がり）

[relations.md](./relations.md) 参照。`depends_on`: ZOS-RACF-001 / ZOS-SAF-001 / ZOS-ACEE-001 / ZOS-ICSF-001、`used_by`: CICS / DB2 / IMS / TSO / WAS / FTP。

## 5. pitfalls（実装・運用での落とし穴）

- pitfall-001: 発行ホストと z/OS の時刻ズレで PassTicket 検証失敗
- pitfall-002: KEYMASKED のままで鍵漏洩、後で抜き出されて全 user impersonate
- pitfall-003: APPL 名 mismatch (TSO vs TSOnnnn) で同じ key なのに認証失敗
- pitfall-004: R_GenSec 呼び出し権限が広すぎて内部脅威で任意 ID 偽装
- pitfall-005: NOREPLAY 未設定で 10 分間 ticket 使い回し→リプレイ攻撃

## 6. examples（具体例）

[examples.md](./examples.md) 参照。RDEFINE PTKTDATA + KEYENCRYPTED + NOREPLAY / 発行 API 認可 (IRR.RTICKETSERV) / R_ticketserv 疑似 C / CICS SIGNON / IRRDBU00 PTKTDATA 棚卸し / Health Check / 時刻同期確認 / SMF 80 ICH408I 解析 を収録。

## 7. decision_axes（採否を分ける判断軸）

- axis-001: PassTicket vs Kerberos vs SAML/OIDC (z/OS subsystem への SSO 経路)
- axis-002: KEYMASKED vs KEYENCRYPTED (鍵保管方式)
- axis-003: APPL 鍵分離粒度 (APPL 単位 vs subsystem 種別 vs system 全体)

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

本 atom の領域については、IBM 公式 manual を一次出典としつつ、運用事例や設計判断の補強として市販書籍 (BK_MF_001 / BK_ZOS_TECH_001 等の z/OS / RACF 関連書籍) からの実装知識を補助的に参照する。逐語引用は禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
