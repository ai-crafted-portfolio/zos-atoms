# -*- coding: utf-8 -*-
import json, os

PDF = "GDPS_SG24-8241_Active-Active_Overview_and_Planning.pdf"

def src(p):
    return f"{PDF} p.{p}"

rows = []

def add(rid, title, p, naiyou, steps, q, choices, ans, expl, rag):
    rows.append({
        "row_id": rid,
        "title": title,
        "naiyou_jp": naiyou,
        "verify_steps": steps,
        "quiz": {"q": q, "choices": choices, "answer": ans, "explanation": expl},
        "source": src(p),
        "rag_hit": rag,
    })

# 11689
add("11689","Active/Active site configuration options",26,
 "GDPS Active/Active 構成には、ワークロード単位で選択できる2つのサイト構成オプションがある。Active/Standby では、あるワークロード内のトランザクションはすべて静的に一方のサイトへルーティングされ、ワークロード障害時にもう一方のサイトへフェイルオーバーする。Active/Query では参照系ワークロードを両サイトへ同時にルーティングでき、レプリケーション遅延などの環境要因を考慮したポリシーにもとづいて分散される。これらの種別は CONFIG パラメーターで決定される。",
 "ステップ1: GDPS の Web インターフェースにログオンし、メニューバーから Workload Management を選択する。\nステップ2: 表示されたワークロード一覧で各ワークロードの種別（Active/Standby または Active/Query）を確認する。\nステップ3: NetView コンソールで `D A,L` 相当の状況表示を行い、対象 LPAR で Lifeline Agent が稼働していることを確認する。\n期待結果: 各ワークロードが構成どおり Active/Standby か Active/Query のいずれかとして表示され、ルーティング先サイトが意図どおりであること。",
 "GDPS Active/Active の Active/Query 構成の特徴として正しいものはどれか。",
 ["更新系トランザクションを両サイトへ同時にルーティングする","参照系ワークロードを両サイトへ同時にルーティングできる","レプリケーションを行わず単一サイトのみで稼働する","常に手動でのみサイト切替が可能で自動分散はしない"],
 1,
 "Active/Query 構成では参照（クエリー）系ワークロードを両サイトへ同時にルーティングでき、レプリケーション遅延などのポリシーに従って分散される。更新系は Active/Standby として静的にルーティングされる。",
 "p.26 Active/Active site configuration options（Active/Standby と Active/Query の2種別、CONFIG パラメーターで決定）")

# 11690
add("11690","Active/Active sites concept",20,
 "Active/Active sites の概念では、一方のサイトがトランザクションを実際に処理し、もう一方のサイトはスタンバイとして待機する。スタンバイサイトは LPAR、システム、ミドルウェアなどのインフラ構成要素とアプリケーションをすべて備え、いつでも処理を引き受けられる状態に保たれる。Active/Query ワークロードは顧客ポリシーと現在のレプリケーション遅延にもとづいて両サイト間で分散できる。",
 "ステップ1: GDPS Web インターフェースでサイト（Sites）ウィンドウを開き、両サイトの稼働状況を確認する。\nステップ2: スタンバイサイト側 LPAR で `D M=CPU` などにより必要なインフラ（システム・ミドルウェア）が起動済みであることを確認する。\nステップ3: レプリケーション状況を Replication ウィンドウで確認し、スタンバイサイトのデータが最新に追随していることを確認する。\n期待結果: スタンバイサイトが処理引き受け可能な状態（インフラ稼働かつレプリケーション追随中）であること。",
 "Active/Active sites 概念におけるスタンバイサイトの状態として正しいものはどれか。",
 ["インフラを停止しており起動に数時間を要する","LPAR・ミドルウェア等を備え処理を引き受けられる状態にある","データを一切保持していない","本番サイトと物理的に同一筐体である"],
 1,
 "スタンバイサイトは LPAR・システム・ミドルウェア・アプリケーションをすべて備え、レプリケーションでデータを追随させており、いつでも処理を引き受けられる状態に保たれる。",
 "p.20 standby site has all of the infrastructure components (LPARs, systems, middleware) ready to receive work")

# 11691
add("11691","Active/Standby or Active/Query Configuration",91,
 "Active/Standby と Active/Query の構成選択は、参照系ワークロードを両サイトで動かすかどうかに関わる。Active/Query を採用すると、アクティブサイトの Active/Standby ワークロードへの性能影響を抑えつつ、スタンバイサイトの CPU リソースを有効活用できる。ただし、スタンバイサイト上のクエリーワークロードがレプリケーション遅延を許容できることを確認する必要がある。",
 "ステップ1: GDPS Web インターフェースの Workload Management ウィンドウで、対象ワークロードの構成種別を確認する。\nステップ2: スタンバイサイトの CPU 使用率を `D M` や RMF で確認し、クエリーワークロードによる利用状況を把握する。\nステップ3: Replication ウィンドウで現在のレプリケーション遅延（latency）を確認し、クエリー結果が許容範囲内のデータ鮮度であることを検証する。\n期待結果: クエリーワークロードがスタンバイサイトで稼働し、遅延が業務上許容できる範囲に収まっていること。",
 "Active/Query 構成を採用する主な利点はどれか。",
 ["スタンバイサイトの CPU リソースを参照系で有効活用できる","レプリケーション遅延を完全に排除できる","本番サイトを停止できる","データ整合性チェックが不要になる"],
 0,
 "Active/Query は、スタンバイサイト側の CPU を参照系ワークロードで活用しつつ、アクティブサイトの性能影響を抑えられる。ただしクエリー側はレプリケーション遅延を許容できる必要がある。",
 "p.91 run some query workloads on both sites to fully use CPU resource on the standby site")

# 11693
add("11693","Application Middleware for IBM GDPS Active/Active",67,
 "GDPS Active/Active が必要とするアプリケーションミドルウェアは表 5-1 に一覧されている。VSAM レプリケーションを Active/Active ワークロードで使用する場合には、CICS TS と CICS VR が必須となる。これらのミドルウェアは、ワークロードを処理するアプリケーションサービスを提供する基盤であり、両サイトで同等に構成しておく必要がある。",
 "ステップ1: 各本番 LPAR で必要なミドルウェア（CICS TS、Db2、IMS、CICS VR 等）が稼働していることを `D A,L` などで確認する。\nステップ2: VSAM レプリケーションを使うワークロードについて、CICS VR が両サイトで導入・稼働済みであることを確認する。\nステップ3: GDPS Web インターフェースでミドルウェア関連コンポーネントの状態が正常であることを確認する。\n期待結果: 構成上必要なミドルウェアがすべて両サイトで稼働し、VSAM 利用時には CICS TS/CICS VR が揃っていること。",
 "VSAM レプリケーションを Active/Active ワークロードで使用する際に必須となるミドルウェアはどれか。",
 ["IMS のみ","Db2 のみ","CICS TS と CICS VR","WebSphere MQ のみ"],
 2,
 "表 5-1 では、VSAM レプリケーションを A-A ワークロードで使う場合に CICS TS と CICS VR が必須とされている。",
 "p.67 5.6.1 Application Middleware; CICS TS and CICS VR are required when using VSAM replication")

# 11698
add("11698","Benefits of using GDPS Active/Active",21,
 "GDPS Active/Active ソリューションは、重要な業務アプリケーションに対して継続的可用性（continuous availability）を提供する。同時に、代替サイト上のシステムリソースとほぼリアルタイムの本番データを、ワークロードバランシングや大量のリアルタイムデータを扱うデータ分析ワークロードに活用できる。これにより、可用性向上とリソース有効活用を両立できる。",
 "ステップ1: GDPS Web インターフェースで両サイトのワークロード状況を確認し、継続的可用性が維持されていることを確認する。\nステップ2: 代替（スタンバイ）サイトで分析系・参照系ワークロードが稼働しリソースを活用していることを確認する。\nステップ3: 計画切替（Planned Action）を1ワークロードに対して試験実施し、業務を止めずに切り替わることを観察する。\n期待結果: クリティカルアプリが継続提供されつつ、代替サイトのリソースが有効活用されていること。",
 "GDPS Active/Active が提供する主な価値として正しいものはどれか。",
 ["バッチ処理時間の短縮のみ","クリティカルアプリの継続的可用性と代替サイトのリソース活用","ストレージ容量の自動削減","ネットワーク不要化"],
 1,
 "GDPS Active/Active はクリティカル業務に継続的可用性を提供し、同時に代替サイトのリソースとリアルタイムデータをワークロードバランシングや分析に活用できる。",
 "p.21 1.2 Benefits; provides continuous availability and resources on alternate site for workload balancing and analytics")

# 11701
add("11701","Challenges of the batch workload to GDPS Active/Active",107,
 "GDPS Active/Active は主にオンラインワークロードを監視・管理する。バッチワークロードはユーザーが扱い、Active/Active と統合する必要がある。バッチ処理を最も簡単に扱う方法は、Active/Active のワークロード切替やサイト切替の間にバッチが走っていない状態を確保することである。Graceful（計画）切替の際には、GDPS Active/Active スクリプトが関連バッチの停止をユーザーに促す。",
 "ステップ1: 計画切替の前に、対象ワークロードに関連するバッチジョブが実行中でないことを `D JOBS` 等で確認する。\nステップ2: GDPS Web インターフェースで Planned Action（Graceful switch）スクリプトを起動する。\nステップ3: スクリプトが関連バッチ停止を促すプロンプトを出すので、指示に従ってバッチを停止する。\n期待結果: 切替時にバッチが走っておらず、整合性を保ったまま切替が完了すること。",
 "GDPS Active/Active でバッチワークロードを扱う際の基本的な指針はどれか。",
 ["バッチは自動でフェイルオーバーされるため考慮不要","ワークロード/サイト切替中はバッチを走らせないようにする","バッチは常に両サイトで二重実行する","バッチはオンラインと同様に GDPS が完全自動管理する"],
 1,
 "GDPS Active/Active は主にオンラインを管理し、バッチはユーザーが扱う。切替中にバッチが走らないようにするのが基本で、Graceful 切替時はスクリプトがバッチ停止を促す。",
 "p.107 ensure no running batch during workload or site switch; graceful switch prompts user to stop batch")

# 11704
add("11704","Components of the monitoring architecture",62,
 "GDPS Active/Active の監視アーキテクチャは、NetView Monitoring for GDPS を中核に、ワークロードとレプリケーション状況、サイトのヘルスチェック、ソフトウェアレプリケーション性能、ルーティング判断などを監視する。監視は両 Active/Active サイトにまたがり、検出した例外をアラートする。これらの監視情報は表示やシチュエーション起動のために IBM Tivoli Monitoring へ転送される。",
 "ステップ1: NetView コンソールで GDPS Monitoring 関連タスクが稼働していることを確認する。\nステップ2: IBM Tivoli Monitoring（TEP）にログオンし、GDPS Active/Active のワークロード・レプリケーション状況ビューが表示されることを確認する。\nステップ3: 意図的にしきい値を超える状況を試験的に作り、アラート（シチュエーション）が発報されることを確認する。\n期待結果: 監視情報が NetView から Tivoli Monitoring へ転送され、例外がアラートとして表示されること。",
 "GDPS Active/Active の監視情報は最終的にどこへ転送されて表示されるか。",
 ["DS8000 ストレージのコンソール","IBM Tivoli Monitoring（Tivoli Enterprise Portal）","z/OS の SYSLOG のみ","外部ロードバランサーのログ"],
 1,
 "NetView Monitoring for GDPS が収集した監視情報は、表示やシチュエーション起動のために IBM Tivoli Monitoring（TEP）へ転送される。",
 "p.62 monitoring spans Active/Active sites; information forwarded to IBM Tivoli Monitoring for display")

# 11708
add("11708","Decide on an Active/Standby or Active/Query configuration",94,
 "ワークロード識別の一環として、各 Active/Active ワークロードを Active/Standby と Active/Query のどちらの構成にするかを決定する。更新系トランザクションは Active/Standby として一方のサイトへ静的にルーティングし、参照系は Active/Query として両サイトへ分散できる。決定にあたっては、ワークロードの更新有無、レプリケーション遅延の許容度、リソース活用の目的を考慮する。",
 "ステップ1: 対象ワークロードが更新系か参照系かを業務要件から整理する。\nステップ2: 参照系であればレプリケーション遅延の許容度を確認し、Active/Query 適用可否を判断する。\nステップ3: GDPS の構成（CONFIG パラメーター）に決定した種別を反映し、Workload Management ウィンドウで表示を確認する。\n期待結果: 各ワークロードが業務要件に合った Active/Standby または Active/Query として構成されていること。",
 "Active/Standby と Active/Query の選択判断で最も重視すべき観点はどれか。",
 ["ワークロードが更新系か参照系か（およびレプリケーション遅延の許容度）","使用するメインフレームの機種","ネットワークケーブルの色","バッチジョブの本数のみ"],
 0,
 "更新系は Active/Standby、参照系は Active/Query に向く。Active/Query 採否はレプリケーション遅延の許容度に依存するため、更新有無と遅延許容度が判断の中心となる。",
 "p.94 identify workloads and decide on Active/Standby or Active/Query configuration")

# 11711
add("11711","Evolution of GDPS Active/Active solution",18,
 "GDPS Active/Active ソリューションは、ストレージベースのレプリケーションに依存する従来の GDPS から、ソフトウェアベースの非同期レプリケーションへと進化したものである。これは障害発生時に長い回復時間を要するフェイルオーバーモデルから、ほぼ継続的な可用性モデルへのパラダイムシフトである。複数サイトを無制限の距離で結び、同一アプリケーションと同一データを稼働させることでクロスサイトのワークロードバランシングと災害対策を実現する。",
 "ステップ1: 既存の GDPS 構成（ストレージベース）と Active/Active 構成の違いをドキュメントで整理する。\nステップ2: GDPS Web インターフェースで Active/Active のレプリケーション（ソフトウェア非同期）状況を確認する。\nステップ3: 計画切替を試行し、フェイルオーバー型と比較して回復時間（RTO）が秒オーダーに短縮されていることを確認する。\n期待結果: ソフトウェア非同期レプリケーションにより、ほぼ継続的可用性が実現できていること。",
 "GDPS Active/Active が従来の GDPS から進化した点として正しいものはどれか。",
 ["ストレージベース同期レプリケーションへの回帰","フェイルオーバーモデルからほぼ継続的可用性モデルへの転換","単一サイト運用への単純化","テープバックアップ中心への移行"],
 1,
 "GDPS Active/Active はストレージベースのフェイルオーバーモデルから、ソフトウェア非同期レプリケーションによるほぼ継続的可用性モデルへのパラダイムシフトである。",
 "p.18 evolution; paradigm shift from failover model to near continuous availability using software replication")

# 11713
add("11713","GDPS Active/Active co-operation with GDPS/PPRC",104,
 "すでに GDPS/PPRC をデータレプリケーションとシステム管理に使用している（または使用予定の）Active/Active sysplex 環境では、いくつかの考慮事項がある。これらは LOAD や STOP といった Standard Action のシステム管理機能を、どこでどのように実行するかに関わる。GDPS Active/Active と GDPS/PPRC を協調させることで、両方の管理機能を整合的に運用できる。",
 "ステップ1: GDPS/PPRC が管理する sysplex 構成と Active/Active 構成の重なりを確認する。\nステップ2: GDPS Standard Actions（LOAD、STOP 等）が GDPS/PPRC と Active/Active のどちらから発行されるべきか運用ルールを確認する。\nステップ3: テスト環境で LOAD/STOP を実行し、両 GDPS 間で競合せず協調動作することを確認する。\n期待結果: GDPS/PPRC 協調サポートが確立され、システム管理機能が整合的に動作すること。",
 "GDPS Active/Active と GDPS/PPRC の協調で主に整理が必要な機能はどれか。",
 ["LOAD や STOP などの Standard Action（システム管理機能）","ストレージ容量課金","ネットワーク帯域の暗号化","TEP の画面配色"],
 0,
 "GDPS/PPRC と Active/Active が重なる環境では、LOAD/STOP などの Standard Action をどこでどう実行するかの協調が重要になる。",
 "p.104 considerations associated with where and how systems management functions such as LOAD and STOP run")

# 11714
add("11714","GDPS Active/Active integration with GDPS/MGM",105,
 "GDPS Active/Active は、GDPS/MGM（Metro Global Mirror）などのディスクベースレプリケーションソリューションと制御された統合をサポートする。本番 sysplex 内で Active/Active と非 Active/Active の両ワークロードを稼働させる場合に、GDPS/MGM をデータ管理に利用できる。なお、GDPS Active/Active と GDPS/MGM を統合する際には、GDPS/PPRC 協調サポートも併せて確立しておく必要がある。",
 "ステップ1: GDPS/MGM が管理するディスクレプリケーション構成を確認する。\nステップ2: 本番 sysplex 内の Active/Active ワークロードと非 Active/Active ワークロードの分担を整理する。\nステップ3: GDPS/PPRC 協調サポートが確立されていることを確認し、MGM 統合時の整合性を検証する。\n期待結果: Active/Active と GDPS/MGM が制御された形で統合され、PPRC 協調も併せて確立されていること。",
 "GDPS Active/Active と GDPS/MGM を統合する際に併せて確立すべきものはどれか。",
 ["GDPS/PPRC 協調サポート","新しいテープライブラリ","外部 DNS サーバー","追加の TEP ライセンスのみ"],
 0,
 "GDPS Active/Active と GDPS/MGM 統合時には、GDPS/PPRC 協調サポートも併せて確立する必要があるとされている。",
 "p.105/106 controlled integration with GDPS/MGM; ensure GDPS/PPRC cooperation support is also established")

# 11715
add("11715","GDPS Active/Active monitoring and alerting",80,
 "GDPS Active/Active の監視・アラート機能は、ワークロードやレプリケーションの状態、サイトのヘルスを継続的に監視し、検出した例外を通知する。監視情報は Tivoli Enterprise Portal を通じて参照でき、ロードバランサー、レプリケーションサーバー、Workload Lifeline Advisor、ワークロードといった構成要素の詳細にドリルダウンできる。これにより運用者は環境全体の健全性を一目で把握できる。",
 "ステップ1: Tivoli Enterprise Portal を起動し、GDPS Active/Active のサマリービューを表示する。\nステップ2: ロードバランサー、レプリケーションサーバー、Lifeline Advisor、ワークロードへドリルダウンし詳細状態を確認する。\nステップ3: 例外状態を試験的に発生させ、アラートが発報・表示されることを確認する。\n期待結果: 各構成要素の状態が監視され、例外がアラートとして通知・表示されること。",
 "GDPS Active/Active の監視ビューからドリルダウンできる対象として正しいものはどれか。",
 ["ロードバランサー・レプリケーションサーバー・Lifeline Advisor・ワークロード","CPU マイクロコードのみ","テープ媒体のシリアル番号のみ","電源装置の温度のみ"],
 0,
 "Tivoli Enterprise Portal から、ロードバランサー、レプリケーションサーバー、Workload Lifeline Advisor、ワークロードの詳細へドリルダウンできる。",
 "p.78/80 drill down to Load Balancers, Replication Servers, Workload Lifeline Advisors, and Workloads")

# 11717
add("11717","GDPS Active/Active site switch of workloads",99,
 "GDPS Active/Active のサイト切替は、あるサイトで稼働中のワークロードを別サイトへ移行する操作である。計画的（Graceful）な切替では、関連するバッチ停止やルーティング変更を伴い、業務を極力止めずに移行する。切替は GDPS のスクリプト（Planned Action）として実行され、Lifeline によるルーティング更新と協調して行われる。",
 "ステップ1: GDPS Web インターフェースで対象ワークロードの現在のアクティブサイトを確認する。\nステップ2: Planned Action からサイト切替スクリプトを起動し、プロンプトに従って関連バッチを停止する。\nステップ3: 切替後、Workload Management ウィンドウでワークロードが新サイトでアクティブになり、Lifeline がルーティングを更新したことを確認する。\n期待結果: ワークロードが目的サイトへ切り替わり、ルーティングが更新され業務が継続すること。",
 "GDPS Active/Active のサイト切替で、ルーティング更新を担う製品はどれか。",
 ["IBM Multi-site Workload Lifeline","CICS VR","Db2 のみ","RMF"],
 0,
 "サイト切替時のトランザクションルーティング更新は IBM Multi-site Workload Lifeline が担い、GDPS スクリプトと協調して行われる。",
 "p.99 GDPS Active/Active site switch of workloads")

# 11719
add("11719","GDPS Active/Active Workload",26,
 "GDPS Active/Active における「ワークロード」は、特定の業務処理を構成するソフトウェア（ユーザー作成アプリケーションと CICS リージョンや InfoSphere などのミドルウェア実行環境）とそれが扱うデータの集合体（aggregation）として定義される業務関連の概念である。ワークロードは Active/Standby または Active/Query として構成され、サイト切替やルーティングの管理単位となる。",
 "ステップ1: GDPS Web インターフェースの Workload Management ウィンドウで定義済みワークロード一覧を確認する。\nステップ2: 各ワークロードを構成するアプリケーション・ミドルウェア・データの対応を運用ドキュメントと突き合わせる。\nステップ3: 1つのワークロードを単位として切替やルーティング操作が可能なことを確認する。\n期待結果: ワークロードがアプリ・ミドルウェア・データの集合体として正しく定義され、管理単位として機能すること。",
 "GDPS Active/Active における「ワークロード」の定義として正しいものはどれか。",
 ["単一の TCP ポート番号","アプリケーション・ミドルウェア・データの集合体である業務関連の定義","物理ディスク1台","NetView の1コマンド"],
 1,
 "Active/Active ワークロードは、ユーザーアプリケーションとミドルウェア実行環境、扱うデータの集合体として定義される業務関連の概念である。",
 "p.26/90 Active/Active workload is an aggregation of software (applications + middleware) and data")

# 11729
add("11729","How do I contact IBM for GDPS services?",113,
 "GDPS のサービスに関する問い合わせは、IBM Global Technology Services（GTS）組織を通じて行う。付録 A では GTS の概要、GDPS を含むサービス提供、そして GDPS サービスへの問い合わせ方法が説明されている。導入支援やインストールサービス、技術コンサルティングワークショップなどの提供を受ける際の窓口となる。",
 "ステップ1: 付録 A（IBM Global Technology Services and GDPS service offering）の問い合わせ窓口情報を参照する。\nステップ2: 必要なサービス（導入支援、ワークショップ、インストールサービス）を整理する。\nステップ3: IBM の担当者／窓口へ問い合わせ、提供メニューと要件を確認する。\n期待結果: GDPS サービスの問い合わせ先と提供メニューが把握できること。",
 "GDPS のサービスに関する問い合わせ窓口となる IBM の組織はどれか。",
 ["IBM Global Technology Services","IBM Cloud Marketing","IBM Quantum","個々の販売代理店のみ"],
 0,
 "GDPS サービスの問い合わせは IBM Global Technology Services（GTS）を通じて行う。付録 A に窓口情報が記載されている。",
 "p.113 How do I contact IBM for GDPS services?（IBM Global Technology Services）")

# 11730
add("11730","How does IIDR for DB2 work?",37,
 "IIDR for DB2（InfoSphere Data Replication for DB2）は、Q Replication 技術を用いて DB2 のデータを一方のサイトから他方へ非同期にレプリケートする。キャプチャーエンジンがソース DB2 のコミット済みトランザクションデータを捕捉し、トランスポート基盤を経由してターゲット側のアプライエンジンが適用する。GDPS Active/Active 内での DB2 データ同期の中核を担い、詳細設計は SG24-8154 などに記載されている。",
 "ステップ1: ソースおよびターゲットの DB2 サブシステムで IIDR（Q Replication）のキャプチャー／アプライプロセスが稼働していることを確認する。\nステップ2: GDPS の Replication ウィンドウで DB2 ワークロードのレプリケーション遅延（latency）を確認する。\nステップ3: ソース側で更新を行い、ターゲット側へ反映されることを確認する。\n期待結果: DB2 の更新がキャプチャー→トランスポート→アプライの流れでターゲットへ反映されること。",
 "IIDR for DB2 が GDPS Active/Active で用いるレプリケーション技術はどれか。",
 ["同期 PPRC","Q Replication（キャプチャー／アプライ）","テープバックアップ","FlashCopy のみ"],
 1,
 "IIDR for DB2 は Q Replication をベースに、キャプチャーエンジンとアプライエンジンによる非同期ソフトウェアレプリケーションを行う。",
 "p.37 3.2.1 How does IIDR for DB2 work?（Q Replication 参照、SG24-8154）")

# 11731
add("11731","How does IIDR for IMS work?",47,
 "IIDR for IMS は、IMS のデータを一方のシステムから他方へ単方向（unidirectional）に非同期レプリケートする。ソース側でキャプチャー処理が IMS ログの更新レコードを読み取り、ターゲット側ではサブスクリプションごとに用意した apply PSB を用いて変更をターゲットデータベースへ適用する。ターゲットデータの鮮度はソースとターゲット間の遅延に依存し、遅延が小さいほど RPO も小さくなる。",
 "ステップ1: ソース／ターゲットの Classic data server と IMS レプリケーションのキャプチャー／アプライが稼働していることを確認する。\nステップ2: 各サブスクリプションに apply PSB が定義されていることを確認する。\nステップ3: ソース IMS で更新を行い、ターゲットへ反映されることと遅延を確認する。\n期待結果: IMS 更新がログ読み取り→転送→apply PSB 適用の流れでターゲットへ反映されること。",
 "IIDR for IMS がターゲットへ変更を適用する際に各サブスクリプションで必要とするものはどれか。",
 ["apply PSB","FlashCopy リレーション","PPRC ペア","新規 LPAR"],
 0,
 "IIDR for IMS は単方向レプリケーションで、サブスクリプションごとに apply PSB を必要とし、ソースの IMS ログから読み取った更新をターゲットへ適用する。",
 "p.47 IIDR for IMS requires an apply PSB for each subscription; unidirectional")

# 11732
add("11732","How does IIDR for VSAM work?",43,
 "IIDR for VSAM は、システムロガーのログストリームにあるレプリケーションログ（VSAM ソースデータセットへの挿入・更新・削除・コミットのログレコード）を読み取り、ターゲットパーティションで稼働する CICS リージョン経由でターゲット VSAM データセットへ変更を適用する。これにより同期レプリカを維持する。ターゲットデータの鮮度はソースとターゲット間の遅延に依存する。",
 "ステップ1: ソース／ターゲットで CICS VR と IIDR for VSAM のレプリケーションが稼働していることを確認する。\nステップ2: システムロガーのログストリームが構成され、ログレコードが読み取られていることを確認する。\nステップ3: ソース VSAM データセットを更新し、ターゲット CICS リージョン経由で反映されることを確認する。\n期待結果: VSAM 更新がログストリーム読み取り→ターゲット CICS 経由適用の流れで反映されること。",
 "IIDR for VSAM がターゲット VSAM データセットへ変更を適用する経路として正しいものはどれか。",
 ["ターゲットパーティションで稼働する CICS リージョン経由","DS8000 の FlashCopy 経由","テープドライブ経由","TCP ソケットへ直接書き込み"],
 0,
 "IIDR for VSAM はシステムロガーのログストリームからログレコードを読み取り、ターゲット側 CICS リージョン経由でターゲット VSAM データセットへ適用する。",
 "p.43 reads replication logs in system logger log streams; applies via CICS region at target partition")

# 11734
add("11734","IBM GDPS Active/Active Monitor processing during a workload or site failure",68,
 "GDPS Active/Active のモニター処理は、ワークロード障害やサイト障害が発生した際にその状態を検出し、関係コンポーネントへ通知する。GDPS には5分ごとに環境状態をチェックする組み込みモニターがあり、障害検出時にはアラートを発報し、必要に応じて計画外アクション（Unplanned Action）のトリガーとなる。これにより迅速な切替判断が可能になる。",
 "ステップ1: NetView コンソールで GDPS の組み込みモニタータスクが稼働していることを確認する。\nステップ2: テスト環境で対象ワークロードのサーバーアプリケーションをすべて停止し、ワークロード障害を擬似的に発生させる。\nステップ3: GDPS がワークロード障害を検出し、アラートが発報されることを確認する。\n期待結果: ワークロード／サイト障害がモニターにより検出され、アラートが通知されること。",
 "GDPS Active/Active の組み込みモニターが環境状態をチェックする間隔はどれか。",
 ["5分ごと","1時間ごと","1日ごと","リアルタイムに連続（間隔なし）"],
 0,
 "GDPS には5分ごとに環境状態をチェックする組み込みモニターがあり、ワークロード／サイト障害を検出してアラートを発報する。",
 "p.67/68 built-in monitor runs every five minutes; monitor processing during a workload or site failure")

# 11736
add("11736","IBM GDPS Integration",69,
 "IBM Tivoli NetView for z/OS は、すべての IBM GDPS ソリューションの基盤を提供する。GDPS 統合（5.9.2 IBM GDPS Integration）として、NetView は自動化プラットフォーム、ステートマシン構築能力、NetView プログラム間通信、そして Consolidated Audit・NetView・z/OS ログを用いた監査証跡といった機能を提供する。これらが GDPS の制御・監視の土台となる。",
 "ステップ1: NetView が稼働し、GDPS 関連の自動化タスクが起動していることを確認する。\nステップ2: NetView プログラム間通信（RMTCMD 等）が機能していることを確認する。\nステップ3: 監査証跡（Consolidated Audit／NetView／z/OS ログ）に GDPS 操作が記録されることを確認する。\n期待結果: NetView が自動化基盤・通信・監査証跡を提供し、GDPS の制御基盤として機能すること。",
 "IBM Tivoli NetView for z/OS が GDPS に提供する基盤機能として正しいものはどれか。",
 ["自動化プラットフォーム・ステートマシン・プログラム間通信・監査証跡","ディスクの物理フォーマット","ネットワークケーブルの敷設","CPU マイクロコードの更新"],
 0,
 "NetView は全 GDPS の基盤として、自動化プラットフォーム、ステートマシン構築、NetView プログラム間通信、監査証跡を提供する。",
 "p.69 5.9.2 IBM GDPS Integration; NetView provides automation platform, state machine, communication, audit trail")

# 11737
add("11737","IBM Global Technology Services and GDPS service offering",109,
 "付録 A では、IBM Global Technology Services（GTS）組織とその提供内容（GDPS を含むがそれに限らない）について説明している。GTS とは何か、GDPS サービス提供がどのように業務要件に対応するか、IBM への問い合わせ方法といった点を扱う。技術コンサルティングワークショップや GDPS インストールサービスなどが提供される。",
 "ステップ1: 付録 A の構成（GTS の説明、サービス提供、問い合わせ方法）を確認する。\nステップ2: 自組織の業務要件に合致する GDPS サービスメニューを整理する。\nステップ3: GTS の窓口へ問い合わせ、提供範囲と前提条件を確認する。\n期待結果: GTS の GDPS サービス提供内容と自組織要件との対応が把握できること。",
 "IBM Global Technology Services が提供する GDPS 関連サービスに含まれるものはどれか。",
 ["技術コンサルティングワークショップや GDPS インストールサービス","ハードウェアの無償交換のみ","クラウドストレージの提供のみ","通信回線敷設工事のみ"],
 0,
 "GTS は GDPS を含むサービスを提供し、技術コンサルティングワークショップや GDPS インストールサービスなどが含まれる。",
 "p.109 Appendix A. IBM Global Technology Services and GDPS service offering")

# 11738
add("11738","IBM InfoSphere Data Replication for DB2 in GDPS Active/Active",37,
 "IBM InfoSphere Data Replication（IIDR）for DB2 は、GDPS Active/Active 環境で DB2 データを非同期にレプリケートするソフトウェア製品である。Q Replication 技術にもとづき、ソース DB2 のコミット済み変更をキャプチャーし、トランスポート基盤を介してターゲットへ適用する。GDPS Active/Active における DB2 ワークロードのサイト間データ同期を担う。",
 "ステップ1: 両サイトの DB2 で IIDR のキャプチャー／アプライが稼働していることを確認する。\nステップ2: GDPS の Replication ウィンドウで DB2 サブスクリプションの状態と遅延を確認する。\nステップ3: ソース DB2 を更新し、ターゲットへ反映されることを確認する。\n期待結果: IIDR for DB2 が DB2 データを両サイト間で非同期同期していること。",
 "GDPS Active/Active で DB2 のサイト間データ同期を担う製品はどれか。",
 ["IBM InfoSphere Data Replication for DB2","CICS VR","RMF","DFSMShsm"],
 0,
 "IIDR for DB2 は Q Replication ベースのソフトウェアレプリケーションで、GDPS Active/Active の DB2 データをサイト間同期する。",
 "p.37 IBM InfoSphere Data Replication for DB2 in GDPS Active/Active")

# 11739
add("11739","IBM InfoSphere Data Replication for IMS in GDPS/AA",47,
 "IBM InfoSphere Data Replication for IMS は、GDPS Active/Active（GDPS/AA）環境で IMS データを単方向に非同期レプリケートする。ソース側で IMS ログの更新レコードをキャプチャーし、ターゲット側ではサブスクリプションごとの apply PSB を用いて適用する。ターゲットデータの鮮度はレプリケーション遅延に依存し、遅延を抑えることが RPO 低減の鍵となる。",
 "ステップ1: 両サイトの IMS で IIDR（Classic data server、キャプチャー／アプライ）が稼働していることを確認する。\nステップ2: サブスクリプションごとに apply PSB が定義されていることを確認する。\nステップ3: ソース IMS を更新し、ターゲットへ反映される時間（遅延）を確認する。\n期待結果: IIDR for IMS が IMS データを単方向で非同期同期し、遅延が許容範囲であること。",
 "IIDR for IMS のレプリケーション方向の特徴はどれか。",
 ["双方向同期","単方向（unidirectional）","ブロードキャスト型","ストレージ同期のみ"],
 1,
 "IIDR for IMS は単方向（unidirectional）レプリケーションで、サブスクリプションごとに apply PSB を必要とする。",
 "p.47 IIDR for IMS is unidirectional; requires apply PSB per subscription")

# 11740
add("11740","IBM InfoSphere Data Replication for VSAM in GDPS/AA",43,
 "IBM InfoSphere Data Replication for VSAM は、GDPS Active/Active（GDPS/AA）環境で VSAM データをレプリケートする。システムロガーのログストリーム内のレプリケーションログ（挿入・更新・削除・コミットのログレコード）を読み取り、ターゲットパーティションで稼働する CICS リージョン経由でターゲット VSAM データセットへ適用して同期レプリカを維持する。CICS TS／CICS VR が前提となる。",
 "ステップ1: 両サイトで CICS VR と IIDR for VSAM が稼働していることを確認する。\nステップ2: システムロガーのログストリームが構成され、ログレコードが読み取られていることを確認する。\nステップ3: ソース VSAM を更新し、ターゲット CICS リージョン経由で反映されることを確認する。\n期待結果: IIDR for VSAM が VSAM データをサイト間で同期していること。",
 "IIDR for VSAM が読み取るレプリケーションログはどこに置かれるか。",
 ["システムロガーのログストリーム","DS8000 の NVS","テープ媒体","TCP バッファ"],
 0,
 "IIDR for VSAM はシステムロガーのログストリーム内のログレコードを読み取り、ターゲット CICS リージョン経由で VSAM へ適用する。",
 "p.43 reads replication logs in system logger log streams; applies via CICS region")

# 11741
add("11741","IBM Installation Services for GDPS",109,
 "IBM Installation Services for GDPS は、IBM Global Technology Services が提供する GDPS の導入支援サービスである。GDPS の設計・実装・構成にあたって、専門家による導入作業の支援を受けられる。付録 A の GTS サービス提供の一部として位置づけられ、技術コンサルティングワークショップなどと併せて提供される。",
 "ステップ1: 付録 A で IBM Installation Services for GDPS の内容を確認する。\nステップ2: 自組織の GDPS 導入計画と必要な支援範囲を整理する。\nステップ3: GTS 窓口へ問い合わせ、インストールサービスの提供条件を確認する。\n期待結果: GDPS 導入に必要な IBM のインストールサービス内容が把握できること。",
 "IBM Installation Services for GDPS を提供する組織はどれか。",
 ["IBM Global Technology Services","エンドユーザー自身のみ","ハードウェア保守ベンダーのみ","ネットワーク回線業者"],
 0,
 "IBM Installation Services for GDPS は GTS が提供する導入支援サービスで、付録 A のサービス提供の一部である。",
 "p.109 IBM Installation Services for GDPS（Appendix A, IBM Global Technology Services）")

# 11742
add("11742","IBM Multi-site Workload Lifeline for z/OS",25,
 "IBM Multi-site Workload Lifeline for z/OS は、Lifeline Advisor と Lifeline Agent から構成される。Lifeline Advisor はコントローラー上で稼働し、外部ロードバランサーへトランザクション分散先を提供するとともに、GDPS へ Active/Active 環境のヘルス情報を提供する。Lifeline Agent は Active/Active ワークロードが定義された全本番 LPAR で稼働し、ヘルス情報を Advisor へ提供する。",
 "ステップ1: コントローラー上で Lifeline Advisor（Primary）が稼働していることを確認する。\nステップ2: 各本番 LPAR で Lifeline Agent が稼働していることを確認する。\nステップ3: 外部ロードバランサーが Advisor からの分散推奨に従ってルーティングしていることを確認する。\n期待結果: Advisor と Agent が連携し、ロードバランサーへ正しい分散推奨が提供されていること。",
 "IBM Multi-site Workload Lifeline for z/OS を構成する2つのコンポーネントはどれか。",
 ["Lifeline Advisor と Lifeline Agent","Capture と Apply","Master と Slave のディスク","TEMS と TEPS"],
 0,
 "Lifeline は Advisor（コントローラー上、ロードバランサーへ分散情報提供）と Agent（本番 LPAR 上、ヘルス情報提供）から構成される。",
 "p.25 Lifeline consists of Lifeline Advisors and Lifeline Agents")

# 11747
add("11747","IBM Tivoli Monitoring",50,
 "IBM Tivoli Monitoring（ITM）は、GDPS Active/Active の監視情報を表示・分析するための基盤を提供する。Tivoli Enterprise Monitoring Server（hub）、Tivoli Enterprise Portal Server（プレゼンテーション層）、監視エージェントから構成され、NetView Monitoring for GDPS が収集した情報を受け取って表示し、しきい値超過時にはシチュエーションを起動する。NetView エージェントは ITM を必要とする。",
 "ステップ1: TEMS（hub）と TEPS が稼働していることを確認する。\nステップ2: Tivoli Enterprise Portal にログオンし、GDPS Active/Active のビューが表示されることを確認する。\nステップ3: しきい値超過のシチュエーションが定義され、発報することを確認する。\n期待結果: ITM が GDPS の監視情報を表示し、シチュエーションでアラートできること。",
 "GDPS Active/Active の監視データを表示するプレゼンテーション層を提供するコンポーネントはどれか。",
 ["Tivoli Enterprise Portal Server","Lifeline Agent","CICS VR","DS8000 HMC"],
 0,
 "Tivoli Enterprise Portal Server がデータの取得・分析・整形を行うプレゼンテーション層を提供し、hub（TEMS）からデータを取得する。",
 "p.50/64 Tivoli Enterprise Portal Server provides core presentation layer; retrieves data from hub")

# 11748
add("11748","IBM Tivoli Monitoring and IBM Tivoli NetView for z/OS",69,
 "IBM Tivoli Monitoring と IBM Tivoli NetView for z/OS は連携して GDPS の監視を実現する。NetView は自動化と監視データの収集基盤を提供し、IBM NetView エージェントは IBM Tivoli Monitoring を必要とする。収集された監視情報は ITM の Tivoli Enterprise Portal で表示され、運用者は各システムコンポーネントの状態にドリルダウンできる。",
 "ステップ1: NetView と IBM NetView エージェント、ITM（TEMS/TEPS）が稼働していることを確認する。\nステップ2: Tivoli Enterprise Portal で NetView が収集した監視情報が表示されることを確認する。\nステップ3: 各システムコンポーネントへドリルダウンし、状態が確認できることを検証する。\n期待結果: NetView と ITM が連携し、監視情報が Portal で参照できること。",
 "IBM NetView エージェントが必要とする製品はどれか。",
 ["IBM Tivoli Monitoring","CICS VR のみ","DFSMSdss","RACF のみ"],
 0,
 "IBM NetView エージェントは IBM Tivoli Monitoring を必要とし、NetView が収集した監視情報を ITM/TEP で表示する。",
 "p.69 The IBM NetView agent requires IBM Tivoli Monitoring")

# 11751
add("11751","IBM Tivoli NetView for z/OS",69,
 "IBM Tivoli NetView for z/OS は、すべての IBM GDPS ソリューションの基盤を提供する製品である。自動化プラットフォーム、ステートマシン構築能力、NetView プログラム間通信、Consolidated Audit・NetView・z/OS ログを用いた監査証跡などの機能を提供する。GDPS Active/Active では制御・自動化・監視データ収集の中核を担う。",
 "ステップ1: NetView サブシステムが稼働し、GDPS 自動化タスクが起動していることを確認する。\nステップ2: NetView コンソールから GDPS パネル（制御・照会）にアクセスできることを確認する。\nステップ3: 監査証跡へ GDPS 操作が記録されることを確認する。\n期待結果: NetView が GDPS の自動化・制御・監視基盤として機能していること。",
 "IBM Tivoli NetView for z/OS が GDPS において果たす役割はどれか。",
 ["全 GDPS ソリューションの自動化・制御・監視の基盤","ディスクの物理レプリケーション","CPU の電力管理","テープ媒体の暗号化のみ"],
 0,
 "NetView for z/OS は全 GDPS の基盤として、自動化プラットフォーム、ステートマシン、プログラム間通信、監査証跡を提供する。",
 "p.69 IBM Tivoli NetView for z/OS provides the base for all IBM GDPS solutions")

# 11752
add("11752","IBM Tivoli NetView for z/OS and IBM Tivoli NetView Monitoring for GDPS",57,
 "IBM Tivoli NetView for z/OS は GDPS の自動化・制御基盤を提供し、IBM Tivoli NetView Monitoring for GDPS は GDPS Active/Active ソリューション専用のコンポーネントである。NetView Monitoring for GDPS は、ワークロードとレプリケーションの状態、ヘルスチェック、ソフトウェアレプリケーション性能、ルーティング判断などを監視し、両サイトにまたがって例外を検出してアラートする。",
 "ステップ1: NetView と NetView Monitoring for GDPS の両タスクが稼働していることを確認する。\nステップ2: NetView Monitoring がワークロード・レプリケーション状況を監視していることを確認する。\nステップ3: 例外状態を擬似的に発生させ、アラートが両サイトをまたいで検出されることを確認する。\n期待結果: NetView Monitoring for GDPS が監視・アラートを行い、情報が ITM へ転送されること。",
 "IBM Tivoli NetView Monitoring for GDPS が監視する対象に含まれないものはどれか。",
 ["ワークロードとレプリケーションの状態","サイトのヘルスチェック","ソフトウェアレプリケーション性能とルーティング判断","CPU マイクロコードのバージョン番号"],
 3,
 "NetView Monitoring for GDPS はワークロード・レプリケーション状態、ヘルスチェック、レプリケーション性能、ルーティング判断を監視する。CPU マイクロコードのバージョン監視は対象ではない。",
 "p.57/21 NetView Monitoring for GDPS monitors workload/replication status, health checks, performance, routing")

# 11753
add("11753","IBM Tivoli System Automation for z/OS",87,
 "IBM Tivoli System Automation for z/OS（SA z/OS）は、GDPS が利用するシステム自動化製品である。SA z/OS は BCPii（Base Control Program internal interface）をサポートし、GDPS は SA を介してこのインターフェースを利用してハードウェアと直接通信し、LOAD・ACTIVATE・RESET といった HMC 自動化機能を実行する。GDPS のシステム管理アクションの基盤となる。",
 "ステップ1: 各システムで SA z/OS が稼働していることを確認する。\nステップ2: BCPii が構成され、GDPS が HMC 機能（LOAD/ACTIVATE/RESET）を呼び出せることを確認する。\nステップ3: テスト環境で Standard Action（例: RESET）を実行し、SA/BCPii 経由でハードウェアが応答することを確認する。\n期待結果: SA z/OS と BCPii により GDPS のハードウェア制御アクションが機能すること。",
 "GDPS が SA z/OS を介して利用し、ハードウェアと直接通信するインターフェースはどれか。",
 ["BCPii（Base Control Program internal interface）","TCP/IP ソケットのみ","CICS リージョン","DFSMS"],
 0,
 "SA z/OS は BCPii をサポートし、GDPS は SA を介して BCPii でハードウェアと直接通信し LOAD/ACTIVATE/RESET を実行する。",
 "p.87 SA supports BCPii; GDPS uses this interface through System Automation for HMC automation (LOAD, ACTIVATE, RESET)")

# 11756
add("11756","IIDR for DB2 and GDPS Active/Active",37,
 "IIDR for DB2 と GDPS Active/Active の統合では、Q Replication によるソフトウェア非同期レプリケーションが Active/Active の DB2 ワークロードのサイト間データ同期を担う。GDPS はレプリケーションの状態を監視し、サイト切替時にはレプリケーション方向の制御やワークロードルーティングと協調する。詳細な IIDR for DB2 の設計は SG24-8154 を参照する。",
 "ステップ1: GDPS の Replication ウィンドウで DB2 サブスクリプションの稼働と遅延を確認する。\nステップ2: 計画切替を試行し、GDPS が IIDR for DB2 のレプリケーション制御と協調することを確認する。\nステップ3: 切替後、データがターゲットで整合し、ルーティングが更新されることを確認する。\n期待結果: IIDR for DB2 と GDPS が協調してデータ同期と切替を行うこと。",
 "GDPS Active/Active が IIDR for DB2 に対して行う役割はどれか。",
 ["レプリケーション状態の監視と切替時の制御・協調","DB2 表の物理設計","SQL の最適化","バッファプールのサイジング"],
 0,
 "GDPS は IIDR for DB2 のレプリケーション状態を監視し、サイト切替時にレプリケーション制御やルーティングと協調する。",
 "p.37/28 IIDR for DB2 and GDPS Active/Active")

# 11757
add("11757","IIDR for DB2 architectural overview",40,
 "IIDR for DB2 のアーキテクチャは、ソースとターゲットの DB2、キャプチャープログラム、アプライプログラム、そして変更データを運ぶトランスポート基盤（一般に WebSphere MQ）から構成される。キャプチャーは DB2 のログからコミット済み変更を読み取り、トランスポートを介してアプライがターゲット DB2 へ適用する。これにより非同期のトランザクション整合レプリケーションを実現する。",
 "ステップ1: ソース／ターゲット DB2、キャプチャー、アプライ、トランスポート（MQ）の各コンポーネントが稼働していることを確認する。\nステップ2: キャプチャーが DB2 ログを読み取り、変更がトランスポートへ送られていることを確認する。\nステップ3: アプライがターゲット DB2 へ変更を適用していることを確認する。\n期待結果: キャプチャー→トランスポート→アプライの流れが機能し、ターゲット DB2 が同期していること。",
 "IIDR for DB2 アーキテクチャでソース DB2 のコミット済み変更を読み取るコンポーネントはどれか。",
 ["キャプチャープログラム","アプライプログラム","ロードバランサー","Lifeline Advisor"],
 0,
 "キャプチャープログラムが DB2 ログからコミット済み変更を読み取り、トランスポートを介してアプライがターゲットへ適用する。",
 "p.40 3.2.2 IIDR for DB2 architectural overview（capture/apply/transport）")

# 11758
add("11758","IIDR for IMS and GDPS/AA",47,
 "IIDR for IMS と GDPS Active/Active（GDPS/AA）の統合では、IMS データの単方向非同期レプリケーションが Active/Active の IMS ワークロードのサイト間同期を担う。GDPS はレプリケーション状態を監視し、サイト切替時にレプリケーション制御とワークロードルーティングを協調させる。ターゲットデータの鮮度はレプリケーション遅延に依存する。",
 "ステップ1: GDPS の Replication ウィンドウで IMS サブスクリプションの稼働と遅延を確認する。\nステップ2: 計画切替を試行し、GDPS が IIDR for IMS のレプリケーション制御と協調することを確認する。\nステップ3: 切替後、IMS データがターゲットで整合していることを確認する。\n期待結果: IIDR for IMS と GDPS が協調して IMS データ同期と切替を行うこと。",
 "GDPS/AA における IIDR for IMS のレプリケーション方向はどれか。",
 ["単方向（unidirectional）","双方向","マルチマスター","同期 PPRC"],
 0,
 "IIDR for IMS は単方向レプリケーションであり、GDPS はその状態監視と切替制御を担う。",
 "p.47 IIDR for IMS and GDPS/AA; unidirectional")

# 11759
add("11759","IIDR for IMS Architectural Overview",48,
 "IIDR for IMS のアーキテクチャは、ソース／ターゲットの IMS データベース、更新ログレコードを含む IMS ログ、両サイトで稼働する Classic data server、キャプチャーおよびアプライコンポーネントから構成される。キャプチャー処理が IMS ログの更新レコードを読み取り、トランスポートを介してアプライがサブスクリプションごとの apply PSB を用いてターゲット IMS へ適用する。",
 "ステップ1: ソース／ターゲットの Classic data server が稼働していることを確認する。\nステップ2: キャプチャーが IMS ログを読み取り、変更が転送されていることを確認する。\nステップ3: アプライが apply PSB を用いてターゲット IMS へ適用していることを確認する。\n期待結果: IMS レプリケーションフロー（ログ読取→転送→PSB 適用）が機能していること。",
 "IIDR for IMS アーキテクチャの主要コンポーネントに含まれるものはどれか。",
 ["Classic data server","DS8000 HMC","CICS VR のみ","RMF モニター"],
 0,
 "IIDR for IMS は、IMS ソース／ターゲット DB、IMS ログ、両サイトで稼働する Classic data server、キャプチャー／アプライから構成される。",
 "p.48 3.4.2 IIDR for IMS Architectural Overview; Classic data servers on both sites")

# 11760
add("11760","IIDR for VSAM and GDPS/AA",43,
 "IIDR for VSAM と GDPS Active/Active（GDPS/AA）の統合では、VSAM データのレプリケーションが Active/Active の VSAM ワークロードのサイト間同期を担う。システムロガーのログストリームから読み取った変更を、ターゲット側 CICS リージョン経由で適用する。GDPS はレプリケーション状態を監視し、サイト切替時に協調する。CICS TS／CICS VR が前提となる。",
 "ステップ1: GDPS の Replication ウィンドウで VSAM レプリケーションの稼働と遅延を確認する。\nステップ2: ターゲット側 CICS リージョンが稼働し、変更を適用していることを確認する。\nステップ3: 計画切替を試行し、GDPS と IIDR for VSAM が協調することを確認する。\n期待結果: VSAM データがサイト間で同期され、切替時に協調動作すること。",
 "IIDR for VSAM and GDPS/AA でターゲットへの適用に用いられるものはどれか。",
 ["ターゲット側 CICS リージョン","DS8000 の FlashCopy","テープライブラリ","DFSMShsm"],
 0,
 "IIDR for VSAM はシステムロガーのログストリームから変更を読み取り、ターゲット側 CICS リージョン経由でターゲット VSAM へ適用する。",
 "p.43 IIDR for VSAM and GDPS/AA; applies via CICS region at target partition")

# 11761
add("11761","IIDR for VSAM architectural overview",44,
 "IIDR for VSAM のアーキテクチャは、ソース／ターゲットの VSAM データセット、変更ログレコードを保持するシステムロガーのログストリーム、ログを読み取るキャプチャー処理、そしてターゲットパーティションで稼働してターゲット VSAM へ変更を適用する CICS リージョンから構成される。これにより同期レプリカを維持し、ターゲットデータの鮮度はレプリケーション遅延に依存する。",
 "ステップ1: システムロガーのログストリームが構成され、VSAM 更新のログレコードが書き込まれていることを確認する。\nステップ2: キャプチャー処理がログストリームを読み取っていることを確認する。\nステップ3: ターゲット CICS リージョンがターゲット VSAM へ変更を適用していることを確認する。\n期待結果: ログストリーム読取→ターゲット CICS 経由適用の流れが機能していること。",
 "IIDR for VSAM アーキテクチャで変更ログレコードを保持する場所はどれか。",
 ["システムロガーのログストリーム","DB2 表","IMS データベース","DS8000 のキャッシュ"],
 0,
 "IIDR for VSAM はシステムロガーのログストリームに保持された VSAM 変更のログレコードを読み取り、ターゲット CICS リージョン経由で適用する。",
 "p.43/44 IIDR for VSAM architectural overview; reads system logger log streams")

# 11763
add("11763","Integrate with current disaster recovery plan",95,
 "既存の災害対策（DR）計画と GDPS Active/Active を統合する際には、いくつかの考慮が必要である。まず既存 DR ソリューションをレビューし、GDPS Active/Active とどのように統合するかを決定し、DR 計画を精緻化する。GDPS Active/Active は主に Active/Active ワークロードへの近継続的可用性を提供する一方、既存 DR との統合・協調をサポートする。",
 "ステップ1: 既存の DR ソリューションと手順をレビューし、対象範囲を整理する。\nステップ2: GDPS Active/Active と既存 DR の役割分担（A/A ワークロードは GDPS、その他は既存 DR 等）を決定する。\nステップ3: 統合後の DR 計画を文書化し、テストで検証する。\n期待結果: GDPS Active/Active と既存 DR 計画が整合的に統合され、テストで確認できること。",
 "既存 DR 計画と GDPS Active/Active を統合する際の最初のステップはどれか。",
 ["既存 DR ソリューションのレビュー","全ワークロードの即時停止","DR 計画の破棄","新規メインフレームの購入"],
 0,
 "統合では、既存 DR ソリューションをレビューし、GDPS Active/Active との統合方法を決定し、DR 計画を精緻化する手順をとる。",
 "p.95 Review existing DR solution; decide how to integrate with GDPS Active/Active; refine plan")

# 11764
add("11764","Interaction with other components within GDPS Active/Active",51,
 "Lifeline は GDPS Active/Active 内の他のコンポーネントと相互作用する。Lifeline Advisor は外部ロードバランサーへ分散推奨を提供し、GDPS へ環境のヘルス情報を提供する。Lifeline Agent は各本番 LPAR でワークロードのヘルスを Advisor へ報告する。これらの相互作用により、無制限距離の2サイト間で知的なロードバランシングと近継続的可用性が実現される。",
 "ステップ1: Lifeline Advisor と Agent、外部ロードバランサー、GDPS（NetView）の連携経路を確認する。\nステップ2: Agent がワークロードヘルスを Advisor へ報告していることを確認する。\nステップ3: Advisor がロードバランサーへ分散推奨を、GDPS へヘルス情報を提供していることを確認する。\n期待結果: Lifeline が他コンポーネントと相互作用し、ルーティングと可用性が維持されること。",
 "Lifeline Advisor が外部ロードバランサーへ提供する情報はどれか。",
 ["トランザクションの分散推奨（ルーティング情報）","DB2 表定義","ストレージ容量","CPU マイクロコード"],
 0,
 "Lifeline Advisor は外部ロードバランサーへ分散推奨（ルーティング情報）を提供し、GDPS へヘルス情報を提供する。Agent は LPAR のヘルスを報告する。",
 "p.51 Lifeline interacts with other components; load balances workloads across two sites")

# 11765
add("11765","Introduction",17,
 "第1章「Introduction」では、GDPS Active/Active ソリューションの概念とビジネス価値を説明する。本章には「GDPS Active/Active solution concepts」と「Benefits of using GDPS Active/Active」のセクションが含まれる。GDPS Active/Active は無制限距離の複数サイトを管理し、同一アプリケーションと同一データを稼働させてクロスサイトのワークロードバランシング、継続的可用性、災害対策を提供する。",
 "ステップ1: 第1章で GDPS Active/Active の概念とビジネス価値の概要を把握する。\nステップ2: GDPS Web インターフェースで複数サイトのワークロードが同一アプリ・データで稼働していることを確認する。\nステップ3: 継続的可用性と災害対策の観点で、自組織要件との対応を整理する。\n期待結果: GDPS Active/Active の目的（CA とワークロードバランシング、DR）が理解できること。",
 "第1章 Introduction が扱うテーマとして正しいものはどれか。",
 ["GDPS Active/Active の概念とビジネス価値","ディスクの物理フォーマット手順","CICS の SQL チューニング","テープ媒体の管理手順"],
 0,
 "第1章は GDPS Active/Active の概念（solution concepts）とビジネス価値（benefits）を説明する導入章である。",
 "p.17 Chapter 1. Introduction; concepts and business value of GDPS Active/Active")

# 11768
add("11768","Launching Tivoli Enterprise Portal from the GDPS web interface",78,
 "GDPS Web インターフェースから Tivoli Enterprise Portal（TEP）を起動できる。TEP を起動すると、GDPS Active/Active のウィンドウへドリルダウンし、IBM GDPS Active/Active のロードバランサー、レプリケーションサーバー、Workload Lifeline Advisor、ワークロードに関する詳細を参照できる。これにより監視と運用操作を統合的に行える。",
 "ステップ1: GDPS Web インターフェースにログオンし、Tivoli Enterprise Portal 起動の操作を行う。\nステップ2: TEP が起動し、GDPS Active/Active のビューが表示されることを確認する。\nステップ3: ロードバランサー、レプリケーションサーバー、Lifeline Advisor、ワークロードへドリルダウンして詳細を確認する。\n期待結果: GDPS Web インターフェースから TEP を起動し、各構成要素の詳細を参照できること。",
 "GDPS Web インターフェースから TEP を起動してドリルダウンできる対象はどれか。",
 ["ロードバランサー・レプリケーションサーバー・Lifeline Advisor・ワークロード","CPU マイクロコードのみ","RACF プロファイルのみ","テープ媒体のみ"],
 0,
 "TEP 起動後、GDPS Active/Active のロードバランサー、レプリケーションサーバー、Workload Lifeline Advisor、ワークロードへドリルダウンできる。",
 "p.78 launch Tivoli Enterprise Portal; drill down to Load Balancers, Replication Servers, Lifeline Advisors, Workloads")

# 11773
add("11773","Lifeline recommendation on workload distribution",51,
 "IBM Multi-site Workload Lifeline は、2サイトにまたがるワークロードの知的なロードバランシングを実現する。Lifeline Advisor は環境のヘルスと性能情報をもとに、外部ロードバランサーへワークロードの分散推奨を提供する。新規接続は最も処理能力の高いアプリケーション・サーバー・システムへルーティングされ、性能向上と近継続的可用性に寄与する。",
 "ステップ1: Lifeline Advisor が稼働し、ロードバランサーへ分散推奨を提供していることを確認する。\nステップ2: 各サイトのワークロードヘルスと性能情報が Advisor に集約されていることを確認する。\nステップ3: 新規接続が処理能力の高いサイトへルーティングされることを確認する。\n期待結果: Lifeline の推奨に従って、ワークロードが最適に分散されること。",
 "Lifeline がワークロード分散推奨を行う際に考慮する主な情報はどれか。",
 ["環境のヘルスと性能情報","ディスクのシリアル番号","オペレーターの氏名","テープ媒体の本数"],
 0,
 "Lifeline Advisor は各サイトのヘルスと性能情報をもとに分散推奨を提供し、新規接続を最も処理能力の高いサイトへルーティングする。",
 "p.51 intelligent load balancing; new connections routed to most capable applications/servers/systems")

# 11775
add("11775","Minimizing latency (and RPO) and improving replication performance by using parallel apply",46,
 "Parallel apply（並列適用）は、複数の UOR（作業単位）をターゲットデータセット／データベースへ並行して適用することで、レプリケーション環境の性能を向上させる。サブスクリプション全体で利用可能な作業をほぼリアルタイムに書き込むことで遅延（latency）と RPO を最小化できる。並列適用では「遅延の最小化」と「整合性の維持」という2つの目標が考慮される。",
 "ステップ1: レプリケーションのサブスクリプションで parallel apply が有効化されていることを確認する。\nステップ2: GDPS の Replication ウィンドウで現在の遅延（latency）を確認する。\nステップ3: 高負荷時に並列適用により遅延が抑制されること、整合性が維持されることを確認する。\n期待結果: 並列適用により遅延と RPO が低減され、かつデータ整合性が保たれること。",
 "Parallel apply が遅延・RPO 低減のために行うことはどれか。",
 ["複数の UOR をターゲットへ並行適用する","レプリケーションを停止する","同期 PPRC へ切り替える","データを圧縮するのみ"],
 0,
 "Parallel apply は複数の UOR を並行してターゲットへ適用し、遅延と RPO を最小化する。遅延の最小化と整合性維持の両立が目標である。",
 "p.46 3.3.4 parallel apply; applying UORs concurrently to minimize latency (and RPO); Latency and Consistency")

# 11777
add("11777","Multi-Site Workload Lifeline for z/OS",25,
 "Multi-Site Workload Lifeline for z/OS は、無制限距離の2サイトにまたがって TCP/IP ワークロードを知的にロードバランスする製品で、GDPS Active/Active ソリューションにおいて中核的な役割を果たす。Lifeline Advisor と Lifeline Agent から構成され、Advisor が外部ロードバランサーへ分散先を、GDPS へ環境のヘルス情報を提供する。現時点では TCP/IP ワークロードをサポートする。",
 "ステップ1: コントローラー上で Lifeline Advisor（Primary）が稼働していることを確認する。\nステップ2: 本番 LPAR で Lifeline Agent が稼働していることを確認する。\nステップ3: TCP/IP ワークロードが2サイト間で分散されていることを確認する。\n期待結果: Lifeline が TCP/IP ワークロードを2サイト間で知的に分散していること。",
 "Multi-Site Workload Lifeline for z/OS が現時点でサポートするワークロード種別はどれか。",
 ["TCP/IP ワークロード","SNA ワークロードのみ","バッチジョブのみ","テープ I/O のみ"],
 0,
 "Lifeline は現時点で TCP/IP ワークロードをサポートし、2サイト間で知的にロードバランスする（SNA は将来サポート予定）。",
 "p.25/30 Lifeline product only supports TCP/IP workload; load balances across two sites")

# 11779
add("11779","Network Connectivity and bandwidth considerations",91,
 "ネットワーク接続性と帯域幅の考慮は、ソフトウェア非同期レプリケーションの性能と RPO に直結する。変更データ量が増えると遅延が高くなる可能性があるため、書き込みワークロードの実測データをもとに必要帯域を見積もる必要がある。実際のデータとワークロードで自らテストを行い、単一のレプリケーション経路でどれだけのスループットを処理できるかを把握することが推奨される。",
 "ステップ1: 対象ワークロードの書き込み量を15分間隔・1週間程度で測定する。\nステップ2: その実測値をもとに必要なネットワーク帯域を見積もる。\nステップ3: 実データ・実ワークロードでレプリケーションをテストし、スループットと遅延を確認する。\n期待結果: 必要帯域が確保され、レプリケーション遅延が目標 RPO 内に収まること。",
 "ネットワーク帯域幅の見積もりで最も重視すべきデータはどれか。",
 ["書き込み（write）ワークロードの実測量","読み取り専用クエリーの本数","オペレーターの作業時間","ディスクの空き容量のみ"],
 0,
 "帯域見積もりでは書き込みワークロードの実測量が重要で、実データ・実ワークロードでのテストによりスループットと遅延を把握する。",
 "p.91/53 bandwidth planning; you are only interested in the write workload; run your own test")

# 11785
add("11785","Overview",23,
 "第2章「Architectural overview」の概要では、GDPS Active/Active の設計がフェイルオーバーモデルから近継続的可用性モデルへのパラダイムシフトであることを示す。他の GDPS ソリューションがストレージベースレプリケーションに依存するのに対し、Active/Active はソフトウェアベースの非同期レプリケーションを用いる。ストレージ上のデータは即座にアクセスできないため回復に時間を要するが、Active/Active はこの課題を解決する。",
 "ステップ1: Active/Active のアーキテクチャ概要（ソフトウェア非同期レプリケーション）をドキュメントで確認する。\nステップ2: GDPS Web インターフェースでレプリケーションが稼働していることを確認する。\nステップ3: ストレージベース GDPS と比較し、RTO/RPO が秒オーダーに改善されることを確認する。\n期待結果: ソフトウェア非同期レプリケーションにより近継続的可用性が実現できること。",
 "GDPS Active/Active のアーキテクチャがストレージベース GDPS と異なる点はどれか。",
 ["ソフトウェアベースの非同期レプリケーションを用いる","同期ディスクミラーリングのみを用いる","レプリケーションを行わない","テープのみでデータを保護する"],
 0,
 "GDPS Active/Active はソフトウェアベースの非同期レプリケーションを用い、フェイルオーバーモデルから近継続的可用性モデルへ転換している。",
 "p.23 Chapter 2 Architectural overview; asynchronous software replication-based solution; paradigm shift")

# 11786
add("11786","Overview of IBM Tivoli Monitoring",50,
 "IBM Tivoli Monitoring（ITM）の概要として、ITM は監視サーバー（hub）、Tivoli Enterprise Portal Server（プレゼンテーション層）、各種監視エージェントから構成される階層型の監視基盤である。ポータルサーバーは hub からデータを取得してユーザー操作に応じて表示し、hub はリモートサーバーや直接接続された監視エージェントを制御する。GDPS Active/Active の監視情報もこの基盤上で表示される。",
 "ステップ1: hub 監視サーバー（TEMS）と Tivoli Enterprise Portal Server が稼働していることを確認する。\nステップ2: 監視エージェントが hub に接続されていることを確認する。\nステップ3: Tivoli Enterprise Portal で GDPS Active/Active の監視データが表示されることを確認する。\n期待結果: ITM の階層（hub・ポータルサーバー・エージェント）が機能し、監視データが表示されること。",
 "IBM Tivoli Monitoring でユーザーへのデータ表示・整形を担うコンポーネントはどれか。",
 ["Tivoli Enterprise Portal Server","Lifeline Agent","CICS リージョン","DS8000 HMC"],
 0,
 "Tivoli Enterprise Portal Server がプレゼンテーション層を提供し、hub（TEMS）からデータを取得してユーザー操作に応じて表示する。",
 "p.50/64 Overview of IBM Tivoli Monitoring; portal server retrieves data from hub; presentation layer")

# 11791
add("11791","Planned Actions windows and functions",77,
 "GDPS Active/Active の Planned Actions（計画アクション）は、GDPS ユーザーインターフェース内の Planned Actions ウィンドウから起動する。メニューバーから Planned Actions タスクを選択すると Planned Actions ウィンドウが表示される。ここでは、サイトのシャットダウン、サイトの起動、CEC のシャットダウン／起動といった計画シナリオ向けのスクリプトを参照・実行できる。",
 "ステップ1: GDPS Web インターフェースのメニューバーから Planned Actions タスクを選択する。\nステップ2: 表示された Planned Actions ウィンドウで、実行可能なスクリプト（サイトシャットダウン／起動、CEC 操作）の一覧を確認する。\nステップ3: テスト用シナリオのスクリプトを実行し、計画アクションが想定どおり進行することを確認する。\n期待結果: Planned Actions ウィンドウから計画シナリオのスクリプトを参照・実行できること。",
 "Planned Actions ウィンドウから実行できる計画シナリオに含まれるものはどれか。",
 ["サイトのシャットダウン／起動や CEC の操作","DB2 表の作成","RACF ユーザー登録","テープ媒体の初期化"],
 0,
 "Planned Actions ウィンドウでは、サイトシャットダウン・サイト起動・CEC シャットダウン／起動などの計画シナリオ向けスクリプトを参照・実行できる。",
 "p.77 5.11.5 Planned Actions windows; run scripts for site shutdown, site start, CEC shutdown/start")

# 11792
add("11792","Planning considerations",90,
 "計画上の考慮事項では、ワークロードをオンラインワークロードとバッチワークロードに分け、さらにオンラインは業務分野（line of business）ごとに細分化する。Active/Active ワークロードはより厳密な定義を持ち、業務関連の定義（アプリケーションとミドルウェア実行環境、扱うデータの集合体）として識別する。これにより適切な構成（Active/Standby か Active/Query）を決定できる。",
 "ステップ1: ワークロードをオンライン／バッチに分類し、オンラインを業務分野ごとに整理する。\nステップ2: 各 Active/Active ワークロードを構成するアプリ・ミドルウェア・データを特定する。\nステップ3: 各ワークロードに適した構成（Active/Standby か Active/Query）を決定し、GDPS に反映する。\n期待結果: ワークロードが適切に定義・分類され、構成方針が決定できること。",
 "Active/Active ワークロードの計画における「ワークロード」の定義の特徴はどれか。",
 ["アプリ・ミドルウェア・データの集合体である業務関連の定義","物理ディスク1台の単位","NetView の1コマンド","単一のオペレーター操作"],
 0,
 "Active/Active ワークロードはより厳密な業務関連の定義を持ち、アプリケーション・ミドルウェア実行環境・データの集合体として識別される。",
 "p.90 Planning; Active/Active workload is a business-related definition; aggregation of software and data")

# 11794
add("11794","Prerequisite software for controlling and monitoring",69,
 "GDPS Active/Active の制御・監視に必要な前提ソフトウェアには、IBM Tivoli NetView for z/OS（自動化・監視基盤）、IBM NetView Monitoring for GDPS、IBM Tivoli Monitoring（監視データ表示）、IBM Tivoli System Automation for z/OS（ハードウェア制御）などが含まれる。これらが連携して GDPS の制御・監視機能を提供する。NetView エージェントは ITM を必要とする。",
 "ステップ1: NetView、NetView Monitoring for GDPS、ITM、SA z/OS の各前提製品が導入・稼働していることを確認する。\nステップ2: それぞれのバージョンが GDPS の要件を満たすことを確認する。\nステップ3: 各製品が連携し、制御・監視機能が動作することを確認する。\n期待結果: 前提ソフトウェアが揃い、GDPS の制御・監視が機能すること。",
 "GDPS Active/Active の制御・監視に必要な前提ソフトウェアに含まれないものはどれか。",
 ["IBM Tivoli NetView for z/OS","IBM Tivoli Monitoring","IBM Tivoli System Automation for z/OS","一般的な Web ブラウザーのみで他は不要"],
 3,
 "制御・監視には NetView、NetView Monitoring for GDPS、ITM、SA z/OS などの前提製品が必要であり、ブラウザーのみで足りるわけではない。",
 "p.69 Prerequisite software for controlling and monitoring（NetView, ITM, SA z/OS）")

# 11795
add("11795","Prerequisites for each component",69,
 "各コンポーネントの前提条件として、IBM NetView エージェントは IBM Tivoli Monitoring を必要とし、SA z/OS は BCPii をサポートしてハードウェア制御を行う。レプリケーション製品（IIDR for DB2/IMS/VSAM）はそれぞれのデータベース／ミドルウェア（DB2、IMS、CICS TS/CICS VR）を前提とする。これらの前提を満たすことで GDPS Active/Active 環境が正しく機能する。",
 "ステップ1: 各コンポーネント（NetView エージェント、SA z/OS、IIDR 各種）の前提製品を一覧化する。\nステップ2: NetView エージェントの ITM 前提、IIDR for VSAM の CICS VR 前提などを個別に確認する。\nステップ3: すべての前提が満たされていることを確認する。\n期待結果: 各コンポーネントの前提条件が満たされ、環境全体が整合的に稼働すること。",
 "IBM NetView エージェントの前提となる製品はどれか。",
 ["IBM Tivoli Monitoring","CICS VR","DFSMShsm","RACF のみ"],
 0,
 "各コンポーネントには個別の前提があり、IBM NetView エージェントは IBM Tivoli Monitoring を前提とする。",
 "p.69 Prerequisites for each component; IBM NetView agent requires IBM Tivoli Monitoring")

# 11797
add("11797","Reduce planned and unplanned outages for critical applications",21,
 "GDPS Active/Active は、クリティカルなアプリケーションの計画停止および計画外停止を削減する。継続的可用性モデルにより、サイト切替を非破壊的に（業務を止めずに）実行できるため、計画メンテナンス時の停止を回避できる。また障害検出と迅速な切替により、計画外停止の影響時間（RTO）を秒オーダーに短縮する。",
 "ステップ1: 計画切替（Planned Action）を1ワークロードに実施し、業務を止めずに切り替わることを確認する。\nステップ2: 障害を擬似的に発生させ、GDPS が検出して迅速に切替できることを確認する。\nステップ3: 切替前後の業務影響時間（RTO）を測定し、秒オーダーであることを確認する。\n期待結果: 計画・計画外いずれの停止も最小化され、業務影響が短縮されること。",
 "GDPS Active/Active が計画停止を削減できる主な理由はどれか。",
 ["サイト切替を非破壊的（業務無停止）に実行できる","ストレージ容量を増やせる","バッチを高速化する","ネットワークを暗号化する"],
 0,
 "GDPS Active/Active は非破壊的なサイト切替により計画メンテナンス時の停止を回避し、迅速な切替で計画外停止の影響時間も短縮する。",
 "p.21 reduce planned and unplanned outages; continuous availability; non-disruptive planned switch")

# 11799
add("11799","Single consistency groups or multiple?",91,
 "ソフトウェアレプリケーション製品は、GDPS Active/Active のためにトランザクション整合性を保ってデータをレプリケートする。変更データ量が増えると遅延が高くなる可能性があるため、ソフトウェアレプリケーションの性能リファレンスデータを用いてスループットと遅延を見積もる際は注意が必要である。実データと実ワークロードで自らテストを行い、単一の整合性グループでどれだけ処理できるかを把握すべきである。",
 "ステップ1: 対象データの変更量（スループット）を測定する。\nステップ2: 単一の整合性グループで処理した場合の遅延を実データ・実ワークロードでテストする。\nステップ3: 遅延が目標を超える場合は複数の整合性グループへの分割を検討する。\n期待結果: 整合性グループの単一／複数の構成判断が、実測スループットと遅延にもとづいて行えること。",
 "整合性グループを単一にするか複数に分けるかの判断材料として最も適切なものはどれか。",
 ["実データ・実ワークロードでのスループットと遅延の実測","オペレーターの人数","ディスクの色","ライセンス料金のみ"],
 0,
 "単一／複数の整合性グループの判断は、変更データ量の増加に伴う遅延を考慮し、実データ・実ワークロードでのスループットと遅延の実測にもとづいて行う。",
 "p.91 Single consistency groups or multiple?; run your own test with real data to understand throughput")

# 11811
add("11811","Tivoli OMEGAMON XE on z/OS",51,
 "Tivoli OMEGAMON XE on z/OS は、IBM Tivoli Monitoring 基盤上で稼働する z/OS 向け監視製品であり、システムリソース（CPU、ストレージ、ワークロード等）の監視を提供する。GDPS Active/Active 環境では、OMEGAMON が収集する z/OS システムの性能情報を Tivoli Enterprise Portal で参照でき、GDPS の監視情報と併せてシステム全体の健全性を把握する助けとなる。",
 "ステップ1: OMEGAMON XE on z/OS のエージェントが稼働し、ITM の hub に接続されていることを確認する。\nステップ2: Tivoli Enterprise Portal で z/OS システムの性能情報（CPU・ストレージ等）が表示されることを確認する。\nステップ3: GDPS の監視情報と併せてシステム全体の状態を確認する。\n期待結果: OMEGAMON の z/OS 監視情報が TEP で参照でき、GDPS 監視と統合的に把握できること。",
 "Tivoli OMEGAMON XE on z/OS が提供する監視対象として正しいものはどれか。",
 ["z/OS システムリソース（CPU・ストレージ・ワークロード等）の性能","ディスクの物理シリアル番号のみ","ネットワークケーブルの長さ","オペレーターの勤務時間"],
 0,
 "OMEGAMON XE on z/OS は ITM 基盤上で z/OS のシステムリソース（CPU・ストレージ・ワークロード等）を監視し、TEP で参照できる。",
 "p.51 Tivoli OMEGAMON XE on z/OS（ITM 基盤上の z/OS 監視）")

# 11813
add("11813","What are GDPS service offerings and how do they address business requirements?",98,
 "GDPS サービス提供は、業務要件（高可用性・継続的可用性・災害対策など）にどのように対応するかという観点で説明される。IBM Global Technology Services は、技術コンサルティングワークショップやインストールサービスなどを通じて、顧客の業務要件に合った GDPS ソリューションの選定・設計・導入を支援する。これにより RTO/RPO 目標やコンプライアンス要件に対応する。",
 "ステップ1: 付録 A で GDPS サービス提供と業務要件の対応を確認する。\nステップ2: 自組織の業務要件（RTO/RPO、コンプライアンス等）を整理する。\nステップ3: GTS のサービスメニュー（ワークショップ、インストール等）と要件を突き合わせる。\n期待結果: GDPS サービス提供が自組織の業務要件にどう対応するか把握できること。",
 "GDPS サービス提供が対応する業務要件として適切なものはどれか。",
 ["高可用性・継続的可用性・災害対策などの要件","オフィスの内装デザイン","社員の給与計算","印刷物の配送"],
 0,
 "GDPS サービス提供は、高可用性・継続的可用性・災害対策といった業務要件に対し、選定・設計・導入支援を通じて対応する。",
 "p.98 What are GDPS service offerings and how do they address business requirements?")

# 11817
add("11817","Workload Management windows and functions",75,
 "Workload Management（ワークロード管理）タスクは、メニューバーから選択すると Workload Management ウィンドウを表示する。このウィンドウは、当該 GDPS 環境に定義されたすべてのワークロード（更新系・参照系の両方）について、一目で分かる高レベルの状況サマリーを提供する。各サイトに表示される状況は、サーバーアプリケーションの可用性などにもとづく。",
 "ステップ1: GDPS Web インターフェースのメニューバーから Workload Management タスクを選択する。\nステップ2: Workload Management ウィンドウで全ワークロード（更新系・参照系）の状況サマリーを確認する。\nステップ3: あるワークロードのサーバーアプリをすべて停止し、状況がワークロード障害として表示されることを確認する。\n期待結果: Workload Management ウィンドウで全ワークロードの状況が一目で把握でき、障害が反映されること。",
 "Workload Management ウィンドウが提供する情報はどれか。",
 ["全ワークロード（更新系・参照系）の高レベルな状況サマリー","DB2 の SQL 実行計画","RACF プロファイル一覧","テープ媒体の在庫"],
 0,
 "Workload Management ウィンドウは、定義された全ワークロード（更新系・参照系）の状況を一目で把握できる高レベルなサマリーを提供する。",
 "p.75 5.11.4 Workload Management windows; at-a-glance status summary for all workloads (updates and queries)")

# Build output
out = {
    "page": "g058",
    "product": "IBM GDPS 4.7",
    "total_rows": 129,
    "target_rows": 56,
    "fixed_count": len(rows),
    "rows": rows,
}
os.makedirs(r"_phase2_outputs", exist_ok=True)
with open(r"_phase2_outputs/g058_fixed.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("rows:", len(rows))
# validate
with open(r"_phase2_outputs/g058_fixed.json", encoding="utf-8") as f:
    json.load(f)
print("JSON valid")
