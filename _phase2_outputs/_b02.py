# -*- coding: utf-8 -*-
import json,os
BASE=os.path.dirname(__file__)
CJSON=os.path.join(BASE,'_g052_content.json')
C=json.load(open(CJSON,encoding='utf-8'))
PDF="TSA_z_OS_4.3_Customizing_and_Programming.pdf"
def add(rid,naiyou,steps,q,choices,answer,expl,rag,src=None):
    C[rid]=dict(naiyou=naiyou,steps=steps,q=q,choices=choices,answer=answer,expl=expl,rag=rag,src=src or PDF)

add("10508",
"System Recovery Boost は IBM z15 以降で利用可能な機能で、IPL・シャットダウン時に一時的に追加のプロセッサー能力を活用し、リカバリーや保守によるダウンタイムを短縮する。SA z/OS ではシャットダウン時に System Recovery Boost を自動で有効化できる。Boost フィールドが YES（デフォルト）の場合、システム・シャットダウン時に自動で有効化され、NO の場合は明示的にオプトアウトする。このパラメーターはシステム・シャットダウンにのみ適用され、他リソースのシャットダウンでは無視される。",
["INGREQ パネルまたはシャットダウン定義で Boost フィールドの設定（YES/NO）を確認する。",
 "対象システムに対し INGREQ ALL でシャットダウンを実行する。",
 "シャットダウン時に System Recovery Boost が自動的に有効化されることを確認する。",
 "必要に応じて INGREQ ユーザー出口 AOFEXC01 でデフォルトを上書きできることを確認する。"],
"System Recovery Boost のシャットダウン時自動有効化を制御する Boost フィールドのデフォルト値はどれか?",
["NO","YES","AUTO","NORM"],1,
"Boost フィールドのデフォルトは YES で、システム・シャットダウン時に System Recovery Boost が自動有効化される。",
"TSA_z_OS_4.3_Operators_Commands.pdf p.245 / Customizing_and_Programming.pdf p.163")

add("10509",
"ISQCCMD インターフェースを使うハードウェア・コマンドの一部は NetView へ 2 つのメッセージを返す。第 1 にコマンドが実行受付（Accepted）か拒否（Rejected）かのメッセージ、第 2 に受付された場合は実際の成否を示す完了イベント・メッセージが非同期に送られる。アプリケーション・スクリプトは ISQCCMD 終了時に受付/拒否応答を直接取得でき、受付応答を完了イベント・メッセージの待機に利用できる。ACTIVATE・CBU などのコマンドが対象である。",
["NetView 自動化環境で ISQCCMD により ACTIVATE などの非同期ハードウェア・コマンドを発行する。",
 "ISQCCMD 終了時に Accepted/Rejected の応答が返ることを確認する。",
 "受付の場合、後続の完了イベント・メッセージを PIPE で受信・処理する。",
 "ISQ メッセージと AOFA0017 レポート・データが PIPE 処理可能であることを確認する。"],
"ISQCCMD による非同期ハードウェア・コマンドが NetView へ返す 2 番目のメッセージはどれか?",
["コマンドのヘルプ・テキスト","受付/拒否を示すメッセージ","成否を示す完了イベント・メッセージ","SDF パネル更新通知"],2,
"第 1 に受付/拒否、第 2 に実際の成否を示す完了イベント・メッセージが非同期で送られる。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.98")

add("10512",
"対象システム上で自動化できないメッセージ（特に IPL 時に現れるもの）を SA z/OS のプロセッサー・オペレーションで自動化するため、プロキシー定義を用いる。システム・オペレーションの仕組みを利用するには、プロセッサー・オペレーション・リソースを表すプロキシー・リソースをカスタマイズ・ダイアログでエントリー・タイプ Application（APL）として生成する。プロキシーとプロセッサー・オペレーション・リソース（ターゲット・システム）は一対一の関係を持つ。",
["カスタマイズ・ダイアログでターゲット・システムを表す SYS と対応するプロキシー APL を定義する。",
 "プロキシー APL をタイプ SYSTEM・Nature BASIC の APG にリンクする。",
 "ターゲット・システムでメッセージを発生させ、プロキシー経由でシステム・オペレーションが反応することを確認する。",
 "INGLIST/INGREQ からプロキシー・リソースを操作できることを確認する。"],
"プロキシー定義でプロセッサー・オペレーション・リソースを表すために使うエントリー・タイプはどれか?",
["System（SYS）","Application（APL）","Monitor（MTR）","Group（GRP）"],1,
"プロキシー・リソースはエントリー・タイプ Application（APL）として生成し、ターゲット・システム（SYS）と一対一に対応させる。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.90 / p.91")

add("10517",
"自動化ネットワーク定義プロセスでは、フォーカル・ポイント・システム、それが監視・制御するターゲット・システム、およびシステム間のゲートウェイ・セッションを定義する。ゲートウェイ・セッションの定義方法は「Defining Gateway Sessions」で説明される。さらに自動化ネットワーク構成を反映するよう NetView 定義を変更する。例ではプライマリー・フォーカル・ポイントが CHI01、バックアップが CHI02 となる。",
["カスタマイズ・ダイアログでフォーカル・ポイント・システムとターゲット・システムを定義する。",
 "システム間のゲートウェイ・セッションを定義する。",
 "NetView 定義を自動化ネットワーク構成に合わせて変更する。",
 "ゲートウェイ・オートタスクによりシステム間セッションが確立されることを確認する。"],
"自動化ネットワーク定義プロセスでシステム間通信に定義する要素はどれか?",
["SMF レコード","ゲートウェイ・セッション","ローカル・ページ・データ・セット","SDF ツリー構造"],1,
"自動化ネットワークではフォーカル・ポイント、ターゲット・システム、ゲートウェイ・セッションを定義する。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.153")

add("10519",
"SA z/OS は重要アプリケーションや依存ソフトウェアの信頼性レポート作成や課金を支援する可用性・リカバリー時間レポート機能を提供する。例えばアプリケーション実行に要した時間に基づき正確に課金できる。これは USS アプリケーションや NetView アドレス空間で稼働するモニターリソースなど非 MVS リソースで特に重要である。状況変化はタイプ 114 の SMF レコードに反映され、INGPUSMF 等で表形式レポートを作成する。",
["対象リソースの APPLICATION INFO ポリシーの Inform List に SMF を指定する。",
 "SMFPRMxx でタイプ 114 レコードの収集を有効化する。",
 "APL/APG/MTR の状況変化が SMF タイプ 114 レコードへ記録されることを確認する。",
 "SMF データを順次データ・セットへダンプし INGPUSMF で表形式レポートを生成する。"],
"可用性・リカバリー時間レポートで状況変化を記録する SMF レコードのタイプはどれか?",
["タイプ 30","タイプ 114","タイプ 99","タイプ 70"],1,
"APL/APG/MTR の状況変化はタイプ 114 の SMF レコードに反映され、INGPUSMF で表形式レポートを作成する。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.81 / Users_Guide.pdf p.115")

add("10522",
"プロセッサー・オペレーション・メッセージの自動化を追加した後、新しい自動化定義をビルドする。NetView 自動化テーブル（AT）と SA z/OS コマンド・セットを用いてコンソール自動化を実装し、構成をビルドして自動化エージェントへ反映する。ビルドは ACF/AMC/AT/MRT/MPF が常に同期して呼び出される。",
["カスタマイズ・ダイアログで新しい自動化テーブル定義/オーバーライドを行う。",
 "構成ビルド・パネルで構成をビルドし、ACF/AMC/AT/MRT/MPF が同期生成されることを確認する。",
 "INGAMS で新しい構成をロード/リフレッシュする。",
 "AT エントリーがアクティブになり対象メッセージが自動化されることを NETLOG で確認する。"],
"新しい自動化定義のビルドで常に同期して生成されるのはどれか?",
["SMF とログストリーム","ACF/AMC/AT/MRT/MPF","SDF パネルのみ","RDS テーブルのみ"],1,
"構成ビルドでは ACF・AMC・AT・MRT・MPF が常に同期して生成され、INGAMS でロードする。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.96 / Defining_Automation_Policy.pdf p.335")

add("10523",
"自動化状況ファイル（ACF）に独自の情報をコーディングできる。自動化ポリシーはカスタマイズ・ダイアログで定義され、データは ACF に格納される。例えば ACFREP を呼び出して自動化制御ファイルから DUMP や PURG の応答を発行するなど、応答情報をポリシーで定義し ACF へ格納して利用する。",
["カスタマイズ・ダイアログで応答情報（ACFREP 用）を自動化ポリシーに定義する。",
 "構成をビルドして ACF に独自情報を格納する。",
 "ACFREP を呼び出してポリシーに定義した応答（例: DUMP / PURG）が発行されることを確認する。",
 "NETLOG で ACF から取得された応答の発行を確認する。"],
"自動化状況ファイル（ACF）に格納した応答情報を発行するために呼び出すルーチンはどれか?",
["AOCQRY","ACFREP","INGMON","INGALERT"],1,
"応答情報はポリシーで定義され ACF に格納され、ACFREP の呼び出しで DUMP/PURG などの応答が発行される。",
"TSA_z_OS_4.3_Programmers_Reference.pdf p.38 / Customizing_and_Programming.pdf p.3")

add("10529",
"プロキシー定義の概念では、プロセッサー・オペレーションで自動化したい各ターゲット・システムについて、プロセッサー・オペレーション・リソースをエントリー・タイプ System（SYS）として、対応するプロキシー・リソースをエントリー・タイプ Application（APL）として定義する。多数のプロキシーを定義する場合はアプリケーション・クラス概念を利用できる。ターゲット・システムは ISQCCMD や ISQSEND などプロセッサー・オペレーション・コマンドで管理される。",
["カスタマイズ・ダイアログでターゲット・システムごとに SYS とプロキシー APL を定義する。",
 "多数定義する場合はアプリケーション・クラス概念を利用する。",
 "ISQCCMD/ISQSEND によりターゲット・システムへハードウェア/MVS コマンドを送れることを確認する。",
 "プロキシーと SYS が一対一に対応していることを INGLIST で確認する。"],
"プロキシー定義の概念で、ターゲット・システムの管理に使用するコマンドはどれか?",
["AOCQRY/INGMON","ISQCCMD/ISQSEND","ACF/INGAMS","SDF/SDFTREE"],1,
"ターゲット・システムは ISQCCMD や ISQSEND などのプロセッサー・オペレーション・コマンドで管理される。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.90 / p.89")

add("10530",
"アプリケーション・リソース（APL）の構成では、カスタマイズ・ダイアログのアプリケーション・エントリーで APPLICATION INFO ポリシー項目などを設定し、起動/停止コマンド、監視、Inform List（SDF/EIF/E2E/IOM/ITM/SMF/TTT/USR）などを定義する。APL をアプリケーション・グループ（APG）経由でシステム/シスプレックスにリンクして自動化対象とする。",
["カスタマイズ・ダイアログで APL の APPLICATION INFO に起動/停止/監視を設定する。",
 "Inform List で状況変化の伝播先（SDF/SMF/E2E など）を指定する。",
 "APL を APG 経由でシステム/シスプレックスにリンクする。",
 "INGLIST で APL が想定どおり構成・自動化されていることを確認する。"],
"APL の Inform List に指定できる伝播先として正しいものはどれか?",
["TYPE114 のみ","SDF/EIF/E2E/IOM/ITM/SMF/TTT/USR","JES2/JES3 のみ","CDS/ENQ のみ"],1,
"Inform List には SDF・EIF・E2E・IOM・ITM・SMF・TTT・USR を指定でき、状況変化の伝播先を制御する。",
"TSA_z_OS_4.3_Defining_Automation_Policy.pdf p.285 / p.139")

add("10531",
"Automatic Restart Manager（ARM）は z/OS 基本コンポーネントで、指定アプリケーションがアベンドした場合や、シスプレックス内のシステムが障害を起こした場合に、designated なアプリケーションを自動的に（別システム上で）再始動するリカバリー機能である。SA z/OS システム・オペレーションは ARM と協調動作し、ARM 関連状況（例: EXTSTART は外部で起動/再始動中）を SA z/OS 状況にマッピングする。",
["ARM 対応アプリケーションに一意のエレメント名を MVS Automatic Restart Management Element Name フィールドで定義する。",
 "アプリケーションをアベンドさせ ARM が自動再始動を行うことを確認する。",
 "SA z/OS 状況に EXTSTART（外部起動/再始動中）が反映されることを INGLIST で確認する。",
 "シスプレックス内システム障害時に ARM が別システムで再始動することを確認する。"],
"ARM 関連で「アプリケーションが外部で起動/再始動中」を示す SA z/OS 状況はどれか?",
["AUTODOWN","EXTSTART","BROKEN","CTLDOWN"],1,
"ARM では EXTSTART 状況がアプリケーションが外部で起動/再始動中であることを示す。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.267")

add("10533",
"VOST（仮想オペレーター・ステーション・タスク）を管理するため、タイプ NONMVS のアプリケーションを作成する。INGCPSM を実行する VOST は、INGVSTRT を APL の起動コマンドとして使い（そのジョブ名を VOST のアタッチ名とする）、INGVSTOP の停止コマンド列で停止し、管理 APL 内の INGVMON 監視ルーチンで状況を監視する。",
["カスタマイズ・ダイアログでタイプ NONMVS の VOST 管理アプリケーションを作成する。",
 "起動コマンドに INGVSTRT、停止コマンドに INGVSTOP を定義する。",
 "監視ルーチンに INGVMON を指定し VOST の状況を監視する。",
 "INGVMON の戻りコード 0（VOST が ACTIVE）を NETLOG で確認する。"],
"VOST を管理するアプリケーションで起動コマンドとして使用するのはどれか?",
["INGVMON","INGVSTRT","INGVSTOP","AOCQRY"],1,
"VOST は INGVSTRT を起動コマンド、INGVSTOP を停止コマンド、INGVMON を監視ルーチンとして管理する。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.60 / Programmers_Reference.pdf p.215")

add("10534",
"自動化プロシージャの作成では、NetView コマンド・リスト（CLIST）や REXX などの解釈型言語、あるいは PL/I・C・アセンブラーなどのコンパイル型言語を使用する。解釈型の場合は NetView コマンド・リスト・ライブラリーへコピーし、任意で CNMCMDU メンバーへエントリーを追加すると検出・呼び出しが高速になる。",
["REXX/CLIST で自動化プロシージャを作成し NetView コマンド・リスト・ライブラリーへコピーする。",
 "任意で NetView DSIPARM の CNMCMDU メンバーにエントリーを追加する。",
 "自動化テーブル（AT）から当該プロシージャがトリガーされるよう定義する。",
 "対象メッセージを発生させ、プロシージャが呼び出されることを NETLOG で確認する。"],
"解釈型言語（REXX/CLIST）の自動化プロシージャを高速に検出・呼び出すために任意で追加するメンバーはどれか?",
["AOFINIT","CNMCMDU","SMFPRMxx","AOFTREE"],1,
"REXX/CLIST はコマンド・リスト・ライブラリーへコピーし、任意で CNMCMDU メンバーへエントリーを追加すると高速に検出される。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.37")

add("10535",
"カスタマイズの章では、SA z/OS のカスタマイズ・ダイアログを使って自動化ポリシーを作成・編集し、ポリシー・データベース（PDB）から構成ファイルをビルドする方法を扱う。エントリー・タイプ（APL/APG/SYS/MTR など）を選択し、定義したオブジェクトをシステムにリンクして、企業リソースの扱いを指定する。",
["TSO/E にログオンしカスタマイズ・ダイアログを起動する。",
 "エントリー・タイプ選択パネルで APL/APG/SYS/MTR などを選び定義する。",
 "定義をシステム/シスプレックスへリンクする。",
 "PDB から構成ファイルをビルドし INGAMS でロードする。"],
"カスタマイズ・ダイアログで構成ファイルをビルドする元となるものはどれか?",
["SMF データ・セット","ポリシー・データベース（PDB）","SDF ツリー構造","RDS VSAM ファイル"],1,
"カスタマイズ・ダイアログではポリシー・データベース（PDB）内のデータから構成ファイルをビルドする。",
"TSA_z_OS_4.3_Get_Started_Guide.pdf p.49 / Defining_Automation_Policy.pdf p.45")

json.dump(C,open(CJSON,'w',encoding='utf-8'),ensure_ascii=False)
print("total:",len(C))
