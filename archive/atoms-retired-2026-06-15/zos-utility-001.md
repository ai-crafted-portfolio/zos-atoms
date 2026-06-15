---
id: ZOS-UTILITY-001
title: z/OS Utilities (IEBGENER / IEBCOPY / IDCAMS / IEFBR14 / IEHLIST / ICEGENER)
status: stable
last_reviewed: 2026-06-04
authors: [agent]
rag_verified: partially
---

# ZOS-UTILITY-001: z/OS Utilities 全体俯瞰

## 1. purpose（なぜ存在するか）

z/OS には **OS 添付 / プログラムプロダクト系の utility プログラム群** が存在し、JCL の `EXEC PGM=xxx` で呼び出して **dataset コピー / 編集 / 一覧 / VTOC 参照 / dummy step / VSAM 操作** 等の基本 I/O 業務を実行する。これらは Linux で言えば `cp`, `cat`, `ls`, `dd`, `mkfs`, `true` に相当するが、**JCL の DD カードと utility 制御文 (SYSIN) を組み合わせる** 点が独特である。

本アトムは「**どの utility をいつ使うか**」 を俯瞰する **目次アトム** であり、個別 utility の詳細は per-utility アトム (`zos-idcams-001` / `zos-iebcopy-001` / `zos-iefbr14-001` 等) に分割されている。本アトムは utility 選択判断と全体地図を提供する。

なお、`SORT` (DFSORT / SYNCSORT) は独立した重要度のため `zos-sort-001` で別建て。

## 2. mechanism（どう動くか）

### 主要 utility と用途

| Utility | 用途 | 入出力 | 制御文 |
|---|---|---|---|
| IEBGENER | sequential dataset コピー / 単純編集 | SYSUT1 → SYSUT2 | SYSIN (GENERATE / RECORD) |
| ICEGENER | DFSORT 系の高速 IEBGENER 代替 | SYSUT1 → SYSUT2 | SYSIN (DFSORT 構文) |
| IEBCOPY | PDS / PDSE メンバコピー / 圧縮 / unload | SYSUT1 / SYSUT2 / SYSUT3 / SYSUT4 | SYSIN (COPY / SELECT / EXCLUDE) |
| IEBPTPCH | dataset 印刷 / パンチ (歴史的) | SYSUT1 → SYSUT2 | SYSIN (PRINT / PUNCH) |
| IEBUPDTE | source library 更新 | SYSUT1 / SYSUT2 / SYSIN | ./ ADD ./ DELETE 等 |
| IEBEDIT | JCL stream の選択編集 | SYSUT1 → SYSUT2 | EDIT START= |
| IEHLIST | VTOC / catalog / PDS directory 一覧 | DD0001 / SYSIN | LISTVTOC / LISTPDS / LISTCTLG |
| IEHPROGM | dataset rename / delete / SCRATCH / UNCATALOG | DD0001 / SYSIN | SCRATCH / RENAME / UNCATLG |
| IDCAMS | Access Method Services (VSAM 中核 + non-VSAM 一部) | 各種 | DEFINE / REPRO / LISTCAT / DELETE / PRINT / VERIFY |
| IEFBR14 | 何もしない (dataset 作成/削除のみ目的) | なし | なし (BR 14 で即 RC=0) |
| IEBDG | テストデータ生成 | DD / SYSIN | DSD / FD / CREATE |
| IEHINITT | tape volume initialize | DD / SYSIN | INITT |
| IEHMOVE | dataset / volume の move (古い、現在は DFDSS / IDCAMS 推奨) | 各種 | MOVE / COPY |

### 採用優先順 (現代の z/OS V2.x)

1. **IDCAMS** — VSAM 全般、catalog 操作、cross-system copy (REPRO)、cluster 定義の中核
2. **IEBCOPY** — PDS/PDSE のメンバ単位コピー + library 圧縮 (PDS のみ)、unload (transport format)
3. **IEBGENER / ICEGENER** — sequential ファイルの簡易コピー、ICEGENER は DFSORT が使えれば自動 substitute
4. **IEFBR14** — JCL DD で `DISP=(NEW,CATLG,DELETE)` のみで dataset 確保 / 削除する step
5. **IEHLIST** — VTOC / catalog / PDS directory 直接照会 (運用時の確認)
6. **DFSMSdss (ADRDSSU)** — IEHMOVE / IEHPROGM の後継、大量 dataset 移送 / DUMP / RESTORE
7. **DFSMShsm (FSR, ARC)** — 階層管理 (migration / backup / recall)、`zos-hsm-001` 参照

### IEBGENER vs ICEGENER の自動 substitute

- ICEGENER は DFSORT load module の alias で、IEBGENER と同名 entry を持つ
- JCLLIB / STEPLIB に DFSORT (`SYS1.SICELINK` 等) が並んでれば、`EXEC PGM=IEBGENER` でも **ICEGENER が起動 → DFSORT で高速処理**
- 制御文形式は SORT 構文 (`SORT FIELDS=COPY` 等) と IEBGENER の `GENERATE MAXNAME=N` の両方を受け付ける

### IEFBR14 の典型用法

```jcl
//ALLOC   EXEC PGM=IEFBR14
//NEWDD   DD  DSN=USER01.NEWFILE,
//             DISP=(NEW,CATLG,DELETE),
//             SPACE=(TRK,(10,5)),DCB=(RECFM=FB,LRECL=80,BLKSIZE=0)
```
- PGM=IEFBR14 は `BR 14`(分岐レジスタ 14 = 復帰) 1 命令だけのモジュール
- 実際の作業 (= dataset 確保/削除) は **JCL の DD 解析**側で起こり、step 自体は何もしない
- 結果として「dataset の確保専用 step」「dataset 削除専用 step」 に使う

### IEHLIST と LISTCAT の使い分け

- IEHLIST LISTVTOC: 「**VOLSER 単位**でその volume にある dataset 一覧」 (VTOC 読取)
- IDCAMS LISTCAT: 「**catalog 単位**で entry を列挙」、特に VSAM cluster / GDG / alias 等は catalog 経由
- 運用では「VOLSER に何が乗ってるか」 を即知るには IEHLIST、「dataset の catalog 状態」 を知るには LISTCAT

## 3. prerequisites

- ZOS-JCL-001 (JCL DD カード / 制御文 SYSIN)
- ZOS-DATASET-001 (sequential / PDS / PDSE / VSAM の概念)
- ZOS-CATALOG-001 (catalog 階層)
- ZOS-PDS-001 (PDS/PDSE 構造、IEBCOPY 操作対象)
- ZOS-VSAM-001 (IDCAMS の DEFINE CLUSTER 等の対象)

## 4. relations

- `depends_on`: ZOS-JCL-001, ZOS-DATASET-001, ZOS-CATALOG-001
- `specialized_by`: ZOS-IDCAMS-001, ZOS-IEBCOPY-001, ZOS-IEFBR14-001
- `contrasts_with`: Linux coreutils (cp/cat/dd/true), DFDSS (ADRDSSU), DFSMShsm
- `used_by`:
  - 99% の batch JCL (= 何らかの dataset 操作 step を持つ)
  - ZOS-GDG-001 (GDS allocation / catalog 操作)
  - ZOS-HSM-001 (migrate/recall trigger は IDCAMS or HSM command)
  - ZOS-SMS-001 (DATACLAS/STORCLAS が utility 出力に適用)

## 5. constraints

- utility 制御文 (SYSIN) は **column 2-71 で記述**、column 1 は continuation marker (`-` or `*`)
- IEBCOPY は **PDSE 圧縮不要** (= PDSE は自動 reuse)、PDS のみ compress 必要
- IEBGENER の SYSUT1 / SYSUT2 は **DCB attribute が両立可能** である必要 (RECFM/LRECL 互換)
- IDCAMS REPRO は VSAM↔ VSAM, VSAM↔sequential 等 cross 可能、ただし record length 整合が必要
- IEHMOVE は **deprecated**、新規設計では DFDSS / IDCAMS を選択
- IEFBR14 step の DD で `DISP=(NEW,DELETE,DELETE)` だと step 終了時 (=即時) に削除される

## 6. examples

具体例は `examples.md` を参照。代表的なものは:

- IEBGENER で sequential file コピー + member 単位 unload
- IEBCOPY で PDS から PDSE へ migrate + 圧縮
- IDCAMS で VSAM KSDS 定義 + REPRO ロード + LISTCAT 確認
- IEFBR14 で dataset 削除専用 step
- IEHLIST LISTVTOC で VOLSER 一覧

## 7. pitfalls

詳細は `pitfalls/` 配下。代表:

- IEBGENER の DCB 不整合で S013 / SE37 ABEND
- IEBCOPY 圧縮 (PDS) の SYSUT3/SYSUT4 work file 不足で SE37
- IDCAMS DELETE の SCRATCH option 漏れで catalog entry だけ消えて DASD に残骸
- IEFBR14 で DD が syntactically 失敗してても PGM=IEFBR14 は RC=0 で返す (= DD error 見逃し)
- ICEGENER の DFSORT version 差で control statement 文法解釈差

## 8. references

参考文献は `references.md` を参照 (IBM Docs / Redbooks / 市販書籍)。


## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

本 atom の領域については、IBM 公式 manual を一次出典としつつ、運用事例や設計判断の補強として市販書籍 (BK_MF_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 等の z/OS / メインフレーム関連書籍) からの実装知識を補助的に参照する。逐語引用は禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
