---
id: ZOS-DB2-001
title: Db2 for z/OS
status: stable
last_reviewed: 2026-05-09
---


# ZOS-DB2-001: Db2 for z/OS

## 1. purpose（なぜ存在するか）

Db2 for z/OS は z/OS 上の **リレーショナル データベース管理システム (RDBMS)**。Linux/Windows 版の Db2 とは **別実装**（同じ「Db2」だが内部はかなり違う）。

なぜ z/OS 専用版が必要か: メインフレームのハードウェア機能（zIIP、CF、SAP プロセッサ、専用 I/O サブシステム）と密結合し、**Sysplex 内 Data Sharing**（複数 LPAR で同じデータを並行更新可、CF 経由ロック調停）等、z/OS でしか実現できない可用性・性能機能を持つため。1 サブシステムで秒間数万トランザクション + データ整合性保証 + ゼロダウンタイム、が現実的に動く。

Linux 系で例えれば PostgreSQL / Oracle Database。違いは **「z/OS Db2 は他 z/OS 機能とのスタック密結合」** で、CICS / IMS / バッチ JCL からの呼び出しと Web 経由 (DDF) を全部均等にサポートする点。

## 2. mechanism（どう動くか）

中核アーキテクチャ:
- **サブシステム (Subsystem)**: 1 つの Db2 インスタンス。SSID 4 文字で識別
- **構成アドレススペース** (5〜6 種):
  - **MSTR**: マスター、全体管理
  - **DBM1**: バッファプール / DB アクセス本体
  - **IRLM**: ロック管理
  - **DDF**: Distributed Data Facility（TCP/IP 経由）
  - **SPAS**: Stored Procedure 実行
- **データセット階層**: テーブルスペース → テーブル → 行 / 列。テーブルスペース実体は VSAM LDS
- **DSNZPARM**: Db2 設定パラメータの ZAP モジュール
- **BIND**: SQL を **PACKAGE** にプリコンパイル + 実行計画を固定。Static SQL（事前 BIND）と Dynamic SQL（実行時 PREPARE）の 2 種
- **Data Sharing**: Sysplex 内複数 Db2 サブシステムが CF 経由で同じテーブルを共有

## 3. prerequisites（理解の前提）

- VSAM（→ [ZOS-VSAM-001](zos-vsam-001.md)）— Db2 のテーブルスペース実体
- RACF（→ [ZOS-RACF-001](zos-racf-001.md)）— 認可
- データセット概念（→ [ZOS-DATASET-001](zos-dataset-001.md)）
- 一般 IT 知識: SQL、ACID、ロック、トランザクション分離レベル
- Sysplex（→ [ZOS-PARALLELSYSPLEX-001](zos-parallelsysplex-001.md)）— Data Sharing 利用時

## 4. relations（他アトムとの繋がり）

- `depends_on`: [ZOS-VSAM-001](zos-vsam-001.md), [ZOS-RACF-001](zos-racf-001.md), [ZOS-DUMP-001](zos-dump-001.md) (DSNWDMP)
- `specialized_by`: なし
- `contrasts_with`: [ZOS-IMS-001](zos-ims-001.md)（階層 vs 関係）, [ZOS-VSAM-001](zos-vsam-001.md)（フル RDB vs ファイル単位）, （未作成）DB2-LINUX-001
- `used_by`: [ZOS-PARALLELSYSPLEX-001](zos-parallelsysplex-001.md) (Data Sharing), [ZOS-CICS-001](zos-cics-001.md) (RRSAF/CAF 接続)

## 5. pitfalls（実装・運用での落とし穴）

- **BIND の PLAN 古いまま実行**: アプリ修正で SQL 変更したのに BIND し忘れ → 古い PLAN/PACKAGE で動く → 一見動くが結果が間違ってる。Db2 はソース変更を検出しない。**修正リリースの BIND 漏れは最も恥ずかしいバグ**、CI/CD で BIND を強制する仕組み必須。
- **DSNZPARM の `BUFFERPOOL` 配分**: BP0/BP8K0 等の既定値のままだと業務テーブル全部 BP0 に入って SWAP 連発。**業務系 + システム系 + 索引で BP 分割**、各 BP のサイズを実測ヒット率で調整。**未調整だと数十倍の性能差**。
- **DDF からの distributed deadlock**: Web/Java から DDF 経由でアクセスする時、コネクションプールの設定とトランザクション境界が合わずに dead lock 多発。`-913` (DEADLOCK OR TIMEOUT) を見たら DDF 設定 + アプリの commit タイミングを疑う。
- **REORG 怠慢で性能劣化**: テーブルスペースが断片化（PAGE 内空き率高、CLUSTERRATIO 低下）すると、SQL 実行計画が同じでも I/O 数が増える。**毎月 REORG ジョブ + REORG TABLESPACE STATISTICS で更新** が原則。怠ると 3 ヶ月で SQL が 10 倍遅くなる。
- **テーブル ALTER の影響範囲を過小評価**: `ALTER TABLE ADD COLUMN` は一見軽そうだが、**全 PACKAGE の REBIND が必要**な場合あり（型変更、列順変更等）。ALTER 前に SYSIBM.SYSPACKAGE への影響把握必要。
- **Catalog の `SYSDATABASE` などへのアプリ直アクセス**: 性能のため Db2 内部カタログを SQL で直接読むコードが過去にある。Db2 バージョンアップでカタログ構造変更されると一斉に動かなくなる。**カタログ参照は専用ビュー経由**、直接アクセス禁止が原則。
- **Sysplex Data Sharing でのロックエスカレーション**: ROW ロックが多発で PAGE → TABLESPACE エスカレーションが起こると、CF 上のロック空間が爆発、別 LPAR の Db2 が動かなくなる。**LOCKMAX = SYSTEM** で監視 + 業務ピークに備える。

## 6. examples（具体例）

```sql
//BIND     EXEC PGM=IKJEFT01,DYNAMNBR=20
//SYSTSPRT DD SYSOUT=*
//SYSTSIN  DD *
  DSN SYSTEM(DB2A)
  BIND PACKAGE(MYAPP) MEMBER(MYPGM) -
       OWNER(APPOWN) -
       VALIDATE(BIND) -
       ISOLATION(CS) -
       ACTION(REPLACE) -
       LIBRARY('USER.DBRMLIB')
  END
/*
```

```cobol
EXEC SQL DECLARE C1 CURSOR FOR
   SELECT CUSTID, NAME FROM CUSTOMER WHERE STATUS = :HV-STATUS
END-EXEC.

EXEC SQL OPEN C1 END-EXEC.
PERFORM FETCH-LOOP UNTIL SQLCODE NOT = 0.
EXEC SQL CLOSE C1 END-EXEC.
```

```
-DIS DB(MYDB)
-DIS THREAD(*)
-START DDF
```

## 7. decision_axes（採否を分ける判断軸）

- **Db2 vs Oracle on Linux vs PostgreSQL on Linux**: z/OS 上アプリとの密結合性 + Sysplex Data Sharing が必要なら Db2 一択。**「z/OS の他機能と一体運用しないなら Db2 for z/OS は overkill」** が判断軸。
- **Static SQL vs Dynamic SQL**: バッチ + COBOL/PL/I は Static、Web/JDBC + 動的クエリは Dynamic。**Static は BIND 漏れ事故あり、Dynamic は cache miss + 計画変動**。多くの本番システムは混在運用。
- **Data Sharing vs 単一サブシステム**: 99.99% 可用性で十分なら単一 LPAR + バックアップ機。**99.999% 必要 + 計画停止禁止** なら Data Sharing 必須。**コスト約 2〜3 倍 + 運用知識特殊**。
- **テーブルスペース パーティション戦略**: 大表（数億行）は PARTITION 切る、小表は単一 TS。**PARTITION KEY 設計を間違うと REORG が悪夢**、初期 1 回で当てる必要。
- **DDF を活用するか否か**: 外部システム連携が中心なら DDF 中核に据える。**z/OS 内アプリだけなら DDF 不要**。
- **Replication 戦略**: Db2 Q Replication / WebSphere MQ / IBM Replication Server。**「データ移送は重い、SQL 同期 vs 物理ログ同期」で性能・整合性が大きく変わる**。
