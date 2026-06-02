---
id: ZOS-RACF-001
title: RACF（セキュリティ / SAF）
status: stable
last_reviewed: 2026-05-09
---


# ZOS-RACF-001: RACF

## 1. purpose（なぜ存在するか）

RACF（Resource Access Control Facility）は z/OS のセキュリティ製品。**ユーザ認証 / リソース認可 / 監査ログ** を統合提供する。

z/OS は **SAF (System Authorization Facility)** という統一インタフェースを持ち、OS 内の全アクセス（データセット OPEN, ジョブ SUBMIT, CICS トランザクション実行, Db2 BIND/EXEC, USS ファイルアクセス）を SAF 経由で **「許可されてるか」を呼ぶ**。SAF の実装の 1 つが RACF（他には ACF2, Top Secret 等の競合製品あり）。

Linux/Windows と何が違うか:
- Linux: ファイル毎の rwxrwxrwx + sudo + AppArmor + 各サービス独自認証 = **分散している**
- z/OS + RACF: **単一データベース** に「誰が何にアクセスできるか」を集約。データセット名は文字列パターンで保護（`USER.PROD.**` のような generic profile）

**監査要件（PCI-DSS, SOX 等）が厳しい業界（金融・公共）でメインフレームが選ばれる主因の 1 つ**。RACF ログ（SMF type 80）は、誰がいつ何をしたかを残す必須インフラ。

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

## 3. prerequisites（理解の前提）

- データセット概念（→ [ZOS-DATASET-001](zos-dataset-001.md)）
- SMF（→ [ZOS-SMF-001](zos-smf-001.md)）
- 一般 IT 知識: ACL モデル、認証 vs 認可の区別、監査要件

## 4. relations（他アトムとの繋がり）

- `depends_on`: [ZOS-DATASET-001](zos-dataset-001.md)
- `specialized_by`: なし
- `contrasts_with`: （未作成）UNIX-PERMISSION-001, （未作成）AD-DOMAIN-001
- `used_by`: [ZOS-CICS-001](zos-cics-001.md), [ZOS-IMS-001](zos-ims-001.md), [ZOS-DB2-001](zos-db2-001.md), [ZOS-SMF-001](zos-smf-001.md) (type 80 出力)

## 5. pitfalls（実装・運用での落とし穴）

- **`UACC(READ)` を勧められて全公開**: プロファイル新規作成時、`UACC(NONE)` がデフォルト推奨だが、面倒で `UACC(READ)` を付けてしまうと **全ユーザに READ 権が暗黙付与** される。本番データの個人情報が全社員から読める事故、定期監査で発覚するも対応に半年。**新規プロファイルは UACC(NONE) 必須、PERMIT で個別許可**。
- **WARNING モードのまま放置**: 新規プロファイル作成時 `WARNING` フラグを付けると「許可違反でも通す + ログだけ取る」。テスト用途で WARNING 付け、本番反映時に外し忘れ → 実は権限管理が効いてない、というステルス障害が定期発生。**WARNING 付き全プロファイルの月次棚卸し** が必要。
- **SETROPTS REFRESH 忘れで反映されない**: `PERMIT` してもプロファイル が in-storage キャッシュに古いまま。`SETROPTS RACLIST(...) REFRESH` 必要、これを覚えてないと「権限付けたのに動かない」で深夜運用窓を消費。
- **PROTECTED ID にパスワード再設定で解除**: Started Task 用の技術 ID は `PROTECTED` 属性でパスワード使用不可にする。が、**`ALTUSER` でパスワード再設定すると PROTECTED 解除される**。気付かずパスワードクラック攻撃の対象になる事案、定期スキャンが必要。
- **SPECIAL ID 多発**: SPECIAL を運用都合で複数人に付けると、操作が証跡で追えない。**SPECIAL は 2〜3 名に限定 + 個別 audit 必須**、サービスデスクが「権限ください」と言ってきても安易に与えないルールが必要。
- **データセットプロファイル の generic / discrete 混在**: `USER.PROD.SALES`（discrete）と `USER.PROD.**`（generic）両方ある時、より specific な discrete が優先。これを忘れると generic で許可したつもりが discrete で拒否されてる、または逆。**LISTDSD で実効プロファイルを毎回確認**。
- **DB2 SECDATA の二重管理**: Db2 は内部 GRANT と RACF の両方で認可可能。SECDATA クラスを使うと RACF に統一できるが、初期から GRANT で運用してるシステムは混在してる事多し。**どちらが効いてるか分からない権限が積み上がる事故あり**、定期棚卸しで一致確認。

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

## 7. decision_axes（採否を分ける判断軸）

- **RACF vs ACF2 vs Top Secret**: SAF 互換の 3 製品で機能はほぼ同等。**サイトの長年の選択 + ベンダーサポートで決まる**、新規構築は RACF が IBM 公式 + 普及度高で無難。
- **Generic Profile vs Discrete Profile**: HLQ 単位や PROD/TEST 単位で generic（`USER.PROD.**`）が運用楽。**discrete 多用すると数千プロファイル化して管理崩壊**、generic + 例外を discrete で上書き、が原則。
- **WARNING の使い時**: 新規プロファイル投入時の段階移行で「アクセス傾向を観察」する目的で WARNING を **「期間限定で」** 使う。**「とりあえず WARNING で」と恒常化すると認可機能が無効化**、計画書で外す日を決める運用ルール必要。
- **SPECIAL/AUDITOR/OPERATIONS の役割分離**: 1 ID に全部付けるのは内部統制違反（SOX 等で監査人が指摘）。**3 役分離が原則**、役割兼務は監査説明が困難。
- **パスワード vs パスフレーズ vs 証明書**: 8 文字以下が CICS/IMS の伝統だが現代基準で弱い。**Web 経由は PassTicket（短期トークン）化、内部対話は MFA 連携** が現代的。
- **監査ログの保持期間**: SMF type 80 を 90 日 / 1 年 / 7 年（金融）で。**長期保持は VTS / クラウド アーカイブ化** + 検索可能性確保（Splunk/QRadar に常時転送する事例多し）。
