# -*- coding: utf-8 -*-
import json, os
rows=[]
def add(rid,title,naiyou,verify,q,choices,ans,expl,source,rag):
    rows.append({"row_id":rid,"title":title,"naiyou_jp":naiyou,"verify_steps":verify,
    "quiz":{"q":q,"choices":choices,"answer":ans,"explanation":expl},"source":source,"rag_hit":rag})
EASF="Event/Automation Service の構成ファイルには IHSAACFG（アラートアダプター）、IHSABCFG（確認付きアラートアダプター）、IHSAATCF（アラート・ツー・トラップ）、IHSATCFG（トラップ・ツー・アラート）、IHSAMCFG（メッセージアダプター）、IHSANCFG（確認付きメッセージアダプター）がある。"

add("7495","Data Services Commands",
"データサービスコマンド（DSC）は、データサービスタスク（DST）の下で実行され、外部リソースとのデータ送受信を行うコマンドである。NetView のデータサービスコマンドは、CNMI（通信ネットワーク管理インターフェース）やキープロセスを通じてネットワークからのデータ収集や応答処理を担う。",
"データサービスコマンドを定義・実装し、対応する DST を CNMSTYLE の TASK で起動する。NetView でデータサービスコマンドを実行し、外部リソースとのデータ送受信が機能することを確認する。",
"データサービスコマンドが実行されるタスクはどれか。",
["データサービスタスク（DST）","OST のみ","PPT のみ","NNT のみ"],0,
"データサービスコマンドはデータサービスタスク（DST）の下で実行される。",
"NetView_6.4_Customization_Guide.pdf p.25","NetView_6.4_Customization_Guide.pdf p.25 data services commands DST"),

add("7496","Data Storage and Recording",
"NetView はデータの保存（ストレージ）と記録（レコーディング）を行う。ハードウェアモニターデータベース、セッションモニターデータベース、ネットワークログ、トレースなどにデータが格納される。記録対象や保存方法は CNMSTYLE のステートメントやフィルター設定で制御する。",
"CNMSTYLE のデータ保存・記録に関するステートメントを確認・調整し、NetView を再初期化する。ネットワークログや各モニターを表示し、データが意図どおり記録・保存されていることを確認する。",
"NetView がデータを記録する先に含まれるものはどれか。",
["ネットワークログやハードウェアモニターデータベース","VTAMLST","SYS1.PARMLIB","RACF データベース"],0,
"ネットワークログやハードウェアモニター／セッションモニターのデータベースに記録される。",
"NetView_6.4_Customization_Guide.pdf p.22","NetView_6.4_Customization_Guide.pdf p.22 data storage and recording"),

add("7497","Defaults for Configurable Settings",
"設定可能項目の既定値は、Event/Automation Service の初期化時に適用される。例として、アラート・ツー・トラップのコミュニティー名は public、エンタープライズオブジェクト ID は 1.3.6.1.4.1.1.1588.1.3、トラップ・ツー・アラートの PPI 名は NETVALRT、ポート番号は 162 が既定である。これらは構成ファイルのステートメントで上書きできる。",
"構成ファイルで既定値を上書きするステートメント（Community、PortNumber 等）を設定する。サービスを始動し、既定値または上書き値が適用されていることを確認する。",
"アラート・ツー・トラップのコミュニティー名の既定値はどれか。",
["public","private","NETVALRT","loopback"],0,
"アラート・ツー・トラップのコミュニティー名の既定値は public である。",
"NetView_6.4_Customization_Guide.pdf p.116","NetView_6.4_Customization_Guide.pdf p.121 defaults configurable settings"),

add("7498","Defining a Focal Point",
"フォーカルポイントは管理データの指定受信側である。NetView はアラート、リンクサービス、運用管理データ、サービスポイントコマンドサービス、ユーザー定義カテゴリーのフォーカルポイントとして機能できる。フォーカルポイントの役割は FOCALPT コマンドや制御範囲（sphere of control）マネージャーで定義する。",
"FOCALPT コマンドでフォーカルポイントを定義し、対象カテゴリーを指定する。入口点から管理データを送信させ、フォーカルポイントで受信されることを確認する。",
"フォーカルポイントの役割はどれか。",
["管理データの指定受信側","管理データの指定送信側","VTAM の物理ノード","RACF の管理者"],0,
"フォーカルポイントは管理データの指定受信側である。",
"NetView_6.4_Customization_Guide.pdf p.169","NetView_6.4_Users_Guide_NetView.pdf p.169 focal point receiver"),

add("7499","Defining an Entry Point",
"入口点（エントリーポイント）は管理データの指定送信側である。入口点は、アラートや運用管理データなどを上位のフォーカルポイントへ転送する。FOCALPT コマンドにより、入口点の該当アプリケーションは一方向データを転送すべきフォーカルポイントノードの識別を行える。",
"入口点側で FOCALPT ACQUIRE などを発行し、フォーカルポイントを取得する。入口点から管理データを送信し、フォーカルポイントへ転送されることを確認する。",
"入口点の役割はどれか。",
["管理データの指定送信側","管理データの指定受信側","RODM の管理者","VTAM の APPL ノード"],0,
"入口点は管理データの指定送信側である。",
"NetView_6.4_Customization_Guide.pdf p.170","NetView_6.4_Command_Reference_Vol1 p.404 FOCALPT entry point"),

add("7500","Defining User-Written Programs on the Host: Exits and Commands",
"ホスト上でユーザー作成プログラム（インストール出口とコマンド）を定義できる。インストール出口プログラム（DSIEX02A、DSIEX16 など）はメッセージ処理の各段階で呼び出され、属性や色・強調表示を変更できる。ユーザー作成コマンドはコマンドプロセッサーとして定義し、CNMCMD/CNMCMDU で登録する。",
"インストール出口プログラムをアセンブルしてロードライブラリーに配置し、CNMSTYLE で出口を有効化する。ユーザー作成コマンドを CNMCMDU で定義し、NetView でそれぞれが呼び出されることを確認する。",
"メッセージ処理の各段階で呼び出されるユーザー作成プログラムはどれか。",
["インストール出口プログラム（DSIEX02A、DSIEX16 等）","VTAM USS テーブル","RACF 出口のみ","SMF 出口のみ"],0,
"DSIEX02A や DSIEX16 などのインストール出口がメッセージ処理の各段階で呼び出される。",
"NetView_6.4_Customization_Guide.pdf p.25","NetView_6.4_Automation_Guide.pdf p.113 DSIEX16 installation exit"),

add("7501","Designing Functions",
"カスタマイズに先立ち、機能を設計する段階では、変更前に検討すべき機能を理解し、カスタマイズ領域を見極める。設計では、どの機能をどの言語・メンバーで実装するか、既存機能への影響をどう抑えるかを計画する。重要機能を無効化しないよう注意する。",
"設計段階で対象機能・実装方法・影響範囲を整理し、ユーザーメンバーへの変更方針を決める。試験環境で NetView を再初期化し、設計どおりに機能が動作し既存機能に影響がないことを確認する。",
"機能設計で特に注意すべき点はどれか。",
["重要機能を無効化しないこと","必ず VTAMLST を変更すること","RACF を無効化すること","SMF を停止すること"],0,
"設計時は NetView の重要機能を無効化しないよう注意する。",
"NetView_6.4_Customization_Guide.pdf p.17","NetView_6.4_Installation_Getting_Started.pdf p.62 do not disable vital functions"),

add("7502","Detailed Example for Trap-to-Alert Conversion",
"トラップ・ツー・アラート変換の詳細な例では、受信した SNMP トラップがアラート（NMVT）へ変換される過程が示される。変換後のアラート NMVT は、ハードウェアモニターのイベント明細として表示され、元の SNMP トラップはサブベクトル X'31' に保持される。これにより変換の正しさを検証できる。",
"トラップ・ツー・アラートサービスを構成して SNMP トラップを受信させる。NPDA のイベント明細を表示し、トラップがアラートへ変換され、元のトラップが SV X'31' に含まれていることを確認する。",
"トラップ・ツー・アラート変換後のアラートで元の SNMP トラップが保持される場所はどれか。",
["サブベクトル X'31'","主要ベクトル X'0000'","X'91' サブベクトル","X'92' サブベクトル"],0,
"変換後のアラートでは元の SNMP トラップがサブベクトル X'31' に保持される。",
"NetView_6.4_Customization_Guide.pdf p.158","NetView_6.4_Troubleshooting_Guide.pdf p.388 original SNMP trap in SV 31"),

with open(os.path.join(os.path.dirname(__file__),'_g037_part6.json'),'w',encoding='utf-8') as f:
    json.dump(rows,f,ensure_ascii=False)
print("part6",len(rows))
