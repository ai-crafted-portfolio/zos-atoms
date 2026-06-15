---
id: ZOS-ISPF-001
title: ISPF / Interactive System Productivity Facility
status: stable
last_reviewed: 2026-06-04
authors: [agent]
rag_verified: partially
---

# ZOS-ISPF-001: ISPF / Interactive System Productivity Facility

## 1. purpose（なぜ存在するか）

ISPF は TSO/E の上で動く **対話型パネル / エディタ / ユーティリティ統合環境** であり、z/OS 運用・開発者にとっての日常的「画面」 そのもの。データセット参照、メンバ編集、JCL サブミット、SDSF への遷移、ジョブログ閲覧、コンパイル / リンク呼び出し、設定 (FILE TAILORING) など、ほぼ全てのオペレーション動線がここに集約される。

Linux / Windows 視点だと、ターミナル + ファイラ + テキストエディタ + IDE のメニュー UI が **3270 画面上の階層パネル** として 1 本にまとまっている、というイメージ。テキストモードながら function key / `=` 短縮コマンド / split screen / dialog manager を持ち、独自スクリプト (CLIST / REXX) からのパネル駆動も可能。

## 2. mechanism（どう動くか）

### 主要構成要素

- **Primary Option Menu**: 数字 / 文字でサブ機能 (0 設定、1 View、2 Edit、3 Utilities、4 Foreground、5 Batch、6 Command、7 Dialog Test、…) を選択
- **Edit / View**: PDS member / 順次データセット 編集、line command (`i`, `d`, `c`, `m`, …) と primary command (`FIND`, `CHANGE`, `EXCLUDE`, `RESET`, …)
- **Utilities (option 3)**: データセット allocate、コピー、検索、属性表示、catalog 検索など
- **Foreground / Batch (option 4/5)**: COBOL / PL/I / Assembler コンパイル等を対話 / バッチ起動
- **Command Shell (option 6)**: TSO/E コマンド直接実行
- **SDSF / OUTPUT (option =SD 等)**: ジョブ出力閲覧 (連携アトム ZOS-SDSF-001 参照)
- **SuperC / SuperCE**: 高機能 diff (アトム ZOS-IEBCOMPR-001 と対比)

### Dialog Manager

- パネル定義 (`*PANEL`)、メッセージ (`*MSG`)、テーブル (`*TABL`)、ファイル (`*FILE TAILORING`) を ISPPLIB / ISPMLIB / ISPTLIB 等のライブラリで持ち、REXX / CLIST / アセンブラ / COBOL から `ISPEXEC` 経由で呼び出せる
- 独自業務メニューも構築可能、運用ツールが ISPF 上に乗ることが多い

### Split Screen / Swap

- F2 で画面 split、F9 で swap、最大 4 セッション同時保持
- 重い操作の待ち時間に別画面で SDSF 確認、というのが定番動線

### Profile / File Tailoring

- ユーザごとの ISPPROF データセットに編集設定 (PROFILE / EDIT MACRO) が保存
- File tailoring は雛形 + 変数置換でレポート / JCL 自動生成に使われる

## 3. prerequisites

- ZOS-TSO-001 (TSO/E と address space)
- ZOS-DATASET-001 / ZOS-PDS-001 (編集対象の格納形態)
- 一般 IT 知識: text editor の line / command 概念

## 4. relations

- `depends_on`: ZOS-TSO-001, ZOS-DATASET-001, ZOS-PDS-001
- `specialized_by`: ZOS-SDSF-001 (ジョブ出力閲覧画面)
- `contrasts_with`: zOSMF (Web UI), Visual Studio Code + Zowe 拡張
- `used_by`: 開発・運用者全般のオペレーション動線

## 5. pitfalls

- 同一 PDS member を 2 セッションで `Edit` 開きすると enqueue 競合で待たされる、`View` に切り替えるべき
- 行番号 OFF (`NUMBER OFF`) と SEQ field の有無を勘違いして桁ずれ
- File tailoring の skeleton は変数解決順に敏感、ループ内変数の scope を誤って空展開
- 編集中の commit (PF3) を忘れて画面遷移すると変更破棄

## 6. examples

`examples.md` 参照。

## 7. decision_axes

- 「Web UI でリモート操作したい」 → zOSMF を採用
- 「VS Code から触りたい」 → Zowe 拡張
- 「定型運用画面を作って配布したい」 → ISPF Dialog Manager + パネル定義

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

IBM 公式 manual を一次出典としつつ、ISPF の現場操作慣習・ショートカット運用例の補強として市販書籍 (BK_MF_001 / BK_ZOS_BASIC_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 等) を補助参照する。逐語引用禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
