---
id: ZOS-SYSTEM-SYMBOLS-001
title: System symbols
status: draft
last_reviewed: 2026-06-04
authors: [agent]
rag_verified: false
---

# ZOS-SYSTEM-SYMBOLS-001: System symbols (&SYSNAME, &SYSCLONE, etc.)

## 1. purpose（なぜ存在するか）

system symbols は z/OS の **置換変数機構**。`&SYSNAME`, `&SYSCLONE`, `&SYSPLEX`, `&SYSR1`, ユーザ定義 symbol を JCL / PARMLIB / PROCLIB / RACF / SMP/E 等で書ける。

主要用途は **同一 dataset / member を全 LPAR で共有**しつつ、ランタイムで LPAR 別の値を差し込むこと。Sysplex で 10 LPAR を運用する時、PARMLIB / PROCLIB / JCL を LPAR 毎にコピー管理するのは現実的でなく、`DSN=USER.&SYSNAME..LOG` のように symbol で書き、各 LPAR で `&SYSNAME=SYSA` `SYSB` ... と解決させる。

Linux 対比: shell の `$HOSTNAME` や ansible の `{{ inventory_hostname }}` で hostname-aware template を書くのと同じ発想。z/OS の特異性は **IPL 段階で IEASYMxx により確定し、IPL 中の PARMLIB 解析でもう使える** という点。Linux の `$HOSTNAME` は kernel 起動後にしか定まらない (boot 中の initramfs では使えない) のと対比的。

## 2. mechanism（どう動くか）

### symbol 確定の順序

1. **IPL 開始**: HMC IPL parameter 入力
2. **NIP stage**: SYS0.IPLPARM(LOADxx) read、`IEASYM=(00,L)` 等で IEASYMxx 指定
3. **IEASYMxx 解析**: 
   - HW symbol (`SYSNAME` `SYSCLONE` `SYSPLEX` 等) を LPAR 別条件式で確定
   - ユーザ定義 symbol を SYMDEF statement で確定
4. **IEASYS00 etc.**: 以後の PARMLIB read で symbol 置換が動く
5. **IPL 完了**: symbol set は **read-only**、運転中変更不可
6. **JCL / PROC 内**: 解析時に symbol 置換、ただし JCL の symbol 置換は `&SYSNAME` 等の global と `&PROC_LOCAL` 等の local で挙動差あり

### 主要 built-in symbol

- **&SYSNAME**: LPAR 名 (4 文字、例 `SYSA`)
- **&SYSCLONE**: LPAR 名末尾 2 文字 (`SA`, `SB`)
- **&SYSPLEX**: Sysplex 名 (`SPLEX1`)
- **&SYSR1**: SYSRES VOLSER (`Z25RES`)
- **&SYSR2**: alternate SYSRES
- **&SYSCLUSTER**: GDPS cluster
- **&SYSALVL**: SAF active level
- **&SYSOSCONFIG**: OS config name (HCD で定義)
- **&SYSGRS**: GRS configuration
- **&JOBNAME** (JCL のみ): job 名
- **&STEPNAME** (JCL のみ): step 名
- **&YYMMDD / &HHMMSS** (JCL のみ): execution time

### IEASYMxx での定義

```text
SYMDEF(&SITE='TOKYO')
SYMDEF(&ENV='PROD')
SYMDEF(&CICSPFX='CICSP')

* LPAR 別条件
SYSDEF HWNAME(CPU01) LPARNAME(LPAR01)
  SYMDEF(&NODE='A')
  SYMDEF(&MQNAME='MQA1')
SYSDEF HWNAME(CPU01) LPARNAME(LPAR02)
  SYMDEF(&NODE='B')
  SYMDEF(&MQNAME='MQB1')
```

### 利用箇所

- **PARMLIB member**: 全 member で `&SYMBOL.` 置換可
- **JCL**: PROC parameter / DD DSN 等で利用、ただし JCL の symbol substitution 規則あり
- **PROCLIB**: PROC parameter として symbol 渡し可、`&SYSNAME` は global
- **RACF**: STARTED CLASS member で `&SYSNAME` 等を使い LPAR 別 RACF profile
- **SMP/E**: distribution dataset 名で symbol 利用
- **HSM ARCCMD**: `SETSYS PLEXNAME(&SYSPLEX.)` 等
- **JES2 PARM**: `JOBPRTY` `NETSRV` 等で symbol

### `D SYMBOLS` で確認

- 運用中 `D SYMBOLS` で確定 symbol 一覧表示
- IPL 後は read-only、IPL のみ更新

## 3. prerequisites（理解の前提）

- ZOS-IPL-001, ZOS-IPL-002 (IPL 段階で symbol 確定)
- ZOS-PARMLIB-001 (IEASYMxx の中で書く)
- ZOS-JCL-001 (JCL での symbol 利用)
- ZOS-PARALLELSYSPLEX-001 (sysplex で複数 LPAR symbol 統一)

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-IPL-002, ZOS-PARMLIB-001, ZOS-JCL-001
- `specialized_by`: ZOS-PARALLELSYSPLEX-001 (sysplex 全 LPAR で symbol 整合)
- `contrasts_with`: LINUX-HOSTNAME-001 (未作成、$HOSTNAME), ANSIBLE-INVENTORY-001 (未作成、{{ inventory_hostname }})
- `used_by`: ZOS-PARMLIB-001 (全 PARMLIB member), ZOS-PROCLIB-001 (全 PROC), ZOS-RACF-001 (STARTED CLASS), ZOS-HSM-001 (ARCCMD), ZOS-MVS-ALLOCATION-001 (DSN pattern)

## 5. pitfalls（実装・運用での落とし穴）

- `&SYSNAME.` の末尾 dot 忘れで symbol 名解釈エラー (`IEFC658I`)
- IEASYMxx の SYSDEF 条件式 mismatch で wrong LPAR symbol、想定外 DSN allocate
- symbol 値が予約語 (例 `MASTER`, `JES2`) と衝突して system 異常
- JCL の local symbol と PARMLIB の global symbol の同名衝突
- HMC IPL parameter の `IEASYM=L` (= LOADxx 内 SYSPARM= から決める) を変更し忘れ
- ユーザ定義 symbol を 8 文字超で定義し IEFC129I で IPL failure

## 6. examples（具体例）

[examples.md](./examples.md) 参照。IEASYMxx 例、JCL での `&SYSNAME` 使用例、`D SYMBOLS` operator 出力例。

## 7. decision_axes（採否を分ける判断軸）

- ユーザ定義 symbol を IEASYMxx で多用 vs JCL/PROC 内 local symbol
- symbol を HW 系 (HWNAME/LPARNAME) で条件分岐 vs SYSCLONE 文字列でロジック分岐
- &SYSPLEX を symbol で参照 vs literal で書く
- symbol 値変更を計画 IPL に同期 vs 緊急 IPL でアドホックに

## 8. 市販書籍参考 (ADR-0109 連動)

<!-- DO_NOT_QUOTE -->
- BK_MF_001 — system symbol 概念
- BK_ZOS_TECH_001 — IEASYMxx 設計事例

詳細は ADR-0109 参照。


## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

本 atom の領域については、IBM 公式 manual を一次出典としつつ、運用事例や設計判断の補強として市販書籍 (BK_MF_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 等の z/OS / メインフレーム関連書籍) からの実装知識を補助的に参照する。逐語引用は禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
