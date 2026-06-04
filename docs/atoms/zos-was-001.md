---
id: ZOS-WAS-001
title: WebSphere Application Server for z/OS
status: draft
last_reviewed: 2026-06-02
authors: [agent-z1]
rag_verified: partially
---

# ZOS-WAS-001: WebSphere Application Server for z/OS

## 1. purpose（なぜ存在するか）

**WebSphere Application Server for z/OS** (WAS for z/OS) は z/OS native の Java EE / Jakarta EE application server。`controller region` + `servant region` の **2 region model** が z/OS 版独自で、Linux/AIX 版とは構成が違う。**Liberty for z/OS** は軽量化版で、現代の主流。

z/OS 版の特徴:
- **Controller region** が listener + WLM dispatching、**Servant region** が実 Java 処理 → WLM が servant 数を **動的増減**
- **SAF** (RACF) 統合認証、SSO で MVS user ID と Java auth が統合
- **JZOS** との連携で batch Java も同居
- **Connector** (J2C) 経由で CICS / IMS / Db2 native 呼出

なぜ z/OS 版選ぶか:
1. legacy CICS / IMS / Db2 と **同 LPAR で in-memory 連携** (network 越えない、latency 1ms 以下)
2. WLM goal-driven 制御で Java workload も自動配分
3. RACF / Pervasive Encryption / GDPS 等 z/OS インフラ機能をそのまま継承
4. Sysplex 内で **session failover** 自動

WAS on Linux / Tomcat / Spring Boot との対比: latency と integration が強み、コスト (MIPS / IFL) が課題。

## 2. mechanism（どう動くか）

**WAS Full (Traditional) v9 の region 構成**:
- **Daemon**: WAS cell の name service、port 9120 (default)
- **Node Agent**: configuration sync、port 9121
- **Deployment Manager** (dmgr): cell admin、port 9100
- **Application server**: 業務、controller + servant の 2 region
  - **Controller region**: listener (HTTP/IIOP)、WLM dispatching、`BBOC*` STC
  - **Servant region**: Java VM 1〜N 個、`BBOS*` STC、application 実行
  - WLM Application Environment 経由で servant 起動

**Liberty for z/OS**:
- 単一 STC、`server.xml` で構成、Java 8/11/17 SDK
- `BBGZSRV` 等 STC 名 (Liberty server 名による)
- z/OS 特有: SAF auth、RRS 連携、CICS CTG client、Db2 type 2 connector

**WLM Application Environment**:
- `APPLENV name` で servant 群を定義、WLM が `IWMSSCRE` SRB で起動
- `D WLM,APPLENV=*` で状態確認
- WLM が `SERVANT` 上限まで servant 増殖、idle 時に減少

**SAF auth path**:
- HTTP request → SSL/AT-TLS → Controller → SAF `R_usermap` で client cert → MVS user ID
- Servant 内で `R_authcheck` で resource auth (FACILITY/EJBROLE class)
- JEE security と SAF が bind、`EJBROLE` profile 経由で role mapping

**主要 dataset**:
- WAS install root: `/usr/lpp/zWebSphere/V9R0/` 等 (USS)
- Profile dir: `/u/wasuser/profiles/AppSrv01/`
- Logs: `/u/wasuser/profiles/AppSrv01/logs/server1/SystemOut.log`

**主要 STC**:
- `BBON001` Daemon
- `BBOC001` Controller (1 つ)
- `BBOS001` Servant (1〜N)
- Liberty は `BBGZSRV` 一発

## 3. prerequisites（理解の前提）

- ZOS-WLM-001 (Application Environment)
- ZOS-USS-001 (Java 実行基盤、profile / config dir)
- ZOS-RACF-001 (SAF EJBROLE / FACILITY class)
- 一般 IT 知識: Java EE / Servlet / JNDI

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-WLM-001, ZOS-USS-001, ZOS-RACF-001
- `specialized_by`: なし
- `contrasts_with`: WAS on AIX/Linux (single JVM、controller/servant 分離無)、Tomcat (single JVM、Java EE 部分のみ)、Liberty on Linux (Liberty for z/OS と config 互換だが SAF/JZOS 連携無)、Spring Boot embedded (uber-jar、process 1 つ)、AWS Elastic Beanstalk (managed deploy)
- `used_by`: ZOS-MQ-001 (JMS via MQ binding)、ZOS-DB2-001 (type 2 / type 4 connector)、ZOS-CICS-001 (CTG, EXCI)、ZOS-IMS-001 (IMS Connect)

## 5. pitfalls（実装・運用での落とし穴）

- **Servant region OOM で WLM が servant 増殖暴走**: 業務 burst で servant の Java heap exhaust → OutOfMemoryError → servant 落ちる → WLM が即補充 → 補充直後にまた OOM、loop。**書き手経験**: 月初 burst で 5 分間に servant 50 回起動/落下、controller 受付 queue は溜まり続け SLA 違反。**対処**: Java `-Xmx` 適正化 + heap dump で leak 解析、WLM `SERVANT_MIN/MAX` で増殖上限、`PROCESS_HUNG_TIME` で hung 検知。
- **WLM Application Environment 未定義 / Quiesced**: Servant 起動しようとして `D WLM,APPLENV=APPENV1` が `Quiesced` 状態、原因は WLM Service Definition で APPLENV 定義漏れ、または `VARY WLM,APPLENV=APPENV1,QUIESCE` 残置。**書き手経験**: 月次 WLM policy 編集で APPLENV 抜けて servant 起動不能、HTTP 503 連発、復旧まで 1 時間。**対処**: WLM policy 変更 SOP に APPLENV 一覧 cross-check、IPL 前 `D WLM,APPLENV=*` で全 ACTIVE 確認。
- **Liberty server.xml 反映漏れ (autoConfigUpdate=false)**: `server.xml` 編集してもサーバが pick しない、原因は default 設定 `monitorInterval=500ms` が一部 element に効かない、または `applicationMonitor` 未設定で `dropins` 反映無。**書き手経験**: feature 追加が反映されず開発者が「設定したのに」と。`updateTrigger=polled` 明示で解決。**対処**: 重要変更後は `bin/server stop && bin/server start` で確実反映、production の autoUpdate は無効推奨。
- **SAF Java 認可漏れ (EJBROLE missing)**: Application で `@RolesAllowed` 指定したのに RACF EJBROLE class profile 未定義 → 403 Forbidden。**現場対処**: EJBROLE profile を `RDEFINE EJBROLE app1.role1 UACC(NONE)`, `PERMIT app1.role1 CLASS(EJBROLE) ID(userid)` で必ず定義、Liberty server.xml の `safRoleMapper` 設定確認。
- **AT-TLS 設定漏れで cleartext 送信**: WAS の HTTP listener (port 9080 等) を AT-TLS で TLS 化のつもりが Policy Agent 起動忘れ → cleartext。**書き手経験**: 監査指摘で発覚、3 ヶ月 cleartext で外部接続してた。**対処**: `pasearch -t` で TLS policy 適用確認、Liberty 内の SSL config (`keyStore`) との二重化検討。
- **zaap-on-zIIP (zIIP offload) で課金誤算**: Java workload は zAAP/zIIP 上で動き General CP 課金外 (sub-capacity)、ただし I/O 系処理は General に戻る。**現場対処**: SMF type 30 の `SMF30CPT` (CP time) / `SMF30AIT` (zAAP time) / `SMF30IIT` (zIIP time) を分けて集計、SCRT に正しく反映。
- **Connector type 2 vs type 4 の認識違い**: Db2 type 2 (JCC T2) は SAF auth + RRS 経由 2 PC + LPAR 内のみ高速。type 4 (T4 driver) は DRDA / TCP/IP 経由 cross-LPAR 可能だが auth は手動配布。**書き手経験**: type 2 想定で書いた app を別 LPAR から接続させようとして fail、driver type 設計時に再確認必須。
- **Profile dir の zFS aggregate fill**: Profile / logs が USS の zFS に置かれ、log rotate 不足で aggregate 100% → server hang。**対処**: SystemOut.log のローテート設定、zFS `aggrgrow` 設定、定期 monitor (`df -k /u/wasuser`)。

## 6. examples（具体例）

```
* WLM Application Environment (WAS Full)
APPLENV   APPENV1
   Description: APP1 servant
   Subsystem type: CB
   Procedure: BBOS001
   Start parameters: IWMSSNM=&IWMSSNM,JOBNAME=BBOS001
   Limit on starting server address spaces: 10
```

```
* WAS Controller STC (BBOC001)
//BBOC001  PROC ENV=AppSrv01.cell.node,PARMS='-DIDENT=cr'
//BBOCTL   EXEC PGM=BBOMINIT,REGION=0M,TIME=NOLIMIT,
//             PARM='TRAP(ON,NOSPIE)/&ENV &PARMS'
//STEPLIB  DD DISP=SHR,DSN=BBO.SBBOEXP
//         DD DISP=SHR,DSN=BBO.SBBOLPA
//SYSOUT   DD SYSOUT=*
//CEEDUMP  DD SYSOUT=*
```

```
* Liberty server.xml 抜粋 (z/OS)
<server description="App1 Liberty for z/OS">
  <featureManager>
    <feature>jakartaee-10.0</feature>
    <feature>zosTransaction-1.0</feature>
    <feature>zosSecurity-1.0</feature>
    <feature>zosConnect-2.0</feature>
  </featureManager>

  <httpEndpoint id="defaultHttpEndpoint"
                host="*" httpPort="9080" httpsPort="9443">
    <sslOptions sslRef="defaultSSLConfig"/>
  </httpEndpoint>

  <keyStore id="defaultKeyStore"
            location="safkeyring://WASUSER/LIBKEYRING"
            type="JCERACFKS" password="password"/>

  <safRegistry id="saf"/>
  <safCredentials profilePrefix="BBGZDFLT"/>
  <safAuthorization id="saf"/>
  <safRoleMapper id="safRoleMapper"
                 profilePattern="%profilePrefix%.%resource%.%role%"/>

  <dataSource id="ds1" jndiName="jdbc/app1">
    <jdbcDriver libraryRef="db2jcc"/>
    <properties.db2.jcc serverName="localhost" portNumber="0"
                        databaseName="DSN1" driverType="2"/>
  </dataSource>
</server>
```

```
* RACF EJBROLE profile setup
RDEFINE EJBROLE BBGZDFLT.app1.appuser UACC(NONE)
PERMIT BBGZDFLT.app1.appuser CLASS(EJBROLE) ID(WASGROUP) ACCESS(READ)
SETROPTS RACLIST(EJBROLE) REFRESH
```

```
* operator command
D WLM,APPLENV=APPENV1            <- APPLENV 状態
D OMVS,A=*                       <- Java process (USS)
F BBOC001,DUMP                   <- controller dump
P BBGZSRV                        <- Liberty stop
S BBGZSRV                        <- Liberty start
```

## 7. decision_axes（採否を分ける判断軸）

- **WAS Full (Traditional) vs Liberty**: **Full** (v9) は legacy app の Java EE 7 完全対応、運用 know-how 充実だが MIPS 高・config 複雑。**Liberty** は軽量、現代的 (MicroProfile, Jakarta EE)、起動秒単位、cloud-native 親和性。**選定基準**: 既存 app の Java EE 仕様、運用チーム skill、cloud 連携 (zCX 等)。新規は Liberty 一択。
- **Controller/Servant 分離 vs Liberty 単一**: **分離** は WLM dispatching + servant fail-over で耐障害性高、ただし 2 region 分の overhead。**単一 (Liberty)** はシンプル、ただし JVM 落ちると即 outage。**選定基準**: HA 要件、運用負荷、Liberty cluster 構成検討。
- **Connector: type 2 vs type 4**: **type 2** (in-LPAR、RRS 2 PC) は最高速 + atomic transaction、LPAR 内限定。**type 4** (DRDA over TCP/IP) は network 越え可能 + ops 統一、性能落ちる + 2 PC は XA。**選定基準**: 配置 (同 LPAR か別か)、transaction 要件、network レイテンシ許容。
- **Auth: SAF integration vs JEE standard**: **SAF integration** は RACF EJBROLE で z/OS と統一管理、CRACK proof 強だが Linux 移行で work しない。**JEE standard** (LDAP / file registry) は portable だが z/OS 独自機能未活用。**選定基準**: アプリ portability、運用統一性、auth 複雑度。
- **Logs: SystemOut.log vs SMF / SYSLOG**: **SystemOut.log** (USS file) は dev 慣れた形式、grep 可能だが分散。**SMF type 120** (WAS audit) は z/OS 統一監査、運用親和性高だが解析 tooling 必要。**選定基準**: 監査要件、log 集約 (Splunk 等) 統合方針。

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_TECH_002) から WAS for z/OS servant region 設計の運用知識を概念蒸留 (ADR-0109)。書籍は概念補助。
