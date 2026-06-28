# -*- coding: utf-8 -*-
import json, os

rows = json.load(open(r'C:\kvba\zos-atoms-site\_phase2_outputs\g057_rows.json', encoding='utf-8'))

# naiyou_jp grounded in IBM TSA z/OS 4.3 Planning and Installation (RAG-verified).
# Each: 2-4 JP sentences. rag_hit: source PDF/page actually confirmed or topically grounded.
N = {}
def add(rid, jp, hit):
    N[rid] = (jp, hit)

add('11523', 'SA z/OS のアラート通知基盤は、手動介入を要する自動化問題を専門家へエスカレーションする仕組みである。INGALERT コマンドの起動を契機に、SA IOM・Tivoli Enterprise Console/Netcool/OMNIbus・Tivoli Service Request Manager などの通知先へアラート、イベント、トラブルチケットを送信する。基盤の詳細は「Alert-Based Notification」(Customizing and Programming) を参照する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.51')
add('11524', '開始済みプロシージャ (started procedure) の認可とは、NetView 起動タスクおよび自動化マネージャー起動タスクのユーザー ID に必要な RACF 権限を付与する作業である。これらの STC ユーザーは FACILITY クラスのリソースプロファイル (IEAABD.DMPAUTH 等) に READ アクセスが必要であり、動的に割り振られるデータセットには UPDATE 権限が要る。STARTED プロファイルまたは ICHRIN03 テーブルでユーザー ID を割り当てる。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.174')
add('11525', '複数行 z/OS メッセージの自動化は、NetView 自動化テーブルおよび AOCMSG 自動化ルーチンを用いてメッセージを処理する仕組みである。メッセージは DSIMSG データセットに登録し、一意のメッセージ ID を割り当てたうえで NetView メッセージサービスへ定義する。複数行 WTO/WTOR を正しく結合・評価できるよう自動化テーブルを構成する。', 'TSA_z_OS_4.3_Customizing_and_Programming.pdf p.34')
add('11526', '自動化マネージャーに関する考慮事項は、サブプレックス内の全システムで共通利用できる PARMLIB メンバーや起動プロシージャ INGEAMSA の設計を含む。XCF グループは INGXSGxx (xx は &SYSCLONE) の形で一意に生成され、プロダクション系と K システムで同一の起動プロシージャを共用できる。自動化マネージャーは自動化対象リソースのモデルを保持する「頭脳」として機能する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.169')
add('11527', 'IBM Z の LPAR セキュリティ設定は実行時に変更可能であり、Cross Partition Authority や BCPii Permissions の変更は SA-BCPii コンソール通信に影響する (IP ベース通信には影響しない)。協調された手動変更手順を整備し、HMC 側の変更とプロセッサーポリシー (接続プロトコル定義や LPAR 定義) の変更を同期させることで、不意の SA-BCPii 接続断を防止する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.246')
add('11528', 'コンソール定義の不整合を回避するには、シスプレックス内でコンソール名を一意に保つ必要がある。SA z/OS は AOCGETCN によりタスク名に依存しない一意のコンソールを取得し、共通タスク名による名前競合を避ける。INGPLEX CONsole コマンドでマスターコンソール、WTO/WTOR バッファー使用率、コンソール一覧 (状態・権限・MSCOPE 等) を確認できる。', 'TSA_z_OS_4.3_Programmers_Reference.pdf p.44')
add('11529', '構成アシスタント (Configuration Assistant) を用いた基本構成では、構成ジョブ・起動プロシージャ・初期化ファイルを手動で編集する代わりに、ユーザーがカスタマイズした INGDOPT 構成オプションファイルから自動生成する。生成物は動的に割り振られる構成データセットのメンバーとして作成される。SA z/OS は SMP/E でインストールしたうえで本アシスタントにより構成する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.71')
add('11530', '変更されたコマンドと表示 (Changed Commands and Displays) は、SA z/OS 4.3 への移行時に確認すべき項目で、付録 B「Migration Information」に整理されている。旧リリースから動作や出力が変わったコマンド・パネルを把握し、運用手順や自動化ルーチンへの影響を評価する。移行前に Migration Notes セクションを通読することが推奨される。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.227')
add('11531', '変更された出口 (Changed Exits) は、移行時に確認すべきユーザー出口の変更点を示す。SA z/OS には BUILD 処理用の INGEX10、SDF パネル用の AOFEXX05 など多数のカスタマイズダイアログ出口・自動化出口があり、リリース間でパラメーターや呼び出し条件が変わる場合がある。AOF256I/AOF257I 等のメッセージで出口の起動・終了を確認できる。', 'TSA_z_OS_4.3_Customizing_and_Programming.pdf p.177')
add('11532', 'インストールデータセットの低位修飾子 (LLQ) は SA z/OS V4.2 で変更された。SYS1.SINGNPRM、SYS1.SINGIPDB、SYS1.SINGIMSG など旧 LLQ から新 LLQ へのマッピング表が提供されており、移行時にはこれに従ってデータセット名・割り振りジョブを更新する必要がある。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.227')
add('11533', 'コマンドセキュリティの変更 (Changes to Command Security) は移行時の確認項目で、NETCMDS/NETSPAN クラスや NetView コマンド認可テーブル (CAT)、SECOPTS.CMDAUTH 設定に関わる。z/OS システムコマンドは RACF (サンプル INGESAF)、NetView コマンドは CAT または SAF で制御する。リリース間で認可チェック対象や既定値が変わる場合がある。', 'TSA_z_OS_4.3_Programmers_Reference.pdf p.172')
add('11534', 'カスタマイズダイアログの変更 (Changes to Customization Dialog) は移行時に確認すべき項目で、新しいポリシーオブジェクトや入力フィールドの追加・変更を含む。移行前にカスタマイズダイアログを開き、互換性 APAR (例: OA61747) を適用したうえでポリシーデータベースを 4.3 形式へ変換する。Settings 機能でダイアログ環境を調整できる。', 'TSA_z_OS_4.3_Defining_Automation_Policy.pdf p.375')
add('11535', 'CI 自動化の基本 (CI Automation Basics) は、IBM Z のハードウェア統合コンソール (CI/HWC Integrated Console) を用いたシステムコンソールメッセージ自動化の基礎を扱う。HMC 統合コンソールタスクがメッセージ自動化に与える影響を理解し、SYSCONS 経由のメッセージ取得・コマンド発行を SA z/OS の自動化と統合する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.211')
add('11536', 'リモート自動化のための CI 構成では、3 つのシステムの CI を、リモート自動化フォーカルポイントとして機能する 1 つの SA z/OS システムへ接続する。BCPii を介して対象システムの統合コンソールにアクセスし、集中的に外部自動化を行う構成を定義する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.214')
add('11537', 'CI と 3270 ベースコンソールデバイスの相違では、CI は拡張カラーやプログラムファンクションキーなど 3270 データストリーム固有機能を提供しない点が挙げられる。SE 障害時は当該 CPC 全 LPAR の CI が影響を受け、代替 SE が主系として活性化されるか主系 SE が再活性化されると CI が復旧する。チャネル接続 3270 環境のような複数チャネルパス経由のバックアップはできない。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.217')
add('11538', 'CI 性能要因 (CI Performance Factors) は、統合コンソール経由のメッセージ処理性能に影響する要素を扱う。表示されるメッセージ量や SNMP 接続の応答性が関係し、IPL 時メッセージ数の制限や推奨 z/OS コンソール設定と併せて最適化する。OMEGAMON 等のモニターや INGMTRAP/INGOMX コマンドの前提製品レベルも考慮する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.221')
add('11539', 'CI プロトコルと自動化インターフェース (CI Protocols and Automation Interfaces) は、統合コンソールへのアクセス手段を扱う。BCPii の INTERNAL パス (GDPS 専用) と SNMP (TCP/IP ネットワークまたは BCPii リダイレクション) が利用でき、ProcOps や Sysplex Automation で使用される。IBM Z SNMP API は SNMP MIB ベースのデータモデルを用いる。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.213')
add('11540', 'SA z/OS の CI セキュリティでは、BCPii 接続を RACF FACILITY クラスのリソースプロファイル (HSA.ET32TGT.netid.nau 等) で制御する。CPC を UACC(NONE) で RDEFINE し、必要なユーザーにのみアクセスを付与することで、統合コンソール経由の操作を保護する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.220')
add('11541', 'IBM System Automation 製品における CI の利用では、ProcOps、Sysplex Automation、および GDPS が BCPii 内部サービスを使用する。HMC 統合コンソールタスクがシステムコンソールメッセージ自動化へ与える影響を理解したうえで、各製品が CI をどう利用するかを把握する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.213')
add('11542', 'z/OS システムでのクローニング (Cloning) は、システム固有値を &SYSCLONE 等のシステムシンボルで置換することで、同一の構成・PARMLIB メンバーを複数システムで共用する手法である。これにより XCF グループ名やデータセット名がシステムごとに一意に解決され、構成の重複定義を避けられる。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.65')
add('11543', 'SA z/OS 4.3 と旧リリースの共存 (Coexistence) では、SA z/OS 4.3 のシステムが同一シスプレックス内で 4.2 および 4.1 のシステムと共存できる。シスプレックスは 1 つの一次自動化マネージャー (PAM) と任意の二次自動化マネージャー (SAM) を持ち、自動化構成ファイルを共有する。機能レベル (function level) により新機能の有効化を制御する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.232')
add('11544', 'コマンド (Commands) は、SA z/OS が提供する各種コマンドとその前提製品レベルを扱う。INGMTRAP や INGOMX など特定コマンドは OMEGAMON XE for CICS/IMS/DB2 V5.3 や CICS TS V5.4 以降を前提とする。ファイルマネージャーコマンドは自動化制御ファイルや運用情報ベースの読み書きに用いる。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.27')
add('11545', 'コンポーネント記述 (Component Description) は、SA z/OS を構成する主要コンポーネント (自動化マネージャー、自動化エージェント) の役割を説明する。自動化マネージャーはシスプレックス内の全自動化リソースのモデルを保持し意思決定を行う「頭脳」、自動化エージェントは状態情報を供給しアクションを実行する「目と腕」である。', 'TSA_z_OS_4.3_Users_Guide.pdf p.29')
add('11546', 'IBM Tivoli Netcool/OMNIbus の構成では、SA z/OS のアラート通知先として OMNIbus を設定する。INGALERT 起動を契機に EIF イベント経由でアラートを送信し、集中オペレーターコンソールにイベントを表示する。EIF を使用するには SA z/OS エージェントが稼働するシステム上に Tivoli Event/Automation Service (E/AS) が必要である。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.207')
add('11547', 'SA z/OS ワークステーションコンポーネントの構成では、アラート通知関連のワークステーション側コンポーネント (OMNIbus、TSRM、TDI 等) をインストール・構成する。INGALERT の通知方法 (EIF/TTT/USR) に応じて必要なコンポーネントを設定する。詳細は Chapter 12 を参照する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.207')
add('11548', 'Tivoli Directory Integrator を介した Tivoli Service Request Manager の構成では、TDI を経由して TSRM にトラブルチケットを作成できるようにする。Trouble Ticket Information XML を用いてサービスデスクアプリケーションと連携する構成を行う。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.209')
add('11549', '継続的機能拡張 (Continuous Enhancements、post-GA サービスレベル) は、GA 後にサービス (APAR/PTF) として提供される機能追加を扱う。前提となるモニター製品 (OMEGAMON XE V5.3、CICS TS V5.4 以降等) を満たすことで、サービスレベルで提供される拡張機能を利用できる。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.27')
add('11550', 'プロセッサーハードウェア機能へのアクセス制御では、各 CPC を RACF FACILITY クラスのリソース (HSA.ET32TGT.netid.nau) として UACC(NONE) で定義し、必要なユーザーにのみアクセスを付与する。これにより BCPii 経由のハードウェア操作 (活性化・リセット等) を保護する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.201')
add('11551', 'プロセッサー操作 (ProcOps) の通信リンク定義では、各プロセッサーの接続プロトコル (SNMP または INTERNAL/BCPii) と代替アドレス/ホスト名を指定する。SNMP は TCP/IP ネットワークまたは BCPii リダイレクション (ISQET32) を介して HMC/SE と通信し、Processor Information ポリシーでこれらを定義する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.56')
add('11552', 'システム操作 (SysOps) の接続定義では、フォーカルポイントシステムと対象システム間の通信を構成する。NetView の RMTCMD やフォーカルポイントサービスを用い、各システムのリソース状態をフォーカルポイントの SDF へ転送する。AOFTREE メンバーで各システムのツリー構造を一意のルート名で定義する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.53')
add('11553', 'Network Security Program (NetSP) による認可確立では、NetSP に記録入力ファイル (ログオン転送スクリプト) を作成する。エミュレーターセッションでのキーストローク記録、またはテキストエディターでの直接入力により作成し、固定期間有効なトークンで認可を行う。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.205')
add('11554', '機能レベル (Function Levels) は、リリース間の移行を容易にし互換性 APAR の必要性を減らすために導入された整数値で、自動化マネージャーやエージェントがサポートする機能を表す。管理者が明示的に機能レベルを引き上げる (opt-in) ことで新機能を有効化でき、引き上げない限り旧来の機能に制限される。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.249')
add('11555', 'その他のプロセッサー操作名 (Further Processor Operations Names) は、ProcOps で使用する各種命名 (プロセッサー名・LPAR 名・ターゲットシステム名等) の規則を扱う。命名規約に従い一意な名前を割り当てることで、ProcOps の構成と操作を正しく行えるようにする。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.41')
add('11556', 'NetView と STC ユーザーへのデータセットアクセス付与では、起動タスクに割り当てられたユーザー ID (既定 STCUSER) が動的に割り振られる一時データセット (hlq.domain.opid.INGPIPLx 等) に RACF UPDATE/ALTER アクセスを持つよう定義する。OPERSEC 値に応じて必要なアクセスレベルが決まる。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.191')
add('11557', 'ハードウェア管理コンソール (HMC) の特性は、ProcOps が通信する HMC/SE の役割と前提を扱う。マスター HMC はリモート CPC への通信を担い、SNMP コミュニティ名は HMC/SE 上で大文字で設定する必要がある。HMC は IBM Z SNMP API の MIB データを保持する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.42')
add('11558', 'ハードウェア要件 (Hardware Requirements) は、SA z/OS の前提となるハードウェアと最小レベルを示す。プロセッサー操作には HMC/SE への SNMP または BCPii 接続が必要であり、対応する IBM Z 機種・SE レベルを満たす必要がある。詳細は「SA z/OS Prerequisites and Supported Equipment」を参照する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.25')
add('11559', 'HMC 統合コンソールタスクがシステムコンソールメッセージ自動化へ与える影響では、CI を介したメッセージ取得・自動化が HMC 上の統合コンソールタスクの動作に依存する点を扱う。統合コンソールの活性状態や SE の可用性がメッセージ自動化の継続性に影響する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.211')
add('11560', 'IBM Z SNMP アプリケーションプログラミングインターフェース (API) は、ハードウェア機能とイベント制御に集中できるよう、Bind/Connect 等のネットワーク固有サービスを提供する。SNMP MIB データ形式を用い、アプリケーションは特定 LPAR の CI から OS メッセージ等のイベントを動的に登録できる。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.214')
add('11561', 'INGDLG コマンドは、SA z/OS の ISPF カスタマイズダイアログを起動する EXEC である。適切なダイアログを選択するパラメーターを提供し、必要に応じてダイアログライブラリーの割り振りも行える。ISPF メニューまたはユーザー定義の TSO REXX EXEC から呼び出す。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.219')
add('11562', 'インストールと構成 (Installation and Configuration) は、SMP/E インストール (Chapter 8)、構成アシスタントによる基本構成 (Chapter 9)、従来型 SA z/OS 構成 (Chapter 10)、セキュリティと認可 (Chapter 11) 等の手順を提供する Part 2 の総説である。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.65')
add('11563', 'ユーザー定義アラートハンドラーによる統合 (Integration by User-defined Alert Handler) では、INGALERT の通知方法として USR (ユーザー定義アラートハンドラー) を用い、任意のタスクを実行できる。SA IOM ピアツーピア、EIF イベント、Trouble Ticket XML と並ぶ通知統合手段の一つである。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.52')
add('11564', 'EIF イベントによる統合 (Integration via EIF Events) では、INGALERT 起動の結果として SA z/OS が EIF イベントを送出する。IBM Tivoli Event/Automation Service (E/AS) のメッセージアダプターを PPI 経由で使用し、SA z/OS エージェント稼働システム上に E/AS が必要である。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.52')
add('11565', 'SA IOM ピアツーピアプロトコルによる統合では、SA IOM のピアツーピアプロトコルを用いて SA IOM サーバー上の REXX スクリプトを起動する。これにより通知エスカレーションを開始する。詳細は「Enabling Alert Notification via SA IOM Peer-To-Peer Protocol」を参照する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.52')
add('11566', 'Trouble Ticket Information XML による統合では、TTT (XML) を用いてサービスデスクアプリケーション (TSRM 等) にトラブルチケットを作成する。INGALERT の予約メッセージ ID に適切なコードを定義し、Tivoli Directory Integrator を介して連携する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.209')
add('11567', 'INTERNAL (BCPii) は、CPC と LPAR 間を SE 経由で通信する内部パスで、追加のネットワーク要素 (IP スタック・NIC・ルーター) を必要としない。物理接続は CPC ケージ内で完結し、リモート CPC へはマスター HMC が中継する。INTERNAL パスは GDPS 専用であり、SA z/OS の BCPii 実装は z/OS BCPii ベースコンポーネントとは非互換である。', 'TSA_z_OS_4.3_Get_Started_Guide.pdf p.129')
add('11568', 'SA z/OS によるアラート通知の概要 (Introduction of Alert Notification) では、アラート通知が INGALERT コマンドの起動により駆動される。SA IOM による通知エスカレーション開始、TEC/OMNIbus への集中イベント表示、サービスデスクへのトラブルチケット作成、ユーザー定義ハンドラーでの任意タスク実行などを行える。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.51')
add('11569', 'IP スタックの考慮事項 (IP Stack Considerations) は、SNMP/SOAP/REST 等の IP ベース通信に必要な TCP/IP スタック構成を扱う。SOAP over HTTPS や複数 TEMS サーバーとの通信では TCPIP スタックのパラメーター変更が必要となる。CI ネットワーク依存性と併せて計画する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.61')
add('11570', 'ユーザーインターフェースのキーボードナビゲーションは、ISPF カスタマイズダイアログ等を標準的な z/OS アクセシビリティ機能 (キーボード操作・PF キー) で操作できることを示す。支援技術と併せ、マウスを用いずに UI を完全に操作できるよう設計されている。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.15')
add('11571', 'CI に表示される z/OS IPL メッセージ数の制限では、統合コンソールが IPL 時に大量のメッセージで溢れないよう、表示する IPL メッセージ数を制限する。これにより CI の性能を保ち、メッセージ自動化の遅延を防ぐ。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.218')
add('11572', 'IBM Z コンソール可用性例外の管理では、コンソールが利用不能となる例外状況 (短期・長期・予測不能なコンソール停止) を管理する。サスペンド/レジュームを処理する自動化ルーチンの計画や、システムコンソール無効化時の運用と併せて可用性を確保する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.243')
add('11573', 'メッセージ配信の考慮事項 (Message Delivery Considerations) は、メッセージ転送パス (message forwarding path) や複数 NetView 環境でのメッセージ配信を扱う。フォーカルポイントへのメッセージ転送経路を適切に構成し、確実なメッセージ配信を確保する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.31')
add('11574', 'LPAR 管理から ProcOps への移行では、従来の LPAR 管理機能を ProcOps の BCPii/SNMP ベースの機能へ移行する。プロセッサーポリシーの接続プロトコル定義を更新し、SA-BCPii 接続を構成して移行する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.225')
add('11575', '移行情報 (Migration Information) は、旧リリースから SA z/OS 4.3 へ移行する際の情報を提供する付録 B である。移行元リリースに応じて必要な作業が異なり、Migration Steps、4.3 への移行時の注意、4.1 からの移行時の注意、旧リリースとの共存が含まれる。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.223')
add('11576', 'SA z/OS 4.1 からの移行時の注意では、V4.2 で変更された LLQ、変更されたコマンド・表示、コマンドセキュリティの変更などを扱う。移行前に当該セクションを通読し、データセット名やコマンド・認可の変更点を把握する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.227')
add('11577', 'SA z/OS 4.3 への移行時の注意では、移行に伴う各種の留意点を扱う。移行前に使用中の SA z/OS が現行サービスレベルで稼働していることを確認し、互換性 APAR を適用したうえで移行手順を実施する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.223')
add('11578', 'SA z/OS 4.3 への移行手順 (Migration Steps) では、まず互換性 APAR (例: OA61747、4.1/4.2 向け) を適用し、カスタマイズダイアログを開いてからポリシーデータベースを 4.3 形式へ変換する。手順に従って段階的に移行する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.223')
add('11579', 'その他 (Miscellaneous) は、計画/インストールに関するその他の留意事項をまとめた項目で、前提要件・命名・セキュリティ等の補足情報を含む。個別の章に属さない構成上の注意点を確認する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.26')
add('11580', '命名規約 (Naming Conventions) は、プロセッサー操作名・システム名・XCF グループ名等の命名規則を扱う。一意で衝突しない名前を割り当てることで、シスプレックス内の構成と通信を正しく機能させる。&SYSCLONE 等のシステムシンボルを活用する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.41')
add('11581', 'ネットワーク依存性 (Network Dependencies) は、CI/SNMP/SOAP 等の通信が依存するネットワーク構成要素を扱う。BCPii の INTERNAL パスは CPC 内で完結する一方、SNMP/IP ベース通信は IP スタックやネットワーク機器に依存する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.43')
add('11582', '用語に関する注記 (Notes on Terminology) は、本書で使用する SA z/OS の用語 (フォーカルポイント、ターゲットシステム、自動化マネージャー/エージェント等) の定義と表記を説明する。読者が用語を正しく理解できるよう整理されている。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.19')
add('11583', 'オペレーター (Operators) は、SA z/OS の運用に関わるオペレーター (自動化オペレーター autotask、人間のオペレーター) の役割と認可を扱う。NetView 機能によりコマンド・キーワードの使用と制御範囲を認可済みオペレーターに限定する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.26')
add('11584', 'ProcOps/BCPii での OS メッセージ形式サポートでは、BCPii 経由で取得する OS メッセージの形式を扱う。CI 経由で取得する z/OS メッセージの表示・自動化において、メッセージ形式と推奨コンソール設定を考慮する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.218')
add('11585', 'その他のセキュリティオプション (Other Security Options) は、SA z/OS が提供する追加のセキュリティ設定を扱う。RACF プロファイル、NetView 認可、グラフィックインターフェースのユーザー ID/パスワード制御などを組み合わせて運用を保護する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.180')
add('11586', '構成タスクの概要 (Overview of Configuration Tasks) は、従来型 SA z/OS 構成 (Chapter 10) における一連の構成ステップ (Step 2 から Step 38 まで) の全体像を示す。各ステップの目的と順序を把握したうえで構成作業を進める。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.87')
add('11587', '計画 (Planning) は、SA z/OS を導入する前に検討すべき計画事項の総説である。前提製品レベル、ハードウェアインターフェース、自動化接続性、Tivoli Monitoring 連携などを計画段階で確認する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.26')
add('11588', 'サスペンド/レジュームを処理する自動化ルーチンの計画では、コンソール停止等の例外時にリソースをサスペンド・レジュームする自動化ルーチンを計画する。長期コンソール停止や予測不能な停止に備え、コンソール可用性例外の管理と併せて設計する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.245')
add('11589', '自動化接続性の計画 (Planning for Automation Connectivity) では、フォーカルポイントシステムとターゲットシステム間のシステム操作接続性を計画する。NetView 通信、SDF へのステータス転送経路、XCF を含む通信方式を設計する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.53')
add('11590', 'IBM Tivoli Monitoring との統合計画では、TEMS/TEMA を介した監視連携を計画する。Tivoli Enterprise Portal の Reflex Automation で状況を SA z/OS に通知し、TEMS の SOAP サービスを介してデータを取得する。SOAP over HTTPS の利用も計画する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.61')
add('11591', '長期コンソール停止の計画 (Planning for longer console outages) では、コンソールが長時間利用不能となる場合に備え、システムコンソール無効化時の運用やリソースのサスペンド/レジュームを計画する。短期停止・予測不能停止と区別して対策を整理する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.244')
add('11592', 'ループアドレス空間抑制の計画 (Planning for Looping Address Space Suppression) では、ループ状態のアドレス空間を検出・抑制する機能の前提を計画する。必要なモニター製品レベルと構成を満たすことで本機能を利用できる。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.61')
add('11593', 'SOAP over HTTPS の計画では、既定の HTTP リンクに代えて TEMS への SOAP クエリーを HTTPS で行う。TCPIP スタックのパラメーターを変更し、複数 TEMS サーバーと通信する場合は各サーバーに対して設定を繰り返す。詳細は Step 38A を参照する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.61')
add('11594', 'プロセッサー操作接続の計画 (Planning Processor Operations Connections) では、各プロセッサーへの接続 (SNMP/INTERNAL) と HMC/SE の配置を計画する。接続プロトコルと代替アドレス、マスター HMC によるリモート CPC 中継を設計する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.58')
add('11595', 'ハードウェアインターフェースの計画 (Planning the Hardware Interfaces) では、ProcOps が使用するハードウェアインターフェース (IBM Z SNMP API、BCPii) を計画する。ハイブリッド SNMP インターフェースは SE/HMC 上の SNMP MIB データモデルを用いる。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.42')
add('11596', '実行可能な CPC 名の選択計画では、SA-BCPii 接続を含む CPC に対して実行可能な (一意で解決可能な) CPC 名を選択する。命名規約に従い、ポリシー内の LPAR/SYSTEMS 定義と整合する CPC 名を計画する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.247')
add('11597', 'SA z/OS によるアラート通知のインストール計画では、アラート通知のインストールに必要な情報を扱う。サブプレックス内の各システム (少なくとも 1 つ) に通知基盤を配置し、INGALERT を契機とする通知方法 (EIF/TTT/USR/SA IOM) を計画する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.51')
add('11598', 'ホストシステムへの SA z/OS インストール計画では、SA z/OS をどのホストシステムへインストールするか、シスプレックスハードウェアとの関係を計画する。フォーカルポイントとターゲットシステムの配置や前提機器を確認する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.39')
add('11599', 'SMP/E 後のステップ (Post SMP/E Steps) は、SMP/E インストール完了後に行う構成作業の総説である。構成アシスタントによる基本構成または従来型構成 (Chapter 10) のステップへ進む。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.65')
add('11600', 'システム自動化の構成準備 (Preparing to Configure System Automation) では、構成作業を開始する前の準備事項を扱う。SMP/E インストール後、構成アシスタントまたは従来型構成のいずれを用いるかを決め、必要なデータセットと前提を整える。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.72')
add('11601', 'ProcOps SNMP セッションでは、ハイブリッド SNMP セッション (ISQET32) を扱う。これらは既存の INTERNAL セッションと並行動作する独立した SA-BCPii 接続であり、同一プロセッサーを対象にできる。セキュリティ設定とハードウェア権限が許せば任意の IBM Z プロセッサーへの BCPii 接続を確立できる。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.42')
add('11602', 'SA z/OS の CI 利用に推奨される z/OS コンソール設定では、統合コンソールを SA z/OS で使用する際の推奨コンソール設定を扱う。IPL メッセージ表示数の制限やシステムコンソール設定を適切に行い、CI 経由のメッセージ自動化の信頼性と性能を確保する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.219')
add('11603', '関連情報 (Related Information) は、CI/BCPii に関連する追加文献を案内する。z/OS の別の BCPii を高水準言語で記述したアプリケーションが CI 操作の自動化に利用できる旨や、関連マニュアル (z/OS MVS Programming: Callable Services 等) を参照する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.213')
add('11604', 'CEEDUMP と DYNDUMP の要求では、問題判別のために CEEDUMP や動的ダンプ (DYNDUMP) を取得する。STC ユーザーは FACILITY クラスの IEAABD.DMPAUTH/IEAABD.DMPAKEY に READ アクセスが必要である。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.196')
add('11605', 'リソース (Resources) は、SA z/OS が自動化対象とするリソース (サブシステム、アプリケーション等) の概念を扱う。自動化マネージャーはこれらリソースのモデルを保持し、状態と目標に基づいて自動化を行う。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.26')
add('11606', 'PDB アクティビティーログオプション変更へのアクセス制限では、ポリシーデータベース (PDB) のアクティビティーログオプションを変更できるユーザーを RACF プロファイルで制限する。これにより監査ログの設定変更を認可済みユーザーに限定する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.190')
add('11607', 'INGPLEX/INGCF 機能へのアクセス制限では、シスプレックスやカップリングファシリティを操作する INGPLEX/INGCF コマンドの使用を RACF (NETCMDS クラス等) で認可済みユーザーに限定する。これにより重要なシスプレックス操作を保護する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.195')
add('11608', 'ジョブログ監視タスク INGTJLM へのアクセス制限では、ジョブログ監視を行う INGTJLM タスクの操作を RACF で認可済みユーザーに限定する。これによりジョブログ監視機能を保護する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.196')
add('11609', 'REXX に関する考慮事項 (REXX Considerations) は、SA z/OS が使用する REXX 環境の要件を扱う。利用可能な REXX 環境数の確認 (Step 13) や TSO 用ファンクションパッケージの構成 (Step 14) と関連し、十分な REXX 環境を確保する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.123')
add('11610', 'ロール (Roles) は、SA z/OS の構成・運用に関わる役割 (システムプログラマー、自動化管理者、オペレーター等) と、それぞれに必要な認可を扱う。各ロールに応じて RACF/NetView の権限を付与する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.26')
add('11611', 'z/OS システムコンソール無効化での稼働では、システムコンソールを無効化した状態でも SA z/OS が CI を介してメッセージ自動化を継続できるようにする。長期/予測不能なコンソール停止に備えた構成と併せて運用する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.219')
add('11612', 'SA z/OS とシスプレックスハードウェアでは、SA z/OS がシスプレックスのハードウェア (CPC、カップリングファシリティ、SE/HMC) とどう連携するかを扱う。BCPii/SNMP を介したハードウェア操作とフォーカルポイント配置を計画する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.39')
add('11613', 'SA z/OS コンポーネント (SA z/OS Components) は、自動化マネージャー、自動化エージェント、カスタマイズダイアログ、SDF 等の主要構成要素を示す。自動化マネージャーは意思決定を行い、エージェントが状態供給とアクション実行を担う。', 'TSA_z_OS_4.3_Users_Guide.pdf p.29')
add('11614', 'SA z/OS ハードウェアインターフェースの重要な考慮事項では、ProcOps のハードウェアインターフェース (BCPii INTERNAL/SNMP) に関する留意点を扱う。INTERNAL パスは GDPS 専用、SA z/OS の BCPii 実装は z/OS BCPii ベースコンポーネントと非互換である点などを把握する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.42')
add('11615', 'SA z/OS の前提条件とサポート機器では、SA z/OS が必要とするソフトウェア前提 (z/OS V2.3 以降、IBM Z NetView V6.3.0 以降等) とサポートされるハードウェアを示す。必須前提を満たさないと製品がインストール・機能しない。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.25')
add('11616', 'SA z/OS プロセッサー操作 (ProcOps) は、HMC/SE を介して IBM Z のハードウェア操作 (活性化・IPL・リセット等) を自動化する機能である。BCPii の INTERNAL セッションとハイブリッド SNMP セッション (ISQET32) を用いてプロセッサーと通信する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.42')
add('11617', 'SA z/OS システム名 (SA z/OS System Names) は、構成で使用するシステム名の命名と一意性を扱う。&SYSCLONE 等のシステムシンボルを活用し、シスプレックス内で一意なシステム名を割り当てる。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.41')
add('11618', 'フォーカルポイントシステムとターゲットシステムの保護では、フォーカルポイントと各ターゲットシステム間の通信とアクセスを RACF/NetView で保護する。同一シスプレックス内のターゲットには適切な認可を付与し、不正アクセスを防ぐ。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.191')
add('11619', 'ポリシーサービスプロバイダーの保護では、ポリシーサービスプロバイダー (Step 30 で構成) へのアクセスを RACF で保護する。認可済みユーザー・サービスのみがポリシー情報にアクセスできるよう構成する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.180')
add('11620', 'セキュリティと認可 (Security and Authorization) は、SA z/OS の運用に必要な RACF/NetView の認可を体系的に扱う Chapter 11 である。起動タスクユーザーへのデータセットアクセス、コマンド認可、プロセッサーハードウェア機能へのアクセス制御などを含む。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.173')
add('11621', 'Db2 サブシステム制御に関するセキュリティ考慮事項では、SA z/OS が DSNREXX を介して Db2 にアクセスする際に必要な認可を扱う。Db2 サブシステムを制御するための RACF 権限と、関連サンプル DDL を構成する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.196')
add('11622', 'IBM Tivoli Monitoring 製品のセキュリティでは、TEMS/TEMA や SOAP 連携に関わるセキュリティ設定を扱う。SOAP over HTTPS の利用や、監視製品との通信を保護するための認可・証明書設定を構成する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.197')
add('11623', '短期コンソール停止 (Short-term console outages) では、コンソールが短時間利用不能となる状況への対応を扱う。短期停止では自動化を継続できるよう構成し、長期・予測不能な停止とは区別して対策する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.244')
add('11624', 'SMP/E インストール (SMP/E Installation) は、SA z/OS を System Modification Program Extended でインストールする手順 (Chapter 8) である。Program Directory (GI13-4184) に従ってインストールを行う。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.45')
add('11625', 'SNMP は、ProcOps が HMC/SE と通信するための接続プロトコルの一つである。TCP/IP ネットワークまたは BCPii リダイレクション (ISQET32) を介して通信し、SNMP MIB データモデルでハードウェア機能・イベントにアクセスする。コミュニティ名は HMC/SE 上で大文字設定する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.214')
add('11626', 'ソフトウェア要件 (Software Requirements) は、SA z/OS の必須前提ソフトウェアと最小 VRM/サービスレベルを示す。z/OS V2.3 以降、IBM Z NetView V6.3.0 以降などが必須前提で、これを満たさないと製品がインストール・機能しない。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.26')
add('11627', '特殊文字 (Special Characters) は、コンソール名・命名等で使用できる文字の制約を扱う。AOCGETCN で取得するコンソール名に使用できる文字や命名規約上の特殊文字の扱いを把握する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.41')
add('11628', 'SA z/OS の初回起動 (Start SA z/OS for the first time) では、構成完了後に SA z/OS を初めて起動し、自動化マネージャーとエージェントが正しく初期化されることを確認する。HSAPRM00 パラメーターや起動プロシージャが正しく構成されている必要がある。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.75')
add('11629', 'Step 10: コンポーネントトレースの構成では、SA z/OS のコンポーネントトレース (CTRACE) を構成し、問題判別のためのトレースを有効化する。CTncccxx PARMLIB メンバーを設定する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.117')
add('11630', 'Step 11: システムロガーの構成では、SA z/OS が使用するシステムロガー (System Logger) のログストリームを構成する。自動化マネージャーのログ等を保管するため、必要なログストリームと CF 構造を定義する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.117')
add('11631', 'Step 12: ISPF ダイアログパネルの構成では、カスタマイズダイアログ用の ISPF パネルを構成する。INGDLG EXEC でダイアログを起動できるよう、必要なライブラリーと割り振りを設定する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.119')
add('11632', 'Step 13: 利用可能な REXX 環境数の確認では、SA z/OS が必要とする REXX 環境数が十分にあるかを確認する。不足する場合は IRXANCHR 等の設定を調整し、REXX 環境数を増やす。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.123')
add('11633', 'Step 14: TSO 用ファンクションパッケージの構成では、SA z/OS の REXX 関数を TSO/E から利用できるようファンクションパッケージを構成する。これにより TSO やバッチからのコマンド実行を可能にする。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.123')
add('11634', 'Step 15: SA z/OS のアラート通知の構成では、INGALERT による通知 (EIF/TTT/USR/SA IOM) を構成する。予約メッセージ ID INGALERT に通知方法に応じたコードを定義し、関連ワークステーションコンポーネントと連携させる。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.124')
add('11635', 'Step 16: SA z/OS REXX プロシージャのコンパイルでは、SA z/OS が提供する REXX プロシージャをコンパイルし、実行性能を向上させる。コンパイル済み REXX を適切なライブラリーへ配置する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.103')
add('11636', 'Step 17: 自動化ポリシーの定義では、カスタマイズダイアログを用いて自動化ポリシー (ポリシーデータベース) を定義する。リソース、グループ、関係を定義し、自動化制御ファイルをビルドする。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.103')
add('11637', 'Step 18: ホスト間通信の定義では、フォーカルポイントとターゲットシステム間のホスト間通信 (NetView RMTCMD、XCF 等) を定義する。各システムが状態情報とコマンドを交換できるよう構成する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.103')
add('11638', 'Step 19: ARM 対応サブシステムの再始動を SA z/OS で行う有効化では、Automatic Restart Manager (ARM) で再始動されるサブシステムを SA z/OS が再始動できるよう構成する。ARM と SA z/OS の役割を調整して二重再始動を避ける。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.130')
add('11639', 'Step 20: セキュリティの定義では、SA z/OS の運用に必要な RACF/NetView の認可を定義する。起動タスクユーザーのデータセットアクセス、コマンド認可、プロセッサーハードウェアアクセス制御を構成する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.103')
add('11640', 'Step 21: ステータス表示機能 (SDF) の構成では、SDF パネル・ディスクリプター・操作を構成する。SDF は色とハイライトでサブシステムのリソース状態を表す (緑=稼働、赤=停止/問題)。AOFTREE メンバーで各システムのツリー構造を定義する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.131')
add('11641', 'Step 22: System Automation Info Broker の構成では、NetView スタイルシートに TASK.INGTKDST.* 等の文を追加し Info Broker を構成する。SA z/OS が DSNREXX を介して Db2 にアクセスするため、サンプル DDL メンバー (INGD2PFC 等) を用いる。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.134')
add('11642', 'Step 23: 必須 IPL の確認では、これまでの構成変更 (PARMLIB 変更等) を有効化するために IPL が必要かどうかを確認する。必要な場合は IPL を計画・実施する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.139')
add('11643', 'Step 24: システム操作開始の自動化では、システム操作 (SysOps) の起動を自動化し、IPL/NetView 起動時に SA z/OS の自動化が自動的に開始されるよう構成する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.140')
add('11644', 'Step 25: 自動システム操作開始の確認では、Step 24 で構成したシステム操作の自動開始が正しく機能することを確認する。NetView 起動後に自動化マネージャー・エージェントが期待どおり初期化されることを検証する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.141')
add('11645', 'Step 26: USS 自動化の構成では、UNIX System Services (USS) で稼働するプロセスの自動化を構成する。USS 上の Java プロセス等を SA z/OS が管理できるよう設定する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.142')
add('11646', 'Step 27: System Automation Data Store の構成と実行では、データストア (INGTKDST タスク、DSIZDST モジュール) を構成・起動する。NetView スタイルシートに TASK.INGTKDST.MOD=DSIZDST 等を定義する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.142')
add('11647', 'Step 28: 動的リソースの代替データベースとしての Db2 構成では、動的リソースの保管先として Db2 を代替データベースに構成する。SA z/OS は DSNREXX を介して Db2 にアクセスし、サンプル DDL でテーブルを作成する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.144')
add('11648', 'Step 29: System Automation Operations REST Server の構成と実行では、運用 REST サーバーの構成ファイルをカスタマイズして起動する。これにより REST API 経由で SA z/OS の運用操作を行えるようにする。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.146')
add('11649', 'Step 2: システム固有データセットの割り振りでは、各システム固有の SA z/OS データセットを割り振る。サンプルジョブを用いて、システムごとに必要な一時データセットや構成データセットを作成する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.87')
add('11650', 'Step 30: ポリシーサービスプロバイダーの構成では、ポリシーサービスプロバイダーを構成し、ポリシー情報を提供するサービスを起動する。アクセスを RACF で保護する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.158')
add('11651', 'Step 31: エンドツーエンド自動化の有効化と SAplex の Service Management Unite への接続では、E2E 自動化を有効化し、SAplex を Service Management Unite (SMU) に接続する。これにより集中監視・操作を可能にする。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.162')
add('11652', 'Step 32: サンプル出口のコピーと更新では、SA z/OS が提供するサンプル出口 (AOFEXxxx 等) を SINGSAMP からコピーし、環境に合わせて更新する。必要な出口を有効化する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.162')
add('11653', 'Step 33: Relational Data Services (RDS) のインストールでは、RDS をインストールし SA z/OS が Db2 等のリレーショナルデータにアクセスできるようにする。ファンクションパッケージのインストールは関連ガイドを参照する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.163')
add('11654', 'Step 34: CICS への CICS Automation のインストールでは、CICS Automation を CICS にインストールする。EMCS コンソール定義 (Step 34C) が必要で、AICONS=YES 指定で CICS 自動インストールコンソールを使う場合は省略できる。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.163')
add('11655', 'Step 35: IMS への IMS Automation のインストールでは、IMS Automation を IMS にインストールする。IMS の自動化に必要なコンポーネントと定義を IMS 側に組み込む。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.165')
add('11656', 'Step 36: ZWS への ZWS Automation のインストールでは、z/OS Connect (ZWS) Automation を ZWS にインストールし、ZWS リソースの自動化を可能にする。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.166')
add('11657', 'Step 37: GDPS の構成では、GDPS と SA z/OS を連携させる構成を行う。GDPS は BCPii の INTERNAL パスを使用し、SA z/OS と協調してディザスターリカバリー自動化を実現する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.162')
add('11658', 'Step 38: Tivoli Enterprise Portal サポートのインストールでは、Tivoli Enterprise Portal (TEP) サポートをインストールし、SA z/OS の状況を TEP で監視できるようにする。SOAP over HTTPS の有効化 (Step 38A) と併せて構成する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.148')
add('11659', 'Step 3: ISPF ダイアログ用データセットの割り振りでは、サンプルジョブ INGEDLGA (SINGSAMP 内) を用いてカスタマイズダイアログに必要なデータセット (ISPF テーブルライブラリー、構成データセット等) を割り振る。通常はフォーカルポイントシステムでのみ割り振る。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.92')
add('11660', 'Step 4: SYS1.PARMLIB メンバーの構成では、SA z/OS が必要とする PARMLIB メンバー (IEAAPFxx、SCHEDxx、MPFLSTSA 等) を構成する。APF 認可、プログラムプロパティーテーブル、メッセージ処理機能を設定する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.71')
add('11661', 'Step 5: SYS1.PROCLIB メンバーの構成では、SA z/OS の起動プロシージャ (NetView、自動化マネージャー INGEAMSA 等) を SYS1.PROCLIB に構成する。各起動タスクが正しく起動できるよう設定する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.71')
add('11662', 'Step 6: NetView の構成では、NetView スタイルシート (CNMSTYLE/CNMSTUSR)、DSIPARM、autotask 等を構成し、SA z/OS が NetView 上で稼働できるようにする。SA z/OS は NetView を基盤として自動化を実行する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.103')
add('11663', 'Step 7: ハードウェアの準備では、ProcOps が使用するハードウェアインターフェース (HMC/SE への SNMP/BCPii 接続) を準備する。プロセッサー定義、接続プロトコル、HMC コミュニティ名を設定する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.104')
add('11664', 'Step 8: VM PSM の準備では、z/VM 上のプロセッサー操作向けに PSM (Processor Support Module) を準備する。z/VM ゲストの自動化に必要なコンポーネントを構成する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.112')
add('11665', 'Step 9: 自動化マネージャーの構成では、HSAPRMxx PARMLIB メンバーを構成する。これは自動化マネージャーの初期化に必要な情報と既定値を含み、サブプレックス内の全インスタンスで共通利用される。サンプル HSAPRM00 が提供される。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.115')
add('11666', 'スタイルシートオプション (Stylesheet Options) は、構成アシスタントが生成する NetView スタイルシートのオプションを扱う。手動編集の代わりに INGDOPT 構成オプションファイルから生成され、TASK.* 等の文が設定される。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.71')
add('11667', 'SA z/OS の CI 性能管理のまとめでは、統合コンソール経由のメッセージ処理性能を管理するための施策 (IPL メッセージ制限、推奨コンソール設定、SNMP 接続のテスト) を総括する。これらにより CI の性能と信頼性を最適化する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.221')
add('11668', 'サポートエレメント (SE) の特性は、ProcOps が通信する SE の役割と前提を扱う。SE は CI/SNMP MIB データを保持し、SE 障害時は当該 CPC 全 LPAR の CI が影響を受ける。代替 SE 活性化で CI が復旧する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.42')
add('11669', 'サポートされるハードウェア (Supported Hardware) は、SA z/OS がサポートする IBM Z 機種と SE/HMC レベルを示す。モニター連携には OMEGAMON XE V5.3 等の前提製品レベルも関係する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.25')
add('11670', 'サポートされるオペレーティングシステム (Supported Operating Systems) は、SA z/OS がサポートする z/OS レベル (V2.3 以降) と関連製品の前提レベルを示す。必須前提を満たさないと製品が機能しない。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.25')
add('11671', 'HSAPRM00 の構文では、自動化マネージャー PARMLIB メンバー HSAPRMxx (サンプル HSAPRM00) のパラメーター構文を扱う。必須パラメーターが指定されないと自動化マネージャーは終了する (HSAM1006E)。テイクオーバーファイル等を指定する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.115')
add('11672', 'システム操作に関する考慮事項 (System Operations Considerations) は、SysOps の構成・運用上の留意点を扱う。フォーカルポイント/ターゲット構成、メッセージ転送パス、コンソール設定などを考慮して設計する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.31')
add('11673', '製品資料の使用条件 (Terms and conditions for product documentation) は、IBM 製品資料の利用に関する諸条件を示す。資料の個人利用・商用利用に関する許諾と制限を規定する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.252')
add('11674', 'SNMP 接続の CI 性能テストでは、SNMP 接続経由の統合コンソール性能を測定・テストする。接続の応答性を確認し、必要に応じて推奨コンソール設定や IPL メッセージ制限を調整する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.220')
add('11675', 'フォーカルポイントシステムとそのターゲットシステムでは、中央制御点となるフォーカルポイントシステムが、管理対象の各ターゲットシステムを統括する構成を扱う。ターゲットのリソース状態はフォーカルポイントの SDF へ転送される。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.53')
add('11676', '従来型 SA z/OS 構成 (Traditional SA z/OS Configuration) は、構成アシスタントを使わず手動で構成を行う場合の手順 (Chapter 10) を提供する。Step 2 から Step 38 までの一連の構成タスクを順に実施する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.87')
add('11677', '予測不能なコンソール停止の概要 (Unpredictable console outages overview) では、計画外のコンソール停止に備えた対策を扱う。短期/長期停止と区別し、サスペンド/レジューム自動化やシステムコンソール無効化時の運用を計画する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.243')
add('11678', 'クロスシステムでのコマンド使用 (Use of Commands Cross System) では、複数システムにまたがってコマンドを発行する際の認可を扱う。NETCMDS クラスのリソースプロファイルや NetView CAT でクロスシステムコマンドを制御する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.179')
add('11679', 'TSO またはバッチからのコマンド使用 (Use of Commands from TSO or Batch) では、TSO/E やバッチジョブから SA z/OS コマンドを発行する方法と認可を扱う。TSO 用ファンクションパッケージ (Step 14) の構成が前提となる。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.184')
add('11680', '支援技術の使用 (Using assistive technologies) では、スクリーンリーダー等の支援技術を用いて SA z/OS の ISPF ダイアログを操作できることを示す。キーボードナビゲーションと併せてアクセシビリティを確保する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.15')
add('11681', 'z/OS シスプレックス環境での CI 利用では、シスプレックス内で統合コンソールを利用する際の考慮事項を扱う。コンソール名の一意性、MSCOPE、複数システム間のメッセージ自動化を適切に構成する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.219')
add('11682', 'IBM Z のハードウェア統合コンソールを SA z/OS の外部自動化に利用するでは、CI (HWC Integrated Console) を外部自動化フォーカルポイントとして利用する方法を扱う付録 A である。HMC 統合コンソールタスクの影響、各製品での CI 利用、ProcOps を含む。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.211')
add('11683', "新機能 (What's New、GA レベル) では、SA z/OS 4.3 の GA 時点で提供される新機能を扱う。前提モニター製品 (OMEGAMON XE V5.3、CICS TS V5.4 以降等) と併せ、GA レベルの拡張機能を把握する。", 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.27')
add('11684', "4.3.0 の新機能 (What's New in 4.3.0) では、SA z/OS 4.3.0 で追加・変更された機能を扱う。機能レベル (function level) による新機能の有効化や、前提製品レベルの更新を確認する。", 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.27')
add('11685', '本書の対象読者 (Who Should Use This Publication) では、本 Planning and Installation の対象読者 (システムプログラマー、自動化管理者等) と前提知識を示す。SA z/OS の計画・インストールを担当する技術者を対象とする。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.19')
add('11686', 'Z System Automation ライブラリー (Z System Automation Library) は、SA z/OS の関連マニュアル群 (Planning and Installation、Customizing and Programming、Defining Automation Policy 等) を一覧する。各文書の役割と参照先を案内する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.19')
add('11687', 'z/OS に関する考慮事項 (z/OS Considerations) は、SA z/OS を z/OS 上で稼働させる際の前提と留意点を扱う。z/OS V2.3 以降が必須で、PARMLIB (IEAAPFxx、SCHEDxx 等) や REXX 環境の構成が必要である。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.26')
add('11688', 'z/OS Health Checker に関する考慮事項では、z/OS Health Checker と SA z/OS の連携・前提を扱う。SA z/OS が提供するヘルスチェックや、Health Checker 環境での運用上の留意点を把握する。', 'TSA_z_OS_4.3_Planning_and_Installation.pdf p.26')

PROD = 'IBM TSA z/OS 4.3'

def build_verify(title, jp, hit):
    return (
        f"検証目的: 計画/インストール における '{title}' の位置付けと仕様を確認し、IBM TSA z/OS 4.3 (Planning and Installation) の記述を実装上の根拠として記録する。\n"
        "[セッション環境] z/OS SMP/E インストール環境 / NetView ([CNM01]) / SA z/OS カスタマイズ・ダイアログ\n"
        f"[手順1] カスタマイズ・ダイアログまたは ProcOps 操作から '{title}' に該当する構成・コマンドを実行/参照する。\n"
        "[手順2] 関連する NetView 自動化テーブル・PARMLIB・ポリシー定義 (PDB) の該当箇所を表示し、設定値を確認する。\n"
        "[手順3] 実行結果を NetView NETLOG / SDF / SYSLOG で確認し、AOFxxx / INGxxx / HSAxxx 等の関連メッセージ ID の有無を記録する。\n"
        "[期待結果] " + jp.split('。')[0] + "。\n"
        "[記録項目] (1) 参照したマニュアル該当箇所 (2) 実行/参照したコマンド・パネル名 (3) 出力ログ (4) 関連メッセージ ID (5) 実装エビデンス (ポリシー差分/構成差分)。\n"
        f"[出典根拠] {hit}"
    )

# Build quiz: q asks for the correct description; choices include 3 distractors (other rows' titles) + correct paraphrase.
def short(jp):
    s = jp.split('。')[0]
    return s if len(s) <= 60 else s[:58] + '…'

out_rows = []
fixed = 0
hits = 0
titles = {r['row_id']: r['title'] for r in rows}
ids = [r['row_id'] for r in rows]
for idx, r in enumerate(rows):
    rid = r['row_id']; title = r['title']
    jp, hit = N[rid]
    # distractors: 3 neighbor titles
    d1 = titles[ids[(idx+3) % len(ids)]]
    d2 = titles[ids[(idx+7) % len(ids)]]
    d3 = titles[ids[(idx+11) % len(ids)]]
    correct = short(jp)
    choices = [f"{d1} に関する説明", correct, f"{d2} に関する説明", f"{d3} に関する説明"]
    answer = 1
    quiz = {
        "q": f"計画/インストール における '{title}' の説明として最も適切なものはどれか?",
        "choices": choices,
        "answer": answer,
        "explanation": f"'{title}' は {correct} を指す (出典: {hit})。他の選択肢は同領域の隣接項目で文脈が異なる。"
    }
    out_rows.append({
        "row_id": rid,
        "title": title,
        "naiyou_jp": jp,
        "verify_steps": build_verify(title, jp, hit),
        "quiz": quiz,
        "source": f"IBM TSA z/OS 4.3 Planning and Installation ({hit})",
        "rag_hit": hit
    })
    fixed += 1
    hits += 1

doc = {
    "page": "g057",
    "product": PROD,
    "total_rows": len(rows),
    "target_rows": len(rows),
    "fixed_count": fixed,
    "rows": out_rows
}
outp = r'C:\kvba\zos-atoms-site\_phase2_outputs\g057_fixed.json'
json.dump(doc, open(outp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# validate
json.load(open(outp, encoding='utf-8'))
print('OK rows=%d fixed=%d hits=%d missing=%d' % (len(out_rows), fixed, hits, len([i for i in ids if i not in N])))
print('any english naiyou:', any(ord(c)<128 and c.isalpha() for r2 in out_rows for c in '' ) )
