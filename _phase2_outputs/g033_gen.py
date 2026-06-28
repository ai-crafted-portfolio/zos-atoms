# -*- coding: utf-8 -*-
import json

rows = json.load(open('_phase2_outputs/g033_rows.json', encoding='utf-8'))
APG = "NetView_6.4_Application_Programmers_Guide.pdf"

def Q(q, choices, ans, exp):
    return {"q": q, "choices": choices, "answer": ans, "explanation": exp}

# Authored, RAG-grounded content keyed by row_id.
# naiyou_jp: 2-4 sentences (JP). verify: console-session reproduction (JP). quiz dict. source (manual ref). rag_hit (English page anchor).
C = {}

C["6632"] = dict(
 naiyou_jp="MDS-MU（multiple-domain support message unit）は、LU 6.2 会話上で要求と応答を運ぶデータの封筒であり、エージェント作業単位相関子（agent-unit-of-work correlator）と、トランザクション内でのデータの目的を示すフラグビットを含む。受信側アプリケーションは「応答を期待する要求」「応答を期待しない要求」などの種別に応じて受け取った MDS-MU を処理する。NetView 高性能トランスポート API は MS トランスポート API と異なり、送信した MDS-MU ごとの確認応答を行わない。",
 verify="NetView コンソールで NCCFIC にログオンし、`LIST STATUS=TASKS` で DSI6DST など MS トランスポート関連タスクが ACTIVE であることを確認する。受信側アプリを登録した後、`DISPLU` や受信者状況照会で MDS-MU を受信したことをログ（NETLOG）で確認する。",
 quiz=Q("MDS-MU に含まれ、トランザクションを一意に識別するものはどれか。",
   ["エージェント作業単位相関子（X'1549'）", "RACF ユーザー ID", "VTAM ログモード名", "SMF レコード番号"], 0,
   "MDS-MU はエージェント作業単位相関子とフラグビットを含み、相関子がトランザクションを一意に識別する。"),
 source=f"{APG} p.91 (Accepting an MDS-MU)", rag_hit=f"{APG} p.58 / p.55")

C["6633"] = dict(
 naiyou_jp="NetView の刊行物はオンラインで参照でき、コンソールから HELP コマンドでオンラインヘルプ機能を利用できる。問題判別時には、たとえば異常終了（ABEND）に対して `HELP ABEND` と入力することで該当する説明を表示できる。アプリケーションプログラマーは、SNA Formats や Management Services の関連刊行物を併せて参照する必要がある。",
 verify="NCCF コンソールで `HELP ABEND` と入力し、異常終了コードに関するオンラインヘルプが表示されることを確認する。続けて `HELP` のみを入力して NetView ヘルプメニューが開くことを確認する。",
 quiz=Q("NetView のオンラインヘルプ機能を呼び出すコマンドはどれか。",
   ["HELP", "BROWSE", "VPDCMD", "SEQUENT"], 0,
   "オンラインヘルプ機能は HELP コマンドで呼び出し、`HELP ABEND` のように引数を付けて特定トピックを表示できる。"),
 source=f"{APG} p.12 (Accessing publications online)", rag_hit="NetView_6.4_Troubleshooting_Guide.pdf p.64")

C["6634"] = dict(
 naiyou_jp="Additional Product Set Attributes（追加製品セット属性、サブベクター X'86'）は、VPDCMD コマンドで収集される製品識別データの一部で、製品セット ID サブベクターに付随する追加属性を運ぶ SNA サブベクターである。製品セット ID（PSID）は 2〜9 文字の英数字で、アラート送出時には PSID キーワードで指定される。これらのサブベクターはネットワーク資産管理での製品情報の解釈に用いられる。",
 verify="NCCF で `VPDCMD` をサービスポイント宛てに発行し、返ってくる製品データに製品セット ID 関連サブベクターが含まれることをログで確認する。GENALERT 系コマンドで PSID キーワードを付けてアラートを生成し、サブベクター構造を確認する。",
 quiz=Q("サブベクター X'86'（Additional Product Set Attributes）が属するデータはどれか。",
   ["製品識別／ネットワーク資産管理の VPD", "RACF 監査レコード", "REXX 変数プール", "GTF トレースバッファ"], 0,
   "X'86' は製品セット ID に付随する追加製品属性を運ぶサブベクターで、VPD（vital product data）として収集される。"),
 source=f"{APG} p.119 (Additional Product Set Attributes Subvector X'86')", rag_hit=f"{APG} p.6 / Command_Reference_Vol1 p.452")

C["6635"] = dict(
 naiyou_jp="エージェント作業単位相関子（X'1549'）GDS 変数は MDS ヘッダーに含まれ、作業単位（unit of work）を一意に識別する。発信元ノード名（NETID と LU 名）、発信元 MS アプリケーション名、および作業単位を一意化する日時付きシーケンス番号で構成される。MDS 応答やエラーメッセージは、元の要求と同じ相関子を返さなければならない。",
 verify="MS トランスポートを使うアプリ間でトランザクションを発生させ、NETLOG で送信 MDS-MU と応答 MDS-MU の相関子が一致することを確認する。構文エラー時には MDS エラーメッセージとソフトウェアアラートがハードウェアモニターへ生成されることを確認する。",
 quiz=Q("X'1549' GDS 変数（エージェント作業単位相関子）の役割はどれか。",
   ["作業単位を一意に識別する", "バッファキュー上限を設定する", "RACF アクセスを許可する", "GTF へトレースを書き出す"], 0,
   "X'1549' は発信元名・MS アプリ名・日時付きシーケンス番号からなり、作業単位（トランザクション）を一意に識別する。"),
 source=f"{APG} p.105 (Agent Unit of Work Correlator X'1549' GDS Variable)", rag_hit=f"{APG} p.106 (Table 14)")

C["6636"] = dict(
 naiyou_jp="Answering Node Configuration Data（応答ノード構成データ）は、VPDCMD コマンドで返される vital product data（VPD）の一種で、応答（answering）側ノードの構成情報を表す。ネットワーク資産管理では、この種の VPD をシリアル番号・機種・モデル番号などのインベントリ情報として収集する。NetView はデバイスから返されたデータの正当性検証は行わない。",
 verify="NCCF で `VPDCMD` を発行し、応答ノードの構成データが返ることを NETLOG で確認する。サンプルのネットワーク資産管理コマンドリストを実行し、外部ファイルに VPD レコードが記録されることを確認する。",
 quiz=Q("Answering Node Configuration Data はどのコマンドで収集される VPD か。",
   ["VPDCMD", "TRACEPPI", "SEQUENT", "REGISTER"], 0,
   "応答ノード構成データは VPDCMD コマンドが返す VPD の一種で、ネットワーク資産管理で収集される。"),
 source=f"{APG} p.115 (Answering Node Configuration Data)", rag_hit=f"{APG} p.115 (Vital Product Data Descriptions)")

C["6637"] = dict(
 naiyou_jp="Application Program-Level Error Reporting（アプリケーションプログラムレベルのエラー報告）は、MDS エラーメッセージ以外の方法でアプリケーション検出のエラーを報告する仕組みである。コマンド拒否、構文例外、機能未サポートなどのエラーは、応答メジャーベクターなどアプリ独自の手法で報告される。状況によっては MS アプリケーションが、未処理の MDS トランザクションを無条件に終了させる必要がある。",
 verify="MS アプリケーションでタイマーを起動し、応答が来ないトランザクションをアプリ側で打ち切る挙動を再現する。NETLOG で MDS エラーメッセージまたはアプリ定義のエラー応答が記録されることを確認する。",
 quiz=Q("MDS エラーメッセージ以外で報告されるアプリケーションレベルのエラーはどれか。",
   ["コマンド拒否・構文例外・機能未サポート", "GTF バッファ不足", "RACF パスワード期限切れ", "VTAM セッション確立"], 0,
   "これらのエラーは応答メジャーベクターなどアプリ定義の手法で報告され、MDS エラーメッセージとは別経路である。"),
 source=f"{APG} p.112 (Application Program-Level Error Reporting)", rag_hit=f"{APG} p.112")

C["6638"] = dict(
 naiyou_jp="Assembler Programs（アセンブラープログラム）の章では、高水準言語およびアセンブラーを用いて NetView へ要求を送る方法を扱う。MVS でインターフェースを有効化するには、NMVT または CP-MSU 形式のアラートを受信できるよう PPI を初期化し、NetView サブシステムアドレス空間を起動する必要がある。アセンブラーでは DSIxxx 系マクロを使って要求パラメーターブロックを構築する。",
 verify="NetView サブシステムアドレス空間を起動し、`DISPPI` などで PPI が ACTIVE であることを確認する。アセンブラーサンプル（例: CNMS4287）をアセンブル・リンクして実行し、アラートがハードウェアモニターに到達することを確認する。",
 quiz=Q("MVS でアラート受信用インターフェースを有効化するために必要な前提はどれか。",
   ["NetView サブシステムアドレス空間の初期化（PPI 有効化）", "GTF の停止", "RACF クラス APPL の削除", "SEQUENT 排他制御の取得"], 0,
   "NMVT/CP-MSU アラートを受信するには PPI を有効化し、NetView サブシステムアドレス空間を初期化する必要がある。"),
 source=f"{APG} p.22 (Assembler Programs)", rag_hit=f"{APG} p.27 (Enabling the Interface for MVS)")

C["6639"] = dict(
 naiyou_jp="Attached Device Configuration Data（接続デバイス構成データ、サブベクター X'82'）は、VPDCMD コマンドで返される VPD の一種で、ノードに接続されたデバイスの構成情報を表す SNA サブベクターである。ネットワーク資産管理のコマンドリストがこのサブベクターを解釈し、インベントリレコードとして外部ファイルに記録する。",
 verify="NCCF で `VPDCMD` をサービスポイント宛てに発行し、接続デバイス構成データ（X'82'）が返ることを NETLOG で確認する。サンプルコマンドリストで該当レコードタイプが外部ファイルに出力されることを確認する。",
 quiz=Q("サブベクター X'82' が表す VPD はどれか。",
   ["接続デバイス構成データ", "コマンド統計", "RACF 監査", "セッション稼働率"], 0,
   "X'82' は接続デバイス構成データ（Attached Device Configuration Data）を表すサブベクターで VPD の一部である。"),
 source=f"{APG} p.118 (Attached Device Configuration Data Subvector X'82')", rag_hit=f"{APG} p.6 (Subvector list)")

C["6640"] = dict(
 naiyou_jp="Avoiding Interlock（インターロック回避）は、長時間実行コマンドや WAIT を含むプログラムでデッドロックを避けるための技法を扱う。長時間実行コマンドはアセンブラーマクロ DSIPUSH を用いて待機し、その間もメッセージ自動化など必須の NetView 機能を継続させる。コマンドリストでは &WAIT による待機やネスト時の制約に注意し、メッセージキューの肥大化を避ける必要がある。",
 verify="REXX コマンドリストで長時間実行コマンドを発行し、待機中も他コマンドが低優先度キューで処理されることを `LIST` 系コマンドで確認する。WAIT 応答が無くプロセッサ使用も増えない状態を再現し、Troubleshooting Guide の WAIT キーワードに沿って切り分ける。",
 quiz=Q("長時間実行コマンドが待機中に必須機能を継続させるために使うアセンブラーマクロはどれか。",
   ["DSIPUSH", "DSIGET", "DSIMQS", "DSIPRS"], 0,
   "長時間実行コマンドは DSIPUSH を使って待機し、低優先度キュー上の他コマンドやメッセージ自動化の継続を可能にする。"),
 source=f"{APG} p.64 (Avoiding Interlock)", rag_hit="NetView_6.4_Programming_REXX_and_NetView_Command_List_Language.pdf p.25")

C["6641"] = dict(
 naiyou_jp="Buffering Replies（応答のバッファリング）は、データ要求に対する応答をすぐに転送するか、バッファに溜めるかを選択する技法である。PL/I・C のプログラムでは、応答待ちの間にプログラムを中断するか継続するかを選べ、継続させる場合は応答をバッファリングするか即時受信するかを指定できる。複数の応答を最大 31K まで 1 回の送信にブロック化することもでき、その場合受信側は処理前にブロックを分解する。",
 verify="PL/I/C アプリで応答待ちをバッファリング指定にして起動し、応答が即時転送されずキューに溜まることを確認する。複数応答をブロック化送信し、受信側で 1 送信に複数応答が含まれていることを NETLOG で確認する。",
 quiz=Q("ブロック化した応答の 1 回のデータ送信で許容される最大サイズはどれか。",
   ["31K", "1024 バイト", "208 バイト", "4096 バイト"], 0,
   "NetView は最大 31K のデータ送信をサポートし、複数応答をまとめて 1 回の送信でブロック化できる。"),
 source=f"{APG} p.73 (Buffering Replies)", rag_hit=f"{APG} p.57 / p.59")

C["6642"] = dict(
 naiyou_jp="Building the Request Buffer（要求バッファの構築）は、PPI へ要求を送るための要求パラメーターバッファ（RPB）を組み立てる作業を指す。RPB は固定長（96 バイト）の構造で、要求種別（TYPE）、受信者 ID、ワークエリアアドレス、バッファキュー上限などのフィールドを持つ。各要求ごとに RPB を構築し、PPI は同じ RPB を使って結果（戻りコード等）をプログラムへ返す。",
 verify="アセンブラー／HLL サンプルで RPB を初期化し、TYPE フィールドに要求種別をセットして PPI を呼び出す。戻りコードが RPB に格納されることを確認し、`DISPPI` で PPI 状況を照会する。",
 quiz=Q("PPI が要求結果（戻りコード）を返すために使う構造はどれか。",
   ["同じ要求パラメーターバッファ（RPB）", "SMF レコード", "GTF トレーステーブル", "RACF プロファイル"], 0,
   "プログラムは RPB で要求を送り、PPI は同じ RPB を使ってデータと戻りコードをプログラムに返す。"),
 source=f"{APG} p.29 (Building the Request Buffer)", rag_hit=f"{APG} p.18 (Processing Requests)")

C["6643"] = dict(
 naiyou_jp="Character Tables（文字テーブル）は、正規表現や自動化テーブルでの文字クラス照合に用いられるテーブルである。NetView の自動化では、メッセージ ID やテキスト内の文字パターンを照合し、条件に応じてコマンドを実行する。文字テーブルは正規表現処理（PIPE の LOCATE/NLOCATE、REXX の MATCH、自動化テーブル関数 DSIAMMCH）で使われる文字集合の定義を支える。",
 verify="自動化テーブルに正規表現を含むメッセージ照合条件を定義し、テスト用メッセージを投入して該当アクションが起動することを `MSG` 系コマンドや NETLOG で確認する。`PIPE ... | LOCATE /pattern/` で文字パターン照合を検証する。",
 quiz=Q("文字テーブルが関与する正規表現の利用箇所として正しいものはどれか。",
   ["PIPE の LOCATE/NLOCATE と REXX の MATCH", "GTF 外部トレース", "RACF パスワード検証", "VPDCMD のサブベクター"], 0,
   "正規表現は PIPE の LOCATE/NLOCATE、REXX の MATCH、自動化テーブル関数 DSIAMMCH で利用される。"),
 source=f"{APG} p.85 (Character Tables)", rag_hit=f"{APG} p.81 (Regular expressions)")

C["6644"] = dict(
 naiyou_jp="Choosing the Request Type（要求種別の選択）では、PPI 要求の構成要素となる要求種別を選ぶ。各プログラムは、まず要求ごとに要求パラメーターバッファ（RPB）を構築し、適切な要求種別（例: 1=PPI 状況照会、4=受信者の定義と初期化、12=アラート送信、14=同期データ送信、22=データ受信など）を設定する。要求種別はプログラムの構築ブロックとして機能する。",
 verify="サンプルプログラムで RPB に TYPE=1（PPI 状況照会）をセットし戻りコード 10（PPI 利用可能）を確認する。続けて TYPE=4 で受信者を定義し、`DISPPI` で受信者が ACTIVE になることを確認する。",
 quiz=Q("PPI の各プログラムが要求ごとに最初に行うことはどれか。",
   ["要求パラメーターバッファ（RPB）の構築", "GTF の起動", "RACF への ADDUSER", "VTAM メジャーノードの活性化"], 0,
   "各要求では、まず RPB を構築し、選択した要求種別を設定する。要求種別はプログラムの構築ブロックである。"),
 source=f"{APG} p.34 (Choosing the Request Type)", rag_hit=f"{APG} p.34 (Table 2) / p.18")

C["6645"] = dict(
 naiyou_jp="Common Operations Services Commands（共通操作サービスコマンド、COS）は、サービスポイントアプリケーション宛てに RUNCMD などのコマンドを流す仕組みである。DSIGDS タスクが MS トランスポートに SPCS（COS_NETOP）として登録し、COS コマンドが MS API 上を流れる。コマンドが MS API を流れるとき、メジャーベクターは MDS-MU の CP-MSU 内の X'1212' GDS 変数に格納され、RUNCMD の SP パラメーターが宛先 LU 名、EP_COS が宛先となる。",
 verify="NCCF で `RUNCMD SP=spname,EP_COS,...` を発行し、COS コマンドがサービスポイントへ流れ応答が返ることを NETLOG で確認する。`LIST STATUS=TASKS` で DSIGDS タスクが ACTIVE であることを確認する。",
 quiz=Q("COS コマンドが MS API を流れるとき、メジャーベクターが格納される GDS 変数はどれか。",
   ["X'1212'（CP-MSU 内）", "X'1549'", "X'1311'", "X'86'"], 0,
   "COS コマンドの MS API 経由では、メジャーベクターは MDS-MU の CP-MSU 内の X'1212' GDS 変数に置かれる。"),
 source=f"{APG} p.91 (Common Operations Services Commands)", rag_hit=f"{APG} p.91 (DSIGDS / COS_NETOP)")

C["6646"] = dict(
 naiyou_jp="Considerations for Applications（アプリケーションでの考慮事項）は、どのトランスポート API を使うかを決める際の指針を補足する。事前構築済みの MDS-MU を使うとアプリは単純化されるが、インターフェース利用のための準備作業が増える場合がある。PL/I・C のプログラムでは、応答待ちでプログラムを中断するか継続するか、応答をバッファリングするか即時受信するかを選べる。",
 verify="PL/I/C サンプルで事前構築済み MDS-MU を用いる方式と、サービスルーチンにヘッダー構築を任せる方式の双方を実行し、挙動の差を NETLOG で比較する。応答待ちの中断／継続オプションを切り替えて確認する。",
 quiz=Q("事前構築済みの MDS-MU を使う利点はどれか。",
   ["アプリケーションが単純化される", "RACF 認可が不要になる", "GTF が自動起動する", "バッファ上限が無制限になる"], 0,
   "事前構築済み MDS-MU はアプリを単純化するが、インターフェース利用のための準備作業が増える場合がある。"),
 source=f"{APG} p.57 (Considerations for Applications)", rag_hit=f"{APG} p.57")

C["6647"] = dict(
 naiyou_jp="Controlling overuse of SEQUENT Names（SEQUENT 名の過剰使用の抑制）は、SEQUENT コマンドで資源を直列化する際に、SEQUENT 名を使いすぎないよう管理する技法である。SEQUENT は OBTAINEX（排他制御）または OBTAINSH（共有制御）で資源を獲得し、RELEASE で解放する。排他制御中は他のプログラムは待機させられるため、名前の粒度設計が並行性に影響する。",
 verify="複数タスクで同一 SEQUENT 名に対し OBTAINEX を発行し、後続タスクが先行タスクの RELEASE まで待機することを再現する。OBTAINSH に変えると共有アクセスが並行することを確認する。",
 quiz=Q("SEQUENT で排他制御を獲得するキーワードはどれか。",
   ["OBTAINEX", "OBTAINSH", "RELEASE", "REGISTER"], 0,
   "OBTAINEX は排他制御、OBTAINSH は共有制御を獲得し、RELEASE で解放する。排他中は他プログラムが待機する。"),
 source=f"{APG} p.62 (Controlling overuse of SEQUENT Names)", rag_hit=f"{APG} p.61-62 (SEQUENT)")

C["6648"] = dict(
 naiyou_jp="Controlling the Trace Facility（トレース機能の制御）は、コマンド機能トレースで、ディスパッチ・バッファのキューイング・プレゼンテーションサービス・モジュール入出口・記憶域取得解放・出口呼び出しなどを記録する制御を扱う。DSITRACE タスクを起動し、TRACE コマンドの OPTION や MODE（INT/EXT）でトレース対象を指定する。内部トレース（MODE=INT）が既定で、外部出力（MODE=EXT）は DSITRACE データセットを用いる。",
 verify="NCCF で `START TASK=DSITRACE` を実行し、`TRACE` コマンドで OPTION=(DISP,PSS,QUE,STOR,UEXIT) を指定する。トレースが内部（INT）に記録され、`TRACE` 照会で状態を確認する。",
 quiz=Q("コマンド機能トレースを外部データセットへ書き出すモードはどれか。",
   ["MODE=EXT", "MODE=INT", "MODE=GTF のみ", "MODE=RACF"], 0,
   "MODE=EXT は DSITRACE データセットへ外部出力する。既定は MODE=INT（内部・仮想記憶）である。"),
 source=f"{APG} p.101 (Controlling the Trace Facility)", rag_hit="NetView_6.4_Users_Guide_NetView.pdf p.180 / Troubleshooting_Guide p.118")

C["6650"] = dict(
 naiyou_jp="CP-MSU Format（CP-MSU 形式）は、制御点管理サービス単位（control point management services unit）の形式で、MS トランスポートとそのアプリケーション（ハードウェアモニター含む）が用いるデータ型の一つである。MDS-MU 内では X'1212' GDS 変数として CP-MSU が運ばれる。NMVT・CP-MSU 形式のアラートを NetView へ送る要求種別 12 では、これらの形式が用いられる。",
 verify="アセンブラー／HLL サンプルで要求種別 12 を使い CP-MSU 形式アラートを送出し、ハードウェアモニターのフィルター（AREC/ESREC）を PASS にしてアラートが表示されることを確認する。NETLOG で CP-MSU が到達したことを確認する。",
 quiz=Q("CP-MSU が MDS-MU 内で格納される GDS 変数はどれか。",
   ["X'1212'", "X'1549'", "X'82'", "X'7D'"], 0,
   "COS/MS 経由ではメジャーベクター（CP-MSU 含む）は MDS-MU の X'1212' GDS 変数に置かれる。"),
 source=f"{APG} p.107 (CP-MSU Format)", rag_hit=f"{APG} p.107 (MS data types)")

C["6651"] = dict(
 naiyou_jp="Creating Buffer Queues（バッファキューの作成）は、HLL サービスルーチンが扱うデータ・メッセージキューを準備する処理である。受信者を定義する要求種別 4 でバッファキュー上限（BUFFQ-L）を設定でき、SETBQL コマンドでも上限を後から調整できる。NetView サブシステムアドレス空間は、受信者数と平均バッファサイズ・キュー上限から必要な記憶域を確保する必要がある。",
 verify="要求種別 4 で受信者を定義し BUFFQ-L を設定する。`SETBQL receiverid qlimit` でバッファキュー上限を変更し、`DISPPI` で反映を確認する。",
 quiz=Q("受信者のバッファキュー上限を後から調整するコマンドはどれか。",
   ["SETBQL", "TRACEPPI", "RUNCMD", "GENALERT"], 0,
   "SETBQL コマンドで受信者のバッファキュー上限（0〜4294967295）を調整できる。"),
 source=f"{APG} p.19 (Creating Buffer Queues)", rag_hit="NetView_6.4_Command_Reference_Vol2_O-Z.pdf p.243 (SETBQL)")

C["6652"] = dict(
 naiyou_jp="Data Formats for LU 6.2 Conversations（LU 6.2 会話のデータ形式）は、MDS-MU の形式を規定する付録である。MDS-MU は MDS ヘッダーとアプリケーションプログラム GDS 変数から成り、全体は 32767（X'7FFF'）バイト未満、MDS ヘッダーは 1024（X'400'）バイトでなければならない。アプリケーションプログラム GDS 変数の最大は 31743（X'7BFF'）バイトである。",
 verify="MS トランスポートでアプリ間データを送信し、MDS-MU 全体長が 32767 バイト未満かつ MDS ヘッダーが 1024 バイトであることを、構文エラー時の MDS エラーメッセージ（先頭 100 バイトを含む）で確認する。",
 quiz=Q("MDS ヘッダーの長さとして正しいものはどれか。",
   ["1024（X'400'）バイト", "208 バイト", "31743 バイト", "4096 バイト"], 0,
   "MDS ヘッダーは 1024（X'400'）バイト、アプリ GDS 変数の最大は 31743 バイト、MDS-MU 全体は 32767 バイト未満。"),
 source=f"{APG} p.103 (Data Formats for LU 6.2 Conversations)", rag_hit=f"{APG} p.103")

C["6653"] = dict(
 naiyou_jp="DCE Data（DCE データ）は、VPDCMD コマンドで返される VPD の一種だが、NetView for z/OS V5R4 以降は非推奨（deprecated）である。歴史的には分散コンピューティング環境（DCE）に関する製品情報を運んだ。現在のネットワーク資産管理では、製品データやリンク構成データなど他の VPD 種別が用いられる。",
 verify="`VPDCMD` を発行し、返る VPD 種別の中で DCE データが非推奨である旨を文書で確認する。サンプルコマンドリスト（VPDDCE 等）の挙動を確認し、現行構成では他の VPD 種別を使うことを確認する。",
 quiz=Q("DCE Data（VPD の一種）の現在の扱いはどれか。",
   ["NetView for z/OS V5R4 以降は非推奨", "唯一の必須 VPD", "RACF 専用データ", "GTF トレース形式"], 0,
   "DCE データは VPD の一種だが V5R4 以降は deprecated（非推奨）である。"),
 source=f"{APG} p.118 (DCE Data)", rag_hit=f"{APG} p.115 (Vital Product Data Descriptions)")

C["6654"] = dict(
 naiyou_jp="Deciding Which Transport API to Use（使用するトランスポート API の決定）では、アプリケーションが NetView MS トランスポート API と高性能トランスポート API のどちらを使うかを選ぶ指針を示す。MS トランスポートは遠隔操作やアーキテクチャ準拠の管理サービスに適し、高性能トランスポートは性能重視のアプリや RU サイズ等のセッションパラメーター指定が必要な場合に適する。高性能トランスポートは MDS-MU ごとの確認応答を行わず会話を持続させる分、一般的なエラー通知のみとなる。",
 verify="同一トランザクションを MS トランスポートと高性能トランスポートで実行し、確認応答の有無やネットワークトラフィック量の差を NETLOG・性能指標で比較する。`LIST STATUS=TASKS` で各トランスポートタスクの状態を確認する。",
 quiz=Q("高性能トランスポート API の特徴として正しいものはどれか。",
   ["MDS-MU ごとの確認応答を行わず会話を持続させる", "全 MDS-MU を確認応答する", "LU 6.2 を使わない", "アラート送信専用である"], 0,
   "高性能トランスポートは MDS-MU ごとの確認応答を省き LU 6.2 会話を持続させるため高速だが、エラー通知は一般的なものになる。"),
 source=f"{APG} p.56 (Deciding Which Transport API to Use)", rag_hit=f"{APG} p.56 / Tuning_Guide p.115")

C["6655"] = dict(
 naiyou_jp="Description of Available APIs（利用可能な API の説明）は、NetView が提供する LU 6.2 系トランスポート API（MS トランスポート API と高性能トランスポート API）の概要を説明する。両者の外部機能の多くは共通だが、高性能トランスポートは異なる LU 6.2 プロトコルを使って性能を高め、会話を持続させる。アプリは用途に応じて適切な API を選択する。",
 verify="文書で両 API の機能差（確認応答・会話持続・エラー通知粒度）を確認し、サンプルアプリで MS／高性能の両方を起動して挙動を比較する。",
 quiz=Q("NetView が提供する 2 つの LU 6.2 系トランスポート API はどれか。",
   ["MS トランスポート API と高性能トランスポート API", "RACF API と SAF API", "GTF API と SMF API", "REST API と SNMP API"], 0,
   "NetView は MS トランスポート API と高性能トランスポート API の 2 つの LU 6.2 系 API を提供する。"),
 source=f"{APG} p.95 (Description of Available APIs)", rag_hit=f"{APG} p.55")

C["6656"] = dict(
 naiyou_jp="Destination Name（宛先名）は、MS アプリケーション宛てに送るデータの送り先を特定する名前で、宛先ロケーションの NETID・修飾なし LU 名・MS アプリケーションプログラム名から成るロケーション名 MS サブベクターで構成される。名前は A〜Z・0〜9・$・#・@ を使い、英字は大文字かつ先頭は非数字とする。$・#・@ は移行目的のみで新規利用は避ける。",
 verify="MS アプリで宛先名（NETID・LU 名・アプリ名）を指定して送信し、宛先で受信されることを NETLOG で確認する。不正文字を含む名前で送信し、拒否されることを確認する。",
 quiz=Q("宛先名（ロケーション名 MS サブベクター）に含まれないものはどれか。",
   ["RACF パスワード", "NETID", "修飾なし LU 名", "MS アプリケーションプログラム名"], 0,
   "宛先名は宛先の NETID・修飾なし LU 名・MS アプリ名から成る。RACF パスワードは含まれない。"),
 source=f"{APG} p.68 (Destination Name)", rag_hit=f"{APG} p.104")

C["6657"] = dict(
 naiyou_jp="Differences between Transports（トランスポート間の差異）は、MS トランスポート API と高性能トランスポート API の違いを説明する。高性能トランスポートは MDS-MU ごとの確認応答を行わず、LU 6.2 会話をアイドル時も持続させるため、会話の停止・再開のオーバーヘッドを排除する。高性能トランスポートは user-written アプリ向けの汎用 LU 6.2 API で、性能を高める異なる LU 6.2 プロトコルを使う。",
 verify="MS と高性能の各トランスポートでアイドル時の会話状態を観測し、高性能では会話が持続することを `DISPLU` 等で確認する。確認応答の頻度差を NETLOG で比較する。",
 quiz=Q("MS トランスポートと比べた高性能トランスポートの違いはどれか。",
   ["アイドル時も LU 6.2 会話を持続させる", "LU 6.2 を使わない", "確認応答を増やす", "アラート専用である"], 0,
   "高性能トランスポートは確認応答を省き、アイドル時も会話を持続させて停止・再開のオーバーヘッドを排除する。"),
 source=f"{APG} p.55 (Differences between Transports)", rag_hit=f"{APG} p.55 / p.77")

C["6658"] = dict(
 naiyou_jp="Disconnecting a Receiver（受信者の切断）は、PPI 受信者をインターフェースから切り離す操作である。受信者は要求種別 9（無効化）や要求種別 10（削除）で状態を変更でき、REXX では DSIPHONE の CLOSE で受信者を削除できる。切断後はその受信者宛てのデータは受け付けられない。",
 verify="要求種別 9 で受信者を無効化し、`DISPPI` で状態が INACTIVE になることを確認する。続けて要求種別 10 または DSIPHONE 'CLOSE' で受信者を削除し、状態が undefined になることを確認する。",
 quiz=Q("REXX（DSIPHONE）で PPI 受信者を削除するキーワードはどれか。",
   ["CLOSE", "OPENRECV", "SEND", "AUTHRECV"], 0,
   "DSIPHONE の CLOSE は指定した PPI 受信者を削除する。OPENRECV は受信者を定義する。"),
 source=f"{APG} p.90 (Disconnecting a Receiver)", rag_hit=f"{APG} p.91 (DSIPHONE CLOSE)")

C["6662"] = dict(
 naiyou_jp="Enabling the Interface for MVS（MVS でのインターフェース有効化）は、NetView が NMVT または CP-MSU 形式のアラートを受信できるようにする手順である。まず NetView サブシステムアドレス空間を初期化して PPI を有効化し、受信者がキューに溜めるデータを保持できる十分なリージョンサイズを確保する。必要記憶域は受信者数・平均バッファサイズ・バッファキュー上限から見積もる。",
 verify="NetView サブシステムアドレス空間を起動し、`DISPPI` で PPI が ACTIVE であることを確認する。要求種別 12 でアラートを送り、受信されることを NETLOG で確認する。",
 quiz=Q("MVS でアラート受信を有効化する最初のステップはどれか。",
   ["NetView サブシステムアドレス空間の初期化（PPI 有効化）", "GTF の停止", "RACF の削除", "SEQUENT の取得"], 0,
   "NMVT/CP-MSU アラート受信のため、まず NetView サブシステムアドレス空間を初期化して PPI を有効化する。"),
 source=f"{APG} p.27 (Enabling the Interface for MVS)", rag_hit=f"{APG} p.27")

C["6663"] = dict(
 naiyou_jp="Examples（例）の節は、PPI やトランスポート API を用いるプログラムのコーディング例を示す。NetView 配布テープには NMVT/CP-MSU アラート送信例（アセンブラー CNMS4287、C CNMS4257、PL/I CNMS4227）などのサンプルが含まれる。これらの例を参照して受信者の定義・データ送受信・アラート送信の実装方法を学べる。",
 verify="配布データセットからサンプル（例: CNMS4257）を取り出してコンパイル・リンクし、実行してアラートがハードウェアモニターに到達することを確認する。NETLOG で結果を確認する。",
 quiz=Q("NMVT/CP-MSU アラート送信の PL/I サンプルはどれか。",
   ["CNMS4227", "CNMS4287", "CNMS4257", "DSIPHONE"], 0,
   "アセンブラーは CNMS4287、C は CNMS4257、PL/I は CNMS4227 がアラート送信サンプルである。"),
 source=f"{APG} p.87 (Examples)", rag_hit=f"{APG} p.19 (sample CNMS42xx)")

C["6664"] = dict(
 naiyou_jp="External Log Record Formats（外部ログレコード形式）は、SMF ログやユーザー作成ログへ書き出される各種 NetView ログレコードの形式を規定する付録である。レコードは外部ログレコードヘッダーに続くデータセクションで構成される。代表例として、ハードウェアモニターが書く type 37、コマンド監査・統計の type 38、セッションモニター系の type 39 がある。",
 verify="SMF へのログ出力を有効化し（例: CMDMON.INIT.LOGSMF を CNMSTYLE で指定）、コマンド監視を起動して SMF に type 38 レコードが書かれることを確認する。`RECORD` コマンドで type 39 を生成し SMF を確認する。",
 quiz=Q("NetView の外部ログレコードが書き出される先として正しいものはどれか。",
   ["SMF ログまたはユーザー作成ログ", "RACF データベース", "GTF トレースのみ", "VTAM ログモードテーブル"], 0,
   "外部ログレコードは SMF ログまたはユーザー作成ログへ書き出される。"),
 source=f"{APG} p.127 (External Log Record Formats)", rag_hit=f"{APG} p.127")

C["6665"] = dict(
 naiyou_jp="External Log Record Type 37（外部ログレコード type 37）は、ハードウェアモニターが書き出すレコードで、type 37・サブタイプ 4 として外部ログに記録される。各レコードは外部ログレコードヘッダーに続くデータセクションで構成される。SMF などの外部ログを解析して、ハードウェアモニターが捕捉したイベント情報を取得できる。",
 verify="ハードウェアモニターのアラート捕捉を有効化し、テストアラートを送出して SMF に type 37 サブタイプ 4 レコードが書かれることを SMF ダンプで確認する。",
 quiz=Q("type 37 レコードを書き出す NetView コンポーネントはどれか。",
   ["ハードウェアモニター", "セッションモニター", "コマンド監査機能", "REST サーバー"], 0,
   "type 37・サブタイプ 4 はハードウェアモニターが外部ログへ書き出すレコードである。"),
 source=f"{APG} p.127 (External Log Record Type 37)", rag_hit=f"{APG} p.127")

C["6666"] = dict(
 naiyou_jp="External Log Record Type 38（外部ログレコード type 38）は、コマンド監査・コマンド統計に関するレコードである。サブタイプ 1 はコマンド認可テーブルの監査で生成され、DEFAULTS CATAUDIT や PERMIT/EXEMPT の AUDIT キーワードで制御される。サブタイプ 4 はコマンド統計機能が一定間隔で監視対象 NetView コマンドについて生成し、CMDMON.INIT.LOGSMF（CNMSTYLE）または CMDMON コマンドで SMF 出力を指定する。",
 verify="`DEFAULTS CATAUDIT=YES` を設定し認可違反を発生させ、SMF に type 38 サブタイプ 1 が書かれることを確認する。CMDMON を起動して一定間隔でサブタイプ 4 が書かれることを確認する。",
 quiz=Q("type 38 サブタイプ 1 が生成される契機はどれか。",
   ["コマンド認可テーブルの監査", "セッション開始", "アラート捕捉", "GTF トレース"], 0,
   "type 38 サブタイプ 1 はコマンド認可テーブルの監査で生成され、CATAUDIT や AUDIT キーワードで制御される。"),
 source=f"{APG} p.133 (External Log Record Type 38)", rag_hit=f"{APG} p.134")

C["6667"] = dict(
 naiyou_jp="External Log Record Type 39（外部ログレコード type 39）は、セッションモニター系のカウンターレコードである。RECORD コマンドの STRGDATA でカウンターレコード（サブタイプ X'0008'）が書かれ、ネットワーク会計・可用性測定が活動中はセッション開始・終了や SESSTATS で type 39（X'27'）が書かれる。応答時間データ機能が活動中も type 39 が書かれる。",
 verify="セッションモニターを起動し `RECORD SESSTATS` を発行して、SMF に type 39（X'27'）レコードが書かれることを確認する。`RECORD STRGDATA` でストレージ／イベントカウンターレコードが書かれることを確認する。",
 quiz=Q("RECORD コマンドの SESSTATS で書き出される外部ログレコードはどれか。",
   ["type 39（X'27'）", "type 37", "type 38 サブタイプ 1", "type 80"], 0,
   "ネットワーク会計・可用性測定が活動中、SESSTATS や セッション開始終了で type 39（X'27'）が書かれる。"),
 source=f"{APG} p.149 (External Log Record Type 39)", rag_hit=f"{APG} p.149 / p.151")

C["6668"] = dict(
 naiyou_jp="Fields in the RPB（RPB のフィールド）は、要求パラメーターブロック（96 バイト）の各フィールドを説明する。RPB-LEN（長さ）、TYPE（要求種別）、RECEIVER-ID（受信者 ID）、WORK-ADR（ワークエリアアドレス）、BUFFQ-L（バッファキュー上限）、TCB-TOKEN（送信側タスクトークン、PPI が受信時に設定）などがあり、各要求種別ごとに設定／返却されるフィールドが決まる。",
 verify="アセンブラーサンプルで RPB の各フィールド（TYPE、RECEIVER-ID 等）を設定して要求種別 4 を発行し、PPI が返すフィールド（TCB-TOKEN 等）を確認する。`DISPPI` で受信者状態を確認する。",
 quiz=Q("RPB の TCB-TOKEN フィールドはどのように設定されるか。",
   ["PPI が受信要求時に送信側タスクトークンを設定", "RACF が認可時に設定", "VTAM が活性化時に設定", "GTF が常に上書き"], 0,
   "TCB-TOKEN は受信要求で PPI が送信側のタスクトークンを設定する（受信前にユーザーが設定することも可）。"),
 source=f"{APG} p.29 (Fields in the RPB)", rag_hit=f"{APG} p.34 (Table 2)")

C["6669"] = dict(
 naiyou_jp="Get Data Facility（データ取得機能）は、NetView のデータ・メッセージキューから情報を取得する機能で、HLL では CNMGETD 関数（GETDATA）を用いてキュー上のデータを操作する。取得したデータを加工してネットワーク管理を強化できる。データ／メッセージ管理用に複数のキューが定義され、関数で内容を取り出す。",
 verify="HLL アプリで CNMGETD（GETDATA）を呼び出してメッセージキューからデータを取得し、返却データを変数に格納できることを確認する。NETLOG で取得処理の結果を確認する。",
 quiz=Q("HLL でデータ・メッセージキューから情報を取得する関数はどれか。",
   ["CNMGETD", "DSIPUSH", "SETBQL", "VPDCMD"], 0,
   "CNMGETD（GETDATA）関数で NetView のデータ・メッセージキューから情報を取得・操作する。"),
 source=f"{APG} p.78 (Get Data Facility)", rag_hit="NetView_6.4_Programming_PL_I_and_C.pdf p.76 / p.142")

# Generic builders for remaining clustered rows -------------------------------

def add(rid, naiyou, verify, quiz, source, rag):
    C[rid] = dict(naiyou_jp=naiyou, verify=verify, quiz=quiz, source=source, rag_hit=rag)

add("6670",
 "High Performance Transport Restrictions（高性能トランスポートの制約）は、高性能トランスポート API を使えないケースや制限を示す。一部のアプリケーション（アーキテクチャ上 MDS が必須のもの等）は高性能トランスポートを使用できない。高性能トランスポートは MDS-MU ごとの確認を行わないため、データに関する具体的なエラー通知ではなく一般的なエラー通知のみを提供する。",
 "MDS が必須のアプリで高性能トランスポート登録を試み、利用できないことを文書・戻りコードで確認する。高性能トランスポート使用時にエラーを発生させ、通知が一般的なものになることを NETLOG で確認する。",
 Q("高性能トランスポートのエラー通知の特徴はどれか。",
   ["データ固有でなく一般的なエラー通知のみ", "全データに対し詳細通知", "エラー通知を行わない", "RACF 経由でのみ通知"], 0,
   "確認応答を省くため、高性能トランスポートはデータ固有ではなく一般的なエラー通知を提供する。"),
 f"{APG} p.56 (High Performance Transport Restrictions)", f"{APG} p.56 / Tuning_Guide p.115")

add("6671",
 "High-Level Language and Assembler Programming Examples（高水準言語・アセンブラーのプログラム例）は、HLL（PL/I・C）とアセンブラーで PPI 要求を送る実装例を示す。MVS でインターフェースを有効化したうえで、要求パラメーターブロックを構築し、受信者定義・データ送受信・アラート送信などを行う。配布テープのサンプル（CNMS42xx 系）を参照できる。",
 "PL/I・C・アセンブラーの各サンプルを取り出してコンパイル・リンクし、PPI への要求送信が成功することを NETLOG と戻りコードで確認する。",
 Q("HLL/アセンブラー例の前提として正しいものはどれか。",
   ["MVS でインターフェース（PPI）を有効化しておく", "GTF を停止する", "RACF を無効化する", "VTAM を停止する"], 0,
   "HLL/アセンブラーで要求を送るには、まず MVS でインターフェース（PPI）を有効化する必要がある。"),
 f"{APG} p.112 (HLL and Assembler Programming Examples)", f"{APG} p.27 / p.19")

add("6672",
 "High-Level Language Programs（高水準言語プログラム）は、PL/I や C を用いて NetView へ要求を送るプログラムを扱う。HLL ではサービスルーチン（CNMxxx 関数）を介して PPI やトランスポート API を呼び出す。応答待ちの中断／継続や、応答のバッファリング／即時受信を選択できる。",
 "PL/I/C サンプルで CNMxxx サービスルーチンを呼び出して受信者を定義し、データ送受信が成功することを確認する。応答待ちの中断オプションを切り替えて挙動を比較する。",
 Q("HLL プログラムが PPI/トランスポートを呼び出す手段はどれか。",
   ["CNMxxx サービスルーチン", "RACF マクロ", "GTF コマンド", "VTAM API のみ"], 0,
   "PL/I・C などの HLL は CNMxxx 系サービスルーチンを介して PPI やトランスポート API を利用する。"),
 f"{APG} p.95 (High-Level Language Programs)", f"{APG} p.57 / PL_I_and_C p.76")

add("6673",
 "How the Interface Works（インターフェースの仕組み）は、PPI（プログラム間インターフェース）の基本動作を説明する。PPI は要求と呼ばれる基本タスクを実行し、各要求に対し状況を示す戻りコードを生成する。プログラムは要求パラメーターブロック（RPB）で要求を送り、PPI は同じ RPB を使ってデータを返す。NMVT/CP-MSU の構築自体はこの章では扱わない。",
 "サンプルで RPB に要求種別をセットして PPI を呼び出し、戻りコードが RPB に返ることを確認する。`DISPPI` で PPI 状況を照会し基本動作を確認する。",
 Q("PPI が各要求に対して生成するものはどれか。",
   ["要求の状況を示す戻りコード", "RACF プロファイル", "SMF レコードのみ", "VTAM メジャーノード"], 0,
   "PPI は要求ごとに状況を示す戻りコードを生成し、同じ RPB を使ってプログラムへ返す。"),
 f"{APG} p.17 (How the Interface Works)", f"{APG} p.17 / p.18")

add("6674",
 "How the Interface Works with Applications（アプリケーションとのインターフェースの仕組み）は、PPI を介したアプリケーション間のデータ授受の流れを示す。例として、プログラム A が NMVT/CP-MSU アラートを NetView へ送り、別のプログラムがバッファキューからデータバッファを受信する。送信側と受信側は受信者名で結び付けられる。",
 "送信プログラムと受信プログラムを起動し、送信側がデータバッファを受信者キューへ送り、受信側が要求種別 22 で取り出すことを NETLOG で確認する。",
 Q("PPI で送信側と受信側を結び付けるものはどれか。",
   ["受信者名（receiver name）", "RACF グループ", "GTF トレース ID", "VTAM PU 名"], 0,
   "PPI では受信者名でデータの送り先（受信者キュー）を特定し、送信側と受信側を結び付ける。"),
 f"{APG} p.17 (How the Interface Works with Applications)", f"{APG} p.17")

add("6675",
 "IBM Z NetView library（IBM Z NetView ライブラリ）は、NetView 関連の刊行物群を指す。アプリケーションプログラマーは、Application Programmer's Guide のほか、SNA Formats や SNA/Management Services Alert Implementation Guide などの SNA 関連刊行物に精通する必要がある。刊行物はオンラインで参照でき、HELP コマンドでオンラインヘルプを利用できる。",
 "NCCF で `HELP` を入力してオンラインヘルプメニューを表示し、ライブラリ内の該当トピックを参照できることを確認する。",
 Q("アプリケーションプログラマーが併せて精通すべき刊行物はどれか。",
   ["SNA Formats 等の SNA 関連刊行物", "RACF Security Administrator's Guide のみ", "GTF ユーザーズガイドのみ", "VTAM Diagnosis のみ"], 0,
   "アプリプログラマーは SNA Formats や SNA/Management Services Alert Implementation Guide に精通する必要がある。"),
 f"{APG} (IBM Z NetView library)", f"{APG} p.17 (Reference publications)")

add("6676",
 "Implementing High Performance Transport API Applications（高性能トランスポート API アプリの実装）は、高性能トランスポートを使う user-written アプリの作り方を扱う。アプリは CNMHREGIST で高性能アプリとして登録し、CNMHSMU 等のサービスで MDS-MU を送受信する。会話は LU 6.2 上で確立・監視され、アイドル時も持続する。",
 "高性能アプリを CNMHREGIST で登録し、`DISPLU` 等で LU 6.2 会話が確立・持続することを確認する。CNMHSMU で MDS-MU を送信し受信されることを確認する。",
 Q("高性能トランスポートにアプリを登録するサービスルーチンはどれか。",
   ["CNMHREGIST", "CNMGETD", "SETBQL", "VPDCMD"], 0,
   "高性能アプリは CNMHREGIST（CNMHregist）で登録し、CNMHSMU 等で MDS-MU を送受信する。"),
 f"{APG} p.95 (Implementing High Performance Transport API Applications)", f"{APG} p.77 / Command_Reference_Vol2 p.140")

add("6677",
 "Implementing the Application（アプリケーションの実装）は、トランスポート API を用いるアプリを実装する一般的手順を示す。アプリは適切なトランスポートに登録し、宛先名を指定して MDS-MU を送り、応答を受信する。事前構築済み MDS-MU を使うか、サービスルーチンにヘッダー構築を任せるかを選べる。",
 "サンプルアプリを登録・起動し、宛先名を指定して MDS-MU を送信、応答を受信する一連の流れを NETLOG で確認する。",
 Q("アプリ実装で MDS-MU ヘッダーを用意する 2 つの方法はどれか。",
   ["事前構築済み MDS-MU を渡す／サービスルーチンに構築させる", "RACF と SAF", "GTF と SMF", "INT と EXT"], 0,
   "アプリは事前構築済み MDS-MU を渡すか、サービスルーチンにヘッダー構築を任せるかを選べる。"),
 f"{APG} p.95 (Implementing the Application)", f"{APG} p.57 / Programming_Assembler p.263")

add("6678",
 "Initializing a Receiver（受信者の初期化）は、要求種別 4 でプログラムを受信者として定義し状態を active にする操作である。この要求種別はバッファキュー上限のリセットにも使う。RPB には受信者 ID、ワークエリアアドレス、バッファキュー上限（BUFFQ-L）などを設定する。",
 "要求種別 4 を発行して受信者を定義し、`DISPPI` で受信者が ACTIVE になることを確認する。BUFFQ-L を設定してキュー上限が反映されることを確認する。",
 Q("受信者を定義し状態を active にする要求種別はどれか。",
   ["要求種別 4", "要求種別 1", "要求種別 12", "要求種別 22"], 0,
   "要求種別 4 はプログラムを受信者として定義し active にする。バッファキュー上限のリセットにも使う。"),
 f"{APG} p.37 (Initializing a Receiver / Request Type 4)", f"{APG} p.37 (Request Type 4)")

add("6679",
 "Introduction to a Regular Expression（正規表現の導入）は、文字列の望ましい形式を抽象的に記述するパターンである正規表現の概要を示す。正規表現は部分文字列より強力で、多様な要素を記述できる。NetView では PIPE の LOCATE/NLOCATE ステージ、REXX 組込関数 MATCH、自動化テーブル関数 DSIAMMCH で利用できる。",
 "NCCF で `PIPE NETVIEW LOG | LOCATE /pattern/ | CONSOLE` を実行し、正規表現に一致する行のみ抽出されることを確認する。REXX の MATCH 関数でパターン照合を確認する。",
 Q("NetView で正規表現が利用できる箇所はどれか。",
   ["PIPE の LOCATE/NLOCATE、REXX の MATCH、DSIAMMCH", "RACF プロファイル定義", "VTAM ログモード", "GTF オプション"], 0,
   "正規表現は PIPE の LOCATE/NLOCATE、REXX の MATCH、自動化テーブル関数 DSIAMMCH で利用できる。"),
 f"{APG} p.81 (Introduction to a Regular Expression)", f"{APG} p.81")

add("6680",
 "Link Configuration Data（リンク構成データ、サブベクター X'52'）は、VPDCMD コマンドで返される VPD の一種で、ノード間リンクの構成情報を表す SNA サブベクターである。ネットワーク資産管理のコマンドリストがこれを解釈し、インベントリレコードとして外部ファイルに記録する。",
 "`VPDCMD` を発行し、リンク構成データ（X'52'）が返ることを NETLOG で確認する。サンプルコマンドリストで該当レコードが外部ファイルに記録されることを確認する。",
 Q("サブベクター X'52' が表す VPD はどれか。",
   ["リンク構成データ", "応答ノード構成データ", "コマンド統計", "セッション稼働率"], 0,
   "X'52' はリンク構成データ（Link Configuration Data）を表すサブベクターで VPD の一部である。"),
 f"{APG} p.118 (Link Configuration Data Subvector X'52')", f"{APG} p.115 (VPD Descriptions)")

add("6681",
 "Maintaining Data Integrity（データ整合性の維持）は、複数プログラムが直列再利用資源を更新する際にデータの整合性を保つ技法を扱う。SEQUENT コマンドで資源を排他（OBTAINEX）または共有（OBTAINSH）で獲得し、更新時は排他制御を要求することで同時更新による破壊を防ぐ。更新後は RELEASE で解放する。",
 "2 つのタスクで同一資源を SEQUENT OBTAINEX で更新しようとし、一方が待機させられて同時更新が起きないことを再現する。RELEASE 後にもう一方が処理を進めることを確認する。",
 Q("資源を更新するプログラムが要求すべき制御はどれか。",
   ["排他制御（OBTAINEX）", "共有制御（OBTAINSH）", "制御なし", "RACF READ"], 0,
   "資源の内容を変更するプログラムは、同時更新による破壊を防ぐため排他制御（OBTAINEX）を要求すべきである。"),
 f"{APG} p.61 (Maintaining Data Integrity)", f"{APG} p.61-62 (SEQUENT)")

add("6682",
 "Management Services Applications（管理サービスアプリケーション）は、MS トランスポートを使い MDS-MU でアーキテクチャ準拠の管理サービスをやり取りするアプリである。MS アプリは CNMREGIST（REGISTER）で MS アプリケーションとして登録し、操作管理サービス対象アプリやフォーカルポイントアプリとして振る舞える。データ型には CP-MSU・SNACR・ルーティングレポート・NMVT・R&TI などがある。",
 "MS アプリを REGISTER で登録し、`LIST` 系で登録状態を確認する。MS トランスポートで MDS-MU を送受信し、NETLOG で到達を確認する。",
 Q("MS アプリケーションを登録するコマンド／サービスはどれか。",
   ["REGISTER（CNMREGIST）", "VPDCMD", "SETBQL", "TRACEPPI"], 0,
   "MS アプリは REGISTER コマンド（CNMREGIST/CNMRGS サービスルーチン）で登録する。"),
 f"{APG} p.55 (Management Services Applications)", f"{APG} p.107 / Command_Reference_Vol2 p.140")

add("6683",
 "MDS Data Types（MDS データ型）は、MS トランスポートとそのアプリが用いるデータ型を示す。代表的には CP-MSU（制御点管理サービス単位）、SNA 条件報告（SNACR）、ルーティングレポート、NMVT、ルーティング・ターゲティング指示（R&TI）がある。各メジャーベクターは GDS 変数であり、操作管理対象アプリがアーキテクチャ準拠コマンドを遠隔送受信するために用いる。",
 "MS トランスポートで各データ型（CP-MSU、NMVT 等）を含む MDS-MU を送受信し、種別ごとの挙動を NETLOG で確認する。",
 Q("MS トランスポートのデータ型に含まれないものはどれか。",
   ["RACF パスフレーズ", "CP-MSU", "SNA 条件報告（SNACR）", "R&TI"], 0,
   "MDS データ型は CP-MSU・SNACR・ルーティングレポート・NMVT・R&TI などで、RACF パスフレーズは含まれない。"),
 f"{APG} p.107 (MDS Data Types)", f"{APG} p.107")

add("6684",
 "MDS Error Message Example（MDS エラーメッセージ例）は、MDS エラーメッセージの具体例とその構成を示す。MDS エラーメッセージは MDS-MU の一種で、メッセージ種別が MDS error message であり、アプリケーションプログラム GDS 変数として常に SNA 条件報告（X'1532'）を含む。MDS ヘッダー内の X'1549' 相関子が、配送できなかった MDS-MU または失敗トランザクションを特定する。",
 "MS トランスポートで宛先不達のトランザクションを発生させ、MDS エラーメッセージが生成されることを NETLOG で確認する。エラーメッセージに SNA 条件報告（X'1532'）が含まれることを確認する。",
 Q("MDS エラーメッセージが常に含むアプリ GDS 変数はどれか。",
   ["SNA 条件報告（X'1532'）", "製品セット ID（X'10'）", "リンク構成（X'52'）", "CP-MSU（X'1212'）"], 0,
   "MDS エラーメッセージは MDS-MU の一種で、常に SNA 条件報告（X'1532'）をアプリ GDS 変数として含む。"),
 f"{APG} p.93 (MDS Error Message Example)", f"{APG} p.109-110")

add("6685",
 "MDS Error Message Format（MDS エラーメッセージ形式）は、MDS エラーメッセージの形式を規定する。MDS エラーメッセージは、エラーを検出したノードの MDS ルーターまたは通信中の MS アプリから送られ、MDS ヘッダー内の X'1549' 相関子で失敗トランザクションを特定する。NetView は受信した MDS-MU ヘッダーの構文を検査し、エラー時はソフトウェアアラートをハードウェアモニターへ生成し、失敗 MDS-MU の先頭 100 バイトを含む MDS エラーメッセージをシステムログに書く。",
 "不正な MDS-MU ヘッダーを送信し、ソフトウェアアラートがハードウェアモニターに上がり、システムログに先頭 100 バイトを含む MDS エラーメッセージが記録されることを確認する。",
 Q("MDS ヘッダー構文エラー時に NetView が行うことはどれか。",
   ["ソフトウェアアラート生成と先頭 100 バイトのログ記録", "RACF へ通報", "GTF を停止", "VTAM を再起動"], 0,
   "構文エラー時はソフトウェアアラートを生成し、失敗 MDS-MU の先頭 100 バイトを含む MDS エラーメッセージをログに書く。"),
 f"{APG} p.93 (MDS Error Message Format)", f"{APG} p.87 / p.110")

add("6687",
 "MDS Header Structure（MDS ヘッダー構造）は、MDS-MU 内の MDS ヘッダーの構造を示す。MDS ヘッダーは 1024（X'400'）バイトで、MDS ルーティング情報（X'1311'）GDS 変数とエージェント作業単位相関子（X'1549'）GDS 変数を含む。NetView は受信した MDS ヘッダーの構文を検査する。",
 "MS トランスポートで MDS-MU を送信し、MDS ヘッダーが 1024 バイトで X'1311' と X'1549' を含むことを、構文エラー時の MDS エラーメッセージから確認する。",
 Q("MDS ヘッダーに含まれる GDS 変数はどれか。",
   ["X'1311'（ルーティング情報）と X'1549'（作業単位相関子）", "X'10' と X'11'", "X'52' と X'82'", "X'7D' と X'86'"], 0,
   "MDS ヘッダー（1024 バイト）は X'1311' ルーティング情報と X'1549' 作業単位相関子の GDS 変数を含む。"),
 f"{APG} p.107 (MDS Header Structure)", f"{APG} p.103 (Figure 9)")

add("6688",
 "MDS Routing Information（MDS ルーティング情報、X'1311'）GDS 変数は、MDS ヘッダーに含まれ、MDS-MU をどのノード・アプリへ送るかのルーティング情報を運ぶ。X'1549' 作業単位相関子と並んで MDS ヘッダーの主要構成要素であり、NetView は受信時にその構文を検査する。",
 "MS トランスポートで宛先を指定して MDS-MU を送信し、X'1311' ルーティング情報に基づき正しい宛先へ配送されることを NETLOG で確認する。",
 Q("X'1311' GDS 変数の役割はどれか。",
   ["MDS-MU のルーティング情報を運ぶ", "作業単位を一意化する", "製品セット ID を運ぶ", "RACF 認可を行う"], 0,
   "X'1311' は MDS ルーティング情報の GDS 変数で、MDS-MU の送り先情報を運ぶ。"),
 f"{APG} p.105 (MDS Routing Information X'1311' GDS Variable)", f"{APG} p.103")

add("6689",
 "MDS Transactions（MDS トランザクション）は、MDS-MU を用いた要求・応答のやり取りである。種別には「応答を期待する要求」（トランザクション開始）、「応答を期待しない要求」、各種応答がある。応答を期待する要求は、エージェント作業単位相関子で一意に識別されるトランザクションを開始し、関連データを含む MDS-MU の受信を期待する。",
 "MS アプリで「応答を期待する要求」を送り、相関子で対応付けられた応答 MDS-MU が返ることを NETLOG で確認する。応答を期待しない要求の挙動も比較する。",
 Q("「応答を期待する要求」が開始するものはどれか。",
   ["相関子で一意化されるトランザクション", "RACF セッション", "GTF トレース", "VTAM LU-LU セッション"], 0,
   "応答を期待する要求は、エージェント作業単位相関子で一意に識別されるトランザクションを開始する。"),
 f"{APG} p.91 (MDS Transactions)", f"{APG} p.58")

add("6690",
 "MDS-MU Example（MDS-MU 例）は、MDS-MU の具体的な構成例を示す。MDS-MU は MDS ヘッダー（1024 バイト）とアプリケーションプログラム GDS 変数から成り、全体は 32767 バイト未満である。例を通じて、ヘッダー内の X'1311'・X'1549' とアプリデータの配置を理解できる。",
 "MS トランスポートで MDS-MU を送受信し、構文エラー時の MDS エラーメッセージ（先頭 100 バイト）から MDS ヘッダーとアプリ GDS 変数の構成を確認する。",
 Q("MDS-MU の全体長の上限はどれか。",
   ["32767（X'7FFF'）バイト未満", "1024 バイト", "208 バイト", "31K 固定"], 0,
   "MDS-MU 全体は 32767 バイト未満、ヘッダーは 1024 バイト、アプリ GDS 変数最大は 31743 バイト。"),
 f"{APG} p.91 (MDS-MU Example)", f"{APG} p.103")

add("6691",
 "Message to Operator（オペレーターへのメッセージ）は、アプリやコマンドリストからオペレーターへメッセージを送る仕組みである。NetView ではメッセージはオペレーターステーションタスク（OST）の端末に表示され、メッセージ自動化テーブルで処理・抑止・自動化できる。MLWTO 形式の複数行メッセージにも対応する。",
 "コマンドリストからオペレーター宛てメッセージを発行し、OST 端末に表示されることを確認する。自動化テーブルでそのメッセージを抑止・自動化できることを確認する。",
 Q("NetView でオペレーター宛てメッセージが表示される対象はどれか。",
   ["オペレーターステーションタスク（OST）の端末", "GTF データセット", "RACF コンソール", "VTAM バッファ"], 0,
   "オペレーター宛てメッセージは OST の端末に表示され、自動化テーブルで処理できる。"),
 f"{APG} p.91 (Message to Operator)", f"{APG} p.18 / Automation_Guide")

add("6692",
 "MLWTO Attributes Support（MLWTO 属性サポート）は、複数行 WTO（multiline write-to-operator）メッセージの属性を扱うサポートである。NetView はメッセージの行種別（制御行・ラベル行・データ行・終了行）などの MLWTO 属性を認識し、自動化テーブルでこれらの属性に基づく条件照合を行える。",
 "複数行メッセージを生成し、自動化テーブルで MLWTO の行種別属性に基づく照合・アクションが動作することを NETLOG で確認する。",
 Q("MLWTO が指す対象はどれか。",
   ["複数行 WTO メッセージ", "単一行コマンド", "GTF レコード", "RACF プロファイル"], 0,
   "MLWTO は multiline write-to-operator（複数行 WTO）メッセージで、NetView はその属性をサポートする。"),
 f"{APG} p.91 (MLWTO Attributes Support)", f"{APG} (MLWTO) / Automation_Guide")

add("6693",
 "Monitoring the Trace Facility（トレース機能の監視）は、コマンド機能トレースや PPI トレースの状態を監視する操作を扱う。TRACE コマンドや TRACEPPI コマンドで現在のトレース状態（ON/OFF、オプション、MODE）を照会できる。内部トレースは常時有効にしておくことが診断上重要とされる。",
 "NCCF で `TRACE` を引数なしで発行して現在のトレース状態を照会し、`TRACEPPI` で PPI トレース状態を確認する。OPTIONS や MODE が想定どおりか確認する。",
 Q("PPI トレースの状態を照会・制御するコマンドはどれか。",
   ["TRACEPPI", "VPDCMD", "SETBQL", "RUNCMD"], 0,
   "PPI トレースは TRACEPPI コマンドで状態照会・制御する。コマンド機能トレースは TRACE コマンド。"),
 f"{APG} p.101 (Monitoring the Trace Facility)", f"{APG} p.101 / Command_Reference_Vol2 p.456")

add("6694",
 "MS Transport Restrictions（MS トランスポートの制約）は、MS トランスポート API 使用時の制約を示す。MS トランスポートは送信した MDS-MU ごとに確認応答を行い、高性能トランスポートより多くのネットワークトラフィックを生む。アーキテクチャ準拠の管理サービスや遠隔操作には適するが、性能重視のアプリでは高性能トランスポートが推奨される。",
 "MS トランスポートでアプリ間通信を行い、各 MDS-MU に確認応答が伴うことと、トラフィック量が高性能トランスポートより多いことを NETLOG・性能指標で確認する。",
 Q("MS トランスポートの特徴はどれか。",
   ["MDS-MU ごとに確認応答を行う", "確認応答を省く", "LU 6.2 を使わない", "アラート専用"], 0,
   "MS トランスポートは MDS-MU ごとに確認応答を行い、その分トラフィックが増えるが管理サービスに適する。"),
 f"{APG} p.55 (MS Transport Restrictions)", f"{APG} p.55 / Tuning_Guide p.115")

add("6695",
 "Naming the Resource（資源の命名）は、SEQUENT コマンドで直列化する資源に付ける SEQUENT 名の付け方を扱う。同じ SEQUENT 名に対する OBTAINEX/OBTAINSH 要求どうしが直列化の対象となるため、名前の粒度が並行性を左右する。名前を細かくすれば並行性は上がるが、名前の過剰使用に注意する。",
 "異なる SEQUENT 名で OBTAINEX を発行したタスクどうしが互いに待機しないこと、同一名では直列化されることを再現して確認する。",
 Q("SEQUENT で直列化の対象となる単位はどれか。",
   ["同一の SEQUENT 名", "同一の RACF ユーザー", "同一の LU 名", "同一の GTF レコード"], 0,
   "同じ SEQUENT 名に対する OBTAINEX/OBTAINSH 要求どうしが直列化される。名前の粒度が並行性を決める。"),
 f"{APG} p.62 (Naming the Resource)", f"{APG} p.61-63 (SEQUENT)")

add("6696",
 "NetView Command Authorization Table External Log Record（コマンド認可テーブル外部ログレコード）は、外部ログレコード type 38・サブタイプ 1 として書かれる監査レコードである。コマンド認可テーブルの監査により生成され、DEFAULTS CATAUDIT コマンドで全体を、PERMIT/EXEMPT 文の AUDIT キーワードで個別に制御する。",
 "`DEFAULTS CATAUDIT=YES` を設定し、認可違反となるコマンドを発行して SMF に type 38 サブタイプ 1 が記録されることを確認する。",
 Q("コマンド認可テーブル監査レコードを制御するコマンドはどれか。",
   ["DEFAULTS CATAUDIT", "SETBQL", "VPDCMD", "TRACEPPI"], 0,
   "type 38 サブタイプ 1 はコマンド認可テーブル監査で生成され、DEFAULTS CATAUDIT や AUDIT キーワードで制御する。"),
 f"{APG} p.133 (NetView Command Authorization Table External Log Record)", f"{APG} p.133")

add("6697",
 "NetView Command Statistics External Log Record（コマンド統計外部ログレコード）は、外部ログレコード type 38・サブタイプ 4 として書かれる。コマンド統計機能が、監視対象 NetView コマンドについて一定間隔でレコードを生成し、CMDMON.INIT.LOGSMF（CNMSTYLE）または CMDMON コマンドで SMF 出力を指定する。レコードは共通ヘッダー・製品セクション・データ記述子セクション・コマンドデータセクションから成る。",
 "CMDMON を起動し CMDMON.INIT.LOGSMF を有効化して、一定間隔で SMF に type 38 サブタイプ 4 のコマンド統計レコードが書かれることを確認する。",
 Q("コマンド統計外部ログレコードのサブタイプはどれか。",
   ["type 38 サブタイプ 4", "type 37 サブタイプ 4", "type 39 サブタイプ 8", "type 80"], 0,
   "コマンド統計は type 38 サブタイプ 4 として一定間隔で生成され、CMDMON/CMDMON.INIT.LOGSMF で制御する。"),
 f"{APG} p.118 (NetView Command Statistics External Log Record)", f"{APG} p.134")

add("6698",
 "NetView High Performance Transport API（高性能トランスポート API）は、汎用 LU 6.2 API で、MS トランスポート API と似た外部機能を持つが、性能を高める異なる LU 6.2 プロトコルを使う。アプリケーションと VTAM の間のインターフェースとして LU 6.2 会話を確立・監視し、会話はアイドル時も持続する。通信は MDS-MU 形式で行われる。",
 "高性能アプリを CNMHREGIST で登録し、`DISPLU` で LU 6.2 会話が確立・持続することを確認する。MDS-MU を送受信し NETLOG で到達を確認する。",
 Q("高性能トランスポート API がインターフェースする相手はどれか。",
   ["アプリケーションと VTAM の間", "RACF と SAF の間", "GTF と SMF の間", "TSO と ISPF の間"], 0,
   "高性能トランスポート API はアプリと VTAM の間のインターフェースとして LU 6.2 会話を確立・監視する。"),
 f"{APG} p.95 (NetView High Performance Transport API)", f"{APG} p.55 / p.77")

add("6699",
 "NetView MS Transport API（MS トランスポート API）は、MDS-SEND/MDS-RECEIVE トランザクションプログラムを介して MDS-MU をやり取りする LU 6.2 API である。LU 6.2 会話プロトコルを用い、送信プロセスやタイムアウトメッセージなどの基準に従う。アーキテクチャ準拠の管理サービスや遠隔操作に適し、MDS-MU ごとに確認応答を行う。",
 "MS アプリを REGISTER で登録し、MDS-SEND/MDS-RECEIVE 相当のやり取りで MDS-MU を送受信して NETLOG で到達を確認する。タイムアウト時の挙動も確認する。",
 Q("MS トランスポート API が用いるトランザクションプログラムはどれか。",
   ["MDS-SEND/MDS-RECEIVE", "RUNCMD のみ", "VPDCMD のみ", "TRACEPPI のみ"], 0,
   "MS トランスポート API は MDS-SEND/MDS-RECEIVE トランザクションプログラムで MDS-MU をやり取りする。"),
 f"{APG} p.95 (NetView MS Transport API)", f"{APG} p.70")

add("6700",
 "NetView Operator（NetView オペレーター）は、コンソールから NetView を操作する利用者で、オペレーターステーションタスク（OST）を介してコマンド発行やメッセージ受信を行う。アプリケーションプログラミングの文脈では、オペレーター宛てメッセージの送信先や、コマンド認可（SAF/RACF）の対象として扱われる。",
 "NCCF にオペレーター ID でログオンし OST が起動することを確認する。アプリからオペレーター宛てメッセージを送り、当該 OST 端末に表示されることを確認する。",
 Q("NetView オペレーターが介して操作を行うタスクはどれか。",
   ["オペレーターステーションタスク（OST）", "DSITRACE タスク", "DSIGDS タスク", "REST サーバータスク"], 0,
   "オペレーターは OST（operator station task）を介してコマンド発行・メッセージ受信を行う。"),
 f"{APG} (NetView Operator)", f"{APG} p.18 (OST) / Users_Guide")

add("6701",
 "NetView REST Server APIs Used for Service Management Unite（SMU が使う NetView REST サーバー API）は、Service Management Unite（SMU）ダッシュボードが利用する RESTful API の一覧を扱う。例として、ドメイン一覧に NetView Configuration API（/ibm/netview/v1/enterprise/members、LIST STATUS=XCFGRPS）、タスク稼働率に Task API（/ibm/netview/v1/tasks/utilization、TASKUTIL）、汎用コマンドに /ibm/netview/v1/command がマップされる。",
 "NetView REST サーバーを起動し、`/ibm/netview/v1/enterprise/members` を呼び出して LIST STATUS=XCFGRPS 相当の結果が返ることを確認する。`/ibm/netview/v1/tasks/utilization` で TASKUTIL 相当の結果を確認する。",
 Q("SMU の NetView ドメイン一覧に対応する REST API/コマンドはどれか。",
   ["/ibm/netview/v1/enterprise/members（LIST STATUS=XCFGRPS）", "/ibm/netview/v1/command（VPDCMD）", "TRACEPPI", "SETBQL"], 0,
   "ドメイン一覧は /ibm/netview/v1/enterprise/members（LIST STATUS=XCFGRPS）にマップされる。"),
 f"{APG} p.99 (NetView REST Server APIs Used for Service Management Unite)", f"{APG} p.99 (Table 9)")

add("6702",
 "NetView Span Authorization Table External Log Record（スパン認可テーブル外部ログレコード）は、外部ログレコード type 38 系として書かれる監査レコードである。スパン認可（span of control）に関する認可・監査を記録し、SAF（RACF）と連携してオペレーターのスパンへのアクセスを制御する文脈で用いられる。",
 "スパン認可を設定し、認可・違反となるアクセスを発生させて、対応する監査レコードが SMF に書かれることを確認する。",
 Q("スパン認可テーブル外部ログレコードが記録する対象はどれか。",
   ["スパン（span of control）に関する認可・監査", "セッション稼働率", "アラート捕捉", "VPD 収集"], 0,
   "スパン認可テーブル外部ログレコードはスパン（span of control）認可の監査を記録する。"),
 f"{APG} p.133 (NetView Span Authorization Table External Log Record)", f"{APG} p.133 / Security_Reference")

add("6703",
 "NetView System Programmer（NetView システムプログラマー）は、NetView の導入・構成・チューニング・トレース・問題判別を担う利用者である。アプリケーションプログラミングの文脈では、PPI の有効化やサブシステムアドレス空間のリージョンサイズ確保、トレース設定など、アプリ実行基盤の整備を担当する。",
 "システムプログラマー権限で NetView を起動し、PPI 有効化やリージョンサイズ確保が適切であることを `DISPPI` 等で確認する。",
 Q("NetView システムプログラマーの役割に含まれるものはどれか。",
   ["PPI 有効化やサブシステム記憶域の確保", "オペレーターメッセージへの応答のみ", "VPD の手動入力のみ", "RACF パスワード変更のみ"], 0,
   "システムプログラマーは PPI 有効化やサブシステムアドレス空間のリージョンサイズ確保などアプリ基盤を整備する。"),
 f"{APG} (NetView System Programmer)", f"{APG} p.27 (subsystem region size)")

add("6704",
 "NetView Task Resource-Utilization-Data External Log Record（タスク資源使用データ外部ログレコード）は、NetView タスクの資源使用状況（CPU・記憶域等）を記録する外部ログレコードである。TASKUTIL コマンドや REST API（/ibm/netview/v1/tasks/utilization）でタスク稼働率を取得でき、これらのデータは外部ログにも記録される。",
 "`TASKUTIL` を発行してタスク資源使用状況を表示し、外部ログ出力を有効にしていれば SMF に該当レコードが記録されることを確認する。",
 Q("NetView タスクの資源使用状況を表示するコマンドはどれか。",
   ["TASKUTIL", "VPDCMD", "SEQUENT", "GENALERT"], 0,
   "TASKUTIL でタスクの資源使用状況（稼働率）を取得でき、外部ログにも記録できる。"),
 f"{APG} p.99 (NetView Task Resource-Utilization-Data External Log Record)", f"{APG} p.99 (Task APIs / TASKUTIL)")

add("6705",
 "Network Asset Management（ネットワーク資産管理）は、VPDCMD コマンドで返される vital product data（VPD）を解釈し、シリアル番号・機種・モデル番号などのインベントリ情報を自動収集する付録機能である。応答ノード構成データ・製品データ・リンク構成データ等の VPD を扱う。NetView はデバイスから返されたデータの正当性検証は行わない。",
 "サンプルのネットワーク資産管理コマンドリストを実行して `VPDCMD` を発行し、VPD が外部ファイルに記録されることを確認する。",
 Q("ネットワーク資産管理が収集する情報はどれか。",
   ["シリアル番号・機種・モデル番号等の VPD", "RACF パスワード", "GTF トレース", "VTAM ログモード"], 0,
   "ネットワーク資産管理は VPDCMD で返る VPD（シリアル番号・機種・モデル等）を収集する。"),
 f"{APG} p.115 (Network Asset Management)", f"{APG} p.115 / Customization_Guide p.111")

add("6706",
 "Network Asset Management Command Lists（ネットワーク資産管理コマンドリスト）は、基本的な VPD 収集を行うサンプルコマンドリスト群である。サンプルはそのまま利用するか、要件に応じて変更・自作できる。各サンプルは外部ファイルに記録する VPD レコードにレコードタイプ番号を割り当て、その値は共通グローバル変数に設定される。",
 "サンプルコマンドリスト（VPDACT、VPDPU 等）を実行し、VPD レコードがレコードタイプ番号付きで外部ファイルに記録されることを確認する。",
 Q("ネットワーク資産管理サンプルコマンドリストがレコードに割り当てるものはどれか。",
   ["レコードタイプ番号（共通グローバル変数に設定）", "RACF プロファイル名", "VTAM PU 名", "GTF バッファサイズ"], 0,
   "サンプルは VPD レコードにレコードタイプ番号を割り当て、その値を共通グローバル変数に設定する。"),
 f"{APG} p.115 (Network Asset Management Command Lists)", f"{APG} p.120")

add("6707",
 "Network Asset Management Record Formats（ネットワーク資産管理レコード形式）は、サンプルネットワーク資産管理コマンドリストが用いるレコード形式を規定する。VPDCMD から返るメッセージの解釈や、サンプルの変更・自作の際の参照に用いる。応答ノード構成データ・製品データ・リンク構成データなどの VPD 種別ごとにレコード形式が定義される。",
 "サンプルを実行して外部ファイルに記録された VPD レコードを取り出し、付録のレコード形式定義どおりにフィールドが並んでいることを確認する。",
 Q("ネットワーク資産管理レコード形式の参照用途はどれか。",
   ["VPDCMD 応答の解釈やサンプル変更時の参照", "RACF 認可の定義", "GTF トレースの解析", "VTAM 定義の生成"], 0,
   "レコード形式は VPDCMD 応答の解釈やサンプルコマンドリストの変更・自作時の参照に用いる。"),
 f"{APG} p.115 (Network Asset Management Record Formats)", f"{APG} p.115")

add("6708",
 "NMVT Format（NMVT 形式）は、ネットワーク管理ベクター転送（network management vector transport）の形式で、ジェネリックアラートを通じてハードウェアモニターへエラーを報告する。NMVT のメジャーベクター X'0000' にはアラートを含む多くの SNA メジャーベクターが含まれる。user-written プログラムは要求種別 12 で NMVT/CP-MSU 形式アラートを NetView へ送れる。",
 "要求種別 12 で NMVT 形式のジェネリックアラートを送り、ハードウェアモニターのフィルター（AREC/ESREC）を PASS にしてアラートが表示されることを確認する。",
 Q("NMVT のメジャーベクター X'0000' に含まれるものはどれか。",
   ["アラートを含む SNA メジャーベクター", "RACF プロファイル", "REST API 定義", "GTF レコード"], 0,
   "NMVT のメジャーベクター X'0000' にはアラートを含む多くの SNA メジャーベクターが含まれる。"),
 f"{APG} p.107 (NMVT Format)", f"{APG} p.17 / Customization_Guide p.97")

add("6709",
 "Operations Management Routing Considerations（操作管理ルーティングの考慮事項）は、操作管理サービス対象アプリ間でデータを送る際のルーティングと R&TI（ルーティング・ターゲティング指示）の扱いを示す。R&TI 内の発信元アプリ名は宛先アプリ名と異なる必要があり、サービス対象アプリは送信データに R&TI GDS 変数を含める。発信元アプリは操作管理でなければならない。",
 "操作管理サービス対象アプリ間で R&TI を含む MDS-MU を送り、ルーティングレポートが問題報告に使われることを NETLOG で確認する。発信元と宛先のアプリ名が異なることを確認する。",
 Q("R&TI における発信元アプリ名の制約はどれか。",
   ["宛先アプリ名と異なる必要がある", "宛先アプリ名と同一でなければならない", "RACF ユーザー名と一致させる", "常に空でなければならない"], 0,
   "R&TI 内の発信元アプリ名は宛先アプリ名と異なる必要がある。発信元は操作管理でなければならない。"),
 f"{APG} p.95 (Operations Management Routing Considerations)", f"{APG} p.75")

add("6710",
 "Operations Management Served Applications（操作管理サービス対象アプリケーション）は、操作管理を発信元として、アーキテクチャ準拠の操作管理コマンドを遠隔システムへ送受信するアプリである。これらは MS トランスポートを介し、R&TI GDS 変数を含むデータをやり取りする。COS（共通操作サービス）もこの枠組みで RUNCMD をサービスポイントへ流す。",
 "サービス対象アプリを登録し、操作管理を発信元として遠隔システムへコマンドを送り応答が返ることを NETLOG で確認する。`RUNCMD SP=...,EP_COS` で COS 経路を確認する。",
 Q("操作管理サービス対象アプリが送受信するものはどれか。",
   ["アーキテクチャ準拠の操作管理コマンド", "RACF 監査レコード", "GTF トレース", "VTAM ログモード"], 0,
   "サービス対象アプリは操作管理を発信元としてアーキテクチャ準拠の操作管理コマンドを遠隔送受信する。"),
 f"{APG} p.95 (Operations Management Served Applications)", f"{APG} p.75 / p.107")

add("6711",
 "Ordering publications（刊行物の注文）は、NetView 関連の刊行物を入手する方法を案内する節である。刊行物はオンラインで参照でき、必要に応じて注文できる。アプリケーションプログラマーは Application Programmer's Guide や SNA 関連刊行物を参照する。",
 "オンラインで NetView ライブラリを参照し、必要な刊行物が入手可能であることを確認する。NCCF で `HELP` を使い該当トピックを参照する。",
 Q("NetView 刊行物の入手方法として案内されるものはどれか。",
   ["オンライン参照・注文", "RACF 経由のみ", "GTF 経由のみ", "VTAM 定義経由のみ"], 0,
   "刊行物はオンラインで参照でき、必要に応じて注文できる。"),
 f"{APG} (Ordering publications)", f"{APG} (Accessing publications online)")

add("6712",
 "Other System Programmer（その他のシステムプログラマー）は、NetView 以外のサブシステム（VTAM・SAF/RACF・SMF 等）を担当するシステムプログラマーとの連携を指す。アプリ実行基盤の整備では、VTAM のメジャーノード定義、RACF のオペレーター認可、SMF ログ設定などで他領域の担当者と協調が必要になる。",
 "VTAM・RACF・SMF の各担当と連携し、NetView アプリ実行に必要なメジャーノード活性化・認可・ログ設定が整っていることを確認する。",
 Q("NetView アプリ基盤整備で連携が必要な他領域はどれか。",
   ["VTAM・RACF・SMF などの担当", "Web デザイナー", "DBA のみ", "ネットワーク配線業者のみ"], 0,
   "VTAM 定義・RACF 認可・SMF ログ設定など、他のシステムプログラマーとの連携が必要になる。"),
 f"{APG} (Other System Programmer)", f"{APG} p.27 / Installation_Getting_Started p.48")

add("6714",
 "Privacy policy considerations（プライバシーポリシーの考慮事項）は、製品がクッキー等を用いて情報を収集する場合のプライバシーに関する一般的な注意を示す定型節である。アプリケーションプログラミングの技術内容ではなく、製品ドキュメントに共通して含まれる法的・運用上の注意である。",
 "製品ドキュメントのプライバシーポリシーに関する記述を確認し、収集情報の取り扱い方針を把握する（技術的検証手順は伴わない）。",
 Q("プライバシーポリシーの考慮事項が扱う内容はどれか。",
   ["情報収集に関するプライバシー上の注意", "PPI 要求種別の一覧", "MDS-MU の最大長", "SEQUENT の排他制御"], 0,
   "プライバシーポリシーの考慮事項は、クッキー等による情報収集に関する一般的注意を示す定型節である。"),
 f"{APG} (Privacy policy considerations)", f"{APG} (front matter / notices)")

add("6715",
 "Processing Requests（要求の処理）は、PPI が「要求」と呼ばれる基本タスクを処理する流れを示す。各プログラムは一連の要求を含み、PPI は各要求を処理して状況を示す戻りコードを生成する。プログラムは RPB で要求を送り、PPI は同じ RPB を使ってデータを返す。",
 "サンプルで複数要求（種別 1→4→14 等）を順に発行し、各要求ごとに戻りコードが RPB に返ることを確認する。`DISPPI` で状態を照会する。",
 Q("PPI が各要求の処理結果を示すために生成するものはどれか。",
   ["戻りコード", "RACF プロファイル", "SMF type 80", "VTAM PU 定義"], 0,
   "PPI は各要求を処理して状況を示す戻りコードを生成し、同じ RPB でプログラムに返す。"),
 f"{APG} p.18 (Processing Requests)", f"{APG} p.18")

add("6716",
 "Processing the Requests（要求の処理（受信側））は、受信側プログラムがバッファキューに届いた要求／データを処理する流れを示す。受信者は要求種別 22 でデータバッファを受信し、必要に応じて要求種別 24 で受信／接続 ECB を待つ。処理後はバッファを解放する。",
 "受信側で要求種別 22 を発行してバッファを受信し、データが無ければ戻りコード 30（バッファ無し）を確認する。要求種別 24 で ECB 待ちにし、データ到着で起こされることを確認する。",
 Q("受信側がデータバッファを受信する要求種別はどれか。",
   ["要求種別 22", "要求種別 12", "要求種別 4", "要求種別 1"], 0,
   "受信側は要求種別 22 でデータバッファを受信する。要求種別 24 で受信/接続 ECB を待つ。"),
 f"{APG} p.18 (Processing the Requests)", f"{APG} p.89 (RETCODE 30)")

add("6717",
 "Product Data（製品データ、サブベクター X'10' と X'11'）は、VPDCMD で返る VPD の一種で、製品セット ID サブベクター（X'10'）と、それに続く埋め込み製品 ID サブベクター（X'11'）から成る。各埋め込み製品 ID サブベクターは製品セット ID サブベクターの直後に別構造として置かれる。SNA 準拠のため 2 つ目の製品セット ID サブベクターが含まれる場合がある。",
 "`VPDCMD` を発行し、返る製品データに製品セット ID（X'10'）と埋め込み製品 ID（X'11'）サブベクターが含まれることを確認する。",
 Q("製品データを構成するサブベクターの組はどれか。",
   ["X'10'（製品セット ID）と X'11'（製品 ID）", "X'52' と X'82'", "X'7D' と X'86'", "X'1311' と X'1549'"], 0,
   "製品データは製品セット ID サブベクター X'10' と埋め込み製品 ID サブベクター X'11' から成る。"),
 f"{APG} p.115 (Product Data Subvectors X'10' and X'11')", f"{APG} RODM_GMFHS p.179 / p.96")

add("6718",
 "Product Set Attributes（製品セット属性、サブベクター X'84'）は、VPDCMD で返る VPD の一種で、製品セットの属性情報を運ぶ SNA サブベクターである。Additional Product Set Attributes（X'86'）と並び、ネットワーク資産管理での製品情報解釈に用いられる。",
 "`VPDCMD` を発行し、製品セット属性（X'84'）サブベクターが返ることを確認する。サンプルコマンドリストで該当レコードが記録されることを確認する。",
 Q("サブベクター X'84' が表すものはどれか。",
   ["製品セット属性", "リンク構成", "応答ノード構成", "作業単位相関子"], 0,
   "X'84' は製品セット属性（Product Set Attributes）を表すサブベクターで VPD の一部である。"),
 f"{APG} p.103 (Product Set Attributes Subvector X'84')", f"{APG} p.6 (Subvector list)")

add("6719",
 "Program Placement（プログラム配置）は、アプリケーションを NetView アドレス空間内に置くか、別アドレス空間（例: NetView サブシステムアドレス空間や独立アドレス空間）に置くかの配置設計を扱う。配置は PPI の利用形態（同一空間内か空間間か）や記憶域・性能に影響する。受信者数に応じてサブシステム空間のリージョンサイズを確保する。",
 "アプリを NetView 空間内／外で起動し、それぞれ PPI で受信者定義・データ送受信が成立することを確認する。サブシステム空間のリージョンサイズが十分か確認する。",
 Q("プログラム配置が影響する主な要素はどれか。",
   ["PPI 利用形態・記憶域・性能", "RACF パスワード長", "GTF レコード長", "VTAM ログモード名"], 0,
   "配置は PPI の利用形態（同一空間/空間間）や記憶域・性能に影響する。"),
 f"{APG} (Program Placement)", f"{APG} p.27 (subsystem region size)")

add("6720",
 "Program-to-Program Interface Return Codes（PPI 戻りコード）は、PPI が各要求種別に対して生成する戻りコードとその 16 進値を一覧化した付録である。例として戻りコード 10（PPI 利用可能）、24（PPI 非活動）、28/X'1C'（サブシステム空間はあるが PPI 空間が非活動）、30/X'1E'（受信者バッファキューにデータ無し）、31/X'1F'（受信バッファが小さい）、32/X'20'（NetView 記憶域無し）がある。",
 "要求種別 1 を発行して戻りコード 10（利用可能）または 24（非活動）を確認する。データが無い受信で 30、バッファ不足で 31 が返ることを再現して確認する。",
 Q("PPI が利用可能であることを示す要求種別 1 の戻りコードはどれか。",
   ["10", "24", "30", "90"], 0,
   "戻りコード 10 は PPI が利用可能、24 は PPI 非活動、30 は受信バッファキューにデータ無しを示す。"),
 f"{APG} p.113 (Program-to-Program Interface Return Codes)", f"{APG} p.113-114 (Table 17) / p.35")

add("6721",
 "Programming Interfaces（プログラミングインターフェース）は、NetView が提供する一般利用プログラミングインターフェース（GUPI）と関連参照情報を指す。外部ログレコード形式やネットワーク資産管理のレコード形式などは GUPI として文書化され、user-written プログラムからの利用が想定される。",
 "外部ログレコードやネットワーク資産管理のレコードを user-written プログラムで解析し、文書化されたインターフェースどおりに扱えることを確認する。",
 Q("NetView の一般利用プログラミングインターフェース（GUPI）に含まれるものはどれか。",
   ["外部ログレコード形式やネットワーク資産管理レコード形式", "RACF 内部制御ブロック", "VTAM 内部バッファ", "GTF 内部テーブル"], 0,
   "外部ログレコード形式やネットワーク資産管理レコード形式は GUPI として文書化される。"),
 f"{APG} (Programming Interfaces)", f"{APG} p.127 (General-use programming interface)")

add("6722",
 "Programming Techniques（プログラミング技法）は、PPI やトランスポートを用いるプログラムを書く際の技法をまとめた章で、PPI 利用前に読むべき内容を含む。長時間実行コマンドの扱い、応答のバッファリング、資源の直列化（SEQUENT）、相関子の保存と再利用などが含まれる。",
 "サンプルで長時間実行コマンドや応答バッファリング、SEQUENT による直列化を組み合わせて実装し、想定どおり動作することを NETLOG で確認する。",
 Q("PPI を使う前に参照すべき章はどれか。",
   ["Programming Techniques", "Ordering publications", "Privacy policy considerations", "Terminology in this Library"], 0,
   "PPI を使う前に Programming Techniques 章を参照するよう案内されている。"),
 f"{APG} p.65 (Programming Techniques)", f"{APG} p.17 (see Chapter 9)")

add("6724",
 "Receive Macro（受信マクロ）は、アセンブラーで受信側処理を行うためのマクロ／要求である。受信者は要求種別 22 でデータバッファを受信し、入力バッファ長が不明なら BUFFQ-L を 0 に設定する。受信前に RPB の必須フィールドを埋める。",
 "アセンブラーで受信マクロ（要求種別 22）を発行し、データ受信に成功、または戻りコード 30（データ無し）／31（バッファ不足）を確認する。",
 Q("入力バッファ長が不明なときの BUFFQ-L 設定はどれか。",
   ["0 に設定する", "最大値に設定する", "208 に固定する", "設定不要"], 0,
   "受信時に入力バッファ長が不明なら BUFFQ-L を 0 に設定する（要求種別 22）。"),
 f"{APG} p.95 (Receive Macro)", f"{APG} p.89 (Request Type 22 example)")

add("6725",
 "Receiving a Buffer（バッファの受信）は、受信者がバッファキューからデータバッファを取り出す処理である。要求種別 22 でデータバッファを受信し、データが無ければ戻りコード 30、受信バッファが小さければ 31 が返る。受信後はバッファを解放する。",
 "受信側で要求種別 22 を発行し、データ受信成功または戻りコード 30/31 を確認する。`DISPPI` で受信者キューの状態を確認する。",
 Q("受信バッファが小さく受信できないときの戻りコードはどれか。",
   ["31（X'1F'）", "30（X'1E'）", "10", "24"], 0,
   "戻りコード 31 は受信バッファが小さい、30 はデータ無しを示す。"),
 f"{APG} p.95 (Receiving a Buffer)", f"{APG} p.113-114 (Table 17)")

add("6726",
 "Receiving a Data Buffer Synchronously（データバッファの同期受信）は、受信側が要求種別 22 でデータバッファを同期的に受け取る処理を示す。プログラムは受信ループでバッファが取れるまで繰り返し、要求種別 24 で受信／接続 ECB を待つことで効率化できる。",
 "受信側で要求種別 24 により ECB 待ちにし、データ到着で起こされた後に要求種別 22 でバッファを受信するループを確認する。",
 Q("受信／接続 ECB を待つ要求種別はどれか。",
   ["要求種別 24", "要求種別 22", "要求種別 12", "要求種別 4"], 0,
   "要求種別 24 で受信／接続 ECB を待ち、データ到着後に要求種別 22 で受信する。"),
 f"{APG} p.95 (Receiving a Data Buffer Synchronously)", f"{APG} p.89")

add("6727",
 "Receiving Alerts（アラートの受信）は、user-written プログラムやハードウェアモニターがアラートを受信する仕組みを示す。プログラム間インターフェースを介してアラートを送受信でき、フィルター（AREC/ESREC）を PASS にすればハードウェアモニターのアラートとしてオペレーターに表示される。REXX では PIPE PPI ステージでアラートをハードウェアモニターへ送れる。",
 "要求種別 12 でアラートを送り、ハードウェアモニターの AREC/ESREC フィルターを PASS にして、オペレーターにアラートが表示されることを確認する。",
 Q("送ったアラートがハードウェアモニターのアラートになる条件はどれか。",
   ["AREC/ESREC フィルターが PASS であること", "RACF READ 権限", "GTF が起動中であること", "VTAM が停止中であること"], 0,
   "アラートが適切なハードウェアモニターフィルター（AREC/ESREC）を通過すれば、オペレーターに表示される。"),
 f"{APG} p.17 (Receiving Alerts)", f"{APG} p.17 / Automation_Guide p.337 / Troubleshooting_Guide p.379")

add("6728",
 "Record Header and Section Formats（レコードヘッダーとセクション形式）は、外部ログレコード（特に type 38）の共通ヘッダーと製品情報セクションの形式を規定する。type 38 ヘッダーは S38LENG（レコード長、2 バイト、2 進）などのフィールドを持ち、共通ヘッダー・共通製品セクション・データ記述子セクション・データセクションで構成される。",
 "SMF に書かれた type 38 レコードをダンプし、先頭にレコード長 S38LENG を含む共通ヘッダーが、付録のテーブル定義どおりに並ぶことを確認する。",
 Q("type 38 ヘッダーの先頭フィールド S38LENG が表すものはどれか。",
   ["レコード長", "製品 ID", "セッション稼働率", "RACF ユーザー"], 0,
   "S38LENG（2 バイト、2 進）はレコード長を表す type 38 ヘッダーの先頭フィールドである。"),
 f"{APG} p.118 (Record Header and Section Formats)", f"{APG} p.134 (Table 39)")

add("6729",
 "Record Section Formats（レコードセクション形式）は、外部ログレコードを構成する各データセクションの形式を規定する。NetView は、ヘッダーとデータ記述子セクションに、製品 ID セクション・セッション経路データ・セッション構成データ・応答時間データ・会計可用性データ・各種カウンターデータ・ストレージデータなどを組み合わせてレコードを構築する。",
 "type 39 レコードを生成し、SMF ダンプで製品 ID・セッション経路・カウンター等のセクションが付録定義どおりに含まれることを確認する。",
 Q("外部ログレコードのセクションに含まれないものはどれか。",
   ["RACF パスワードセクション", "製品 ID セクション", "セッション経路データセクション", "ストレージデータセクション"], 0,
   "セクションは製品 ID・セッション経路・応答時間・カウンター・ストレージ等で、RACF パスワードは含まれない。"),
 f"{APG} p.133 (Record Section Formats)", f"{APG} p.151")

add("6730",
 "Record Subtypes（レコードサブタイプ）は、外部ログレコード（特に type 39）のサブタイプを規定する。例として、ストレージ・イベントカウンターレコードはサブタイプ X'0008' で、RECORD STRGDATA 発行時に書かれ、製品 ID・イベントカウンター・セッションアウェアネスカウンター・資源カウンター・ストレージの 5 セクションを持つ。",
 "`RECORD STRGDATA` を発行し、SMF に type 39 サブタイプ X'0008' のカウンターレコードが 5 セクション構成で書かれることを確認する。",
 Q("RECORD STRGDATA で書かれる type 39 のサブタイプはどれか。",
   ["X'0008'", "X'0001'", "X'0004'", "X'0027'"], 0,
   "RECORD STRGDATA はストレージ・イベントカウンターレコード（サブタイプ X'0008'）を書く。"),
 f"{APG} p.133 (Record Subtypes)", f"{APG} p.151")

add("6732",
 "Register Conventions（レジスター規約）は、アセンブラーで NetView サービスルーチンやマクロを呼び出す際のレジスターの使用規約を示す。一般に標準リンケージ規約に従い、レジスター 1 にパラメーターリストアドレス、13 に保存域、14 に戻りアドレス、15 にエントリーポイント／戻りコードを置く。NetView マクロはこの規約に沿ってレジスターを使う。",
 "アセンブラーアプリで標準リンケージ規約に従ってレジスターを設定し NetView マクロを呼び出し、戻りコード（R15）が想定どおりに返ることを確認する。",
 Q("アセンブラーで戻りコードが返される標準レジスターはどれか。",
   ["レジスター 15", "レジスター 1", "レジスター 13", "レジスター 14"], 0,
   "標準リンケージ規約ではレジスター 15 に戻りコード／エントリーポイントアドレスを置く。"),
 f"{APG} (Register Conventions)", f"{APG} Programming_Assembler (linkage)")

add("6733",
 "Registration Service（登録サービス）は、user-written アプリを MS アプリ・操作管理サービス対象アプリ・高性能アプリとして登録するサービスである。CNMREGIST（CNMRGS）や CNMHREGIST サービスルーチン、REGISTER コマンドで登録する。登録時には受信したデータを処理するコマンド名と、コマンドが実行されるタスクを指定する。",
 "REGISTER コマンドまたは CNMREGIST でアプリを登録し、`LIST` で登録状態を確認する。受信データ処理用コマンドが指定タスクで起動することを確認する。",
 Q("user-written アプリを登録するサービスルーチンはどれか。",
   ["CNMREGIST / CNMHREGIST", "CNMGETD", "SETBQL", "VPDCMD"], 0,
   "CNMREGIST（CNMRGS）や CNMHREGIST、REGISTER コマンドでアプリを登録する。"),
 f"{APG} p.95 (Registration Service)", f"{APG} Command_Reference_Vol2 p.140 / Programming_Assembler p.260")

add("6734",
 "Registration Services（登録サービス（複数）） は、登録サービスの各種オプションを扱う。登録は MS アプリ・操作管理サービス対象アプリ・高性能アプリの種別ごとに独立で、一方の登録は他方に影響しない。REPLACE=YES（既定）は同一アプリの既存登録を置き換え、コマンド名や受信タスク名を変更できる。フォーカルポイント指定（FP=YES）は MS アプリ登録でのみ有効。",
 "同一アプリを REPLACE=YES で再登録し、コマンド名／受信タスクが置き換わることを確認する。MS アプリで FP=YES を指定し、操作管理サービス対象では指定できないことを確認する。",
 Q("登録の REPLACE=YES（既定）の効果はどれか。",
   ["同一アプリの既存登録を置き換える", "登録を拒否する", "RACF を再認可する", "GTF を起動する"], 0,
   "REPLACE=YES（既定）は同一アプリの既存登録を置き換え、コマンド名や受信タスク名を変更できる。"),
 f"{APG} p.95 (Registration Services)", f"{APG} Programming_Assembler p.260-261")

add("6735",
 "Releasing the Resource（資源の解放）は、SEQUENT で獲得した資源を RELEASE キーワードで解放する操作である。排他制御（OBTAINEX）中は他のプログラムが待機するため、更新完了後は速やかに RELEASE して待機中のプログラムに制御を渡す。共有制御の場合は全共有利用者が RELEASE するまで排他要求は待たされる。",
 "OBTAINEX で資源を獲得した後 RELEASE を発行し、待機していた別タスクが処理を進めることを再現して確認する。",
 Q("SEQUENT で獲得した資源を解放するキーワードはどれか。",
   ["RELEASE", "OBTAINEX", "OBTAINSH", "REGISTER"], 0,
   "RELEASE で資源を解放する。排他中の待機者は RELEASE 後に制御を得る。"),
 f"{APG} p.62 (Releasing the Resource)", f"{APG} p.62 (SEQUENT RELEASE)")

add("6736",
 "Request Type 10: Delete a Receiver（要求種別 10: 受信者の削除）は、定義済みの受信者を削除する要求である。削除すると受信者は undefined 状態になり、その受信者宛てのデータは受け付けられなくなる。先に要求種別 9 で無効化してから削除するのが一般的である。",
 "要求種別 9 で受信者を無効化後、要求種別 10 で削除し、`DISPPI` で受信者が undefined になることを確認する。",
 Q("要求種別 10 の機能はどれか。",
   ["受信者の削除", "受信者の定義", "アラート送信", "PPI 状況照会"], 0,
   "要求種別 10 は受信者を削除する。削除後は undefined 状態になる。"),
 f"{APG} p.18 (Request Type 10: Delete a Receiver)", f"{APG} p.18 / p.113")

add("6737",
 "Request Type 12: Send an NMVT or CP-MSU Formatted Alert（要求種別 12: NMVT/CP-MSU 形式アラートの送信）は、user-written プログラムが NMVT または CP-MSU 形式のアラートを NetView へ送る要求である。バッファが PPI にコピーされると即座に制御が戻り、バッファ記憶域の解放はプログラム側の責任となる。NetView アラート受信者のバッファキュー上限は 1000 で、超過時や戻りコード 22 以上ではバッファは送られない。",
 "要求種別 12 でアラートを送り、戻りコード 0 を確認、ハードウェアモニターに表示されることを確認する。連続送信でキュー上限 1000 を超えると拒否されることを確認する。",
 Q("要求種別 12 で送る NetView アラート受信者のバッファキュー上限はどれか。",
   ["1000", "100", "31", "4294967295"], 0,
   "NetView アラート受信者のバッファキュー上限は 1000 件で、超過するとバッファは受け付けられない。"),
 f"{APG} p.41 (Request Type 12)", f"{APG} p.41 / p.19")

add("6738",
 "Request Type 14: Send a Data Buffer to a Receiver Synchronously（要求種別 14: 受信者へのデータバッファ同期送信）は、送信側が受信者のバッファキューへデータバッファを同期送信する要求である。送信側は受信者 ID を指定し、PPI が受信者キューへバッファを置く。受信側は要求種別 22 でそのバッファを取り出す。",
 "送信側で要求種別 14 を発行して受信者へバッファを送り、受信側が要求種別 22 で取り出せることを NETLOG で確認する。",
 Q("要求種別 14 の機能はどれか。",
   ["受信者へデータバッファを同期送信", "受信者を削除", "PPI 状況照会", "アラート送信"], 0,
   "要求種別 14 は受信者のバッファキューへデータバッファを同期送信する。"),
 f"{APG} p.18 (Request Type 14)", f"{APG} p.4 (Figure 3) / p.18")

add("6739",
 "Request Type 1: Query the PPI Status（要求種別 1: PPI 状況の照会）は、PPI が利用可能かを照会する任意の要求である。戻りコード 10 は PPI 利用可能、24 は PPI 非活動、28 はサブシステム空間はあるが PPI 空間が非活動、90 は処理エラーを示す。",
 "送信前に要求種別 1 を発行し、戻りコード 10（利用可能）を確認してから後続要求を行う。PPI 停止時に 24 が返ることを確認する。",
 Q("要求種別 1 の戻りコード 24 が示すものはどれか。",
   ["PPI が非活動", "PPI が利用可能", "処理エラー", "受信バッファ不足"], 0,
   "要求種別 1 では 10=利用可能、24=非活動、28=PPI 空間非活動、90=処理エラー。"),
 f"{APG} p.18 (Request Type 1: Query the PPI Status)", f"{APG} p.35")

add("6740",
 "Request Type 22: Receive a Data Buffer（要求種別 22: データバッファの受信）は、受信者がバッファキューからデータバッファを取り出す要求である。データが無ければ戻りコード 30、受信バッファが小さければ 31 が返る。入力バッファ長が不明なら BUFFQ-L を 0 に設定し、要求種別 4 と同じワークエリアを使う。",
 "受信側で要求種別 22 を発行し、データ受信成功または戻りコード 30/31 を確認する。BUFFQ-L=0 での受信を確認する。",
 Q("要求種別 22 でデータが無いときの戻りコードはどれか。",
   ["30（X'1E'）", "31（X'1F'）", "10", "24"], 0,
   "要求種別 22 では 30=データ無し、31=受信バッファ不足。"),
 f"{APG} p.18 (Request Type 22: Receive a Data Buffer)", f"{APG} p.89")

add("6741",
 "Request Type 23: Purge a Data Buffer（要求種別 23: データバッファのパージ）は、受信者のバッファキューに溜まったデータバッファを破棄する要求である。不要になったバッファを一括で除去してキューを整理し、記憶域を解放するのに用いる。",
 "受信者キューにバッファを溜めた後、要求種別 23 を発行してキューがパージされることを `DISPPI` のキュー深さで確認する。",
 Q("要求種別 23 の機能はどれか。",
   ["受信者キューのデータバッファをパージ", "受信者を定義", "アラート送信", "PPI 状況照会"], 0,
   "要求種別 23 は受信者のバッファキューに溜まったデータバッファを破棄（パージ）する。"),
 f"{APG} p.18 (Request Type 23: Purge a Data Buffer)", f"{APG} p.113-114 (Table 17)")

add("6742",
 "Request Type 24: Wait for the Receive or Connect ECB（要求種別 24: 受信／接続 ECB の待機）は、受信側がデータ到着または接続を ECB（event control block）で待つ要求である。ポーリングを避け、データ到着時に起こされてから要求種別 22 で受信することで効率化する。",
 "受信側で要求種別 24 を発行して ECB 待ちにし、送信側がデータを送ると起こされ、続けて要求種別 22 で受信できることを確認する。",
 Q("要求種別 24 が待機する対象はどれか。",
   ["受信／接続 ECB", "RACF 認可", "GTF バッファ", "VTAM セッション"], 0,
   "要求種別 24 は受信／接続 ECB を待ち、データ到着で起こされる。"),
 f"{APG} p.18 (Request Type 24: Wait for the Receive or Connect ECB)", f"{APG} p.113-114 (Table 17)")

add("6743",
 "Request Type 2: Query a Receiver's Status（要求種別 2: 受信者状況の照会）は、送信側・受信側双方で使える要求で、RPB に指定した受信者の状況（active・inactive・undefined）を判定する。送信前に宛先受信者が active かを確認するのに用いる。",
 "要求種別 2 で対象受信者を照会し、active/inactive/undefined のいずれかが返ることを確認する。未定義受信者で undefined が返ることを確認する。",
 Q("要求種別 2 が返す受信者状況に含まれないものはどれか。",
   ["pending", "active", "inactive", "undefined"], 0,
   "要求種別 2 は受信者状況として active・inactive・undefined を返す。pending は無い。"),
 f"{APG} p.18 (Request Type 2: Query a Receiver's Status)", f"{APG} p.35")

add("6744",
 "Request Type 3: Obtain the ASCB and TCB Addresses（要求種別 3: ASCB・TCB アドレスの取得）は、受信者に関連付けられたアドレス空間制御ブロック（ASCB）とタスク制御ブロック（TCB）のアドレスを取得する要求である。取得したアドレスは、後続のデータ送受信や記憶域の所有関係の管理に用いる。",
 "要求種別 3 を発行して受信者の ASCB／TCB アドレスを取得し、RPB の該当フィールドに値が返ることを確認する。",
 Q("要求種別 3 が取得するものはどれか。",
   ["ASCB と TCB のアドレス", "RACF プロファイル", "VPD サブベクター", "GTF レコード"], 0,
   "要求種別 3 は受信者に関連する ASCB と TCB のアドレスを取得する。"),
 f"{APG} p.18 (Request Type 3: Obtain the ASCB and TCB Addresses)", f"{APG} p.37 (RPB fields)")

add("6745",
 "Request Type 4: Define and Initialize a Receiver（要求種別 4: 受信者の定義と初期化）は、プログラムを受信者として定義し状態を active にする要求である。バッファキュー上限のリセットにも使う。RPB には受信者 ID（RECEIVER-ID）、ワークエリアアドレス（WORK-ADR）、ASCB アドレス、バッファキュー上限（BUFFQ-L）などを設定する。",
 "要求種別 4 で受信者を定義し、`DISPPI` で active になることを確認する。BUFFQ-L を設定してキュー上限が反映されることを確認する。",
 Q("要求種別 4 で設定するフィールドに含まれるものはどれか。",
   ["受信者 ID・バッファキュー上限", "RACF パスワード", "GTF オプション", "VTAM ログモード"], 0,
   "要求種別 4 では RECEIVER-ID・WORK-ADR・ASCB-ADR・BUFFQ-L 等を設定して受信者を定義する。"),
 f"{APG} p.37 (Request Type 4: Define and Initialize a Receiver)", f"{APG} p.37")

add("6746",
 "Request Type 9: Deactivate a Receiver（要求種別 9: 受信者の無効化）は、受信者の状態を active から inactive にする要求である。無効化された受信者は新規データを受け付けないが、定義自体は残るため要求種別 4 で再度 active にできる。完全に除去するには要求種別 10 で削除する。",
 "要求種別 9 で受信者を無効化し `DISPPI` で inactive を確認する。要求種別 4 で再度 active にできることを確認する。",
 Q("要求種別 9 で無効化した受信者を再び active にする要求種別はどれか。",
   ["要求種別 4", "要求種別 10", "要求種別 12", "要求種別 22"], 0,
   "要求種別 9 で無効化した受信者は要求種別 4 で再び active にできる（定義は残る）。"),
 f"{APG} p.18 (Request Type 9: Deactivate a Receiver)", f"{APG} p.18 / p.37")

add("6747",
 "Requesting Exclusive or Shared Control（排他制御または共有制御の要求）は、SEQUENT で資源を OBTAINEX（排他）または OBTAINSH（共有）で獲得する選択を扱う。排他制御中は獲得プログラムのみが資源を使え、他は RELEASE まで待機する。共有制御では他の共有利用者と並行アクセスできるが、排他要求が先にあると待たされる。",
 "あるタスクで OBTAINSH 後、別タスクが OBTAINEX を要求して全共有利用者の RELEASE まで待機することを再現して確認する。",
 Q("資源を変更するプログラムが要求すべき制御はどれか。",
   ["排他制御（OBTAINEX）", "共有制御（OBTAINSH）", "制御なし", "RACF UPDATE"], 0,
   "資源を変更するプログラムは排他制御（OBTAINEX）を要求すべき。共有は読み取り並行向け。"),
 f"{APG} p.62 (Requesting Exclusive or Shared Control)", f"{APG} p.62")

add("6748",
 "Restrictions（制約事項）は、PPI やトランスポート、正規表現、SEQUENT などの利用上の制約をまとめた節である。例として、MDS が必須のアプリは高性能トランスポートを使えない、WAIT は Data REXX ファイルでは使えない、SETBQL は同一先頭 4 文字の手続きにのみ使える、などの制約がある。",
 "制約に該当する操作（例: Data REXX 内 WAIT、MDS 必須アプリの高性能登録）を試み、文書どおりに拒否・制限されることを確認する。",
 Q("次のうち制約事項の例として正しいものはどれか。",
   ["MDS 必須アプリは高性能トランスポートを使えない", "全アプリが高性能トランスポートを使える", "WAIT は Data REXX で常に使える", "SETBQL は任意の手続きに使える"], 0,
   "MDS が必須のアプリは高性能トランスポートを使えないなど、各機能に制約がある。"),
 f"{APG} (Restrictions)", f"{APG} p.56 / REXX p.46")

add("6749",
 "REXX Example（REXX 例）は、DSIPHONE を使って NetView PPI 経由でデータを送受信する REXX のコーディング例を示す。例ではクライアントが OPENRECV で受信者を開き SEND で送信、CLOSE で受信者を削除する。サーバーは OPENRECV 後、RECEIVE でデータと送信者名を受け取るループを回す。",
 "REXX で `call DSIPHONE 'OPENRECV','CLIENT'` を実行し受信者を開き、`SEND`/`RECEIVE` でデータをやり取り、`CLOSE` で削除する一連を NETLOG で確認する。",
 Q("REXX 例で受信者を開くために呼ぶ DSIPHONE のキーワードはどれか。",
   ["OPENRECV", "CLOSE", "AUTHRECV", "VERSION"], 0,
   "DSIPHONE 'OPENRECV','name' で PPI 受信者を開く。CLOSE は削除。"),
 f"{APG} p.49 (REXX Example)", f"{APG} p.91 (DSIPHONE server/client)")

add("6750",
 "REXX Programming Examples（REXX プログラミング例）は、DSIPHONE を用いたサーバー・クライアントアプリの定義例を含む。サーバーは OPENRECV で受信者 SERVER を定義し、do forever でデータ到着を待って受信、クライアントは CLIENT 受信者を開いて SERVER へ送信し応答を受け取る。任意の z/OS REXX アプリが PPI 受信者を開閉・送受信できる。",
 "サーバー REXX を起動して SERVER 受信者を待機させ、クライアント REXX から SEND して、サーバーが受信・応答する往復を NETLOG で確認する。",
 Q("DSIPHONE が PPI 機能を提供する対象はどれか。",
   ["REXX が動作する任意の z/OS アプリ", "RACF サブシステムのみ", "VTAM のみ", "GTF のみ"], 0,
   "DSIPHONE は REXX を実行できる任意の z/OS アプリが PPI 受信者を開閉・送受信できるようにする。"),
 f"{APG} p.91 (REXX Programming Examples)", f"{APG} p.49 / p.91")

add("6751",
 "Routing Alerts to Multiple Receivers（複数受信者へのアラートルーティング）は、1 つのアラートを複数の PPI 受信者へ振り分ける仕組みを扱う。フィルター設定や受信者登録により、ハードウェアモニターや user-written アプリなど複数の宛先へアラートを配送できる。",
 "複数の受信者を登録し、要求種別 12 でアラートを送って各受信者およびハードウェアモニターに配送されることを NETLOG で確認する。",
 Q("複数受信者へのアラート配送を制御する要素はどれか。",
   ["フィルター設定と受信者登録", "RACF パスワード長", "GTF バッファサイズ", "VTAM ログモード"], 0,
   "フィルター設定と受信者登録により、1 アラートを複数受信者へルーティングできる。"),
 f"{APG} p.17 (Routing Alerts to Multiple Receivers)", f"{APG} p.17 / Troubleshooting_Guide p.379")

add("6753",
 "Send Macro（送信マクロ）は、アセンブラーで送信側処理を行うマクロ／要求である。送信側は要求種別 14 で受信者へデータバッファを同期送信、または要求種別 12 でアラートを送る。送信前に RPB の必須フィールド（受信者 ID 等）を埋める。",
 "アセンブラーで送信マクロ（要求種別 14）を発行して受信者へバッファを送り、受信側が要求種別 22 で取り出せることを確認する。",
 Q("送信マクロでデータバッファを受信者へ同期送信する要求種別はどれか。",
   ["要求種別 14", "要求種別 22", "要求種別 24", "要求種別 9"], 0,
   "送信側は要求種別 14 で受信者へデータバッファを同期送信する。"),
 f"{APG} p.95 (Send Macro)", f"{APG} p.18 / p.4")

add("6754",
 "Send Service（送信サービス）は、高性能トランスポートでアプリが MDS-MU を送るための CNMHSMU（CNMHsmu）サービスである。アプリはこのサービスで MDS-MU を送信し、登録時に指定したコマンド／タスクで応答を受け取る。会話はアイドル時も持続する。",
 "高性能アプリを登録後、CNMHSMU で MDS-MU を送信し、宛先で受信されることを NETLOG で確認する。",
 Q("高性能トランスポートで MDS-MU を送る送信サービスはどれか。",
   ["CNMHSMU", "CNMGETD", "VPDCMD", "SETBQL"], 0,
   "高性能トランスポートでは CNMHSMU（送信サービス）で MDS-MU を送信する。"),
 f"{APG} p.78 (Send Service)", f"{APG} p.78")

add("6755",
 "Send-Receive Interface（送受信インターフェース）は、アプリがトランスポート API を通じてデータを送受信する一連のインターフェースを示す。MS／高性能トランスポートで MDS-MU を送り（送信サービス）、登録したコマンド／タスクで受信する。要求と応答は相関子で対応付けられる。",
 "送受信アプリを登録し、片方が MDS-MU を送り、相手が登録コマンド／タスクで受信して相関子付き応答を返す往復を NETLOG で確認する。",
 Q("送受信インターフェースで要求と応答を対応付けるものはどれか。",
   ["エージェント作業単位相関子", "RACF ユーザー ID", "GTF レコード番号", "VTAM PU 名"], 0,
   "要求と応答はエージェント作業単位相関子（X'1549'）で対応付けられる。"),
 f"{APG} p.95 (Send-Receive Interface)", f"{APG} p.58 / p.78")

add("6756",
 "Sending a Buffer Synchronously（バッファの同期送信）は、送信側が要求種別 14 で受信者のバッファキューへデータバッファを同期送信する処理を示す。送信前に要求種別 1 で PPI 状況、要求種別 2 で受信者状況を確認するのが望ましい。",
 "要求種別 1→2→14 の順で発行し、PPI 利用可能・受信者 active を確認したうえでバッファを同期送信し、受信側が取り出せることを確認する。",
 Q("バッファ同期送信の前に受信者状況を確認する要求種別はどれか。",
   ["要求種別 2", "要求種別 12", "要求種別 22", "要求種別 24"], 0,
   "要求種別 2 で受信者状況を確認してから要求種別 14 で同期送信する。"),
 f"{APG} p.18 (Sending a Buffer Synchronously)", f"{APG} p.4 / p.18")

add("6757",
 "Sending a Data Buffer Synchronously（データバッファの同期送信）は、送信側プログラムが受信者キューへデータバッファを同期送信する流れを示す。例ではプログラム B が要求種別 1（任意の PPI 状況照会）に続いて要求種別 14 でプログラム Z の受信者キューへ送信する。",
 "プログラム B 役で要求種別 1 を発行し PPI 利用可能を確認後、要求種別 14 でプログラム Z の受信者へ送信し、Z が要求種別 22 で受信することを NETLOG で確認する。",
 Q("データ同期送信の例で任意とされる要求はどれか。",
   ["要求種別 1（PPI 状況照会）", "要求種別 14", "要求種別 22", "要求種別 4"], 0,
   "例では要求種別 1（PPI 状況照会）は任意で、要求種別 14 で同期送信する。"),
 f"{APG} p.4 (Sending a Data Buffer Synchronously)", f"{APG} p.19 (Figure 3)")

add("6758",
 "Sending an NMVT or CP-MSU Formatted Alert（NMVT/CP-MSU 形式アラートの送信）は、要求種別 12 で user-written プログラムが NMVT または CP-MSU 形式のアラートを NetView へ送る処理を示す。配布テープにサンプル（アセンブラー CNMS4287、C CNMS4257、PL/I CNMS4227）がある。NetView はアラートを未送信記録として扱い、フィルターを通過すればハードウェアモニターアラートになる。",
 "サンプル（例: CNMS4287）を実行して要求種別 12 でアラートを送り、フィルター PASS でオペレーターに表示されることを確認する。",
 Q("NMVT/CP-MSU 形式アラートを送る要求種別はどれか。",
   ["要求種別 12", "要求種別 14", "要求種別 4", "要求種別 22"], 0,
   "要求種別 12 で NMVT または CP-MSU 形式のアラートを NetView へ送る。"),
 f"{APG} p.19 (Sending an NMVT or CP-MSU Formatted Alert)", f"{APG} p.19 / p.41")

add("6759",
 "Sending Commands and Messages to the NetView Program（NetView へのコマンド・メッセージ送信）は、外部アプリや REXX から NetView へコマンドやメッセージを送る方法を示す。DSIPHONE（REXX）や PPI を介して NetView の受信者へデータを送り、NetView 側でコマンドとして処理させたり、メッセージとして自動化テーブルにかけたりできる。",
 "REXX の DSIPHONE で NetView 受信者へコマンド文字列を送り、NetView 側で当該コマンドが実行されることを NETLOG で確認する。",
 Q("外部 REXX アプリから NetView へデータを送る手段はどれか。",
   ["DSIPHONE（PPI）", "RACF ADDUSER", "GTF TRACE", "VTAM VARY"], 0,
   "DSIPHONE を用いて REXX アプリから PPI 経由で NetView へコマンド・メッセージを送れる。"),
 f"{APG} p.49 (Sending Commands and Messages to the NetView Program)", f"{APG} p.49 / p.91")

add("6760",
 "Sense Data（センスデータ、サブベクター X'7D'）は、VPDCMD で返る VPD の一種で、エラーの詳細を示すセンスデータを運ぶ SNA サブベクターである。ネットワーク資産管理や問題判別の文脈で、デバイスから返るセンス情報の解釈に用いる。",
 "`VPDCMD` を発行し、エラー時にセンスデータ（X'7D'）サブベクターが返ることを NETLOG で確認する。",
 Q("サブベクター X'7D' が運ぶものはどれか。",
   ["センスデータ", "製品セット ID", "リンク構成", "作業単位相関子"], 0,
   "X'7D' はセンスデータ（Sense Data）を運ぶサブベクターで、エラー詳細を示す。"),
 f"{APG} p.103 (Sense Data Subvector X'7D')", f"{APG} p.6 (Subvector list)")

add("6761",
 "Session Outage Notification（セッション停止通知、SON）は、LU 6.2 セッションの停止をアプリへ通知する仕組みである。登録時に ALL（異常と判定できなくても通知）・ERROR（異常と判定できる場合のみ通知）・NONE（通知しない、既定）を選べる。通知はノードへの最後の LU 6.2 セッションが失われたときのみ提供され、非 LU 6.2 のセッション停止では駆動されない。",
 "アプリを SON=ERROR で登録し、対象ノードへの最後の LU 6.2 セッションを異常停止させて通知が来ることを NETLOG で確認する。SON=NONE では通知が来ないことを確認する。",
 Q("セッション停止通知の既定値はどれか。",
   ["NONE", "ALL", "ERROR", "WARN"], 0,
   "SON の既定は NONE（通知しない）。ALL は常時、ERROR は異常と判定できる場合のみ通知。"),
 f"{APG} p.67 (Session Outage Notification)", f"{APG} p.67 / p.74 / p.78")

add("6762",
 "Syntax of a Regular Expression（正規表現の構文）は、NetView がサポートする正規表現の構文規則を示す。区切り文字・エスケープ（バックスラッシュ）・グループ化（括弧）・量指定子などの規則があり、区切り文字を式中に含める場合はエスケープするか別の区切り文字を選ぶ。構文エラー時は BNH923I（不一致記号）や BNH925I（無効な量指定子）などのメッセージが出る。",
 "`PIPE ... | LOCATE /pattern/` で正規表現を試し、不一致の括弧を含む式で BNH923I が出ることを確認する。正しい式で意図どおり照合されることを確認する。",
 Q("正規表現で区切り文字を式中に含めたいときの対処はどれか。",
   ["バックスラッシュでエスケープするか別の区切り文字を選ぶ", "RACF で認可する", "GTF を起動する", "BUFFQ-L を 0 にする"], 0,
   "区切り文字を式中に含める場合はバックスラッシュでエスケープするか、別の区切り文字を選ぶ。"),
 f"{APG} p.81 (Syntax of a Regular Expression)", f"{APG} p.84 / Messages_Vol1 p.349")

add("6763",
 "Tasking Structure（タスク構造）は、NetView のタスク（OST・PPT・DST・autotask 等）の構造と、アプリ／コマンドがどのタスクで実行されるかを示す。登録時に受信データを処理するコマンドが実行されるタスクを指定でき、長時間実行コマンドは DSIPUSH で待機しつつ他タスクの処理を妨げない。",
 "アプリ登録時に受信データ処理用タスクを指定し、`LIST STATUS=TASKS` で該当タスクが ACTIVE であること、受信時にそのタスクでコマンドが起動することを確認する。",
 Q("登録時に指定できるタスク関連項目はどれか。",
   ["受信データを処理するコマンドが実行されるタスク", "RACF グループ", "GTF データセット", "VTAM ログモード"], 0,
   "登録時に、受信データを処理するコマンドが実行されるタスクを指定できる。"),
 f"{APG} (Tasking Structure)", f"{APG} Command_Reference_Vol2 p.140 / REXX p.25")

add("6764",
 "Terminology in this Library（本ライブラリの用語）は、NetView 刊行物で用いる用語の定義をまとめた定型節である。MDS-MU・PPI・OST・GDS 変数・サブベクターなどの用語の意味を確認できる。アプリプログラマーはこれらの用語を理解したうえで実装を進める。",
 "刊行物の用語節を参照し、MDS-MU・PPI・GDS 変数などの定義を把握する（技術的検証手順は伴わない）。",
 Q("本ライブラリの用語節の目的はどれか。",
   ["刊行物で用いる用語の定義の提供", "PPI 要求種別の実行", "VPD の収集", "アラートの送信"], 0,
   "用語節は刊行物で用いる用語の定義を提供する定型節である。"),
 f"{APG} (Terminology in this Library)", f"{APG} (front matter)")

add("6765",
 "Understanding the NetView Program-to-Program Interface（PPI の理解）は、PPI の概念を導入する章である。PPI は要求と呼ばれる基本タスクを実行し、各要求に戻りコードを生成する。プログラムは RPB で要求を送り、PPI は同じ RPB でデータを返す。例として、アラート送信やプログラム間のデータバッファ授受がある。",
 "サンプルでアラート送信（要求種別 12）とプログラム間データ授受（要求種別 14/22）を実行し、PPI の基本動作を NETLOG で確認する。",
 Q("PPI の基本タスクの呼称はどれか。",
   ["要求（request）", "セッション", "トランザクション ID", "プロファイル"], 0,
   "PPI は「要求（request）」と呼ばれる基本タスクを実行し、各要求に戻りコードを生成する。"),
 f"{APG} p.1 (Understanding the NetView Program-to-Program Interface)", f"{APG} p.1 / p.18")

add("6766",
 "Usage Scenario（利用シナリオ）は、PPI やトランスポートを用いる代表的な利用シナリオを示す。例として、user-written アプリがアラートを NetView へ送りハードウェアモニターで表示する、アプリ間で MDS-MU をやり取りする、REXX サーバー／クライアントで PPI 通信する、などがある。",
 "代表シナリオ（アラート送信、アプリ間 MDS-MU、REXX サーバー/クライアント）を順に実行し、各シナリオが成立することを NETLOG で確認する。",
 Q("PPI の利用シナリオに含まれるものはどれか。",
   ["アプリからのアラート送信", "RACF パスワード変更", "VTAM 定義生成", "GTF 起動のみ"], 0,
   "利用シナリオには、アプリからのアラート送信やアプリ間 MDS-MU 授受などが含まれる。"),
 f"{APG} (Usage Scenario)", f"{APG} p.17 / p.91")

add("6767",
 "Using COS Command Lists（COS コマンドリストの利用）は、共通操作サービス（COS）でサービスポイント宛てにコマンドを流すコマンドリストの利用を扱う。DSIGDS タスクが MS トランスポートに COS_NETOP として登録し、RUNCMD でコマンドを送る。サービスポイントが分散 NetView 上にある場合は LU 6.2 セッション経由でルーティングされる。",
 "COS コマンドリストから `RUNCMD SP=spname,EP_COS,...` を発行し、サービスポイントへコマンドが流れ応答が返ることを NETLOG で確認する。",
 Q("COS コマンドを流すために登録される DSIGDS の MS アプリ名はどれか。",
   ["COS_NETOP", "OPERATIONS_MGMT_NETOP", "EP_OPERATIONS_MGMT", "MS_CAPS"], 0,
   "DSIGDS タスクは MS トランスポートに SPCS（COS_NETOP）として登録し COS コマンドを流す。"),
 f"{APG} p.91 (Using COS Command Lists)", f"{APG} p.91 / RODM_GMFHS p.98")

add("6768",
 "Using High-Level Languages and Assembler to Send Requests（HLL・アセンブラーで要求を送る）は、PL/I・C・アセンブラーから PPI へ要求を送る方法を扱う章である。MVS でインターフェースを有効化し、NetView サブシステムアドレス空間を初期化したうえで、RPB を構築して各要求種別を発行する。",
 "HLL／アセンブラーサンプルで MVS のインターフェース有効化を確認し、RPB を構築して要求種別 4・14 を発行、送受信が成立することを確認する。",
 Q("HLL・アセンブラーで要求を送る前提として正しいものはどれか。",
   ["MVS でインターフェースを有効化しサブシステム空間を初期化", "RACF を停止", "GTF を停止", "VTAM を停止"], 0,
   "要求送信前に MVS でインターフェースを有効化し、NetView サブシステムアドレス空間を初期化する。"),
 f"{APG} p.27 (Using High-Level Languages and Assembler to Send Requests)", f"{APG} p.27")

add("6769",
 "Using IBM Z NetView online help（IBM Z NetView オンラインヘルプの利用）は、HELP コマンドでオンラインヘルプを参照する方法を示す。`HELP` でメニュー、`HELP ABEND` のように引数を付けて特定トピックを表示できる。問題判別時に異常終了コードや手順を素早く参照できる。",
 "NCCF で `HELP` を入力してメニューを表示し、`HELP ABEND` で異常終了に関するヘルプが表示されることを確認する。",
 Q("特定トピックのオンラインヘルプを表示する方法はどれか。",
   ["HELP に引数を付ける（例: HELP ABEND）", "VPDCMD を発行", "SETBQL を発行", "GTF を起動"], 0,
   "HELP に引数を付けて（例: HELP ABEND）特定トピックのオンラインヘルプを表示できる。"),
 f"{APG} (Using IBM Z NetView online help)", f"{APG} (Online help facility) / Troubleshooting_Guide p.64")

add("6770",
 "Using Regular Expressions for Advanced Data Processing（高度なデータ処理での正規表現利用）は、PIPE の LOCATE/NLOCATE、REXX の MATCH、自動化テーブル関数 DSIAMMCH で正規表現を使い、文字列を柔軟に照合・抽出する方法を示す。正規表現は部分文字列より強力で、多様なパターンを記述できる。",
 "`PIPE NETVIEW LOG | LOCATE /[A-Z]{3}[0-9]{3}/ | CONSOLE` のように正規表現で行を抽出し、意図どおりに照合されることを確認する。",
 Q("高度なデータ処理で正規表現が使えない箇所はどれか。",
   ["RACF プロファイル定義", "PIPE の LOCATE/NLOCATE", "REXX の MATCH", "自動化テーブル DSIAMMCH"], 0,
   "正規表現は PIPE の LOCATE/NLOCATE、REXX の MATCH、DSIAMMCH で利用できる。RACF 定義では使わない。"),
 f"{APG} p.81 (Using Regular Expressions for Advanced Data Processing)", f"{APG} p.81")

add("6771",
 "Using REXX to Send Requests（REXX で要求を送る）は、REXX 外部サブルーチン DSIPHONE を使って NetView PPI 経由でデータを送受信する方法を扱う章である。DSIPHONE は PIPE TSO ステージで TSO へコマンドを発行した際に NetView へデータを戻すのにも使う。任意の z/OS REXX アプリが PPI 受信者を開閉・送受信できる。",
 "REXX で `call DSIPHONE 'OPENRECV','name'` → `SEND`/`RECEIVE` → `CLOSE` を実行し、PPI 経由のデータ送受信が成立することを NETLOG で確認する。",
 Q("REXX で PPI を介して送受信する外部サブルーチンはどれか。",
   ["DSIPHONE", "DSIPUSH", "CNMGETD", "VPDCMD"], 0,
   "DSIPHONE は REXX 外部サブルーチンで、NetView PPI 経由のデータ送受信を行う。"),
 f"{APG} p.49 (Using REXX to Send Requests)", f"{APG} p.49 / p.52")

add("6772",
 "Using the NetView LU 6.2 Transport APIs（NetView LU 6.2 トランスポート API の利用）は、MS トランスポート API と高性能トランスポート API を使ってアプリ間で MDS-MU をやり取りする方法を扱う。アプリは用途に応じて API を選び、登録（REGISTER/CNMREGIST 等）してから送受信する。両 API は LU 6.2 会話上で通信する。",
 "MS／高性能の各 API でアプリを登録し、MDS-MU を送受信して LU 6.2 会話上で通信が成立することを `DISPLU`・NETLOG で確認する。",
 Q("NetView の LU 6.2 トランスポート API はどれか。",
   ["MS トランスポート API と高性能トランスポート API", "REST API と SNMP API", "RACF API と SAF API", "GTF API と SMF API"], 0,
   "NetView の LU 6.2 トランスポート API は MS トランスポート API と高性能トランスポート API。"),
 f"{APG} p.55 (Using the NetView LU 6.2 Transport APIs)", f"{APG} p.55")

add("6773",
 "Using the NetView REST Server（NetView REST サーバーの利用）は、RESTful API を介して NetView 機能を呼び出す方法を扱う。Service Management Unite（SMU）などのクライアントが /ibm/netview/v1/ 配下の API（command・tasks/utilization・enterprise/members 等）を使う。REST サーバーは Apache Tomcat 上で稼働し、事前準備が必要である。",
 "NetView REST サーバーを起動し、`/ibm/netview/v1/command` に汎用コマンドを投げて結果が返ることを確認する。`/ibm/netview/v1/tasks/utilization` で稼働率を確認する。",
 Q("NetView REST サーバーが稼働する基盤はどれか。",
   ["Apache Tomcat", "VTAM", "GTF", "RACF サブシステム"], 0,
   "NetView REST サーバーは Apache Tomcat 上で稼働し、SMU 等が RESTful API を利用する。"),
 f"{APG} p.99 (Using the NetView REST Server)", f"{APG} p.99 / Installation_Configuring_Additional_Components p.241")

add("6774",
 "Using the RPB（RPB の利用）は、要求パラメーターブロック（96 バイト）を使って PPI に要求を送り、結果を受け取る方法を示す。各要求種別ごとに設定・返却フィールドが決まり、TYPE に要求種別、RECEIVER-ID に受信者、BUFFQ-L にキュー上限などを設定する。PPI は同じ RPB を使ってデータ・戻りコードを返す。",
 "サンプルで RPB を初期化し TYPE と必須フィールドを設定して要求を発行、PPI が同じ RPB に戻りコードを返すことを確認する。",
 Q("RPB の TYPE フィールドに設定するものはどれか。",
   ["要求種別", "RACF ユーザー", "GTF オプション", "VTAM ログモード"], 0,
   "RPB の TYPE フィールドに要求種別を設定し、PPI は同じ RPB で結果を返す。"),
 f"{APG} p.29 (Using the RPB)", f"{APG} p.34 (Table 2)")

add("6775",
 "Using the Sample Command Lists（サンプルコマンドリストの利用）は、ネットワーク資産管理のサンプルコマンドリストをそのまま使って基本的な VPD 収集を行う方法を示す。サンプルは外部ファイルに記録する VPD レコードにレコードタイプ番号を割り当て、その値を共通グローバル変数に設定する。要件に合わなければ変更・自作できる。",
 "サンプルコマンドリストを実行して `VPDCMD` を発行し、VPD レコードがレコードタイプ番号付きで外部ファイルに記録されることを確認する。",
 Q("サンプルコマンドリストがそのまま行えるものはどれか。",
   ["基本的な VPD 収集", "RACF 認可設定", "VTAM 定義生成", "GTF 解析"], 0,
   "サンプルコマンドリストはそのまま基本的な VPD（vital product data）収集を行える。"),
 f"{APG} p.115 (Using the Sample Command Lists)", f"{APG} p.120")

add("6776",
 "Using the SEQUENT Command to Serialize Access to Resources（SEQUENT による資源アクセスの直列化）は、直列再利用資源（グローバル変数・グローバル KEEP・データセット等）を複数プログラムが同時に変更しないよう SEQUENT で直列化する方法を扱う。OBTAINEX（排他）または OBTAINSH（共有）で獲得し、RELEASE で解放する。排他中は同名への OBTAINEX/OBTAINSH 要求が待機する。",
 "2 タスクで同一 SEQUENT 名に OBTAINEX を発行し、後者が前者の RELEASE まで待機することを再現する。OBTAINSH では共有並行が成立することを確認する。",
 Q("SEQUENT で共有制御を獲得するキーワードはどれか。",
   ["OBTAINSH", "OBTAINEX", "RELEASE", "REGISTER"], 0,
   "OBTAINSH は共有制御、OBTAINEX は排他制御を獲得し、RELEASE で解放する。"),
 f"{APG} p.61 (Using the SEQUENT Command to Serialize Access to Resources)", f"{APG} p.61-63")

add("6777",
 "Using the Trace Facility（トレース機能の利用）は、コマンド機能トレースや PPI トレースを使って問題判別データ（パラメーター値・アドレス・戻りコード・フラグ等）を収集する方法を示す。トレースは内部（仮想記憶）・外部（DSITRACE データセット）・GTF に記録でき、内部トレースは常時有効が推奨される。",
 "`START TASK=DSITRACE` でトレースを起動し、`TRACE OPTION=(DISP,PSS,QUE,STOR,UEXIT)` を設定して問題判別データが記録されることを確認する。",
 Q("トレース機能で収集できる問題判別データに含まれるものはどれか。",
   ["パラメーター値・アドレス・戻りコード・フラグ", "RACF パスワード", "VPD シリアル番号", "REST トークン"], 0,
   "トレースはパラメーター値・アドレス・戻りコード・フラグ設定などの問題判別データを収集する。"),
 f"{APG} p.101 (Using the Trace Facility)", f"{APG} p.101 / Troubleshooting_Guide p.118")

add("6778",
 "Vital Product Data Descriptions（VPD の説明）は、VPDCMD コマンドで返る VPD の種別を説明する。応答ノード構成データ・製品データ・DCE データ（V5R4 以降非推奨）・リンク構成データ・センスデータなどがあり、ネットワーク資産管理で機種・モデル・シリアル番号等の収集に用いる。NetView はデバイスから返るデータの正当性検証は行わない。",
 "`VPDCMD` を発行し、応答ノード構成・製品・リンク構成・センスなどの VPD が返ることを NETLOG で確認する。",
 Q("VPDCMD が返す VPD 種別に含まれないものはどれか。",
   ["RACF 監査レコード", "応答ノード構成データ", "製品データ", "リンク構成データ"], 0,
   "VPD には応答ノード構成・製品・DCE・リンク構成・センスデータ等がある。RACF 監査は含まれない。"),
 f"{APG} p.115 (Vital Product Data Descriptions)", f"{APG} p.115")

add("6779",
 "When to Use the NetView High Performance Transport API（高性能トランスポート API を使う場面）は、性能重視のアプリや、RU サイズなどセッションパラメーターを定義したい場合に高性能トランスポートを選ぶ指針を示す。高性能トランスポートは確認応答を省き会話を持続させるため高速だが、エラー通知は一般的なものになる。",
 "性能重視のアプリを高性能トランスポートで実装し、トラフィックや応答性が MS トランスポートより良いことを性能指標で確認する。",
 Q("高性能トランスポートが適する場面はどれか。",
   ["性能重視・RU サイズ等のセッションパラメーター指定が必要な場合", "アーキテクチャ上 MDS が必須の場合", "確認応答が必須の場合", "RACF 監査が主目的の場合"], 0,
   "高性能トランスポートは性能重視やセッションパラメーター定義が必要な場合に適する。"),
 f"{APG} p.40 (When to Use the NetView High Performance Transport API)", f"{APG} p.40 / p.55")

add("6780",
 "When to Use the NetView MS Transport API（MS トランスポート API を使う場面）は、遠隔操作やアーキテクチャ準拠の管理サービス、異なる S/390 システム間のデータベース内容コピーなど、MDS が必要な場合に MS トランスポートを選ぶ指針を示す。MS トランスポートは MDS-MU ごとに確認応答を行い、データ固有のエラー通知を提供する。",
 "遠隔操作や管理サービスのアプリを MS トランスポートで実装し、MDS-MU ごとの確認応答とデータ固有のエラー通知が得られることを NETLOG で確認する。",
 Q("MS トランスポートが適する場面はどれか。",
   ["遠隔操作・アーキテクチャ準拠の管理サービス", "性能最優先で確認応答不要の場合", "VPD 収集のみ", "GTF トレースのみ"], 0,
   "MS トランスポートは遠隔操作やアーキテクチャ準拠の管理サービスなど MDS が必要な場面に適する。"),
 f"{APG} p.40 (When to Use the NetView MS Transport API)", f"{APG} p.56")

add("6781",
 "Word Boundaries（単語境界）は、正規表現で単語の先頭・末尾の境界を指定する要素である。単語境界を用いると、文字列中の単語単位での照合が可能になり、部分一致を避けて正確なパターンマッチングができる。NetView の正規表現（PIPE LOCATE 等）で利用できる。",
 "`PIPE ... | LOCATE /pattern/` で単語境界を含む正規表現を試し、単語単位で正しく照合され部分一致が排除されることを確認する。",
 Q("単語境界を使う目的はどれか。",
   ["単語単位での正確な照合（部分一致の回避）", "RACF 認可", "GTF 起動", "VPD 収集"], 0,
   "単語境界は単語単位での正確な照合を可能にし、不要な部分一致を避ける。"),
 f"{APG} p.81 (Word Boundaries)", f"{APG} p.81-84 (regular expression)")

add("6782",
 "Writing Command Lists（コマンドリストの作成）は、REXX または NetView コマンドリスト言語でコマンドリストを作成する方法を扱う。コマンドリストでは &WAIT による待機、長時間実行コマンド（DSIPUSH で待機）、PPI 通信（DSIPHONE）、正規表現照合などを組み合わせて自動化処理を記述する。メッセージキューの肥大化を避ける配慮が必要である。",
 "REXX コマンドリストを作成し、&WAIT やコマンド発行を含む処理が NCCF で正しく動作することを NETLOG で確認する。",
 Q("コマンドリストでメッセージキュー肥大化を避ける手段はどれか。",
   ["TRAP NO MESSAGES や FLUSHQ の利用", "BUFFQ-L を無制限化", "GTF を停止", "RACF を無効化"], 0,
   "TRAP NO MESSAGES や FLUSHQ を使い、メッセージキューの肥大化を防ぐ。"),
 f"{APG} (Writing Command Lists)", f"{APG} REXX p.46 / p.25")

add("6783",
 "Writing Effective Programs（効果的なプログラムの作成）は、PPI やトランスポートを用いるプログラムを効率的・安全に書くための指針を示す。記憶域の所有関係（MAINTSK・Q オプション）に注意し、不正確なストレージ会計を避ける、長時間実行コマンドで他処理を妨げない、資源を SEQUENT で適切に直列化する、などが含まれる。",
 "サンプルで記憶域取得時の MAINTSK/Q 指定を適切に行い、ストレージ会計が正しく行われることを確認する。長時間実行コマンドが他タスクを妨げないことを確認する。",
 Q("効果的なプログラム作成で注意すべき点はどれか。",
   ["記憶域の所有関係（MAINTSK/Q）とストレージ会計", "RACF パスワード長", "REST トークン長", "VTAM ログモード名"], 0,
   "記憶域の所有関係（MAINTSK/Q）に注意し、不正確なストレージ会計を避けることが重要である。"),
 f"{APG} (Writing Effective Programs)", f"{APG} Programming_Assembler p.184 / p.212")

add("6784",
 "Writing to External Storage with GTF（GTF による外部ストレージへの書き出し）は、PPI トレース情報を一般化トレース機能（GTF）へ書き出す方法を示す。GTF オプションを使うには GTF を導入・活性化・有効化し、TRACEPPI コマンドで GTF を指定する。GTF 指定時は内部 PPI トレーステーブルは作成されず、トレースレコードは外部データセット（IEFRDER DD、既定 SYS1.TRACE）に書かれる。GTF の場合バッファ上限は 208 バイト。",
 "GTF を起動し `TRACEPPI ON GTF` を発行して、PPI トレースが外部データセットに書かれることを確認する。IPCS で GTF 出力を参照する。",
 Q("TRACEPPI で GTF を指定したときの挙動はどれか。",
   ["内部トレーステーブルを作らず外部データセットへ書き出す", "内部テーブルのみ作成", "RACF へ通報", "VTAM を再起動"], 0,
   "GTF 指定時は内部 PPI トレーステーブルを作らず、トレースを外部データセットへ書き出す（バッファ上限 208 バイト）。"),
 f"{APG} p.101 (Writing to External Storage with GTF)", f"{APG} p.101 / Command_Reference_Vol2 p.456 / Troubleshooting_Guide p.171")

add("6785",
 "Writing to Internal Storage（内部ストレージへの書き出し）は、PPI トレース情報を共通記憶域（CSA）内の内部トレーステーブルへ書き出す方法を示す。TRACEPPI で SIZE を指定して内部テーブルを確保する（GTF キーワードとは併用不可）。サブシステムインターフェースが内部トレース有効中に停止すると、内部 PPI トレース情報がダンプされる。",
 "`TRACEPPI ON SIZE=n` を発行して内部トレーステーブルを確保し、トレースが CSA 内に記録されることを確認する。サブシステム停止時に内部トレースがダンプされることを確認する。",
 Q("PPI 内部トレーステーブルのサイズを指定するキーワードはどれか。",
   ["SIZE", "GTF", "BUFSIZE", "MODE"], 0,
   "TRACEPPI の SIZE で内部トレーステーブルサイズを指定する。GTF キーワードとは併用できない。"),
 f"{APG} p.101 (Writing to Internal Storage)", f"{APG} p.101 / Command_Reference_Vol2 p.456")

# Build output
out_rows = []
for r in rows:
    rid = r['row_id']; title = r['title']
    c = C.get(rid)
    if c is None:
        # Should not happen; flag uncovered
        continue
    out_rows.append({
        "row_id": rid,
        "title": title,
        "naiyou_jp": c['naiyou_jp'],
        "verify_steps": c['verify'],
        "quiz": c['quiz'],
        "source": c['source'],
        "rag_hit": c['rag_hit'],
    })

result = {
    "page": "g033",
    "product": "IBM NetView 6.4",
    "total_rows": len(rows),
    "target_rows": len(rows),
    "fixed_count": len(out_rows),
    "rows": out_rows,
}
json.dump(result, open('_phase2_outputs/g033_fixed.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print("total", len(rows), "fixed", len(out_rows))
missing = [r['row_id'] for r in rows if r['row_id'] not in C]
print("uncovered:", missing)
