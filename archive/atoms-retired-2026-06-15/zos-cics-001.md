---
id: ZOS-CICS-001
title: CICS（オンライン トランザクション）
status: stable
last_reviewed: 2026-05-09
authors: [agent]
rag_verified: partially
---

# ZOS-CICS-001: CICS

## 1. purpose（なぜ存在するか）

CICS（Customer Information Control System、現 IBM 名は CICS Transaction Server）は **オンライン トランザクション処理 (OLTP) のミドルウェア**。

JCL ベースのバッチ処理（→ ZOS-JCL-001）が秒〜時間単位の処理単位なら、CICS は **ミリ秒単位のトランザクション**。世界中の銀行・保険・航空・物流の基幹オンライン処理を 1970 年代から動かしている。「ATM で残高照会したら 200ms で返ってくる」その裏側にいる事が多い。

Linux 系で例えれば **Java EE の Application Server (WebLogic, WebSphere)** に近いが、CICS はもっと低レベル: アプリ + DB ロック + 通信 + ログ + リカバリを単一プロセス内で密結合に管理。Java EE が JEE 仕様で抽象化されているのに対し、CICS は「CICS 流儀」が独自仕様（COMMAREA, BMS マップ, EXEC CICS マクロ）。

なぜ Java EE 普及後も生き残るか: 1 トランザクションあたりのオーバーヘッドが極めて小さく、メインフレームのハードウェアと密結合（zIIP, RoCE, 専用 CF）で、**1 リージョンで秒間 1 万 TPS 越え**を狙える。

書籍 (BK_MF_001 / BK_ZOS_TECH_001) 蒸留の補強観点として、CICS は **「アプリ層と OS 層の境界を意図的にぼかした設計」** と理解すると本質が分かる。通常の Linux アプリは「プロセス分離 + システムコール経由で OS 機能を呼ぶ」が、CICS は OS と同居する形で task scheduling / lock 管理 / log writing / recovery を内製化。これによりコンテキストスイッチコストを大幅に削減して TPS を稼いでいる。**「アプリと OS の安全な分離」を犠牲にして性能と一貫性を取った**設計思想なので、現代の microservices/REST と発想が真逆である点を理解しておくと CICS 設計判断がブレない。

## 2. mechanism（どう動くか）

中核概念:
- **リージョン (Region)**: CICS の実行アドレススペース
- **トランザクション ID (Tranid)**: 4 文字。`MENU` `INQR` `UPDT` 等
- **プログラム**: COBOL/PL/I/C/Java で書く。CICS マクロ `EXEC CICS RECEIVE/SEND/READ/WRITE` でリソース操作
- **マップ (BMS map)**: 3270 端末画面定義
- **COMMAREA**: トランザクション間で受け渡すデータ領域（最大 32K）
- **CSD** (CICS System Definition): リソース定義
- **VSAM ファイル**（→ ZOS-VSAM-001）が標準ストレージ。Db2 連携も多い
- **TS Queue / TD Queue**: 一時データ保管
- **トランザクション境界**: `EXEC CICS SYNCPOINT` で COMMIT、`SYNCPOINT ROLLBACK` で UNDO

書籍 (BK_ZOS_TECH_001 / BK_ZOS_TECH_002) 蒸留での追加 mechanism: CICS 内では **タスク (Task) と トランザクション (Transaction) が概念分離** されている。Tranid を起動するたびに新規 Task が作られ、Task は SYNCPOINT 〜 SYNCPOINT 単位で 1 つ以上の Unit-of-Work (UOW) を保持する。**Pseudo-Conversational 方式では「画面 1 枚 = 1 Task」**でユーザ思考時間中はリソースを完全に解放する。これを Conversational に倒すと「ユーザ思考時間 = リソース占有時間」になり、TPS が桁違いに落ちる。設計時に「画面遷移をどこで切るか」が即座にスループット設計になるのが CICS の特徴。

## 3. prerequisites（理解の前提）

- VSAM（→ ZOS-VSAM-001）— CICS のリソース DB が VSAM
- RACF（→ ZOS-RACF-001）— トランザクション認可
- データセット概念 + JCL（CICS 起動 JCL の理解）
- 一般 IT 知識: トランザクション概念（COMMIT / ROLLBACK）、3270 端末画面プロトコル

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-VSAM-001, ZOS-RACF-001, ZOS-DUMP-001 (transaction dump = SVC dump 派生)
- `specialized_by`: なし
- `contrasts_with`: ZOS-IMS-001（同じく OLTP だが階層 DB ベース）, ZOS-JCL-001（オンライン vs バッチ）, （未作成）JEE-APPSERVER-001
- `used_by`: ZOS-PARALLELSYSPLEX-001 (CICSplex)

## 5. pitfalls（実装・運用での落とし穴）

- **PCT/PPT に新リソース登録忘れ**: COBOL モジュール書いて LOAD ライブラリに置いただけでは CICS から呼べない。**PPT (Processing Program Table) と PCT (Program Control Table) に登録**（CSD の DEFINE PROGRAM/TRANSACTION）+ `CEMT SET PROGRAM(...) NEWCOPY` が必要。新人が「ロードしたのに動かない」で半日溶かす定番。
- **NEWCOPY せずに CICS 再起動**: 上記の `CEMT SET PROGRAM(...) NEWCOPY` をしないと旧モジュールがメモリに残る。「直したのに直ってない」現象。再起動でも反映されるが、**プロダクション CICS を再起動するのは数秒数百万円失う事**もあり得るので NEWCOPY が原則。
- **COMMAREA 32K 超え**: COMMAREA は 32760 バイト上限。複雑な画面遷移で「全部 COMMAREA に持つ」設計だと早晩破綻。**Channel/Container** (CICS TS 3.1 以降) で大きなデータ受け渡しに切り替える要、知らないと 32K の壁にぶつかってアーキ全面書換え。
- **EXEC CICS HANDLE CONDITION の漏れ**: VSAM 読み込みで RECORD NOT FOUND をハンドル無しにすると、CICS デフォルトで `AEIB` ABEND（NOTFND condition）で tranid 丸ごと死亡。**全 VSAM/Db2 操作の後に必ず HANDLE / RESP 確認** が CICS COBOL の基本作法。
- **Pseudo-Conversational vs Conversational の混同**: 旧式の Conversational（端末待ちでもメモリ保持）は資源占有で論外。**Pseudo-Conversational** が正解。新人がついうっかり Conversational で書くと TPS が劇的に下がる。
- **CICS と Db2 の RRSAF/CAF 接続**: Db2 接続方式で RRSAF（推奨、2 phase commit 可）と CAF（旧、分散整合性に穴）。**新規システムで CAF を選ぶ理由は今や無いが、レガシー CICS で CAF が残ってる事案多し**。
- **ストレージ違反 SOS**: Storage Outside Space は CICS リージョン内で予約 storage が枯渇した時。長時間放置すると `IGZ0035S` 等で CICS 自体が缶詰状態。原因は大半が「プログラムが GETMAIN したまま FREEMAIN しない」リーク。
- **TS Queue 漏らしっぱなしで Auxiliary Storage 圧迫 (BK_MF_001 蒸留)**: 一時データを `WRITEQ TS` で書いた後、`DELETEQ TS` を忘れると Auxiliary TS Queue データセットに蓄積され続ける。タスク終了で自動消去される **Main TS Queue** と、明示的に消去するまで残る **Auxiliary TS Queue** の動作差を理解していないと、毎晩 CICS 領域が膨らみ続けて週末に CEMT NEWCOPY で乗り切る、という劣化運用が定着してしまう。
- **APPLID 重複によるネットワーク到達不能**: Sysplex 内で複数 CICS リージョンの VTAM APPLID を一意管理しないと、Bind 時に競合してネットワーク経由でユーザが繋がらなくなる。**新規リージョン構築時の APPLID 命名規約 (`xxnnnCICn` 等)** をサイト全体で固める。
- **TWA / COMMAREA / Container の使い分け間違い**: TWA (Transaction Work Area) は同一 Task 内の一時データ、COMMAREA は擬似会話的に画面間で受け渡すデータ、Container は大容量データ用。これらを混同して TWA に COMMAREA 用データを入れる設計をすると、次回 RETURN 後にデータが消えて「動いたり動かなかったり」する不安定挙動になる。
- **CEMT SET と PARMLIB 反映の差**: 運用窓で `CEMT SET PROGRAM(...) NEWCOPY` を打って改修反映したつもりでも、**CICS 再起動時には PARMLIB ベースの定義に戻る**。CEMT 系コマンドは一時的反映で、永続化は CSD の DEFINE PROGRAM 修正が必要。これを知らないと「再起動したら直したはずの不具合が再発した」という事故が起こる。

## 6. examples（具体例）

```cobol
       EXEC CICS READ
            FILE('CUSTFILE')
            INTO(WS-CUST-REC)
            RIDFLD(WS-CUST-ID)
            RESP(WS-RESP)
       END-EXEC.

       EVALUATE WS-RESP
          WHEN DFHRESP(NORMAL)
             MOVE WS-CUST-NAME TO LK-CUST-NAME
          WHEN DFHRESP(NOTFND)
             MOVE 'NOT FOUND'  TO LK-MSG
          WHEN OTHER
             MOVE 'ERROR'      TO LK-MSG
       END-EVALUATE.

       EXEC CICS RETURN
            COMMAREA(DFHCOMMAREA)
            LENGTH(80)
       END-EXEC.
```

```cics
CEMT INQ PROGRAM(INQRPGM)
CEMT SET PROGRAM(INQRPGM) NEWCOPY
CEMT INQ TRANSACTION(INQR)
CEMT INQ TASK
CEMT INQ FILE(CUSTFILE)
```

書籍 (BK_ZOS_TECH_001) 蒸留の運用例として、本番 CICS リージョンでの障害時 1 次対応コマンド一式を運用ランブックに固める慣習がある。**「とりあえず叩く 5 コマンド」を全運用者が即座に出せる状態にしておく**ことで、深夜障害の MTTR (平均復旧時間) が劇的に改善される。

```cics
* 障害時 1 次対応 (運用ランブック例)
CEMT INQ TASK                       * 滞留タスクと CPU 使用
CEMT INQ DSAS                       * ストレージ余裕度
CEMT INQ JOURNAL                    * ジャーナル状況
CEMT INQ CONN                       * 上下流接続の生死
CEMT PERFORM SNAP                   * トラブル時の現状スナップ採取
```

## 7. decision_axes（採否を分ける判断軸）

- **CICS vs IMS**: 共に OLTP だが流儀が違う。CICS は VSAM/Db2 + 後付け RDB、IMS は DBD/PSB ベースの階層 DB が中核。**CICS は新規開発・モダン化との親和性高**、IMS は既存資産が膨大なら据え置きが安全。新規 z/OS 採用なら CICS 一択。
- **CICS Java vs CICS COBOL**: CICS は Java サポート（JVM Server）あるが、レガシー COBOL コードベースが圧倒的多数。**新規 Java 開発なら Liberty + JCICS で書ける**が、既存システムへの統合面で COBOL のままが安牌。
- **VSAM ファイル vs Db2 表**: シンプルなキーバリュー型は VSAM、**複雑検索 / 複数システム連携は Db2**。
- **Pseudo-Conversational vs Conversational**: Pseudo 一択。**Conversational は教育用 or 緊急対応で使うが、本番では絶対禁止**。
- **Single Region vs CICSplex**: 小規模なら 1 region で十分。中〜大規模で可用性要件あれば CICSplex。**初期構築は 1 region から始め、必要時 CICSplex に拡張**。最初から CICSplex は構築コスト過大。
- **RRSAF vs CAF**: 新規 RRSAF 一択。**既存 CAF 環境を RRSAF に移行するプロジェクトは数ヶ月単位**だが、後で必ず必要になる。


## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

本 atom の領域については、IBM 公式 manual を一次出典としつつ、運用事例や設計判断の補強として市販書籍 (BK_MF_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 等の z/OS / メインフレーム関連書籍) からの実装知識を補助的に参照する。逐語引用は禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
