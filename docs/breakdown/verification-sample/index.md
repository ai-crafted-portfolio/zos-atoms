# 検証手順サンプル 50 件

**全件数**: 50 技術項目（うち 19 件に実コンソールセッション再現の検証手順を収録）

実際のコンソール画面の雰囲気を再現した検証手順サンプルです。コマンド入力・応答メッセージ・パネル遷移を含みます。

## 対象技術項目 50 件

???+ note "技術項目一覧 （50 件）"

    | 連番 | 大分類 | 中分類 | 技術項目 | 内容説明 | 出典 |
    |---:|---|---|---|---|---|
    | 5082 | Tivoli NetView z/OS 自動化 | Assembler 拡張 | Abend Code | NetView の Assembler 拡張で使用するサービスマクロの戻りコードと ABEND の扱い。多くの NetView サービスマクロは START でアタッチされたタスク下でのみ使用可能で、DSIFIND マクロでは戻り値 32=マクロ呼び出し無効/アセンブリエラー、36=指定 NAME 未検出 を返す。 | NV |
    | 5463 | Tivoli NetView z/OS 自動化 | NetView Pipes | PIPE MEMLIST | PIPE MEMLIST ステージは PDS のメンバ一覧を取得する。MEMLIST DSIPARM A* のように接頭文字マスクで絞り込み可能で、MEMLIST USER.INIT のように完全データセット名指定も可。エラー時は DWO970I メッセージで戻りコードを示す。 | NV |
    | 5844 | Tivoli NetView z/OS 自動化 | NetView コマンド | LOADTBL (AON) | LOADTBL (同義語 LOAD) は AON のオプション定義テーブルの共通グローバル変数を再初期化する。CNMSTYLE で AON タワー有効化が前提。1 回の発行で 1 テーブルのみ再ロード可能で、複数テーブルは複数回発行。テーブル名は EZLTABLE (AON Base) / FKVTABLE (AON/SNA) / FKXTABLE (AON/TCP) / user 作成テーブル。 | NV |
    | 6225 | Tivoli NetView z/OS 自動化 | PL/I / C 拡張 | Parsing input string in CNMSCAN | CNMSCAN は PL/I 専用の文字列パース/変換サービス (CNMSSCAN は別名)。入力文字列を左から右へ走査し format 文字列の指定に従い最大 10 個の受信変数へ抽出値を代入する。受信変数は varying length character として宣言。format 指定子に合致しない/入力終端で戻る。 | NV |
    | 6606 | Tivoli NetView z/OS 自動化 | RODM / GMFHS | Tasks Best Performed with Methods | GMFHS 監視対象のリソースは RODM ロード関数文と GMFHS データモデルで定義する。DUIFFAWS メソッドは RODM データキャッシュ内の status aggregation フィールドを初期化し、起動時/RODM 接続復旧時/CONFIG NETWORK 処理時に実行される。GMFHS 起動 PROC で AGGRST=NO で無効化可能。 | NV |
    | 6987 | Tivoli NetView z/OS 自動化 | インストール / 構成 | Defining the NMCSTATUS Policy Autotask | NMCSTATUS Policy 定義は DSIPARM メンバに記述。NMCSTATUS は大文字で 1 桁目から開始、継続行は 2 桁目以降、policy 名は一意、キーワードは順不同・重複不可。BLDVIEWSSPEC/COLLECTIONSPEC/TIME 値内に空白埋め込み不可。違反時は DUI262E (RESOURCE と MYNAME 同時指定不可) などで通知。 | NV |
    | 7368 | Tivoli NetView z/OS 自動化 | インストール / 構成 | Starting the Topology Server | Topology Server は Windows サービスとして導入可能。account_name は DomainName\UserName 形式 (ローカルは .\UserName)。Topology Server + Topology Comms Server の 2 サービスが導入され startup は manual。tserver config で daemon 化や heartbeat 設定。 | NV |
    | 7749 | Tivoli NetView z/OS 自動化 | セキュリティ (SAF 連携) | Scenario 1: Migrating from a System with No Security | セキュリティ未設定からの移行手順。CNMSTYLE の SECOPTS 文を確認し、NetView 側 / SAF 製品 (RACF 等) 側のどちらで管理するか方針決定。コマンド権限チェックには NetView 提供サンプル CNMSCAT2 と CNMSAF2/CNMSAFPW を利用可能。 | NV |
    | 8130 | Tivoli NetView z/OS 自動化 | トラブルシューティング | RECFMS header | AON/SNA でリソース回復イベントを処理するメッセージ群の文脈で扱われる SNA RECFMS データ。リンクステーション接続検知時 IST464I が出力され、NCP の LOAD/DUMP 失敗時は FKV501I/FKV502I で通知される。EZL504I は AON/SNA で利用可能 (AVAILABLE) 状態のリソース通知。 | NV |
    | 8511 | Tivoli NetView z/OS 自動化 | ユーザーズガイド (操作) | Customizing the NetView Management Console Topology Server | NetView Management Console Topology Console のカスタマイズ。トポロジコンソールアイコン/背景/ヘルプ等の基本カスタマイズと、見た目・機能を変える高度なカスタマイズの 2 段階。 | NV |
    | 8892 | Tivoli NetView z/OS 自動化 | ユーザーズガイド (操作) | Stack Situations | IP リソース (IP スタック/ホスト/インタフェース/ルータ/TN3270 サーバ) のプロアクティブ監視機能。ルータの性能 MIB をクエリし閾値超過時に AON/TCP が通知。本機能は NetView 本体に取込済で AON/TCP 不要。IP コネクション監視・閾値判定もサポート。 | NV |
    | 9273 | Tivoli NetView z/OS 自動化 | 管理リファレンス | FULLSESS | AON コマンド名 (例: ACTMON/AHED/ANO/AON/AONAIP 等) と SAF Resource または Command Authorization Table 識別子 (例: netid.luname.EZLE0000) との対応の枠組み。 | NV |
    | 9654 | Tivoli NetView z/OS 自動化 | 管理リファレンス | TCPCONN.PDDNM | TCPCONN.PDDNM 文は TCP/IP 接続管理の主データセット DD 名を 1-8 文字で指定する (デフォルト DSITCONP)。NetView 開始時に DD で指定し VSAM 経由で利用。複数 DSTINIT 文がある場合は少なくとも 1 度指定する必要がある。 | NV |
    | 10045 | Z System Automation (TSA) | Workload Scheduler 連携 | Automated Recovery Functions | Workload Scheduler の自動回復は事前に依存関係を持つ回復アプリケーションを TWS に定義 (但しスケジュールはしない)。バックアップサイトでの critical app 回復決定時に通常 TWS パネルで current plan を変更し最初の回復アプリをスケジュール。手動 workstation で手順/JCL 修正をオペレータに提示。 | TSA |
    | 10171 | Z System Automation (TSA) | エンドツーエンド自動化 | Examples | End-to-End Automation で SA z/OS が実装するリソースデータモデルの例。DSIPARM 内 INGXINIT を LISTA で参照しリモートドメインのリソースとの関連を把握する。INGXINIT で PPI=YES に設定して PPI 通信を有効化、サンプル JCL INGXADPT を ING.SINGSAMP からコピーして JCL シンボル DIRI/DIRC をカスタマイズする。 | TSA |
    | 10297 | Z System Automation (TSA) | オペレータコマンド | DISPMTR | DISPMTR は MTR (Monitor Resource) の health 状態と詳細を表示する。各 monitor command は ①データ収集 ②return code (1-8) 設定 ③DISPMTR 表示用メッセージ追加 ④終了の基本ステップ。F キーで INGINFO 表示、A=ハードリセット要求、B=リフレッシュ要求。 | TSA |
    | 10423 | Z System Automation (TSA) | オペレータコマンド | SETHOLD | SETHOLD は AOF メッセージのうちどの種別を自分のオペレータ ID 用に hold するかを選択する。CONFIG は自動化制御ファイル設定に合わせる、AUTO は automation に従う、i/a/e/d/w で各種別 (information/action/eventual/decision/wait) を個別指定可能。OST タスクでのみ有効、NNT/RMT では無効。AUTO 以外では INGNTFY globals を更新しない。 | TSA |
    | 10549 | Z System Automation (TSA) | カスタマイズ / プログラミング | Define Specific Timeout Values | リソース個別の timeout 値定義。TIMEOUT パラメータで秒指定 (最大 999、省略時 30 秒)。E2E では INGREQ_WAIT/INGSET_WAIT/INGLIST_WAIT といった AAO (Advanced Automation Option) で最小値を制御、未設定なら 30 秒。共通グローバル変数で運用調整可能。 | TSA |
    | 10675 | Z System Automation (TSA) | カスタマイズ / プログラミング | Resource Lifecycle | リソースは観察状態 (Observed) と希望状態 (Desired) を持ち、SA z/OS は希望状態に向け開始/停止を agent に指示する。MTR リソースは健康状態で観察し、suspended 状態では agent/MTR 双方 2 値のみのライフサイクルモデルへ縮退する (UP/DOWN, AVAILABLE/SOFTDOWN 等)。 | TSA |
    | 10801 | Z System Automation (TSA) | プログラマーズリファレンス | DATETIME | TWS Programmer's Reference / Operator's Guide で扱われる日時関連のサービス。INGEXEC コマンドのフレームワーク内で扱われ CATEGORY/SUBCAT/DESCR/STATUS/OBSERVED/DESIRED/AUTOSTAT/COMPOUND/HEALTH のステータスタイプを操作可能。 | TSA |
    | 10927 | Z System Automation (TSA) | プロダクト自動化プログラミング | Critical Event Monitoring | Product Automation (CICS/DB2/IMS) を SA z/OS で監視/制御する枠組み。ローカル/リモート region を一元的に監視・制御するための customization と operation を扱う。INGOMX で OMEGAMON コマンド最大 22 件を default SAFE 経由で渡せる。 | TSA |
    | 11053 | Z System Automation (TSA) | ユーザーズガイド | Displaying and Setting Events | DISPEVTS は Sysplex 内に定義された全イベントを表示するフルスクリーンパネル。SET (白) / UNSET (赤) / 不明 (UNSET 扱い) を区別し、パネルから set/reset 操作と関連リソース表示が可能。INGEVENT で個別イベントを変更し、共通グローバル DISPEVTS_WAIT で WAIT 値を制御可能。 | TSA |
    | 11179 | Z System Automation (TSA) | 概要 / 開始 | Getting help | SA z/OS の入門情報。製品 introduction (Get Started Guide) と Product Automation Programmer's Guide が参照点で、各リソースの希望状態に基づき agent が起動/停止を行う設計思想を解説。 | TSA |
    | 11305 | Z System Automation (TSA) | 自動化ポリシー定義 | Defining Data Sets for Batch Processing | Build/Migrate のバッチオプションを使うため、batch processing 用データセット名を customization dialog の Settings Menu で定義する。これらの名前は batch ジョブ JCL の DD concatenation に組み込まれる。入力パラメータには target/source policy database 名・データセット名・entry name/type、移動対象 string / 置換 string リスト等。 | TSA |
    | 11431 | Z System Automation (TSA) | 自動化ポリシー定義 | Policy Items for Remote Domains | Remote Domains entry type は E2E 自動化スコープにあるリソースが動作する遠隔ドメイン (例: z/OS sysplex) を定義する。Policy items として DESCRIPTION / DOMAIN INFO / REFERENCES / WHERE USED があり、REFERENCES では遠隔リソース参照を選択/解除可能。 | TSA |
    | 11557 | Z System Automation (TSA) | 計画 / インストール | Hardware Management Console characteristics | HMC は processor hardware LAN に接続可能でハードウェア LAN 内の CPC オブジェクトの単一制御点となる。SE/HMC の Console Integration (CI) 機能で OS へのコマンド送信とメッセージ受信を行う。HWMCA は SE/HMC 上の licensed app で GUI と自動化 IF を提供、BCPii/SNMP 接続が利用する。 | TSA |
    | 11689 | GDPS 災害対策・サイトスイッチ | Active-Active 概要・計画 | Active/Active site configuration options | GDPS Active/Active は理論的に無制限の距離にある 2 以上のサイトで同一アプリ/データを並行稼働、サイト間ワークロード負荷分散と継続可用性を提供。実装は target site sysplex のセットアップから開始 (secondary site は後追い可)。SASP-compliant routing と software replication を伴う。 | GDPS |
    | 11778 | GDPS 災害対策・サイトスイッチ | Active-Active 概要・計画 | NetView Web Application requirements | GDPS Active/Active の UI は NetView Web Application 経由のみ (3270 不可)。Web App を Windows/AIX/Linux 上に配置し、各サイトに少なくとも 1 インスタンス置いて HA を確保する。詳細サポート OS/ブラウザは NetView V6R2 DVD の readme znetview_webapp_readme_en.htm を参照。 | GDPS |
    | 11867 | GDPS 災害対策・サイトスイッチ | DS8000 Copy Services | Consistency group function | DS8000 CG 機能の運用。chrcconsistgrp -consistencyfreeze H2:H4 で CG 整合性をフリーズし、chrcconsistgrp -failover H3:H1 で H3 を primary 昇格する手順を含む。GM 関係が idle のとき FlashCopy 発行可能で、CG 形成中なら停止後に FlashCopy が確立される。 | GDPS |
    | 11956 | GDPS 災害対策・サイトスイッチ | DS8000 Copy Services | FlashCopy | FlashCopy はバックアップを高速確立する point-in-time コピー。mkflash で確立、rmflash で関係解消。in-band で remote storage へは rmremoteflash。dscli> mkflash -nocp -tgtse -persist 0111:0110 で 'CMUC00137I mkflash: FlashCopy pair 0111:0110 successfully created.'。 | GDPS |
    | 12045 | GDPS 災害対策・サイトスイッチ | DS8000 Copy Services | Interfaces | GDPS Virtual Appliance / GDPS Metro の管理 UI として GDPS GUI (ブラウザベース) と 3270 パネルが提供される。GDPS GUI は Remote Copy Management、Standard Actions、Sysplex Resource Mgmt、SDF Monitoring、CANZLOG 参照を point-and-click で操作可能。GDPS Enterprise Portal で複数 GDPS 環境を統合可視化。 | GDPS |
    | 12134 | GDPS 災害対策・サイトスイッチ | DS8000 Copy Services | Outage at H2 | H1 (production) 障害/計画停止時、MM + GM 構成では MM secondary H2 へ swap 可能。計画フェイルオーバではアプリ停止後に H2/H3 で recovery 開始しボリュームをホストに割り当てアプリ起動。H1 で計画保守を実施する場合は H2 への recovery が production 影響最小化。MM H1-H2 は H2 復旧後再開で MM 保護回復。 | GDPS |
    | 12223 | GDPS 災害対策・サイトスイッチ | DS8000 Copy Services | Returning the production environment from H3 to H1 | 回復サイトで運用後に primary に戻す手順。非対称 GM 構成では Global Copy で戻すため逆方向 DR 保護なし → 長時間 secondary 運用は想定外。標準は ①Failover で secondary を host 利用可能化 ②H1 復旧後 Failback で逆方向 mirroring 再確立。MGM 3 サイトでは Region A→B の切替と return home が可能。 | GDPS |
    | 12312 | GDPS 災害対策・サイトスイッチ | DS8000 Copy Services | Using FlashCopy for DEFRAG | DFSMSdss DEFRAG コマンドは FlashCopy 機能と組合せ高速にデータセット extent を再配置する。FASTREPLICATION(REQuired) or (PREFerred、デフォルト) を指定。MM/GM ミラー対象ボリュームでは FCTOPPRCPrimary パラメータも必要で、MM primary なら Remote Pair FlashCopy も可。 | GDPS |
    | 12401 | GDPS 災害対策・サイトスイッチ | DS8000 Global Mirror ベストプラクティス | Setting up a Global Mirror session | Global Mirror は secondary site で CG を形成する。primary site の LSS に start コマンドを発行し master storage system と master LSS を設定、以降の session 関連コマンドはこの master LSS 経由で行う。start で CG 形成イベント連鎖が開始される。 | GDPS |
    | 12490 | GDPS 災害対策・サイトスイッチ | GDPS Family 概要 / 機能 | GDPS GM Copy Once facility | Copy Once は recovery 用だが内容が critical でない (常時 mirror 不要な) ボリュームの初期コピーと再作成を提供する。Page data sets や Sort 等の temp 作業 volume が典型例。Copy Once 対象 volume には継続レプリケート必須データを置かないことが前提。 | GDPS |
    | 12579 | GDPS 災害対策・サイトスイッチ | GDPS Family 概要 / 機能 | Maximizing application availability | GDPS Continuous Availability は RTO/RPO 観点で application 可用性を最大化するソリューション。複数 GDPS 製品の連携で monitoring と management を行い、同一 sysplex 上に Continuous Availability と他 workload を共存させる構成も扱う。 | GDPS |
    | 12668 | GDPS 災害対策・サイトスイッチ | Metro/Global Mirror Incremental Resync | z/OS Metro/Global Mirror | z/OS Metro/Global Mirror は multi-target 3 サイトソリューションで Metro Mirror と z/OS Global Mirror (XRC) の組合せ。incremental resync support を加えた構成とその HyperSwap 拡張 (RMZ Resync) で耐障害性を高める。 | GDPS |
    | 12762 | IBM MQ メッセージング | MQ Explorer | Adding an initial context | MQ Explorer で JMS オブジェクトを管理するには JNDI namespace のルートを表す initial context を追加する必要がある。各 JNDI namespace ごとに 1 つ追加し、JMS Administered Objects フォルダに表示。ニックネーム編集や 'Connect immediately on finish' チェックでウィザード閉時の自動接続を選択可能。 | MQ |
    | 12845 | IBM MQ メッセージング | MQ Explorer | Using MQ Telemetry | MQ Telemetry (MQTT) を MQ Explorer から利用。Telemetry フォルダから MQTT Client Utility を起動し、対象 telemetry channel を右クリックで Launch MQTT Client Utility 経由でテスト。前提条件は telemetry (MQXR) サービスと telemetry channel が稼働中。 | MQ |
    | 12928 | IBM MQ メッセージング | MQSC / PCF / 管理 | Stopping MQI channels | STOP CHANNEL を server-connection channel に発行する際 client-connection channel の停止方法を選択可能。MODE オプションは QUIESCE (current batch 終了後停止 / デフォルト)、FORCE (即停止, 再開時 resync 必要)、TERMINATE (停止 + 関連プロセス終了)。MQIS_YES オプションで停止状態に関わらずコマンド成功、MQIS_NO (default) なら既に停止中はエラー (MQRCCF_CHANNEL_DISABLED)。 | MQ |
    | 13011 | IBM MQ メッセージング | アプリ開発 (MQI / JMS) | Introduction to the IBM MQ custom channel for WCF with .NET | Developing Applications for IBM MQ で扱われる custom services 全般のリファレンス。Requestor/Server オブジェクトを基本に独自サービスをアプリ統合する。詳細は同マニュアル各章を参照。 | MQ |
    | 13094 | IBM MQ メッセージング | セキュリティ (CHLAUTH / TLS) | Configuring SSL or TLS between the Connect:Direct bridge agent and the Connect:Direct node | QM 間 TLS は ①QM で使用するデジタル証明書を管理 ②QM を TLS-enabled messaging 用に構成 ③channel 定義で SSLCIPH を指定、の手順。両端で trust が正しく構成されていないと 2393 MQRC_SSL_INITIALIZATION_ERROR が発生。SSLCAUTH(REQUIRED) でクライアント証明書必須化、TLS 1.2/1.3 (MQSECPROT_TLSV12/13) 推奨。 | MQ |
    | 13177 | IBM MQ メッセージング | セキュリティ (CHLAUTH / TLS) | Subscription security | publish/subscribe のアクセス制御は admin topic object のセキュリティ属性 (subscribe/publish 操作の許可ユーザ/グループ) で行う。subscription 位置に該当する topic object がない場合、最も近い親 admin topic object 名でセキュリティプロファイルが検査される。setmqaut で allmqi (browse/connect/get/inq/pub/put/resume/set/sub) を一括付与可能、alladm (chg/clr/dlt/dsp/ctrl/ctrlx) で管理権限。 | MQ |
    | 13260 | IBM MQ メッセージング | 全般リファレンス | Administration reference PDF | IBM MQ のリファレンス情報は mq93.reference.pdf に集約され、管理関連は mq93.refadmin.pdf に分離 (2021年5月以降)、構成関連は mq93.refconfig.pdf に分離。MQSC コマンドの詳細運用は Administering IBM MQ using MQSC commands を参照。runmqsc コマンドプロンプトでインタラクティブに MQSC 実行可能。 | MQ |
    | 13343 | IBM MQ メッセージング | 構成 (QM / Queue / Channel) | Additional configuration options for IBM MQ Bridge to Salesforce | MQ Explorer で QM セットを管理する追加構成。Automatic sets で関連 QM を自動的にメンバ追加、フィルタで自動 set のメンバシップを管理。手動 set では QM の追加/削除を手作業で行い、ドラッグで set 間移動も可能。既存 set のコピーで新 set 作成も支援。 | MQ |
    | 13426 | IBM MQ メッセージング | 構成 (QM / Queue / Channel) | High availability configurations | Multi-instance QM は active/standby ペアでフェイルオーバ可能 (合計 2 インスタンス、standby 2/active 1 は不可)。共有ストレージ前提で MQ 標準機能。strmqm -x で standby 起動、endmqm -x で standby 停止 (active 継続)、endmqm (-x なし) で active 停止し standby が active 昇格可能。HA cluster より構成簡単、Explorer 統合あり、フェイルオーバ高速。 | MQ |
    | 13509 | IBM MQ メッセージング | 管理リファレンス | IBM MQ Administration Interface reference | MQAI は AIX/IBM i/Linux/Windows で利用可能な MQ 管理タスク用プログラミング IF。PCF を扱うためのプログラミング IF で、command server を直接扱う代わりに PCF メッセージを easier に送受信できる。詳細利用法は IBM MQ Administration Interface reference を参照。 | MQ |
    | 13592 | IBM MQ メッセージング | 開発リファレンス | CCSID | MQ 9.0 以降は Unicode 8.0 標準の全文字を data conversion でサポート (UTF-16 含む)。ccsid_part2.tbl 利用推奨。CCSID 1388/1390/1399/4933/5488/16884 では Unicode supplementary planes へのマッピングを含む全 code points をサポート。1390/1399/16884 は JIS X 0213 (JIS2004) 文字含む。MQCCSI_DEFAULT は QM の CCSID を使用、MQCCSI_Q_MGR は実際の QM CCSID に変換。 | MQ |
    | 13675 | IBM MQ メッセージング | 開発リファレンス | MQAuthenticationInformationRecord.NET class | MQAuthenticationInformationRecord は IBM MQ TLS client 接続で使用する認証情報を指定するクラス、MQAIR 認証情報レコードをカプセル化。AuthInfoRecPtr/AuthInfoRecOffset で参照、値不正で MQRC_AUTH_INFO_REC_COUNT_ERROR。MQADPCTX_NO 設定で認証は実施するが credentials を採用しない (authorization は app 実行ユーザ ID で実施)。 | MQ |

## 検証手順（コンソールセッション再現）

### VRF-001 — PIPE MEMLIST

**分類**: Tivoli NetView z/OS 自動化 ／ NetView Pipes

**検証目的**: PIPE MEMLIST ステージが指定 PDS/DD のメンバ一覧を取得できることを確認 (接頭マスク絞込・複数 DD 連結対応含む)。

```text
NCCF        Tivoli NetView           USER1            06/15/26 09:30:15
- DOMAIN: CNM01
- USER1   IS LOGGED ON IN PRIMARY POS
?

* USER1   PIPE NETV MEMLIST DSIPARM | CONS
  DSI020I MEMLIST PROCESSING STARTED
  A        1
  ABCMEM   1
  A        10
  DSIPARM  3 MEMBERS LISTED

* USER1   PIPE NETV MEMLIST DSIPARM A* | CONS
  A        1
  ABCMEM   1
  A        10
  DSIPARM  3 MEMBERS LISTED (FILTER=A*)

* USER1   PIPE NETV MEMLIST USER.INIT | CONS
  (USER.INIT 配下全メンバの一覧)

* USER1   PIPE (END ;) a: MEML USER.INIT | CONS ONLY; a:| COLOR YEL | CONS
  (黄色着色で再出力 → カラー指定 PIPE 構文の確認)

   --- 異常時 ---
* USER1   PIPE NETV MEMLIST NONEXIST.DSN | CONS
  DWO970I MEMLIST FAILED RC=N    ← 戻りコードは NetView online help 参照
```

**前提条件**: 【前提】NetView オペレータコンソールでログオン済。MEMLIST/MEML は LIST 系で常時利用可。

**プレースホルダ**: 【プレースホルダ】[DSN]=対象 PDS のデータセット名 (例: SYS1.PARMLIB) または NetView 起動 PROC 内 DD 名 (例: DSIPARM, DSIVTAM)

**記録項目**:

- ① 実行コマンド全文 (PIPE NETV MEMLIST [DSN] | CONS)
- ② 出力メンバ数とサンプル先頭/末尾行
- ③ 接頭マスク (A*) 適用時のヒット件数
- ④ DWO970I エラー有無と (出た場合) 戻りコード
- ⑤ 実行時刻 / オペレータ ID / 対象 NetView ドメイン

### VRF-002 — LOADTBL (AON)

**分類**: Tivoli NetView z/OS 自動化 ／ NetView コマンド

**検証目的**: LOADTBL コマンドが指定 AON option definition table を再ロードし共通グローバル変数を再初期化することを確認。

```text
NCCF        Tivoli NetView           USER1            06/15/26 09:30:15
- DOMAIN: CNM01

* USER1   LIST TOWER
  EZL023I AON TOWER STATUS:
    AON.BASE                    ENABLED
    AON.SNA                     ENABLED
    AON.TCP                     ENABLED
  EZL025I END OF DISPLAY

* USER1   AON 1.8.6
   EZLK8600                    AON: Loader Tables                     CNM01
   Type one or more action codes. Then press enter.                   More:
     1=Browse 2=Reload
       Type       Table       Description                         Status
    _  AON        EZLTABLE    AON Base                            Loaded
    _  SNA        FKVTABLE    AON SNA Automation                  Loaded
    _  TCPIP      FKXTABLE    AON TCP/IP Automation               Loaded
    _             ________
    Command ===>
    F1=Help      F2=Main Menu   F3=Return                  F5=Refresh    F6=Roll
    F7=Backward  F8=Forward                                             F12=Cancel

* USER1   LOADTBL EZLTABLE
  EZL048I EZLTABLE HAS BEEN RELOADED                  ← 一次資料 部分一致: 本文は推定形式

* USER1   AON 1.8.6
   EZLK8600                    AON: Loader Tables                     CNM01
       Type       Table       Description                         Status
    _  AON        EZLTABLE    AON Base                            Reloaded  ← 反映確認
    _  SNA        FKVTABLE    AON SNA Automation                  Loaded
    _  TCPIP      FKXTABLE    AON TCP/IP Automation               Loaded
    Command ===>
```

**前提条件**: 【前提】CNMSTYLE 内で TOWER.AON.* が有効化済。LOADTBL は NetView OPER 権限で実行可能。

**プレースホルダ**: 【プレースホルダ】対象テーブル名は固定: EZLTABLE/FKVTABLE/FKXTABLE/[USER_TABLE]。[USER_TABLE]=サイト独自定義テーブル名

**記録項目**:

- ① LIST TOWER 結果 (AON タワー ENABLED 確認)
- ② AON 1.8.6 パネル 実行前 Status (Loaded)
- ③ 実行コマンド: LOADTBL [TABLE_NAME]
- ④ EZL048I 受領時刻 + 完全メッセージ本文
- ⑤ AON 1.8.6 パネル 実行後 Status (Reloaded)
- ⑥ 失敗時の戻りメッセージ ID

### VRF-003 — Defining the NMCSTATUS Policy

**分類**: Tivoli NetView z/OS 自動化 ／ インストール / 構成

**検証目的**: NMCSTATUS Policy 定義 (DSIPARM メンバ) が NetView 解釈可能で NMC コンソール状態管理に反映されることを確認。

```text
--- DSIPARM(NMCPOL01) を ISPF 3.4 で編集 ---
EDIT       USER1.DSIPARM(NMCPOL01) - 01.00                    Columns 00001 00072
Command ===> SAVE                                              Scroll ===> CSR
****** ***************************** Top of Data ******************************
000001 NMCSTATUS POLICY=POL01,RESOURCE=NETRES01,
000002           TIME=(05.00.00,06.00.00),BLDVIEWSSPEC=YES
****** **************************** Bottom of Data ****************************

   --- NetView コンソールで REFRESH ---
NCCF        Tivoli NetView           USER1            06/15/26 10:05:42
- DOMAIN: CNM01

* USER1   LISTSTATEMGR REFRESH MEMBER=NMCPOL01
  DUI260I POLICY POL01 LOADED SUCCESSFULLY            ← 一次資料 部分一致: 本文は推定形式

* USER1   D NMCSTATUS,POLICY=POL01
  POL01 DEFINITION:
    RESOURCE      = NETRES01
    TIME          = (05.00.00,06.00.00)
    BLDVIEWSSPEC  = YES
  END OF DISPLAY

   --- 異常時 (RESOURCE + MYNAME 同時指定) ---
EDIT       USER1.DSIPARM(NMCPOL01)
000001 NMCSTATUS POLICY=POL01,RESOURCE=NETRES01,MYNAME=XYZ,
000002           TIME=(05.00.00,06.00.00)

* USER1   LISTSTATEMGR REFRESH MEMBER=NMCPOL01
  DUI262E POL01: ONLY ONE OF THE FOLLOWING KEYWORDS IS ALLOWED FOR THIS
  POLICY DEFINITION IN MEMBER NMCPOL01: RESOURCE OR MYNAME    ← 一次資料 記載どおり
```

**前提条件**: 【前提】DSIPARM ライブラリ更新権限、NetView 再起動 (or LISTSTATEMGR REFRESH) 可能。

**プレースホルダ**: 【プレースホルダ】[NMCSTAT]=DSIPARM メンバ名 (1-8 文字)、[POLNAME]=ポリシー名 (一意)、[RESID]=NMC で扱うリソース名

**記録項目**:

- ① DSIPARM([NMCSTAT]) メンバ全テキスト (Save 後)
- ② LISTSTATEMGR REFRESH MEMBER=[NMCSTAT] 出力 (DUI260I)
- ③ D NMCSTATUS,POLICY=[POLNAME] の RESOURCE/TIME 値
- ④ DUI262E/DUI258I 等の構文エラー有無
- ⑤ NMC コンソール反映確認 (画面キャプチャ)

### VRF-004 — Starting the Topology Server

**分類**: Tivoli NetView z/OS 自動化 ／ インストール / 構成

**検証目的**: Topology Server (Windows サービス) のインストール・起動・daemon 化・heartbeat 設定が完了しトポロジコンソールから接続できることを確認。

```text
C:\Program Files\IBM\NetView\bin> tserver service .\Administrator P@ssw0rd
Tivoli NetView Topology Server service installed successfully.
Tivoli NetView Topology Communications Server service installed successfully.
Startup type: Manual

C:\Program Files\IBM\NetView\bin> sc query "Tivoli NetView Topology Server"

SERVICE_NAME: Tivoli NetView Topology Server
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 1  STOPPED
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x0

C:\Program Files\IBM\NetView\bin> net start "Tivoli NetView Topology Server"
The Tivoli NetView Topology Server service is starting...
The Tivoli NetView Topology Server service was started successfully.

C:\Program Files\IBM\NetView\bin> tserver config -d -h 30 -f 0.0.0.0
Config saved:
  daemon mode        = YES
  heartbeat interval = 30 sec
  bind address       = 0.0.0.0

   --- Topology Console (GUI) から接続 ---
   [Server hostname] tserver-host.example.com
   [Port]            4007
   [Connect] → Status: Connected
   Welcome to NetView Management Console
```

**前提条件**: 【前提】Windows サーバに NetView Topology Server 導入媒体配置済、管理者権限ユーザでログオン。

**プレースホルダ**: 【プレースホルダ】[PASSWORD]=Administrator のパスワード。ドメイン参加時は .\Administrator を DOMAIN\Administrator に置換

**記録項目**:

- ① tserver service コマンド実行結果 (2 サービス導入確認)
- ② sc query 出力 (SERVICE_NAME / STATE)
- ③ net start 完了メッセージと起動時刻
- ④ tserver config -d -h 30 設定値 (daemon 化 / heartbeat)
- ⑤ Topology Console 接続成功スクリーンショット
- ⑥ 失敗時の Windows イベントログ抜粋

### VRF-005 — FULLSESS

**分類**: Tivoli NetView z/OS 自動化 ／ 管理リファレンス

**検証目的**: FULLSESS を含む AON コマンド識別子 (netid.luname.EZLE0000 等) の SAF NETCMDS クラス保護が機能することを確認。

```text
--- Security Reference p.217 表より対象 AON コマンドの識別子確認 ---
   Table 12. AON Command Identifiers
    Commands      Command         SAF Resource or Command
    and Synonyms  List Name       Authorization Table Identifier
    ACTMON        EZLE450A        netid.luname.EZLE450A
    AHED          EZLE100A        netid.luname.EZLE100A
    ANO           EZLE000         netid.luname.EZLE0000
    ANOMENU       EZLE000         netid.luname.EZLE0000
    AON           EZLE000         netid.luname.EZLE0000
    AONAIP        EZLESAIP        netid.luname.EZLESAIP

   --- TSO RACF コマンドで保護プロファイル定義 ---
READY
RLIST NETCMDS NET1.CNM01.EZLE0000
ICH13003I PROFILE NETCMDS NET1.CNM01.EZLE0000 NOT FOUND.    ← 一次資料 部分一致: ICH 形式

READY
RDEFINE NETCMDS NET1.CNM01.EZLE0000 UACC(NONE)
ICH10006I RACLISTED PROFILES FOR NETCMDS WILL NOT REFLECT THE ADDITION(S)
UNTIL A SETROPTS REFRESH IS ISSUED.

READY
PERMIT NET1.CNM01.EZLE0000 CLASS(NETCMDS) ID(OPER1) ACCESS(READ)
ICH10006I RACLISTED PROFILES FOR NETCMDS WILL NOT REFLECT THE ADDITION(S)
UNTIL A SETROPTS REFRESH IS ISSUED.

READY
SETROPTS RACLIST(NETCMDS) REFRESH
ICH14063I SETROPTS COMMAND COMPLETE.

   --- NetView OPER1 でログオン後テスト ---
NCCF        Tivoli NetView           OPER1            06/15/26 10:20:30
- DOMAIN: CNM01

* OPER1   ANO
   (AON Main Menu が正常表示)

   --- 権限なしユーザ ---
* OPER9   ANO
  DSI008I COMMAND ANO NOT AUTHORIZED FOR OPER9
```

**前提条件**: 【前提】NetView Security_Reference p.217 の AON Command Identifiers 表で対象コマンドの SAF 識別子を取得済。RACF 権限あり。

**プレースホルダ**: 【プレースホルダ】[NETID]=VTAM NETID、[LUNAME]=NetView LU、[OPER]=対象オペレータ ID

**記録項目**:

- ① RLIST NETCMDS [NETID].[LUNAME].EZLE0000 結果 (UACC / access list)
- ② RDEFINE / PERMIT 実行コマンド全文と ICH10006I 出力
- ③ SETROPTS RACLIST(NETCMDS) REFRESH 実行時刻
- ④ 許可ユーザでの ANO 発行結果
- ⑤ 未許可ユーザでの DSI008I (権限拒否) 出力

### VRF-006 — TCPCONN.PDDNM

**分類**: Tivoli NetView z/OS 自動化 ／ 管理リファレンス

**検証目的**: TCPCONN.PDDNM 文と DD 文の整合により NetView TCP/IP 接続管理 VSAM 主データセットが open でき TCPCONN QUERY が応答することを確認。

```text
--- DSIPARM(DSITINIT) を編集して TCPCONN.PDDNM 追加 ---
EDIT       USER1.DSIPARM(DSITINIT) - 01.04                    Columns 00001 00072
Command ===> SAVE
****** **************************** Top of Data ******************************
000054 TCPCONN.PDDNM=DSITCONP
****** *************************** Bottom of Data ****************************

   --- NetView 開始 PROC (CNMPROC) に DD 文追加 ---
EDIT       USER1.PROCLIB(CNMPROC) - 01.05
Command ===> SAVE
000077 //DSITCONP DD DSN=NETVIEW.DSITCONP,DISP=SHR

   --- システムコンソール ---
S CNMPROC
$HASP100 CNMPROC ON STCINRDR
$HASP373 CNMPROC STARTED
DSI020I NETVIEW STARTED
CNM493I TCPCONN DATA SET OPENED: DSITCONP                ← 一次資料 部分一致

   --- NetView コンソール ---
NCCF        Tivoli NetView           USER1            06/15/26 10:45:12
- DOMAIN: CNM01

* USER1   TCPCONN QUERY
   TCP/IP   Local IP Address          Remote IP Address         State
   TCPCS    10.1.2.3                  10.4.5.6                  ESTABLISHED
   TCPCS    10.1.2.3                  10.4.5.7                  LISTEN
   TCPCS    fd00::1                   fd00::2                   TIME_WAIT

   --- 異常時 ---
   IEF196I OPEN ERROR FOR DSITCONP - DD NAME NOT FOUND
   CNM494E TCPCONN OPEN FAILED FOR DSITCONP                ← 一次資料 部分一致
```

**前提条件**: 【前提】NetView 開始 PROC (CNMPROC) と DSIPARM ライブラリの更新権限あり。VSAM データセット予め定義済。

**プレースホルダ**: 【プレースホルダ】[CNMPROC]=NetView 開始 PROC 名、[NETVIEW]=NetView 製品データセット HLQ

**記録項目**:

- ① DSIPARM 内 init メンバの TCPCONN.PDDNM=[DDNAME] 行
- ② CNMPROC JCL の DD 追加内容 (DSN/DISP)
- ③ NetView 起動メッセージ (DSI020I + TCPCONN init)
- ④ TCPCONN QUERY 出力サンプル (TCP/IP 名 / Local IP / Remote IP)
- ⑤ OPEN FAILED 時の CNM[NNN]E メッセージ全文

### VRF-007 — DISPMTR

**分類**: Z System Automation (TSA) ／ オペレータコマンド

**検証目的**: DISPMTR コマンドが MTR (Monitor Resource) の health 状態 (NORMAL/MINOR/MAJOR/CRITICAL/FATAL/UNKNOWN) と詳細を表示できることを確認。

```text
NCCF        Tivoli NetView           USER1            06/15/26 11:00:00
- DOMAIN: CNM01

* USER1   DISPMTR
   AOFXM1                 Monitor Resource Display          SA z/OS V4.3
   System: SYS1            Date: 06/15/26       Time: 11:00:05
   Cmd  Name           Type      System    Observed   Desired   Health
    _   MTRA           MTR       SYS1      AVAILABLE  AVAILABLE NORMAL
    _   MTRB           MTR       SYS1      SOFTDOWN   AVAILABLE MINOR
    _   MTRC           MTR       SYS2      AVAILABLE  AVAILABLE NORMAL
   Action: A=Hard reset  B=Refresh  F=INGINFO details
   Command ===>
   F1=Help     F3=Return    F5=Refresh    F12=Cancel

* USER1   (MTRA 行に F を入力 → Enter)
   AOFXM2                 INGINFO Detail                    SA z/OS V4.3
   Name           : MTRA
   Type           : MTR
   System         : SYS1
   Observed Status: AVAILABLE
   Desired Status : AVAILABLE
   Auto Status    : IDLE
   Health Status  : NORMAL
   Last collected : 06/15/26 10:59:50
   Command ===>

* USER1   DISPMTR MTRA
   (上記詳細を単一表示)

* USER1   (MTRB 行に B を入力 → Enter → Refresh 要求)
   AOF[NNN]I REFRESH REQUEST QUEUED FOR MTRB              ← 一次資料 部分一致
```

**前提条件**: 【前提】SA z/OS 初期化済 (DISPMTR は初期化前は使えない)、対象 MTR リソース定義済。

**プレースホルダ**: 【プレースホルダ】[MTR_NAME]=Customization Dialog で定義済 MTR リソース名 (1-11 文字)

**記録項目**:

- ① DISPMTR 一覧パネル スクリーンショット
- ② 対象 MTR の INGINFO 詳細 (Observed/Desired/Auto Status/Health)
- ③ DISPMTR [MTR_NAME] 単一表示の health 値と収集時刻
- ④ A (Active reset) / B (refresh) 実行後の health 更新値

### VRF-008 — SETHOLD

**分類**: Z System Automation (TSA) ／ オペレータコマンド

**検証目的**: SETHOLD が AOF メッセージの hold 種別 (i/a/e/d/w) を OST タスク単位で設定し、OST 内オペレータ ID 用 hold 動作が反映されることを確認。

```text
NCCF        Tivoli NetView           USER1            06/15/26 11:15:30
- DOMAIN: CNM01

* USER1   SETHOLD
   SETHOLD CURRENT VALUES FOR USER1:
     i (information) = Y
     a (action)      = Y
     e (eventual)    = N
     d (decision)    = Y
     w (wait)        = N

* USER1   SETHOLD CONFIG
   AOF[NNN]I HOLD SETTINGS RESET TO CONFIG VALUES FOR USER1   ← 一次資料 部分一致

* USER1   SETHOLD a e d w
   AOF[NNN]I HOLD FLAGS UPDATED:                              ← 一次資料 部分一致
     i = N  (not specified)
     a = Y
     e = Y
     d = Y
     w = Y

* USER1   SETHOLD AUTO
   AOF[NNN]I HOLD FLAGS SET TO AUTOMATION TABLE VALUES        ← 一次資料 部分一致
   INGNTFY GLOBALS UPDATED FOR USER1

   --- NNT タスクで実行した場合 (Restrictions) ---
* USER1   SETHOLD CONFIG
   AOF[NNN]I SETHOLD IS ONLY USEFUL ON OST TASK; COMMAND IGNORED  ← 一次資料 部分一致
```

**前提条件**: 【前提】OST タスクでログオン中 (NNT/RMT ではコマンド無視される)、対象オペレータ ID が automation control file の Notify Operators に定義済。

**プレースホルダ**: 【プレースホルダ】[OPER]=現在ログオン中のオペレータ ID

**記録項目**:

- ① SETHOLD 現状値 (i/a/e/d/w フラグ)
- ② SETHOLD CONFIG 実行後 hold 値 + AOF[NNN]I メッセージ
- ③ SETHOLD a e d w 個別指定後の AOF[NNN]I 更新確認
- ④ SETHOLD AUTO 実行後 INGNTFY globals 更新確認
- ⑤ テストメッセージ発生時に対象種別だけが保持されることのログ抜粋

### VRF-009 — DATETIME

**分類**: Z System Automation (TSA) ／ プログラマーズリファレンス

**検証目的**: INGEXEC コマンドフレームワーク内で DATETIME カテゴリの実行が CATEGORY/STATUS/OBSERVED 等のステータスタイプを適切に操作することを確認。

```text
NCCF        Tivoli NetView           USER1            06/15/26 11:30:00
- DOMAIN: CNM01

   --- INGEXEC で DATETIME カテゴリを発行 ---
* USER1   NETVASIS INGEXEC APL1/APL CMD='DATETIME' CATEGORY=DATETIME STATUS=ACTIVE
  INGY1000I INGEXEC ACCEPTED, REQID=20260615113001        ← 一次資料 部分一致

* USER1   INGLIST APL1/APL STATUS=ACTIVE
   AOFXM3                  INGLIST                         SA z/OS V4.3
   Cmd  Name           Type    System   Observed   Desired   Compound
    _   APL1           APL     SYS1     AVAILABLE  AVAILABLE SATISFACTORY
        Category=DATETIME  LastExec=20260615113001  RC=0

   --- 完了確認 ---
* USER1   BROWSE NETLOGA
   --- BROWSE NETLOG ---
   06/15/26 11:30:01 INGY1000I INGEXEC ACCEPTED REQID=20260615113001
   06/15/26 11:30:02 INGY[NNN]I INGEXEC COMPLETED REQID=20260615113001 RC=0
```

**前提条件**: 【前提】SA z/OS 初期化済、INGEXEC 実行権限あり、対象 application/resource 定義済。

**プレースホルダ**: 【プレースホルダ】[RESOURCE_NAME]=対象リソース名 (name/type[/system])、[REQID]=システム採番

**記録項目**:

- ① INGEXEC コマンド全文 (NETVASIS プレフィックス含む)
- ② INGY1000I ACCEPTED メッセージ + REQID
- ③ INGLIST 結果 (STATUS=ACTIVE 行の DATETIME 反映)
- ④ NETLOG INGEXEC 戻り RC=0 確認

### VRF-010 — Policy Items for Remote Domains

**分類**: Z System Automation (TSA) ／ 自動化ポリシー定義

**検証目的**: Remote Domains entry type (RMD) の DESCRIPTION/DOMAIN INFO/REFERENCES 定義が E2E ハブで認識され該当 sysplex リソースが見えることを確認。

```text
--- TSO Customization Dialog 起動 ---
READY
INGENV
ISPF
   (SA z/OS Customization Dialog Main Menu 表示)

   --- Entry Type Selection で RMD 選択 ---
   AOFGENT      Entry Type Selection                    Row 1 of 18
   Action  Entry Type                Description
       _   AOP                       Application Group
       _   APL                       Application
       _   RMD                       Remote Domains
   Command ===> S RMD

   AOFGRMD      Remote Domains Entry List                Row 1 of 0
   Cmd  Entry Name
   Command ===> C
   (Create を選択 → Entry Name 入力)
   Entry Name: REMDOM01

   --- Policy Items 一覧 (一次資料 記載どおり) ---
   ACTIONS  HELP
   -------------------------------------------------------------------------
   Entry Type : Remote Domain
   Entry Name : REMDOM01
   Action      Policy Name          Policy Description
                DESCRIPTION          Enter description
                DOMAIN INFO          Define domain information
                REFERENCES           Select references to remote resources
                -------------------- ---------------------------------------
                WHERE USED
   Command ===>

   --- DESCRIPTION 編集 ---
   Description: Sysplex BACKUP @ Site B
   AOF[NNN]I POLICY ITEM SAVED                         ← 一次資料 部分一致

   --- DOMAIN INFO 編集 ---
   DOMAIN ID    : CNM02
   SYSPLEX NAME : PLEXB
   AOF[NNN]I POLICY ITEM SAVED                         ← 一次資料 部分一致

   --- REFERENCES 選択 ---
   COMMANDS  HELP
   -------------------------------------------------------------------------
   Command ===>                                          SCROLL===> CSR
   Entry Type : Remote Domain
   Action  Resource Reference
       S   APLA/APL/SYS1
       S   APLB/APL/SYS1
   AOF[NNN]I 2 REFERENCES SELECTED                      ← 一次資料 部分一致

   --- F3 で Build Policy DB ---
   INGY1000I BUILD COMPLETED, RC=0                       ← 一次資料 部分一致

   --- E2E ハブ側で確認 ---
NCCF        Tivoli NetView           USER1            06/15/26 12:00:00
* USER1   INGE2E LIST DOMAINS
   Domain Name    Status      Sysplex     Last Update
   REMDOM01       AVAILABLE   PLEXB       06/15/26 12:00:05
```

**前提条件**: 【前提】SA z/OS Customization Dialog 起動可能、Policy DB 更新権限、対象 sysplex / リモート NetView ドメイン情報判明。

**プレースホルダ**: 【プレースホルダ】[REMOTE_DOMAIN]=Remote Domain entry 名、[REM_DOMID]=リモート NetView ドメイン ID、[REM_PLEX]=リモート sysplex 名

**記録項目**:

- ① Customization Dialog RMD entry 作成画面
- ② DESCRIPTION/DOMAIN INFO の入力値 (DOMAIN ID/SYSPLEX NAME)
- ③ REFERENCES 選択行 ('+' マーク確認)
- ④ Build Policy DB ログ (INGY1000I BUILD COMPLETED RC=0)
- ⑤ INGE2E LIST DOMAINS 出力 (STATUS=AVAILABLE)

### VRF-011 — Hardware Management Console

**分類**: Z System Automation (TSA) ／ 計画 / インストール

**検証目的**: HMC が Hardware LAN 経由で CPC オブジェクトを管理可能で、SA z/OS ProcOps から SNMP/BCPii 接続および Console Integration (CI) 経由の OS コマンド送受信ができることを確認。

```text
--- HMC Web UI ログイン ---
   https://10.10.10.1/hmc
   Logon ID:  HMCOPER
   Password:  ********
   [About] → HWMCA Version 2.16.0    ← SA z/OS 4.3 互換

   --- NetView から SNMP 接続テスト ---
NCCF        Tivoli NetView           USER1            06/15/26 12:30:00
- DOMAIN: CNM01

* USER1   F NETVPROCOPS,SNMP TEST CPC=CPC1,HMC=10.10.10.1,COMMUNITY=public
  INGP1000I SNMP CONNECTION ESTABLISHED CPC=CPC1                ← 一次資料 部分一致

* USER1   ISQXDST CPC1
   ISQX001                ProcOps Status Display              SA z/OS V4.3
   CPC Name : CPC1
   Status   : CONNECTED
   HMC      : 10.10.10.1
   Type     : SNMP
   Last Hb  : 06/15/26 12:30:15
   Command ===>

* USER1   ISQSEND CPC1 CMD='D T'
  ISQ[NNN]I COMMAND SENT TO CPC1                              ← 一次資料 部分一致
  IEE136I  LOCAL: TIME=12.30.20 DATE=2026.166 UTC: TIME=03.30.20 DATE=2026.166

   --- BCPii テスト ---
* USER1   F NETVPROCOPS,BCPII TEST CPC=CPC1
  INGP1001I BCPii CONNECTION OK                               ← 一次資料 部分一致
```

**前提条件**: 【前提】HMC が Hardware LAN に接続済、SA z/OS ProcOps 構成済、Comm Server TCP/IP スタック稼働中、HWMCA バージョン互換性確認済。

**プレースホルダ**: 【プレースホルダ】[HMC_IP]=HMC IP アドレス、[CPC_NAME]=CPC オブジェクト名、[COMMUNITY_STR]=SNMP community 文字列

**記録項目**:

- ① HMC HWMCA バージョン (SA z/OS 4.3 互換確認)
- ② SNMP TEST CPC コマンド + INGP1000I 結果
- ③ ISQXDST [CPC_NAME] パネル (CONNECTED 状態)
- ④ ISQSEND CMD='D T' の応答 (IEE136I)
- ⑤ BCPII TEST CPC 結果 (INGP1001I)
- ⑥ 失敗時の SNMP community 文字列 / TCP/IP 接続診断結果

### VRF-012 — Consistency group function

**分類**: GDPS 災害対策・サイトスイッチ ／ DS8000 Copy Services

**検証目的**: DS8000 CG 機能で chrcconsistgrp -consistencyfreeze による CG 整合性フリーズと -failover による H3 primary 昇格が動作することを確認 (3 サイト DR 構成での recovery 演習)。

```text
$ dscli -hmc1 10.20.30.40 -user admin -passwd ********
DSCLI[10000]I DSCLI started.
dscli>

dscli> lspprc -dev IBM.2107-75ABC10 1000-10FF
ID         State         Reason  Type            Out Of Sync   Tgt Read   Tgt Write
1000:2000  Full Duplex   -       Metro Mirror    0             Disabled   True
1001:2001  Full Duplex   -       Metro Mirror    0             Disabled   True
... (省略)

dscli> chrcconsistgrp -dev IBM.2107-75ABC10 -consistencyfreeze 10:14
CMUC00139I chrcconsistgrp: Consistency group 10:14 frozen.    ← 一次資料 部分一致: ID 番号は推定

dscli> chrcconsistgrp -dev IBM.2107-75ABC20 -failover 14:10
CMUC00141I chrcconsistgrp: Failover 14:10 succeeded.          ← 一次資料 部分一致: ID 番号は推定

dscli> lspprc -dev IBM.2107-75ABC20 1400-14FF
ID         State                       Reason  Type
1400:1000  Suspended Host Source       -       Global Copy   ← 一次資料 記載どおり (p.318 形式)
1401:1001  Suspended Host Source       -       Global Copy
2001:1001  Suspended Host Source Global Copy 20        unknown        Disabled      True
2100:1100  Suspended Host Source Global Copy 21        unknown        Disabled      True

dscli> lsflash -dev IBM.2107-75ABC20 1400-14FF
ID          SrcLSS  Sequence  State           Active Copy
1400:1500   14      0001      Valid           True
1401:1501   14      0001      Valid           True
```

**前提条件**: 【前提】DS CLI (dscli) 導入済、HMC への接続情報 (IP/user/password) 設定済、対象 storage image ID 判明、recovery 演習モード。

**プレースホルダ**: 【プレースホルダ】[HMC_IP]/[DSCLI_USER]/[DSCLI_PW]=DS HMC 接続情報、[STORAGE_ID]=ストレージイメージ ID、[LSS_*]=LSS ID 範囲 (16 進)

**記録項目**:

- ① dscli ログオン応答 (DSCLI[NNNN]I started)
- ② lspprc 実行前の pair 状態 (Full Duplex 等)
- ③ chrcconsistgrp -consistencyfreeze 実行ログ (CMUC[NNNNN]I frozen)
- ④ chrcconsistgrp -failover 実行ログ (CMUC[NNNNN]I succeeded)
- ⑤ lspprc 実行後の H3 pair 状態 (Suspended/Source)
- ⑥ lsflash 結果 (FlashCopy 関係 consistent 確認)

### VRF-013 — FlashCopy

**分類**: GDPS 災害対策・サイトスイッチ ／ DS8000 Copy Services

**検証目的**: mkflash で FlashCopy 関係 (-nocp -tgtse -persist) を確立しバックアップ取得後 rmflash で関係解消できることを確認 (in-band/remote 両モード対応)。

```text
$ dscli -hmc1 10.20.30.40 -user admin -passwd ********
DSCLI[10000]I DSCLI started.
dscli>

dscli> lsfbvol -dev IBM.2107-75ABC10 0111 0110
ID    accstate  datastate    configstate  deviceMTM  datatype  extpool  cap (GiB)  cap (10^9B)  cap (blocks)
0111  Online    Normal       Normal       2107-900   FB 512    P0       1.0        1.1          2097152
0110  Online    Normal       Normal       2107-900   FB 512    P0       1.0        1.1          2097152

dscli> mkflash -nocp -tgtse -persist 0111:0110                  ← 一次資料 記載どおり (p.88)
CMUC00137I mkflash: FlashCopy pair 0111:0110 successfully created.

dscli> mkflash -nocp -tgtse -persist 0110:0112
CMUC00137I mkflash: FlashCopy pair 0110:0112 successfully created.

dscli> lsflash -dev IBM.2107-75ABC10 0111
ID          SrcLSS  Sequence  State           Active Copy
0111:0110   01      0001      Valid           True

   --- バックアップ取得 (z/OS 側 ADRDSSU DUMP) ---
ADR454I (001)-PRIME(01), THE FOLLOWING DATA SETS WERE DUMPED:
   USER1.MYDATA
ADR454I (001)-DUMP COMPLETED SUCCESSFULLY

   --- FlashCopy 関係解消 ---
dscli> rmflash 111:110                                          ← 一次資料 記載どおり (p.88)
CMUC00144W rmflash: Are you sure you want to remove the FlashCopy pair 111:110:? [y/n]:
y
CMUN81131I rmflash: 0111:0110: The Withdraw command was accepted and the FLC
relationship has been removed.

dscli> lsflash -dev IBM.2107-75ABC10 0111
CMUC00234I lsflash: No FlashCopy relations to display.          ← 一次資料 部分一致: ID 形式
```

**前提条件**: 【前提】DS CLI 接続中、FlashCopy ライセンス有効、対象 source/target volume が同一 storage image、source/target 同サイズ。

**プレースホルダ**: 【プレースホルダ】[STORAGE_ID]=ストレージイメージ ID、[SRC_VOL]/[TGT_VOL]=4 桁 volume ID (例: 0111)

**記録項目**:

- ① lsfbvol 結果 (source/target volume サイズ一致)
- ② mkflash 実行コマンド + CMUC00137I メッセージ
- ③ lsflash 結果 (State=Valid / OutOfSyncTrack)
- ④ バックアップ取得ログ (ADR454I 完了)
- ⑤ rmflash 実行 + CMUN81131I Withdraw メッセージ
- ⑥ rmflash 後の lsflash 結果 (pair なし)

### VRF-014 — GDPS GM Copy Once facility

**分類**: GDPS 災害対策・サイトスイッチ ／ GDPS Family 概要 / 機能

**検証目的**: Copy Once 対象 volume (page/sort 等 temp) の初期コピーと REINIT 機能が動作し、継続レプリケート対象データが混入していないことを確認。

```text
NCCF        Tivoli NetView (GDPS)    USER1            06/15/26 13:00:00
- DOMAIN: CNM01

* USER1   GEOMON DISPLAY VOLUMES COPYONCE=YES
  GEO[NNN]I NO VOLUMES MATCHED CRITERIA                     ← 一次資料 部分一致

* USER1   GEOMON SET COPYONCE VOLUME=PAGE01 ACTION=ADD
  GEO[NNN]I VOLUME PAGE01 ADDED TO COPY ONCE LIST           ← 一次資料 部分一致

* USER1   GEOMON COPYONCE INIT VOLUME=PAGE01
  GEO[NNN]I COPY ONCE INIT STARTED FOR PAGE01               ← 一次資料 部分一致
  GEO[NNN]I COPY ONCE INIT COMPLETED FOR PAGE01

* USER1   GEOMON DISPLAY VOLUMES COPYONCE=YES
   VOLSER    Status              Last Init
   PAGE01    Initial Copied      06/15/26 13:00:15

   --- アプリ変更時の REINIT ---
* USER1   GEOMON COPYONCE REINIT VOLUME=PAGE01
  GEO[NNN]I COPY ONCE REINIT COMPLETED FOR PAGE01           ← 一次資料 部分一致

   --- 定期確認 (継続 mirror データ非混入チェック) ---
READY
DCOLLECT VOLUME(PAGE01)
   (出力で PAGE01 に PAGE/SORT 以外のデータがないか確認)
```

**前提条件**: 【前提】GDPS Global - GM 構成稼働中、対象ボリュームが page/sort 等の temp 用と確認済、運用責任者承認済。

**プレースホルダ**: 【プレースホルダ】[VOLSER]=Copy Once 対象ボリューム VOLSER (6 文字)

**記録項目**:

- ① GEOMON DISPLAY VOLUMES COPYONCE=YES 実行前一覧
- ② GEOMON SET COPYONCE VOLUME=[VOLSER] 実行ログ (GEO[NNNN]I)
- ③ INIT 実行完了メッセージ (GEO[NNNN]I COMPLETED)
- ④ REINIT 実行ログ
- ⑤ DCOLLECT 結果 (継続 mirror データ非混入確認)

### VRF-015 — z/OS Metro/Global Mirror

**分類**: GDPS 災害対策・サイトスイッチ ／ Metro/Global Mirror

**検証目的**: MM (H1↔H2) + XRC (H1↔H3) の 3 サイト構成で Incremental Resync 有効化と HyperSwap 連動の RMZ Resync (H2→H3 full copy 不要) が機能することを確認。

```text
$ dscli -hmc1 10.20.30.40 -user admin -passwd ********
dscli> mkpprc -dev IBM.2107-75ABC10 -remotedev IBM.2107-75ABC20 -type mmir 1000:2000
CMUC00153I mkpprc: Remote Mirror and Copy volume pair relationship 1000:2000
successfully created.

   --- z/OS XRC ホストコンソール ---
RESPONSE=SYS1
 IEE600I REPLY TO 003 IS;XSTART SESSION(MZGM01) HLQ(USER1)
ANTX5103I SESSION MZGM01 STARTED SUCCESSFULLY               ← 一次資料 部分一致

  XADDPAIR SESSION(MZGM01) PRIMARY(1000) SECONDARY(3000)
ANTX5104I XADDPAIR ACCEPTED FOR SESSION MZGM01              ← 一次資料 部分一致
ANTX5121I PAIR 1000:3000 STATE=DUPLEX                       ← 一次資料 部分一致

  XQUERY SESSION(MZGM01) STATE
   Session: MZGM01
   Pairs: 1
   STATE     COUNT
   DUPLEX    1
   REPLICATING

   --- GDPS controlling LPAR ---
NCCF        Tivoli NetView (GDPS)    USER1            06/15/26 14:00:00
* USER1   GEOPARM SET INCREMENTAL_RESYNC=YES
  GEO[NNN]I INCREMENTAL RESYNC ENABLED                      ← 一次資料 部分一致
* USER1   GEOMON REFRESH
  GEO[NNN]I REFRESH COMPLETED

   --- HyperSwap 計画切替試験 ---
* USER1   GEOMON HYPERSWAP MODE=PLANNED H1=H2
  GEO[NNN]I HYPERSWAP COMPLETED, RMZ RESYNC STARTING H2->H3 ← 一次資料 部分一致
  ANTX[NNN]I INCREMENTAL RESYNC IN PROGRESS

  XQUERY SESSION(MZGM01) STATE
   STATE              COUNT
   PENDING_DUPLEX     1
   (incremental progress → 数分後 DUPLEX 復帰)
```

**前提条件**: 【前提】3 サイト (H1/H2/H3) DS8000 全展開済、MM + XRC ライセンス、SDM (System Data Mover) 稼働、GDPS MzGM 制御 LPAR、RMZ Resync 機能有効化条件 (Incremental Resync) 確認済。

**プレースホルダ**: 【プレースホルダ】[H*_ID]=各サイト storage image ID、[H*_LSS]=LSS 範囲、[XRC_SESSION]=XRC session 名 (1-8 文字)、[H1_VOL]/[H3_VOL]=対象 volume 範囲

**記録項目**:

- ① mkpprc MM 確立ログ (CMUC00153I)
- ② XADDPAIR 実行 + ANTX[NNNN]I + PAIR DUPLEX 出力
- ③ XQUERY SESSION STATE 結果 (全 pair DUPLEX/REPLICATING)
- ④ GEOPARM INCREMENTAL_RESYNC=YES 反映ログ
- ⑤ HyperSwap 計画切替実行ログ (RMZ Resync 開始メッセージ)
- ⑥ HyperSwap 後の XQUERY 結果 (incremental 進捗 → DUPLEX 復帰)

### VRF-016 — Subscription security

**分類**: IBM MQ メッセージング ／ セキュリティ (CHLAUTH /  TLS)

**検証目的**: publish/subscribe で admin topic object に紐付けたセキュリティ属性が機能し、許可ユーザのみ subscribe 可能、親 topic 継承も適用されることを確認。

```text
$ runmqsc QMGR1
Starting MQSC for queue manager QMGR1.

DEFINE TOPIC(SALES.NA) TOPICSTR('sales/na') REPLACE
     1 : DEFINE TOPIC(SALES.NA) TOPICSTR('sales/na') REPLACE
AMQ8690I: IBM MQ topic created.

end
No commands have a syntax error.
All valid MQSC commands were processed.

$ setmqaut -m QMGR1 -t topic -n SALES.NA -p alice +sub
AMQ7024I: The setmqaut command completed successfully.

$ dspmqaut -m QMGR1 -t topic -n SALES.NA -p alice
Entity alice has the following authorizations for object SALES.NA:
        sub

   --- alice での subscribe テスト ---
$ amqsbcg 'sales/na' QMGR1
Sample AMQSBCG0 start
MQOPEN -  'sales/na'
... (subscription opened, waiting messages) ...
Sample AMQSBCG0 end

   --- 権限なし bob でのテスト ---
$ amqsbcg 'sales/na' QMGR1
Sample AMQSBCG0 start
MQOPEN -  'sales/na'
MQOPEN failed with CompCode:2, Reason:2035 (MQRC_NOT_AUTHORIZED)
Sample AMQSBCG0 end

   --- 親 topic 継承テスト ---
$ amqsbcg 'sales/na/east' QMGR1
   (子トピックは親 SALES.NA の ACL が適用される)
   alice → 受信可、bob → 2035 MQRC_NOT_AUTHORIZED
```

**前提条件**: 【前提】対象 QM ([QMGR]) 稼働中、setmqaut 実行権限、対象トピックツリーが事前設計済、テストユーザ ([SUBUSER]) 作成済。

**プレースホルダ**: 【プレースホルダ】[QMGR]=QM 名、[TOPIC_NAME]=admin topic object 名、[TOPIC_STR]=トピック文字列、[SUBUSER]/[BADUSER]=ユーザ ID

**記録項目**:

- ① DEFINE TOPIC 実行 + AMQ8690I 出力
- ② setmqaut +sub 実行 + AMQ7024I 出力
- ③ dspmqaut 結果 (Entity に sub 権限表示)
- ④ 許可ユーザでの MQSUB/amqsbcg 受信成功ログ
- ⑤ 未許可ユーザでの 2035 MQRC_NOT_AUTHORIZED ログ
- ⑥ 親 topic 継承テストの子 topic 受信結果

### VRF-017 — IBM MQ Administration Interface

**分類**: IBM MQ メッセージング ／ 管理リファレンス

**検証目的**: MQAI (PCF プログラミング IF) で command server 経由の管理 PCF 投入と応答パースが行えることを確認 (AIX/IBM i/Linux/Windows 環境)。

```text
$ runmqsc QMGR1
Starting MQSC for queue manager QMGR1.

DISPLAY QMSTATUS CMDSERV
     1 : DISPLAY QMSTATUS CMDSERV
AMQ8705I: Display Queue Manager Status details.
   QMNAME(QMGR1)                            STATUS(RUNNING)
   CMDSERV(RUNNING)

end
All valid MQSC commands were processed.

$ cc -I/opt/mqm/inc -L/opt/mqm/lib64 -lmqm -o myadm amqsail.c
$ ls -l myadm
-rwxr-xr-x 1 mqm mqm 28456 Jun 15 14:30 myadm

$ ./myadm QMGR1
MQAI sample - inquire queue manager attributes
Connected to QMGR1
Issuing MQCMD_INQUIRE_Q_MGR via MQAI...
Response received:
   DefinitionType : Permanent
   QMgrIdentifier : QMGR1_2026-06-15
   CodedCharSetId : 1208
Disconnected from QMGR1
End MQAI sample

   --- 権限不足時 ---
$ su - bob
$ ./myadm QMGR1
MQAI sample - inquire queue manager attributes
Connected to QMGR1
Issuing MQCMD_INQUIRE_Q_MGR via MQAI...
MQI Reason: 2035 (MQRC_NOT_AUTHORIZED)
Error in mqExecute; CompCode=2, Reason=2035

$ setmqaut -m QMGR1 -t qmgr -p bob +dsp
AMQ7024I: The setmqaut command completed successfully.

$ ./myadm QMGR1                               ← bob で再実行 → 成功
```

**前提条件**: 【前提】対象 QM ([QMGR]) 稼働中、command server 稼働中 (DISPLAY QMSTATUS CMDSERV で RUNNING)、MQAI ヘッダ (cmqcfc.h) を含む開発環境。

**プレースホルダ**: 【プレースホルダ】[QMGR]=QM 名

**記録項目**:

- ① DISPLAY QMSTATUS CMDSERV 結果 (CMDSERV RUNNING)
- ② サンプルアプリのコンパイル/リンクログ (警告 0)
- ③ ./myadm [QMGR] 実行出力 (QM 属性表示)
- ④ 失敗時 MQCFH の CompCode/Reason 値
- ⑤ setmqaut +dsp 適用前/後の応答差

### VRF-018 — CCSID

**分類**: IBM MQ メッセージング ／ 開発リファレンス

**検証目的**: MQ 9.0 以降の Unicode 8.0 / UTF-16 / JIS X 0213 サポートが CCSID 設定 + ccsid_part2.tbl 配備で機能し data conversion が正しく動作することを確認。

```text
$ ls -l /var/mqm/conv/table/ccsid_part2.tbl
-rw-r--r-- 1 mqm mqm 1048576 Jun 10 09:00 /var/mqm/conv/table/ccsid_part2.tbl

$ runmqsc QMGR1
Starting MQSC for queue manager QMGR1.

DISPLAY QMGR CCSID
     1 : DISPLAY QMGR CCSID
AMQ8408I: Display Queue Manager details.
   QMNAME(QMGR1)                            CCSID(819)

ALTER QMGR CCSID(1208)
     1 : ALTER QMGR CCSID(1208)
AMQ8005I: IBM MQ queue manager changed.
AMQ8910I: The change has been committed. Queue manager restart may be
required for some attributes to take effect.

end
All valid MQSC commands were processed.

   --- JIS X 0213 文字 ('𠮟責') を JMS テストアプリで送信 ---
$ java -classpath ".:/opt/mqm/java/lib/com.ibm.mq.allclient.jar" SendJIS2004
Connected to QMGR1
Sending message: '𠮟責' (CCSID=1208, UTF-8 4-byte encoding)
MQPUT successful, MsgId=414D5120514D4752312020...
CURDEPTH(1)

   --- 異 CCSID クライアント (EBCDIC CCSID 939) で受信 ---
$ java -classpath "..." RecvEBCDIC
Connected to QMGR1 (client CCSID=939)
MQGET successful, payload = '𠮟責' ← data conversion 経由で正しく取得
CURDEPTH(0)

   --- 変換失敗時 ---
2026-06-15T14:50:12 AMQ7042E MQGET ended with reason code 2111
   MQRC_SOURCE_CCSID_ERROR
   (ccsid_part2.tbl 更新 or QM CCSID 適切化が必要)
```

**前提条件**: 【前提】対象 QM ([QMGR]) 稼働中、ccsid_part2.tbl 配備済 (/var/mqm/conv/table/ccsid_part2.tbl)、JIS X 0213 文字を含むテスト文字列準備。

**プレースホルダ**: 【プレースホルダ】[QMGR]=QM 名

**記録項目**:

- ① ccsid_part2.tbl の存在 + updated date
- ② DISPLAY QMGR CCSID 結果 (現行 CCSID 値)
- ③ ALTER QMGR CCSID(1208) 実行ログ (AMQ8005I)
- ④ JIS X 0213 文字を含むテスト送信メッセージ (例: '𠮟責')
- ⑤ 異 CCSID クライアントでの受信内容 (機種化けゼロ確認)
- ⑥ 失敗時の 2111 MQRC_SOURCE_CCSID_ERROR 出力

### VRF-019 — MQAuthenticationInformationRec

**分類**: IBM MQ メッセージング ／ 開発リファレンス

**検証目的**: MQAuthenticationInformationRecord クラス + AUTHINFO オブジェクト (CRLLDAP type) が .NET client 接続で機能し ADOPTCTX 設定により credentials 採用挙動が制御できることを確認。

```text
$ runmqsc QMGR1
Starting MQSC for queue manager QMGR1.

DEFINE AUTHINFO(AUTH.CRL) AUTHTYPE(CRLLDAP) +
   CONNAME('crlldap.example.com(389)') +
   LDAPUSER('cn=admin,dc=example,dc=com') +
   LDAPPWD('********') REPLACE
     1 : DEFINE AUTHINFO(AUTH.CRL) AUTHTYPE(CRLLDAP) ...
AMQ8004I: IBM MQ authentication information object created.

ALTER QMGR SSLCRLNL(AUTH.CRL)
     1 : ALTER QMGR SSLCRLNL(AUTH.CRL)
AMQ8005I: IBM MQ queue manager changed.

REFRESH SECURITY TYPE(SSL)
     1 : REFRESH SECURITY TYPE(SSL)
AMQ8560I: IBM MQ security cache refreshed.

end

   --- .NET C# サンプルコンパイル ---
C:\dev> csc /r:amqmdnetstd.dll TestAir.cs
Microsoft (R) Visual C# Compiler version 4.7
TestAir.cs(45,7): warning CS0168: variable declared but never used (none)
Build succeeded.

C:\dev> TestAir.exe
Connecting to QMGR1 with MQAuthenticationInformationRecord (CRLLDAP)
   CONNAME = crlldap.example.com(389)
   LDAPUserName = cn=admin,dc=example,dc=com
MQQueueManager.Connect: CompCode=0, Reason=0
DISPLAY CONN(*) USERID:
   CONN(1234)  USERID(DOMAIN\appuser)
TestAir completed.

   --- 失敗 (Auth Info Rec Count 不整合) ---
C:\dev> TestAirBad.exe
MQConnect failed: CompCode=2, Reason=2384 (MQRC_AUTH_INFO_REC_COUNT_ERROR)
   AuthInfoRec 配列サイズと AuthInfoRecCount フィールド不整合 → 修正

   --- ADOPTCTX(NO) 設定時 ---
$ runmqsc QMGR1
ALTER AUTHINFO(AUTH.CRL) ADOPTCTX(NO)
AMQ8005I: IBM MQ authentication information changed.

   再接続後 DISPLAY CONN(*) で USERID() は app 実行 OS ユーザのまま
   (認証は実施するが credentials は採用されない - 一次資料 記載どおり 仕様)
```

**前提条件**: 【前提】対象 QM ([QMGR]) 稼働中、CRL LDAP サーバ ([CRL_LDAP]) アクセス可能、.NET MQ client (amqmdnetstd.dll) 配備済。

**プレースホルダ**: 【プレースホルダ】[QMGR]=QM 名、[AUTH_NAME]=AUTHINFO オブジェクト名、[CRL_LDAP_HOST]/[CRL_LDAP_PORT]=CRL LDAP 接続情報、[LDAP_USER]/[LDAP_PW]=LDAP バインド資格情報

**記録項目**:

- ① DEFINE AUTHINFO 実行ログ (AMQ8004I)
- ② ALTER QMGR SSLCRLNL + REFRESH SECURITY 実行ログ
- ③ .NET アプリのコンパイル結果 (csc /r:amqmdnetstd.dll)
- ④ MQConnect 成功ログ + DISPLAY CONN(*) の USERID 値
- ⑤ 2384 MQRC_AUTH_INFO_REC_COUNT_ERROR 出る場合の配列サイズ
- ⑥ ADOPTCTX(NO) 設定時の app OS ユーザ採用確認
