---
id: ZOS-VSAM-001
title: VSAM（KSDS / RRDS / ESDS / LDS）
status: stable
last_reviewed: 2026-05-09
authors: [agent]
rag_verified: partially
---

# ZOS-VSAM-001: VSAM

## 1. purpose（なぜ存在するか）

VSAM（Virtual Storage Access Method）は z/OS の高機能アクセス方式。順次データセット（PS）と違い、**キー検索 / 直接アクセス / 索引 / 物理レイアウト最適化** を OS レベルで提供する。

なぜ存在するか: メインフレームの「データを RDB 入れずに、ファイル単体で検索したい」要件への解。1980〜2000 年代の COBOL アプリは、Db2 が無かった時代に VSAM KSDS で「商品マスター = キー：商品 ID」を持っていた。今でも CICS のリソース DB（→ ZOS-CICS-001）、Db2 の内部ストレージ（→ ZOS-DB2-001）、カタログ自身（→ ZOS-CATALOG-001）等、**z/OS の根幹インフラで使われ続けている**。

Linux で例えるなら「sqlite + Berkeley DB を OS が直接サポート」みたいなもの。アプリは独自の B-Tree 実装を持たなくて良い、OS が提供する。

## 2. mechanism（どう動くか）

VSAM は 4 種類の編成タイプ:

- **KSDS** (Key-Sequenced): キー順 + 索引付き。最も使われる
- **RRDS** (Relative Record): レコード番号でアクセス、配列風
- **ESDS** (Entry-Sequenced): 入力順、削除不可、ログ用途
- **LDS** (Linear Data Set): バイト列のみ、構造化レコード無し。Db2 のテーブルスペース実体はこれ

物理構造（KSDS）:
- **Control Interval (CI)**: 物理 I/O 単位。CISIZE（512〜32768 バイトの 512 整数倍）で決まる
- **Control Area (CA)**: CI のグループ、通常 1 シリンダ
- **Data Component**: 実データ
- **Index Component**: B-Tree 索引（KSDS のみ）

ALTERNATE INDEX (AIX): KSDS の **副キー** を別索引で。MySQL の secondary index 相当。

## 3. prerequisites（理解の前提）

- データセット概念（→ ZOS-DATASET-001）
- カタログ（→ ZOS-CATALOG-001）— カタログ自体が VSAM、再帰理解
- 一般 IT 知識: B-Tree 索引、レコード ID

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-DATASET-001, ZOS-CATALOG-001, ZOS-DASD-001, ZOS-SMS-001 (DataClass 集中設定)
- `specialized_by`: KSDS / RRDS / ESDS / LDS（同一アトム内）
- `contrasts_with`: ZOS-DB2-001（フル RDB）, ZOS-PDS-001（メンバベース）
- `used_by`: ZOS-CICS-001, ZOS-DB2-001, ZOS-CATALOG-001

## 5. pitfalls（実装・運用での落とし穴）

- **CISIZE 既定値で性能崩壊**: `CISIZE(4096)` でレコード長 32760 のジョブを動かすと、1 レコードあたり 8 個の CI に Spanned 配置。I/O 数倍増、CA Split 連発。**CISIZE は LRECL × 2 + α** が定石、レコード長 32760 なら CISIZE=32768 が必要。
- **CA Split / CI Split 連発で性能劣化**: KSDS は挿入で空き不足になると CI を半分に分割。**Free Space (FREESPACE) を 10〜20% 取らないと挿入の度に Split**。Split 多発したら IDCAMS REPRO で再構築（オンライン中は不可、オフライン窓必要）。
- **Backup なしの ALTER が破壊**: `ALTER ... RECORDSIZE(80,80)` のような構造変更で、既存データの一部が新サイズに収まらないと ABEND ＆ 部分破損。VSAM の ALTER は **DEFINE と同じくらい慎重に**、IDCAMS BACKUP 取得後実施。
- **CICS / バッチ並行で `IGW01030I` (RLS not enabled)**: VSAM をオンラインジョブと夜間バッチで共有したい場合、**RLS (Record Level Sharing)** を ENABLE してないとバッチ実行中 CICS 停止が必要。RLS 設定は CFRM ポリシー必要、簡単に有効化できない。
- **ALTERNATE INDEX の同期失敗**: AIX 経由で書く時、PRIMARY と AIX の整合は OS 任せだが、**メンテで AIX を REBUILD し忘れる** とクエリ結果が古い。`BLDINDEX` 実行が運用ルーチン要、忘れると「データはあるのに AIX 検索でヒットしない」現象。
- **DEFINE の SHAREOPTIONS 誤設定**: `(2,3)` (1 ライタ多リーダ)、`(3,3)` (制限なし、整合は呼び出し側責任)、`(4,3)` (RLS 経由)。**多くの初心者が `(3,3)` をデフォルト扱いし、後で破損を発見する**。

## 6. examples（具体例）

```idcams
DEFINE CLUSTER (
    NAME(USER.PROD.CUSTOMER)
    INDEXED
    KEYS(10 0)
    RECORDSIZE(200 200)
    CISZ(8192)
    FREESPACE(20 10)
    SHAREOPTIONS(2 3)
    VOLUMES(DASD01)) -
DATA (
    NAME(USER.PROD.CUSTOMER.DATA)
    CYLINDERS(50 10)) -
INDEX (
    NAME(USER.PROD.CUSTOMER.INDEX)
    CYLINDERS(2 1))

REPRO INDATASET(USER.PROD.CUSTOMER) -
      OUTDATASET(USER.PROD.CUSTOMER.NEW)

DEFINE AIX (
    NAME(USER.PROD.CUSTOMER.AIX)
    RELATE(USER.PROD.CUSTOMER)
    KEYS(8 30)
    UPGRADE
    VOLUMES(DASD01)) -
DATA (CYLINDERS(2 1)) -
INDEX (CYLINDERS(1 1))

DEFINE PATH (
    NAME(USER.PROD.CUSTOMER.PATH)
    PATHENTRY(USER.PROD.CUSTOMER.AIX))

BLDINDEX INDATASET(USER.PROD.CUSTOMER) -
         OUTDATASET(USER.PROD.CUSTOMER.AIX)
```

## 7. decision_axes（採否を分ける判断軸）

- **KSDS vs RRDS vs ESDS vs LDS**: KSDS が圧倒的多数。RRDS は配列アクセス用途で今は少ない。ESDS はログ追記専用。LDS は Db2 等の基盤専用。**新規アプリで RRDS/ESDS を選ぶ場面はほぼ無い**、選んでる時点で誰かが Db2 移行を提案すべき。
- **VSAM vs Db2**: 単純なキー値ストアで Web/オンライン側が薄ければ VSAM。複数索引・JOIN・SQL 必要 + ACID トランザクション要なら Db2。**VSAM + CICS で十分なシステムを Db2 化する移行は数千万円単位**、逆に VSAM の限界（複合索引が複雑、JOIN 不可）で苦しんでるなら Db2 移行が逃げ道。
- **CISIZE 設計**: LRECL × 2 + α が出発点、ピーク時挿入率を考慮して FREESPACE 10〜30%。**CISIZE 4096 を疑問なく使うのは初心者**、レコード設計毎に計算する。**「VSAM は遅い」と言われる現場の 9 割は CISIZE 不適**。
- **SHAREOPTIONS の選定**: `(2,3)` (シングルライタ + マルチリーダ) が最も無難。`(3,3)` は整合性をアプリ側が見る前提、本番で安易に使うべきでない。**プロダクションでは原則 (2,3)、RLS 環境のみ (4,3)** が定石。
- **AIX 採用 vs 別 KSDS**: 副キー検索を AIX で持つか、別 KSDS を作って双方更新するか。**両方の DSN 数を見て判断**: 1 副キーなら AIX、3 副キー以上なら別 KSDS の方が運用管理楽。

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_BASIC_001, BK_ZOS_TECH_002) から VSAM クラスター設計の実運用知識を概念蒸留 (ADR-0109)。書籍は概念補助。
