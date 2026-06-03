---
title: ZOS-ZCX-001
description: Linux container on z/OS、Docker、provisioning workflow、zCX appliance
tags:
  - Modernization
  - Sysplex-Modernization
---
# ZOS-ZCX-001: zCX (z/OS Container Extensions)

## 1. purpose

zCX は z/OS Address Space として **Linux on Z + Docker Engine** を appliance で動かす機能 (z/OS V2.4+)。z/OS データに低遅延 access する Linux container を z/OS の WLM/RACF/SMF 体制下で運用、modernization 経路として設計。x86 Docker (mainframe 外) や Linux on Z LPAR (resource 分離) と並ぶが、z/OS 一体運用が独自ポジション。

## 2. mechanism

- z/OSMF workflow で provisioning、SMF type 30 課金
- 1 zCX = 1 z/OS Started Task、内部に KVM + Linux guest + Docker engine
- s390x Docker image (Liberty, MQ, Db2, OpenJDK 等)
- Hipersockets で z/OS TCP/IP と μs 通信、OSA で外部
- zIIP 100% eligible、WLM service class で goal 設定

## 3. prerequisites

- ZOS-USS-001
- ZOS-ZOSMF-001
- ZOS-WLM-001

## 4. relations

- `depends_on`: ZOS-USS-001, ZOS-ZOSMF-001, ZOS-WLM-001
- `specialized_by`: なし
- `contrasts_with`: x86 Docker, Linux on Z LPAR, Kubernetes on x86, OpenShift on Z
- `used_by`: ZOS-WAS-001, ZOS-JAVA-001, ZOS-ANSIBLE-001

## 5. pitfalls

- **DASD 過小設計** → ZFS 逼迫で container 起動失敗、online resize 不可
- **TCP/IP stack 共有衝突** → port collision、Hipersockets MTU 過大
- **Java vs zCX 性能トレードオフ判断ミス** → CPU 30% 増、native との分割原則
- **Provisioning workflow 反映漏れ** → WLM/RACF/SMF 後処理漏れで slow + 監査 NG

## 6. examples

```
S ZCXAPP1
ssh -p 8022 admin@zcxapp1.example.com
docker pull docker.io/ibmcom/websphere-liberty:latest
docker run -d --name liberty1 -p 9080:9080 ibmcom/websphere-liberty
```

## 7. decision_axes

- **zCX vs Linux on Z LPAR**: z/OS 隣接 → zCX、大規模 k8s → LPAR
- **zCX vs Liberty native**: CICS/Db2 密 → native、Spring 派 → zCX
- **Container registry**: 規制業界 → 社内 registry 一択
