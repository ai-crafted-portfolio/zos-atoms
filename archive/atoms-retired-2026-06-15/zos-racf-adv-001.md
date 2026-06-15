---
id: ZOS-RACF-ADV-001
title: RACF Advanced (Mixed-case password / MFA / Health Check)
status: stable
last_reviewed: 2026-06-02
authors: [agent]
rag_verified: partially
---

# ZOS-RACF-ADV-001: RACF Advanced（強化機能群）

## 1. purpose（なぜ存在するか）

ZOS-RACF-001 は RACF の基礎 (ユーザ / グループ / プロファイル / SETROPTS) を扱う。実運用では基礎だけでは持続可能なセキュリティが回らず、**現代基準（NIST 800-63 / PCI-DSS 4.0 / FFIEC）に追従するための強化機能群** が必要になる。本アトムはその強化機能群を独立して扱う:

- **Mixed-case password / password phrase**: 8 文字大文字限定の旧 RACF 規約からの脱却。NIST が「最低 8 文字、12 文字以上推奨、複雑性より長さ」と要求する世界に合わせる
- **Multi-Factor Authentication (MFA)**: RSA SecurID / TOTP / IBM TouchToken / Generic TOTP の RACF ネイティブ統合 (IBM Z MFA、旧称 IBM MFA for z/OS)
- **Health Check (IBM Health Checker for z/OS の RACF 系チェック)**: SETROPTS 設定の劣化、未使用 ID、危険な属性付与を **自動継続検査** で検出
- **IRRDBU00 / IRRRID00 (RACF database unload / data inventory)**: RACF DB をフラットファイル化、SQL/REXX で大規模分析

Linux / クラウドとの対比:
- Linux: PAM stack に pam_unix + pam_google_authenticator + pam_radius を組合せ。**設定が複数ファイルに分散、整合性チェックは管理者が手で取る**
- AWS IAM: MFA は IAM Policy 上で `aws:MultiFactorAuthPresent`、Trusted Advisor で IAM ベストプラクティス検査
- z/OS + RACF Advanced: **同じ SAF データベースに MFA token / password phrase / 属性が同居**、Health Check が「RACF 全体の現状」を 1 つの report で表現する単一視点が強み

監査要件 (SOX / PCI-DSS 4.0 / FFIEC) の対応で「**最近 90 日アクセス無し ID の自動 REVOKE**」「**SPECIAL 属性者の継続監視**」を仕組み化する時、Health Check + IRRDBU00 が中核になる。

## 2. mechanism（どう動くか）

### Mixed-case password / Password Phrase
- `SETROPTS PASSWORD(MIXEDCASE)` で大小区別を有効化 (z/OS 1.7 以降)
- `ALTUSER USER01 PHRASE('This Is My Long Phrase 2026')` でパスフレーズ設定 (14〜100 文字)
- パスフレーズ有効化要件: KDFAES key encryption (z/OS 2.1+) + ICHDEX01 exit カスタマイズ無効化
- 最小長 / 履歴 / 有効期限は `SETROPTS PASSWORD(MINCHANGE / HISTORY / INTERVAL)`

### Multi-Factor Authentication (IBM Z MFA)
- 認証 factor 種類:
  - **RSA SecurID** (legacy hardware token)
  - **IBM TouchToken** (z/OS native TOTP, AZFTOTP1 factor name)
  - **Generic TOTP** (Google Authenticator / Microsoft Authenticator 互換、AZFTOTPG factor name)
  - **PIV/CAC certificate** (米国政府向け)
- factor ごとに RACF 内 `MFADEF` class profile を定義、`ALTUSER USER01 MFA(FACTOR(AZFTOTP1) ACTIVE)` で登録
- ログオン時、password の代わりに `password + token` の連結文字列 / SEPARATE factor で別 prompt
- AZF (Authentication Z Factor) 一覧は `LISTUSER USER01 MFA`

### Health Check (RACF 系)
- IBM Health Checker for z/OS が常駐 (HZSPROC started task)
- RACF 提供チェック例:
  - `RACF_AIM_STAGE`: AIM (Application Identity Mapping) ステージ、Stage 3 推奨
  - `RACF_SENSITIVE_RESOURCES`: 重要リソース (PARMLIB / LINKLIST / APF library) の RACF 保護状態
  - `RACF_GRS_RNL`: GRS RNL に SYSDSN 等の重要 enq が含まれてるか
  - `RACF_CSFKEYS_ACTIVE` / `RACF_CSFSERV_ACTIVE`: ICSF 関連 class の状態
  - `RACF_UNIX_ID`: UID/GID 自動割当の有効化
- 結果は SDSF CK で確認、状態は SUCCESSFUL / EXCEPTION-LOW/MED/HIGH

### IRRDBU00 (RACF DB unload)
- バックアップ RACF DB (or live DB) を読み、固定長 record にフラット展開
- 出力 record type:
  - `0100` (User basic), `0200` (Group basic), `0400` (Dataset profile), `0500` (General resource), `1210` (Connect record)
  - 各 type ごとに数十フィールド (例: `0100` の USBD_NAME / USBD_LJDATE / USBD_REVOKE / USBD_SPECIAL)
- DB2 LOAD で取り込んで SQL 分析、または REXX で集計
- 計画的に「先月末 vs 今月末の diff」で属性付与/剥奪を追跡する運用が定着

### IRRRID00 (RACF Remove ID utility)
- 引数 ID が DB 内のどこから参照されてるか (DATASET ACL / OWNER / DFLTGRP / RESOURCE PERMIT) を抽出
- 「人事退職者の ID を抹消する」時、残骸を作らない退場手順の必須ツール
- 出力は RACF コマンド (REMOVE / DELUSER / DELDSD) として実行可能

## 3. prerequisites（理解の前提）

- ZOS-RACF-001 (RACF 基礎: ユーザ / プロファイル / SETROPTS)
- ZOS-SAF-001 (SAF callable services)
- ZOS-SMF-001 (type 80 の RACF 監査記録)
- 一般 IT 知識: NIST 800-63B (Authenticator Assurance Level)、TOTP の仕組み (HMAC-SHA1 / 30 秒 / 6 桁)、フラットファイル ↔ SQL の集計設計

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-RACF-001, ZOS-SAF-001, ZOS-SMF-001
- `specialized_by`: ZOS-ACEE-001 (実行時 identity 構造の詳細)
- `contrasts_with`: Linux PAM + pam_google_authenticator, AWS IAM + MFA + Trusted Advisor, Active Directory + Azure MFA
- `used_by`: ZOS-CERTMGMT-001 (証明書 logon 経路で MFA と排他), ZOS-FTP-001 (FTP logon で MFA), ZOS-ZOSMF-001 (web logon で MFA)

## 5. pitfalls

詳細は `pitfalls/` 配下。

## 6. examples

詳細は `examples.md`。

## 7. decision_axes

詳細は `decision-axes/` 配下。


## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

本 atom の領域については、IBM 公式 manual を一次出典としつつ、運用事例や設計判断の補強として市販書籍 (BK_MF_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 等の z/OS / メインフレーム関連書籍) からの実装知識を補助的に参照する。逐語引用は禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
