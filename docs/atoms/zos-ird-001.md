---
title: ZOS-IRD-001
description: LPAR weight 自動調整、CPU management、I/O priority queueing、Channel subsystem priority queuing
tags:
  - Workload
  - Recovery-Workload
---
# ZOS-IRD-001: IRD (Intelligent Resource Director)

## 1. purpose（なぜ存在するか）

IRD（Intelligent Resource Director）は **PR/SM（LPAR ハイパーバイザ）** と **WLM（Workload Manager）** を結合して、**LPAR 間の CPU weight / I/O 優先度 / Channel 帯域を WLM goal に基づき動的調整** する機能群。1 つの CPC（物理筐体）上に複数 LPAR が同居する環境で、**重要な OLTP LPAR が業務ピーク時に CPU 不足にならない** よう、他 LPAR から CPU 容量を自動移動する。

Linux で例えれば、複数 VM（KVM guest）が動くホスト上で、ホスト側 hypervisor が VM 毎に cgroup cpu.weight + I/O scheduler 優先度を **アプリ層の SLA に基づき自動再配分する** ような仕組み。VMware DRS（Distributed Resource Scheduler）が VM 間の migration で似た目的を果たすが、IRD は **migration せず weight/priority を動かす**（同じ LPAR は同じ CPC に居続ける）。

なぜこれが必要か: PR/SM の LPAR weight は静的設定が伝統で、テスト LPAR と本番 LPAR を混在させた時に「本番が忙しいときテストが weight を食ってる」「本番空いてる時テストが weight 上限に縛られる」状態になる。IRD はこれを WLM の Importance + goal 達成度から「**今、本番 LPAR が CPU 不足 → テスト LPAR の weight を一時的に下げる**」と動かす。**1 物理筐体 / 複数 LPAR で SLA 差がある時に効く**。

## 2. mechanism（どう動くか）

### 構成 3 機能
- **LPAR CPU Management**: WLM cluster（同 CPC 上の LPAR 群）内で、各 LPAR の **CPU weight を動的調整**。重要 workload が PI > 1 になった LPAR に CPU 移動。
- **Dynamic Channel Path Management (DCM)**: ESCON/FICON チャネル経路を I/O 負荷に応じて動的再割当。Managed Pool に登録された Channel が空き / 余裕のある LPAR から busy LPAR に移動。
- **Channel Subsystem Priority Queueing (CSS Priority)**: I/O queue の優先度を WLM Importance に基づき設定。Importance 1 OLTP の I/O が Importance 5 batch を追い越す。

### 前提条件
- **同 CPC 内の LPAR 群**: 物理筐体跨ぎの IRD は不可（PR/SM scope 限定）。
- **Parallel Sysplex 同 LPAR cluster**: 全 LPAR が同 Sysplex に属し、同 WLM Service Definition を共有。
- **PR/SM LPAR 設定**: 各 LPAR の WORKLOAD MANAGEMENT 設定で `YES`、ACTIVATION profile で initial / minimum / maximum weight 範囲。
- **WLM ポリシー activate**: WLM Service Class に Importance + goal が定義されてないと IRD は判断不能。

### 動作判断
- WLM が SMF type 70/72 で各 LPAR の PI（実測/目標）を計算 → **同 cluster 内で PI > 1 の LPAR に CPU weight を再配分** → PR/SM に新 weight を SET → 数秒で反映。
- maximum weight / minimum weight が天井 / 床、weight 合計は CPC 全体で一定。

### CSS Priority
- 各 IO request に WLM Importance を tag、CHPID（Channel Path）の queue で **Importance 1 の IO を先に dispatch**。
- 大量 batch IO が OLTP IO を待たせる現象を防ぐ。

### 監視
- `D M=CPU` で CPU weight 現在値
- `D IOS,CONFIG` で managed Channel
- RMF Monitor I 報告書 (Partition Data Report) で LPAR weight 推移
- `D WLM,SYSTEMS` で WLM cluster 構成

## 3. prerequisites（理解の前提）

- Workload Manager — `ZOS-WLM-001`
- Parallel Sysplex — `ZOS-PARALLELSYSPLEX-001`
- PR/SM / HMC LPAR 設定
- 一般 IT 知識: hypervisor、CPU scheduling、I/O queueing、weight-based scheduling

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-WLM-001, ZOS-PARALLELSYSPLEX-001
- `specialized_by`: なし（LPAR CPU Management / DCM / CSS Priority の 3 サブ機能は IRD 内）
- `contrasts_with`: Linux cgroup cpu.weight + I/O scheduler, VMware DRS + Storage I/O Control, Kubernetes resource limits + QoS classes, AWS EC2 burst credits
- `used_by`: ZOS-CICS-001（CICS region の Importance 設定経由）, ZOS-DB2-001（Db2 sproc Service Class）, 全 z/OS subsystem（WLM Importance → IRD priority queueing）

## 5. pitfalls（実装・運用での落とし穴）

- **WLM goal 不明確で IRD 動かず**: WLM Service Class に Velocity 30 のようなゴール設定だけで Importance が均一（全部 3 等）だと、IRD が「どの LPAR を優先するか」判断不能 → weight 変動なし。**Importance 1〜5 を計画的に配分**（OLTP=1、業務 batch=3、開発=5）、WLM が機能してない組織では IRD も機能しない。
- **LPAR weight 上下動で隣接 LPAR 影響**: 本番 LPAR の weight が動的に上がると、同 CPC の他 LPAR の weight が連動して下がる。テスト LPAR の処理時間が読めなくなる「速度ジッタ」発生。**maximum weight / minimum weight で振れ幅を制限**、テスト LPAR の minimum を確保しないと業務影響評価が困難。
- **I/O priority 設定漏れ**: CSS Priority Queueing は OPT パラメタ `STORAGE` + WLM Service Class の I/O priority enable 必須。これを設定せず Channel Priority だけ有効化しても **I/O queue priority は機能しない**。CHPID Priority と CSS Priority の 2 段階を両方有効化 + WLM policy 側の `IIO=YES`。
- **PR/SM minimum weight 不設定**: minimum weight を 0 にしておくと、IRD が「他 LPAR が忙しい」と判断したとき weight 0 まで下がる → batch LPAR が事実上停止 → batch SLA 違反。**全 LPAR で minimum weight ≥ 10% 程度の床を設置**、IRD が「下げてはいけない床」を policy で明示。
- **WLM cluster 越境で IRD 効かない**: 異なる Sysplex / 異なる WLM Service Definition の LPAR は IRD cluster の外。同 CPC でも別 Sysplex を載せると、その LPAR は IRD scope 外で固定 weight 運用。**Sysplex 統合（本番 + テスト同一 Sysplex）か、IRD 効果を諦めるかの設計判断**、ハイブリッドは不可。
- **DCM Managed Channel の枯渇**: DCM 用 managed pool に Channel が少ないと、busy LPAR が「足りない」と判断しても移動できる Channel がない。**managed pool 設計時に CPC 全 channel の 30〜50% を pool に投入**、専用 channel ばかりで pool が薄いと DCM が無効化に近い。
- **HMC / PR/SM 設定変更で IRD 効果消失**: HMC で ACTIVATION profile の WORKLOAD MANAGEMENT を `NO` に手動変更 / weight cap を MAX=INIT に固定すると IRD が制御権を失う。**ACTIVATION profile の保護 + 定期 audit**、HMC operator の操作ミスで IRD が無効化されてた事例。

## 6. examples（具体例）

```text
* PR/SM ACTIVATION profile 設定 (HMC 上の入力)
* LPAR: PROD01
*   Initial Weight: 100
*   Minimum Weight: 50
*   Maximum Weight: 300
*   WLM Management: YES
*
* LPAR: TEST01
*   Initial Weight: 50
*   Minimum Weight: 20
*   Maximum Weight: 100
*   WLM Management: YES
```

```text
* WLM Service Definition 抜粋 (IRD が参照する Importance)
Service Classes:
  PRODOLTP  (Importance 1, Response Time 90% < 0.5s, IIO=YES)
  PRODBATCH (Importance 3, Velocity 40)
  TESTOLTP  (Importance 4, Velocity 50)
  DISC      (Discretionary)

Classification:
  Subsystem JES:  Job class A -> PRODBATCH
                  Job class T -> TESTOLTP
```

```text
* 状態確認 / 監視
D M=CPU                       -- CPU weight 現在値
D IOS,CONFIG                  -- Channel 設定
D WLM,SYSTEMS                 -- WLM cluster 構成
D WLM,APPLENV=*               -- WLM Application Environment

* RMF Monitor I 起動 (Partition Data Report)
F RMF,START III
F RMF,STOP III
```

## 7. decision_axes（採否を分ける判断軸）

- **IRD 有効化 vs 静的 LPAR weight**: 同 CPC 内に SLA 差がある LPAR を混在させるなら **IRD 有効** が原則。全 LPAR 同等の優先度（本番のみ / テストのみ）なら静的でも問題ない。**「テスト LPAR が本番 weight を食う」事案がある組織は IRD 必須**。
- **WLM cluster 範囲設計**: 1 CPC 全 LPAR を 1 cluster（同 Sysplex）にするか、本番 / テストで分離するか。**SLA 共有 + 動的 balance 優先 → 同 cluster、独立予算 + 干渉防止 → 分離**。
- **DCM Managed Channel 比率**: managed pool に何 % の Channel を入れるか。**FICON 環境では 50% 程度を pool 化が標準、ESCON 残存環境では pool 化リスクで低めに**。
- **CSS Priority Queueing 採否**: I/O 競合多い OLTP 環境では有効、I/O 軽い処理だけなら overhead 増のみ。**OLTP + batch 混在 → 有効、OLTP only / batch only → 無効でも可**。
- **minimum weight 床の設計**: 開発 / テスト LPAR の minimum を **どこまで下げてよいか**。0 にすると IRD が完全制御できるが処理時間予測不能、20〜30 程度にすると床保証あり。**監査要件 / SLA から逆算**。
- **HMC operator 教育**: ACTIVATION profile を operator が手動操作する vs IRD に任せる。**operator manual override 禁止 + audit log 監視** が SOP、operator が IRD を「邪魔」と感じて無効化する事案あり。
