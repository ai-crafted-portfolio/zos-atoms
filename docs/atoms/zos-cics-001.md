---
id: ZOS-CICS-001
title: CICS（オンライン トランザクション）
status: stable
last_reviewed: 2026-05-09
---


# ZOS-CICS-001: CICS

## 1. purpose（なぜ存在するか）

CICS（Customer Information Control System、現 IBM 名は CICS Transaction Server）は **オンライン トランザクション処理 (OLTP) のミドルウェア**。

JCL ベースのバッチ処理（→ [ZOS-JCL-001](zos-jcl-001.md)）が秒〜時間単位の処理単位なら、CICS は **ミリ秒単位のトランザクション**。世界中の銀行・保険・航空・物流の基幹オンライン処理を 1970 年代から動かしている。「ATM で残高照会したら 200ms で返ってくる」その裏側にいる事が多い。

Linux 系で例えれば **Java EE の Application Server (WebLogic, WebSphere)** に近いが、CICS はもっと低レベル: アプリ + DB ロック + 通信 + ログ + リカバリを単一プロセス内で密結合に管理。Java EE が JEE 仕様で抽象化されているのに対し、CICS は「CICS 流儀」が独自仕様（COMMAREA, BMS マップ, EXEC CICS マクロ）。

なぜ Java EE 普及後も生き残るか: 1 トランザクションあたりのオーバーヘッドが極めて小さく、メインフレームのハードウェアと密結合（zIIP, RoCE, 専用 CF）で、**1 リージョンで秒間 1 万 TPS 越え**を狙える。

## 2. mechanism（どう動くか）

中核概念:
- **リージョン (Region)**: CICS の実行アドレススペース
- **トランザクション ID (Tranid)**: 4 文字。`MENU` `INQR` `UPDT` 等
- **プログラム**: COBOL/PL/I/C/Java で書く。CICS マクロ `EXEC CICS RECEIVE/SEND/READ/WRITE` でリソース操作
- **マップ (BMS map)**: 3270 端末画面定義
- **COMMAREA**: トランザクション間で受け渡すデータ領域（最大 32K）
- **CSD** (CICS System Definition): リソース定義
- **VSAM ファイル**（→ [ZOS-VSAM-001](zos-vsam-001.md)）が標準ストレージ。Db2 連携も多い
- **TS Queue / TD Queue**: 一時データ保管
- **トランザクション境界**: `EXEC CICS SYNCPOINT` で COMMIT、`SYNCPOINT ROLLBACK` で UNDO

## 3. prerequisites（理解の前提）

- VSAM（→ [ZOS-VSAM-001](zos-vsam-001.md)）— CICS のリソース DB が VSAM
- RACF（→ [ZOS-RACF-001](zos-racf-001.md)）— トランザクション認可
- データセット概念 + JCL（CICS 起動 JCL の理解）
- 一般 IT 知識: トランザクション概念（COMMIT / ROLLBACK）、3270 端末画面プロトコル

## 4. relations（他アトムとの繋がり）

- `depends_on`: [ZOS-VSAM-001](zos-vsam-001.md), [ZOS-RACF-001](zos-racf-001.md), [ZOS-DUMP-001](zos-dump-001.md) (transaction dump = SVC dump 派生)
- `specialized_by`: なし
- `contrasts_with`: [ZOS-IMS-001](zos-ims-001.md)（同じく OLTP だが階層 DB ベース）, [ZOS-JCL-001](zos-jcl-001.md)（オンライン vs バッチ）, （未作成）JEE-APPSERVER-001
- `used_by`: [ZOS-PARALLELSYSPLEX-001](zos-parallelsysplex-001.md) (CICSplex)

## 5. pitfalls（実装・運用での落とし穴）

- **PCT/PPT に新リソース登録忘れ**: COBOL モジュール書いて LOAD ライブラリに置いただけでは CICS から呼べない。**PPT (Processing Program Table) と PCT (Program Control Table) に登録**（CSD の DEFINE PROGRAM/TRANSACTION）+ `CEMT SET PROGRAM(...) NEWCOPY` が必要。新人が「ロードしたのに動かない」で半日溶かす定番。
- **NEWCOPY せずに CICS 再起動**: 上記の `CEMT SET PROGRAM(...) NEWCOPY` をしないと旧モジュールがメモリに残る。「直したのに直ってない」現象。再起動でも反映されるが、**プロダクション CICS を再起動するのは数秒数百万円失う事**もあり得るので NEWCOPY が原則。
- **COMMAREA 32K 超え**: COMMAREA は 32760 バイト上限。複雑な画面遷移で「全部 COMMAREA に持つ」設計だと早晩破綻。**Channel/Container** (CICS TS 3.1 以降) で大きなデータ受け渡しに切り替える要、知らないと 32K の壁にぶつかってアーキ全面書換え。
- **EXEC CICS HANDLE CONDITION の漏れ**: VSAM 読み込みで RECORD NOT FOUND をハンドル無しにすると、CICS デフォルトで `AEIB` ABEND（NOTFND condition）で tranid 丸ごと死亡。**全 VSAM/Db2 操作の後に必ず HANDLE / RESP 確認** が CICS COBOL の基本作法。
- **Pseudo-Conversational vs Conversational の混同**: 旧式の Conversational（端末待ちでもメモリ保持）は資源占有で論外。**Pseudo-Conversational** が正解。新人がついうっかり Conversational で書くと TPS が劇的に下がる。
- **CICS と Db2 の RRSAF/CAF 接続**: Db2 接続方式で RRSAF（推奨、2 phase commit 可）と CAF（旧、分散整合性に穴）。**新規システムで CAF を選ぶ理由は今や無いが、レガシー CICS で CAF が残ってる事案多し**。
- **ストレージ違反 SOS**: Storage Outside Space は CICS リージョン内で予約 storage が枯渇した時。長時間放置すると `IGZ0035S` 等で CICS 自体が缶詰状態。原因は大半が「プログラムが GETMAIN したまま FREEMAIN しない」リーク。

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

## 7. decision_axes（採否を分ける判断軸）

- **CICS vs IMS**: 共に OLTP だが流儀が違う。CICS は VSAM/Db2 + 後付け RDB、IMS は DBD/PSB ベースの階層 DB が中核。**CICS は新規開発・モダン化との親和性高**、IMS は既存資産が膨大なら据え置きが安全。新規 z/OS 採用なら CICS 一択。
- **CICS Java vs CICS COBOL**: CICS は Java サポート（JVM Server）あるが、レガシー COBOL コードベースが圧倒的多数。**新規 Java 開発なら Liberty + JCICS で書ける**が、既存システムへの統合面で COBOL のままが安牌。
- **VSAM ファイル vs Db2 表**: シンプルなキーバリュー型は VSAM、**複雑検索 / 複数システム連携は Db2**。
- **Pseudo-Conversational vs Conversational**: Pseudo 一択。**Conversational は教育用 or 緊急対応で使うが、本番では絶対禁止**。
- **Single Region vs CICSplex**: 小規模なら 1 region で十分。中〜大規模で可用性要件あれば CICSplex。**初期構築は 1 region から始め、必要時 CICSplex に拡張**。最初から CICSplex は構築コスト過大。
- **RRSAF vs CAF**: 新規 RRSAF 一択。**既存 CAF 環境を RRSAF に移行するプロジェクトは数ヶ月単位**だが、後で必ず必要になる。
