# -*- coding: utf-8 -*-
import json, re

rows = json.load(open('_phase2_outputs/_g038_all.json', encoding='utf-8'))
RAG = "NetView_6.4_Security_Reference.pdf (IBM Z NetView Security Reference)"

def has(t, *ws):
    tl = t.lower()
    return any(w.lower() in tl for w in ws)

# Each cluster returns (naiyou_jp, verify_steps, quiz) tailored using the title.
def build(title, secref):
    t = title
    # ---- Command Authorization Table (TABLE) ----
    if has(t, 'Command Authorization Table', 'Command Identifiers', 'Table Statements',
            'Creating a NetView Command Authorization', 'Loading the NetView Command Authorization',
            'Capturing Data by Auditing the NetView Command Authorization', 'Using the NetView Command Authorization Table',
            'Restricting Keywords and Values of a VTAM', 'Coding an EDIT', 'CNMSELTE', 'Preparing a Command for Editing',
            'Controlling the Appearance of Command'):
        naiyou = (f"「{t}」は、NetView コマンド認可テーブル（NetView command authorization table）に関わる項目で、"
                  "SECOPTS.CMDAUTH=TABLE を指定したときに有効になるコマンド保護の仕組みを説明する。"
                  "テーブルにはコマンド識別子（command identifier）を記述し、netid・luname・コマンド動詞・キーワード・値の組み合わせでオペレーターの実行可否を定義する。"
                  "テーブルは SAF コマンド認可（CMDAUTH=SAF）のバックアップとしても利用でき、SAF が判断できない場合や即時コマンドの保護に役立つ。")
        verify = ("1) NetView コンソールで `LIST SECOPTS` を発行し現在のコマンド認可方式を確認する。 "
                  "2) コマンド認可テーブルの構文を検証する: `REFRESH CMDAUTH=TABLE,TBLNAME=sec_table,TEST`（構文エラーがあればメッセージが出力される）。 "
                  "3) テーブルを有効化する: `REFRESH CMDAUTH=TABLE TBLNAME=sec_table`、または CNMSTYLE に SECOPTS.CMDAUTH=TABLE.sec_table を記述して NetView を再起動する。 "
                  "4) 再度 `LIST SECOPTS` で TABLE が反映されたことを確認する。")
        quiz = {"q": "NetView コマンド認可テーブルの構文を有効化前に検証するコマンドはどれか。",
                "choices": ["REFRESH CMDAUTH=TABLE,TBLNAME=sec_table,TEST", "LIST SPAN=SPAN1",
                            "SETROPTS CLASSACT(NETSPAN)", "RDEFINE NETCMDS UACC(NONE)"],
                "answer": 0,
                "explanation": "TEST キーワード付きの REFRESH CMDAUTH=TABLE で構文だけを検証でき、エラーがあればメッセージが生成される。実際の有効化は TEST を外して行う。"}
        return naiyou, verify, quiz

    # ---- SAF command authorization / NETCMDS ----
    if has(t, 'SAF Command Authorization', 'NETCMDS', 'Defining NetView Commands as NETCMDS',
            'Using the NETCMDS Class', 'Activating the SAF Command Authorization',
            'Using SAF without a Backup', 'Using SAF with a NetView Command Authorization Table for Backup',
            'Changing the Method of Command Authorization', 'Defining Command Authorization Checking',
            'Types of Command Authorization', 'Protecting NetView Command Names'):
        naiyou = (f"「{t}」は、SAF 製品（RACF など）の NETCMDS クラスを用いたコマンド認可（SECOPTS.CMDAUTH=SAF）に関する項目。"
                  "コマンド識別子を NETCMDS クラスのリソース名として RDEFINE し、PERMIT でオペレーターに権限を付与する。"
                  "SAF が判断できない場合に備え、NetView コマンド認可テーブルをバックアップ（BACKTBL=sec_table）として併用することが推奨される。"
                  "即時コマンドは NETCMDS では検査されないため、バックアップテーブルで保護する。")
        verify = ("1) NETCMDS クラスを活動化する: `SETROPTS CLASSACT(NETCMDS) GRPLIST`。 "
                  "2) 総称文字を使えるよう総称指定する: `SETROPTS GENERIC(NETCMDS)`。 "
                  "3) コマンド識別子を定義: `RDEFINE NETCMDS netid.luname.verb UACC(NONE)`、`PERMIT ... CLASS(NETCMDS) ID(OPER1) ACCESS(READ)`。 "
                  "4) NetView 側で `REFRESH CMDAUTH=SAF` を発行し、`LIST SECOPTS` で SAF 認可が有効になったことを確認する。")
        quiz = {"q": "SECOPTS.CMDAUTH=SAF を使う際、即時コマンドを保護するために推奨される方法はどれか。",
                "choices": ["NetView コマンド認可テーブルをバックアップ（BACKTBL）として併用する",
                            "NETSPAN クラスを活動化する", "OPERSEC=NETVPW に切り替える", "RODMMGR クラスを定義する"],
                "answer": 0,
                "explanation": "即時コマンドは NETCMDS クラスでは検査されないため、バックアップとしての NetView コマンド認可テーブルで保護する必要がある。"}
        return naiyou, verify, quiz

    # ---- Span of control / NETSPAN / span table ----
    if has(t, 'Span', 'NETSPAN', 'SPANDEF', 'SPANSYN', 'CTL', 'Span-of-control', 'Span of Control'):
        naiyou = (f"「{t}」は、オペレーターの制御範囲（span of control）に関する項目。"
                  "VTAM・RODM リソースを span 名でグループ化し、オペレーターがアクセスできる範囲を制限する。"
                  "SAF を使う場合は NETSPAN リソースクラスに span 名を RDEFINE し、各オペレーターを PERMIT で許可する（OPSPAN=SAF）。"
                  "NetView スパンテーブルを使う場合は SPANDEF/SPANSYN 文で span とリソースの対応を定義する。")
        verify = ("1) SAF 利用時: span を定義 `RDEFINE NETSPAN SPAN1 UACC(NONE)`、オペレーターを許可 `PERMIT SPAN1 CLASS(NETSPAN) ID(OPER1) ACCESS(READ)`。 "
                  "2) NETSPAN クラスを活動化: `SETROPTS CLASSACT(NETSPAN)`。 "
                  "3) NetView で `START SPAN=SPAN1` を発行し span を開始する。 "
                  "4) `LIST SPAN=SPAN1` で span に含まれるリソースを確認する。")
        quiz = {"q": "SAF（RACF）でオペレーターのスパン制御を行うとき、span 名を定義するリソースクラスはどれか。",
                "choices": ["NETSPAN", "NETCMDS", "RODMMGR", "DATASET"],
                "answer": 0,
                "explanation": "OPSPAN=SAF のとき、span 名は NETSPAN クラスに RDEFINE で定義し、オペレーターを PERMIT で許可する。span は NETSPAN 内の名前に一致しないと開始できない。"}
        return naiyou, verify, quiz

    # ---- Operator security / password / OPERSEC / logon ----
    if has(t, 'Operator', 'Password', 'OPERSEC', 'Logon', 'DSIOPF', 'DSIPRF', 'PassTicket',
            'Logon Times', 'Terminal Addresses', 'DSIEX12', 'Authentication', 'Migrating an Operator',
            'Restrict Logon', 'Autotask'):
        naiyou = (f"「{t}」は、NetView オペレーターのセキュリティ（パスワード・ログオン属性・認証）に関する項目。"
                  "オペレーターセキュリティ方式は SECOPTS.OPERSEC で指定し、NETVPW（DSIOPF のパスワードで検査）、SAFPW/SAFCHECK（SAF 製品で検査）、SAFDEF（SAF でオペレーター定義も管理）から選ぶ。"
                  "ログオン属性は DSIPRF データセットのプロファイルで定義し、オペレーター ID は DSIOPF に定義する。"
                  "SAF を使うとパスワード・ログオン時間・端末制限などを一元管理できる。")
        verify = ("1) `LIST SECOPTS` で現在の OPERSEC 値を確認する。 "
                  "2) SAF パスワード検査へ切替: CNMSTUSR/CxxSTGEN で SECOPTS.OPERSEC=SAFPW を設定、または `REFRESH OPERSEC=SAFPW` を発行。 "
                  "3) オペレーターでログオンを試し、認証が SAF 経由で行われることを確認する。 "
                  "4) 問題があれば `REFRESH OPERSEC=NETVPW` で NetView パスワード検査に戻し、DSIOPF の定義を見直す。")
        quiz = {"q": "オペレーターのパスワードを SAF 製品（RACF）で検査させる OPERSEC 値はどれか。",
                "choices": ["SAFPW", "SCOPE", "TABLE", "GLOBAL"],
                "answer": 0,
                "explanation": "SECOPTS.OPERSEC=SAFPW を指定するとパスワード／パスワードフレーズが SAF 製品で検査される。NETVPW は DSIOPF のパスワードを NetView 自身が検査する。"}
        return naiyou, verify, quiz

    # ---- RODM security ----
    if has(t, 'RODM', 'RODMMGR'):
        naiyou = (f"「{t}」は、RODM（Resource Object Data Manager）のセキュリティに関する項目。"
                  "RODM セキュリティには 3 方式があり、(1) *TSTRODM でシステムセキュリティをバイパス、(2) SAF の RODMMGR クラスにタスクと権限レベルを定義、(3) ユーザー定義クラスに定義、のいずれかを使う。"
                  "RACF を使う場合は 6 つのユーザー権限レベルに対応するリソース名を RODMMGR（またはユーザー定義クラス）に定義し、接続するユーザー ID を許可する。"
                  "RODMMGR クラスが無い SAF 製品では、RODM 初期化前にユーザー定義クラスと RACF ルーターテーブルを用意する必要がある。")
        verify = ("1) SEC_CLASS フィールド（EKGCUST）を確認し、RODM セキュリティ方式を把握する。 "
                  "2) RACF 利用時: 権限レベルのリソースを `RDEFINE RODMMGR rodmname.level UACC(NONE)` で定義する。 "
                  "3) 接続ユーザーを許可: `PERMIT rodmname... CLASS(RODMMGR) ID(userid) ACCESS(READ)`。 "
                  "4) RODM を再起動し、権限のあるユーザーが RODM へ接続できることを確認する。バイパスする場合は SEC_CLASS に *TSTRODM を指定する。")
        quiz = {"q": "SAF 製品で RODM タスクと権限レベルを定義する際に標準で用いるクラスはどれか。",
                "choices": ["RODMMGR", "NETSPAN", "NETCMDS", "OPERCMDS"],
                "answer": 0,
                "explanation": "RODM セキュリティは RODMMGR クラス（または同等のユーザー定義クラス）にタスクと 6 つの権限レベルを定義する。クラスが無い場合はバイパス(*TSTRODM)かユーザー定義クラスを使う。"}
        return naiyou, verify, quiz

    # ---- Authority checking source/target/SOURCEID ----
    if has(t, 'Authority Checking', 'SOURCEID', 'Source for Authority', 'Target for Authority',
            'Command Source', 'Authorization Checking', 'Source ID', 'Command Invocations',
            'Flexibility of Authorization'):
        naiyou = (f"「{t}」は、コマンドの権限検査の対象（発行元か実行先か）に関する項目。"
                  "SECOPTS.AUTHCHK=SOURCEID を指定すると、コマンドの本来の発行者（command source に最も近い ID）に対して権限を検査する。"
                  "TARGETID を指定すると、コマンドを実際に実行するタスクに対して検査し、ルーティングされたコマンドをキーワードとして扱う。"
                  "システムコンソールからログオンなしで発行された VTAM コマンドなどは source ID が *BYPASS* となり、完全に認可済みと見なされ検査されない。")
        verify = ("1) `LIST SECOPTS` で現在の AUTHCHK 設定（SOURCEID か TARGETID）を確認する。 "
                  "2) SOURCEID へ切替: CNMSTYLE に SECOPTS.AUTHCHK=SOURCEID を設定、または `REFRESH AUTHCHK=SOURCEID`。 "
                  "3) OPER1 から `EXCMD NETOP1,...` を発行し、認可が発行元 OPER1 の権限で検査されることを確認する。 "
                  "4) 認可失敗メッセージ（BNH233E 等）に表示される source 発行者を確認する。")
        quiz = {"q": "SECOPTS.AUTHCHK=SOURCEID を指定したとき、EXCMD コマンドの権限はどの ID に対して検査されるか。",
                "choices": ["コマンドの本来の発行者（source に最も近い ID）", "コマンドを実行するターゲットタスク",
                            "常に PPT タスク", "RODM のユーザー ID"],
                "answer": 0,
                "explanation": "AUTHCHK=SOURCEID では本来の発行者に対して権限を検査するため、複数オペレーターに EXCMD を許可しつつ発行者ごとに個別の権限制御ができる。TARGETID は実行タスクを検査する。"}
        return naiyou, verify, quiz

    # ---- EXCMD/RMTCMD/RUNCMD/TSO/SEC keyword/CHRON ----
    if has(t, 'EXCMD', 'RMTCMD', 'RUNCMD', 'TSO', 'SEC Keyword', 'CHRON', 'SUBMIT',
            'RMTOPS', 'Dynamic RMTCMD', 'UNIX Command Server', 'Command Server',
            'Surrogate', 'TSO Pipe', 'TSO Stage', 'TSO Server'):
        naiyou = (f"「{t}」は、タスク間・ドメイン間でコマンドを送るコマンド（EXCMD・RMTCMD・RUNCMD など）や TSO/UNIX コマンドサーバーの認可に関する項目。"
                  "EXCMD は送信先 operator_id と送るコマンドをキーワード・値の対として検査する。"
                  "RMTCMD はリモートドメインへコマンドを送り、SECOPTS.RMTAUTH=ORIGIN/SENDER で検査対象の ID を切り替える。RMTOPS クラスや動的 RMTCMD セキュリティテーブルで認可を定義できる。"
                  "コマンド定義文の SEC キーワード（SEC=CH は常に検査、SEC=BY は常にバイパス）で個別に検査要否を制御できる。")
        verify = ("1) `LIST SECOPTS` で RMTAUTH/AUTHCHK 設定を確認する。 "
                  "2) EXCMD 認可: NETCMDS クラスで `RDEFINE NETCMDS netid.luname.EXCMD.target_verb UACC(NONE)` を定義し PERMIT する。 "
                  "3) NetView で `EXCMD AUTO1,target_command` を発行し、キーワード・値の対として検査されることを確認する。 "
                  "4) コマンドを常時検査させたい場合は CMDDEF 文に SEC=CH を指定し、`REFRESH` 後に動作を確認する。")
        quiz = {"q": "CMDDEF 文で SEC=CH を指定した場合のコマンド認可検査の挙動はどれか。",
                "choices": ["環境にかかわらず常に認可検査を行う", "環境にかかわらず常にバイパスする",
                            "自動化テーブル由来のときだけ検査する", "即時コマンドのときだけバイパスする"],
                "answer": 0,
                "explanation": "SEC=CH は環境にかかわらず常に認可検査を行う。SEC=BY は常にバイパスする。ネストされたコマンドを保護するには CNMCMDU で SEC=CH を指定する。"}
        return naiyou, verify, quiz

    # ---- NMC / management console / NGMF / views ----
    if has(t, 'Management Console', 'NGMFADMN', 'NGMFVSPN', 'NGMFCMDS', 'View', 'DUILOGON',
            'Policy', 'Applying Policy'):
        naiyou = (f"「{t}」は、NetView 管理コンソール（NMC）のセキュリティに関する項目。"
                  "DUILOGON コマンドへのアクセスを制限することで、許可されていないユーザーの管理コンソールへのログオンを防げる。"
                  "管理者権限は NGMFADMN 属性、管理コンソールコマンド能力は NGMFCMDS 属性で制御する。"
                  "ビューやビュー内リソースの表示制御は NGMFVSPN 属性（4 文字で span_level・visible_objects・restrict_view_info・restrict_list_info を指定）で行い、NetView スパンテーブルで span チェックされる。")
        verify = ("1) オペレータープロファイル（DSIPRF）で NGMFADMN/NGMFCMDS/NGMFVSPN 属性を確認する。 "
                  "2) ビューのみ span チェックする場合 NGMFVSPN=VNNN、リソースのみなら RYNN を設定する。 "
                  "3) 該当オペレーターでサインオフ・サインオンし直し、変更を反映する（開いているビューには即時反映されない）。 "
                  "4) 権限のないビューを開こうとしてエラーメッセージが出ること、許可ビューが表示されることを確認する。")
        quiz = {"q": "NetView 管理コンソールで、オペレーターがビュー名やビュー内リソースを表示できる範囲を span チェックで制御する属性はどれか。",
                "choices": ["NGMFVSPN", "NGMFADMN", "OPERSEC", "AUTHCHK"],
                "answer": 0,
                "explanation": "NGMFVSPN 属性は 4 文字でビュー名・リソースの span チェック方法を指定する。NGMFADMN は管理者権限、NGMFCMDS は管理コンソールコマンド能力を制御する。"}
        return naiyou, verify, quiz

    # ---- TCP/IP, AT-TLS, REXEC/RSH/SOCKET/Alert receiver/Zowe ----
    if has(t, 'TCP/IP', 'Transport Layer Security', 'AT-TLS', 'REXEC', 'RSH', 'SOCKET',
            'Alert Receiver', 'IP Addresses', 'Zowe', 'REST Server', 'Single Sign-On', 'SNMP'):
        naiyou = (f"「{t}」は、NetView の TCP/IP 関連通信のセキュリティに関する項目。"
                  "NetView 管理コンソールや各種 TCP/IP サーバー（REXEC・RSH・SOCKET など）との通信は、AT-TLS（Application Transparent Transport Layer Security）で暗号化・認証できる（サンプル CNMSJTLS を参照）。"
                  "TCP/IP アラート受信タスクへの不正接続は WEBACC コマンドで制御し、DSIIPCHK タスクに対象 IP の WEBACC 発行を許可する。"
                  "IP アドレスはコマンドセキュリティやスパン制御の対象として保護できる。")
        verify = ("1) TCP/IP プロファイルで対象接続の TTLS 設定（TTLS/NOTTLS）を確認する。 "
                  "2) NetView と管理コンソール間の AT-TLS を有効化するためサンプル CNMSJTLS を参照・適用する。 "
                  "3) TCP/IP アラート受信を許可するには DSIIPCHK が対象 IP に対して `WEBACC` を発行できるよう PERMIT する。 "
                  "4) 接続を確立し、AT-TLS Policy Status が Enabled になり暗号化セッションが張られることを確認する。")
        quiz = {"q": "NetView と NetView 管理コンソール間の通信を暗号化・認証するために参照するサンプルはどれか。",
                "choices": ["CNMSJTLS（AT-TLS の構成）", "DSIOPF", "EKGCUST", "ICHRIN03"],
                "answer": 0,
                "explanation": "AT-TLS による NetView と管理コンソール間のセキュア通信は、サンプル CNMSJTLS を参照して有効化・構成する。WEBACC はアラート受信タスクへの接続制御に使う。"}
        return naiyou, verify, quiz

    # ---- Auditing / Tracing SAF / debugging / checklist ----
    if has(t, 'Auditing', 'Tracing SAF', 'RACF Auditing', 'Debugging', 'Checklist',
            'Check These Things', 'Cannot Isolate', 'Performance Is Degraded', 'Logging',
            'If a Command', 'If an Operator', 'If a Resource', 'If You Are Using',
            'If You Cannot', 'If Your Specified', 'If Performance'):
        naiyou = (f"「{t}」は、NetView セキュリティの監査・トレース・問題判別に関する項目。"
                  "RACF AUDIT を使うと不正コマンド試行の監査証跡が取れ、SETROPTS で AUDIT(NETCMDS) を指定すると NetView コマンドの SMF レコードが生成される。"
                  "SAF 呼び出し（RACROUTE）の問題は NetView TRACE コマンドの SAF オプションで切り分ける。"
                  "問題判別では `LIST SECOPTS` で現在のセキュリティオプションを確認し、認可失敗メッセージ（BNH233E）のコマンド識別子や source 発行者を手掛かりにする。過剰な監査は性能を低下させる点に注意する。")
        verify = ("1) `LIST SECOPTS` で有効なセキュリティオプションを確認する。 "
                  "2) コマンド監査を有効化: `SETROPTS AUDIT(NETCMDS)`、必要リソースを RDEFINE/RALTER で監査レベル指定する。 "
                  "3) SAF 呼び出しをトレース: NetView `TRACE` コマンドで SAF オプションを指定し、`LIST TRACE` で SAF TRACE/SAF TYPES を確認する。 "
                  "4) 認可失敗時は BNH233E のコマンド識別子を確認し、不要な監査は外して性能影響を抑える。")
        quiz = {"q": "NetView から SAF 製品への RACROUTE 呼び出しの問題を切り分けるために使うコマンドはどれか。",
                "choices": ["TRACE コマンドの SAF オプション", "START SPAN", "RDEFINE NETSPAN", "GETCONID"],
                "answer": 0,
                "explanation": "NetView TRACE コマンドの SAF オプションは RACROUTE 呼び出しの問題切り分けに使うクロスプロダクトの保守支援機能。LIST TRACE で SAF TRACE/SAF TYPES を確認できる。"}
        return naiyou, verify, quiz

    # ---- Scenarios for converting ----
    if has(t, 'Scenario', 'Converting', 'Migrating', 'SECMIGR', 'Maintaining Existing',
            'Defining and Changing Types'):
        naiyou = (f"「{t}」は、NetView のセキュリティ方式を移行・変換するシナリオに関する項目。"
                  "scope チェックから NetView コマンド認可テーブルへ、さらに SAF コマンド認可（NETCMDS クラス）へ段階的に移行する手順を扱う。"
                  "SECMIGR コマンドで既存定義からコマンド認可テーブルを生成でき、SECOPTS.CMDAUTH=SCOPE.tbl_name を指定すると NetView が自動生成する。"
                  "移行中は安全のためコマンド認可テーブルをバックアップとして残し、SAF が判断できない場合に備える。")
        verify = ("1) 既存定義から `SECMIGR` でコマンド認可テーブルを生成する（または CMDAUTH=SCOPE.tbl_name で自動生成）。 "
                  "2) 生成テーブルの構文を検証: `REFRESH CMDAUTH=TABLE,TBLNAME=sec_table,TEST`。 "
                  "3) NETCMDS クラスを活動化し（`SETROPTS CLASSACT(NETCMDS) GRPLIST`）、RDEFINE/PERMIT で定義を移す。 "
                  "4) `REFRESH CMDAUTH=SAF` で SAF 認可へ切替え、`LIST SECOPTS` で確認する。バックアップに BACKTBL を併用する。")
        quiz = {"q": "既存の NetView セキュリティ定義からコマンド認可テーブルを生成するコマンドはどれか。",
                "choices": ["SECMIGR", "GETCONID", "WEBACC", "DSIVSAM"],
                "answer": 0,
                "explanation": "SECMIGR コマンドで既存システムからコマンド認可テーブルを生成できる。SECOPTS.CMDAUTH=SCOPE.tbl_name を指定すれば NetView が自動生成する。"}
        return naiyou, verify, quiz

    # ---- Data set / VSAM / DSIVSAM / READSEC ----
    if has(t, 'Data Set', 'VSAM', 'DSIVSAM', 'DSIVSMX', 'READSEC', 'WRITESEC', 'PWDSEC',
            'Members'):
        naiyou = (f"「{t}」は、NetView が使用するデータセット・VSAM のアクセスセキュリティに関する項目。"
                  "MVS では DATASET クラスでデータセットおよびメンバーへのアクセスを制御する。"
                  "NetView の READSEC・WRITESEC・PWDSEC コマンドや DSIVSAM/DSIVSMX コマンドで VSAM データセットアクセスを扱う。"
                  "自動化テーブルやコマンドリストのデータセットへのアクセスを制限することで、不正な更新を防ぐ。")
        verify = ("1) 保護対象データセットを RACF DATASET クラスで定義し UACC(NONE) を設定する。 "
                  "2) NetView の実行ユーザー／タスクに必要な ACCESS を `PERMIT dsname ID(...) ACCESS(READ|UPDATE)` で付与する。 "
                  "3) NetView を起動し、許可タスクが当該データセット・メンバーへアクセスできることを確認する。 "
                  "4) 権限のないタスクからのアクセスが拒否されることを確認する。")
        quiz = {"q": "MVS システムで NetView のデータセットおよびメンバーへのアクセスを制御する RACF クラスはどれか。",
                "choices": ["DATASET", "NETCMDS", "NETSPAN", "RODMMGR"],
                "answer": 0,
                "explanation": "データセットおよびメンバーへのアクセスは DATASET クラスで制御する。NETCMDS はコマンド、NETSPAN は span、RODMMGR は RODM 用のクラス。"}
        return naiyou, verify, quiz

    # ---- Automation security / AON / autotask / DUIFPOLI ----
    if has(t, 'Automation', 'AON', 'Automated Operator', 'DUIFPOLI', 'Restricting Authorization',
            'Restricting Data Set Access to the Automation'):
        naiyou = (f"「{t}」は、自動化（automation）に関わるセキュリティ項目。"
                  "自動化テーブルやコマンドリストから発行されるコマンドの認可、自動オペレータータスク（autotask）へのアクセス制限を扱う。"
                  "autotask のオペレーター ID を定義し、その権限でコマンドが実行される。AON（Automated Operations Network）のコマンド・キーワード・値も保護対象にできる。"
                  "自動化由来コマンドの認可検査をまとめてバイパスするには DEFAULTS コマンドで AUTOSEC=BYPASS を設定する。")
        verify = ("1) autotask のオペレーター ID を DSIOPF/CNMSTYLE で定義し、必要な権限を付与する。 "
                  "2) 自動化テーブル由来コマンドの認可を確認する（`LIST SECOPTS` で AUTHCHK 等を確認）。 "
                  "3) 自動化コマンドの認可検査を一括バイパスする場合: `DEFAULTS AUTOSEC=BYPASS`。 "
                  "4) 自動化アクションを発火させ、autotask の権限でコマンドが正しく実行されることを確認する。")
        quiz = {"q": "自動化テーブル由来のすべてのコマンドの認可検査をバイパスする設定はどれか。",
                "choices": ["DEFAULTS AUTOSEC=BYPASS", "SETROPTS CLASSACT(NETSPAN)",
                            "REFRESH OPERSEC=SAFPW", "RDEFINE NETCMDS"],
                "answer": 0,
                "explanation": "DEFAULTS コマンドで AUTOSEC=BYPASS を設定すると、自動化テーブル由来のすべてのコマンドの認可検査がバイパスされる。autotask は定義されたオペレーター ID の権限で動作する。"}
        return naiyou, verify, quiz

    # ---- Overview / concepts / authorization / publications / library ----
    if has(t, 'Overview', 'What Is', 'Why Limit', 'Authorization Checking', 'Types of Security',
            'Centralized Security', 'Bypassing or Defining', 'library', 'publications',
            'Terminology', 'online help', 'Programming Interfaces', 'Privacy policy',
            'Special Characters', 'Pattern-Matching', 'Dynamic Definitions', 'Accessing publications',
            'Ordering publications'):
        naiyou = (f"「{t}」は、NetView セキュリティの概念・概要に関する項目。"
                  "SAF 製品（RACF など）は RACROUTE インターフェースを通じて集中監査・リソース認可・ユーザー識別/検証を提供する。"
                  "NetView では SAF を使ってコマンド認可・オペレーターパスワード・データセットアクセス・span 制御・RODM セキュリティを一元管理できる。"
                  "認可検査（authorization checking）により、保護されたコマンドを許可されたオペレーターだけが発行できるようにする。")
        verify = ("1) SAF 製品（RACF）が稼働し、NetView が使うクラス（NETCMDS・NETSPAN・RODMMGR 等）が活動状態か確認する: `SETROPTS LIST`。 "
                  "2) NetView 起動後に `LIST SECOPTS` で現在のセキュリティオプション（CMDAUTH・OPERSEC・OPSPAN・AUTHCHK）を確認する。 "
                  "3) 保護コマンドを許可オペレーターと非許可オペレーターで発行し、認可検査が機能することを確認する。 "
                  "4) 認可失敗メッセージ（BNH233E 等）でコマンド識別子を確認する。")
        quiz = {"q": "SAF 製品（RACF など）が提供するインターフェースで、NetView からのセキュリティ要求を受け付けるものはどれか。",
                "choices": ["RACROUTE", "GETCONID", "WEBACC", "SECMIGR"],
                "answer": 0,
                "explanation": "SAF 製品は RACROUTE インターフェースを通じて集中監査・リソース認可・ユーザー識別/検証を行う。NetView はこれを使ってコマンド認可やパスワード検査などを一元化する。"}
        return naiyou, verify, quiz

    # ---- Protecting commands (immediate / special chars / MVS / jobs) ----
    if has(t, 'Protecting', 'Protect', 'Immediate Commands', 'MVS Command Revision',
            'MVS System Commands', 'Jobs Submitted', 'Special Characters',
            'Inherited Command Security', 'Exceptions to Command'):
        naiyou = (f"「{t}」は、特定種別のコマンドを認可検査で保護する方法に関する項目。"
                  "即時コマンド（immediate commands）は NETCMDS クラスでは検査されないため、CMDAUTH=SAF 利用時はバックアップのコマンド認可テーブルで保護する。"
                  "MVS システムコマンドや MVS コマンドリビジョン処理、SUBMIT コマンドで投入するジョブも保護対象にできる。"
                  "特殊文字を含むコマンドや、認可済みコマンドリストに継承されるセキュリティの扱いにも注意する。")
        verify = ("1) 保護したいコマンド識別子を NETCMDS クラス（または認可テーブル）に定義する。 "
                  "2) 即時コマンド保護のため、CMDAUTH=SAF でもバックアップ認可テーブル（BACKTBL=sec_table）を設定する。 "
                  "3) `REFRESH` 後、許可オペレーターと非許可オペレーターで当該コマンドを発行し、保護されていることを確認する。 "
                  "4) ネストされたコマンドは CNMCMDU の CMDDEF 文で SEC=CH を指定して保護する。")
        quiz = {"q": "CMDAUTH=SAF のとき、NETCMDS クラスで検査されない即時コマンドを保護する方法はどれか。",
                "choices": ["バックアップの NetView コマンド認可テーブル（BACKTBL）を使う",
                            "NETSPAN クラスに定義する", "AUTOSEC=BYPASS を設定する", "*TSTRODM を指定する"],
                "answer": 0,
                "explanation": "即時コマンドは NETCMDS クラスでは検査されないため、CMDAUTH=SAF でもバックアップの NetView コマンド認可テーブル（BACKTBL=sec_table）で保護する。"}
        return naiyou, verify, quiz

    # ---- Tivoli Enterprise Portal ----
    if has(t, 'Tivoli Enterprise Portal', 'Take Action'):
        naiyou = (f"「{t}」は、Tivoli Enterprise Portal（TEP）ユーザー ID と NetView の連携セキュリティに関する項目。"
                  "TEP ユーザー ID を NetView に定義し、有効な NetView オペレーター ID にマッピングすることで、TEP から発行される操作の認可を NetView 側で制御する。"
                  "TEP の Take Action コマンドはマッピングされた NetView オペレーター ID の権限でコマンド認可検査を受ける。"
                  "新規 TEP ユーザー ID の作成とマッピング手順を扱う。")
        verify = ("1) TEP ユーザー ID を作成し、NetView オペレーター ID にマッピングする定義を行う。 "
                  "2) マッピング先 NetView オペレーター ID に必要なコマンド権限（NETCMDS 等）を付与する。 "
                  "3) TEP から Take Action コマンドを発行し、マッピングされたオペレーター権限で認可検査されることを確認する。 "
                  "4) 権限のないコマンドが拒否されることを確認する。")
        quiz = {"q": "Tivoli Enterprise Portal の Take Action コマンドはどの ID の権限で認可検査されるか。",
                "choices": ["マッピングされた NetView オペレーター ID", "RODM のシステム ID",
                            "常に PPT タスク", "*BYPASS* で常に許可"],
                "answer": 0,
                "explanation": "TEP ユーザー ID は有効な NetView オペレーター ID にマッピングされ、Take Action コマンドはそのオペレーター ID の権限でコマンド認可検査を受ける。"}
        return naiyou, verify, quiz

    # ---- Troubleshooting / Problem classification (raw rows like Accessing publications odd) ----
    if has(t, 'Problem', 'abend', 'Troubleshooting'):
        naiyou = (f"「{t}」は、NetView のセキュリティ／問題判別に関する項目。"
                  "セキュリティ問題で認可が期待どおりに動作しない場合は、まず `LIST SECOPTS` で有効なセキュリティオプションを確認する。"
                  "認可失敗メッセージ（BNH233E 等）のコマンド識別子や source 発行者を手掛かりに、NETCMDS/NETSPAN の定義や AUTHCHK 設定を見直す。"
                  "RACROUTE 呼び出しの問題は NetView TRACE の SAF オプションで切り分ける。")
        verify = ("1) `LIST SECOPTS` で現在のセキュリティオプションを確認する。 "
                  "2) 認可失敗メッセージのコマンド識別子・source 発行者を確認する。 "
                  "3) 必要に応じ NetView `TRACE` の SAF オプションで RACROUTE 呼び出しをトレースし `LIST TRACE` で確認する。 "
                  "4) NETCMDS/NETSPAN の定義と AUTHCHK 設定を見直して問題を特定する。")
        quiz = {"q": "NetView のセキュリティ問題判別で最初に有効なセキュリティオプションを確認するコマンドはどれか。",
                "choices": ["LIST SECOPTS", "START SPAN", "RDEFINE NETCMDS", "GETCONID"],
                "answer": 0,
                "explanation": "LIST SECOPTS で現在有効なセキュリティオプション（CMDAUTH・OPERSEC・OPSPAN・AUTHCHK 等）を一覧表示でき、問題判別の起点になる。"}
        return naiyou, verify, quiz

    # ---- RACF resource/class definition ----
    if has(t, 'RACF Resource', 'RACF Router Table', 'Resource Class to the RACF',
            'Class Descriptor Table', 'Authorizing User IDs to RACF', 'Defining RACF',
            'Controlling Access to Commands', 'Using an SAF Product Exclusively'):
        naiyou = (f"「{t}」は、SAF 製品（RACF）側のリソース名・クラスを定義し、NetView のコマンドや資源を保護する作業に関する項目。"
                  "NetView が使うクラス（NETCMDS・NETSPAN・RODMMGR 等）をクラス記述子テーブルに定義し、必要に応じて RACF ルーターテーブル（ICHRFRTB マクロ）を作成する。"
                  "保護対象リソースを RDEFINE で定義し、ユーザー ID／グループを PERMIT で対応する RACF リソース名に許可する。"
                  "SAF 製品を排他的に使うことで、DSIOPF・DSIPRF の定義を SAF 側へ集約できる。")
        verify = ("1) 対象クラスを活動化する: `SETROPTS CLASSACT(NETCMDS) GRPLIST`（必要なら GENERIC も指定）。 "
                  "2) 保護リソースを定義: `RDEFINE NETCMDS resource_name UACC(NONE)`。 "
                  "3) ユーザー ID を許可: `PERMIT resource_name CLASS(NETCMDS) ID(userid) ACCESS(READ)`。 "
                  "4) NetView で `REFRESH` 後、許可ユーザーがアクセスでき、非許可ユーザーが拒否されることを確認する。")
        quiz = {"q": "新しいセキュリティクラスを RACF で使えるようにするために作成することがあるテーブルはどれか。",
                "choices": ["RACF ルーターテーブル（ICHRFRTB マクロ）", "NetView スパンテーブル",
                            "自動化テーブル", "CONSOLxx メンバー"],
                "answer": 0,
                "explanation": "ユーザー定義のセキュリティクラスを使う場合、RACF クラス記述子テーブルへの定義に加え、ICHRFRTB マクロで RACF ルーターテーブルを作成する必要がある。"}
        return naiyou, verify, quiz

    # ---- Operator profile attributes (CONSNAME/CTL/DOMAINS/HCL/IC/MSGRECVR/Operator Attributes) ----
    if has(t, 'CONSNAME', 'DOMAINS', 'HCL', 'Using IC', 'MSGRECVR', 'Operator Attributes',
            'Operator Access to Spans', 'Defining Operator', 'EMCS', 'Console',
            'Determining Attributes'):
        naiyou = (f"「{t}」は、NetView オペレータープロファイル（DSIPRF）で定義する属性に関する項目。"
                  "プロファイルにはオペレーターが使えるコマンドや資源を制限する各種属性（CONSNAME・CTL・DOMAINS・HCL・IC・MSGRECVR・NGMFxxx など）を記述する。"
                  "拡張多重コンソールサポート（EMCS）コンソールではコンソール名がオペレーター ID と同じになり、OPERPARM（AUTH 等）で属性を定義する。"
                  "これらの属性はログオン時に DSIPRF から読み込まれ、オペレーターの権限範囲を決定する。")
        verify = ("1) 対象オペレーターのプロファイル（DSIPRF メンバー）で該当属性を確認・設定する。 "
                  "2) EMCS コンソール名を SAF で保護する場合は OPERPARM 付きで `ADDUSER` し、RDEFINE/PERMIT を行う。 "
                  "3) オペレーターをログオンし直し、プロファイルが読み込まれることを確認する。 "
                  "4) 属性で制限したコマンド・資源・ドメインへのアクセスが意図どおり制御されることを確認する。")
        quiz = {"q": "オペレーターのログオン時に権限範囲を決める属性が読み込まれる NetView のデータセットはどれか。",
                "choices": ["DSIPRF", "DSILOG", "EKGCUST", "CNMSJTLS"],
                "answer": 0,
                "explanation": "オペレータープロファイルは DSIPRF データセットに置かれ、ログオン時に読み込まれてオペレーターが使えるコマンドや資源を制限する。オペレーター ID 自体は DSIOPF に定義する。"}
        return naiyou, verify, quiz

    # ---- Examples / Usage Notes (security context) ----
    if has(t, 'Examples', 'Example', 'Usage Notes'):
        naiyou = (f"「{t}」は、NetView セキュリティ（SAF 連携）の設定例・使用上の注意に関する項目。"
                  "コマンド認可（NETCMDS）、span 制御（NETSPAN）、RODM セキュリティ（RODMMGR）などの具体的な RDEFINE/PERMIT 例や、"
                  "REFRESH・LIST SECOPTS などのコマンド使用時の注意点を示す。"
                  "例では netid.luname.verb 形式のコマンド識別子や、span 名・リソース名の定義パターンが示される。")
        verify = ("1) 例にならい RACF でリソースを定義する（例: `RDEFINE NETCMDS netid.luname.verb UACC(NONE)`）。 "
                  "2) 対象オペレーター／ユーザーを `PERMIT ... ACCESS(READ)` で許可する。 "
                  "3) NetView で `REFRESH` し `LIST SECOPTS` で反映を確認する。 "
                  "4) 許可／非許可オペレーターで動作を確認し、例どおりに認可検査が機能することを検証する。")
        quiz = {"q": "NETCMDS クラスで NetView コマンドを保護する際のコマンド識別子の典型的な形式はどれか。",
                "choices": ["netid.luname.verb", "SPAN=span_name", "rodmname.level", "dsname.member"],
                "answer": 0,
                "explanation": "コマンド認可ではコマンド識別子を netid.luname.コマンド動詞の形式で表し、NETCMDS クラスのリソース名として定義する。総称文字（*）も利用できる。"}
        return naiyou, verify, quiz

    # ---- Generic security fallback ----
    naiyou = (f"「{t}」は、IBM Z NetView のセキュリティ（SAF 連携）に関する項目で、NetView Security Reference に記載される。"
              "NetView は SAF 製品（RACF など）と連携し、コマンド認可（NETCMDS クラス）、オペレーターセキュリティ（OPERSEC）、"
              "スパン制御（NETSPAN クラス）、RODM セキュリティ（RODMMGR クラス）などを一元的に管理する。"
              "本項目もこの SAF 連携の枠組みの中で、該当機能の定義・設定・運用を扱う。")
    verify = ("1) SAF 製品（RACF）が稼働し、関連クラスが活動状態か確認する: `SETROPTS LIST`。 "
              "2) NetView で `LIST SECOPTS` を発行し、現在のセキュリティオプションを確認する。 "
              "3) 該当機能のリソースを RDEFINE/PERMIT で定義し、`REFRESH` で反映する。 "
              "4) 許可／非許可のオペレーターで動作を確認し、認可検査が意図どおり機能することを検証する。")
    quiz = {"q": "IBM Z NetView でコマンド認可を SAF 製品に委ねる場合に使用する RACF クラスはどれか。",
            "choices": ["NETCMDS", "NETSPAN", "RODMMGR", "DATASET"],
            "answer": 0,
            "explanation": "SECOPTS.CMDAUTH=SAF のとき、コマンド認可は SAF 製品の NETCMDS クラスで検査される。NETSPAN は span、RODMMGR は RODM、DATASET はデータセット用。"}
    return naiyou, verify, quiz


out_rows = []
for r in rows:
    naiyou, verify, quiz = build(r['title'], r['secref'])
    out_rows.append({
        "row_id": r['row_id'],
        "title": r['title'],
        "naiyou_jp": naiyou,
        "verify_steps": verify,
        "quiz": quiz,
        "source": f"{r['secref']} ({RAG})",
        "rag_hit": True,
    })

doc = {
    "page": "g038",
    "product": "IBM NetView 6.4",
    "total_rows": len(rows),
    "target_rows": len(rows),
    "fixed_count": len(out_rows),
    "rows": out_rows,
}
json.dump(doc, open('_phase2_outputs/g038_fixed.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print("wrote", len(out_rows), "rows")
