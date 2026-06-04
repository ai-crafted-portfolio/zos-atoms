---
id: ZOS-FTP-001
title: z/OS FTP / Connect:Direct
status: stable
last_reviewed: 2026-06-02
authors: [agent]
rag_verified: partially
---

# ZOS-FTP-001: z/OS FTP / Connect:Direct

## 1. purpose（なぜ存在するか）

z/OS のファイル転送は、企業システム間でデータをやり取りする中核経路。**(a) z/OS FTP server / client** (z/OS Communications Server に標準同梱、RFC 959 + RFC 4217 (FTPS) 対応、SITE command で MVS dataset 属性指定) と **(b) Connect:Direct (旧称 NDM, Network Data Mover)** (IBM が買収した Sterling Commerce 製の専用 product、PROCESS と呼ぶ独自 script で送受信指示、エンタープライズ EAI で広範に使われる) の 2 大経路が並存する。

加えて MVS dataset を扱える独自ハンドリングとして、(a) RECFM / LRECL / BLKSIZE / DSORG (PS/PO/VS) 等の dataset 属性を SITE command で server 側に通知する必要、(b) EBCDIC / ASCII 自動変換、(c) Connect:Direct は dataset 属性 + 暗号化 + checkpoint restart を PROCESS 内に書く、という共通テーマがある。

Linux / クラウドとの対比:
- Linux: `sftp` (SSH-based)、`rsync`、`curl`、ファイルはバイトストリーム + Unix permission のみ、属性概念無し
- AWS: S3 transfer、API ベース、Object key + metadata、暗号化は SSE-KMS / SSE-S3
- z/OS: RECFM/LRECL/BLKSIZE/DSORG + EBCDIC ↔ ASCII + DCB 継承の独自世界、SITE command でこれらを送信元 / 受信先で揃える必要

業務系インターフェースで「**Connect:Direct で送ったが受信側で読めない**」事故の主因は **(a) RECFM 不一致、(b) 文字コード変換漏れ、(c) checkpoint 残骸、(d) AT-TLS 強制漏れで cleartext**。本アトムはこれらを実務トピックとして扱う。

## 2. mechanism（どう動くか）

### z/OS FTP server (FTPD)
- STC として `S FTPD` で起動、TCP/IP stack に PORT 21 (control) + PORT 20 (data) で bind
- 認証は SAF (RACF) 経由、`PERMIT EZB.FTP.* CLASS(SERVAUTH) ...` でアクセス制御
- 設定は `FTP.DATA` (SYS1.PARMLIB or STC JCL DD)、SITE command の動作は `FTP.DATA` の `SITE`/`SBSUBSTITUTE`/`AUTOSWAPONFTP` 等で制御
- AT-TLS 経由で FTPS (TLS-encapsulated FTP) 提供

### z/OS FTP client
- TSO / JCL / USS shell から `ftp host` で起動、INPUT DD で commands 流入
- `SITE LRECL=80 RECFM=FB BLKSIZE=27920` で server に dataset 属性指定
- ASCII / BINARY / EBCDIC mode 切替: `TYPE A` (ASCII)、`TYPE I` (BINARY 無変換)、`TYPE E` (EBCDIC)
- `QUOTE SITE` で server local の SITE command を強制実行

### Connect:Direct (NDM)
- 専用 product、STC として常駐 (`SNODE` (Secondary Node, 受信側) + `PNODE` (Primary Node, 開始側))
- PROCESS と呼ぶ独自 script 言語で送受信を記述、COPY statement + 各種 SYSOPTS
- 通信は TCP/IP 上の専用プロトコル (port 1364 default)、TLS 化可
- Statistics file に履歴記録、Restart / Checkpoint で大型ファイル転送の途中再開
- Sterling Connect:Direct Secure Plus で SSL/TLS + S/MIME

### RDW (Record Descriptor Word)
- VB (Variable Block) 系 dataset を転送する時、各 record の先頭に 4-byte RDW (record length) が付く
- ASCII / BINARY mode で transfer すると RDW がそのまま入って、受信側で raw bytes として処理すると先頭 4 bytes ゴミ扱い
- 対策: `SITE RDW` / `SITE NORDW`、Connect:Direct なら `SYSOPTS=":DATATYPE=TEXT:"` 等で明示

## 3. prerequisites

- ZOS-TCPIP-001 (FTP は TCP/IP 上)
- ZOS-DATASET-001 (RECFM / LRECL / BLKSIZE の理解)
- ZOS-RACF-001 (SAF 認可 + Connect:Direct local user ID)
- ZOS-AT-TLS-001 (FTPS の TLS 透過化、Connect:Direct Secure Plus との対比)
- 一般 IT 知識: FTP active/passive mode, TLS handshake

## 4. relations

- `depends_on`: ZOS-TCPIP-001, ZOS-DATASET-001, ZOS-RACF-001
- `specialized_by`: なし
- `contrasts_with`: Linux sftp + rsync, AWS S3 transfer + multipart upload, MFT (Managed File Transfer) product (IBM Sterling B2B Integrator, MFT 製品全般)
- `used_by`: ZOS-CICS-001 (CICS BTS の file transfer), ZOS-DB2-001 (Db2 unload data の受渡し), ZOS-HSM-001 (DR site への migration data 転送)

## 5. pitfalls

詳細は `pitfalls/` 配下。

## 6. examples

詳細は `examples.md`。

## 7. decision_axes

詳細は `decision-axes/` 配下。


## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

本 atom の領域については、IBM 公式 manual を一次出典としつつ、運用事例や設計判断の補強として市販書籍 (BK_MF_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 等の z/OS / メインフレーム関連書籍) からの実装知識を補助的に参照する。逐語引用は禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
