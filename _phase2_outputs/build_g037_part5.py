# -*- coding: utf-8 -*-
import json, os
rows=[]
def add(rid,title,naiyou,verify,q,choices,ans,expl,source,rag):
    rows.append({"row_id":rid,"title":title,"naiyou_jp":naiyou,"verify_steps":verify,
    "quiz":{"q":q,"choices":choices,"answer":ans,"explanation":expl},"source":source,"rag_hit":rag})

add("7485","Customizing Alert and Message Routing from the NetView program",
"NetView プログラムからのアラートおよびメッセージのルーティングをカスタマイズできる。Event/Automation Service を介して、アラートを EIF イベントや SNMP トラップへ変換し、メッセージアダプターを通じて自動化テーブルのメッセージを EIF イベントへ変換して、指定のイベントサーバーへ転送する。ハードウェアモニターの TRAPROUTE／AREC フィルターをPASSに設定することでアラートを転送できる。",
"ハードウェアモニターの TRAPROUTE と AREC フィルターを SRFILTER で PASS に設定する。Event/Automation Service を始動し、アラート／メッセージが指定先へルーティングされることを確認する。",
"NetView からアラートをアラート・ツー・トラップへルーティングするために PASS にするフィルターはどれか。",
["TRAPROUTE と AREC","TASK と AUTOTASK","KCLASS と PCLASS","COLOR と XHILITE"],0,
"アラートを転送するにはハードウェアモニターの TRAPROUTE と AREC フィルターを PASS にする。",
"NetView_6.4_Customization_Guide.pdf p.127","NetView_6.4_Installation_Configuring_Additional_Components.pdf p.220 TRAPROUTE AREC PASS"),

add("7486","Customizing Hardware Monitor Displayed Data",
"ハードウェアモニターの表示データをカスタマイズし、汎用および非汎用アラートの表現を変更できる。非汎用の Recommended Action パネルや Event Detail パネルのテキスト変更、非汎用アラートメッセージの変更、汎用アラートからの推奨アクション番号の上書き、色と強調表示の制御、ユーザー定義エラーの組み込みなどが行える。",
"カラーマップやパネルメンバー、コードポイントテーブルを編集してハードウェアモニター表示をカスタマイズする。NPDA でイベント明細やアラートを表示し、変更が反映されていることを確認する。",
"ハードウェアモニター表示データのカスタマイズに含まれるものはどれか。",
["推奨アクション番号の上書きや色・強調表示の制御","RACF プロファイルの作成","VTAM 始動オプション変更","SMF データセット割り当て"],0,
"推奨アクション番号の上書きや色・強調表示の制御などがカスタマイズに含まれる。",
"NetView_6.4_Customization_Guide.pdf p.85","NetView_6.4_Customization_Guide.pdf p.85 customizing hardware monitor displayed data"),

add("7487","Customizing PF Keys and Immediate Message Line",
"PF キーと即時メッセージ行をカスタマイズできる。PF キーは CNMKEYS メンバーや PFKDEF コマンドで定義し、コンポーネントごと、または全体で設定値を変更できる。dispfk all コマンドで全 PF キー設定を表示できる。即時メッセージ行の表示位置や内容も調整できる。",
"CNMKEYS メンバーを編集して PF キーを定義し、NetView を再初期化する。コンソールで dispfk all を発行し、PF キー設定が変更どおりであることを確認する。",
"全 PF キー設定を表示するコマンドはどれか。",
["dispfk all","TASKUTIL","GENALERT","SRFILTER"],0,
"dispfk all で全 PF キー設定を表示できる。",
"NetView_6.4_Customization_Guide.pdf p.39","NetView_6.4_Users_Guide_NetView.pdf p.62 CNMKEYS dispfk all"),

add("7488","Customizing Session Monitor Sense Descriptions",
"セッションモニターのセンス記述（sense description）をカスタマイズできる。センスコードに対応する説明テキストを変更することで、セッション関連の問題診断時に表示される記述を自社環境に合わせられる。セッションモニターのセンスコードはオンラインヘルプや資料で参照できる。",
"セッションモニターのセンス記述を定義するメンバーを編集して説明テキストを変更し、NetView を再初期化する。NLDM（セッションモニター）でセンスコードを表示し、記述が変更どおりであることを確認する。",
"セッションモニターのセンス記述をカスタマイズする目的はどれか。",
["センスコードに対応する説明テキストを変更する","VTAM ノードを活動化する","RODM クラスを定義する","SMF を採取する"],0,
"センス記述のカスタマイズはセンスコードに対応する説明テキストを変更するためのものである。",
"NetView_6.4_Customization_Guide.pdf p.81","NetView_6.4_Customization_Guide.pdf p.81 session monitor sense descriptions"),

add("7489","Customizing the Event/Automation Service",
"Event/Automation Service のカスタマイズでは、初期化、構成ファイル、始動パラメーターを調整する。サービスはメッセージアダプター、確認付きメッセージアダプター、イベントレシーバー、アラート・ツー・トラップ、トラップ・ツー・アラートなどの機能を提供し、それぞれの構成ファイルで動作を制御する。",
"Event/Automation Service の構成ファイル群（IHSAMCFG 等）と始動パラメーターを編集する。IHSAEVNT ジョブでサービスを始動し、各サービスが構成どおりに初期化されることを確認する。",
"Event/Automation Service が提供する機能に含まれるものはどれか。",
["メッセージアダプターやアラート・ツー・トラップ","VTAM ノード活動化","RACF 認証","SMF 採取"],0,
"メッセージアダプターやアラート・ツー・トラップなどが Event/Automation Service の機能である。",
"NetView_6.4_Customization_Guide.pdf p.115","NetView_6.4_Customization_Guide.pdf p.115 EAS services overview"),

add("7490","Customizing the Event/Automation Service Configuration Files",
"Event/Automation Service の構成ファイルをカスタマイズする。構成ファイルには IHSAACFG（アラートアダプター）、IHSABCFG（確認付きアラートアダプター）、IHSAATCF（アラート・ツー・トラップ）、IHSATCFG（トラップ・ツー・アラート）、IHSAMCFG（メッセージアダプター）、IHSANCFG（確認付きメッセージアダプター）がある。UNIX System Services から始動する場合は /etc/netview 配下の .conf ファイルが既定で読み込まれる。",
"対象の構成ファイル（例: IHSAMCFG）を編集し、サービス固有のステートメントを設定する。Event/Automation Service を再始動し、構成ファイルの変更が反映されることを確認する。",
"メッセージアダプターの構成ファイル名はどれか。",
["IHSAMCFG","IHSAATCF","IHSATCFG","IHSAACFG"],0,
"メッセージアダプターの構成ファイルは IHSAMCFG である。",
"NetView_6.4_Customization_Guide.pdf p.123","NetView_6.4_Customization_Guide.pdf p.124 / Administration_Reference p.495 config files"),

add("7491","Customizing the Event/Automation Startup Parameters",
"Event/Automation Service の始動パラメーターをカスタマイズできる。設定可能項目にはアラート・ツー・トラップのコミュニティー名（既定 public）、エンタープライズオブジェクト ID、トラップ・ツー・アラートの PPI 名（既定 NETVALRT）、ポート番号（既定 162）などがあり、それぞれ構成ファイルのステートメントで上書きできる。",
"始動パラメーター（コミュニティー名、ポート番号など）を構成ファイルで設定する。サービスを始動し、設定したパラメーターが有効になっていることをトレースまたは動作で確認する。",
"トラップ・ツー・アラートの既定ポート番号はどれか。",
["162","public","NETVALRT","1588"],0,
"トラップ・ツー・アラートの既定ポート番号は 162 である。",
"NetView_6.4_Customization_Guide.pdf p.121","NetView_6.4_Customization_Guide.pdf p.121 startup parameters defaults"),

add("7492","Customizing the IBM Tivoli Enterprise Console",
"IBM Tivoli Enterprise Console（TEC）と連携するためのカスタマイズを行う。Event/Automation Service のアラートアダプターやメッセージアダプターが NetView のアラート・メッセージを EIF イベントへ変換し、TEC などのイベントサーバーへ転送する。イベントクラス定義やルールファイルを調整する。",
"メッセージ／アラートアダプターの構成ファイルと EIF イベントクラス定義を TEC 連携用に編集する。Event/Automation Service を始動し、生成された EIF イベントが TEC で受信されることを確認する。",
"TEC 連携で NetView のアラートが変換される形式はどれか。",
["EIF イベント","SMF レコード","RODM オブジェクト","VTAM セッション"],0,
"TEC 連携ではアラート・メッセージが EIF イベントへ変換され転送される。",
"NetView_6.4_Customization_Guide.pdf p.167","NetView_6.4_Users_Guide_NetView.pdf p.127 EIF events event server"),

add("7493","Customizing the Initialization of the Event/Automation Service",
"Event/Automation Service の初期化をカスタマイズする。z/OS システムコンソールから始動する場合は IHSAEVNT ジョブを使用し、UNIX System Services シェルから始動する場合は /etc/netview/global_init.conf などのファイルから定義ステートメントを読み込む。初期化時に各サービスの設定可能項目の既定値が適用される。",
"グローバル初期化ファイル（IHSAINIT または global_init.conf）を編集し、初期化で読み込むサービスを指定する。サービスを始動し、初期化が構成どおりに行われることを確認する。",
"Event/Automation Service を z/OS コンソールから始動するジョブはどれか。",
["IHSAEVNT","IHSAMCFG","IHSAATCF","CNMSJM01"],0,
"z/OS コンソールからは IHSAEVNT ジョブで始動する。",
"NetView_6.4_Customization_Guide.pdf p.116","NetView_6.4_Installation_Configuring_Additional_Components.pdf p.220 IHSAEVNT global_init.conf"),

add("7494","Customizing the NetView Command Facility Panel",
"NetView コマンド機能（NCCF）パネルをカスタマイズできる。コマンド行、即時メッセージ行、PF キー、画面の色や強調表示などを調整し、オペレーターの操作画面を自社環境に合わせる。画面フォーマット定義ステートメントや CNMKEYS により表示を制御する。",
"画面フォーマット定義や CNMKEYS を編集してコマンド機能パネルの表示をカスタマイズし、NetView を再初期化する。NCCF パネルを表示し、レイアウトや PF キーが変更どおりであることを確認する。",
"NetView コマンド機能パネルのカスタマイズ対象に含まれるものはどれか。",
["コマンド行・PF キー・色などの画面表示","VTAM NCP 定義","RACF データベース","SMF データセット"],0,
"コマンド行・PF キー・色などの画面表示がカスタマイズ対象である。",
"NetView_6.4_Customization_Guide.pdf p.41","NetView_6.4_Customization_Guide.pdf p.39 PF keys immediate message line"),

with open(os.path.join(os.path.dirname(__file__),'_g037_part5.json'),'w',encoding='utf-8') as f:
    json.dump(rows,f,ensure_ascii=False)
print("part5",len(rows))
