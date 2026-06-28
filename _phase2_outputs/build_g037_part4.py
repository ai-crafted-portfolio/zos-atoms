# -*- coding: utf-8 -*-
import json, os
rows=[]
def add(rid,title,naiyou,verify,q,choices,ans,expl,source,rag):
    rows.append({"row_id":rid,"title":title,"naiyou_jp":naiyou,"verify_steps":verify,
    "quiz":{"q":q,"choices":choices,"answer":ans,"explanation":expl},"source":source,"rag_hit":rag})
EAS="Event/Automation Service は、NetView のアラートやメッセージを EIF イベントや SNMP トラップへ変換し、Tivoli Netcool/OMNIbus などのイベントサーバーへ転送する仲介サービスである。"

add("7476","Considerations",
"NetView Instrumentation（インスツルメンテーション）を構成する際の考慮事項を扱う。インスツルメンテーションの開始・停止やパフォーマンスへの影響を考慮し、収集する統計の範囲やオーバーヘッドを評価する。TASKUTIL などのコマンドで定期的にタスクの CPU・ストレージ使用状況を確認することが推奨される。",
"NetView コンソールで TASKUTIL を発行し、タスクの CPU・ストレージ使用状況を確認する。EVERY タイマーを自動タスク配下に設定し、一定間隔でインスツルメンテーション統計を取得して傾向を把握する。",
"インスツルメンテーションの考慮事項として適切なものはどれか。",
["パフォーマンスへの影響と収集オーバーヘッドを評価する","RACF プロファイルを必ず削除する","VTAM 始動オプションを無効化する","SMF を停止する"],0,
"インスツルメンテーション導入時はパフォーマンス影響とオーバーヘッドを考慮する。",
"NetView_6.4_Customization_Guide.pdf p.165","NetView_6.4_Tuning_Guide.pdf p.129 TASKUTIL instrumentation"),

add("7477","Controlling Color and Highlighting of Fields",
"フィールドの色と強調表示は、パネルソースファイル内の特殊文字によって制御する。ドル記号（$）やパーセント記号（%）などの特殊文字がフィールドの属性を指定する。一般ヘルプフィールドでもこれらの特殊文字を用いて色や強調表示を定義する。",
"パネルソースに $ や % などの属性制御文字を記述してフィールドの色・強調表示を指定する。VIEW でパネルを表示し、各フィールドが指定どおりの色・強調表示になっていることを確認する。",
"フィールドの色と強調表示を制御する要素はどれか。",
["ソースファイル内の特殊文字（$、% など）","RACF NETCMDS クラス","VTAM モードテーブル","SMF サブタイプ"],0,
"$ や % などの特殊文字でフィールドの色と強調表示を制御する。",
"NetView_6.4_Customization_Guide.pdf p.52","NetView_6.4_Customization_Guide.pdf p.46 special characters $ % fields"),

add("7478","Copying and Changing Help Source Files",
"ヘルプソースファイルをコピーして変更することで、独自のオンラインヘルプを作成できる。まずヘルプソースファイルの場所を特定し、コピーしたうえで内容を編集する。NetView 稼働中に変更する場合は、パネルデータセットを 2 次エクステントなしで定義することが推奨される。",
"既存のヘルプソースファイルをユーザーデータセットへコピーし、内容を編集する。HELP コマンドで変更後のヘルプパネルを表示し、正しく反映されていることを確認する。",
"独自ヘルプ作成の最初の手順はどれか。",
["ヘルプソースファイルの場所を特定してコピーする","RODM クラスを定義する","VTAM ノードを活動化する","SMF レコードを採取する"],0,
"まずヘルプソースファイルの場所を特定し、コピーしてから変更する。",
"NetView_6.4_Customization_Guide.pdf p.78","NetView_6.4_Customization_Guide.pdf p.75 locate help source files"),

add("7479","Creating a Rollable Component with VIEW",
"VIEW コマンドを用いて、ロール可能（rollable）なコンポーネントを作成できる。ロール可能コンポーネントは、複数のパネル間をロール（切り替え）して表示できる全画面コンポーネントである。compname に PF キー定義で使用する名前を指定し、パネル定義とパラメーターを適切にコーディングする。",
"VIEW コマンドで compname を指定したロール可能コンポーネントのパネル定義を作成する。NetView でコマンドを実行し、PF キーでコンポーネント間をロールできることを確認する。",
"VIEW でロール可能コンポーネントを識別する名前を指定するオペランドはどれか。",
["compname","pnlname","NOINPUT","COMPAT"],0,
"compname は PF キー定義で使用される、コンポーネントを識別する名前である。",
"NetView_6.4_Customization_Guide.pdf p.60","NetView_6.4_Customization_Guide.pdf p.48 VIEW compname rollable"),

add("7480","Creating Full-Screen Panels",
"全画面パネルは VIEW コマンドで表示される、ユーザー定義の全画面表示である。パネルソースに属性シンボルや変数、コマンド行（チルダ）を記述して、入力フィールドや表示内容を定義する。INPUT／NOINPUT オプションにより入力可否を制御する。",
"パネルソースに全画面パネルの定義（属性シンボル、変数、コマンド行）を記述する。VIEW コマンドでパネルを表示し、全画面で正しくレイアウトされ入力が機能することを確認する。",
"全画面パネルを表示するコマンドはどれか。",
["VIEW","SRFILTER","TASKUTIL","GENALERT"],0,
"全画面パネルは VIEW コマンドで表示する。",
"NetView_6.4_Customization_Guide.pdf p.45","NetView_6.4_Customization_Guide.pdf p.48 full-screen panels VIEW"),

add("7481","Cross-Reference for Message and Environment Functions",
"メッセージ関数および環境関数の相互参照は、コマンドリストやコマンドプロセッサーで利用できる組み込み関数を一覧化したものである。REXX や NetView コマンドリスト言語の関数（APPLID()、ASID()、AUTOTASK() など）を機能別に参照でき、メッセージ属性や実行環境の情報取得に用いる。",
"コマンドリスト内でメッセージ・環境関数（例: APPLID()、ATTENDED()）を呼び出すコードを記述する。NetView で実行し、関数が現在の環境・メッセージ情報を正しく返すことを確認する。",
"メッセージ・環境関数の相互参照が一覧化する対象はどれか。",
["コマンドリストで利用できる組み込み関数","RACF プロファイル","VTAM ノード","SMF サブタイプ"],0,
"相互参照はコマンドリストで利用できるメッセージ・環境の組み込み関数を一覧化する。",
"NetView_6.4_Customization_Guide.pdf p.30","NetView_6.4_Programming_REXX p.215 built-in functions"),

add("7482","Customization",
"NetView のカスタマイズは、CNMSTYLE 初期化ステートメント、パネル、ヘルプ、自動化テーブル、ハードウェアモニター表示、Event/Automation Service など多岐にわたる。カスタマイズ領域を理解し、変更前に検討すべき機能を確認したうえで、CNMSTUSR や CxxSTGEN などのユーザーメンバーへ変更を加える。",
"カスタマイズしたい領域（例: CNMSTYLE）を特定し、ユーザーメンバー（CNMSTUSR/CxxSTGEN）へ変更を記述する。NetView を再初期化し、カスタマイズが反映されていることを確認する。",
"NetView のカスタマイズで変更を加えるべきメンバーはどれか。",
["CNMSTUSR や CxxSTGEN などのユーザーメンバー","デフォルトの CNMSTYLE メンバー本体","SYS1.PARMLIB","VTAMLST"],0,
"カスタマイズはデフォルトの CNMSTYLE を直接変更せず CNMSTUSR/CxxSTGEN へ加える。",
"NetView_6.4_Customization_Guide.pdf p.165","NetView_6.4_Administration_Reference.pdf p.31 CNMSTUSR CxxSTGEN"),

add("7483","Customization Areas",
"カスタマイズ領域は、NetView を自社環境に合わせて調整する対象範囲を示す。パネル、ヘルプ情報、ハードウェアモニター表示、自動化、Event/Automation Service、PF キーなどが含まれる。各領域に対し、変更前に検討すべき機能を理解してから設計を行う。",
"カスタマイズ対象の領域（パネル、ヘルプ、自動化など）を選定し、関連するユーザーメンバーやサンプルを編集する。NetView を再初期化し、対象領域のカスタマイズが反映されることを確認する。",
"NetView のカスタマイズ領域に含まれないものはどれか。",
["VTAM の NCP 生成（NetView のカスタマイズ領域ではない）","パネル","ヘルプ情報","ハードウェアモニター表示"],0,
"パネル・ヘルプ・ハードウェアモニター表示などが領域で、NCP 生成は NetView カスタマイズ領域ではない。",
"NetView_6.4_Customization_Guide.pdf p.17","NetView_6.4_Customization_Guide.pdf p.17 customization areas"),

add("7484","Customization Considerations",
"カスタマイズを行う際の考慮事項として、変更前に検討すべき機能の把握、デフォルトメンバーを直接変更しないこと、ユーザーメンバー（CNMSTUSR／CxxSTGEN）の使用、互換性や保守性への影響評価が挙げられる。これらを踏まえて安全にカスタマイズを設計する。",
"カスタマイズ計画時に対象機能と影響範囲を洗い出し、ユーザーメンバーへ変更を限定する方針を確認する。変更後に NetView を再初期化し、既存機能に影響が出ていないことを確認する。",
"カスタマイズの考慮事項として適切なものはどれか。",
["デフォルトメンバーを直接変更せずユーザーメンバーを使う","必ず VTAMLST を書き換える","RACF を無効化する","SMF を停止する"],0,
"デフォルトメンバーを直接変更せず CNMSTUSR/CxxSTGEN を使うのが基本方針である。",
"NetView_6.4_Customization_Guide.pdf p.113","NetView_6.4_Installation_Migration_Guide.pdf p.83 do not modify default CNMSTYLE"),

with open(os.path.join(os.path.dirname(__file__),'_g037_part4.json'),'w',encoding='utf-8') as f:
    json.dump(rows,f,ensure_ascii=False)
print("part4",len(rows))
