# -*- coding: utf-8 -*-
import json,os
BASE=os.path.dirname(__file__)
CJSON=os.path.join(BASE,'_g052_content.json')
C=json.load(open(CJSON,encoding='utf-8'))
PDF="TSA_z_OS_4.3_Customizing_and_Programming.pdf"
def add(rid,naiyou,steps,q,choices,answer,expl,rag,src=None):
    C[rid]=dict(naiyou=naiyou,steps=steps,q=q,choices=choices,answer=answer,expl=expl,rag=rag,src=src or PDF)

add("10537",
"z/OS UNIX リソースのカスタマイズでは、z/OS UNIX System Services が SA z/OS にどのように統合されるかに基づき、USS アプリケーション向けの定義を行う。プロセス（コマンド/パスとユーザー ID で表現）、TCP ポート、ファイル/ファイル・システムなどの監視ルーチンや、起動/停止定義を構成する。*USS ベスト・プラクティス・ポリシーが sshd などのデーモンの定義を提供する。",
["カスタマイズ・ダイアログで USS アプリケーションの起動/停止定義と監視ルーチンを設定する。",
 "監視対象としてプロセス（コマンド/パス・ユーザー ID）、TCP ポート、ファイルのいずれかを指定する。",
 "*USS ベスト・プラクティス・ポリシー（C_USS_xxx クラス）を活用する。",
 "INGLIST で USS リソースが認識・監視されていることを確認する。"],
"z/OS UNIX リソースの監視対象として正しくないものはどれか?",
["プロセス（コマンド/パス）","TCP ポート","ファイル/ファイル・システム","カップリング・ファシリティー構造"],3,
"USS リソースではプロセス・TCP ポート・ファイル/ファイル・システムを監視できるが、CF 構造は USS 監視の対象ではない。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.103 / p.324")

add("10539",
"プロキシー・リソースの自動化をカスタマイズする際、Restart after IPL オプションを NO に設定すると、プロキシー・リソース（つまりプロセッサー・オペレーション・ターゲット・システム）が IPL 時に自動起動されないようにできる。プロキシー・アプリケーションはタイプ SYSTEM・Nature BASIC・Behavior PASSIVE の APG にリンクし、Automation Name を空にしてグループ用リソースが作成されないようにする。",
["カスタマイズ・ダイアログでプロキシー APL の Restart after IPL を必要に応じて NO に設定する。",
 "プロキシー APL をタイプ SYSTEM・Nature BASIC・Behavior PASSIVE の APG にリンクする。",
 "APG の Automation Name を空にしてリソースが作成されないようにする。",
 "INGLIST でプロキシー・リソースの自動起動挙動を確認する。"],
"プロキシー・リソースを IPL 時に自動起動させないために設定するオプションはどれか?",
["Boost フィールド = NO","Restart after IPL = NO","ALERTMODE = OFF","Inform List = なし"],1,
"Restart after IPL を NO に設定するとプロキシー・リソースは IPL 時に自動起動されない。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.91 / p.90")

add("10540",
"SA z/OS は応答済みでない（未応答の）すべての WTOR を追跡し、SDF を介して表示する。WTOR の保管方法をカスタマイズでき、アクションが定義されていない WTOR は OUTREP により保管され、そのための自動化テーブル文が作成される。SA z/OS は WTOR からどの可変情報を抽出し、それをコード値として関連コマンドへ渡すかも定義できる。",
["未応答の WTOR を発生させ SA z/OS が追跡し SDF に表示することを確認する。",
 "アクション未定義の WTOR が OUTREP により保管されることを確認する。",
 "MESSAGES/USER DATA で WTOR からの可変情報抽出とコード値の受け渡しを定義する。",
 "SDF パネルで未応答 WTOR の一覧を確認する。"],
"アクションが定義されていない着信 WTOR を保管するために使われる仕組みはどれか?",
["REP アクション","OUTREP","INGALERT","ACFREP"],1,
"アクション未定義の WTOR は OUTREP により保管され、対応する自動化テーブル文が生成される。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.166")

add("10541",
"ターゲット・システムのカスタマイズでは、プロセッサー・オペレーションのデータ・モデルが各 LPAR/イメージに固有のターゲット・システム名を要求するため、カスタマイズ・ダイアログの Processors エントリー > LPARS AND SYSTEMS ポリシーで LPAR とターゲット・システム名を定義する。TARGET SYSTEM INFO ポリシーで時間帯・メッセージ受信オペレーター・コンソールなどの基本情報を、IPL 時の重要なオペレーター・プロンプト・メッセージへの自動応答を指定できる。",
["カスタマイズ・ダイアログの Processors > LPARS AND SYSTEMS で LPAR とターゲット・システム名を定義する。",
 "TARGET SYSTEM INFO ポリシーで時間帯・コンソール・IPL プロンプト応答を設定する。",
 "AOF_AAO_ISQ_DYNTGT を使う場合は動的ターゲット・システム名の設定を確認する。",
 "INGLIST/ISQ コマンドでターゲット・システムが定義どおり認識されることを確認する。"],
"ターゲット・システムの LPAR とターゲット・システム名を定義するポリシーはどれか?",
["MONITOR INFO","LPARS AND SYSTEMS","MESSAGES/USER DATA","AUTOMATION FLAGS"],1,
"プロセッサー・オペレーションでは LPARS AND SYSTEMS ポリシーで各 LPAR とターゲット・システム名を定義する。",
"TSA_z_OS_4.3_Users_Guide.pdf p.255")

add("10542",
"状況表示機能（SDF）のカスタマイズでは、SDF のパネル・記述子・操作をカスタマイズする方法を扱う。SDF は色と強調表示でサブシステム・リソースの状態を表現し、緑は稼働、赤は停止/問題状態を示す。SDF 状況パネルは任意の環境を反映するようカスタマイズでき、例えば全プロセッサーの全 JES サブシステムの状況を表示するパネルを定義できる。",
["AOFTREE/AOFPNLS メンバーで SDF のツリー構造とパネルを定義する。",
 "AOFINIT メンバーで SDF 初期化パラメーター（PF キー・色・優先順位）を設定する。",
 "SDF コマンドでオペレーター・セッションを開始しパネルを表示する。",
 "緑=稼働、赤=停止/問題の色表現が正しく反映されることを確認する。"],
"SDF で稼働中のサブシステムを表す色はどれか?",
["赤","緑","黄","白"],1,
"SDF は色でリソース状態を表し、緑が稼働、赤が停止/問題状態を示す。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.251 / p.257")

add("10543",
"システムをこれらの機能で使用するためのカスタマイズでは、シスプレックス自動化で提供される各機能（CDS・CF・システム・ロガー・リカバリー・アクション・ハードウェア検証）を SA z/OS カスタマイズ・ダイアログで有効化し、リカバリー・フラグなどの自動化フラグを設定する。フラグ自動化指定でリカバリー・フラグを NO に設定して無効化でき、実行時には INGAUTO コマンドで変更できる。",
["カスタマイズ・ダイアログのフラグ自動化指定でリカバリー・フラグを設定する。",
 "シスプレックス自動化機能（CDS/ENQ など）の最小リソース名を指定する。",
 "実行時に INGAUTO コマンドで自動化リカバリー・フラグを変更できることを確認する。",
 "INGLIST でリカバリー・フラグの設定状態を確認する。"],
"自動化リカバリー・フラグを実行時に変更するコマンドはどれか?",
["INGAMS","INGAUTO","INGREQ","INGALERT"],1,
"自動化リカバリー・フラグは実行時に INGAUTO コマンドで変更できる。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.151")

add("10544",
"SOAP サーバーのカスタマイズでは、SA z/OS カスタマイズ・ダイアログのエントリー・タイプ（Networks の SOAP SERVER ポリシー項目）で、ホスト名/IP アドレス、SOAP サーバーのポート、SOAP サービスのパス名を定義する。OMEGAMON を用いたヘルス監視などで、PIPE と NETVASIS を使って SOAP リクエストを発行できる。",
["カスタマイズ・ダイアログの Networks > SOAP SERVER でホスト名/IP・ポート・パスを定義する。",
 "SOAP サーバー属性パネルでサーバー名・説明を設定する。",
 "PIPE（NETVASIS）で SOAP リクエストを発行し応答を取得する。",
 "NETLOG で SOAP サーバーへの接続と応答を確認する。"],
"SOAP サーバーの定義に含まれない項目はどれか?",
["ホスト名/IP アドレス","SOAP サーバーのポート","SOAP サービスのパス名","カップリング・ファシリティー名"],3,
"SOAP サーバー定義にはホスト名/IP・ポート・サービスのパス名が含まれるが、CF 名は関係しない。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.54 / Defining_Automation_Policy.pdf p.299")

add("10547",
"TSO 配下でビュー/編集するための RDS 作業データ・セットの定義では、専用 PDS の一時メンバーを使ってテーブルを表示・編集する。NetView と TSO はこの PDS への読み書きアクセスが必要で、PDS はこの機能専用とする。最大レコード長は最長のテーブル行を収容できる十分な大きさが必要である。INGRDS EDIT/VIEW を呼び出した TSO ユーザーごとに、その TSO ユーザー ID を用いて一意の一時メンバーが作成される。",
["RDS ビュー/編集専用の PDS を割り振り、NetView と TSO に読み書きアクセスを付与する。",
 "PDS の最大レコード長が最長テーブル行を収容できることを確認する。",
 "TSO で INGRDS EDIT または VIEW を実行する。",
 "TSO ユーザー ID に基づく一意の一時メンバーが作成されることを確認する。"],
"RDS 作業データ・セット（PDS）の一時メンバーは何に基づいて一意に作成されるか?",
["ジョブ名","TSO ユーザー ID","NetView ドメイン ID","シスプレックス名"],1,
"INGRDS EDIT/VIEW を呼び出した TSO ユーザーの ID を用いて一意の一時メンバーが作成される。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.132 / p.5")

add("10548",
"アプリケーション・ポリシー・オブジェクトの定義では、カスタマイズ・ダイアログでエントリー・タイプ Application（APL）のオブジェクトを作成し、サブシステム名・ジョブ・タイプ・起動/停止コマンドなどを指定する。定義後、APG 経由でシステム/シスプレックスにリンクして自動化対象とする。サブシステム名を指定しない場合はエントリー名がデフォルトとなる。",
["カスタマイズ・ダイアログのエントリー・タイプ選択で Application（APL）を選ぶ。",
 "サブシステム名・ジョブ・タイプ・起動/停止コマンドを定義する。",
 "APL を APG 経由でシステム/シスプレックスにリンクする。",
 "構成をビルドし INGLIST で APL が認識されることを確認する。"],
"アプリケーション・ポリシー・オブジェクトを定義するエントリー・タイプはどれか?",
["System（SYS）","Application（APL）","Monitor（MTR）","Network（NET）"],1,
"アプリケーション・ポリシー・オブジェクトはエントリー・タイプ Application（APL）として定義する。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.25 / Defining_Automation_Policy.pdf p.177")

add("10550",
"Automatic Restart Manager 用の MOVE グループの定義では、MOVE グループ内のアプリケーションが自動化マネージャーによる再始動の前に ARM から完全に登録解除されるよう、ARM 化された各アプリケーションに対し MOVE グループを supporting リソースとする Prepareavailable/WhenObservedDown（受動）関係を定義する。MOVE グループにリンクしたアプリケーションが起動されるよう、HardDown 状態にせず Start On IPL を NO にしないようにする。",
["カスタマイズ・ダイアログで ARM 化アプリケーションに MOVE グループを supporting とする Prepareavailable/WhenObservedDown 関係を定義する。",
 "アプリケーションを HardDown 状態にせず、Start On IPL を NO にしないことを確認する。",
 "MOVE グループ・メンバーをアベンドさせ、ARM 登録解除後に自動化マネージャーが再始動することを確認する。",
 "INGLIST で MOVE グループ内アプリケーションの状況を確認する。"],
"MOVE グループ内 ARM 化アプリケーションに定義する関係はどれか?",
["HasParent","Prepareavailable/WhenObservedDown","HasMonitor","MakeAvailable/WhenAvailable"],1,
"ARM 登録解除を保証するため、Prepareavailable/WhenObservedDown（受動）関係を MOVE グループを supporting として定義する。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.268")

add("10551",
"VTAM アプリケーションを SA z/OS に定義する際は、SHUTDOWN FINAL 定義を行い、アプリケーション稼働中に VTAM が再始動された場合にメジャー・ノードを再アクティブ化できるよう、VTAM サブシステムの UP メッセージ/ユーザー・データ・ポリシーに INGVTAM コマンドをコーディングする。VTAM アプリケーションのリカバリーを有効にするには、INGVTAM を用いてサブシステムを SA z/OS リカバリー・コードに登録する。",
["カスタマイズ・ダイアログで VTAM アプリケーションと SHUTDOWN FINAL を定義する。",
 "VTAM サブシステムの UP メッセージ/ユーザー・データ・ポリシーに INGVTAM をコーディングする。",
 "VTAM 再始動時にメジャー・ノードが再アクティブ化されることを確認する。",
 "INGVTAM によりサブシステムが SA z/OS リカバリーに登録されることを NETLOG で確認する。"],
"VTAM 再始動時にメジャー・ノードを再アクティブ化するためコーディングするコマンドはどれか?",
["INGREQ","INGVTAM","INGAUTO","INGALERT"],1,
"VTAM サブシステムの UP メッセージ/ユーザー・データ・ポリシーに INGVTAM をコーディングし、再始動時のメジャー・ノード再アクティブ化を行う。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.157")

add("10552",
"ARM エレメント名の定義では、Automatic Restart Manager がエレメント名を使ってアプリケーションを識別するため、ARM 対応の各アプリケーションは ARM とのすべての通信で使う一意のエレメント名を持つ必要がある。エレメント名はアプリケーションのエントリー・パネル、またはポリシー項目 APPLICATION INFO の MVS Automatic Restart Management Element Name フィールドで指定する。",
["カスタマイズ・ダイアログのアプリケーション・エントリーまたは APPLICATION INFO で MVS ARM Element Name を指定する。",
 "各 ARM 対応アプリケーションに一意のエレメント名を割り当てる。",
 "アプリケーションを ARM 登録し、エレメント名で識別されることを確認する。",
 "ARM による再始動時にエレメント名が使用されることを確認する。"],
"ARM エレメント名はどのフィールドで指定するか?",
["Boost フィールド","MVS Automatic Restart Management Element Name","Inform List","ALERTMODE"],1,
"ARM エレメント名は APPLICATION INFO の MVS Automatic Restart Management Element Name フィールドで指定する。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.267 / p.268")

add("10553",
"SDF フォーカル・ポイント・システムの定義では、状況表示機能（SDF）のフォーカル・ポイントを定義する。SDF は色と強調表示でリソース状態を表示し、フォーカル・ポイント・システムが監視・制御を集中させる。自動化ネットワーク定義プロセスの一部として、フォーカル・ポイント、ターゲット・システム、ゲートウェイ・セッションを定義する。",
["カスタマイズ・ダイアログで SDF フォーカル・ポイント・システムを定義する。",
 "フォーカル・ポイントとターゲット・システム間のゲートウェイ・セッションを定義する。",
 "SDF コマンドでフォーカル・ポイントから各システムの状況を表示する。",
 "ターゲット・システムの状況変化がフォーカル・ポイント SDF に反映されることを確認する。"],
"SDF フォーカル・ポイント・システムの役割として最も適切なものはどれか?",
["SMF レコードの集計","監視・制御を集中させる中心システム","RDS テーブルの保管","CF 構造のリバランス"],1,
"SDF フォーカル・ポイント・システムは監視・制御を集中させ、ターゲット・システムの状況を表示する中心となる。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.251 / p.153")

add("10554",
"自動起動 TAF（Terminal Access Facility）フルスクリーン・セッションの定義では、Fullscreen TAF Application Definition パネルを用いて、SA z/OS が自動的に開始する TAF フルスクリーン・セッションを定義する。これは自動化ネットワーク（ネットワーク自動化）の章の一部であり、オペレーターの介入なしにアプリケーションへのフルスクリーン・セッションを確立できる。",
["カスタマイズ・ダイアログの Fullscreen TAF Application Definition パネルで TAF セッションを定義する。",
 "自動起動対象のアプリケーションとセッション・パラメーターを指定する。",
 "構成をビルドし SA z/OS が TAF フルスクリーン・セッションを自動開始することを確認する。",
 "NETLOG でセッション確立を確認する。"],
"自動起動 TAF フルスクリーン・セッションを定義するために使うパネルはどれか?",
["Monitor Resource Information パネル","Fullscreen TAF Application Definition パネル","SOAP-Server Attributes パネル","Local Page Data Set Recovery パネル"],1,
"自動起動 TAF フルスクリーン・セッションは Fullscreen TAF Application Definition パネルで定義する。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.155 / p.156")

json.dump(C,open(CJSON,'w',encoding='utf-8'),ensure_ascii=False)
print("total:",len(C))
