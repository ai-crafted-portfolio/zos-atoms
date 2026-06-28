# -*- coding: utf-8 -*-
import json, os
rows=[]
def add(rid,title,naiyou,verify,q,choices,ans,expl,source,rag):
    rows.append({"row_id":rid,"title":title,"naiyou_jp":naiyou,"verify_steps":verify,
    "quiz":{"q":q,"choices":choices,"answer":ans,"explanation":expl},"source":source,"rag_hit":rag})

add("7513","Event/Automation Service Output",
"Event/Automation Service の出力は、変換されたイベントやトラップ、ログ情報などである。構成ファイル（IHSAACFG／IHSAATCF など）により各サービスの出力が制御され、出力先のイベントサーバーや SNMP マネージャーへデータが送られる。出力データの形式や出力ログ名も構成で定義される。",
"Event/Automation Service の構成ファイルで出力先と出力データ形式を設定する。サービスを始動し、変換されたイベント／トラップが意図した出力先へ送られることを確認する。",
"Event/Automation Service の出力を制御するものはどれか。",
["構成ファイル（IHSAACFG／IHSAATCF など）","VTAMLST","RACF プロファイル","SYS1.PARMLIB"],0,
"出力は各サービスの構成ファイルで制御される。",
"NetView_6.4_Customization_Guide.pdf p.124","NetView_6.4_Customization_Guide.pdf p.124 EAS config files"),

add("7514","Event/Automation Service Output Log Names",
"Event/Automation Service の出力ログ名は、各サービスが生成するログの名前を指定する。構成ファイル内のステートメントで出力ログ名を定義し、サービスの動作やエラーを記録するログの出力先を制御する。これによりトラブルシューティング時にサービスごとのログを参照できる。",
"構成ファイルで出力ログ名を設定し、Event/Automation Service を始動する。指定したログにサービスの動作情報が記録されることを確認する。",
"Event/Automation Service の出力ログ名を指定する場所はどれか。",
["構成ファイル内のステートメント","VTAM 始動オプション","RACF プロファイル","CNMKEYS"],0,
"出力ログ名は構成ファイル内のステートメントで指定する。",
"NetView_6.4_Customization_Guide.pdf p.125","NetView_6.4_Customization_Guide.pdf p.124 output log names config"),

add("7515","Event/Automation Service: Overview",
"Event/Automation Service は、NetView のメッセージやアラートを EIF イベントや SNMP トラップへ変換し、Tivoli Netcool/OMNIbus などのイベントサーバーへ転送する仲介サービスである。メッセージアダプター、確認付きメッセージアダプター、イベントレシーバー、アラートアダプター、アラート・ツー・トラップ、トラップ・ツー・アラートのサービスから構成される。NetView の PPI に登録してメッセージを受け取る。",
"Event/Automation Service を IHSAEVNT ジョブで始動し、NetView の PPI 登録状況を確認する。メッセージ／アラートが EIF イベントや SNMP トラップへ変換され、イベントサーバーへ転送されることを確認する。",
"Event/Automation Service がメッセージを受け取るために登録するものはどれか。",
["NetView の PPI（プログラム間インターフェース）","RACF","VTAM USS テーブル","SMF"],0,
"Event/Automation Service は NetView の PPI に登録してメッセージを受け取る。",
"NetView_6.4_Customization_Guide.pdf p.115","NetView_6.4_Customization_Guide.pdf p.115 register with NetView PPI"),

add("7516","Examples",
"カスタマイズの具体例を示す節である。ヘルプソースの作成例、パネル定義例、VIEW コマンドのコーディング例、Event/Automation Service の構成例などが含まれ、実際の記述方法を例示してカスタマイズ作業を支援する。例を参照して自社向けの定義を作成する。",
"資料の例を参考にして、対象のカスタマイズ定義（パネルや構成ファイル）を作成する。NetView で動作させ、例どおりの結果が得られることを確認する。",
"カスタマイズの「例」節の目的はどれか。",
["具体的な記述方法を例示して作業を支援する","VTAM ノードを定義する","RACF を構成する","SMF を採取する"],0,
"例の節は具体的な記述方法を例示してカスタマイズ作業を支援するものである。",
"NetView_6.4_Customization_Guide.pdf p.82","NetView_6.4_Customization_Guide.pdf p.46 examples source"),

add("7517","FETCH Segment of a Class Definition Statement",
"クラス定義ステートメントの FETCH セグメントは、入力データから特定の値を取得（フェッチ）する処理を定義する。SELECT で選択、MAP で対応付け、FETCH で取得という構成の一部であり、アラート・ツー・トラップなどのサービスではアラートアダプター属性を FETCH ステートメントで使用できる。",
"クラス定義ステートメントファイルで FETCH セグメントを記述し、取得対象の属性を指定する。サービスを再始動し、FETCH で指定した値が出力に反映されることを確認する。",
"クラス定義ステートメントの FETCH セグメントの役割はどれか。",
["入力データから特定の値を取得する","パネルに色を設定する","タスクを定義する","RACF を構成する"],0,
"FETCH セグメントは入力データから特定の値を取得する処理を定義する。",
"NetView_6.4_Customization_Guide.pdf p.136","NetView_6.4_Customization_Guide.pdf p.132 FETCH SELECT MAP"),

add("7518","Finding Customization Information",
"カスタマイズ情報の探し方を示す節である。Customization Guide のほか、CNMSTYLE については Administration Reference や Installation: Getting Started を相互参照する。オンラインヘルプ（HELP コマンド）や IBM Knowledge Center を活用して、目的のカスタマイズ手順を見つける。",
"目的のカスタマイズ項目について HELP コマンドや該当資料（Customization Guide 等）を参照する。記載された手順に従って設定し、期待どおりに反映されることを確認する。",
"CNMSTYLE のカスタマイズ情報を相互参照すべき資料はどれか。",
["Administration Reference や Installation: Getting Started","VTAM 資料のみ","RACF 資料のみ","SMF 資料のみ"],0,
"CNMSTYLE は Administration Reference や Installation: Getting Started を相互参照する。",
"NetView_6.4_Customization_Guide.pdf p.19","NetView_6.4_Administration_Reference.pdf p.31 refer to Installation Getting Started"),

add("7519","Focal Point VPD Collection",
"フォーカルポイント VPD 収集では、フォーカルポイント NetView プログラムがネットワークから VPD（重要製品データ）を収集する。例では、インストール時に NV1 が共通グローバル変数 SMFVPD を 200 に設定し、NV1 をフォーカルポイントに指定する。CNMSTYLE は SMFVPD を既定で 37 に設定する。自動化テーブル（DSITBL01）でフォーカルポイント固有の処理を定義する。",
"フォーカルポイント側で共通グローバル変数 SMFVPD を設定し、自動化テーブルにフォーカルポイント固有の VPD 収集処理を定義する。VPDALL/VPDPU コマンドで VPD 収集を実行し、フォーカルポイントへデータが集まることを確認する。",
"CNMSTYLE が設定する共通グローバル変数 SMFVPD の既定値はどれか。",
["37","200","250","162"],0,
"CNMSTYLE は共通グローバル変数 SMFVPD を既定で 37 に設定する。",
"NetView_6.4_Customization_Guide.pdf p.112","NetView_6.4_Customization_Guide.pdf p.113 SMFVPD 37 focal point VPD"),

add("7520","Format of Event/Automation Service Output Data",
"Event/Automation Service の出力データの形式は、変換先（EIF イベントまたは SNMP トラップ）に応じて定義される。EIF イベントはスロット／値のペアで構成され、SNMP トラップは変数バインディングを持つ。出力データ形式はメッセージ形式ファイルやクラス定義ステートメントで制御する。",
"メッセージ形式ファイルやクラス定義で出力データ形式を設定する。サービスを始動し、出力された EIF イベントや SNMP トラップが定義どおりの形式であることを確認する。",
"EIF イベントの出力データを構成するものはどれか。",
["スロット／値のペア","変数バインディングのみ","RODM フィールド","VTAM ノード名"],0,
"EIF イベントはスロット／値のペアで構成される。",
"NetView_6.4_Customization_Guide.pdf p.126","NetView_6.4_Users_Guide_NetView.pdf p.127 slot/value pairs EIF"),

with open(os.path.join(os.path.dirname(__file__),'_g037_part8.json'),'w',encoding='utf-8') as f:
    json.dump(rows,f,ensure_ascii=False)
print("part8",len(rows))
