---
title: ZOS-CF-001
description: cache / list / lock 構造、CFLEVEL、CF link、CFRM ポリシー、SCM-augmented
tags:
  - Sysplex
  - Sysplex-Modernization
---
# ZOS-CF-001: Coupling Facility (CF) 構造詳細

## 1. purpose（なぜ存在するか）

**Coupling Facility (CF)** は Parallel Sysplex の **データ共有 + ロック調停 + イベント通知** を担う専用ハードウェア / 専用 LPAR。Sysplex 全体で「**サブ-ミリ秒オーダで複数 LPAR が同じデータを並行更新**」を実現するための物理層であり、ZOS-PARALLELSYSPLEX-001 が抽象論を扱うのに対し、本アトムは **CF 構造の種類 (cache / list / lock) と CFRM policy の運用** という構造詳細を扱う。

なぜ専用 HW が必要か:
1. **TCP/IP ベースの分散ロックでは遅延が桁違い** (CF link 4-10 μs vs IP-based 100 μs-ms)
2. **CF 自身が複数 LPAR 共有の信頼境界**。1 LPAR が hang しても CF 上の lock 状態は正常維持
3. **CFLEVEL** という独立 microcode 階層で構造機能を進化させる

**他プラットフォーム対比**: AWS DynamoDB Streams や Redis Cluster は分散合意プロトコル + IP で似た領域を狙うがレイテンシ・整合性モデルともに別物。Linux DRBD + Pacemaker は HA レプリケーション止まり。

## 2. mechanism（どう動くか）

- **Cache Structure**: Db2 GBP、RACF database cache
- **List Structure**: Logger logstream、MQ Shared Queue、XCF signaling
- **Lock Structure**: IRLM、GRS Star
- **CFRM policy**: IXCMIAPU で CDS 書込み、SETXCF で activate、PREFLIST / REBUILDPERCENT / DUPLEX
- **CF link**: CIB / ICA-SR / CE LR、4-link 並列冗長が一般
- **CFLEVEL**: 22 (z14), 23 (z15), 24 (z16)
- **SCM-augmented**: z14+ で容量 30x

## 3. prerequisites（理解の前提）

- ZOS-PARALLELSYSPLEX-001
- ZOS-WLM-001
- 分散 lock、cache coherence

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-PARALLELSYSPLEX-001
- `specialized_by`: なし
- `contrasts_with`: Linux DRBD + Pacemaker, AWS DynamoDB Streams, Redis Cluster
- `used_by`: ZOS-DB2-001, ZOS-IMS-001, ZOS-XCF-001, ZOS-GRS-001, ZOS-OPERLOG-001

## 5. pitfalls（実装・運用での落とし穴）

- **CFRM ポリシー activate 失敗で構造取り残し** → IXC511I + 灰色状態 → Db2/IRLM 起動不可
- **CF link MAINT で性能 SLA 違反** → 残 link 負荷集中 → IXL040E、OLTP TPS 30% 落ち
- **Structure full → rebuild 連鎖** → ALLOWAUTOALT 抜けで full → rebuild ループ
- **CFLEVEL upgrade で client compat 漏れ** → Db2/IMS バージョン混在で connector reject

## 6. examples（具体例）

```
//CFRMUPD  EXEC PGM=IXCMIAPU
   DATA TYPE(CFRM) REPORT(YES)
   DEFINE POLICY NAME(PROD2026Q2) REPLACE(YES)
     STRUCTURE NAME(DSNDB0G_GBP0)
        INITSIZE(512000)
        SIZE(1024000)
        PREFLIST(CF01,CF02)
        DUPLEX(ENABLED)
        REBUILDPERCENT(1)
```

`SETXCF START,POLICY,TYPE=CFRM,POLNAME=PROD2026Q2`
`SETXCF START,REBUILD,CFNAME=CF01,LOCATION=OTHER`

## 7. decision_axes（採否を分ける判断軸）

- **Stand-Alone CF vs ICF**: 性能 vs コスト、本番 OLTP は Stand-Alone 2 台 + DR ICF
- **Duplex vs Simplex**: 5-10% overhead vs 100ms failover、Lock は Duplex / Db2 GBP は SCM + Simplex モダン
- **SCM-augmented vs in-memory**: warm/cold data の hit ratio 向上 vs DRAM の 10-100x latency、hot lock は in-memory
