# -*- coding: utf-8 -*-
import json, os
rows=[]
def add(rid,title,naiyou,verify,q,choices,ans,expl,source,rag):
    rows.append({"row_id":rid,"title":title,"naiyou_jp":naiyou,"verify_steps":verify,
    "quiz":{"q":q,"choices":choices,"answer":ans,"explanation":expl},"source":source,"rag_hit":rag})

EAS_FILES="Event/Automation Service の構成ファイルには IHSAACFG（アラートアダプター）、IHSABCFG（確認付きアラートアダプター）、IHSAATCF（アラート・ツー・トラップ）、IHSATCFG（トラップ・ツー・アラート）、IHSAMCFG（メッセージアダプター）、IHSANCFG（確認付きメッセージアダプター）がある。"

add("7459","Alert Adapter Service, Confirmed Alert Adapter Service, and Alert-to-Trap Service Data Encoding",
"アラートアダプターサービスは NetView のアラートを EIF イベントへ変換する。確認付きアラートアダプターサービスおよびアラート・ツー・トラップサービスは、それぞれ確認応答付きの変換、SNMP トラップへの変換を担う。これらのサービスのデータエンコードは構成ファイルの SELECT／MAP／FETCH ステートメントで制御され、アラート内の属性をイベントやトラップのスロットへマップする。",
"Event/Automation Service 構成ファイル（IHSAACFG／IHSABCFG／IHSAATCF）の SELECT／MAP／FETCH ステートメントを編集する。サービスを再始動し、NetView のアラートが EIF イベントまたは SNMP トラップへ期待どおりエンコードされることを確認する。",
"アラートアダプターサービスが NetView アラートを変換する先はどれか。",
["EIF イベント","RODM オブジェクト","VTAM セッション","SMF レコード"],0,
"アラートアダプターサービスは NetView アラートを EIF イベントへ変換する。",
"NetView_6.4_Customization_Guide.pdf p.129","NetView_6.4_Users_Guide_NetView.pdf p.127 Alert Adapter Service"),

add("7460","Alert-to-Trap Post-CDS Processing",
"アラート・ツー・トラップサービスでは、クラス定義ステートメント（CDS）による処理の後段で追加の後処理（Post-CDS Processing）を行う。"+EAS_FILES+" この後処理段で、変換後のトラップに対する最終的な値の設定や調整が行われる。",
"IHSAATCF 構成ファイルでクラス定義および後処理に関するステートメントを編集する。Event/Automation Service を再始動し、アラートが SNMP トラップへ変換される際に後処理が適用されることをトレースで確認する。",
"Event/Automation Service でアラート・ツー・トラップサービスの構成ファイル名はどれか。",
["IHSAATCF","IHSAMCFG","IHSANCFG","IHSATCFG"],0,
"アラート・ツー・トラップサービスの構成ファイルは IHSAATCF である。",
"NetView_6.4_Customization_Guide.pdf p.164","NetView_6.4_Customization_Guide.pdf p.124 EAS config files"),

add("7461","Alert-to-Trap Service Data Encoding",
"アラート・ツー・トラップサービスは、アラートアダプターのキーワード属性にアクセスでき、これらを SELECT、MAP、FETCH ステートメントで使用できる。ただし、すべてのアラートアダプター属性が SNMP トラップに適用できるわけではない。データエンコードでは、アラート属性を SNMP トラップの各フィールドへ対応付ける。",
"IHSAATCF 構成ファイルで SELECT／MAP／FETCH ステートメントを編集し、アラートアダプター属性を SNMP トラップへマップする。サービスを再始動し、生成された SNMP トラップに属性が正しく反映されることを確認する。",
"アラート・ツー・トラップサービスでアラート属性のマップに使えるステートメントはどれか。",
["SELECT、MAP、FETCH","TASK、AUTOTASK","COLOR、XHILITE","KCLASS、PCLASS"],0,
"アラート・ツー・トラップサービスは SELECT／MAP／FETCH でアラートアダプター属性を使用できる。",
"NetView_6.4_Customization_Guide.pdf p.132","NetView_6.4_Customization_Guide.pdf p.132 alert-adapters keyword attributes SELECT MAP FETCH"),

add("7462","Alerts-Dynamic Panel",
"Alerts-Dynamic パネルはハードウェアモニターが表示するアラートパネルの一つである。このパネルのアラート色は、SVFILTER コマンドの COLOR キーワード、SRFILTER の COLOR フィルター、またはカラーマップによって設定できる。COLOR 記録フィルターを設定すると、カラーマップで設定された色を上書きする。",
"NetView コンソールで NPDA を起動し Alerts-Dynamic パネルを表示する。SRFILTER COLOR でアラートに色を設定し、当該アラートが指定した色で表示されることを確認する。",
"Alerts-Dynamic パネルのアラート色を設定できる手段はどれか。",
["SVFILTER／SRFILTER の COLOR またはカラーマップ","RACF プロファイル","VTAM モードテーブル","CNMSTASK の TASK"],0,
"アラート色は SVFILTER/SRFILTER の COLOR フィルターまたはカラーマップで設定できる。",
"NetView_6.4_Customization_Guide.pdf p.101","NetView_6.4_Command_Reference_Vol2 p.344 Alerts-Dynamic color"),

add("7463","Attribute Symbols",
"属性シンボルは、VIEW コマンドで表示するパネルソース内でフィールドの色や強調表示を制御するために使う特殊文字である。ソースファイル内のドル記号（$）やパーセント記号（%）などの特殊文字がフィールドの属性を指定する。チルダ（~）属性シンボルは NOINPUT オプションのコマンド行を定義する。",
"パネルソースに属性シンボル（$、%、~ など）を記述してフィールド属性を定義する。VIEW コマンドでパネルを表示し、指定した色・強調表示・コマンド行が意図どおりになっていることを確認する。",
"パネルソースでコマンド行を定義する属性シンボルはどれか。",
["チルダ（~）","アンパサンド（&）","スラッシュ（/）","アスタリスク（*）"],0,
"NOINPUT オプションではチルダ（~）属性シンボルがコマンド行を定義する。",
"NetView_6.4_Customization_Guide.pdf p.52","NetView_6.4_Customization_Guide.pdf p.48 tilde attribute symbol"),

add("7464","Attribute Variables",
"属性変数は、パネル内で色や強調表示などの表示特性を制御するために使われる変数である。VIEW の INPUT オプションでは、'UY' を指定した最後の属性変数の位置にカーソルがデフォルトで置かれる。属性変数とアンパサンド変数を組み合わせて、ソースパネル内の動的な表示を実現する。",
"パネル定義に属性変数を記述し、'UY' などのカーソル指定を含める。VIEW INPUT でパネルを表示し、カーソルが意図した属性変数の位置に置かれることを確認する。",
"VIEW の INPUT オプションでカーソルがデフォルトで置かれる位置はどれか。",
["'UY' を指定した最後の属性変数","常に左上隅","コマンド行の末尾","最初のアンパサンド変数"],0,
"INPUT オプションでは 'UY' を指定した最後の属性変数にカーソルがデフォルトで置かれる。",
"NetView_6.4_Customization_Guide.pdf p.54","NetView_6.4_Customization_Guide.pdf p.48 attribute variable UY cursor"),

add("7465","Building Generic Alert Panels",
"汎用アラートパネルは、汎用アラートのコードポイントを用いてハードウェアモニターが動的に構築する。従来のリリースでは Recommended Action パネルや Event Detail パネル、アラートメッセージがホストに格納されていたが、汎用アラートではコードポイントから動的にパネルが生成される。サンプルの汎用アラートと関連パネルが資料に示されている。",
"GENALERT コマンドで汎用 NMVT を生成し、ハードウェアモニターのデータベースへログする。NPDA でイベント明細を表示し、汎用アラートパネルがコードポイントから動的に構築されていることを確認する。",
"汎用アラートパネルの構築方法はどれか。",
["汎用アラートのコードポイントから動的に構築","ホストに事前格納された固定パネルを参照","RODM オブジェクトから生成","VTAM USS テーブルから生成"],0,
"汎用アラートパネルは汎用アラートのコードポイントを用いて動的に構築される。",
"NetView_6.4_Customization_Guide.pdf p.99","NetView_6.4_Customization_Guide.pdf p.97 generic alert panels built"),

add("7466","Changing Color and Highlighting for Hardware Monitor Panels",
"ハードウェアモニターパネルの色と強調表示は、カラーマップを通じて制御できる。カラーマップの変更や選択、プロンプト強調表示トークンの設定により、パネルやアラートメッセージの表示色を調整する。DBCS（2 バイト文字）に翻訳されたパネルでは、DBCS ストリングの整合性を保つよう注意が必要である。",
"カラーマップメンバーを編集して色と強調表示を変更し、該当のカラーマップを選択（活動化）する。NPDA でハードウェアモニターパネルを表示し、色・強調表示が変更どおりになっていることを確認する。",
"ハードウェアモニターパネルの色・強調表示を制御する仕組みはどれか。",
["カラーマップ","RACF NETCMDS クラス","VTAM 始動オプション","SMF タイプ 38"],0,
"ハードウェアモニターパネルの色と強調表示はカラーマップで制御する。",
"NetView_6.4_Customization_Guide.pdf p.93","NetView_6.4_Customization_Guide.pdf p.85 color map hardware monitor"),

add("7467","Changing Colors in Browse",
"BROWSE（ブラウズ）機能で表示するデータの色を変更できる。ただし、ネットワークログをブラウズする場合、メッセージは NetView コンソール上で表示されていたときと同じ色では表示されない。色と強調表示は CNMSTYLE ステートメントの設定や関連する制御により決まる。",
"CNMSTYLE（または CNMSTUSR/CxxSTGEN）でブラウズ表示の色設定を変更し、NetView を再初期化する。BROWSE コマンドでネットワークログを表示し、色が変更どおりになっていることを確認する。",
"ネットワークログをブラウズしたときの色について正しいものはどれか。",
["コンソール表示時と同じ色にはならない","常に元の色が保持される","必ず白黒で表示される","RODM の色設定に従う"],0,
"ネットワークログをブラウズすると、メッセージはコンソール表示時と同じ色では表示されない。",
"NetView_6.4_Customization_Guide.pdf p.72","NetView_6.4_Automation_Guide.pdf p.309 browse network log colors"),

with open(os.path.join(os.path.dirname(__file__),'_g037_part2.json'),'w',encoding='utf-8') as f:
    json.dump(rows,f,ensure_ascii=False)
print("part2",len(rows))
