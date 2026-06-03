---
title: ZOS-GRS-001
description: ENQ/DEQ、RNL (Resource Name List)、GRS star vs ring、SYSTEMS/SYSTEM/STEP scope
tags:
  - Sysplex
  - Sysplex-Modernization
---
# ZOS-GRS-001: GRS (Global Resource Serialization)

## 1. purpose

GRS は Sysplex 全 LPAR で dataset / dataset member / 任意リソース名の **排他制御 (ENQ / DEQ)** を同期する OS 基盤。Linux flock や Redis distributed lock とは異なり、データセット名前空間が Sysplex 全体で 1 つというモデル前提、CF lock structure 経由 < 100 μs で完結する。

## 2. mechanism

- ENQ scope 3 種: STEP / SYSTEM / SYSTEMS
- GRS Star (CF ISGLOCK 構造、3-32 LPAR スケール) vs Ring (legacy、4 LPAR 限界)
- RNL: SYSTEM Inclusion / SYSTEMS Exclusion / RESERVE Conversion
- 既定: SYSDSN, SYSIEFSD, SYSZRACF などは SYSTEMS scope

## 3. prerequisites

- ZOS-PARALLELSYSPLEX-001
- ZOS-CF-001
- ZOS-DATASET-001

## 4. relations

- `depends_on`: ZOS-PARALLELSYSPLEX-001, ZOS-CF-001
- `specialized_by`: なし
- `contrasts_with`: Linux flock + lockd, Redis distributed lock, ZooKeeper
- `used_by`: ZOS-DATASET-001, ZOS-CATALOG-001, ZOS-RACF-001, ZOS-JCL-001

## 5. pitfalls

- **RNL で意図しない resource を local 化** → 両 LPAR 同時 update で catalog 不整合
- **Ring → Star 移行で ISGLOCK 未定義** → IPL disabled wait 0A2
- **Long-lived ENQ で contention** → DISP=OLD で巨大 dataset 抑え続け後続全直列化
- **SYSDSN ENQ で batch hang** → 複数 dataset 逆順 allocate で deadlock

## 6. examples

```
D GRS,CONTENTION
D GRS,RES=(SYSDSN,USER.PROD.DATA)
D GRS,ANALYZE,DEPENDENCY
SETGRS PURGE,JOBNAME=JOBLONG,ASID=003F
```

```
GRS=STAR
GRSCNF=00
```

## 7. decision_axes

- **Star vs Ring**: 新規構築は Star 一択
- **RNL 戦略**: 既定 + 自社 QNAME prefix ハイブリッド
- **RESERVE 残存 vs 変換**: 現代標準は全変換
