---
id: ZOS-IDCAMS-001
title: IDCAMS (Access Method Services)
status: stable
last_reviewed: 2026-06-02
authors: [Z2]
rag_verified: true
---
# ZOS-IDCAMS-001: IDCAMS (Access Method Services)

## 1. purpose（なぜ存在するか）

IDCAMS は z/OS の **VSAM 操作 + ICF catalog 操作の中核 utility**。VSAM cluster のDEFINE / DELETE、データコピー (REPRO)、整合性検査 (EXAMINE)、catalog entry のREPRO / EXPORT / IMPORT / ALIAS / CONNECT / DELETE が 1 本の utility に集約されている。JCL 上では `//SYSIN DD *` 経由でコマンドを流すバッチ実行が標準。

Linux の `dd` + `mkfs` + ファイルシステム utility 群 + `lvm` 系コマンド + cifs/nfsの mount 管理を 1 つに統合したような立ち位置。Windows の `diskpart` + `format`が物理寄りなのに対し、IDCAMS は **VSAM logical view と catalog (= filesystemmetadata) の両方を 1 本で扱う**。

## 2. mechanism（どう動くか）

- 主要コマンド: **DEFINE** (CLUSTER / GDG / ALIAS / USERCATALOG / PATH /  AIX)、**DELETE** (CLUSTER / GDG / VVR / NVR / NOSCRATCH)、**REPRO**  (copy + load + merge)、**ALTER** (属性変更)、**LISTCAT** (entry 一覧 + 詳細)、  **PRINT** (内容 dump)、**EXAMINE** (整合性検査)、**EXPORT/IMPORT** (catalog  entry の搬出入)、**DIAGNOSE** (catalog 内部整合性検査)
- 戻り値: コマンドごとに condition code (0 / 4 / 8 / 12 / 16) を返し、`SET  MAXCC` / `SET LASTCC` で制御可。step の RC は最大値
- メッセージ: `IDCxxxxA/I/E` 系。例: `IDC3009I VSAM CATALOG RETURN CODE IS 8` ←
  catalog 操作で何らかの問題発生
- VSAM 操作の input/output: `INDATASET` / `OUTDATASET` か DD 参照 `INFILE` /
  `OUTFILE`。DD 参照は JCL の DCB 上書きが効くので柔軟だが trouble の源
- DELETE NOSCRATCH: catalog entry のみ削除し、VTOC からは消さない (孤児化)

## 3. prerequisites（理解の前提）

- VSAM (KSDS / ESDS / RRDS / LDS) の構造 — `ZOS-VSAM-001`
- ICF catalog (master / user) — `ZOS-CATALOG-001`
- dataset attribute (DSORG / RECFM / SPACE 等) — `ZOS-DATASET-001`
- JCL の `//SYSIN DD *` 経由 utility 起動 — `ZOS-JCL-001`

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-VSAM-001, ZOS-CATALOG-001, ZOS-DATASET-001, ZOS-JCL-001
- `specialized_by`: なし
- `contrasts_with`: Linux dd + mkfs + lvm, Windows diskpart + format
- `used_by`: ZOS-VSAM-001 (構築・運用本流), ZOS-CATALOG-001 (運用),
  ZOS-GDG-001 (GDG base 定義), ZOS-DB2-001 (image copy)

## 5. pitfalls（実装・運用での落とし穴）

- **DELETE NOSCRATCH と DELETE FORCE の混乱**: `DELETE 'XXX' NOSCRATCH` は **catalog entry だけ消して VTOC を残す**。意図せず使うと dataset が VTOC 上残骸として永久に居座り、容量だけ食う。逆に `DELETE 'XXX' FORCE` は profile 等を無視して破壊的に削除する強制経路。両方混同すると「消したつもりが残ってる」「残したかったのに消えた」の二重事故。site 規約で NOSCRATCH と FORCE は profile 担当者 root reviewを要する change で扱う。
- **REPRO 上書きで旧 alias / AIX 関係が壊れる**: 既存 KSDS に `REPRO ... REPLACE` で別 cluster の内容を流し込むと、**target cluster に紐付いていた AIX / PATH の参照は古いまま** で、key 順序が変わった瞬間に index 再構築が必要。BLDINDEX し忘れてAIX 経由のアクセスが壊れる事例。target の AIX / PATH の有無を事前 LISTCAT で確認するルーチンを REPRO の前段に必ず入れる。
- **DEFINE の RECATALOG 連鎖で SMS と非 SMS が分裂**: `DEFINE CLUSTER ... RECATALOG` は VVDS から read した属性で catalog 再登録する。だが SMS 化されていた cluster を非 SMS 環境で RECATALOG すると、DATACLAS / STORCLAS / MGMTCLAS の参照が空になり、後続の VOL=SER= 指定が必須化される。DR site への移送で典型的な落とし穴。DR test で必ず再現確認、`LISTCAT ALL` で DATACLAS 行を見る。
- **PRINT が代替 index (AIX) を含めず entire と誤解**: `PRINT INDATASET('xxx.KSDS')` は KSDS の本体のみ出力し、AIX 経由レコードは別ジョブで PRINT する必要がある。audit log として KSDS 本体だけ取って「全件 dump 取った」と報告するインシデント。AIX が存在する cluster は LISTCAT で AIX 一覧を取って各 AIX に対するPRINT も流す script を運用標準にする。
- **EXAMINE で OPEN error 発生時の I/O 損傷誤判定**: `EXAMINE NAME('xxx.KSDS') INDEXTEST DATATEST` で整合性検査するが、対象 cluster が他 job で OPEN されてると `IDC11707I` (open failure) を「破損あり」と誤読する運用がある。実際は単に in-use。EXAMINE は scheduled maintenance window で他 job が CLOSE した状態で実行することを SOP に明記。GRS で SYSDSN ENQ を取りに行く設計。

## 6. examples（具体例）

```jcl
//STEP1    EXEC PGM=IDCAMS
//SYSPRINT DD SYSOUT=*
//SYSIN    DD *
  DEFINE CLUSTER                          -
    (NAME(USER.PROD.MASTER)               -
     INDEXED                              -
     KEYS(12 0)                           -
     RECORDSIZE(200 400)                  -
     CYLINDERS(50 10)                     -
     VOLUMES(*)                           -
     SHAREOPTIONS(2 3))                   -
    DATA  (NAME(USER.PROD.MASTER.DATA)    -
           CISZ(8192))                    -
    INDEX (NAME(USER.PROD.MASTER.INDEX))
/*
```

```jcl
//STEP2    EXEC PGM=IDCAMS
//OLD      DD DSN=USER.PROD.MASTER.OLD,DISP=SHR
//NEW      DD DSN=USER.PROD.MASTER,DISP=SHR
//SYSPRINT DD SYSOUT=*
//SYSIN    DD *
  REPRO INFILE(OLD) OUTFILE(NEW) REPLACE
/*
```

```jcl
//* catalog 一覧 + 整合性検査
//SYSIN DD *
  LISTCAT ENTRIES(USER.PROD.MASTER) ALL
  EXAMINE NAME(USER.PROD.MASTER) INDEXTEST DATATEST
/*
```

## 7. decision_axes（採否を分ける判断軸）

- **REPRO によるコピー vs DFSMSdss DUMP/RESTORE**: REPRO は **logical copy** (record 単位)、cluster 構造を新規 target に整え直すため壊れた CI 構造の修復も兼ねる。だが大規模 dataset (1TB+) ではCPU + 時間がかかる。DSS は **physical copy** (track 単位) で速いが、壊れた構造をそのまま転写するので修復にならない。**整合性修復目的なら REPRO**、**バックアップ / DR 移送なら DSS** が定石。
- **DEFINE で属性明示 vs MODEL 継承**: `DEFINE CLUSTER ... MODEL('xxx.MODEL')` で既存 cluster の属性を継承コピーできる。テンプレ化で運用工数低いが、MODEL 側の属性変更が新規 clusterに伝播するため、本番 dataset の属性が黙って変わる事故。属性明示は冗長だが意図が JCL に残る。site 規約で MODEL 使用は標準 datasetに限定、ad-hoc 案件は属性明示、と分けるのが安全。
- **AIX (代替インデックス) を作る vs application 側でキー変換**: AIX を作ると主キー以外でも VSAM の高速 lookup が使えるが、(a) BLDINDEX 維持コスト (b) 主 cluster 更新時 AIX 同期 (UPGRADE オプション)(c) 障害時 AIX 単独損傷で application 全面停止リスク、がある。application 側で別 dataset (cross-reference) を持ち、batch 同期する方が障害局所化しやすい site もある。lookup 頻度と一貫性要件で判断。
- **LISTCAT 全件 ALL vs NAMES のみ**: `LISTCAT ALL` は dataset 単位で全属性を出すため大規模 catalog で出力 GB 級になる。`LISTCAT NAMES` は entry 名と type のみで軽い。棚卸し用は NAMES、詳細調査は ALL を target 限定で実行、の使い分け。ALL を月次で全 catalog にかける運用は SMF 大量出力で監視に悪影響。

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_TECH_002) から IDCAMS 運用パターンを概念蒸留 (ADR-0109)。書籍は概念補助。
