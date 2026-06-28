# -*- coding: utf-8 -*-
import json, os
rows=[]
def add(rid,title,naiyou,verify,q,choices,ans,expl,source,rag):
    rows.append({"row_id":rid,"title":title,"naiyou_jp":naiyou,"verify_steps":verify,
    "quiz":{"q":q,"choices":choices,"answer":ans,"explanation":expl},"source":source,"rag_hit":rag})
CNMSTYLE="NetView の初期化ステートメントは DSIPARM の CNMSTYLE メンバーで定義され、変更時は CNMSTUSR または CxxSTGEN へコピーしてから更新する。"

add("7521","Full-Screen Input Capabilities",
"全画面入力機能では、VIEW コマンドの INPUT オプションを使って全画面パネルからの入力を受け付ける。入力フィールドや設定可能 PF キーを定義でき、PFKDEF コマンドで定義した PF キーやコマンドリスト内での PF キー解釈を利用できる。属性変数でカーソル位置を制御する。",
"VIEW INPUT で入力フィールドと PF キーを定義した全画面パネルを作成する。NetView でパネルを表示し、入力や PF キーが期待どおりに機能することを確認する。",
"全画面入力機能で使う VIEW のオプションはどれか。",
["INPUT","NOINPUT","COMPAT のみ","EXTEND のみ"],0,
"全画面入力機能は VIEW の INPUT オプションを使用する。",
"NetView_6.4_Customization_Guide.pdf p.62","NetView_6.4_Customization_Guide.pdf p.69 VIEW INPUT option PF keys"),

add("7522","Functions to Consider before Making Modifications",
"変更を加える前に検討すべき機能を把握しておく必要がある。重要な NetView 機能を無効化しないよう注意し、変更がコマンド処理、自動化、表示などに与える影響を評価する。デフォルトの自動化テーブル（DSITBL01）の重要機能を維持し、CONTINUE(YES) でメッセージが既定テーブルへ流れるようにする。",
"変更前に対象機能と依存関係を洗い出し、影響評価を行う。試験環境で NetView を再初期化し、重要機能が維持され既存処理に影響がないことを確認する。",
"変更前の検討で重要なことはどれか。",
["重要な NetView 機能を無効化しないこと","VTAMLST を必ず変更すること","RACF を無効化すること","SMF を停止すること"],0,
"変更前は重要な NetView 機能を無効化しないことを確認する。",
"NetView_6.4_Customization_Guide.pdf p.18","NetView_6.4_Installation_Getting_Started.pdf p.62 do not disable vital functions"),

add("7523","General Help Fields",
"一般ヘルプフィールド（General Help Fields）は、ヘルプソースファイルの構成要素である。ソースファイル内の特殊文字（ドル記号 $、パーセント記号 % など）でフィールドの色と強調表示を制御する。プロローグはプログラマーコメント用の任意セクションで、各行は 1〜2 桁目の /* で始まる。",
"ヘルプソースに一般ヘルプフィールドとプロローグ（/* で始まる行）を記述し、特殊文字で属性を指定する。HELP コマンドでヘルプを表示し、フィールドの色・強調表示とコメントの扱いが正しいことを確認する。",
"ヘルプソースのプロローグ行の先頭にあるものはどれか。",
["/*（1〜2 桁目）","$ 記号","% 記号","~ チルダ"],0,
"プロローグの各行は 1〜2 桁目の /* で始まる。",
"NetView_6.4_Customization_Guide.pdf p.46","NetView_6.4_Customization_Guide.pdf p.46 prologue /* general help fields"),

add("7524","General-Use Programming Interface Control Blocks and Include Files",
"一般使用プログラミングインターフェース（General-Use Programming Interface）の制御ブロックとインクルードファイルは、ユーザー作成プログラムが NetView と連携するために提供される。これらの制御ブロックやマクロ、インクルードファイルを用いて、コマンドプロセッサーや出口がデータ構造へアクセスできる。",
"ユーザー作成プログラムで一般使用プログラミングインターフェースの制御ブロック／インクルードファイルを参照するコードを記述する。アセンブル・リンクして NetView 配下で実行し、制御ブロックへ正しくアクセスできることを確認する。",
"一般使用プログラミングインターフェースが提供するものはどれか。",
["制御ブロックとインクルードファイル","RACF プロファイル","VTAM USS テーブル","SMF レコード"],0,
"一般使用プログラミングインターフェースは制御ブロックとインクルードファイルを提供する。",
"NetView_6.4_Customization_Guide.pdf p.175","NetView_6.4_Customization_Guide.pdf p.193 general-use programming interfaces control blocks"),

add("7525","HELPMAP Facility",
"HELPMAP 機能は、コマンドと対応するヘルプパネルのマッピングを管理する仕組みである。コマンドの同義語（シノニム）を作成した場合、その同義語に対するヘルプを作成するか、helpmap サンプル（CNMS1048）へ追加できる。NetView のヘルプはコマンド名にひも付けられる。",
"helpmap サンプル（CNMS1048）へ同義語とヘルプパネルの対応を追加し、NetView を再初期化する。HELP synonym を発行し、同義語に対するヘルプが表示されることを確認する。",
"NetView のヘルプは何にひも付けられるか。",
["コマンド名","RODM クラス名","VTAM ノード名","SMF サブタイプ"],0,
"NetView のヘルプはコマンド名にひも付けられる。",
"NetView_6.4_Customization_Guide.pdf p.79","NetView_6.4_Administration_Reference.pdf p.312 helpmap CNMS1048 synonym"),

add("7526","IBM Z NetView library",
"IBM Z NetView ライブラリーは、製品のマニュアル群を指す。Customization Guide、Administration Reference、Automation Guide、Command Reference、Installation: Getting Started などが含まれる。CNMSTYLE ステートメントの変更については Installation: Getting Started を参照するなど、資料間で相互参照する。",
"IBM Knowledge Center または HELP コマンドで IBM Z NetView ライブラリーの該当資料を参照する。記載手順に従い設定し、内容が一致することを確認する。",
"CNMSTYLE ステートメントの変更について参照すべき資料はどれか。",
["IBM Z NetView Installation: Getting Started","RACF 管理ガイド","VTAM リソース定義","SMF レコード解説"],0,
"CNMSTYLE ステートメントの変更は Installation: Getting Started を参照する。",
"NetView_6.4_Customization_Guide.pdf p.9","NetView_6.4_Administration_Reference.pdf p.107 IBM Z NetView library Installation Getting Started"),

add("7527","Immediate Commands",
"即時コマンド（immediate command）は、通常のコマンドキューを経由せず即座に処理されるコマンドである。SAF セキュリティーを使う場合、即時コマンドは NETCMDS クラスでチェックされないが、バックアップのコマンド許可を構成できる。即時コマンドは長時間実行コマンドの実行中でも割り込んで処理される。",
"即時コマンド（例: RESET、GO 等）を全画面コマンド処理の実行中に発行する。即時コマンドが即座に処理され、コマンドキューを待たないことを確認する。",
"即時コマンドの SAF セキュリティーでの扱いとして正しいものはどれか。",
["NETCMDS クラスではチェックされない","必ず NETCMDS でチェックされる","RACF を経由しない","常に拒否される"],0,
"即時コマンドは NETCMDS クラスではチェックされず、バックアップのコマンド許可を構成できる。",
"NetView_6.4_Customization_Guide.pdf p.24","NetView_6.4_Administration_Reference.pdf p.248 immediate commands NETCMDS"),

add("7528","Input and Output",
"NetView の入出力（I/O）には、バッファープールやデータセットアクセスが関わる。VSAM の局所共用リソース（LSR）パフォーマンスオプションは、入出力制御ブロックやバッファー、チャネルプログラムなどの共通制御ブロックを共用する。バッファープールはジョブ CNMSJM01（NETVIEW.V6R4M0.CNMSAMP 内）で定義する。",
"ジョブ CNMSJM01 を用いてバッファープールを定義し、VSAM LSR オプションを設定する。NetView を再始動し、I/O が定義したバッファープール構成で動作することを確認する。",
"NetView のバッファープールを定義するジョブはどれか。",
["CNMSJM01","IHSAEVNT","CNMSJ000","DSITBL01"],0,
"バッファープールはジョブ CNMSJM01 で定義する。",
"NetView_6.4_Customization_Guide.pdf p.28","NetView_6.4_Installation_Configuring_Additional_Components.pdf p.32 CNMSJM01 buffer pools VSAM LSR"),

with open(os.path.join(os.path.dirname(__file__),'_g037_part9.json'),'w',encoding='utf-8') as f:
    json.dump(rows,f,ensure_ascii=False)
print("part9",len(rows))
