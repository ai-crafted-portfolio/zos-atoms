---
id: ZOS-IEFBR14-001
title: IEFBR14 + dummy step utility
status: stable
last_reviewed: 2026-06-02
authors: [Z2]
rag_verified: true
---
# ZOS-IEFBR14-001: IEFBR14 + dummy step utility

## 1. purpose（なぜ存在するか）

IEFBR14 は **「何もしない」プログラム** (アセンブラ命令 `BR 14` 1 行) で、JCL step として実行されると即 RC=0 で正常終了する。狙いは **dataset の allocate/ delete / catalog 操作だけを JCL の DISP で起こすこと**。何かを「処理する」プログラムが要らないため、運用の足場 utility として標準化された。

Linux の shell の `:` (null command) や `true` に似ているが、IEFBR14 は **JCL のDD と DISP 系統と組み合わせて副作用 (allocate / delete / catalog 化) を起こす点で意味が違う**。Windows batch の `rem` も「何もしない」だがファイル操作の副作用は持たない。

## 2. mechanism（どう動くか）

- 実体は SYS1.LPALIB の load module。コードは `BR 14` (= return) のみで、  load → 即 control 戻る。RC は R15 残値 = 通常 0
- JCL の各 DD の `DISP=(status, normal-disp, abnormal-disp)` が step 終了時に  起動する: NEW なら allocate、CATLG/KEEP/DELETE の指示通り
- 例: `DD DSN=...,DISP=(NEW,CATLG,DELETE),SPACE=(CYL,(5,1))` で「step 内で何も  処理しないけど dataset は新規作成して catalog に登録」が成る
- 例: `DD DSN=...,DISP=(OLD,DELETE,DELETE)` で「step 内で何もしないけど step 終了  時に dataset を削除 (= 実質 dataset 削除 utility)」が成る
- COND 制御の入口としても使う。前 step の RC を見て後続 step の skip 判定する時、  IEFBR14 を最初の step に置いて RC=0 で確実に通すパターン
- `PARM=` は無視される (受け取らない)。R1 が指す parm 領域には触れない
- 拡張: IEFBR14 は SYS1.LPALIB から **共有 LPA 経由** で load されるため、超軽量。  CPU = 命令 1 つ、I/O = load module 1 page

## 3. prerequisites（理解の前提）

- JCL の DD と DISP の仕組み — `ZOS-JCL-001`
- dataset の allocate / catalog 化 — `ZOS-DATASET-001`, `ZOS-CATALOG-001`
- COND parameter の論理 (RC 比較)
- 一般 IT 知識: shell の null command 概念

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-JCL-001, ZOS-DATASET-001
- `specialized_by`: なし
- `contrasts_with`: Linux shell `:` / `true` / `touch` + `rm`,
  Windows batch `rem` + `del`
- `used_by`: ZOS-JCL-001 (テンプレ step), ZOS-RECOVERY-001 (clean-up step),
  ZOS-DATASET-001 (allocate 経路)

## 5. pitfalls（実装・運用での落とし穴）

- **DD で DISP=NEW を期待したのに既存 dataset が DELETE 化**: `DISP=(NEW,CATLG,DELETE)` で IEFBR14 を流したら、想定外に既存 dataset があった場合 `JCL ERROR IGD17103I` で job が落ち、DISP の abnormal 側(DELETE) が **既存 dataset を消す** 事故。防御として `DISP=(MOD,CATLG,DELETE)` か事前 `IDCAMS DELETE` step を入れるのが SOP。NEW 系 IEFBR14 の前に既存確認は site 規約として必須。
- **COND=(0,EQ) の逆論理で意図と逆に skip**: `COND=(0,EQ,STEP1)` は **STEP1 の RC が 0 と等しい時に当該 step を skip**という二重否定的論理。初心者が「STEP1 が 0 なら実行」と読み違える。IEFBR14 を「成功時通過、失敗時 skip」の sentinel に使う設計で COND を逆向きに書いてしまい、本番フローが想定と逆に流れる事故。新規 JCL は **IF/THEN/ELSE/ENDIF** を使い、古い COND は使わない方針が安全。
- **Allocate 失敗 (volume なし等) で JCL ERROR**: IEFBR14 自体は失敗しないが、DD の allocate が失敗 (例: VOL=SER 指定のvolume が offline) すると step は実行されずに JCL ERROR。「IEFBR14 = 必ず成功」と思って後続 step の COND を組むと、allocate 失敗時の挙動が想定外。SMS 化された site では UNIT/VOL 指定を抜く方向にしてallocate 失敗確率を下げるが、非 SMS site では DD 順序と SMF 30 で確認が要る。
- **VOL=SER 指定で dummy step が想定外 volume 占有**: テスト用の clean-up IEFBR14 で `VOL=SER=TESTV1` を指定したまま本番にpromote すると、本番で TESTV1 volume を占有 (排他) して他 job が wait。VOL=SER は site 移送時に必ず除去するチェックリストが要る。site SMS なら DATACLAS/STORCLAS のみ指定し、VOL/UNIT を JCL から消すのが現代的。
- **IEFBR14 で SYSUDUMP / SYSABEND DD を入れて常時容量食う**: テンプレ流用で `//SYSUDUMP DD SYSOUT=*` を IEFBR14 step にも入れたままになると、ABEND しなくても spool 上に空 record / 関連 dataset が allocateされて溜まる site がある。IEFBR14 は ABEND しないので SYSUDUMP は不要。site テンプレ JCL に default で付けてる場合は IEFBR14 step では明示削除するか `DD DUMMY` にする。

## 6. examples（具体例）

```jcl
//* 用途 1: dataset allocate のみ (NEW + CATLG)
//STEP1    EXEC PGM=IEFBR14
//OUTDD    DD DSN=USER.PROD.NEW,
//            DISP=(NEW,CATLG,DELETE),
//            DCB=(DSORG=PS,RECFM=FB,LRECL=80,BLKSIZE=27920),
//            SPACE=(CYL,(5,1),RLSE),
//            UNIT=SYSDA
```

```jcl
//* 用途 2: dataset 削除のみ
//STEP1    EXEC PGM=IEFBR14
//OLDDD    DD DSN=USER.PROD.OLD,DISP=(OLD,DELETE,DELETE)
```

```jcl
//* 用途 3: 前 step の RC 検査の sentinel として
//STEP1    EXEC PGM=IEFBR14         先頭で必ず RC=0 を立てる
//STEP2    EXEC PGM=MYPROG,COND=(0,NE,STEP1)
//* STEP1 が 0 でないなら STEP2 を skip = ありえないので必ず実行
```

```jcl
//* 用途 4: IF/THEN/ELSE/ENDIF で flow 制御 (推奨の現代的書き方)
//STEP1    EXEC PGM=MYPROG
// IF (STEP1.RC = 0) THEN
//STEP2A   EXEC PGM=IEFBR14    success path で何もせず通る
// ELSE
//STEP2B   EXEC PGM=NOTIFY     failure 通知
// ENDIF
```

## 7. decision_axes（採否を分ける判断軸）

- **IEFBR14 vs IDCAMS DELETE (削除手段)**: dataset 削除だけが目的なら (a) IEFBR14 + `DISP=(OLD,DELETE,DELETE)` か (b) IDCAMS `DELETE 'xxx'`。(a) は dataset が無いと JCL ERROR、(b) は無くても RC=8 で続行可。**冪等性が欲しい automation は IDCAMS**、**JCL 内で 1 行で済ませたいならIEFBR14**。CI/CD で何度も再実行する batch なら IDCAMS 一択。
- **COND parameter (旧) vs IF/THEN/ELSE/ENDIF (新)**: COND は二重否定論理で誤読しやすい。IF/THEN/ELSE/ENDIF は素直に「RC=0 なら実行」と書ける。**新規 JCL は IF/THEN/ELSE 一択**、既存 COND は読み替えコメントを必ず付ける。site 規約として「新規 IEFBR14 sentinel 禁止、IF/THEN/ELSE で書け」と決めてる先進 site も多い。
- **IEFBR14 の bulk allocate vs ISPF 3.2 / TSO ALLOC**: 1 dataset の allocate なら ISPF 3.2 / TSO `ALLOC` コマンドが速い。10+ dataset の bulk allocate / scheduler 制御下なら JCL + IEFBR14 が再現性 + audit trail で勝る。**ad-hoc 1 件は ISPF、bulk + 自動化は JCL** が SOP。
- **IEFBR14 step 単独 vs main step 内で副作用**: main 処理 step の DD に副作用 (allocate / delete) を入れることもできるが、main 処理が失敗した時に dataset 状態が不定になる。**副作用は独立 IEFBR14 step に分離**、main step は処理に集中、という分割が運用整理として明らかに勝つ。debugging で各 step の状態を切り分けやすい利点もある。

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_BASIC_001) から IEFBR14 / DD 文 allocate パターンを概念蒸留 (ADR-0109)。書籍は概念補助。
