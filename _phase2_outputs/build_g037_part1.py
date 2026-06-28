# -*- coding: utf-8 -*-
import json, os

rows = []

def add(rid, title, naiyou, verify, q, choices, ans, expl, source, rag):
    rows.append({
        "row_id": rid, "title": title, "naiyou_jp": naiyou,
        "verify_steps": verify,
        "quiz": {"q": q, "choices": choices, "answer": ans, "explanation": expl},
        "source": source, "rag_hit": rag
    })

# 7453 ACB Monitor Customization
add("7453","ACB Monitor Customization",
"ACB（アプリケーション制御ブロック）モニターのフォーカルポイントは、フォーカルポイント VTAM および入口点 VTAM から ACB の状況更新を受信する。Tivoli Business Service Manager と併用すると、汎用リソース、ユーザー指定アプリケーション、ユーザー指定モデルに一致するアプリケーションを検出できる。ACB の状況、セッション数、永続セッションなどを監視する。",
"NetView コンソールにログオンし、INITAMON コマンドを入口点パラメーターなしで発行して ACB モニターを初期化する。続いて INITAMON entry_point を発行して特定の入口点を活動化し、ACB 状況更新がフォーカルポイントへ報告されることを確認する。",
"ACB モニターのフォーカルポイントが ACB 状況を受信する相手はどれか。",
["フォーカルポイント VTAM および入口点 VTAM","TCP/IP スタックのみ","RODM データベースのみ","JES サブシステム"],0,
"ACB モニターはフォーカルポイント VTAM と入口点 VTAM の両方から ACB 状況更新を受信する。",
"NetView_6.4_Customization_Guide.pdf p.168","NetView_6.4_Customization_Guide.pdf p.168 / Command_Reference_Vol1 p.498"),

# 7454 Accessing publications online
add("7454","Accessing publications online",
"IBM Z NetView のマニュアルはオンラインで参照でき、IBM Knowledge Center（資料センター）から HTML 形式や PDF 形式で入手できる。CNMSTYLE 初期化ステートメントなどのカスタマイズ情報は、Customization Guide や Installation: Getting Started などの関連資料を相互参照しながら確認する。オンライン参照により最新の更新内容を反映した情報を得られる。",
"NetView オンラインヘルプから HELP コマンドを発行し、参照したいコマンド名（例: HELP VIEW）を指定してオンライン資料を表示する。Web ブラウザーで IBM Knowledge Center を開き、製品バージョン 6.4 のライブラリーから該当 PDF を取得して内容が一致することを確認する。",
"NetView のオンライン資料を参照する主な入口はどれか。",
["IBM Knowledge Center（資料センター）","RACF データベース","SYS1.PARMLIB","VTAMLST"],0,
"オンライン資料は IBM Knowledge Center から HTML/PDF で参照できる。",
"NetView_6.4_Customization_Guide.pdf p.11","NetView_6.4_Customization_Guide.pdf p.193 publications accessing online"),

# 7455 Adding Optional Tasks to the NetView Program
add("7455","Adding Optional Tasks to the NetView Program",
"NetView プログラムには必須タスクのほかに任意（オプション）タスクを追加できる。タスクは CNMSTYLE メンバーおよび CNMSTASK メンバーの TASK ステートメントで定義され、最も変更頻度の高い TASK ステートメントは CNMSTYLE 側に置かれる。オプションタスクを追加することで、機能（タワー）の有効化や追加のデータサービスを利用できる。",
"DSIPARM の CNMSTUSR または CxxSTGEN メンバーに、追加したいオプションタスク用の TASK ステートメントを記述する。NetView を再初期化（または該当タスクを START）し、LIST STATUS=TASKS を発行して新しいタスクが活動状態になっていることを確認する。",
"NetView のタスクを定義するステートメントが置かれるメンバーはどれか。",
["CNMSTYLE および CNMSTASK","DSIPARM の DSIOPF","SYS1.PROCLIB","BNJPNL1"],0,
"TASK ステートメントは CNMSTYLE と CNMSTASK で定義され、変更頻度の高いものは CNMSTYLE に置かれる。",
"NetView_6.4_Customization_Guide.pdf p.27","NetView_6.4_Administration_Reference.pdf p.265 TASK statements"),

# 7456 Adding or Modifying Resource Types
add("7456","Adding or Modifying Resource Types",
"ハードウェアモニターに対して、ユーザー定義のエラーやリソースタイプを追加・変更できる。汎用コードポイント（generic code point）の作成・変更や、リソースタイプの追加により、パネルが動的に構築される。これにより独自機器や独自エラー条件をハードウェアモニターの表示に反映できる。",
"BNJPNL1 DD のコードポイントメンバーを編集してリソースタイプを追加し、MODCTBL（または該当する活動化コマンド）でコードポイントテーブルをテストおよび活動化する。NPDA のイベント明細パネルで新しいリソースタイプが正しく表示されることを確認する。",
"ハードウェアモニターでパネルを動的に構築するために使われるものはどれか。",
["汎用コードポイント（generic code point）","RACF プロファイル","VTAM モードテーブル","SMF レコード"],0,
"汎用コードポイントを使ってハードウェアモニターのパネルが動的に構築される。",
"NetView_6.4_Customization_Guide.pdf p.108","NetView_6.4_Customization_Guide.pdf p.85 generic code points"),

# 7457 Advanced Customization - SNMP Trap Forwarding
add("7457","Advanced Customization - SNMP Trap Forwarding",
"Event/Automation Service のトラップ・ツー・アラート変換タスクは、データグラムソケットを通じてトラップを受信する。このソケットは設定したポートにバインドされる。SNMP トラップ転送の高度なカスタマイズでは、受信ポートやエンタープライズ OID、コミュニティー名などを構成ファイルで調整し、SNMP マネージャーへの転送経路を制御する。",
"トラップ・ツー・アラートサービス構成ファイル（IHSATCFG 等）で PortNumber や NetViewAlertReceiver ステートメントを設定する。z/OS コンソールから IHSAEVNT ジョブで Event/Automation Service を開始し、SNMP トラップが指定ポートで受信・変換されることをトラブルシューティングガイドの手順で確認する。",
"トラップ・ツー・アラート変換タスクがトラップを受信する仕組みはどれか。",
["指定ポートにバインドされたデータグラムソケット","VTAM の APPL メジャーノード","RODM のオブジェクトリンク","JES の SYSOUT"],0,
"トラップはポートにバインドされたデータグラムソケット経由で受信される。",
"NetView_6.4_Customization_Guide.pdf p.158","NetView_6.4_Customization_Guide.pdf p.158 SNMP Trap Forwarding"),

# 7458 Advanced Customization - Translating Data
add("7458","Advanced Customization - Translating Data",
"EIF イベントと異なり、SNMP トラップのデータは文字ストリング以外のデータタイプを持つことがある。変数バインディングが ASCII オクテットストリングである場合の翻訳を支援するため、追加のエスケープシーケンス $[ と $] が用意されている。データ翻訳の高度なカスタマイズでは、トラップ内のデータタイプに応じて適切なストリングへ変換する処理を制御する。",
"トラップ・ツー・アラート構成で対象の変数バインディングに $[ $] エスケープシーケンスを適用するよう編集する。Event/Automation Service を再始動し、NPDA のイベント明細で ASCII オクテットストリングが正しく文字列に翻訳されていることを確認する。",
"EIF イベントと異なり SNMP トラップデータが持ちうるのはどれか。",
["文字ストリング以外のデータタイプ","常に固定長 8 バイト","必ず EBCDIC エンコード","RODM フィールド型のみ"],0,
"SNMP トラップデータは文字ストリング以外のデータタイプを持ちうる点が EIF イベントと異なる。",
"NetView_6.4_Customization_Guide.pdf p.127","NetView_6.4_Customization_Guide.pdf p.158 Translating Data escape $[ $]"),

with open(os.path.join(os.path.dirname(__file__),'_g037_part1.json'),'w',encoding='utf-8') as f:
    json.dump(rows,f,ensure_ascii=False)
print("part1",len(rows))
