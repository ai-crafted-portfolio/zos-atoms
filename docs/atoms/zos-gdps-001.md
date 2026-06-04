---
id: ZOS-GDPS-001
title: GDPS / PPRC / XRC / HyperSwap
status: draft
last_reviewed: 2026-06-02
authors: [agent-z6]
rag_verified: partially
---

# ZOS-GDPS-001: GDPS / PPRC / XRC / HyperSwap

## 1. purpose

GDPS は DR 自動化フレームワーク、下位の storage mirroring (PPRC = Metro Mirror、XRC = Global Mirror、GM) + HyperSwap (透過 swap) を組合せ、サイト障害から数分〜数秒で復旧。AWS Aurora Global Database や Azure Site Recovery は近いが、RPO=0 同期 + application 透過切替まで届かない。

## 2. mechanism

- PPRC (sync, < 200km, RPO=0) / XRC (async, SDM, RPO 秒) / Global Mirror (async, consistency group, RPO 3-5s)
- HyperSwap: I/O subsystem level の透過切替、UCB swap
- GDPS variants: PPRC / XRC / GM / MGM / Active-Active
- K-system (control LPAR) で GDPS scripts 実行
- Consistency Group (CGROUP) で複数 pair freeze

## 3. prerequisites

- ZOS-DASD-001
- ZOS-PARALLELSYSPLEX-001
- ZOS-RECOVERY-001

## 4. relations

- `depends_on`: ZOS-DASD-001, ZOS-PARALLELSYSPLEX-001, ZOS-RECOVERY-001
- `specialized_by`: なし
- `contrasts_with`: Linux DRBD remote, AWS Aurora Global Database, Azure Site Recovery, VMware SRM
- `used_by`: ZOS-DB2-001, ZOS-CICS-001, ZOS-HSM-001, ZOS-XCF-001 (CDS DR)

## 5. pitfalls

- **HyperSwap policy mismatch** → 追加 LPAR 設定漏れで swap 後データ不整合
- **Metro vs Global RPO 認識違い** → RPO=0 と RPO≈5s の業務影響理解不足
- **GDPS script test 不足** → 本番初動作で想定外、復旧 6h
- **PPRC 同期失敗手動切替手順未整備** → freeze 状態で運用者フリーズ

## 6. examples

```
PPRCOPY ESTPAIR MODE(COPY) SOURCE(X'1234') TARGET(X'5678') CRIT(YES)
ANTRQST QUERY,LOCATE(1234),DEV(1234),TYPE=PRIM
SETHS PLANSWAP,SITE=2
D HS
F GDPSPROC,DISPLAY,HS
```

## 7. decision_axes

- **variant 選定**: 業務 RPO/RTO + 距離 + コストの 3 軸
- **HyperSwap 自動 vs 手動**: PPRC 自動 / XRC,GM 手動
- **CRIT=YES vs NO**: 決済 YES / 参照 NO、CGROUP で局所最適化

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_TECH_002) から GDPS 災害対策設計の運用知識を概念蒸留 (ADR-0109)。書籍は概念補助。
