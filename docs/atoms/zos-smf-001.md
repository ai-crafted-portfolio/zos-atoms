---
id: ZOS-SMF-001
title: SMF（システム計測ログ）
status: stable
last_reviewed: 2026-05-09
---


# ZOS-SMF-001: SMF

## 1. purpose（なぜ存在するか）

SMF（System Management Facility）は z/OS の **計測 + 監査ログ集約基盤**。OS / サブシステム / アプリが発する全ての計測イベント（ジョブ起動・終了、データセット OPEN、トランザクション完了、CPU 使用、ネットワーク I/O、セキュリティ違反 等）を **統一フォーマットの「SMF レコード」** として連続追記ストリームに書き出す。

なぜ必要か:
1. **課金 (Chargeback)**: メインフレームは MIPS 課金が伝統。誰がどれだけ使ったかを SMF type 30 / 70 から集計
2. **性能分析**: WLM ゴール達成率、ジョブ実行時間、Db2 SQL コストを type 70/72/100/101 から分析
3. **セキュリティ監査**: 誰が何にアクセスしたかを type 80（RACF）から監査
4. **キャパシティ計画**: 月次・年次の使用量推移から HW 増強判断

Linux で例えれば: dmesg + auditd + sar + journald + accton を全部統一フォーマットで吐く OS 機能。SMF は **30+ 年の歴史でフォーマットが安定**してるため、各種ツール（IBM RMF, OMEGAMON, BMC MAINVIEW 等）が前提にしている。

## 2. mechanism（どう動くか）

- 各イベント発生時、OS / サブシステムが **SMF レコード** を SVC で書き出す
- 全レコードは「SMF データセット」（VSAM か SMF logstream）に追記
- レコードヘッダ: type（数値）+ subtype + サイズ + タイムスタンプ + システム ID
- type の代表例:
  - **0 (IPL)**: システム起動
  - **30 (Common Address Space Work)**: ジョブ・タスクの統合計測。**最重要**
  - **70-79 (RMF)**: Resource Measurement Facility 系
  - **80 (RACF)**: セキュリティ
  - **101 (Db2 Accounting)**
  - **110 (CICS)**
  - **115/116 (MQ)**
- 出力先:
  - 旧式: VSAM データセット (`SYS1.MANx`)。順次フル → switch
  - 新式: SMF logstream（System Logger 機能）。複数 LPAR から書き込み可

## 3. prerequisites（理解の前提）

- データセット概念（→ [ZOS-DATASET-001](zos-dataset-001.md)）
- 一般 IT 知識: ログ集約・ローテーション、構造化レコードフォーマット
- VSAM の理解（旧式 SMF データセット）

## 4. relations（他アトムとの繋がり）

- `depends_on`: [ZOS-DATASET-001](zos-dataset-001.md)
- `specialized_by`: なし
- `contrasts_with`: （未作成）LINUX-AUDITD-001, LINUX-JOURNALD-001
- `used_by`: [ZOS-WLM-001](zos-wlm-001.md) (type 70/72), [ZOS-RACF-001](zos-racf-001.md) (type 80 出力), [ZOS-DB2-001](zos-db2-001.md) (type 101 出力), [ZOS-DUMP-001](zos-dump-001.md) (type 99 ロジレックレコード)

## 5. pitfalls（実装・運用での落とし穴）

- **SMF 全 type 取得で容量爆発**: `SYS(TYPE(0:255))` のように指定すると、type 14 (データセット close) や type 6 (出力 writer) で日量数百 GB に膨らむ。**業務に必要な type だけ選別**（30, 70-79, 80, 101, 110）、不要 type は除外。
- **SMF データセット フル → SWITCH 失敗で停止**: 旧式 VSAM 方式で、`MANA` フル → `MANB` 切替時に `MANB` の処理（archive ジョブ）が遅れて両方フル → SMF 書込み失敗 → システムが「監査機能無し」になり最悪 IPL 必要。**SWITCH ジョブの完了監視必須**、Logstream 移行で根本解決。
- **タイムスタンプは GMT で記録、ローカル時間と勘違い**: SMF レコードのタイムスタンプは **GMT** が原則。日本時間と +9 時間ズレるが、これを忘れて分析すると「夜中に CPU 100%」と誤読する。**分析時に必ず TZ 変換**。
- **Subtype の解釈漏れ**: type 30 は subtype 1〜6（interval, step end, job end, etc.）で意味が違う。**全部足し合わせると CPU 時間を二重カウント**する事案。subtype 4（step end）と subtype 5（job end）で意図的に区別、ツールに任せて手で集計しない。
- **VSAM 構成の logstream 移行で SMF レコード形式変更**: System Logger 経由に変えると、`IFASMFDL` ユーティリティで read する必要あり、過去の `IFASMFDP`（VSAM 用）スクリプトが動かなくなる。**移行前にツール側の対応確認**。
- **type 30 の `SMF30RUC` 単位混乱**: CPU 時間は SU (Service Unit) / 秒 / マイクロ秒で複数フィールド。サイトの machine model（SU/MIPS 換算係数）を考慮しないと比較不可。**チャージバック計算では換算係数の固定が必須**。
- **type 110 の subtype と SMF110V の混在**: CICS 統計は subtype 別の他に SMF110V 構造あり、解析ツール（CICS Performance Analyzer 等）の前提に合わせて出力フォーマット選択。**フォーマット不整合で過去半年のデータが解析不能**になる事案あり。

## 6. examples（具体例）

```parmlib
* SYS1.PARMLIB(SMFPRM00)
       ACTIVE
       DSNAME(SYS1.MANA,SYS1.MANB,SYS1.MANC)
       LSNAME(IFASMF.LOG.STREAM)
       SYS(TYPE(0,30,70:79,80,90,101,110),
           EXITS(IEFU83,IEFU84,IEFU85),
           NODETAIL)
```

```jcl
//* IFASMFDP で SMF レコード dump
//STEP1   EXEC PGM=IFASMFDP
//SYSPRINT DD SYSOUT=*
//DUMPIN   DD DSN=SYS1.MANA,DISP=SHR,AMP=AMORG
//DUMPOUT  DD DSN=USER.SMF.DUMP,DISP=(NEW,CATLG),
//             SPACE=(CYL,(100,50)),
//             DCB=(LRECL=32760,RECFM=VBS,BLKSIZE=27998)
//SYSIN    DD *
   INDD(DUMPIN,OPTIONS(DUMP))
   OUTDD(DUMPOUT,TYPE(30,70:79,80))
   DATE(2026120,2026130)
/*
```

## 7. decision_axes（採否を分ける判断軸）

- **VSAM SMF データセット vs logstream**: 単一 LPAR + 旧運用なら VSAM で十分。**Sysplex 複数 LPAR + Sysplex 全体で SMF 集中ログしたい** なら logstream 必須。新規 z/OS 環境は logstream 標準。
- **取得 type の絞り方**: **最低限 30, 70-79, 80, 101, 110**（業務 + 性能 + セキュリティ + Db2 + CICS）、+ 必要に応じて 14（DSN open）, 115（MQ）, 117（DDF Db2）。**type 14, 6 は大量、抑止が原則**。
- **SMF 保管期間**: 直近 30 日はオンライン VSAM、30〜90 日は VTS / cloud archive、90 日超は別件保管。**金融業界は 7 年保持義務**、コンプラ要件で保持戦略大きく変わる。
- **日次圧縮 / 週次圧縮**: 日次が無難。週次は容量大規模だが運用リスク（dump ジョブ失敗で 1 週間消失）。
- **SMF データを Splunk / QRadar / ElasticSearch に流す**: モダンな SIEM 連携で z/OS 監査を一元化したい場合、IBM Z Data Gatherer / Vanguard 等で SMF リアルタイム転送可。**「Splunk から RACF アクセス検索したい」要件は普通に発生**。
- **type 110 と CICS Performance Analyzer**: CICS 性能分析専用ツール。SMF 110 を直接 SQL に流す自前開発は数年かかるが PA なら数ヶ月。**コストとサイト規模で決定**。
