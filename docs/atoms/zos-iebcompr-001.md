---
id: ZOS-IEBCOMPR-001
title: IEBCOMPR / Dataset Compare Utility
status: stable
last_reviewed: 2026-06-04
authors: [agent]
rag_verified: partially
---

# ZOS-IEBCOMPR-001: IEBCOMPR / Dataset Compare Utility

## 1. purpose（なぜ存在するか）

IEBCOMPR は **2 つのデータセット (PS 同士 / PDS member 同士) のレコード単位での内容比較** を行う IBM 標準ユーティリティ。リリース前後の load module 等価性確認、PDS member の差分検出、テスト期待値 vs 実出力の機械的検証など、「同じになったはず」を客観的に証明する場面で用いられる。

Linux 視点だと `cmp` / `diff` の単純比較に相当する。出力は「差分があった箇所のレコード番号 + 内容」と「最終総括 (ALL RECORDS PROCESSED / UNEQUAL COMPARE)」だけで、編集や同期は行わない。**「コピーが正しく行えたか」「マイグレーション前後で壊れていないか」を確認する受け身の道具** であり、運用テスト工程で IEBGENER / IEBCOPY と組で使われる。

## 2. mechanism（どう動くか）

### 基本 JCL 構造

```
//COMP  EXEC PGM=IEBCOMPR
//SYSPRINT DD SYSOUT=*
//SYSUT1   DD DSN=入力1,DISP=SHR
//SYSUT2   DD DSN=入力2,DISP=SHR
//SYSIN    DD DUMMY
```

PDS 同士の比較は SYSIN に `COMPARE TYPORG=PO` を書く + member 名の列挙を組み合わせる。順次データセット同士は SYSIN を DUMMY にして全件比較で済む。

### 比較ロジック

- レコードを 1 件ずつ読み、SYSUT1 と SYSUT2 を逐次対比
- 異なれば SYSPRINT に「レコード番号 / 両側のレコード内容」を出力
- 10 件まで差分を出力すると、それ以降は件数のみカウント (default、JCL で変更不可)
- 最終的に return code を返す: 0 = 完全一致、8 = 不一致、12 以上 = エラー

### 用途別パターン

- バックアップ → リストア後の同一性検証
- マイグレーションで PDS 配下を一斉移動した時の member 単位比較
- regression test で「期待出力ファイル」vs「実出力ファイル」の確認

### return code 運用

- RC=0 のみを合格にする条件分岐を後続 step `IF` で書く運用が定着
- 「差分があったらジョブ全体 ABEND」のような明示的失敗扱いをするかは現場判断

## 3. prerequisites

- ZOS-DATASET-001 (順次データセット / PDS)
- ZOS-JCL-001 (return code 条件分岐 / IF-THEN-ELSE)
- ZOS-IEBGENER-001 (典型的なペア利用)

## 4. relations

- `depends_on`: ZOS-DATASET-001, ZOS-JCL-001
- `contrasts_with`: ZOS-IEBGENER-001 (コピー), ZOS-IEBCOPY-001 (PDS コピー), ISPF `SuperC` (対話形式の高機能 diff)
- `used_by`: ZOS-RECOVERY-001 (リストア検証), ZOS-SMS-001 (移行後検証)

## 5. pitfalls

- DCB attribute (LRECL / RECFM) が一致しないと比較不能で RC=12、データ内容を比較する前に弾かれる
- 差分 10 件で出力打ち切り → 後続レコードの差分は数だけしか分からない、詳細が必要なら SuperC / ISPF 利用
- バイナリ差分のニュアンス (末尾 padding / EBCDIC vs ASCII 等) は IEBCOMPR は区別しない

## 6. examples

`examples.md` 参照。

## 7. decision_axes

- 「対話的に diff を見たい」 → ISPF SuperC
- 「3-way merge」 → 当ユーティリティ非対応、ISPF SuperCE / 他ツール
- 「JCL 自動工程の合否ゲート」 → IEBCOMPR + IF-THEN-ELSE

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

IBM 公式 manual を一次出典とし、バックアップ検証や migration 運用手順での IEBCOMPR 適用例を補強するため、市販書籍 (BK_MF_001 / BK_ZOS_BASIC_001 / BK_ZOS_TECH_001 等) を補助参照する。逐語引用禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
