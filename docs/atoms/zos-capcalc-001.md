---
title: ZOS-CAPCALC-001
description: sub-capacity reporting、MSU peak、4HRA、SCRT 提出、Tailored Fit Pricing
tags:
  - Workload
  - Recovery-Workload
---
# ZOS-CAPCALC-001: Capacity planning (MSU / 4HRA / SCRT)

## 1. purpose（なぜ存在するか）

メインフレームの **ソフトウェアライセンス課金** は CPU 時間ではなく **MSU（Million Service Units / 月次ピーク）** で計測される。IBM の z/OS / Db2 / CICS / MQ / WebSphere 等のソフトウェアは **sub-capacity pricing** という方式で、「過去 1 ヶ月の **4HRA（Rolling 4-Hour Average）MSU ピーク**」を **SCRT（Sub-Capacity Reporting Tool）** で算出して IBM に毎月提出、その値に基づき課金される。

なぜこんな複雑な仕組みか: メインフレームのソフトウェアは LPAR 容量（最大 MSU）相当の金額が伝統だったが、「使ってない時間も支払う」のは不合理として 2000 年代に sub-capacity が導入された。**「使った最大瞬間 = 4HRA peak」** の方式は、瞬間 spike だけでは課金されず、4 時間平均なので spike 平準化される設計。**1 ヶ月の 4HRA 軌跡の最大値** が課金 MSU。

Linux / クラウドとの違い: AWS なら on-demand / Reserved / Spot で課金、Linux 上の OSS なら無料、商用 RHEL 等は vCPU 数 / socket 数固定。メインフレームの sub-capacity は **「動的な実使用ピーク」** を月次集計する点で異なる。近年は **Tailored Fit Pricing (TFP)** という新方式（年間契約 + 実 MSU 連動）も登場、SCRT 報告は同様に必要。

この atom は capacity 計算の中核（MSU / 4HRA / SCRT 提出フロー / 課金影響 / 容量計画）を扱う。

## 2. mechanism（どう動くか）

### MSU の定義
- **MSU (Million Service Units)**: IBM が CPC モデル毎に定義する正規化 CPU 容量単位。たとえば z16 7XX-700 は約 200 MSU、z15 7XX-700 は約 190 MSU 等。
- 物理 CPU 時間ではなく **CPC モデル係数 × CPU 時間** で算出（同じ wall-clock CPU 時間でも CPC モデル毎に MSU 値が違う）。
- LPAR 毎・Service Class 毎に SMF type 70/72 で記録。

### 4HRA (Rolling 4-Hour Average)
- **過去 4 時間の MSU 平均** を毎時間 sliding window で計算。
- 例: 14:00 時点の 4HRA = 10:00-14:00 の MSU 平均。15:00 時点の 4HRA = 11:00-15:00 の MSU 平均。
- **1 ヶ月の全 4HRA の最大値** が課金対象 MSU。瞬間 spike は 4 時間で平均化されるので、3 時間以内の急増は本物の課金影響を受けにくい。

### Defined Capacity（soft cap）
- LPAR に **MSU 上限** を設定（ACTIVATION profile の Defined Capacity）。
- 4HRA が Defined Capacity を超えそうになると **WLM が CPU を抑制**（soft cap）して LPAR 単位で MSU を制限。
- これで「ピーク MSU 課金」をコントロール可能。

### Group Capacity
- 複数 LPAR の MSU 合計に上限。Defined Capacity を LPAR 個別ではなく **group 単位** で。
- 同 CPC 上の全 z/OS LPAR の合計 4HRA を group cap 以下に保つ。

### SCRT (Sub-Capacity Reporting Tool)
- IBM 提供の **batch utility**（無償）。SMF type 70 (CPU activity)、type 72 (workload)、type 89 (subsystem product usage) を input。
- 月次（または日次）で実行、過去 1 ヶ月の **product 毎の MSU ピーク** を XML / Tab-delimited で出力。
- **IBM への提出は HTTPS upload**（旧来は email）、月初に提出が義務。

### SMF 89 record
- subsystem product（Db2 / CICS / MQ / WebSphere / IMS 等）の MSU 利用を記録する SMF record。
- SCRT は SMF 89 がないと **product 別 MSU が算出不能** → IBM 側は LPAR 全体 MSU で課金（多くの場合過大）。

### Tailored Fit Pricing (TFP)
- 2019 以降 IBM が提供する新方式: **年間 baseline MSU + 月次実消費差分**。
- baseline 内なら一定金額、超過分は予測価格で精算、未消費分は次年度クレジット。
- SCRT 報告は同様に必要、Defined Capacity の役割は変わるが SMF 89 / 4HRA 計算ロジックは継続。

## 3. prerequisites（理解の前提）

- SMF — `ZOS-SMF-001`
- WLM — `ZOS-WLM-001`
- 一般 IT 知識: ソフトウェアライセンス課金、CPU usage metering、sliding window 平均

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-SMF-001, ZOS-WLM-001
- `specialized_by`: なし
- `contrasts_with`: AWS Reserved Instance / Spot pricing, VMware vRealize Operations capacity planning, Linux KVM コスト管理（vCPU 数固定）, Oracle ライセンス（Named User / Processor metric）
- `used_by`: ZOS-DB2-001（Db2 sub-capacity）, ZOS-CICS-001（CICS sub-capacity）, ZOS-WAS-001（WebSphere sub-capacity）, ZOS-MQ-001（MQ sub-capacity）

## 5. pitfalls（実装・運用での落とし穴）

- **SMF 89 record 漏れで SCRT NG**: SMF 89 を SMFPRMxx で `TYPE(89)` 指定せず収集してないと、SCRT が product 別 MSU を算出できず、**IBM 側は LPAR 全体 MSU を課金対象として処理 → 数百万〜数千万円 / 月の過大請求** に。SCRT 出力 XML を月次レビューして「product 毎の MSU が 0」なら警告。**SMFPRMxx に SYS(TYPE(70-79,89,...)) 明示** が必須、IPL 前確認 SOP。
- **Defined capacity 超過で soft cap 発動**: Defined Capacity を低めに設定しすぎると、業務ピーク時に WLM が CPU 抑制 → tx 応答 timeout / batch SLA 違反。**Defined Capacity は実 MSU peak の 110% を目安**、低すぎる cap は SLA 違反、高すぎる cap はライセンス課金過大、の二重最適化問題。
- **4HRA peak 見落としで月跨ぎ過大請求**: 月末日の最後の 4 時間（21:00-24:00）で過去最大 MSU を記録すると、月内の他時間帯の傾向と無関係に **その月の課金 = その 1 時間** で決まる。**月末 4 時間の MSU 監視 + soft cap 微調整 を月末 SOP**、これを知らない組織は「先月急に課金が倍」事案。
- **Tailored Fit へ移行時の旧 sub-cap reset 漏れ**: TFP 契約後も Defined Capacity を旧来値で残すと、TFP の baseline + flex がうまく機能しない（soft cap で抑制されすぎ / 緩すぎ）。**TFP 契約と同時に Defined Capacity の再設計**、契約変更 SOP に「LPAR capacity 設定見直し」を必ず含める。
- **Sysplex member 間で SCRT 集約漏れ**: 4 LPAR Sysplex で各 LPAR が個別に SCRT を実行 → IBM 側で「同 CEC, 同月の重複報告」と判定されない → product 別 MSU が **LPAR 毎に独立加算** されて過大課金。**SCRT は CEC（CPC）単位で集約実行**、同 CPC 上の全 LPAR の SMF を 1 度の SCRT に投入。
- **SMF dataset の archive 漏れで再算出不可**: SCRT 提出後、IBM から「この月の MSU 内訳を再算出してほしい」と問い合わせがあった時、SMF が HSM ML2 → 物理破壊済だと再算出不能 → 結果として IBM 主張 MSU で確定。**SMF 70/72/89 は最低 13 ヶ月オフサイト保管**（過去 1 年分の再算出可能）、archive policy に明記。
- **GA 1 年遅延の MSU 値で見積もり**: IBM が CPC モデルの MSU 値を発表してから運用 stable に至るまで 1 年遅延がある。設計時の見積もりが旧 MSU 値で、購入後実 MSU が違う事案。**契約直前に IBM 最新 MSU rating table を再取得**、購入 LCM サイクルで定期確認。

## 6. examples（具体例）

```text
* SMFPRMxx の SMF 89 収集設定例
SYS(TYPE(0:255),    /* 全 type 取得が安全 */
    EXITS(IEFU83,IEFU84,IEFU85),
    INTERVAL(SMF,SYNC),
    DETAIL,
    NOBUFFS(MSG))
SUBSYS(STC,EXITS(IEFU83,IEFU84,IEFU85))
SUBSYS(JES2,EXITS(IEFU83,IEFU84,IEFU85))
```

```jcl
//* SCRT 月次実行 (簡略)
//SCRT    EXEC PGM=IFASMFDP,REGION=0M
//INDD1   DD DSN=SYS1.MAN1.SMF,DISP=SHR
//INDD2   DD DSN=SYS1.MAN2.SMF,DISP=SHR
//OUTDD1  DD DSN=USER.SMF.MONTHLY,DISP=(NEW,CATLG),
//           SPACE=(CYL,(500,100))
//SYSPRINT DD SYSOUT=*
//SYSIN    DD *
  INDD(INDD1,OPTIONS(DUMP))
  INDD(INDD2,OPTIONS(DUMP))
  OUTDD(OUTDD1,TYPE(70,72,89))
/*
//*
//SCRTRUN EXEC PGM=BPXBATCH,REGION=0M
//STDPARM  DD *
SH /usr/lpp/scrt/scrt.sh INPUT=USER.SMF.MONTHLY OUTPUT=/u/ops/scrt/
/*
```

```text
* Defined Capacity 設定 (HMC ACTIVATION profile)
* LPAR PROD01:
*   Initial: 200 MSU
*   Defined Capacity: 250 MSU (soft cap 発動 threshold)
*   Group: PRODGRP (Group Capacity: 400 MSU)
*
* 確認 command
D M=CPU
D WLM,RESOURCES
```

```text
* SCRT 出力 XML 抜粋 (概念例)
<SubCapacityReport>
  <CPC serial="01234" model="8561-T01">
    <Product name="Z/OS" peak_msu="180" peak_date="2026-05-15T14:00"/>
    <Product name="DB2" peak_msu="120" peak_date="2026-05-15T14:00"/>
    <Product name="CICS" peak_msu="90"  peak_date="2026-05-20T10:00"/>
  </CPC>
</SubCapacityReport>
```

## 7. decision_axes（採否を分ける判断軸）

- **Sub-capacity vs Full-capacity license**: 全 LPAR 容量で課金（full）か、4HRA peak（sub）か。**現代の標準は sub-capacity**、full-capacity は legacy 環境または管理コスト削減目的のみ。sub-capacity 移行で **30〜60% コスト削減** 報告あり。
- **Defined Capacity vs Group Capacity vs Country Multiplex**: LPAR 個別 cap、複数 LPAR group cap、複数 CPC を多国に跨いだ Country Multiplex Pricing の 3 方式。**Sysplex 1 個 = Group Capacity、複数 CEC = Country Multiplex** が定型、設計時に契約形態と合わせ込む。
- **SCRT 月次 vs 日次実行**: 月初一括 vs 日次集計 + 月次集約。**日次実行で当月 trend 把握 → 月末 soft cap 調整**、月次のみだと「気付いたら課金確定」状態。
- **soft cap の積極利用 vs 自然 peak 監視**: WLM 抑制を積極使用してライセンス削減 vs SLA 優先で抑制せず自然 peak。**業務 SLA に響かない範囲で soft cap で月次課金平準化**、SLA が厳しい OLTP は soft cap 緩めにして batch 側を厳しく。
- **Tailored Fit Pricing vs 従来 sub-capacity**: 年間 baseline + 差分の TFP は予算予測しやすい、従来 sub-cap は使った分のみ。**業務量が読める安定 workload = TFP、業務変動が大きい = 従来 sub-cap** の住み分け、新規契約は IBM が TFP 推奨。
- **SMF archive 保管期間**: 12 ヶ月 / 13 ヶ月 / 24 ヶ月 / 永年。**ライセンス監査要件 = 13 ヶ月以上、金融 audit = 24 ヶ月、性能 trend 分析 = 36 ヶ月** が典型。**短期保管は IBM SCRT 再算出依頼に応えられない**。
