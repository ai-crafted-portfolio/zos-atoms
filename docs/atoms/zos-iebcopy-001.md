---
title: ZOS-IEBCOPY-001
description: COPY / COPYMOD / UNLOAD / LOAD、PDS → PDSE 移行、Selected members
tags:
  - Utility
  - Middleware-Utility
---
# ZOS-IEBCOPY-001: IEBCOPY + PDS/PDSE 操作 utility

## 1. purpose（なぜ存在するか）

IEBCOPY は **PDS / PDSE の copy / merge / compress / unload / load** を担当するz/OS utility。COPY は member 単位、COPYMOD は load module 専用 (re-link 含む)、UNLOAD は PDS の中身を sequential file 化 (DASD → tape backup)、LOAD は逆方向。PDS の慢性課題「内部 fragmentation」「directory block 不足」を扱う日常運用 utility。

Linux の `tar` + `cp -R` + `find ... -exec` + `objcopy` を 1 つにしたような立ち位置。Windows の `xcopy` / `robocopy` は普通の file copy だが、IEBCOPY は **load module のalias / authcode / amode / rmode 等の属性を保持** しながら copy できる点が独自。

## 2. mechanism（どう動くか）

- **COPY**: 同一 / 別 PDS への member copy。`SELECT MEMBER=` / `EXCLUDE MEMBER=`
  で対象絞り込み。alias は **自動追跡** (主 member を copy すれば alias も従う)
- **COPYMOD**: load module を re-link しながら copy。RMODE / AMODE 変更、  authcode 変更、reblock を伴う。load lib 専用
- **UNLOAD**: PDS → sequential (`OUTDD DD ...`) に member structure を逐次化
- **LOAD**: sequential → PDS に restore
- **COMPRESS**: PDS 内部 fragmentation 解消 (削除 member が残した穴を詰める)。
  PDSE は自動再利用なので不要
- directory block: PDS は CYL 単位 SPACE の (n,m,d) の d で確保。member 増加で  足りなくなると `IEC031I D37` ABEND。COMPRESS では増えない、再 allocate 必要
- アロケート時の RECFM / LRECL / BLKSIZE が source と target で異なると、  COPY が自動 reblock するが、特殊な内部構造 (object module 等) では失敗する

## 3. prerequisites（理解の前提）

- PDS / PDSE の構造 — `ZOS-PDS-001`
- dataset 属性 (RECFM / LRECL / BLKSIZE) — `ZOS-DATASET-001`
- load module の概念 (link-edit / binder)
- JCL の DD と DCB 上書き — `ZOS-JCL-001`

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-PDS-001, ZOS-DATASET-001, ZOS-JCL-001
- `specialized_by`: なし
- `contrasts_with`: Linux tar + cp -R + objcopy, Windows xcopy / robocopy
- `used_by`: ZOS-PDS-001 (運用), ZOS-RECOVERY-001 (UNLOAD/LOAD 経由 backup)

## 5. pitfalls（実装・運用での落とし穴）

- **COPY で directory block 不足で D37 ABEND**: target PDS の directory block (DSCB に格納された値) が足りないと、member 追加時 `IEC031I D37-04` ABEND。SPACE で `(CYL,(10,5,30))` の 30 がdirectory block 数だが、増やすには再 allocate + REPRO しかない。PDS は **directory block を allocate 後に増やせない** という設計制約のため、site 規約で「PDS は廃止、PDSE のみ新規」が増えている。
- **COPYMOD で alias が失われる**: load module の alias を持つ PDS を COPY なら alias 追従するが、**COPYMOD で RMODE/AMODE 変更などしながら copy すると alias が落ちる** 事例。target PDS で main entry name のみ残り、application がalias 経由で参照していたものが `8068` ABEND (module not found)。COPYMOD 前後に `LIST DSN=... MEMBER=...` で alias 一覧を出力して diffを取るのが site SOP として強い。
- **UNLOAD / LOAD round trip で alias / SSI 失われる**: PDS を UNLOAD → tape → LOAD で復元すると、PDS 一般 record は復元されるが、**load module の SSI (System Status Index)** や **alias の一部** が保持されない事例があり、復元後の load module が動かない。load module を含む PDS の backup は IEBCOPY UNLOAD ではなく **DFSMSdss DUMP** か **PDSE 化して DSS COPY** を選ぶのが現代の正解。古い JCL を引き継ぐ時に踏みやすい。
- **PDS → PDSE 移行で utility 非互換が発覚**: PDSE への移行は IEBCOPY COPY で member 単位 copy するだけで一見できるが、(a) IEBUPDTE 等の古い utility は PDSE で誤動作 (b) 一部の COBOL 製application が member 構造を直接読み (c) DDIO 系 ISPF customization がPDS 前提、等で本番影響が出る。PDSE への全面移行前に **utility 棚卸し** と **回帰 test** が必須。
- **COPY の SELECT で部分指定後に alias が残る**: `SELECT MEMBER=((A,A1),(B,B1))` で member とその alias を明示指定したが、後段で `SELECT MEMBER=A` だけにすると **alias A1 が target に残ったまま**になり、source の master が消えてるのに alias だけが target に居る矛盾。site 規約として `SELECT` 後の target で `LIST MEMBER=*` を必ず走らせて整合性確認するルーチンが必要。

## 6. examples（具体例）

```jcl
//* PDS → PDS の全 member copy
//STEP1    EXEC PGM=IEBCOPY
//SYSPRINT DD SYSOUT=*
//IN       DD DSN=USER.PROD.PROCLIB,DISP=SHR
//OUT      DD DSN=USER.PROD.PROCLIB.BAK,DISP=SHR
//SYSIN    DD *
  COPY OUTDD=OUT,INDD=IN
/*
```

```jcl
//* load module を RMODE=ANY,AMODE=31 で re-link しながら copy
//STEP1    EXEC PGM=IEBCOPY
//SYSPRINT DD SYSOUT=*
//IN       DD DSN=USER.PROD.LOADLIB,DISP=SHR
//OUT      DD DSN=USER.PROD.LOADLIB.NEW,DISP=SHR
//SYSIN    DD *
  COPYMOD OUTDD=OUT,INDD=IN
  SELECT MEMBER=((PROG1),(PROG2))
/*
```

```jcl
//* PDS の compress (in-place)
//STEP1    EXEC PGM=IEBCOPY
//SYSPRINT DD SYSOUT=*
//SYSUT1   DD DSN=USER.PROD.PROCLIB,DISP=OLD
//SYSUT2   DD DSN=USER.PROD.PROCLIB,DISP=OLD
//SYSIN    DD *
  COPY OUTDD=SYSUT2,INDD=SYSUT1
/*
```

## 7. decision_axes（採否を分ける判断軸）

- **PDS COMPRESS スケジュール vs PDSE 化**: PDS は member 削除で穴が残るため、月次 COMPRESS が運用 SOP。compress 中は exclusive ENQ で application 利用不可。PDSE は穴を自動回収するため COMPRESS 不要 + 並行更新可。**新規は PDSE 一択**、既存 PDS は (a) utility 互換性確認後 PDSE 化、(b) site policy で PDS 維持なら COMPRESS schedule、の二択。
- **UNLOAD → tape backup vs DFSMSdss DUMP**: IEBCOPY UNLOAD は member 構造を sequential 化するため、target 環境でRECFM/LRECL が違っても LOAD で復元できる柔軟性。DSS DUMP は physical track 単位で速いが target 環境制約 (容量 / 構造) を厳格に要求。**移送先で PDS 属性変えたい時は UNLOAD、純粋 backup なら DSS**。
- **COPY (alias 追跡) vs SELECT 明示**: default `COPY` は alias 自動追跡で安全だが、不要 member まで copy する。`SELECT MEMBER=...` で絞れるが、alias を明示しないと alias が残る/落ちる事故。**全件 backup は default COPY、部分 promote は SELECT で alias 明示**を SOP に。
- **IEBCOPY vs ISPF 3.3 (member copy GUI)**: ISPF 3.3 はインタラクティブで楽だが、(a) 大量 member で操作ミスしやすい (b) audit trail が残らない (c) automation 化不可。**ad-hoc 1-2 member 移送は ISPF、本番 promote は IEBCOPY JCL** を SOP に。site policy で本番 LOADLIB への member copy は JCL のみ許可、ISPF は test環境限定とする site も多い。
