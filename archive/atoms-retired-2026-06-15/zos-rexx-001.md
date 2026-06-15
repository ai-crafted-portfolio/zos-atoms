---
id: ZOS-REXX-001
title: REXX / Restructured Extended Executor (TSO/E + ISPF Scripting)
status: stable
last_reviewed: 2026-06-04
authors: [agent]
rag_verified: partially
---

# ZOS-REXX-001: REXX / Restructured Extended Executor

## 1. purpose（なぜ存在するか）

REXX は z/OS 上で **対話 / バッチ両用の標準スクリプト言語** として広く使われる解釈型言語。TSO/E、ISPF、SDSF、NetView、Db2 (SPUFI 代替)、USS、IPCS などほぼ全領域でホスト連携が用意されており、運用自動化・ジョブ生成・ログ解析・帳票編集など、JCL では非効率なロジックを記述するための「z/OS 版グルー言語」 と捉えるのが正確。

Linux 視点だと、Bash / awk / Python の役割を 1 つにまとめた立ち位置。可変長文字列を第一級で扱う構文、簡潔な `PARSE` 命令、`ADDRESS` で動作環境 (TSO / ISPEXEC / SDSF / NetView) を切り替えるホスト連携が特徴。CLIST より新しく、現行 z/OS 自動化の主役。

## 2. mechanism（どう動くか）

### 言語コア

- すべての値は文字列、必要に応じて数値演算が暗黙変換 (固定精度の十進演算)
- 主要構文: `IF`, `SELECT`, `DO`, `LEAVE`, `ITERATE`, `CALL`, `SIGNAL`, `RETURN`
- 強力な `PARSE` (空白区切り / 位置指定 / パターン分割) でテキスト処理が短く書ける
- 内部関数 (`SUBSTR`, `WORDS`, `STRIP`, `TRANSLATE`, `DATATYPE`, `LENGTH`, …) が豊富

### ホスト連携 (ADDRESS)

- `ADDRESS TSO "ALLOC FI(SYSIN) ..."` — TSO/E コマンド呼出
- `ADDRESS ISPEXEC "DISPLAY PANEL(MAIN)"` — ISPF Dialog Manager 呼出
- `ADDRESS SDSF` — SDSF REXX 拡張、ジョブ / printer / queue 操作
- `ADDRESS NETVIEW` — NetView 自動化スクリプト
- `ADDRESS LINKMVS / LINKPGM` — ロードモジュール呼出
- `ADDRESS SYSCALL` — USS シスコール

### 実行環境

- TSO/E 上での実行 (`EXEC '...REXX(MEMBER)'`)
- ISPF Edit Macro として PDS member 編集中に呼出
- Batch (`PGM=IKJEFT01` 等で TSO 環境を立ち上げて REXX 実行)
- USS (`/bin/rexx` または `tso rexx`)
- IRXJCL (バッチ REXX エンジン)

### スタック / 環境変数

- データスタック (`PUSH` / `QUEUE` / `PULL`) でホストコマンドとの入出力をやりとり
- グローバル変数共有: ISPF `VGET` / `VPUT` (variable pool)
- 大規模スクリプトでは外部関数 / 外部サブルーチンを LOAD で常駐化

## 3. prerequisites

- ZOS-TSO-001 (TSO/E)
- ZOS-ISPF-001 (Dialog Manager / Edit Macro 経路)
- ZOS-DATASET-001 (ファイル I/O 対象)
- 一般 IT 知識: シェル / スクリプト概念

## 4. relations

- `depends_on`: ZOS-TSO-001, ZOS-ISPF-001
- `specialized_by`: NetView REXX (ZOS-NETVIEW-001), SDSF REXX (ZOS-SDSF-001 連携)
- `contrasts_with`: CLIST (旧世代), JCL (宣言型), Python (現代 / USS 経由), zOSMF REST + 外部スクリプト
- `used_by`: ZOS-NETVIEW-001, ZOS-IPCS-001, ZOS-SDSF-001, 多数の運用自動化スクリプト

## 5. pitfalls

- 文字列が第一級なので、数値演算前に `DATATYPE(v, 'N')` 検証を怠ると謎の結果になる
- `PARSE UPPER` で全部大文字化されることに気付かず後段で比較失敗
- `SIGNAL ON ERROR` / `SIGNAL ON HALT` / `SIGNAL ON NOVALUE` のハンドラ未設定で運用時に静かに失敗
- `ADDRESS` を切り替えたまま戻し忘れ、後続コマンドが想定外環境で動く
- `IRXJCL` バッチ REXX で SYSTSIN / SYSTSPRT を意識せず実行すると入出力が空になる

## 6. examples

`examples.md` 参照。

## 7. decision_axes

- 「z/OS 内 ISPF / TSO 連携が中心」 → REXX
- 「USS / Linux と共有のスクリプト資産にしたい」 → Python on USS
- 「単純な JCL 雛形展開だけ」 → ISPF File Tailoring + REXX

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

IBM 公式 manual を一次出典とし、運用 REXX の実装パターン (ログ解析・ジョブ生成・自動化) の補強として市販書籍 (BK_MF_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 / BK_KORN_001 等) を補助参照する。逐語引用禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
