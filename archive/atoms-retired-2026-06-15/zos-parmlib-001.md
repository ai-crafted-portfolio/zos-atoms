---
id: ZOS-PARMLIB-001
title: SYS1.PARMLIB members
status: draft
last_reviewed: 2026-06-04
authors: [agent]
rag_verified: false
---

# ZOS-PARMLIB-001: SYS1.PARMLIB members

## 1. purpose（なぜ存在するか）

SYS1.PARMLIB は z/OS の **system parameter dataset 群**。Linux の `/etc/` 一式に近いが、構造が明確に違う: (a) PDS / PDSE で **member 単位**、(b) member 名末尾の 2 桁 suffix (`xx`) で **「平常 = 00、保守 = 99、 DR = DR」のような世代切替** を表現、(c) `SET xx=YY` operator command で運転中に suffix を動的切替できる member とできない member が混在。

各 member の責務 + 動的反映可否 + 反映方法を熟知していないと、運用設計を誤る。例えば `IEASYS00` (一般 system parm) は基本的に IPL 限定だが、`SET SMF=01` で SMF parm だけ切替可、`SET IEAOPT=02` で WLM 動作だけ動的切替可、等の member 別 SOP 知識が必要。

Linux 対比: `/etc/sysctl.conf` は `sysctl -p` で動的反映、`/etc/fstab` は mount 単位、`/etc/systemd/` は `systemctl daemon-reload` で動的反映、と member 相当が file/directory で分散。z/OS は **すべて 1 つの PDS member として `SYS1.PARMLIB(xxxxx)`** に集約され、suffix 規約 + `SET` command で切替方式を統一する設計。

## 2. mechanism（どう動くか）

### PARMLIB の物理構造

- **dataset organization**: PDS (legacy) または PDSE (現代推奨、directory 動的拡張可)
- **member 名**: 8 文字、規約上 `xxxxxYY` 形式 (固定 prefix + 2 桁 suffix)、例 `IEASYS00`, `IEAOPT01`
- **concatenation**: LOADxx の PARMLIB statement で 16 dataset まで concat 可、最初に hit した member が使われる
- **代表 dataset 配置**: `SYS1.PARMLIB` (IBM 提供), `SYS1.IBM.PARMLIB` (IBM 提供 PTF 配布用), `CPAC.PARMLIB` (顧客 customize 用) の 3 段 concat が標準

### 主要 member カテゴリ

#### IPL 系 (IPL 限定、動的反映不可)
- **IEASYSxx**: 一般 system parm
- **IEASYMxx**: system symbol (`&SYSNAME`, `&SYSCLONE`)
- **CLOCKxx**: TOD / timezone
- **NUCLSTxx**: nucleus module 選択
- **LPALSTxx**: LPA load list

#### 半動的 (SET command で suffix 切替可)
- **IEAOPTxx**: WLM/SRM 関連 (`SET OPT=xx`)
- **SMFPRMxx**: SMF 設定 (`SET SMF=xx`)
- **CONSOLxx**: console (`SET CON=xx`)
- **GRSCNFxx / GRSRNLxx**: GRS (`SET GRSRNL=xx`)
- **PROGxx**: APF/LNKLST/LPA (`SET PROG=xx` で部分反映)

#### 完全動的 (operator command 単位反映)
- **COMMNDxx**: 起動時の operator command 実行リスト
- **CSDxx (RACF)**: RACF DB

#### subsystem 系 (subsystem 起動時に読まれる、subsystem 単位で SET 可)
- **TCPIPxx (TCP/IP)**: TCP/IP profile
- **VATLSTxx**: VATLST (Volume Attribute List)

### SET command による suffix 切替

- `SET IEASYS=xx` → IEASYSxx を再読、ただし反映項目は限定 (CMD 等は無視)
- `SET OPT=xx` → IEAOPTxx 全項目反映、WLM/SRM が動的に挙動変更
- `SET SMF=xx` → SMFPRMxx 反映、SMF タイプ別の record 取得可否が即座に変わる
- `SET CON=xx` → CONSOLxx 反映、ROUTCODE 等が反映
- `SET PROG=xx` → PROGxx 反映、APF / LNKLST / LPA の **追加**は可、削除は再 IPL 必要

### Syntax check

- `SET PARMLIB=xx CHECK` で syntax 検証 (実反映なし)
- IBM 提供の `IEASYSCK` で詳細検証 (一部)

## 3. prerequisites（理解の前提）

- ZOS-IPL-001 (LOADxx 経由の PARMLIB 参照)
- ZOS-IPL-002 (IPL 段階での member read 順)
- ZOS-DATASET-001 (PDS/PDSE 概念)
- ZOS-PDS-001 (PDS member 操作)

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-IPL-001, ZOS-IPL-002, ZOS-DATASET-001, ZOS-PDS-001
- `specialized_by`: ZOS-SYSTEM-SYMBOLS-001 (IEASYMxx の symbol 解決詳細)
- `contrasts_with`: LINUX-SYSCTL-001 (未作成、/etc/sysctl.conf), WIN-REGISTRY-001 (未作成、Windows Registry)
- `used_by`: ZOS-RACF-001 (PROGxx で APF 認可), ZOS-SMF-001 (SMFPRMxx), ZOS-WLM-001 (IEAOPTxx), ZOS-CONSOLE-001 (CONSOLxx), ZOS-TCPIP-001 (TCPIPxx)

## 5. pitfalls（実装・運用での落とし穴）

- PARMLIB concatenation の前段に古い member が残り意図せず override
- `SET xx=YY` で動的反映できない項目を反映できると誤認、IPL まで効かず障害発覚
- PDSE concatenation で member directory hash 衝突、`IEB143I` 系で member load 失敗
- IEASYSxx の `CMD=` だけは `SET` で反映されない、運用変更の落とし穴
- 同名 member が複数 concat に存在し、運用変更を上位 PDS に書いたつもりで下位に書く事故
- syntax check (`SET PARMLIB CHECK`) を省略して反映、半反映状態で system 異常

## 6. examples（具体例）

[examples.md](./examples.md) 参照。IEASYS00 / IEAOPT00 / SMFPRM00 / CONSOL00 / PROG00 の典型例、SET command の運用例。

## 7. decision_axes（採否を分ける判断軸）

- PDS vs PDSE
- 顧客 PARMLIB 1 本 vs 用途別 (DEV/PROD/DR)
- suffix 命名規約 (`00` 平常 vs 用途別 hex)
- SYS1.PARMLIB を customize vs CPAC.PARMLIB に分離

## 8. 市販書籍参考 (ADR-0109 連動)

<!-- DO_NOT_QUOTE -->
- BK_MF_001 — PARMLIB 概念
- BK_ZOS_TECH_001 — PARMLIB member 詳細運用

詳細は ADR-0109 参照。


## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

本 atom の領域については、IBM 公式 manual を一次出典としつつ、運用事例や設計判断の補強として市販書籍 (BK_MF_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 等の z/OS / メインフレーム関連書籍) からの実装知識を補助的に参照する。逐語引用は禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
