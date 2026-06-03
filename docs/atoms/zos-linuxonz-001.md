---
title: ZOS-LINUXONZ-001
description: z/VM + Linux guest、SUSE/RHEL on Z、KVM on Z、IBM Z Cloud Native
tags:
  - Modernization
  - Sysplex-Modernization
---
# ZOS-LINUXONZ-001: Linux on Z (LPAR / z/VM)

## 1. purpose

Linux on Z は IBM Z 上で s390x Linux を動かす形態 (Native LPAR / z/VM guest / KVM on Z)。IFL という Linux 専用 CPU で z/OS 課金枠外、x86 比で 1-4 TB RAM / LPAR、z/OS データへ Hipersockets μs 近接、Z RAS 継承。AIX on Power と近い RAS 水準だが Linux 生態系完全互換が特徴。

## 2. mechanism

- Native LPAR (PR/SM 直接) / z/VM guest (高密度 + DCSS) / KVM on Z (libvirt 標準)
- distro: RHEL/SUSE/Ubuntu for s390x
- IFL CPU (z/OS 課金外) を LPAR 単位で割当
- DASD: ECKD (3390 互換) または FBA (SCSI 系)
- z/OS と CTC / Hipersockets / shared OSA で接続
- big-endian, EBCDIC 境界に注意

## 3. prerequisites

- ZOS-DASD-001
- Linux 知識 (kernel, systemd, package manager)
- 仮想化知識 (hypervisor, guest)

## 4. relations

- `depends_on`: ZOS-DASD-001
- `specialized_by`: なし
- `contrasts_with`: Linux on x86, AIX on Power, ZOS-ZCX-001
- `used_by`: ZOS-ZCX-001 (KVM 技術), ZOS-ANSIBLE-001 (target), ZOS-JAVA-001

## 5. pitfalls

- **z/VM CP overhead 過小評価** → 100 guest で 15-30% CPU、x86 KVM ベンチ流用 NG
- **DASD share と Linux disk fence 衝突** → 両方 RW で z/OS catalog 破壊
- **Endian / EBCDIC 橋渡し誤り** → unload binary の数値カラム破壊
- **IFL 課金境界 misconfiguration** → Linux LPAR に GP CPU で月跨ぎ MSU 超過

## 6. examples

```
zipl -V -t /boot -i /boot/image-5.14.0-s390x -P "root=/dev/disk/by-path/ccw-0.0.0200-part1"
chzdev -e dasd 0.0.0200
dasdfmt -b 4096 /dev/dasda
chzdev -e qeth 0.0.f300 0.0.f301 0.0.f302
lscpu
cat /proc/sysinfo
```

## 7. decision_axes

- **Native LPAR vs z/VM vs KVM**: density / 性能 / OpenStack 互換のトレードオフ
- **Linux on Z vs x86**: RAS + 大容量 vs コモディティ
- **ECKD vs FBA**: z/OS 共有か Linux 専用 SAN か
