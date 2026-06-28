# -*- coding: utf-8 -*-
import json, os
rows=[]
def add(rid,title,naiyou,verify,q,choices,ans,expl,source,rag):
    rows.append({"row_id":rid,"title":title,"naiyou_jp":naiyou,"verify_steps":verify,
    "quiz":{"q":q,"choices":choices,"answer":ans,"explanation":expl},"source":source,"rag_hit":rag})
CNMSTYLE="NetView の初期化ステートメントは DSIPARM データセットの CNMSTYLE メンバーで定義される。CNMSTYLE ステートメントを変更するには、当該ステートメントを CNMSTUSR または CxxSTGEN メンバーへコピーしてから必要な更新を行う。デフォルトの CNMSTYLE メンバー自体は変更しない。"

add("7468","Changing Panel Text",
"パネルテキストの変更は、画面エディターを使い既存テキストの上書きやテキスト追加によって行う。NetView 稼働中にヘルプソースファイルを変更・作成する場合は、パネルデータセットを 2 次エクステントなしで定義する。そうしないと、パネルが新しいエクステントへ格納され、データセットのクローズが必要になる場合がある。",
"画面エディターでパネルソースを開き、既存テキストを上書きまたは追加してテキストを変更する。HELP コマンドで該当パネルを表示し、変更後のテキストが正しく表示されることを確認する。",
"NetView 稼働中にヘルプソースを変更する際、パネルデータセットをどう定義すべきか。",
["2 次エクステントなしで定義する","必ず複数エクステントで定義する","VSAM LSR で定義する","RODM 上に定義する"],0,
"稼働中に変更するパネルデータセットは 2 次エクステントなしで定義する。",
"NetView_6.4_Customization_Guide.pdf p.87","NetView_6.4_Customization_Guide.pdf p.78 screen editor panel text"),

add("7469","Choosing a Language",
"NetView のコマンドプロシージャーやコマンドリストは複数の言語で記述できる。利用できる言語には REXX、NetView コマンドリスト言語（CLIST）、PL/I、C、アセンブラーがある。機能ごとに適した言語を選択し、コマンドプロセッサーやコマンドリストとして実装する。",
"目的の機能に対し REXX や NetView コマンドリスト言語などからプロシージャー言語を選択し、コマンドリストを作成する。NetView でそのコマンドを実行し、選択した言語で期待どおりに動作することを確認する。",
"NetView のコマンドプロシージャーで使用できる言語に含まれないものはどれか。",
["COBOL（標準のコマンドリスト言語ではない）","REXX","NetView コマンドリスト言語","PL/I"],0,
"REXX、NetView コマンドリスト言語、PL/I、C、アセンブラーが使用でき、COBOL は標準のコマンドリスト言語ではない。",
"NetView_6.4_Customization_Guide.pdf p.27","NetView_6.4_Customization_Guide.pdf p.25 command procedures languages"),

add("7470","Class Definition Statement Files",
"クラス定義ステートメントファイルは、Event/Automation Service のデータエンコードを定義するファイルである。クラス定義ステートメントは FETCH、MAP、SELECT のセグメントから構成され、入力データの選択・取得・対応付けを記述する。"+CNMSTYLE,
"クラス定義ステートメントファイルを編集し、FETCH／MAP／SELECT セグメントを記述する。Event/Automation Service を再始動し、データが定義どおりにエンコードされることを確認する。",
"クラス定義ステートメントを構成するセグメントはどれか。",
["FETCH、MAP、SELECT","TASK、AUTOTASK","COLOR、XHILITE","PRI、SEC"],0,
"クラス定義ステートメントは FETCH／MAP／SELECT のセグメントから構成される。",
"NetView_6.4_Customization_Guide.pdf p.128","NetView_6.4_Customization_Guide.pdf p.132 SELECT MAP FETCH"),

add("7471","Coding the VIEW Command",
"VIEW コマンドは「VIEW compname pnlname」の形式でコーディングする。compname は PF キー定義で NetView が使用する 1〜8 文字の名前、pnlname は表示するパネル名である。NOINPUT／INPUT、COMPAT／EXTEND のオプションを指定でき、ヘルプは VIEW ベースとウィンドウベースの 2 種類がある。",
"コマンドリスト内に「VIEW compname pnlname NOINPUT」などを記述する。NetView で当該コマンドリストを実行し、指定したパネルが VIEW コマンドにより表示されることを確認する。",
"VIEW コマンドの compname オペランドの説明として正しいものはどれか。",
["PF キー定義で使用する 1〜8 文字の名前","表示するパネルのデータセット名","入力フィールドの初期値","カラーマップ名"],0,
"compname は PF キー定義で NetView が使用する 1〜8 文字の名前である。",
"NetView_6.4_Customization_Guide.pdf p.48","NetView_6.4_Customization_Guide.pdf p.48 Coding the VIEW Command"),

add("7472","Collecting Data",
"NetView はネットワークおよびシステムの管理データを収集する。収集したデータはストレージへの保存や記録（ロギング）の対象となり、ハードウェアモニターやセッションモニター、ネットワークログなどに格納される。"+CNMSTYLE,
"CNMSTYLE のデータ収集・記録に関するステートメントを確認・調整し、NetView を再初期化する。該当のモニター（NPDA／NLDM）やネットワークログを表示し、データが収集・記録されていることを確認する。",
"NetView が収集したデータの主な扱いはどれか。",
["ストレージへの保存と記録（ロギング）","破棄して保持しない","常に RACF へ転送","VTAMLST へ書き込み"],0,
"収集したデータはストレージへの保存と記録の対象となる。",
"NetView_6.4_Customization_Guide.pdf p.20","NetView_6.4_Customization_Guide.pdf p.22 Data Storage and Recording"),

add("7473","Color Maps for Hardware Monitor Panels",
"ハードウェアモニターパネル用のカラーマップは、パネルの色と強調表示を定義する。なお、ハードウェアモニターのヘルプパネルおよびコマンド説明パネル用のカラーマップは、NetView の旧リリースでのみ利用可能である。カラーマップの変更・選択により表示色を調整する。",
"カラーマップメンバーを編集し、ハードウェアモニターパネルの色定義を変更する。該当カラーマップを選択し、NPDA でパネルを表示して色が反映されていることを確認する。",
"ハードウェアモニターのヘルプパネル用カラーマップについて正しいものはどれか。",
["旧リリースでのみ利用可能","常に最新リリースで必須","RODM 上に格納される","VTAM が管理する"],0,
"ヘルプパネルおよびコマンド説明パネル用のカラーマップは旧リリースでのみ利用可能である。",
"NetView_6.4_Customization_Guide.pdf p.171","NetView_6.4_Customization_Guide.pdf p.85 color maps prior releases"),

add("7474","Command Processors and Command Lists",
"コマンドプロセッサーとコマンドリストは、NetView の機能を拡張・自動化するためのユーザー作成プログラムである。コマンドプロセッサーはアセンブラーや高水準言語で記述し、コマンドリストは REXX や NetView コマンドリスト言語で記述する。データサービスコマンドや長時間実行コマンドとして動作させることもできる。",
"コマンドプロセッサーまたはコマンドリストを作成し、CNMCMD/CNMCMDU でコマンドとして定義する。NetView でそのコマンドを実行し、期待どおりに処理されることを確認する。",
"コマンドリストを記述する言語に該当するものはどれか。",
["REXX や NetView コマンドリスト言語","VTAM USS テーブル","RACF コマンド","SMF マクロ"],0,
"コマンドリストは REXX や NetView コマンドリスト言語で記述する。",
"NetView_6.4_Customization_Guide.pdf p.25","NetView_6.4_Programming_REXX p.26 command list language"),

add("7475","Compound Symbols",
"複合シンボル（compound symbol）は、REXX や NetView コマンドリスト言語で使われる、ステム部と添字部から構成される変数である。パネルソース内では属性変数やアンパサンド変数と組み合わせて、配列状のデータや動的な値の表示に利用される。"+CNMSTYLE,
"コマンドリストで複合シンボル（例: stem.index）を設定し、VIEW のソースパネルで参照する。パネルを表示し、複合シンボルの値が正しく展開されることを確認する。",
"複合シンボルの構成として正しいものはどれか。",
["ステム部と添字部から構成される","常に固定長 8 文字","RODM フィールドへの参照","VTAM ノード名"],0,
"複合シンボルはステム部と添字部から構成される変数である。",
"NetView_6.4_Customization_Guide.pdf p.58","NetView_6.4_Customization_Guide.pdf p.56 displaying variables source panels"),

with open(os.path.join(os.path.dirname(__file__),'_g037_part3.json'),'w',encoding='utf-8') as f:
    json.dump(rows,f,ensure_ascii=False)
print("part3",len(rows))
