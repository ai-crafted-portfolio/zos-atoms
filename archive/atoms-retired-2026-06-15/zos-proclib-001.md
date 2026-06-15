---
id: ZOS-PROCLIB-001
title: SYS1.PROCLIB cataloged procedures
status: draft
last_reviewed: 2026-06-04
authors: [agent]
rag_verified: false
---

# ZOS-PROCLIB-001: SYS1.PROCLIB cataloged procedures

## 1. purpose（なぜ存在するか）

SYS1.PROCLIB は z/OS の **cataloged procedure 格納 dataset**。JCL の再利用可能 template (PROC) を member 単位で置き、`START procname` (STC) や `EXEC procname` (job 内 EXEC) で呼び出す。Linux で言えば `/etc/init.d/*` + `/etc/systemd/system/*.service` + `/usr/local/bin/*.sh` を 1 つの PDS にまとめた構造。

PROCLIB は **STC (Started Task) 起動の SSOT** であり、JES2/JES3/TCP/IP/RACF/CICS/IMS/DB2/CICSPlex 等の全 subsystem の起動 JCL がここに集まる。

- 顧客固有の customize は通常 `CPAC.PROCLIB` 等の別 dataset で行い、JES2 procedure の concat で SYS1.PROCLIB の前段に置く
- `MSTJCLxx` (PARMLIB) で master scheduler 用 procedure 名を変更可能だが、SYS1.PROCLIB 自身の概念は変わらず

なぜこの分離が必要か: PROCLIB 単体に絞った atom がないと、STC 起動失敗・JES2 起動失敗・concat 順 trap・symbol 解決 trap が PARMLIB / JCL / system symbols の atom に分散し、現場で「どの atom を読めば PROCLIB が分かるか」が不明瞭になる。

Linux 対比: `/etc/systemd/system/*.service` は file 単位だが、PROCLIB は PDS member 単位 + JCL 構文 + system symbol 解決という独自構造。`/etc/init.d/*.sh` の startup script に近いが、PROCLIB の中身は JCL なので step 単位 + DD 配置 + return code chain で構造化される。

## 2. mechanism（どう動くか）

### PROCLIB 配置と concat

- **SYS1.PROCLIB**: IBM 提供の標準 procedure
- **CPAC.PROCLIB**: 顧客 customize 用
- **JES2 PROCLIB concat**: `JES2PARM` の `PROCLIB(PROC00)` で複数 dataset 列挙、JES2 起動時に static concat
  - 例: `PROCLIB(PROC00) DD(1)=CPAC.PROCLIB DD(2)=SYS1.PROCLIB DD(3)=SYS1.IBM.PROCLIB`
- **STC 用 master scheduler PROCLIB**: `MSTJCLxx` で IEFPDSI / IEFPDSE DD として concat 指定
- **TSO LOGON PROC**: TSO 専用 PROCLIB (`SYS1.TSOPROC`) で LOGON 時の PROC を絞る

### PROC member の構造

```text
//PROCNAME PROC  SYMBOL1=DEFAULT1,SYMBOL2=DEFAULT2
//STEP1   EXEC  PGM=IEFBR14
//DD1     DD    DSN=&SYMBOL1.,DISP=SHR
//* ...
//        PEND  ← inline PROC の場合
```

- 1 行目 `PROC` で symbol default 定義
- 各 step は `EXEC PGM=` / `EXEC PROC=` を持つ
- DD は dataset / SYSOUT / DUMMY 等
- `PEND` は inline PROC (JCL stream 内記述) の終端

### 呼び出し方式

- **START procname**: STC (operator console から)
- **EXEC procname**: batch job 内
- **TSO LOGON proc**: TSO logon 時

### symbol override

- `START procname,SYMBOL1=NEWVAL`
- `EXEC procname,SYMBOL1=NEWVAL`
- `S CICS01.CICSP01,REGION=2G`

### STC parameter passing

- STC は **address space** として起動、STC name が address space name
- `START` で procname を指定、`S procname.identifier` で別名起動可
- 同名 STC を 2 つ起動: `S CICS01.CICSP01` と `S CICS01.CICSP02`

### master scheduler との関係

- IEFPDSI DD: 平常 STC 起動用 PROCLIB concat
- IEFPDSE DD: emergency 用
- `MSTJCLxx` PARMLIB member で変更
- IPL 中の COMMNDxx から `S` command で順次起動

## 3. prerequisites（理解の前提）

- ZOS-JCL-001 (JCL 構文の理解)
- ZOS-PDS-001 (PDS member 操作)
- ZOS-DATASET-001 (dataset 概念)
- ZOS-PARMLIB-001 (MSTJCLxx で procedure 選択)

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-JCL-001, ZOS-PDS-001, ZOS-DATASET-001, ZOS-PARMLIB-001
- `specialized_by`: ZOS-CICS-001 (CICS region startup PROC), ZOS-DB2-001 (DB2 startup PROC), ZOS-IMS-001 (IMS region PROC)
- `contrasts_with`: LINUX-SYSTEMD-001 (未作成、/etc/systemd/*.service), WIN-SERVICES-001 (未作成、Windows services.msc)
- `used_by`: ZOS-CICS-001, ZOS-DB2-001, ZOS-IMS-001, ZOS-TCPIP-001, ZOS-RACF-001, ZOS-WLM-001 (全 STC が PROCLIB 経由)

## 5. pitfalls（実装・運用での落とし穴）

- PROCLIB concat 順を間違えて IBM 版 PROC が顧客 customize 版を override
- JES2 起動時 static PROCLIB concat、運転中に member 追加しても次 JES2 再起動まで反映遅延
- PROC 内 symbol が `&SYMBOL.` 形式と `&SYMBOL` 形式で混在し parser error
- STC 同名起動で 2 つ目が ABEND S822 (DUPLICATE NAME)
- TSO LOGON PROC を本番 PROCLIB に混在させ、誤って batch から呼ばれて失敗
- MSTJCLxx の IEFPDSI 行の dataset list 不整合で IPL 後 STC 起動失敗連発

## 6. examples（具体例）

[examples.md](./examples.md) 参照。基本 STC procedure / CICS region PROC / TSO LOGON PROC / JES2 PROCLIB concat 設定例を収録。

## 7. decision_axes（採否を分ける判断軸）

- SYS1.PROCLIB 直接 customize vs CPAC.PROCLIB 分離
- PROCLIB member を per-subsystem に細分 vs 共通 template + symbol override
- inline PROC (JCL stream 内) vs cataloged PROC
- TSO PROCLIB を専用 dataset 分離 vs 共通 PROCLIB

## 8. 市販書籍参考 (ADR-0109 連動)

<!-- DO_NOT_QUOTE -->
- BK_MF_001 — PROCLIB 概念
- BK_ZOS_TECH_001 — STC PROC 設計実例

詳細は ADR-0109 参照。


## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

本 atom の領域については、IBM 公式 manual を一次出典としつつ、運用事例や設計判断の補強として市販書籍 (BK_MF_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 等の z/OS / メインフレーム関連書籍) からの実装知識を補助的に参照する。逐語引用は禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
