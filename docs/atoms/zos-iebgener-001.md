---
id: ZOS-IEBGENER-001
title: IEBGENER / Sequential Dataset Copy Utility
status: stable
last_reviewed: 2026-06-04
authors: [agent]
rag_verified: partially
---

# ZOS-IEBGENER-001: IEBGENER / Sequential Dataset Copy Utility

## 1. purpose（なぜ存在するか）

IEBGENER は **順次データセット (PS) を別の順次データセットへ単純コピー** する用途で使われる IBM 標準ユーティリティ。SYSUT1 (入力) → SYSUT2 (出力) という一方向の流れだけを扱い、レコード長変換、カラム抽出、ヘッダ追加といった軽い変換も SYSIN コントロール文で指定可能。

Linux 視点だと `cp` + `awk` の中間に位置し、「データセット世界の汎用コピー兼軽編集ツール」 と捉えると分かりやすい。SORT を持ち出すほどではない単純コピー、テスト用 input 生成、PDS member の取り出しといった日常タスクで JCL に頻出する。後発の ICEGENER (DFSORT 同梱の高速代替) が同名 step として動くケースも多く、運用上は実体が ICEGENER であることが少なくない。

## 2. mechanism（どう動くか）

### 基本 JCL 構造

```
//COPY  EXEC PGM=IEBGENER
//SYSPRINT DD SYSOUT=*
//SYSUT1   DD DSN=入力DSN,DISP=SHR
//SYSUT2   DD DSN=出力DSN,DISP=(NEW,CATLG),...
//SYSIN    DD DUMMY
```

SYSIN が DUMMY なら単純全件コピー、SYSIN にコントロール文を書けば LRECL 変更や field 編集が可能。

### SYSIN コントロール文

- `GENERATE MAXFLDS=n` — 編集 field 数を宣言
- `RECORD FIELD=(長さ, 入力開始位置, 変換, 出力開始位置)` — カラム単位の編集指示
- `LABELS` / `MEMBER NAME=` — PDS member 単位の処理

### ICEGENER aliasing

DFSORT 入りシステムでは IEBGENER 呼出を ICEGENER (SORT 利用の高速版) に置換するオプション (`ICEAM1` 等の install option) が有効化されている場合があり、運用者から見ると同じ JCL で透過的に高速化される。

### 用途別パターン

- PS → PS 単純コピー (バックアップ取り)
- PS → SYSOUT 印刷出力
- インストリーム data (`DD *`) を PS に流し込む (テスト input 作成)
- 部分 field の取り出し / 編集 (簡易 ETL)

## 3. prerequisites

- ZOS-DATASET-001 (順次データセット概念)
- ZOS-JCL-001 (DD statement / DISP / SYSOUT)
- ZOS-IDCAMS-001 (対比: VSAM 用ユーティリティ)

## 4. relations

- `depends_on`: ZOS-DATASET-001, ZOS-JCL-001
- `contrasts_with`: ZOS-IEBCOPY-001 (PDS 専用コピー), ZOS-SORT-001 (大量 / 編集を伴うコピー), ZOS-IDCAMS-001 (VSAM 用)
- `used_by`: ZOS-RECOVERY-001 (バックアップ手順), ZOS-SMS-001 (データ移行)

## 5. pitfalls

- ICEGENER 透過置換でログ出力 (SYSPRINT) のフォーマットが異なる → ジョブログ自動解析スクリプトが壊れる
- 大量レコードを単純コピーする時は SORT/COPY や DFDSS の方が圧倒的に速く、IEBGENER 固執で運用時間を浪費しがち
- DCB 不一致 (LRECL/RECFM/BLKSIZE) は SYSUT2 側で明示しないと OPEN ABEND する

## 6. examples

`examples.md` 参照。

## 7. decision_axes

- 「PDS member 単位ならどうする?」 → IEBCOPY 採用
- 「条件付き選択 / SORT KEY 付き出力なら?」 → SORT 採用
- 「VSAM への変換も含むなら?」 → IDCAMS REPRO 採用

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

IBM 公式 manual を一次出典とし、運用慣習や ICEGENER 置換の実例補強として市販書籍 (BK_MF_001 / BK_ZOS_BASIC_001 / BK_ZOS_TECH_001 等) を補助的に参照する。逐語引用禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
