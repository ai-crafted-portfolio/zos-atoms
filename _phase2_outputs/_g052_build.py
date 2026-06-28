# -*- coding: utf-8 -*-
import json, os

BASE = os.path.dirname(__file__)
PDF = "TSA_z_OS_4.3_Customizing_and_Programming.pdf"

# meta: row_id -> (title, page, source_pdf)
meta = {m['row_id']: m for m in json.load(open(os.path.join(BASE,'g052_targetA.json'),encoding='utf-8'))}

# content authored from RAG (English read, Japanese written)
# each: rid -> dict(naiyou, steps[list], q, choices[4], answer, expl, rag, src(optional))
C = {}

def add(rid, naiyou, steps, q, choices, answer, expl, rag, src=None):
    C[rid] = dict(naiyou=naiyou, steps=steps, q=q, choices=choices,
                  answer=answer, expl=expl, rag=rag, src=src or PDF)

# 10442 Actions in Response to Incoming WTORs
add("10442",
"MESSAGES/USER DATA 自動化ポリシー項目を使って、アプリケーション・モニターリソース・MVS コンポーネント宛ての着信 WTOR（応答要求付き Write-to-Operator）に対する SA z/OS の応答を定義する。CMD アクション（必要に応じて CODE アクションと組み合わせ）で WTOR に対して発行するコマンドを定義し、REP アクションで即時に返す応答を定義する。応答が定義されていない WTOR は OUTREP により SA z/OS が保管し、対応する自動化テーブル文が生成される。",
["NetView コンソールで対象サブシステムの WTOR を発生させ、DSI/IEE 系メッセージとして着信させる。",
 "カスタマイズ・ダイアログの MESSAGES/USER DATA 項目で CMD / REP / CODE アクションが定義されていることを確認する。",
 "WTOR 着信時に定義したコマンド/応答が %AOFOPGSSOPER% で示される作業オペレータへルーティングされることを NETLOG で確認する。",
 "応答未定義の WTOR が OUTREP により保管され SDF に表示されることを確認する。"],
"着信 WTOR に対する SA z/OS の応答（コマンド/返信）を定義するために使用するポリシー項目はどれか?",
["AUTOMATION FLAGS","MESSAGES/USER DATA","MONITOR INFO","APPLICATION INFO"],1,
"着信 WTOR への CMD/REP/CODE アクションは MESSAGES/USER DATA 項目で定義する。応答未定義の WTOR は OUTREP で保管される。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.166 / p.165")

# 10444 Active Health Monitoring
add("10444",
"モニターリソース（MTR）は監視対象オブジェクトのヘルス状況を取得し、その状況は APL/APG へ伝播されて統合ヘルス状況となる。アクティブ・ヘルス監視ではポーリング、すなわち監視コマンドを一定間隔で周期的に実行して状況を判定する。アクティブ・モニターはポリシーで定義された間隔に基づきスケジュールされ、戻りコードによって SA z/OS が適切にヘルス状況を設定する。",
["NetView 自動化環境で MTR の MONITOR INFO ポリシーに監視コマンドと監視間隔を定義する。",
 "INGLIST または SDF で対象 MTR のヘルス状況（NORMAL/WARNING など）を確認する。",
 "監視間隔ごとに監視コマンドが実行され、その戻りコードがヘルス状況へ反映されることを NETLOG で確認する。",
 "MTR のヘルス状況が関連 APL/APG へ伝播されていることを INGLIST で確認する。"],
"アクティブ・ヘルス監視で MTR がオブジェクトのヘルス状況を判定する方法はどれか?",
["イベント処理による受動的判定","監視コマンドの周期的なポーリング","SDF パネルの色変化","SMF レコードの集計"],1,
"アクティブ・モニターは監視間隔に基づき監視コマンドを周期的に実行（ポーリング）してヘルス状況を判定する。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.44 / p.47")

# 10445 Adding a New Application to Automation
add("10445",
"新しいアプリケーションを自動化に追加するには、まず Define an Application Policy Object でアプリケーション・ポリシー・オブジェクトを定義し、システムまたはシスプレックスへ（アプリケーション・グループ経由で）リンクして構成をビルドする。ビルド後はアプリケーションが SA z/OS に認識され、定義したポリシーに従って自動化される。",
["カスタマイズ・ダイアログでエントリー・タイプ APL の新規アプリケーション・ポリシー・オブジェクトを定義する。",
 "APL をアプリケーション・グループ（APG）経由でシステム/シスプレックスへリンクする。",
 "構成をビルドし、INGAMS で自動化構成をロード/リフレッシュする。",
 "INGLIST で新規アプリケーションが認識され自動化対象となっていることを確認する。"],
"新しいアプリケーションを自動化へ追加する際、最初に行う定義はどれか?",
["SDF パネルの定義","アプリケーション・ポリシー・オブジェクトの定義","ゲートウェイ・セッションの定義","SMF レコードの有効化"],1,
"まずアプリケーション・ポリシー・オブジェクト（APL）を定義し、APG 経由でシステムにリンクしてビルドすることで自動化対象となる。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.25 / p.21")

# 10446 Adding the Application to Automation
add("10446",
"アプリケーション・ポリシー・オブジェクトを定義した後、それを自動化に追加する段階では、アプリケーション・グループ（APG）を介してアプリケーションをシステムまたはシスプレックスへリンクする。これにより SA z/OS は当該アプリケーションをポリシーに基づいて起動・停止・監視できるようになる。",
["カスタマイズ・ダイアログで対象アプリケーションを APG にリンクする。",
 "APG をシステムまたはシスプレックスへリンクし、間接リンクを成立させる。",
 "構成をビルドして INGAMS でロードする。",
 "INGLIST でアプリケーションが対象システム上のリソースとして生成されていることを確認する。"],
"アプリケーションをシステムへ結び付ける（自動化対象にする）ために使う仕組みはどれか?",
["アプリケーション・グループ（APG）による間接リンク","SDF ツリー構造","ゲートウェイ・オートタスク","SMF タイプ 114 レコード"],0,
"APL はシステムへ直接リンクできず、APG を介して間接的にリンクすることで自動化対象となる。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.25 / Defining_Automation_Policy.pdf p.87")

# 10449 Alert-Based Notification
add("10449",
"アラート・ベース通知では、INGALERT メッセージ ID のコード定義を用いて、通知ターゲットへ渡すイベントの追加属性を定義したり、特定アラートのイベント生成を抑止したりできる。コード定義はアラート ID・発行ジョブ・通知ターゲット種別に応じて行え、APL・APG・MTR および MVS コンポーネントのリソースに対して適用できる。該当するコード定義が見つからない場合は対応する MVS コンポーネントの INGALERT 定義が参照される。",
["カスタマイズ・ダイアログで対象リソースの INGALERT メッセージ ID に対するコード定義を行う。",
 "INGCNTL コマンドでアラート機能を有効化し、ALERTMODE（IOM/EIF/TTT/USR など）を設定する。",
 "対象リソースで状況変化を発生させ INGALERT が通知ターゲットへイベントを送出することを確認する。",
 "NETLOG / SDF で通知の発行とコード定義の適用結果を確認する。"],
"アラート・ベース通知で通知属性の定義に使用するメッセージ ID はどれか?",
["ING150I","INGALERT","ISQ900I","AOF603D"],1,
"INGALERT メッセージ ID のコード定義により、APL/APG/MTR/MVS コンポーネントの通知属性やイベント抑止を定義する。",
"TSA_z_OS_4.3_Customizing_and_Programming.pdf p.78 / p.77")

print("part1 loaded:", len(C))
json.dump(C, open(os.path.join(BASE,'_g052_content.json'),'w',encoding='utf-8'), ensure_ascii=False)
