---
id: ZOS-PARALLELSYSPLEX-001
title: Parallel Sysplex（クラスタリング）
status: stable
last_reviewed: 2026-05-09
authors: [agent]
rag_verified: partially
---

# ZOS-PARALLELSYSPLEX-001: Parallel Sysplex

## 1. purpose（なぜ存在するか）

Parallel Sysplex は **複数の z/OS LPAR / 物理機を 1 つのシステムとして統合** するクラスタリング技術。最大 32 LPAR を **CF (Coupling Facility)** で束ね、**同一データを並行更新可能 + LPAR 1 個落ちても無停止** を実現する。

なぜ必要か:
1. **可用性 (5 nines = 99.999%)**: ハードウェア障害・OS 計画停止が起きても業務継続。**金融・公共・航空のミッションクリティカルでは Sysplex 必須**
2. **スケーラビリティ**: 単一 LPAR の CPU 上限を超えるワークロードを複数 LPAR で並列処理
3. **計画停止の回避**: OS / サブシステムをローリングアップグレード可能、ビジネス停止なし

**他社競合**: HP NonStop, Tandem Guardian, Stratus FT が同等領域を狙うが、**Sysplex は 1990 年代から大規模本番運用** + IBM の z シリーズに統合 + **CF というハードウェア専用ロック調停機構** で先行している。Linux + クラスタ系（Pacemaker, Kubernetes）は機能的に近づいているが、**OLTP の単一データ並行更新 + 数ミリ秒以下のロック調停** で Sysplex 同等のところまでは行っていない。

## 2. mechanism（どう動くか）

中核要素:
- **CF (Coupling Facility)**: ロック / キャッシュ / リスト構造を保持する **専用ハードウェア** または PR/SM で割り当てた LPAR
  - **Lock Structure**: 全 LPAR で共有するロック空間（IRLM, GRS Star 等が使う）
  - **Cache Structure**: Db2 Data Sharing の GBP 等
  - **List Structure**: System Logger, MQ Shared Queue, IMS Shared Message Queue
- **CFRM Policy**: CF 構造の定義（Structure 名・サイズ・preference list）
- **XCF (Cross-System Coupling Facility)**: LPAR 間メッセージング基盤
- **GRS (Global Resource Serialization)**: データセット ENQ の全 Sysplex 同期。Star 構成（CF 経由）が標準
- **Sysplex Timer (STP)**: 全 LPAR の時計同期、誤差 数 μs 以内
- **Coupled Datasets**: Sysplex 全体で共有する parmlib データセット

## 3. prerequisites（理解の前提）

- WLM（→ ZOS-WLM-001）— Sysplex 全体で WLM ポリシー単一
- Db2 / CICS / IMS の理解
- 一般 IT 知識: クラスタリング、分散ロック、quorum、failover

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-WLM-001
- `specialized_by`: なし
- `contrasts_with`: （未作成）K8S-CLUSTER-001, ORACLE-RAC-001
- `used_by`: ZOS-DB2-001 (Data Sharing), ZOS-CICS-001 (CICSplex), ZOS-VSAM-001 (RLS), ZOS-IMS-001

## 5. pitfalls（実装・運用での落とし穴）

- **CF 構造サイズの初期見積もり過小**: Db2 GBP の Cache Structure サイズが業務量増で不足 → `IXC0xxI structure full` で書き込みエラー → Db2 Data Sharing が degrade。**サイズ拡張は CFRM 再 Activate**（CF 自体は Sysplex で共通なので操作タイミング慎重に）。**初期は推奨値の 1.5 倍くらい多めが無難**。
- **CF link 帯域不足で性能崩壊**: CF とのリンク（CIB / ICA）の帯域が業務ピーク時に詰まると、ロック取得で待ち列が発生し全 LPAR の TPS 落ちる。**CF link は冗長化 + 4〜8 リンク並列**、これを節約するとピーク時障害再発。
- **CFRM ポリシー Activate 失敗で構造取り残し**: ポリシー差し替え時に旧構造が残置 → 名前空間衝突 → サブシステム起動不可。**Activate 前に `D XCF,STR` で全 structure 状態確認**、削除予定 structure に依存サブシステムが居る場合は順序通りに処理。
- **Sysplex Failure Management (SFM) policy 不在**: LPAR 1 個が hang した時、誰が「死んだ判定」するか。SFM policy 無しだと判定遅延 + manual 介入必要 → 30 分単位の業務停止。**SFM ポリシーで isolation timeout / fence 動作を事前定義**、災害対応シミュレーションで動作確認必須。
- **STP（Sysplex Timer）の primary/backup 切替失敗**: STP は 2 台体制が原則だが、primary 障害時の自動切替が時々失敗。**「時刻が同期取れない sysplex」は実は最悪の状態**。**STP 切替テストを年 1 回実施**、これを怠ると本番障害で初めて発覚。
- **Db2 Data Sharing で GBP 依存性無視**: Data Sharing 設計で GBP を共有しないテーブル設計が混じると、片方の LPAR でしか触らない table が片方に偏在 → 片落ち障害時に「特定アプリ全停止」事案。**全 Data Sharing 対象 table は GBP に登録**。
- **CFCC レベル不整合**: CF のマイクロコード（CFCC）と LPAR の z/OS バージョンの組合せが対応表外だと、structure 操作で意図しない結果。CFCC は z/OS と独立に upgrade 必要、計画的な互換性確認スケジュール要。

## 6. examples（具体例）

```
//IXCMIAPU EXEC PGM=IXCMIAPU
//SYSPRINT DD SYSOUT=*
//SYSIN    DD *
   DATA TYPE(CFRM) REPORT(YES)
   DEFINE POLICY NAME(PROD2026) REPLACE(YES)
     CF NAME(CF1) TYPE(009672) MFG(IBM)
        PARTITION(0) CPCID(00) DUMPSPACE(2000)
     CF NAME(CF2) TYPE(009672) MFG(IBM)
        PARTITION(0) CPCID(00) DUMPSPACE(2000)
     STRUCTURE NAME(IRLMLOCK1)
        SIZE(64000)
        PREFLIST(CF1,CF2)
        REBUILDPERCENT(1)
     STRUCTURE NAME(DSNDB0G_GBP0)
        SIZE(512000)
        PREFLIST(CF1,CF2)
        DUPLEX(ENABLED)
/*

SETXCF START,POLICY,TYPE=CFRM,POLNAME=PROD2026
```

```
D XCF
D XCF,SYSPLEX
D XCF,STR
D XCF,STR,STRNAME=IRLMLOCK1
D XCF,POLICY,TYPE=CFRM
D XCF,COUPLE,TYPE=ALL
```

## 7. decision_axes（採否を分ける判断軸）

- **Sysplex 構築 vs 単一 LPAR**: 99.99% 可用性で十分なら単一 LPAR + バックアップ機。**99.999% 必要 + 計画停止禁止 + Db2 Data Sharing / CICSplex** なら Sysplex 必須。**コスト約 2〜3 倍 + 運用知識特殊**、要件を精査せず Sysplex 導入は浪費。
- **CF Stand-Alone vs ICF (Internal CF)**: 専用 CF ハードウェアは性能最優先、ICF（同一機内 PR/SM partition）はコスト優先。**運用 OLTP 中核は Stand-Alone CF 推奨**、開発・小規模は ICF で OK。**両方を冗長化** が原則。
- **GRS Star vs Ring**: Star（CF 経由）が標準、性能・拡張性で Ring を凌駕。**Ring は z/OS V1.13 以前の遺物**、新規構築で Ring 選ぶ理由は無い。
- **Sysplex メンバ数（LPAR 数）**: 2 LPAR 最小、4〜6 LPAR が中規模、10+ で大規模。**LPAR 数を増やすほど CF 帯域要求が指数増**、構成設計は慎重に。
- **Data Sharing or Workload Sharing**: Db2/IMS は Data Sharing、CICS は Workload Sharing。**「全部 Data Sharing」は overkill**、「全部別 LPAR で別 DB」は冗長性無し。**業務分割 + 共有 DB の戦略を要件で決める**。
- **CF Failure 復旧戦略**: Duplex CF（structure をリアルタイム複製）で 100ms 以下の failover が可能、しかし性能オーバーヘッド 5〜10%。**重要 structure は Duplex、補助 structure は Simplex** が中庸。

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_TECH_001/002) から Parallel Sysplex 設計の運用知識を概念蒸留 (ADR-0109)。逐語引用禁止。
