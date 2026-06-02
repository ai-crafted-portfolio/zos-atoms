---
id: ZOS-JCL-001
title: JCL 基礎（JOB / EXEC / DD）
status: stable
last_reviewed: 2026-05-09
---


# ZOS-JCL-001: JCL 基礎

## 1. purpose（なぜ存在するか）

JCL（**J**ob **C**ontrol **L**anguage）は z/OS のバッチジョブ起動プロトコル。プログラム本体（COBOL/PL/I/Java/etc）を呼び出す前に、「**そのプログラムが使うデータセット・実行環境を全部宣言**」する。

Linux なら `myprog input.txt > output.txt 2>&1` で済む（ファイル名解決・出力先振り分けはシェルが動的に解釈）。z/OS は **静的・宣言的**: ジョブ実行前に「STDIN は USER.INPUT、STDOUT は USER.OUTPUT、ロードモジュールは PROD.LOAD から検索」を全部 JCL で書く。**プログラム側はそれを「論理名 (DDNAME)」で受け取る**ので、ソースコードを変えずに入出力先だけ変えられる。

このパターンは「I/O 抽象化」の極北。1960 年代のメインフレームで、プログラマがソース修正不要で本番機 → テスト機 → 災対機の入出力を切り替えるために設計された。今でも本番運用で重宝される（ソース修正は本番リリースだが、JCL 修正は運用作業）。

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

## 3. prerequisites（理解の前提）

- データセット概念（→ [ZOS-DATASET-001](zos-dataset-001.md)）
- カタログ（→ [ZOS-CATALOG-001](zos-catalog-001.md)）
- 一般 IT 知識: 環境変数による I/O 抽象化（DDNAME はそれの強烈版）

## 4. relations（他アトムとの繋がり）

- `depends_on`: [ZOS-DATASET-001](zos-dataset-001.md), [ZOS-CATALOG-001](zos-catalog-001.md)
- `specialized_by`: なし
- `contrasts_with`: [ZOS-TSO-001](zos-tso-001.md)（対話 vs バッチ）, （未作成）UNIX-SHELLSCRIPT-001
- `used_by`: [ZOS-DATASET-001](zos-dataset-001.md) (DD で参照), [ZOS-SORT-001](zos-sort-001.md) (PGM=SORT 起動), [ZOS-DUMP-001](zos-dump-001.md) (SYSMDUMP/SYSUDUMP DD)

## 5. pitfalls（実装・運用での落とし穴）

- **COND の逆論理で全ステップ skip**: `COND=(0,EQ)` を「RC=0 なら実行」と勘違い。**正しくは「RC=0 なら skip」**。本番でステップが全部走らずジョブ「正常終了」して気付かない事案。`IF/THEN/ELSE/ENDIF` 構文を使うべき、こっちは順方向の論理。
- **STEPLIB に古いロード残置**: 障害調査で STEPLIB に新ロード混ぜたが古いデータセットを除去してない → ロードモジュール検索順で古い方が hit、修正反映されず再障害。STEPLIB は連結の **左から検索**。
- **DSN 連続する `,DISP=(NEW,CATLG,DELETE)` を継承**: 過去 JCL のコピペで `DISP=NEW` のまま使い、既存 DSN と衝突して `IEF285I` で deallocate 失敗。DISP の意味理解せずにコピペが破綻原因。
- **REGION=0M で OOM 連鎖**: REGION=0M は「上限なし」だが、システムの SQA/CSA を食い潰すと隣のジョブを ABEND させる。本番は明示的サイズ（256M, 512M 等）が原則。0M は開発・調査用。
- **ジョブ名重複で `IEF453I JOB FAILED - JCL ERROR`**: 同名ジョブが既に Active だと（JES の duplicate job name check）2 個目は走らない、または待たされる。世代管理用に suffix（YYYYMMDDHHMM 等）を付ける運用が普通だが、付け忘れて夜間バッチが翌朝になって動き出す事故。
- **PROC のシンボル置換失敗**: `&DSN.` のようにピリオドで終端を明示しないと、続く文字と連結されてシンボル解決失敗。`USER.&DSN..PROD` の二重ピリオド必須。これは知らないと数時間溶ける罠。

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

## 7. decision_axes（採否を分ける判断軸）

- **COND vs IF/THEN/ELSE**: IF/THEN/ELSE は読みやすく、複数ステップ参照も楽。**新規 JCL は IF/THEN/ELSE 推奨**、既存 JCL の保守は COND のまま（一斉書換のリスクが大）。
- **JOBLIB vs STEPLIB**: STEPLIB はステップ毎、JOBLIB は全ステップ共通。**JCL の中で 1 つの STEP が別ロードを使う**ようなテストでは STEPLIB を使い分ける。本番 JCL は JOBLIB 1 行で済ますのが管理楽。
- **PROC vs INCLUDE**: PROC はパラメータ化（symbol）が強力だが置換失敗の罠。INCLUDE は単純コピペで分かりやすいが再利用性低い。**シンボル置換が必要なら PROC、定型の塊だけ繰り返すなら INCLUDE**。
- **COND=ONLY / COND=EVEN**: COND=ONLY は「直前 ABEND した時だけ実行」（クリーンアップ用）、COND=EVEN は「直前 ABEND しても実行」（ロギング用）。**普通は使わないが、本番で使う時はコメントを大量に書く**。
- **CLASS / MSGCLASS の運用設計**: ジョブクラス（A, B, ...）はジョブ実行優先度・並列度を決める。**サイトの classes 設計を理解せず CLASS=A 固定で出すと、夜間バッチに紛れて翌朝走る事故**あり。
