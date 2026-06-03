---
title: ZOS-ANSIBLE-001
description: Ansible playbook、`zos_*` モジュール、DevOps for mainframe、Galaxy collection
tags:
  - Modernization
  - Sysplex-Modernization
---
# ZOS-ANSIBLE-001: Ansible for z/OS (Red Hat / IBM collection)

## 1. purpose

Ansible for z/OS は Red Hat (IBM) collections (`ibm.ibm_zos_core`, `ibm.ibm_zos_zosmf`, `ibm.ibm_zos_cics`, `ibm.ibm_zos_ims` 等) を介し、Ansible playbook から z/OS の dataset/JCL/RACF/CICS/IMS/z/OSMF を操作する DevOps 統合経路。3270 手順書を YAML 化 + GitOps 経路化。Chef/Puppet は z/OS 対応限定的、Ansible が de facto。

## 2. mechanism

- Connection: SSH (USS Python interpreter) または z/OSMF REST
- IBM Open Enterprise SDK for Python for z/OS (3.10+) を USS に配置
- Collections: ibm_zos_core / ibm_zos_zosmf / ibm_zos_cics / ibm_zos_ims / ibm_zos_sysauto
- 主要 module: zos_data_set / zos_job_submit / zos_job_output / zos_copy / zos_mvs_raw / zos_operator
- inventory: ansible_user, ansible_python_interpreter 必須
- idempotency: state=present/absent で対応 (限定的)

## 3. prerequisites

- ZOS-USS-001
- ZOS-ZOSMF-001
- Ansible 一般 (playbook, role, inventory)

## 4. relations

- `depends_on`: ZOS-USS-001, ZOS-ZOSMF-001
- `specialized_by`: なし
- `contrasts_with`: Linux Ansible, Chef, Puppet, SaltStack, Terraform
- `used_by`: ZOS-JCL-001, ZOS-RACF-001, ZOS-DATASET-001, ZOS-ZOSMF-001

## 5. pitfalls

- **OMVS segment 漏れ** → SSH login 失敗、ALTUSER OMVS 設定必須
- **zos_data_set DISP 不整合** → 属性 mismatch 黙殺で IEC141I S013-18
- **idempotency 違反** → IDCAMS DEFINE 重複で RC=4、pre-check + failed_when
- **Collection version mismatch** → dev/prod 動作差、requirements.yml 固定必須

## 6. examples

```yaml
- name: Allocate config dataset
  ibm.ibm_zos_core.zos_data_set:
    name: USR001.PROD.CONFIG
    state: present
    type: pds
    space_primary: 5
    record_format: fb
    record_length: 80

- name: Submit JCL
  ibm.ibm_zos_core.zos_job_submit:
    src: "USR001.PROD.JCL(SETUP)"
    location: data_set
  register: job_result

- name: Operator command
  ibm.ibm_zos_core.zos_operator:
    cmd: "-DSNZ DISPLAY GROUP"
```

## 7. decision_axes

- **SSH vs z/OSMF REST**: deep automation は SSH
- **ansible-playbook vs AAP**: PoC は CLI、production は AAP
- **Ansible vs Chef/Puppet/Terraform**: z/OS は Ansible 一択、multi-cloud は Terraform + Ansible hybrid
