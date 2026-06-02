---
id: ZOS-WLM-001
title: Workload Manager（WLM）
status: stable
last_reviewed: 2026-05-09
---


# ZOS-WLM-001: Workload Manager

## 1. purpose（なぜ存在するか）

WLM（Workload Manager）は z/OS の **CPU・メモリ・I/O 配分の自動制御エンジン**。「優先度」ではなく「**ゴール (目標)**」ベース: 「このトランザクションは応答時間 95% を 0.5 秒以内に」「このバッチは X 時までに完了させたい」と宣言すると、WLM が **動的に CPU/メモリ/I/O を配り直して** ゴールを達成しようとする。

なぜ「優先度」でなく「ゴール」か: 1980 年代以前の MVS は静的優先度制御で、業務ピーク時に「優先度高ジョブが資源を食い尽くし、優先度低が永遠に動かない」事故が頻発した。WLM は **「宣言された目標値と実測値の差」を SMF（→ [ZOS-SMF-001](zos-smf-001.md)）から定期取得して、PI (Performance Index) = 実測 / 目標 を計算 → 1 を超えてる workload に資源を回す** 方式。

Linux で例えれば: cgroup + tc + ulimit + nice を全部統合して、kernel が SLA に基づき **動的に再配分する** ような仕組み。Linux にはまだこのレベルの統合 SLA エンジンは存在しない（k8s の HPA/VPA は方向性近いが OS レベルではない）。

## 2. mechanism（どう動くか）

中核オブジェクト:
- **Service Class**: ワークロード分類の単位。各サービスクラスに「ゴール」と「重要度（Importance 1-5）」設定
- **Goal タイプ**:
  - **Response Time**: 「90% を 0.5 秒以内」等。OLTP 用
  - **Velocity**: 「Service rate に対する待ち時間比率」、バッチ向け
  - **Discretionary**: 余り資源で動けば良い、低優先
- **Report Class**: 集計・レポート用の論理分類。Service Class とは別軸
- **Classification Rules**: 走り出すアドレススペース（job, started task, CICS tran etc.）を **どの Service Class に入れるか**
- **Service Definition**: 全部を 1 つの WLM ポリシーに束ねたもの。**1 Sysplex に 1 つだけ active**
- 動作: SMF type 70/72 で性能データ収集 → PI 計算 → ゴール未達なら donor から resource 移動 → Sysplex 全体で WLM は同期

## 3. prerequisites（理解の前提）

- SMF（→ [ZOS-SMF-001](zos-smf-001.md)）— WLM が読む計測データ
- 一般 IT 知識: SLA、優先度、リソース制御
- Sysplex（→ [ZOS-PARALLELSYSPLEX-001](zos-parallelsysplex-001.md)）

## 4. relations（他アトムとの繋がり）

- `depends_on`: [ZOS-SMF-001](zos-smf-001.md)
- `specialized_by`: なし
- `contrasts_with`: （未作成）LINUX-CGROUP-001
- `used_by`: [ZOS-PARALLELSYSPLEX-001](zos-parallelsysplex-001.md), [ZOS-CICS-001](zos-cics-001.md) (enclave 申告), [ZOS-DB2-001](zos-db2-001.md) (stored proc)

## 5. pitfalls（実装・運用での落とし穴）

- **Discretionary 大量で重要 workload が遅延**: 「余ってる時間で動けば良い」を多用しすぎると、本番 OLTP のピーク時に discretionary が CPU を食ってる現象。**Discretionary は Importance 5 / Velocity 低 で本当に「余ったら」しか動かない設計に**、実例で deepl analysis ツールがこれで遅れた事案あり。
- **Velocity ゴール 90% 等の高すぎる設定**: バッチで Velocity 90% を狙うと、I/O 待ちが本質の処理で達成不可能。**Velocity は 30〜60% が現実的**、特に DASD I/O 待ちを伴うバッチは 40% 程度。これを知らない新規構築サイトは「全 PI が 1 超え」状態になる。
- **CICS regional vs CICSPlex SM の Service Class 不一致**: CICS region と CICSplex 全体で Service Class が違うと、tranid の動的振り分けで違う SLA が適用され、性能予測が崩れる。**CICSplex 配下は同一 Service Class** が原則。
- **Importance 1 を多用して全部「最重要」**: 全 work を Importance 1 にすると WLM の優先制御が機能しない（横並びで奪い合い）。**Importance 1 は 5〜10% 以内**、システム本当に重要な OLTP/トランザクションだけに限定。
- **Service Definition Activate 漏れ**: WLM ポリシー編集して Activate しないと反映されない。`F WLM,ACTIVATE` をポリシー変更後に走らせる必要、忘れて深夜帯に変更が効いてない事案。**Activate ジョブはポリシー編集 SOP に組み込む**。
- **Db2 / CICS が enclave 申告失敗で Service Class 不適用**: アプリが SRB 起動などしないと WLM が「親 work と同じ Service Class」と認識せず、独立に判定 → 期待した SLA 違う。**enclave 機構を正しく使う必要あり**、これは設定ミス + 開発者知識不足で頻発。

## 6. examples（具体例）

```
* WLM Service Definition 概念例
Service Classes:
  PRODONLN (Importance 1, Response Time 90% < 0.5s)  <- 業務 OLTP
  PRODBATCH (Importance 3, Velocity 40)               <- 業務バッチ
  TESTONLN (Importance 4, Velocity 50)                <- 開発系 OLTP
  DISC     (Discretionary)                            <- 任意処理

Classification Rules:
  Subsystem Type CICS:
    Tranid PROD* -> PRODONLN
    Tranid TEST* -> TESTONLN
  Subsystem Type STC:
    Started Task ProdSrvr* -> PRODONLN
  Subsystem Type JES:
    Job class A -> PRODBATCH
    Job class T -> TESTONLN
    Job class D -> DISC
```

```
F WLM,REPORT
D WLM,SYSTEMS
D WLM,APPLENV=*
F WLM,ACTIVATE=NEWPOLICY
```

## 7. decision_axes（採否を分ける判断軸）

- **Response Time vs Velocity ゴール**: OLTP（CICS/IMS/Db2 トランザクション）は Response Time、バッチは Velocity。**「混じる Service Class」はゴール定義不能**、用途で完全分離が必要。
- **Importance 配分戦略**: 重要 OLTP 1、業務 OLTP 2、業務バッチ 3、テスト 4、Discretionary 5、で 1〜5 を計画的に使う。**「全部 1 にする」「Importance を全く使わない」は WLM を活かせない**。
- **Sysplex 内 WLM ポリシー単一化**: 1 Sysplex に 1 ポリシー。**Sysplex 統合時にこれが大論争**、本番系・テスト系で同 Sysplex に入れると意見対立。
- **Discretionary の活用**: WLM 上手なサイトは Discretionary を計測ツール / 補助バッチに割り当て、本番に影響無く回す。**Discretionary 全否定（禁止）の運用は柔軟性損失**。
- **CICSplex Workload Manager との連携**: CICS 単体は WLM enclave 申告するが、CICSplex SM 経由で動的振り分けする時に **どの region に飛ぶか** は CICSplex 側の Workload Routing 設定。**WLM Service Class と CICS region 配置を整合**。
- **WLM 監視ツール**: RMF (`ERBRMFPP`) が標準、IBM Tivoli OMEGAMON、BMC MAINVIEW、CA SYSVIEW 等。**「ポリシー設計したが実測してない」は WLM の意味を失う**、最低 RMF 月次レビュー必須。
