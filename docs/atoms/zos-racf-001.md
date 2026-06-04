---
id: ZOS-RACF-001
title: RACF（セキュリティ / SAF）
status: stable
last_reviewed: 2026-05-09
authors: [agent]
rag_verified: partially
---

# ZOS-RACF-001: RACF

## 1. purpose（なぜ存在するか）

RACF（Resource Access Control Facility）は z/OS のセキュリティ製品。**ユーザ認証 / リソース認可 / 監査ログ** を統合提供する。

z/OS は **SAF (System Authorization Facility)** という統一インタフェースを持ち、OS 内の全アクセス（データセット OPEN, ジョブ SUBMIT, CICS トランザクション実行, Db2 BIND/EXEC, USS ファイルアクセス）を SAF 経由で **「許可されてるか」を呼ぶ**。SAF の実装の 1 つが RACF（他には ACF2, Top Secret 等の競合製品あり）。

Linux/Windows と何が違うか:
- Linux: ファイル毎の rwxrwxrwx + sudo + AppArmor + 各サービス独自認証 = **分散している**
- z/OS + RACF: **単一データベース** に「誰が何にアクセスできるか」を集約。データセット名は文字列パターンで保護（`USER.PROD.**` のような generic profile）

**監査要件（PCI-DSS, SOX 等）が厳しい業界（金融・公共）でメインフレームが選ばれる主因の 1 つ**。RACF ログ（SMF type 80）は、誰がいつ何をしたかを残す必須インフラ。

書籍 (BK_MF_001 / BK_ZOS_TECH_002) 蒸留の視点では、RACF は「OS と認証認可を分離する設計」の代表例として理解しておくと体系的に把握できる。OS 内部から見れば RACF は単なる SAF プラグインの一つで、SAF call が「許可 / 拒否 / 知らない」の 3 値を返すだけ。**OS は判定理由を知らない**ので、運用側で SMF type 80 をログ収集→集中分析しないと監査説明ができない。「とりあえず権限を絞る」だけでは内部統制要件を満たさず、「誰が・いつ・何に・どう判定されたか」を後から再現できる体制を初期構築フェーズで決めておくのが鉄則。

## 2. mechanism（どう動くか）

### 認証
- ユーザ ID（1〜8 文字） + パスワード or パスフレーズ or 証明書
- TSO/CICS/IMS/Db2/Web 全部 RACF を使う

### 認可
- **データセットプロファイル** (DATASET class): `USER.PROD.**` のようなパターン
- **一般リソース クラス**: CICS 用（`TCICSTRN`）、Db2 用、JES 用、500+ クラス
- **ユーザの属性**: SPECIAL（管理者）、AUDITOR（監査）、OPERATIONS（運用）、PROTECTED、REVOKE
- **グループ**: ユーザの集合、ACL にグループ単位で許可可能

### 監査
- SMF type 80 レコードに全アクセス記録
- AUDIT 設定で「成功も記録 / 失敗だけ」を選べる

書籍 (BK_ZOS_TECH_001) 蒸留での追加 mechanism: RACF の権限判定は **「ユーザ → グループ → ACL → UACC → 警告」** という決定木を内部で辿る。`PERMIT` で個別許可を与えた場合と、グループ経由で許可を与えた場合では、SMF type 80 のログに残る経路が違う。**LISTDSD の AUTHUSER 出力で「誰が・どの経路で・何の権限を持っているか」を可視化できる**が、これを定期実行して棚卸ししないと、退職者の権限残置・グループ統廃合での権限肥大などが進行する。RACF データベース (RACFDB) は in-memory cache されるため、変更後 `SETROPTS REFRESH` を打たないと反映されない点も運用上の盲点。

## 3. prerequisites（理解の前提）

- データセット概念（→ ZOS-DATASET-001）
- SMF（→ ZOS-SMF-001）
- 一般 IT 知識: ACL モデル、認証 vs 認可の区別、監査要件

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-DATASET-001
- `specialized_by`: なし
- `contrasts_with`: （未作成）UNIX-PERMISSION-001, （未作成）AD-DOMAIN-001
- `used_by`: ZOS-CICS-001, ZOS-IMS-001, ZOS-DB2-001, ZOS-SMF-001 (type 80 出力)

## 5. pitfalls（実装・運用での落とし穴）

- **`UACC(READ)` を勧められて全公開**: プロファイル新規作成時、`UACC(NONE)` がデフォルト推奨だが、面倒で `UACC(READ)` を付けてしまうと **全ユーザに READ 権が暗黙付与** される。本番データの個人情報が全社員から読める事故、定期監査で発覚するも対応に半年。**新規プロファイルは UACC(NONE) 必須、PERMIT で個別許可**。
- **WARNING モードのまま放置**: 新規プロファイル作成時 `WARNING` フラグを付けると「許可違反でも通す + ログだけ取る」。テスト用途で WARNING 付け、本番反映時に外し忘れ → 実は権限管理が効いてない、というステルス障害が定期発生。**WARNING 付き全プロファイルの月次棚卸し** が必要。
- **SETROPTS REFRESH 忘れで反映されない**: `PERMIT` してもプロファイル が in-storage キャッシュに古いまま。`SETROPTS RACLIST(...) REFRESH` 必要、これを覚えてないと「権限付けたのに動かない」で深夜運用窓を消費。
- **PROTECTED ID にパスワード再設定で解除**: Started Task 用の技術 ID は `PROTECTED` 属性でパスワード使用不可にする。が、**`ALTUSER` でパスワード再設定すると PROTECTED 解除される**。気付かずパスワードクラック攻撃の対象になる事案、定期スキャンが必要。
- **SPECIAL ID 多発**: SPECIAL を運用都合で複数人に付けると、操作が証跡で追えない。**SPECIAL は 2〜3 名に限定 + 個別 audit 必須**、サービスデスクが「権限ください」と言ってきても安易に与えないルールが必要。
- **データセットプロファイル の generic / discrete 混在**: `USER.PROD.SALES`（discrete）と `USER.PROD.**`（generic）両方ある時、より specific な discrete が優先。これを忘れると generic で許可したつもりが discrete で拒否されてる、または逆。**LISTDSD で実効プロファイルを毎回確認**。
- **DB2 SECDATA の二重管理**: Db2 は内部 GRANT と RACF の両方で認可可能。SECDATA クラスを使うと RACF に統一できるが、初期から GRANT で運用してるシステムは混在してる事多し。**どちらが効いてるか分からない権限が積み上がる事故あり**、定期棚卸しで一致確認。
- **PROFILE 名の generic 拡張で意図せぬ範囲拡大 (BK_ZOS_TECH_002 蒸留)**: `USER.PROD.*` を作って後で `USER.PROD.SECRET` を作った時、generic profile が暗黙に SECRET も覆ってしまい、想定外のユーザに READ 権が暗黙付与される。**新規 HLQ 拡張時は必ず LISTDSD で実効プロファイル確認**、その上で discrete profile で上書きするか generic を細分化する。
- **RACROUTE 互換 API での監査漏れ**: アプリ独自の SAF 呼出ロジックを実装する時、AUTHCHECK を呼ばずに自前でテーブル参照すると SMF type 80 が出ない。「動くからいい」で済ますとセキュリティ監査時にログ無しで説明不能。**自前認可は SAF 経由で書く SOP** が長寿システムでは厳格化される。
- **PROTECTED 属性の運用浸透不足**: STC 用技術 ID を `PROTECTED` 化する原則を知らずに、人間用パスワードを設定したまま運用しているサイトがある。**全 STC ID を年次棚卸しで PROTECTED 化**するチェック項目を入れないと、退職者ローテーションで穴が開く。
- **Multi-Factor Authentication (MFA) 連携の例外**: Z/OS MFA (RSA SecurID / TOTP) 導入後、特定の STC / 自動ジョブで MFA 不要 ID を例外化する設定 (`MFA(NOPWFALLBACK)` 等) を入れる場面が出てくる。**例外 ID 一覧が暗黙化してドキュメント化されないと、監査人指摘事項になる**。明示的に「MFA 例外台帳」を運用文書として残すのが現代的な内部統制の前提。

## 6. examples（具体例）

```racf
ADDUSER USER01 NAME('YAMADA TARO') OWNER(SYSGRP)
        PASSWORD(INIT01) DFLTGRP(USERGRP)

ADDGROUP USERGRP OWNER(SYSGRP) SUPGROUP(SYSGRP)
CONNECT USER01 GROUP(USERGRP)

ADDSD 'USER.PROD.**' UACC(NONE) OWNER(SYSGRP)
PERMIT 'USER.PROD.**' ID(USERGRP) ACCESS(READ)
PERMIT 'USER.PROD.**' ID(ADMUSER) ACCESS(ALTER)

LISTUSER USER01
LISTDSD DA('USER.PROD.SALES') ALL

* CICS トランザクション認可
RDEFINE TCICSTRN MYAPP.MENU UACC(NONE) OWNER(CICSADM)
PERMIT MYAPP.MENU CLASS(TCICSTRN) ID(CICSUSR) ACCESS(READ)
SETROPTS RACLIST(TCICSTRN) REFRESH

SEARCH CLASS(USER) FILTER(*) SPECIAL
```

書籍 (BK_MF_001) 蒸留の運用パターン: 大企業の RACF 運用では「役割テンプレート」(`TEMPLATE_DEV` / `TEMPLATE_OPS` / `TEMPLATE_AUDIT` 等) を擬似的にグループ階層で表現し、新入社員/異動でグループ付け替えだけで権限を回す体制が定着している。**個別 PERMIT で権限を積み増す運用は数年で破綻**するので、初期からテンプレートグループ + 業務リソースグループの 2 軸設計を強く推奨する。

```racf
* テンプレートグループ階層の例
ADDGROUP G_DEV_TEMPL OWNER(SECADM)
ADDGROUP G_DEV_ACCT  OWNER(SECADM) SUPGROUP(G_DEV_TEMPL)
ADDGROUP G_DEV_SALES OWNER(SECADM) SUPGROUP(G_DEV_TEMPL)
* G_DEV_TEMPL に共通権限、G_DEV_ACCT / G_DEV_SALES に業務固有を付ける
```

## 7. decision_axes（採否を分ける判断軸）

- **RACF vs ACF2 vs Top Secret**: SAF 互換の 3 製品で機能はほぼ同等。**サイトの長年の選択 + ベンダーサポートで決まる**、新規構築は RACF が IBM 公式 + 普及度高で無難。
- **Generic Profile vs Discrete Profile**: HLQ 単位や PROD/TEST 単位で generic（`USER.PROD.**`）が運用楽。**discrete 多用すると数千プロファイル化して管理崩壊**、generic + 例外を discrete で上書き、が原則。
- **WARNING の使い時**: 新規プロファイル投入時の段階移行で「アクセス傾向を観察」する目的で WARNING を **「期間限定で」** 使う。**「とりあえず WARNING で」と恒常化すると認可機能が無効化**、計画書で外す日を決める運用ルール必要。
- **SPECIAL/AUDITOR/OPERATIONS の役割分離**: 1 ID に全部付けるのは内部統制違反（SOX 等で監査人が指摘）。**3 役分離が原則**、役割兼務は監査説明が困難。
- **パスワード vs パスフレーズ vs 証明書**: 8 文字以下が CICS/IMS の伝統だが現代基準で弱い。**Web 経由は PassTicket（短期トークン）化、内部対話は MFA 連携** が現代的。
- **監査ログの保持期間**: SMF type 80 を 90 日 / 1 年 / 7 年（金融）で。**長期保持は VTS / クラウド アーカイブ化** + 検索可能性確保（Splunk/QRadar に常時転送する事例多し）。


## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

本 atom の領域については、IBM 公式 manual を一次出典としつつ、運用事例や設計判断の補強として市販書籍 (BK_MF_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 等の z/OS / メインフレーム関連書籍) からの実装知識を補助的に参照する。逐語引用は禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
