---
id: ZOS-SDSF-001
title: SDSF / System Display and Search Facility
status: stable
last_reviewed: 2026-06-04
authors: [agent]
rag_verified: partially
---

# ZOS-SDSF-001: SDSF / System Display and Search Facility

## 1. purpose（なぜ存在するか）

SDSF は **ジョブ実行状況・出力・システムログ・printer / initiator / device 状態** を対話的に閲覧 / 操作する z/OS 標準ツール。バッチジョブを投入したあとに「動いている? 終わった? 出力は? エラーは?」を確認する第一動線で、運用者・開発者の日常画面の中心に位置する。

ISPF の中から `=SD` 等で入ってくる経路が一般的だが、独立 panel として `TSO SDSF` でも起動可能。RACF SAF クラス (`SDSF`) で各画面 / コマンドへのアクセス権を細かく制御でき、表示できるジョブ範囲もユーザ権限に従って絞り込まれる。

## 2. mechanism（どう動くか）

### 主要パネル

- **DA (Display Active)**: 現在実行中のジョブ / TSO ユーザ / STC を一覧
- **I / O / H (Input / Output / Held queue)**: 入力待ち / 出力済 / HOLD 中ジョブ
- **ST (Status)**: ジョブの状態 (待機 / 実行 / 出力 / 完了)
- **LOG**: SYSLOG / OPERLOG 連携、システムログを time / msg ID で絞り込み
- **PR / INIT / DEV**: printer / initiator / device 状態
- **ULOG**: ユーザ操作ログ
- **CK**: Health Checker 結果

### ジョブ出力閲覧

- ジョブを選択 → SYSOUT data set をブラウザ表示 → DDNAME 毎に切替
- `?` 行コマンドで DD list 展開、`S` で個別表示、`SE` で edit-like 操作
- FIND / NEXT / LOCATE で大規模ログを高速検索

### コマンド・行コマンド

- 行コマンド: `S` (select)、`P` (purge)、`C` (cancel)、`H` (hold)、`A` (release)、`O` (output)、`E` (edit JCL)、`SJ` (再投入用 JCL 表示) など
- primary command: `OWNER`、`PREFIX`、`DEST`、`FILTER`、`SORT`、`SET DISPLAY`、`SET ACTION` 等で範囲・表示を制御
- z/OS コマンドの直接発行: `/D A,L` のように MVS console コマンドを issue 可能 (SAF 権限要)

### REXX 自動化

- SDSF REXX 拡張 (`ADDRESS SDSF`) でパネルを表形式に取得 → 自動判定・action 発行
- 監視 / レポート / 自動再投入スクリプトの実装基盤

### 権限制御

- SAF クラス `SDSF` 配下の resource (`ISFCMD.*`, `ISFOPER.*`, `GROUP.*`, `JOBCLASS.*` 等) に対して RACF / Top Secret / ACF2 で `PERMIT` を与える
- 「自分の job しか見えない」 / 「LPAR 全体見える」 等を権限で切り替え

## 3. prerequisites

- ZOS-TSO-001 (TSO/E)
- ZOS-ISPF-001 (起動経路)
- ZOS-JCL-001 (見ている対象)
- ZOS-RACF-001 / ZOS-SAF-001 (権限制御)
- ZOS-OPERLOG-001 / ZOS-CONSOLE-001 (LOG パネル基盤)

## 4. relations

- `depends_on`: ZOS-TSO-001, ZOS-ISPF-001, ZOS-JCL-001
- `specialized_by`: なし
- `contrasts_with`: zOSMF Jobs Web UI, Zowe CLI `zowe jobs` コマンド
- `used_by`: 日常運用全般、REXX 自動化 (ZOS-REXX-001), 監視スクリプト

## 5. pitfalls

- `OWNER` / `PREFIX` filter を解除し忘れて「ジョブが見えない」と勘違いする
- 出力 HOLD class の挙動を把握せず `P` (purge) で残しておきたい出力を消す
- `/` コマンドでの z/OS console 発行は強権限、操作ミスでシステム影響あり
- LOG パネル (OPERLOG) の時刻表示は LPAR 設定 / GMT のずれで誤解しやすい

## 6. examples

`examples.md` 参照。

## 7. decision_axes

- 「Web で運用画面を共有したい」 → zOSMF
- 「CI/CD でジョブ状態を機械取得」 → Zowe CLI / zOSMF REST
- 「対話最速」 → SDSF

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

IBM 公式 manual を一次出典とし、SDSF の運用テクニック (FILTER / PREFIX 慣習・REXX 連携) の補強として市販書籍 (BK_MF_001 / BK_ZOS_BASIC_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 等) を補助参照する。逐語引用禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
