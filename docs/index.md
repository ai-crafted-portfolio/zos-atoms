# z/OS アトムガイド

メインフレーム z/OS の中核概念を、**62 個の知識アトム**として整理した学習ガイドです。
各アトムは独立して読めて、かつ相互にリンクされています。初学者がメインフレームの「なぜそう設計されているか」を体系的に理解することを目的としています。

アトムの読み方は [凡例](legend.md) を参照してください。

## アトム構成

| 区分 | アトム数 | カバー範囲 |
| --- | --- | --- |
| 既存アトム | 20 | データ管理 / データセット種別 / ジョブと実行 / サブシステム / ワークロード管理 / セキュリティと監査 / UNIX 環境 / 障害復旧と診断 |
| 新規 α | 7 | OS + サブシステム (ASCB / 仮想記憶 / IPL / コンソール / Wait state / MQ / WAS) |
| 新規 β | 8 | ミドルウェア + ユーティリティ (SAF / ICSF / PE / AT-TLS / 証明書管理 / IDCAMS / IEBCOPY / IEFBR14) |
| 新規 γ | 7 | セキュリティ + ネットワーク (RACF Advanced / ACEE / VTAM / TCP/IP / OSA / EE / FTP) |
| 新規 δ | 5 | ストレージ + 監視 (HSM / Tape / RMF / OPERLOG / NetView) |
| 新規 ε | 6 | 復旧 + ワークロード (IPCS / RRS / ARM / IRD / Capacity planning / Batch scheduler) |
| 新規 ζ | 9 | Sysplex + モダナイゼーション (CF / GRS / XCF / GDPS / zCX / Linux on Z / z/OSMF / Java / Ansible) |
| **合計** | **62** | |

## 既存アトム (20)

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

## 新規アトム (42)

### α OS + サブシステム (7)

- [ZOS-ASCB-001: アドレス空間制御ブロック (ASCB / ASSB)](atoms/zos-ascb-001.md)
- [ZOS-VIRTSTOR-001: 仮想記憶 + ストレージ階層](atoms/zos-virtstor-001.md)
- [ZOS-IPL-001: IPL + LOADxx parm](atoms/zos-ipl-001.md)
- [ZOS-CONSOLE-001: MVS コンソール + WTO/WTOR](atoms/zos-console-001.md)
- [ZOS-WAITSTATE-001: Wait state / loop / disabled wait](atoms/zos-waitstate-001.md)
- [ZOS-MQ-001: IBM MQ for z/OS](atoms/zos-mq-001.md)
- [ZOS-WAS-001: WebSphere Application Server for z/OS](atoms/zos-was-001.md)

### β ミドルウェア + ユーティリティ (8)

- [ZOS-SAF-001: System Authorization Facility (SAF) callable services](atoms/zos-saf-001.md)
- [ZOS-ICSF-001: ICSF (Integrated Cryptographic Service Facility) + CKDS/PKDS](atoms/zos-icsf-001.md)
- [ZOS-PE-001: Pervasive Encryption (PE)](atoms/zos-pe-001.md)
- [ZOS-AT-TLS-001: AT-TLS (Application Transparent TLS)](atoms/zos-at-tls-001.md)
- [ZOS-CERTMGMT-001: RACDCERT + 証明書管理](atoms/zos-certmgmt-001.md)
- [ZOS-IDCAMS-001: IDCAMS (Access Method Services)](atoms/zos-idcams-001.md)
- [ZOS-IEBCOPY-001: IEBCOPY + PDS/PDSE 操作 utility](atoms/zos-iebcopy-001.md)
- [ZOS-IEFBR14-001: IEFBR14 + dummy step utility](atoms/zos-iefbr14-001.md)

### γ セキュリティ + ネットワーク (7)

- [ZOS-RACF-ADV-001: RACF Advanced (Mixed-case password / MFA / Health Check)](atoms/zos-racf-adv-001.md)
- [ZOS-ACEE-001: ACEE / Address Space Identity](atoms/zos-acee-001.md)
- [ZOS-VTAM-001: VTAM (SNA Network Communication)](atoms/zos-vtam-001.md)
- [ZOS-TCPIP-001: TCP/IP for z/OS](atoms/zos-tcpip-001.md)
- [ZOS-OSA-001: OSA-Express + FICON / OSM](atoms/zos-osa-001.md)
- [ZOS-EE-001: Enterprise Extender (SNA over IP)](atoms/zos-ee-001.md)
- [ZOS-FTP-001: z/OS FTP / Connect:Direct](atoms/zos-ftp-001.md)

### δ ストレージ + 監視 (5)

- [ZOS-HSM-001: DFSMShsm + tape hierarchy](atoms/zos-hsm-001.md)
- [ZOS-TAPE-001: Tape / VTL (TS7700, Cloud Tape)](atoms/zos-tape-001.md)
- [ZOS-RMF-001: RMF (Resource Measurement Facility)](atoms/zos-rmf-001.md)
- [ZOS-OPERLOG-001: OPERLOG + SYSLOG + log stream](atoms/zos-operlog-001.md)
- [ZOS-NETVIEW-001: NetView + automation](atoms/zos-netview-001.md)

### ε 復旧 + ワークロード (6)

- [ZOS-IPCS-001: IPCS (Interactive Problem Control System)](atoms/zos-ipcs-001.md)
- [ZOS-RRS-001: RRS (Resource Recovery Services)](atoms/zos-rrs-001.md)
- [ZOS-ARM-001: ARM (Automatic Restart Manager)](atoms/zos-arm-001.md)
- [ZOS-IRD-001: IRD (Intelligent Resource Director)](atoms/zos-ird-001.md)
- [ZOS-CAPCALC-001: Capacity planning (MSU / 4HRA / SCRT)](atoms/zos-capcalc-001.md)
- [ZOS-SCHED-001: Batch scheduler (TWS / Control-M / OPC)](atoms/zos-sched-001.md)

### ζ Sysplex + モダナイゼーション (9)

- [ZOS-CF-001: Coupling Facility (CF) 構造詳細](atoms/zos-cf-001.md)
- [ZOS-GRS-001: GRS (Global Resource Serialization)](atoms/zos-grs-001.md)
- [ZOS-XCF-001: XCF (Cross-System Coupling Facility) + JES2/JES3 spool](atoms/zos-xcf-001.md)
- [ZOS-GDPS-001: GDPS / PPRC / XRC / HyperSwap](atoms/zos-gdps-001.md)
- [ZOS-ZCX-001: zCX (z/OS Container Extensions)](atoms/zos-zcx-001.md)
- [ZOS-LINUXONZ-001: Linux on Z (LPAR / z/VM)](atoms/zos-linuxonz-001.md)
- [ZOS-ZOSMF-001: z/OSMF (REST + workflow)](atoms/zos-zosmf-001.md)
- [ZOS-JAVA-001: Java for z/OS + JZOS](atoms/zos-java-001.md)
- [ZOS-ANSIBLE-001: Ansible for z/OS (Red Hat / IBM collection)](atoms/zos-ansible-001.md)
