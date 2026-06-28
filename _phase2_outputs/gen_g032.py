# -*- coding: utf-8 -*-
import json, re

rows = json.load(open(r'C:\kvba\zos-atoms-site\_phase2_outputs\g032_rows.json', encoding='utf-8'))

GUIDE = "NetView_6.4_Resource_Object_Data_Manager_and_GMFHS_Programmers_Guide.pdf"
DMREF = "NetView_6.4_Data_Model_Reference.pdf"
GRAPH = "NetView_6.4_Installation_Configuring_Graphical_Components.pdf"
NMC   = "NetView_6.4_Users_Guide_NetView_Management_Console.pdf"
AUTO  = "NetView_6.4_Automation_Guide.pdf"

# RAG hit reference strings (grounded above)
RAG = {
 'gmfhs': f"{GUIDE} p.103 / {GRAPH} p.17 / Users_Guide_NetView.pdf p.38",
 'rodm':  f"{GUIDE} p.337 / Users_Guide_NetView.pdf p.38 / {AUTO} p.371",
 'bldviews': f"{GUIDE} p.579 / {GRAPH} p.65",
 'method': f"{GUIDE} p.32, p.346, p.349",
 'layout': f"{GUIDE} p.671, p.678 / {DMREF} p.201",
 'load': f"{GUIDE} p.240, p.256, p.268 / p.244",
 'rodmview': f"{GUIDE} p.503 / Users_Guide_NetView.pdf p.151",
 'corr': f"{GUIDE} p.329, p.333, p.334 / IP_Management.pdf p.26",
 'flcarodm': f"{GUIDE} p.573 / {GRAPH} p.64 / Users_Guide_NetView.pdf p.186",
 'alert': f"{GUIDE} p.173, p.177, p.179",
 'platform': f"{GUIDE} p.171, p.578 / {NMC} p.77",
 'nonsna': f"{GUIDE} p.29, p.30, p.650",
 'api': f"{GUIDE} p.308, p.460, p.450",
 'notify': f"{GUIDE} p.32, p.322, p.326, p.347",
}

# ---- cluster classifier by title keywords ----
def cluster(title):
    t = title.lower()
    if 'bldviews' in t or 'delviews' in t: return 'bldviews'
    if 'layout' in t or 'ellip' in t or 'grid' in t or 'radial' in t or 'hierarchical graph' in t \
       or 'token-ring' in t or 'bus network' in t or 'local area network layout' in t \
       or 'connectivity tree' in t or 'view layout' in t or 'choosing a view' in t: return 'layout'
    if 'rodmview' in t: return 'rodmview'
    if 'flcarodm' in t or 'unload' in t: return 'flcarodm'
    if 'correlat' in t or 'span-of-control' in t or 'topology object' in t: return 'corr'
    if 'alert' in t or 'resolution' in t or 'duifedef' in t: return 'alert'
    if 'load function' in t or 'loading' in t or 'load func' in t or ('load' in t and 'data model' in t) \
       or 'using load function' in t or 'process for loading' in t: return 'load'
    if 'method' in t or 'query function' in t or 'change field' in t or 'create actions' in t \
       or 'delete actions' in t or 'link/unlink' in t or 'locate objects' in t or 'subfield actions' in t \
       or 'compound query' in t or 'simple query' in t or 'function reference' in t \
       or 'function parameter' in t or 'method type' in t or 'method api' in t or 'method anchor' in t \
       or 'method services' in t or 'method actions' in t or 'supplied methods' in t \
       or 'coding your rodm method' in t or 'writing rodm methods' in t or 'types of methods' in t: return 'method'
    if 'collection' in t or 'automation platform' in t or 'resource manager' in t: return 'platform'
    if 'non-sna' in t or 'managing sna' in t or 'defining resources' in t or 'defining your network' in t \
       or 'identifying network' in t or 'manual network' in t or 'sample network' in t \
       or 'changing network definitions' in t or 'defining your configuration' in t: return 'nonsna'
    if 'notif' in t or 'object deletion' in t or 'locking' in t or 'asynchronous error' in t \
       or 'error conditions' in t: return 'notify'
    if 'return code' in t or 'reason code' in t or 'connecting to rodm' in t or 'disconnecting' in t \
       or 'api' in t or 'control blocks' in t or 'object data stream' in t or 'result stem' in t \
       or 'stem building' in t or 'programming interface' in t or 'application program interface' in t \
       or 'user application program' in t or 'programming reference' in t: return 'api'
    if 'gmfhs' in t: return 'gmfhs'
    return 'rodm'

# ---- per-cluster JP description + verify + quiz factory ----
def make(title, cl, src):
    T = title
    if cl == 'gmfhs':
        naiyou = (f"GMFHS（Graphic Monitor Facility ホスト・サブシステム）は RODM および NetView 管理コンソールと連携し、"
                  f"ネットワーク資源のグラフィック・ビューを表示してビューから選択した資源へコマンドを発行するホスト・プログラムである。"
                  f"ビューには資源の状況（status）情報と構成（configuration）情報の両方が含まれ、RODM データ・キャッシュの内容を変更することで"
                  f"GMFHS と管理コンソールの動作を制御できる。「{T}」はこの GMFHS と RODM の連携領域に属する項目である。")
        vq, ch, ans, ex = ("GMFHS が表示するビューに含まれる情報の種類はどれか。",
            ["状況（status）情報のみ","構成（configuration）情報のみ","状況情報と構成情報の両方","セキュリティ監査ログのみ"],2,
            "GMFHS のビューには資源の status と configuration の両方が含まれる（Programmer's Guide p.103）。")
        verify = ["NetView コンソールにログオンする。","GMFHS サブタスク（DUIFCDST 等）の稼働を確認: LIST STATUS=TASKS で DUI 系タスクが ACTIVE であることを確認。",
                  "NetView 管理コンソールにサインオンし、RODM ベースのネットワーク・ビューを開く。","ビュー上の資源を選択し status と configuration が表示されることを確認する。"]
        rag = RAG['gmfhs']
    elif cl == 'rodm':
        naiyou = (f"RODM（Resource Object Data Manager）はホスト・プロセッサのメモリ上に常駐するオブジェクト指向データ・キャッシュであり、"
                  f"ネットワークやシステムの資源をオブジェクトとして表現する。約 200 万オブジェクトを保持でき、構成データと資源状況情報を高速・高トランザクションで扱える。"
                  f"NetView はトポロジーや状況などの管理情報を RODM に投入し、ネットワーク自動化およびシステム自動化の基盤として利用する。「{T}」はこの RODM の中核概念に関する項目である。")
        vq, ch, ans, ex = ("RODM データ・キャッシュが置かれる場所はどこか。",
            ["DASD 上の VSAM データ・セット","ホスト・プロセッサのメモリ（in-storage）","結合ファシリティ（CF）構造","リモート・データベース・サーバー"],1,
            "RODM はホスト・メモリ上の in-storage データ・キャッシュである（Users Guide / Automation Guide）。")
        verify = ["NetView コンソールで RODM アドレス空間が稼働中か確認する。","DSIQTSK 経由で対象 RODM が管理対象に定義されていることを CNMSTYLE で確認。",
                  "RODMVIEW コマンドを発行し、データ・キャッシュ内のクラス／オブジェクトが参照できることを確認。","オブジェクト数や代表クラスを照会し、想定どおりの内容が存在することを確認する。"]
        rag = RAG['rodm']
    elif cl == 'bldviews':
        naiyou = (f"BLDVIEWS は新規ビュー／集約（aggregate）の作成や既存ビュー／集約の更新に用いる REXX exec である。GMFHS・SNA トポロジー・マネージャー・"
                  f"MultiSystem Manager の各データ・モデルのオブジェクトと連携し、GMFHS クラス上に資源を作成できる（ただしこれらの他クラス上にはオブジェクトを作成しない）。"
                  f"制御文は DSIPARM メンバーや完全修飾の順次データ・セットで渡す。BLDVIEWS の処理は静的で、実行時点で RODM に存在した資源のみを対象とするため、"
                  f"資源が後から追加・削除された場合は再実行が必要である。「{T}」はこの BLDVIEWS 機能に関する項目である。")
        vq, ch, ans, ex = ("BLDVIEWS で作成したビューの特性として正しいものはどれか。",
            ["RODM 変更に応じて動的に自動更新される","実行時点の RODM 資源のみを対象とする静的なビューである","ローダー・ファイルの一部として保存される","コールド・スタート後も自動的に再構築される"],1,
            "BLDVIEWS の処理は静的で、実行時に存在した資源のみ対象。変更反映には再実行が必要（p.579）。")
        verify = ["NetView コマンド行で制御文メンバーを用意（例: 順次データ・セット ESP.GAF.DATA(MYDEFS)）。","BLDVIEWS MYMEMBER を実行する。",
                  "TEST=YES を指定して構文チェックのみ行い、エラーがないことを確認。","本実行後、NetView 管理コンソールで生成されたビュー／集約が表示されることを確認する。"]
        rag = RAG['bldviews']
    elif cl == 'method':
        naiyou = (f"RODM メソッドは RODM データ・キャッシュ内のフィールド値の照会・変更時にトリガーされるユーザー作成プログラムである。"
                  f"query メソッドはフィールド照会時に、change メソッドは変更時にトリガーされ（サブフィールド変更ではトリガーされない）、フィルタリングやポリシー検証を行える。"
                  f"メソッドにはオブジェクト固有（query/change/notify/named）とオブジェクト独立があり、メソッド API は RODM データとサービスへのエントリー・ポイントを提供し、"
                  f"トランザクション情報ブロック・関数ブロック・応答ブロックを受け渡す。「{T}」はこの RODM メソッド機能に関する項目である。")
        vq, ch, ans, ex = ("フィールドの値を変更したときにトリガーされる RODM メソッドはどれか。",
            ["query メソッド","change メソッド","notify メソッドのみ","どのメソッドもトリガーされない"],1,
            "フィールド値の変更で change メソッドがトリガーされる。サブフィールド変更では起動しない（p.34）。")
        verify = ["RODMVIEW を起動し対象オブジェクト／フィールドを表示する。","対象フィールドに change サブフィールドでメソッドが定義されていることを確認。",
                  "EKG_ChangeField でフィールド値を変更し change メソッドが起動することを RODM ログ（UAPI トレース）で確認。","戻りコード／理由コードが 0 で正常終了することを確認する。"]
        rag = RAG['method']
    elif cl == 'layout':
        naiyou = (f"ビュー・レイアウト・ファシリティは、ネットワーク・モデルの視覚的解釈を容易にするため複数のレイアウト・タイプを生成する。"
                  f"提供されるレイアウトにはリンク／クラスター ID 別の放射状（radial）、トークンリング、LAN、楕円（elliptical）、階層（hierarchical）、"
                  f"接続ツリー（connectivity tree）、グリッド（grid）などがある。各ノードの LayoutType フィールドでレイアウト種別を指定し、LayoutSequence で配置順序を制御する。"
                  f"「{T}」はこのビュー・レイアウト機能に関する項目である。")
        vq, ch, ans, ex = ("ビューのレイアウト種別を指定する GMFHS フィールドはどれか。",
            ["LayoutSequence","LayoutType","DisplayStatus","Correlater"],1,
            "LayoutType フィールドにレイアウト種別を設定する（例: トークンリングは値 4）。LayoutSequence は配置順序（p.678 / DM Ref p.201）。")
        verify = ["RODMVIEW で対象ビュー・オブジェクトを表示する。","LayoutType フィールドに目的のレイアウト値を設定する（例: トークンリング=4）。",
                  "必要に応じ各ノードの LayoutSequence を設定（既定 0）。","NetView 管理コンソールでビューを開き、指定どおりのレイアウトで描画されることを確認する。"]
        rag = RAG['layout']
    elif cl == 'load':
        naiyou = (f"RODM ロード機能は、ロード機能入力ファイル（高水準ステートメントとプリミティブ・ステートメント）を処理して RODM データ・キャッシュを"
                  f"ロード・更新・検証する。提供される操作は PARSE（構文チェックのみ）、LOAD（データ・キャッシュへ反映）、VERIFY（変更せず内容と突合）の 3 種で、OPERATION パラメーターで指定する。"
                  f"高水準ステートメントは内部でプリミティブに変換され、クラス・オブジェクト・フィールド・サブフィールドの作成／削除、親子関係の確立、フィールド値設定、メソッド起動を行う。"
                  f"「{T}」はこの RODM ロード機能に関する項目である。")
        vq, ch, ans, ex = ("構文だけを検査しデータ・キャッシュを変更しない RODM ロード操作はどれか。",
            ["LOAD","PARSE","CHECKPOINT","UNLOAD"],1,
            "OPERATION=PARSE は構文を検査するのみでキャッシュを変更しない。VERIFY は内容と突合、LOAD で反映（p.268）。")
        verify = ["ロード機能入力データ・セット（高水準／プリミティブ文）を用意する。","OPERATION=PARSE で実行し構文エラーがないことを出力リストで確認。",
                  "OPERATION=LOAD で実行し RODM データ・キャッシュへ反映する。","出力リストで戻りコードを確認し、RODMVIEW で作成されたクラス／オブジェクトを検証する。"]
        rag = RAG['load']
    elif cl == 'rodmview':
        naiyou = (f"RODMView は RODM データ・キャッシュ内フィールド値の参照・更新を行うアプリケーション・プログラムで、NetView の OST タスク配下で稼働する。"
                  f"NetView コマンド行で rodmview を入力するとメイン・メニューが表示され、メイン・メニューやアクセラレーター PF キーでナビゲートできる。"
                  f"RODMView コマンドでメソッドのトリガー（オブジェクト独立またはオブジェクト固有の named メソッド）や、クラス・オブジェクト・フィールド値の追加・変更・削除が可能である。"
                  f"「{T}」はこの RODMView に関する項目である。")
        vq, ch, ans, ex = ("RODMView を起動する操作はどれか。",
            ["管理コンソールで右クリック・メニューを開く","NetView コマンド行で rodmview と入力し Enter","FLCARODM コマンドを発行する","BLDVIEWS exec を実行する"],1,
            "NetView コマンド・ファシリティの行に rodmview と入力するとメイン・メニューが表示される（Users Guide p.151）。")
        verify = ["NetView コンソールにログオンする。","コマンド行で rodmview と入力し Enter キーを押す。",
                  "RODMView メイン・メニューが表示されることを確認し、対象クラス／オブジェクトへナビゲートする。","フィールド値を参照し、必要に応じ更新後に値が反映されることを確認する。"]
        rag = RAG['rodmview']
    elif cl == 'corr':
        naiyou = (f"トポロジー・オブジェクト相関（correlation）機能は、IP・オープン・トポロジーなど異なるトポロジー機能が管理する資源を自動的に関連付ける。"
                  f"相関集約オブジェクトにより、NetView 管理コンソール・オペレーターは相関資源間のナビゲートや統合データの参照ができる。"
                  f"相関機能のすべてのカスタマイズは FLCSDM8 RODM ロード・ファイルで行い、ロード後に有効になる。RODMVIEW で設定した相関値は RODM 再生成までしか保持されないため、"
                  f"CLIST や BLDVIEWS スクリプトで Correlater フィールドを設定すれば再実行で復元できる。「{T}」はこの相関機能に関する項目である。")
        vq, ch, ans, ex = ("相関機能のカスタマイズに使用する RODM ロード・ファイルはどれか。",
            ["FLCSDM8","EKGCTABL","DSIPARM","CNMSTYLE"],0,
            "相関機能のカスタマイズは FLCSDM8 RODM ロード・ファイルで行い、ロード後に有効になる（p.334）。")
        verify = ["FLCSDM8 RODM ロード・ファイルで相関対象クラスをカスタマイズする。","RODM ロード機能で FLCSDM8 をロードする。",
                  "RODMVIEW または BLDVIEWS で対象オブジェクトの Correlater フィールドに相関値を設定。","NetView 管理コンソールで相関資源間をナビゲートし統合データが表示されることを確認する。"]
        rag = RAG['corr']
    elif cl == 'flcarodm':
        naiyou = (f"FLCARODM は RODM ツールの一つで、RODM データ・キャッシュに対する照会・更新を行うコマンド・インターフェースを提供する。"
                  f"RODM アンロード・ユーティリティはデータ・キャッシュの内容を RODM ローダー言語ステートメントとして出力し、後で再ロードできる（チェックポイントとは異なり、"
                  f"チェックポイントは再始動用のバイナリ表現である）。FLCARODM は戻りコード・理由コードで処理結果を返す。「{T}」はこの RODM ツール（FLCARODM／アンロード）に関する項目である。")
        vq, ch, ans, ex = ("RODM アンロード・ユーティリティの出力形式として正しいものはどれか。",
            ["バイナリのチェックポイント・データ・セット","再ロード可能な RODM ローダー言語ステートメント","SMF レコード","管理コンソールの XML 定義"],1,
            "アンロード・ユーティリティは内容を RODM ローダー言語文として出力し再ロードできる。チェックポイントはバイナリ表現（Graphical Components p.64）。")
        verify = ["RODM が稼働中であることを確認する。","RODM アンロード機能を実行し、データ・キャッシュ内容をローダー言語ステートメントとして出力。",
                  "出力データ・セットにローダー文が生成されたことを確認。","FLCARODM の戻りコード／理由コードが正常（0）であることを確認する。"]
        rag = RAG['flcarodm']
    elif cl == 'alert':
        naiyou = (f"GMFHS は非 SNA 資源の状況および SNA 資源の alert-received（イベント通知）ユーザー状況を、アラートや解決（resolution）を受信して監視する。"
                  f"GMFHS のカスタマイズでは、RODM に作成するオブジェクト名をアラートが提供する資源名と一致させる必要がある。DUIFEDEF フィードバック・インディケーターが"
                  f"複数の非 SNA 資源名を示す場合、GMFHS は返されたクラス内で各名前のオブジェクトを探し、DUIFEDEF が返す DisplayStatus（または状況マッピング・テーブル）で表示状況を決定する。"
                  f"「{T}」はこのアラート／解決の処理に関する項目である。")
        vq, ch, ans, ex = ("GMFHS のアラート処理を正しく機能させるための前提はどれか。",
            ["管理コンソールを管理者でサインオンする","RODM に作成するオブジェクト名をアラートの資源名と一致させる","LayoutType を 4 に設定する","チェックポイントを毎時取得する"],1,
            "RODM オブジェクト名をアラートが提供する資源名と一致させる必要がある（p.173）。")
        verify = ["GMFHS が稼働中であることを確認する。","アラートの資源名と一致する名前で RODM にオブジェクトを作成する。",
                  "対象資源のアラート／解決を発生させ、GMFHS が受信・処理することを確認。","NetView 管理コンソールで対象オブジェクトの DisplayStatus が更新されることを確認する。"]
        rag = RAG['alert']
    elif cl == 'platform':
        naiyou = (f"RODM Collection Manager は RODM の内容を能動的に監視し、指定した条件に従ってビューや集約を動的に更新する NetView 機能である。"
                  f"BLDVIEWS の静的なビューと異なり、コレクションの追加・変更・削除に追随して継続的に更新されるため、名前や状況を超えた複雑な条件でビューを管理できる。"
                  f"NetView 管理コンソールから利用するには管理者としてサインオンする必要がある。NetView Resource Manager のサンプル・ローダー・ファイル（CNMSJH12 等）が提供される。"
                  f"「{T}」はこの RODM 自動化プラットフォーム／コレクション・マネージャー領域に属する項目である。")
        vq, ch, ans, ex = ("RODM Collection Manager と BLDVIEWS のビュー管理の違いはどれか。",
            ["Collection Manager は静的、BLDVIEWS は動的","Collection Manager は動的に継続更新、BLDVIEWS は静的","両者とも完全に静的","両者とも完全に動的"],1,
            "Collection Manager は RODM 内容を監視して動的に更新する。BLDVIEWS は静的（p.578 / NMC p.77）。")
        verify = ["NetView 管理コンソールに管理者としてサインオンする。","RODM Collection Manager メイン・メニューを開く。",
                  "コレクション定義オブジェクトに基づくビュー／集約を作成する。","RODM 内容を変更し、Collection Manager がビューを自動更新することを確認する。"]
        rag = RAG['platform']
    elif cl == 'nonsna':
        naiyou = (f"非 SNA ネットワークの資源は RODM データ・キャッシュ内のオブジェクトとして表現される。作成できるオブジェクトには管理オブジェクト（management object）と"
                  f"被管理オブジェクト（managed object）があり、GMFHS と NetView 管理コンソールがこれらを用いて非 SNA 資源を管理する。"
                  f"SNA 資源は SNA トポロジー・マネージャーを使ってサブエリア／APPN ネットワーク管理として扱われ、ビューには状況と構成の両方が含まれる。"
                  f"「{T}」はこの非 SNA／SNA 資源の NetView への定義に関する項目である。")
        vq, ch, ans, ex = ("非 SNA ネットワーク資源は RODM 内で何として表現されるか。",
            ["VTAM メジャー・ノード","RODM データ・キャッシュ内のオブジェクト","SMF レコード","JCL ステートメント"],1,
            "非 SNA 資源は RODM データ・キャッシュ内のオブジェクト（管理／被管理オブジェクト）として表現される（p.30）。")
        verify = ["RODM ロード機能で非 SNA 資源を表すオブジェクトを定義・ロードする。","RODMVIEW で被管理オブジェクト／管理オブジェクトが作成されたことを確認。",
                  "GMFHS／管理コンソールでこれらの資源がビューに表示されることを確認。","資源を選択しコマンド発行と状況表示が機能することを確認する。"]
        rag = RAG['nonsna']
    elif cl == 'notify':
        naiyou = (f"RODM 通知（notification）プロセスは、フィールド値が変化したときに登録済みユーザー・アプリケーションへ通知する仕組みで、setup・wait・notification・cleanup の"
                  f"4 段階から成る。notify サブフィールドは通知サブスクリプションのリストを保持し、オブジェクト単位だけでなくクラス単位の通知も定義できる（クラスのフィールド変更時に起動）。"
                  f"オブジェクト削除通知では setup が通常と異なり、notify サブフィールド作成・通知メソッド導入・フィールド・サブスクライブを行わない。"
                  f"通知メソッドは自動化タスクに特に有用である。「{T}」はこの RODM 通知に関する項目である。")
        vq, ch, ans, ex = ("RODM 通知メソッドがトリガーされるのはどのタイミングか。",
            ["フィールドが照会されたとき","フィールドの値が変化したとき","RODM が起動したとき","チェックポイント取得時"],1,
            "通知メソッドはフィールドの値が変化したときにトリガーされ、ユーザー・アプリケーションへ変更を通知する（p.32）。")
        verify = ["RODMVIEW で対象フィールドに notify サブフィールドを作成し通知メソッドを導入する。","EKG_AddNotifySubscription でサブスクリプションを登録する。",
                  "通知キューと ECB を作成し wait 状態にする。","対象フィールドを変更し、登録アプリケーションに通知が届くことを確認する。"]
        rag = RAG['notify']
    else:  # api
        naiyou = (f"RODM ユーザー API（EKGUAPI）を介してアプリケーションはデータ・キャッシュへアクセスする。各呼び出しではアクセス制御ブロックを参照／定義し、"
                  f"Connect 後に発行する後続の API 呼び出しを認証する。複数アプリケーションが同時に RODM にアクセスでき、access ブロックの sign_on_token でユーザーを識別する。"
                  f"RODM はユーザーの許可レベルを検証し、各関数は特定の許可を要求する。エラー時は戻りコード（例: 8）と理由コードをトランザクション情報ブロックに返し、RODM ログに記録される。"
                  f"「{T}」はこの RODM プログラミング・インターフェース／戻りコード領域に属する項目である。")
        vq, ch, ans, ex = ("RODM が API 呼び出しでユーザーを識別するために使用するものはどれか。",
            ["JCL の USER パラメーター","アクセス・ブロックの sign_on_token フィールド","データ・セット名","LayoutType フィールド"],1,
            "access ブロックの sign_on_token フィールドで各トランザクションのユーザーを識別する（p.308）。")
        verify = ["アプリケーションからアクセス制御ブロックを定義し EKGUAPI で RODM へ Connect する。","sign_on_token で識別されることと、RODM が許可レベルを検証することを確認。",
                  "API 関数（照会／変更）を発行し、戻りコード／理由コードを確認する。","エラー時は RODM ログの非ゼロ戻りコード・理由コード（例: RC8 RSN127=未許可）で原因を特定する。"]
        rag = RAG['api']
    return naiyou, verify, {"q": vq, "choices": ch, "answer": ans, "explanation": ex}, rag

out_rows = []
for r in rows:
    cl = cluster(r['title'])
    naiyou, verify, quiz, rag = make(r['title'], cl, r['src'])
    out_rows.append({
        "row_id": r['row_id'], "title": r['title'],
        "naiyou_jp": naiyou, "verify_steps": verify, "quiz": quiz,
        "source": GUIDE, "rag_hit": rag
    })

result = {"page":"g032","product":"IBM NetView 6.4","total_rows":len(rows),
          "target_rows":len(rows),"fixed_count":len(out_rows),"rows":out_rows}
json.dump(result, open(r'C:\kvba\zos-atoms-site\_phase2_outputs\g032_fixed.json','w',encoding='utf-8'),
          ensure_ascii=False, indent=2)

# cluster distribution report
from collections import Counter
c = Counter(cluster(r['title']) for r in rows)
print("clusters:", dict(c))
print("total fixed:", len(out_rows))
