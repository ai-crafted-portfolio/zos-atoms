---
id: ZOS-JAVA-001
title: Java for z/OS + JZOS
status: draft
last_reviewed: 2026-06-02
authors: [agent-z6]
rag_verified: partially
---

# ZOS-JAVA-001: Java for z/OS + JZOS

## 1. purpose

Java for z/OS は IBM Semeru / OpenJDK ベースの z/OS native JVM、JZOS は JCL batch step として起動する launcher 群。zIIP 100% eligible で課金枠外、Java/Spring/REST を z/OS 中核で動かす経路、COBOL/PL/I との共存が現実目標。OpenJDK on Linux と機能近いが JZOS + Db2 type 2 + WLM 連携が独自。

## 2. mechanism

- IBM Semeru Runtime Certified Edition for z/OS、Java 8/11/17/21 LTS
- JZOS launcher: JVMLDM86 (Java 11+)、STDENV DD で env、JAVAJCL/STDIN/STDOUT/STDERR
- Db2 JDBC type 2 (JNI, μs) / type 4 (TCP, ms)
- CICS Java / IMS Java / Liberty for z/OS
- zIIP eligibility、SMF type 30 計測
- EBCDIC default (IBM-1047)、UTF-8 override 可

## 3. prerequisites

- ZOS-USS-001
- ZOS-JCL-001
- Java SE 一般

## 4. relations

- `depends_on`: ZOS-USS-001
- `specialized_by`: なし
- `contrasts_with`: OpenJDK on Linux, OpenJDK on Linux on Z, GraalVM, ZOS-WAS-001
- `used_by`: ZOS-WAS-001, ZOS-ZCX-001, ZOS-ANSIBLE-001

## 5. pitfalls

- **JZOS DD 引き継ぎ失敗** → ZUtil.getDD で取得必須、FileReader NG
- **JNI memory leak** → native heap 別管理、Db2 close 忘れで S0E2
- **EBCDIC string handling miss** → charset 明示、IBM-1047 vs UTF-8
- **JIT compile 起動時遅延** → AOT / SharedClass / 集約 JVM

## 6. examples

```
//JAVA   EXEC PGM=JVMLDM86,REGION=0M,
//   PARM='/-Xms512m -Xmx2048m -Dfile.encoding=UTF-8 com.example.Hello'
//STDENV DD *
JAVA_HOME=/usr/lpp/java/ibm/J17.0_64
CLASSPATH=/u/user/app/lib/hello.jar
/*
```

```java
DB2DataSource ds = new DB2DataSource();
ds.setDriverType(2);   // type 2 = JNI, μs
```

## 7. decision_axes

- **JZOS batch vs Liberty vs CICS Java**: online → CICS、REST → Liberty、夜間 → JZOS
- **type 2 vs type 4 JDBC**: 同一 LPAR → type 2、distributed → type 4
- **Java 8 vs 11 vs 17 vs 21**: 新規 21 LTS or 17 LTS


## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

本 atom の領域については、IBM 公式 manual を一次出典としつつ、運用事例や設計判断の補強として市販書籍 (BK_MF_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 等の z/OS / メインフレーム関連書籍) からの実装知識を補助的に参照する。逐語引用は禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
