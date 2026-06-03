---
title: ZOS-MQ-001
description: MQM (queue manager) / MQI / channel / queue 概念、CSQYINIT / CSQZPARM、CSQ メッセージ ID
tags:
  - Subsystem
  - OS-Subsystem
---
# ZOS-MQ-001: IBM MQ for z/OS

## 1. purpose（なぜ存在するか）

**IBM MQ for z/OS** (旧称 MQSeries / WebSphere MQ) は z/OS native の message-oriented middleware。**MQM** (Queue Manager) という started task が中核で、**queue** にメッセージを put / get するアプリ間非同期通信を提供。CICS / IMS / Batch / Db2 trigger / Java JMS から呼べる。

z/OS 版の特徴: **logger** (Log Manager) + **CF list 構造** で共有 queue を実装、Parallel Sysplex 内で **真の active-active** 構成が可能。これは Kafka / RabbitMQ にはない強み。一方で Linux MQ broker、Kafka より初期構築コスト・運用 know-how 要求が高い。

なぜ z/OS 上に MQ か: legacy CICS/IMS から非同期化したい、Parallel Sysplex の高可用性を活用したい、SAF (RACF) 統合認証が欲しい、Pervasive Encryption で transport 自動暗号化したい等のニーズで採用される。Kafka が distributed log で台頭してきたが、MQ は **message-level transaction (RRS 経由 2 PC)** が組めるという独自価値継続。

## 2. mechanism（どう動くか）

**主要 component**:
- **Queue Manager (QM)**: 1 つの z/OS MQ サブシステム、CSQ で始まる JCL/STC
- **CSQ1MSTR** (Master), **CSQ1CHIN** (Channel Initiator), **CSQ1MQDS** (Dataset 管理) 等 started task
- **Page set**: メッセージ永続化用 VSAM linear、複数 (PSID 0-99)
- **Buffer pool**: page set 単位、`CSQYINIT` で size 指定
- **Log dataset**: BSDS (Bootstrap Data Set) + log VSAM、Db2 と類似構成

**Queue 種類**:
- **Local queue**: 自 QM 内 storage
- **Remote queue**: 別 QM の queue への alias
- **Alias queue**: ローカル別名
- **Model queue**: 動的 dynamic queue の template
- **Shared queue** (CF list): Parallel Sysplex 内共有、CF list 構造に乗る

**Channel**:
- **Sender / Receiver**: 一方向 push
- **Requester / Server**: client/server
- **Client connection / SVR (svrconn)**: MQ Client から接続
- **Cluster sender / receiver**: cluster 内自動 routing

**主要 message ID (CSQxxxx)**:
- `CSQX004E`: channel start 失敗
- `CSQM049E`: queue 定義 error
- `CSQI045E`: page set フル
- `CSQR026I`: indoubt unit-of-work 発生
- `CSQX511I`: channel inactivity
- `CSQ9013E`: 認証失敗

**RRS 連携**:
- 2- を RRS coordinator 経由 (→ ZOS-RRS-001)
- DB2 update + MQ put を atomic に
- indoubt 状態は RRS の URID で resolve

**CSQZPARM** / **CSQ6SYSP**:
- system parameter module (load module)、`OPMODE=`, `EXITLIM=` 等
- Assembler macro でビルドして `CSQYINIT` から load

## 3. prerequisites（理解の前提）

- ZOS-DATASET-001 (page set / BSDS / log dataset)
- ZOS-RACF-001 (queue access 認可)
- ZOS-DUMP-001 (CSQ ABEND 解析)
- 一般 IT 知識: message queue / async messaging

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-DATASET-001, ZOS-RACF-001, ZOS-DUMP-001
- `specialized_by`: なし
- `contrasts_with`: Kafka (distributed log、partition / consumer group、at-least-once)、RabbitMQ (AMQP broker、Linux/Windows)、Linux ActiveMQ (JMS broker)、AWS SQS (managed queue、no transaction)、Solace PubSub+ (enterprise messaging appliance)
- `used_by`: ZOS-CICS-001 (CKTI trigger monitor 経由 MQ get)、ZOS-DB2-001 (stored procedure 内 put)、ZOS-PARALLELSYSPLEX-001 (CF shared queue)、ZOS-RRS-001 (2 PC coordinator)

## 5. pitfalls（実装・運用での落とし穴）

- **CSQX004E channel start 失敗、認証 chain 不明**: Sender channel start で `CSQX004E` 出るが原因が **channel auth record (CHLAUTH)** / **SSL/TLS cert** / **MCAUSER** / **remote QM 側の receiver 状態** のどれか不明。**書き手経験**: cross-LPAR で channel disconnect 連発、原因は CHLAUTH に CONNAUTH 設定漏れ、SSL handshake が見えないため CSQX004E 単独では解析できず、両側 channel exit trace 採取して 1 日。**対処**: CSQX004E 出たら片側だけでなく両側の `DIS CHS(*)`, `DIS CHSTATUS(...)`, CHLAUTH list, SSL key repository を平行確認。
- **DLQ (Dead Letter Queue) 溢れで業務停止**: Invalid message が DLQ (`SYSTEM.DEAD.LETTER.QUEUE`) に流入し、queue depth が `MAXDEPTH` 到達 → 新規 routing 失敗で業務 queue も停止。**書き手経験**: file format mismatch で月次バッチ 100 万件全部 DLQ 化、DLQ MAXDEPTH 5 万で溢れ、新規 OLTP も put 失敗。**対処**: DLQ handler (CSQUDLQH) を必ず常駐、DLQ 監視 SOP、MAXDEPTH を業務 queue より大きく設定 (10 万以上)。
- **Indoubt unit-of-work 放置で resource lock**: channel disconnect 後の committee phase で indoubt 状態 → resolve しないと page set lock 残置、queue access 阻害。**現場対処**: `DIS THREAD(*) TYPE(INDOUBT)` で確認、`RESOLVE INDOUBT(threadno) ACTION(COMMIT|BACKOUT)` で解決。判断は trading partner と擦り合わせ必須、独断 backout で重複送信事故あり。
- **Channel auth record 漏れで unauth user に MCAUSER**: CHLAUTH の default で `MCAUSER('*MQADMIN')` が許可されると、anonymous SVRCONN connection が ADMIN 権限取得可能 (silent escalation)。**書き手経験**: dev QM で 検証中の MCAUSER default 残し、social engineering で MQ Explorer 接続→PUT/GET 自由、本番では即遮断対応。**対処**: 構築直後に `SET CHLAUTH(*) TYPE(BLOCKUSER) USERLIST('*MQADMIN','*NOACCESS')` で防御、最小権限の `MCAUSER` を明示割当。
- **Page set フル (CSQI045E) で put reject**: Page set 使用率 100% で `MQRC_Q_SPACE_NOT_AVAILABLE` (`2192`) reject、業務 OLTP put 失敗。**対処**: page set 動的拡張 `ALTER QMGR ALTER PSID(...)` または `EXPAND` で容量増、buffer pool / log dataset の連動状況も確認。設計時 page set 数 6 以上推奨 (1 業務 = 1 page set で分離)。
- **BSDS (Bootstrap Data Set) 破損で QM 起動不能**: BSDS dual copy のどちらか破損で `CSQJ001E` で QM 起動失敗。**書き手経験**: BSDS 1 つだけの構成で BSDS 破損、log 再生不能で半日業務停止。**対処**: BSDS は必ず dual、自動切替設定、定期的 BSDS image copy。
- **Shared queue (CF list) で CF link 障害時の rebuild 遅延**: CF link 障害で list 構造 rebuild、その間 shared queue 不能。**書き手経験**: CF maintenance 中の rebuild に 5 分かかり、その間 cross-LPAR 業務停止。**対処**: rebuild policy で auto rebuild 設定、CF link 二重化、平時 maint は片寄せ運用。

## 6. examples（具体例）

```
* CSQYINIT (system parameter load module 抜粋)
         CSQ6SYSP CTHREAD=200,                                         X
                  IDBACK=10,                                            X
                  IDFORE=100,                                           X
                  TRACSTR=GLOBAL                                       X
                  OPMODE=(NEWFUNC,930)
         CSQ6LOGP DEALLCT=NO,                                          X
                  LOGLOAD=500000,                                       X
                  TWOACTV=YES
         END
```

```
* QM 起動 JCL
//CSQ1MSTR PROC HLQ='MQM930.SCSQ',                                     ←
//             QMGR='CSQ1',                                            ←
//             SUFFIX='YINIT'
//CSQMSTR  EXEC PGM=CSQYASCP,REGION=0M,
//         PARM=('SSN=&QMGR','CRC=Z','PARM=&SUFFIX')
//STEPLIB  DD DISP=SHR,DSN=&HLQ.AUTH
//BSDS1    DD DISP=SHR,DSN=MQM.&QMGR..BSDS01
//BSDS2    DD DISP=SHR,DSN=MQM.&QMGR..BSDS02
//CSQOUT1  DD SYSOUT=*
//SYSPRINT DD SYSOUT=*
```

```
* MQSC command 例
DEFINE QLOCAL('APP1.IN.Q') DEFPSIST(YES) +
       MAXDEPTH(50000) MAXMSGL(4194304) +
       BOTHRESH(3) BOQNAME('APP1.BACKOUT.Q')

DEFINE CHANNEL('SYSA.TO.SYSB') CHLTYPE(SDR) +
       CONNAME('SYSB.example.com(1414)') XMITQ('SYSB.XMITQ') +
       SSLCIPH(TLS_RSA_WITH_AES_256_CBC_SHA256)

SET CHLAUTH(*) TYPE(BLOCKUSER) USERLIST('*MQADMIN','*NOACCESS')
SET CHLAUTH('SYSA.TO.SYSB') TYPE(SSLPEERMAP) +
       SSLPEER('CN=app1,O=MyCo') MCAUSER('APPID01')
```

```
* operator command (z/OS console)
+CSQ1 DIS Q(*) WHERE(CURDEPTH GT 100)
+CSQ1 DIS CHS(*) STATUS(*)
+CSQ1 DIS THREAD(*) TYPE(INDOUBT)
+CSQ1 RESOLVE INDOUBT(0001) ACTION(COMMIT)
+CSQ1 START CHL('SYSA.TO.SYSB')
+CSQ1 ALTER PSID(03) EXPAND(SYSTEM)
```

## 7. decision_axes（採否を分ける判断軸）

- **Local queue vs Shared queue (CF)**: **Local** は単 QM 内、低 overhead、HA は QM 再起動依存。**Shared** (CF list) は Parallel Sysplex 内で active-active、HA 強だが CF 帯域消費 + CFLEVEL 制約。**選定基準**: HA 要件 (RTO 秒単位なら Shared)、message size (CF list は size 制限)、CF 容量。
- **Channel: Sender/Receiver vs Cluster**: **Sender/Receiver** は明示 routing、設計分かりやすいが QM 増えると channel 数爆発 (N×(N-1))。**Cluster** は repository QM 経由自動 routing、scalable だが trace 困難。**選定基準**: QM 数 (5 以下なら明示、10+ なら cluster)、運用熟練度。
- **DLQ handler の auto-retry 戦略**: **全 retry** は queue depth 増加と loop リスク、**limit 付き retry** は data loss リスク。**選定基準**: message 特性 (再送可 / 不可)、業務影響、retry 回数上限 (典型 3 回)。
- **Transaction: 1 PC vs 2 PC (RRS)**: **1 PC** (MQ 単独 commit) は速いが MQ と DB の atomic 性なし。**2 PC** (RRS 経由) は完全 atomic だが overhead + indoubt 処理必要。**選定基準**: data 整合性 SLA、indoubt 運用負荷許容度、性能要件。
- **CSQZPARM Static vs Dynamic alter**: **Static** (load module rebuild + QM restart) は変更に IPL/restart 必要。**Dynamic** (`SET SYSTEM`, `SET QMGR`) は run-time 反映、ただし全 parameter 対応してない。**選定基準**: 変更頻度、システム停止許容度。
