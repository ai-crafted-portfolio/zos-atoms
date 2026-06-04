---
id: ZOS-JCL-001
title: JCL 基礎（JOB / EXEC / DD）
status: stable
last_reviewed: 2026-05-09
authors: [agent]
rag_verified: partially
---

# ZOS-JCL-001: JCL 基礎

## 1. purpose（なぜ存在するか）

JCL（**J**ob **C**ontrol **L**anguage）は z/OS のバッチジョブ起動プロトコル。プログラム本体（COBOL/PL/I/Java/etc）を呼び出す前に、「**そのプログラムが使うデータセット・実行環境を全部宣言**」する。

Linux なら `myprog input.txt > output.txt 2>&1` で済む（ファイル名解決・出力先振り分けはシェルが動的に解釈）。z/OS は **静的・宣言的**: ジョブ実行前に「STDIN は USER.INPUT、STDOUT は USER.OUTPUT、ロードモジュールは PROD.LOAD から検索」を全部 JCL で書く。**プログラム側はそれを「論理名 (DDNAME)」で受け取る**ので、ソースコードを変えずに入出力先だけ変えられる。

このパターンは「I/O 抽象化」の極北。1960 年代のメインフレームで、プログラマがソース修正不要で本番機 → テスト機 → 災対機の入出力を切り替えるために設計された。今でも本番運用で重宝される（ソース修正は本番リリースだが、JCL 修正は運用作業）。

書籍 (BK_MF_001 / BK_ZOS_TECH_001) から蒸留した補強観点では、JCL は **「実行時点の運用環境契約」** として位置付けると本質を捉えやすい。本番 / 開発 / 災対 でロード元・出力先・課金アカウントが入れ替わる前提なので、JCL を「プログラムの一部」と見ると設計を誤る。プログラムは「論理名で I/O を要求する側」、JCL は「論理名を物理リソースに束ねる契約書」というレイヤ分離を強く意識する。

## 2. mechanism（どう動くか）

JCL は **3 種類の文** から成る:

- **JOB**: ジョブ全体の宣言。`//JOBNAME JOB acct,name,CLASS=A,MSGCLASS=X,REGION=0M`
- **EXEC**: ステップの実行。`//STEP01 EXEC PGM=COBPROG,PARM='ABC'` または `//STEP01 EXEC PROC=MYPROC`
- **DD**: Data Definition。`//SYSIN DD DSN=...` または `//SYSOUT DD SYSOUT=*`

実行モデル:
1. JES2/JES3 が JCL 受領
2. **変換 (Conversion)**: JCL 構文チェック + PROC 展開 + シンボル置換
3. **解釈 (Interpretation)**: データセット allocate (ENQ 取得) → DEB 構築
4. **実行 (Execution)**: PGM をロード、ATTACH。プログラムは DDNAME で I/O。終了時に RC を返す
5. **出力 (Output)**: SYSOUT を spool に保存、ジョブログを残す
6. **パージ (Purge)**: データセットを deallocate

主要パラメータ:
- `DISP=(state,normal,abnormal)`: state は OLD/NEW/MOD/SHR、normal/abnormal は KEEP/CATLG/DELETE/UNCATLG
- `COND=(rc,op,step)`: 直前の RC 評価で当ステップ skip するか判定。`COND=(4,LT)` で「前ステップ RC が 4 未満なら **skip**」（**条件は skip 条件**）
- `JOBLIB` / `STEPLIB`: ロードモジュール検索パス

書籍 (BK_ZOS_TECH_001 / BK_ZOS_TECH_002) からの運用観点での補強として、JCL の実行モデルは「変換 → 解釈 → 実行」の 3 段が論理的に独立した別フェーズである点が重要。**変換フェーズで落ちる JCL エラー (`JCL ERROR`) は、プログラム本体は 1 命令も実行されていない**。一方 **解釈フェーズで落ちるアロケーション失敗 (例: `IEF212I DATASET NOT FOUND`) は、それ以前のステップは既にコミット済 (DISP=CATLG されたデータセットは残る)**。本番運用での障害切り分けで「どこまで進んでいたか」を判定する時、この 3 フェーズ境界を意識すると JOBLOG の読み方が変わる。

## 3. prerequisites（理解の前提）

- データセット概念（→ ZOS-DATASET-001）
- カタログ（→ ZOS-CATALOG-001）
- 一般 IT 知識: 環境変数による I/O 抽象化（DDNAME はそれの強烈版）

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-DATASET-001, ZOS-CATALOG-001
- `specialized_by`: なし
- `contrasts_with`: ZOS-TSO-001（対話 vs バッチ）, （未作成）UNIX-SHELLSCRIPT-001
- `used_by`: ZOS-DATASET-001 (DD で参照), ZOS-SORT-001 (PGM=SORT 起動), ZOS-DUMP-001 (SYSMDUMP/SYSUDUMP DD)

## 5. pitfalls（実装・運用での落とし穴）

- **COND の逆論理で全ステップ skip**: `COND=(0,EQ)` を「RC=0 なら実行」と勘違い。**正しくは「RC=0 なら skip」**。本番でステップが全部走らずジョブ「正常終了」して気付かない事案。`IF/THEN/ELSE/ENDIF` 構文を使うべき、こっちは順方向の論理。
- **STEPLIB に古いロード残置**: 障害調査で STEPLIB に新ロード混ぜたが古いデータセットを除去してない → ロードモジュール検索順で古い方が hit、修正反映されず再障害。STEPLIB は連結の **左から検索**。
- **DSN 連続する `,DISP=(NEW,CATLG,DELETE)` を継承**: 過去 JCL のコピペで `DISP=NEW` のまま使い、既存 DSN と衝突して `IEF285I` で deallocate 失敗。DISP の意味理解せずにコピペが破綻原因。
- **REGION=0M で OOM 連鎖**: REGION=0M は「上限なし」だが、システムの SQA/CSA を食い潰すと隣のジョブを ABEND させる。本番は明示的サイズ（256M, 512M 等）が原則。0M は開発・調査用。
- **ジョブ名重複で `IEF453I JOB FAILED - JCL ERROR`**: 同名ジョブが既に Active だと（JES の duplicate job name check）2 個目は走らない、または待たされる。世代管理用に suffix（YYYYMMDDHHMM 等）を付ける運用が普通だが、付け忘れて夜間バッチが翌朝になって動き出す事故。
- **PROC のシンボル置換失敗**: `&DSN.` のようにピリオドで終端を明示しないと、続く文字と連結されてシンボル解決失敗。`USER.&DSN..PROD` の二重ピリオド必須。これは知らないと数時間溶ける罠。
- **NOTIFY 設定漏れで深夜障害に気付かない (BK_MF_001 / BK_ZOS_TECH_002 概念蒸留)**: 夜間バッチで `NOTIFY=&SYSUID` を入れ忘れた結果、ABEND しても担当者の TSO に通知が来ず、翌朝出社して初めて発覚するパターン。**運用 SOP で「全 JCL に NOTIFY 必須」を構文チェッカで強制**しないと、新人が古い JCL をコピペして再発させる。
- **GDG 世代の `(+1)` を 2 ステップで使い分けるルール忘れ**: 同一ジョブ内で `(+1)` が一貫して「新世代」を指す前提だが、ジョブ間で `(+1)` の意味が変わる。GDG 設計と JCL を分けて管理する運用が前提だが、混同で本番世代を上書きする事故あり。
- **DUMMY 指定の意味取り違え**: `//SYSIN DD DUMMY` は EOF 即返し、書き出しは捨て。「DUMMY = 空ファイル」と勘違いして実体の存在を期待するロジックを組むと、後で値が無くなって ABEND。DUMMY は I/O を no-op 化する宣言であって「データ無し」ではない。

## 6. examples（具体例）

```jcl
//MYJOB    JOB (ACCT),'NAME',CLASS=A,MSGCLASS=X,REGION=128M,
//             NOTIFY=&SYSUID
//STEP01   EXEC PGM=IEBGENER
//SYSPRINT DD SYSOUT=*
//SYSIN    DD DUMMY
//SYSUT1   DD DSN=USER.PROD.IN,DISP=SHR
//SYSUT2   DD DSN=USER.PROD.OUT,DISP=(NEW,CATLG,DELETE),
//             SPACE=(CYL,(5,1)),DCB=(*.SYSUT1)
//STEP02   EXEC PGM=COBPROG,COND=(4,LT,STEP01)
//STEPLIB  DD DSN=PROD.LOAD,DISP=SHR
//SYSIN    DD DSN=USER.PROD.OUT,DISP=SHR
//SYSPRINT DD SYSOUT=*
```

```jcl
//* IF/THEN/ELSE 構文
//IF (STEP01.RC <= 4) THEN
//STEP03 EXEC PGM=POSTPGM
//ENDIF
```

書籍 (BK_ZOS_TECH_001 / BK_ZOS_TECH_002) 蒸留の運用パターン: 本番 JCL の冒頭に `JOBPARM` 系コメントで「目的 / 起動契機 / 関係者 / 異常時連絡先」を 4-5 行で残す慣習が、長寿命システムでは事実上の標準。**コメント行はジョブ本体動作に影響しないが、3 年後に障害対応する担当者にとっては設計書より読まれる**。

```jcl
//* ============================================================
//* JOB    : DAILY SALES AGGREGATION
//* TRIGGER: SCHEDULED 23:00 BY OPS_SCHED
//* OWNER  : TEAM-ACCT (xxxx@xx.xx)
//* ON FAIL: CALL OPS-DESK 24H, RERUN AT 06:00 LATEST
//* ============================================================
```

## 7. decision_axes（採否を分ける判断軸）

- **COND vs IF/THEN/ELSE**: IF/THEN/ELSE は読みやすく、複数ステップ参照も楽。**新規 JCL は IF/THEN/ELSE 推奨**、既存 JCL の保守は COND のまま（一斉書換のリスクが大）。
- **JOBLIB vs STEPLIB**: STEPLIB はステップ毎、JOBLIB は全ステップ共通。**JCL の中で 1 つの STEP が別ロードを使う**ようなテストでは STEPLIB を使い分ける。本番 JCL は JOBLIB 1 行で済ますのが管理楽。
- **PROC vs INCLUDE**: PROC はパラメータ化（symbol）が強力だが置換失敗の罠。INCLUDE は単純コピペで分かりやすいが再利用性低い。**シンボル置換が必要なら PROC、定型の塊だけ繰り返すなら INCLUDE**。
- **COND=ONLY / COND=EVEN**: COND=ONLY は「直前 ABEND した時だけ実行」（クリーンアップ用）、COND=EVEN は「直前 ABEND しても実行」（ロギング用）。**普通は使わないが、本番で使う時はコメントを大量に書く**。
- **CLASS / MSGCLASS の運用設計**: ジョブクラス（A, B, ...）はジョブ実行優先度・並列度を決める。**サイトの classes 設計を理解せず CLASS=A 固定で出すと、夜間バッチに紛れて翌朝走る事故**あり。


## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

本 atom の領域については、IBM 公式 manual を一次出典としつつ、運用事例や設計判断の補強として市販書籍 (BK_MF_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 等の z/OS / メインフレーム関連書籍) からの実装知識を補助的に参照する。逐語引用は禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
