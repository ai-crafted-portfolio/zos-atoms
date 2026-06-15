---
id: ZOS-DUMP-001
title: SVC ダンプ / SYSMDUMP / SYSUDUMP / SYSABEND
status: stable
last_reviewed: 2026-06-01
authors: [agent]
rag_verified: partially
---

# ZOS-DUMP-001: SVC ダンプ系

## 1. purpose（なぜ存在するか）

ダンプは ABEND または異常検知時に **アドレス空間（または LPAR 全体）の主記憶スナップショット** を DASD に書き出す機構。事後解析でレジスタ・PSW・コントロールブロック・ストレージを追跡し、根本原因を特定する。

Linux なら `core dump` ファイルを gdb で開くが、z/OS のダンプは **複数種類** あり、それぞれ「誰が起こすか」「何を含むか」「どう解析するか」が違う。これは「アドレス空間のスコープ」「PSW から見える領域」「システム空間（CSA/SQA/LPA）の含有」が分離されているメインフレーム特有の構造に対応している。

主な区別:
- **SVC dump**: システム発行（操作員 or 障害検知）の包括ダンプ。複数アドレス空間を一括捕捉。`SDUMP` macro / `DUMP COMM=(...)` コマンド。
- **SYSMDUMP**: アドレス空間個別、機械可読バイナリ（IPCS で読む）。
- **SYSUDUMP**: アドレス空間個別、フォーマット済テキスト（人間可読）。最小情報。
- **SYSABEND**: SYSUDUMP より広範な領域を含む人間可読ダンプ（LSQA, SWA, subpools 等）。

解析の主力ツールは **IPCS（Interactive Problem Control System）** で、SVC dump / SYSMDUMP をロードして対話的に subcommand で掘る。SYSUDUMP / SYSABEND はテキストなのでテキストエディタで開ける。

## 2. mechanism（どう動くか）

- **SVC dump の発行経路**: SDUMP macro（COBOL/PL/I/Assembler 内）、`DUMP COMM=(タイトル)` コンソール、SLIP trap 発火、recovery routine（FRR/ESTAE）
- **DUMP の宛先**: `SYS1.DUMPxx` データセット（PRE-ALLOCATED、xx は 00〜99 のスロット）。`CHNGDUMP SET,SDUMP,...` で対象 / 除外 領域を制御。
- **SYSMDUMP / SYSUDUMP / SYSABEND の宛先**: アプリ JCL に DD カードを置く（`//SYSMDUMP DD SYSOUT=*` 等）。DD が無いとダンプは出ない。
- **コンソール書式**: ABEND コード `S0C7` = システムコード x'0C7'（データ例外 = packed decimal 不正）。`U0010` = ユーザコード 0010。`S0C4` = プロテクト例外。
- **IPCS の主要 subcommand**:
  - `STATUS REGS` レジスタ
  - `STATUS CPU` PSW + CPU 状態
  - `STATUS FAILDATA` 障害サマリ
  - `SUMMARY FORMAT` 全 TCB ツリー
  - `LIST address LEN(n)` ストレージダンプ
  - `WHERE address` アドレス所属領域判定（モジュール名解決）
  - `VERBX LOGDATA` ロジレックレコード（recovery 痕跡）
  - `IP RUNCHAIN ASID(x)` 全 RB / TCB ウォーク
- **CHNGDUMP**: SDUMP のデフォルト含有領域変更。`CHNGDUMP SET,SDUMP,Q=NO` で SQA を除外（容量節約）。

## 3. prerequisites（理解の前提）

- アドレス空間と private/common 領域の分離（CSA/SQA/LPA/Private）
- TCB / RB / SVRB の概念（タスク制御ブロック / Request Block）
- JCL の DD 文 — `ZOS-JCL-001`
- SMF（ロジレックレコード type 99 等） — `ZOS-SMF-001`
- データセット — `ZOS-DATASET-001`

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-JCL-001, ZOS-SMF-001, ZOS-DATASET-001
- `specialized_by`: なし（SVC/SYSM/SYSU/SYSABEND は axis 内別種）
- `contrasts_with`: Linux core dump（gdb 解析）, Windows minidump（WinDbg 解析）
- `used_by`: ZOS-CICS-001（CICS transaction dump = SVC dump 派生）, ZOS-IMS-001（IMS region dump）, ZOS-DB2-001（DSNWDMP）

## 5. pitfalls（実装・運用での落とし穴）

- **SYS1.DUMPxx スロット枯渇で重要 dump 取れず**: 100 スロット全部使用済だと **次の SVC dump は捨てられる**（`IEA793A` / `IEA045I`）。日次 `DD CLEAR,DSN=SYS1.DUMP*` でスロット解放する運用、または `AUTO COPY` で自動退避 + DELETE 設定。「障害発生 → ダンプ無い → 解析不能」の典型事故。
- **SYSMDUMP と SYSUDUMP 両方書いて二重コスト**: 同アプリ JCL に両方の DD があると **両方のダンプが書かれる**。重複 + DASD 二倍消費。**SYSMDUMP（IPCS 解析）+ SYSABEND 簡易概要** または **SYSMDUMP のみ** が現代の運用標準。
- **`SYSOUT=*` SYSMDUMP で spool 逼迫**: SYSMDUMP を spool（SYSOUT）に出すと、1 ダンプ数百 MB 〜 GB が SPOOL を埋める。**SYSMDUMP は SYSOUT じゃなく DSN= の永続データセット** に書く。SYSUDUMP/SYSABEND は SYSOUT で良い。
- **CHNGDUMP `SQA=NO` で必要な領域抜け**: SQA を含めないと SLIP trap 系の調査で痕跡が残らない。容量節約のための `SQA=NO` が「次の障害解析不能」を生む。**運用ベースラインは LSQA + RGN + SWA + SUMDUMP**、SQA は障害監視時に追加。
- **SLIP trap 連発で全アドレス空間ダンプ**: `SLIP SET,IF,...,ACTION=SVCD` で trap 仕掛けて、想定外多発で全アドレス空間 dump を量産、SYS1.DUMP00〜99 全部使われて他障害取れず。**SLIP は MATCHLIM= 必須**（n 回で自動解除）。
- **ABEND と RETRY 連鎖でダンプが取れない**: recovery routine（ESTAE）が RETRY すると abnormal termination が完了せず、SYSMDUMP/SYSUDUMP DD が機能しない。**FRR/ESTAE の SDWA で SDUMP 取得 → RETRY** のロジックを recovery routine 側に組む必要あり。
- **IPCS で `WHERE` がモジュール解決失敗**: ロードモジュールのリンクマップ（Linkage Editor の SYSPRINT）と SMF の `MODULE LOAD` レコードが揃っていないと、`WHERE` がアドレスを「Unresolved」と返す。**load library の更新時はリンクマップ保存** が運用ルール。
- **転送漏れによる解析失敗**: SVC dump（DSN）を分析者環境に転送する時、バイナリ転送 (BINARY) でないと文字コード変換で壊れる。FTP の ASCII / EBCDIC モード混在が事故源。**IPCS dump は EBCDIC バイナリのまま転送**。

## 6. examples（具体例）

```jcl
//* アプリで ABEND 時に SYSMDUMP を取る
//STEP1   EXEC PGM=MYPROG
//SYSMDUMP DD DSN=USER.MYPROG.DUMP,DISP=(NEW,CATLG,DELETE),
//           SPACE=(CYL,(50,10)),DCB=(RECFM=FBS,LRECL=4160,BLKSIZE=4160)
//SYSABEND DD SYSOUT=*
```

```text
* コンソール操作: 特定アドレス空間の SVC dump 取得
DUMP COMM=(MYPROBLEM)
R nn,ASID=(00A1),SDATA=(LSQA,RGN,SQA,CSA,LPA,SWA,TRT,SUM),END

* CHNGDUMP で SQA を SDUMP デフォルトから除外
CHNGDUMP SET,SDUMP,Q=NO

* SLIP trap (PSW addr 範囲 hit で dump)
SLIP SET,IF,LPAEQ=(00A1),RANGE=(8C000-8C0FF),ACTION=SVCD,MATCHLIM=3,END
```

```text
* IPCS 解析セッション抜粋
IPCS
  DSNAME('USER.MYPROG.DUMP')
  STATUS FAILDATA
  STATUS REGS
  SUMMARY FORMAT
  WHERE 8C0040
  LIST 8C0040 LENGTH(X'80')
  VERBX LOGDATA
```

## 7. decision_axes（採否を分ける判断軸）

- **SVC dump vs SYSMDUMP vs SYSUDUMP vs SYSABEND**: SVC dump はシステム規模で IPCS 必須。SYSMDUMP はアドレス空間 + IPCS（推奨）。SYSUDUMP は人間可読・即読みだが情報少。SYSABEND は人間可読 + 広範領域（中規模問題向け）。**運用標準: SYSMDUMP を必須、ABEND 詳細欲しいときだけ SYSABEND 併用**。
- **DSN= 永続データセット vs SYSOUT=\* spool**: SYSMDUMP は **絶対 DSN=**（spool 逼迫防止）。SYSUDUMP / SYSABEND は SYSOUT=* で軽量化。**SYSOUT に SYSMDUMP を流すサイトは「SPOOL FULL」障害候補**。
- **CHNGDUMP の領域包含**: 標準 = `LSQA,RGN,SUMDUMP` + 監視時 + `SQA,CSA,LPA`。**容量と解析範囲のトレードオフ**。
- **dump 保存期間 + 自動退避**: 即時解析は 24h、保存は 30〜90 日が典型。AUTO COPY + HSM migrate で長期保存。**短期保存サイトは「過去事案の再現解析」が不可能** になる弱点。
- **SLIP trap 設計**: 「捕まえる条件」「自動解除条件」「対象アドレス空間絞り込み」の 3 軸。**MATCHLIM 無しの SLIP は本番禁止**。
- **dump 取らずに live debug**: 状態保存より MIPS 節約を優先するときは `DISPLAY GRS,...`, `DISPLAY ASM,...` 等のコンソール照会で済ますが、事後解析の証拠が残らないので **重大障害は必ず SVC dump 1 本以上**。


## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

本 atom の領域については、IBM 公式 manual を一次出典としつつ、運用事例や設計判断の補強として市販書籍 (BK_MF_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 等の z/OS / メインフレーム関連書籍) からの実装知識を補助的に参照する。逐語引用は禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
