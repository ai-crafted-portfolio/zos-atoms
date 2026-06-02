# z/OS アトムガイド

メインフレーム z/OS の中核概念を、**20 個の知識アトム**として整理した学習ガイドです。
各アトムは独立して読めて、かつ相互にリンクされています。初学者がメインフレームの「なぜそう設計されているか」を体系的に理解することを目的としています。

アトムの読み方は [凡例](legend.md) を参照してください。

## アトム一覧

### 基礎: データ管理

- [ZOS-DATASET-001: データセット](atoms/zos-dataset-001.md)
- [ZOS-DASD-001: DASD（直接アクセス記憶装置）](atoms/zos-dasd-001.md)
- [ZOS-CATALOG-001: カタログ（ICF, マスター + ユーザ）](atoms/zos-catalog-001.md)
- [ZOS-SMS-001: SMS（System Managed Storage）](atoms/zos-sms-001.md)

### データセット種別

- [ZOS-PDS-001: 区分データセット（PDS / PDSE）](atoms/zos-pds-001.md)
- [ZOS-VSAM-001: VSAM（KSDS / RRDS / ESDS / LDS）](atoms/zos-vsam-001.md)
- [ZOS-GDG-001: GDG（Generation Data Group）](atoms/zos-gdg-001.md)

### ジョブと実行

- [ZOS-JCL-001: JCL 基礎（JOB / EXEC / DD）](atoms/zos-jcl-001.md)
- [ZOS-TSO-001: TSO（対話シェル + ISPF）](atoms/zos-tso-001.md)
- [ZOS-SORT-001: DFSORT / Syncsort（メインフレーム sort/merge/copy utility）](atoms/zos-sort-001.md)

### サブシステム

- [ZOS-CICS-001: CICS（オンライン トランザクション）](atoms/zos-cics-001.md)
- [ZOS-DB2-001: Db2 for z/OS](atoms/zos-db2-001.md)
- [ZOS-IMS-001: IMS（階層 DB + トランザクション）](atoms/zos-ims-001.md)

### ワークロード管理

- [ZOS-WLM-001: Workload Manager（WLM）](atoms/zos-wlm-001.md)
- [ZOS-PARALLELSYSPLEX-001: Parallel Sysplex（クラスタリング）](atoms/zos-parallelsysplex-001.md)

### セキュリティと監査

- [ZOS-RACF-001: RACF（セキュリティ / SAF）](atoms/zos-racf-001.md)
- [ZOS-SMF-001: SMF（システム計測ログ）](atoms/zos-smf-001.md)

### UNIX 環境

- [ZOS-USS-001: UNIX System Services（HFS / zFS）](atoms/zos-uss-001.md)

### 障害復旧と診断

- [ZOS-RECOVERY-001: バックアップ + DR（DFSMShsm / DFSMSdss / DRP）](atoms/zos-recovery-001.md)
- [ZOS-DUMP-001: SVC ダンプ / SYSMDUMP / SYSUDUMP / SYSABEND](atoms/zos-dump-001.md)
