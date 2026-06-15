---
id: ZOS-XCF-001
title: XCF (Cross-System Coupling Facility) + JES2/JES3 spool
status: draft
last_reviewed: 2026-06-02
authors: [agent-z6]
rag_verified: partially
---

# ZOS-XCF-001: XCF (Cross-System Coupling Facility) + JES2/JES3 spool

## 1. purpose

XCF は Sysplex 内 LPAR 間の **メッセージング + heartbeat + member 状態管理** を担うインフラ。CF が「データ + lock 共有」、XCF は「プロセス間制御 + clustering sentinel」と役割分担。Kubernetes etcd + corosync が近いが、OS kernel 層 + CF list/signaling structure で動く点で別物。

## 2. mechanism

- Group / Member, IXCJOIN/IXCQUIT/IXCDEL
- Signaling path: CF list structure 経由 (推奨) or CTC、4-8 path 冗長
- Couple Dataset (sysplex CDS, CFRM CDS, SFM CDS, WLM CDS) + primary/alternate 2 本
- JES2 MAS: spool 共有、CKPT1 (CF) + CKPT2 (DASD or CF)
- JES3 は z/OS V2.4 でサポート終了、現代は JES2 一択

## 3. prerequisites

- ZOS-PARALLELSYSPLEX-001
- ZOS-CF-001
- ZOS-JCL-001

## 4. relations

- `depends_on`: ZOS-PARALLELSYSPLEX-001, ZOS-CF-001
- `specialized_by`: なし
- `contrasts_with`: Kubernetes etcd cluster, Linux corosync, Apache ZooKeeper
- `used_by`: ZOS-JCL-001 (JES2 MAS), ZOS-DB2-001, ZOS-CICS-001, ZOS-IMS-001, ZOS-OPERLOG-001, ZOS-ARM-001

## 5. pitfalls

- **signaling path 偏り** → CF MAINT で全 path degrade → member SS missing
- **JES2 MAS checkpoint 不整合** → CKPT lock 残置で MAS 全 submit 停止
- **spool full** → 1 LPAR 暴走で MAS 全 batch 停止
- **sysplex partitioning 誤判定** → 健全 LPAR が SFM isolation で system reset

## 6. examples

```
D XCF,SYSPLEX
D XCF,GROUP,DSNDB0G
D XCF,PI
D XCF,STR,STRNAME=IXC_DEFAULT_1
$D CKPTDEF
$D MEMBER,DETAIL
SETXCF START,PATHIN,STRNAME=IXC_HIGH_VOL
```

## 7. decision_axes

- **CF list vs CTC signaling**: ハイブリッド推奨
- **JES2 MAS vs 別 spool**: 本番 MAS 一択、開発別 spool 現実的
- **SFM INTERVAL/OPNOTIFY bias**: 本番 INTERVAL=80 程度

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_TECH_001) から XCF / XES 通信設計を概念蒸留 (ADR-0109)。逐語引用禁止。
