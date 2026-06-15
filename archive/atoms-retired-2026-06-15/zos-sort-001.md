---
id: ZOS-SORT-001
title: DFSORT / Syncsort（メインフレーム sort/merge/copy utility）
status: stable
last_reviewed: 2026-06-01
authors: [agent]
rag_verified: partially
---

# ZOS-SORT-001: DFSORT / Syncsort

## 1. purpose（なぜ存在するか）

メインフレームバッチの **大半は「順次データセットを整列・突合・集計する」処理** で構成されており、それを COBOL で 1 から書く代わりに **JCL + 制御文だけで実行できる汎用 sort utility** が DFSORT / Syncsort。OS 直結の I/O 最適化と、数十年蓄積された制御言語（SORT / MERGE / OUTREC / INREC / OUTFIL）を持つ。

Linux なら `sort -k 5,10 -t',' input.csv > output.csv` で済むが、メインフレームでは **数百 GB の固定長レコードを数分で整列** する性能要件があり、汎用 `sort(1)` ではメモリ・I/O 効率が出ない。DFSORT は **DASD への SORTWK 一時データセット** + チャネル並列 I/O + dataspace 利用で、ハードウェアに張り付くチューニングがされている。

副次的に「ICETOOL」というメタユーティリティが DFSORT 上に乗っており、`UNIQUE`, `OCCUR`, `STATS`, `RANGE`, `SPLICE` 等の高水準演算を制御文で書ける。COBOL を書かずに大半のバッチ集計が ICETOOL で済む現場が多い。

## 2. mechanism（どう動くか）

- 入力 DD: `SORTIN`（または `SORTINnn` で複数連結）
- 出力 DD: `SORTOUT`（または `OUTFIL` で複数出力）
- 制御文 DD: `SYSIN`（または `DFSPARM`）
- 作業域 DD: `SORTWK01〜SORTWKnn`（DASD 上の一時 work）または `DSPSIZE` で dataspace 利用
- 制御文の主要動詞:
  - `SORT FIELDS=(start,length,format,A/D)`: ソートキー（A=昇順, D=降順）
  - `MERGE FIELDS=...`: 既ソート複数入力をマージ
  - `INCLUDE COND=(...)`: フィルタ
  - `OMIT COND=(...)`: フィルタ（逆論理）
  - `INREC FIELDS=(...)`: 入力レコード再構成
  - `OUTREC FIELDS=(...)`: 出力レコード再構成
  - `OUTFIL FILES=01,INCLUDE=(...)`: 条件別複数出力
  - `SUM FIELDS=(start,length,format)`: 同キー集計
- `format` の主要種別: `CH`（文字）, `ZD`（ゾーン 10 進）, `PD`（パック 10 進）, `BI`（バイナリ）, `FS`（固定符号 numeric）
- ICETOOL は別 PGM (`ICETOOL`) を呼び、`TOOLIN` DD で OPERATOR 文を書く

## 3. prerequisites（理解の前提）

- データセットの編成と RECFM — `ZOS-DATASET-001`
- JCL の DD 連結 — `ZOS-JCL-001`
- パック 10 進数 / ゾーン 10 進数の符号桁位置（業務データはほぼ PD/ZD）

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-DATASET-001, ZOS-JCL-001
- `specialized_by`: なし（DFSORT / Syncsort / CA-SORT が axis 内別実装）
- `contrasts_with`: COBOL 内 `SORT` 文（プログラム埋め込み）, USS の `sort(1)`（POSIX）, Db2 SQL の `ORDER BY`（RDB 内ソート）
- `used_by`: ZOS-GDG-001（全世代 concatenation の集計）, ZOS-JCL-001（IEBGENER 代替）, ZOS-SMF-001（SMF dump 集計の前処理）

## 5. pitfalls（実装・運用での落とし穴）

- **SORTWK の DASD 不足で `WER268A` / `ICE055I` ABEND**: ソート対象サイズの **1.5〜2 倍** の SORTWK が必要。「100MB の入力なら 100MB の WK」と勘違いして枯渇するのが典型。`DYNALLOC` で動的確保する場合も、SG プール枯渇で詰む。**初手チューニングは SORTWK 容量見直し**。
- **`SORT FIELDS=COPY` を知らずに COBOL を書く**: 「ソートはしないがレコード再構成だけしたい」時、`SORT FIELDS=COPY,INREC=...` で実装できる。これを知らずに COBOL でループを書く悲劇が現場で多発する。**Copy with reformatting は DFSORT の十八番**。
- **OUTFIL の SAVE 句忘れで取りこぼし**: 複数 OUTFIL の INCLUDE 条件で **どれにも当たらないレコード** を集めたい時は `OUTFIL FNAMES=...,SAVE`。SAVE を書かないと「どこにも出力されないレコード」が黙って消える。突合チェックでこれを忘れると残高合わない原因。
- **PD（パック 10 進）の符号位置を CH（文字）で SORT してマイナス値が後ろに飛ぶ**: 業務データは PD/ZD でカネ・数量を持つ。これを `CH` でソートすると、符号桁が文字解釈されて **-1 が +999999999 より後ろに来る**。`PD,A` で書く規約を徹底。
- **OUTREC の桁ずれで数字フィールドが整合崩壊**: `OUTREC FIELDS=(1:1,5,7:6,10)` の **コロン左の出力位置** を見落として、後段の COBOL が「7 桁目から金額」と思って読むのに、DFSORT 出力は 6 桁目から始まっている、というずれ。**INREC/OUTREC は 1 列目から手動で position マップを書く** が安全。
- **DFSORT と Syncsort で制御文の方言差**: 多くは共通だが `SUBSET`, `JOINKEYS`（DFSORT 独自）等は方言差あり。**ベンダーロックインの自覚なく `JOINKEYS` を多用** すると、Syncsort 移行時に書き直し。**「これは標準か方言か」を意識** する。
- **`SORTOUT` を `DISP=MOD` で書いて旧データが混ざる**: 中間ファイル運用で `MOD` を選ぶと前回残骸が頭に残る。**SORTOUT は `DISP=(NEW,CATLG,DELETE)`** が原則、`MOD` は意図のある時だけ。

## 6. examples（具体例）

```jcl
//* シンプル ソート: 1 桁目から 10 バイト文字キー昇順
//SORT EXEC PGM=SORT
//SORTIN   DD DSN=USER.PROD.IN,DISP=SHR
//SORTOUT  DD DSN=USER.PROD.OUT,DISP=(NEW,CATLG,DELETE),
//            SPACE=(CYL,(10,5))
//SYSOUT   DD SYSOUT=*
//SYSIN    DD *
  SORT FIELDS=(1,10,CH,A)
  INCLUDE COND=(11,2,CH,EQ,C'JP')
/*
```

```jcl
//* 条件別 3 出力に振り分け + 集計
//SORT EXEC PGM=SORT
//SORTIN   DD DSN=USER.PROD.SALES,DISP=SHR
//OUT01    DD DSN=USER.PROD.JP,DISP=(NEW,CATLG,DELETE),SPACE=(CYL,(5,1))
//OUT02    DD DSN=USER.PROD.US,DISP=(NEW,CATLG,DELETE),SPACE=(CYL,(5,1))
//OUT03    DD DSN=USER.PROD.OTHERS,DISP=(NEW,CATLG,DELETE),SPACE=(CYL,(5,1))
//SYSOUT   DD SYSOUT=*
//SYSIN    DD *
  SORT FIELDS=(1,10,CH,A)
  OUTFIL FNAMES=OUT01,INCLUDE=(11,2,CH,EQ,C'JP')
  OUTFIL FNAMES=OUT02,INCLUDE=(11,2,CH,EQ,C'US')
  OUTFIL FNAMES=OUT03,SAVE
/*
```

```jcl
//* ICETOOL でユニークカウント + 範囲統計
//TOOL EXEC PGM=ICETOOL
//IN       DD DSN=USER.PROD.SALES,DISP=SHR
//SYSOUT   DD SYSOUT=*
//TOOLMSG  DD SYSOUT=*
//DFSMSG   DD SYSOUT=*
//TOOLIN   DD *
  COUNT FROM(IN) ON(1,10,CH)
  STATS FROM(IN) ON(21,8,PD)
/*
```

## 7. decision_axes（採否を分ける判断軸）

- **DFSORT vs Syncsort vs CA-SORT**: 機能差は小さいが、ライセンス費用 + 方言差で揉める。**新規サイトは DFSORT（IBM 標準同梱）** が無難。Syncsort は性能で有利な局面があるが、独自構文に依存すると将来移行コスト発生。CA-SORT は資産継承サイトでのみ。
- **DFSORT 単体 vs ICETOOL**: 単純ソート / マージは DFSORT 直、複数 OPERATOR をパイプ的に組むなら ICETOOL。**ICETOOL は中間 SORTOUT を持たずに済む** ので大規模集計で有利。だが学習コスト高め。
- **DFSORT vs COBOL 内 SORT 文**: COBOL の SORT 文は内部で DFSORT を呼ぶが、INREC/OUTREC 等の柔軟性が落ち、再利用性も低い。**集計だけなら DFSORT/ICETOOL、業務ロジック絡みなら COBOL**。
- **DFSORT vs Db2 SQL の ORDER BY**: Db2 表上のデータは SQL の `ORDER BY` + `INSERT INTO` で済む。順次データセット相手なら DFSORT が圧倒的に速い（チャネル直結）。**データの居場所で選ぶ**。
- **DASD SORTWK vs dataspace (DSPSIZE)**: 中規模ソート（数 GB 程度）はメモリ dataspace の方が速い。それ以上は DASD SORTWK に逃がす。`DSPSIZE=MAX` 指定で DFSORT が自動判断する設定が現代の標準。
- **OUTFIL 多出力 vs 別 SORT job 連結**: 「同 SORTIN を条件別に複数出力」なら OUTFIL 一発。「全く違うキーで複数出力」なら別ジョブで SORT を 2 回流す。**OUTFIL を多用しすぎる JCL は読解困難になる** ので、論理的に分離が要る場合は別ジョブ化。

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_TECH_002) から DFSORT / ICETOOL 実運用知識を概念蒸留 (ADR-0109)。逐語引用禁止。
