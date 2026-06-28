# -*- coding: utf-8 -*-
import json, os
rows=[]
def add(rid,title,naiyou,verify,q,choices,ans,expl,source,rag):
    rows.append({"row_id":rid,"title":title,"naiyou_jp":naiyou,"verify_steps":verify,
    "quiz":{"q":q,"choices":choices,"answer":ans,"explanation":expl},"source":source,"rag_hit":rag})

add("7503","Determining a Panel Name",
"ハードウェアモニターの非汎用パネルを変更する際は、対象パネルのパネル名を特定する必要がある。パネルには実際（actual）名と別名（alias）があり、ブロック ID とアラート記述コードから NMVT がパネル ID へマップされる。パネル名を特定したうえでテキストや色を変更する。",
"NPDA でイベント明細を表示し、対象パネルの実際名／別名を確認する。該当パネルメンバーを編集し、HELP やイベント表示で正しいパネルが更新されていることを確認する。",
"ハードウェアモニターパネルが持つ名前の種類はどれか。",
["実際（actual）名と別名（alias）","主名と副名のみ","RODM 名のみ","VTAM ノード名"],0,
"パネルには実際（actual）名と別名（alias）がある。",
"NetView_6.4_Customization_Guide.pdf p.85","NetView_6.4_Customization_Guide.pdf p.190 actual alias panel name"),

add("7504","Displaying New Help Panels",
"新しいヘルプパネルを作成した後は、HELP コマンドを使ってそのパネルおよび関連するコマンドやパネルを表示し、正しく表示されることを確認する。MYCOMAND のように、独自コマンドに対応するヘルプパネルを作成して動作確認を行う。",
"新しいヘルプソースを作成・格納した後、HELP コマンド（例: HELP MYCOMAND）を発行する。表示されたヘルプパネルと関連パネルが正しくレイアウトされていることを確認する。",
"新しいヘルプパネルの表示確認に使うコマンドはどれか。",
["HELP","VIEW のみ","SRFILTER","TASKUTIL"],0,
"新しいヘルプパネルは HELP コマンドで表示して確認する。",
"NetView_6.4_Customization_Guide.pdf p.80","NetView_6.4_Customization_Guide.pdf p.80 Displaying New Help Panels HELP"),

add("7505","Displaying Special Attributes",
"パネルでは特殊属性を表示できる。属性シンボルや属性変数を用いて、フィールドの色、強調表示、保護／非保護、入力可否などの特殊属性を制御する。ソースファイル内の特殊文字（$、% など）が表示属性を指定する。",
"パネルソースに特殊属性を指定する属性シンボル・変数を記述する。VIEW でパネルを表示し、各フィールドの特殊属性（色・強調・保護など）が正しく反映されていることを確認する。",
"パネルで特殊属性を制御する要素はどれか。",
["属性シンボルや属性変数（$、% など）","VTAM USS テーブル","RACF プロファイル","SMF サブタイプ"],0,
"属性シンボルや属性変数（特殊文字 $、% など）で特殊属性を制御する。",
"NetView_6.4_Customization_Guide.pdf p.53","NetView_6.4_Customization_Guide.pdf p.46 special characters attributes"),

add("7506","Displaying Variables in Source Panels",
"ソースパネル内では変数を表示できる。アンパサンド変数や複合シンボルをパネルソースに記述すると、VIEW コマンドでパネルを表示する際に変数の値が動的に展開されて表示される。これにより実行時の情報をパネルに反映できる。",
"コマンドリストで変数に値を設定し、ソースパネルでその変数（&var）を参照する。VIEW でパネルを表示し、変数値が正しく展開表示されることを確認する。",
"ソースパネル内で動的に展開されるものはどれか。",
["アンパサンド変数や複合シンボル","RACF プロファイル","VTAM ノード名","SMF レコード"],0,
"ソースパネルではアンパサンド変数や複合シンボルが動的に展開表示される。",
"NetView_6.4_Customization_Guide.pdf p.56","NetView_6.4_Customization_Guide.pdf p.56 displaying variables source panels"),

add("7507","Displaying VIEW Return Codes with SHOWCODE",
"VIEW および BROWSE コマンドからの戻りコードは、SHOWCODE を使って表示できる。SHOWCODE により、パネル表示やブラウズ処理の結果として返された戻りコードを確認でき、コマンドリスト内でのエラー処理や分岐に利用できる。",
"コマンドリストで VIEW を実行した後、SHOWCODE で戻りコードを表示するコードを記述する。NetView で実行し、VIEW の結果に応じた戻りコードが表示されることを確認する。",
"VIEW の戻りコードを表示するために使うものはどれか。",
["SHOWCODE","TASKUTIL","SRFILTER","GENALERT"],0,
"VIEW/BROWSE の戻りコードは SHOWCODE で表示する。",
"NetView_6.4_Customization_Guide.pdf p.51","NetView_6.4_Customization_Guide.pdf p.51 VIEW return codes SHOWCODE"),

add("7508","Dynamic Update Capabilities",
"NetView は動的更新機能を備えており、稼働中にパネルやヘルプ、定義の一部を更新できる。例えば、稼働中にヘルプソースファイルを変更・作成する場合は、パネルデータセットを 2 次エクステントなしで定義することで動的な更新が可能になる。これにより再始動なしに変更を反映できる。",
"稼働中に動的更新の対象（パネルやヘルプ）を変更し、該当の活動化コマンドを発行する。NetView を再始動せずに変更が反映されていることを確認する。",
"動的更新でヘルプパネルを稼働中に変更する際の前提はどれか。",
["パネルデータセットを 2 次エクステントなしで定義する","必ず NetView を停止する","RODM を再構築する","VTAM を再始動する"],0,
"稼働中の動的更新にはパネルデータセットを 2 次エクステントなしで定義する。",
"NetView_6.4_Customization_Guide.pdf p.70","NetView_6.4_Customization_Guide.pdf p.78 dynamic update no secondary extents"),

add("7509","Encoding Incoming Event Data",
"受信したイベントデータのエンコードでは、クラス定義ステートメントの SELECT／MAP／FETCH を用いて、入力データを選択・取得し、出力イベントやアラートのフィールドへ対応付ける。Event/Automation Service の各サービスはこのエンコード処理で受信データを目的の形式へ変換する。",
"クラス定義ステートメントファイルで SELECT／MAP／FETCH を記述し、受信イベントデータのエンコードを定義する。サービスを再始動し、受信データが定義どおりにエンコードされることを確認する。",
"受信イベントデータのエンコードに使うステートメントはどれか。",
["SELECT／MAP／FETCH","TASK／AUTOTASK","COLOR／XHILITE","PRI／SEC"],0,
"受信イベントデータのエンコードは SELECT／MAP／FETCH で行う。",
"NetView_6.4_Customization_Guide.pdf p.129","NetView_6.4_Customization_Guide.pdf p.132 SELECT MAP FETCH encoding"),

add("7510","Event Detail Panel",
"Event Detail（イベント明細）パネルは、ハードウェアモニターが表示する非汎用パネルの一つである。汎用アラート登場以前は、Recommended Action パネルや Event Detail パネル、アラートメッセージがホストに格納されていた。NMVT サポートを用いると、ユーザー作成プログラムが汎用アラートを通じてエラーをハードウェアモニターへ報告できる。",
"NPDA でアラートを選択し Event Detail パネルを表示する。非汎用パネルのテキストをカスタマイズしている場合は、変更が反映されていることを確認する。",
"Event Detail パネルを表示するハードウェアモニター機能はどれか。",
["NPDA（ハードウェアモニター）","NLDM（セッションモニター）","NCCF のみ","RODM"],0,
"Event Detail パネルはハードウェアモニター（NPDA）が表示する。",
"NetView_6.4_Customization_Guide.pdf p.104","NetView_6.4_Customization_Guide.pdf p.97 Event Detail panels NMVT"),

add("7511","Event Receiver Post-CDS Processing",
"イベントレシーバーサービスのクラス定義ステートメント（CDS）後処理では、許可レシーバー、DSIEX02A、自動化テーブル処理が関与する。自動化テーブルはメッセージを自動タスクへルーティングし、その後 NetView はメッセージを送信要求済み（solicited）として扱う。送信要求済みメッセージは待機、DSIEX16、ASSIGN(COPY)、ロギング、表示の各処理を受ける。",
"イベントレシーバーサービスの構成と自動化テーブルを設定し、メッセージを受信させる。メッセージが自動タスクへルーティングされ、DSIEX16 やロギングなどの後処理を受けることをトレースで確認する。",
"イベントレシーバーの CDS 後処理で自動化テーブルがメッセージを送る先はどれか。",
["自動タスク（autotask）","RODM","VTAM ノード","SMF データセット"],0,
"自動化テーブルはメッセージを自動タスクへルーティングする。",
"NetView_6.4_Customization_Guide.pdf p.144","NetView_6.4_Automation_Guide.pdf p.110 authorized receiver DSIEX02A autotask"),

add("7512","Event Receiver Service Data Encoding",
"イベントレシーバーサービスのデータエンコードでは、受信した EIF イベントを NetView のアラートなどへ変換する。アラートアダプターサービスが NetView アラートを EIF イベントへ変換するのに対し、イベントレシーバーサービスは逆方向の受信・変換を担う。確認付きメッセージアダプター、アラート・ツー・トラップ、トラップ・ツー・アラートとともに Event/Automation Service を構成する。",
"イベントレシーバーサービスの構成ファイル（ERCVCFG 関連）でデータエンコードを設定する。サービスを始動し、受信した EIF イベントが NetView 側で正しく処理されることを確認する。",
"イベントレシーバーサービスの主な役割はどれか。",
["受信した EIF イベントを NetView 側へ変換・処理する","NetView アラートを EIF イベントへ変換する","SMF を採取する","VTAM ノードを活動化する"],0,
"イベントレシーバーサービスは受信した EIF イベントを NetView 側で処理するために変換する。",
"NetView_6.4_Customization_Guide.pdf p.134","NetView_6.4_Users_Guide_NetView.pdf p.127 Event Receiver Service"),

with open(os.path.join(os.path.dirname(__file__),'_g037_part7.json'),'w',encoding='utf-8') as f:
    json.dump(rows,f,ensure_ascii=False)
print("part7",len(rows))
