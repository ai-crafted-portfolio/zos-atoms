---
id: ZOS-ZOSMF-001
title: z/OSMF (REST + workflow)
status: draft
last_reviewed: 2026-06-02
authors: [agent-z6]
rag_verified: partially
---

# ZOS-ZOSMF-001: z/OSMF (REST + workflow)

## 1. purpose

z/OSMF は z/OS 操作の REST API + Web UI + workflow 基盤、3270 経路に依存しない modern API surface。Ansible / Jenkins / Zowe CLI から z/OS を制御、若手参入の入り口にも。AWS console API / Kubernetes API server が近いが、SAF + z/OS native 認証で独自構成。

## 2. mechanism

- IZUSVR1 (Liberty for z/OS ベース Started Task)、TCP/IP 443 で待受
- REST API: /zosmf/restxxx/yyy、Basic Auth or JWT or API key
- 主要 API: Jobs / Files / Console / Workflow / Software Management / Cloud Provisioning
- Workflow: XML 定義、REXX/JCL/shell/REST step
- SAF 認可: IZUDFLT class (EJBROLE) で role-based

## 3. prerequisites

- ZOS-USS-001
- ZOS-RACF-001

## 4. relations

- `depends_on`: ZOS-USS-001, ZOS-RACF-001
- `specialized_by`: なし
- `contrasts_with`: AWS console API, Kubernetes API server, Azure ARM API
- `used_by`: ZOS-ZCX-001, ZOS-ANSIBLE-001, ZOS-JAVA-001, ZOS-SCHED-001

## 5. pitfalls

- **IZUSVR1 起動失敗で全停止** → 自動化全停止、HA + USS 監視で対策
- **JWT token 期限切れ** → 長期 job で 401、API key or 再認証ループ
- **Workflow rollback 不能** → 失敗で副作用残置、compensating step 設計
- **IZUDFLT EJBROLE 漏れ** → user 401、onboarding script 必須

## 6. examples

```
S IZUSVR1
curl -k -u USR001:PASSWORD -X PUT --data-binary @hello.jcl https://zosmf.example.com:443/zosmf/restjobs/jobs
zowe jobs submit local-file hello.jcl --zosmf-profile prod
zowe files list ds "USR001.**" --zosmf-profile prod
```

## 7. decision_axes

- **単一 vs HA**: 業務クリティカル自動化なら HA
- **Basic Auth vs JWT vs API key**: CI/CD は API key
- **Zowe CLI vs 直接 REST**: 標準は Zowe、特殊は direct

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_TECH_001/002) から z/OSMF 運用知識を概念蒸留 (ADR-0109)。逐語引用禁止。
