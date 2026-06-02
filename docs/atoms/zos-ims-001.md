---
id: ZOS-IMS-001
title: IMS（階層 DB + トランザクション）
status: stable
last_reviewed: 2026-05-09
---


# ZOS-IMS-001: IMS

## 1. purpose（なぜ存在するか）

IMS（Information Management System）は IBM が 1968 年（アポロ計画の在庫管理）に作った **階層型データベース** + **トランザクション マネージャ**。CICS（→ [ZOS-CICS-001](zos-cics-001.md)）と並んで z/OS 上の OLTP 中核ミドルだが、**「DB 部分が独自ストレージ」** という点が CICS と決定的に違う。

なぜ存在するか: RDB 出現以前の世界で、「親→子→孫」という階層構造（部品表、組織図、口座→明細→取引）を **そのまま物理レイアウトで保持し、I/O 1 回で親子を取得する** のが目的。RDB なら JOIN が必要な処理を、IMS は **物理的に隣接配置** で 1 read で済ます。**1970〜90 年代の業務システムでは性能優位**。

現代の RDB 全盛期になぜ生き残るか: 移行コストが膨大。20〜40 年動いている IMS DB は、業務ルールが DBD/PSB の中に染み込んでいて、Db2 や RDB に「データ移行」だけしても **アプリ全書換** が必要。だから「動いてる物は触るな」原則で残る。

哲学的対立: Db2 は宣言的（SQL で「何が欲しいか」）、IMS は手続的（DL/I コールで「どう辿るか」）。

## 2. mechanism（どう動くか）

### IMS DB（階層 DB）

- **DBD** (Database Description): 物理 DB の定義
- **PSB** (Program Specification Block): プログラム視点の DB ビュー
- **PCB** (Program Communication Block): PSB 内の個別 DB 定義 + 入出力バッファ
- 物理アクセス方式:
  - **HDAM** (Hierarchical Direct): ハッシュベース直接アクセス
  - **HIDAM** (Hierarchical Indexed Direct): KSDS 索引 + 直接
  - **HISAM** (Hierarchical Indexed Sequential): 順次中心
  - **DEDB** (Data Entry Database): Fast Path、超高速更新
- 「セグメント」と呼ぶレコード、親→子の階層関係を物理的に持つ
- **DL/I** コール: `GU`, `GHU`, `GN`, `ISRT`, `REPL`, `DLET` 等

### IMS TM

- **MPP** (Message Processing Program): オンライン
- **BMP** (Batch Message Processing): バッチ
- **IFP** (IMS Fast Path): 超高速 OLTP

## 3. prerequisites（理解の前提）

- データセット概念（→ [ZOS-DATASET-001](zos-dataset-001.md)）
- RACF（→ [ZOS-RACF-001](zos-racf-001.md)）
- 一般 IT 知識: 階層型 DB の概念、トランザクション境界
- VSAM 理解（HIDAM 等）

## 4. relations（他アトムとの繋がり）

- `depends_on`: [ZOS-DATASET-001](zos-dataset-001.md), [ZOS-RACF-001](zos-racf-001.md), [ZOS-DUMP-001](zos-dump-001.md) (region dump)
- `specialized_by`: なし
- `contrasts_with`: [ZOS-CICS-001](zos-cics-001.md)（OLTP 流儀）, [ZOS-DB2-001](zos-db2-001.md)（階層 vs 関係 DB）
- `used_by`: [ZOS-PARALLELSYSPLEX-001](zos-parallelsysplex-001.md) (IMS Data Sharing)

## 5. pitfalls（実装・運用での落とし穴）

- **DBD/PSB の更新で全プログラム再 BIND 必須**: DBD 変更（セグメント追加・キー長変更等）すると、影響する全 PSB を再生成、全プログラムを再 BIND。1 つの DBD 変更で 50 本のプログラムが影響、本番反映窓 8 時間とかザラ。**DBD 設計を最初に間違えると一生取り戻せない**。
- **HDAM のハッシュ衝突で「物理的に近い」が崩壊**: HDAM はハッシュ関数でレコード位置を決めるが、データ偏りで衝突続出 → 物理連続配置の前提が崩れて性能劇的劣化。**Reorg（DBR ユーティリティ）で再配置必要、しかしオフライン窓必要**。年に 1〜2 回の Reorg 計画必須。
- **PCB 数の上限**: 1 PSB に持てる PCB 数に上限あり（IMS バージョン依存、概ね 256 程度）。マイクロサービス化で 1 トランザクションが多数 DB を見るアプリを安易に書くと、PCB 数枯渇で `BA1` 等の起動エラー。
- **IMS Fast Path の DEDB は「データロスト可能」**: DEDB は性能のために WAL の同期書きを省略する設定が可能。性能は出るが、システム障害時にロストする取引あり。**銀行系 OLTP の中でも、別途 mirror で守るのが鉄則**。
- **BMP がオンラインを止める**: BMP は IMS TM 上で動くため、長時間ロック保持すると MPP（オンライン）が待たされて応答時間悪化。**BMP は短時間 + 頻繁な COMMIT (CHKP)** が原則、設計で定期 CHKP 入れないと夜間バッチ後にオンラインが詰まる。
- **DBRC RECON 破損で全停止**: IMS 全体のリカバリ管理 DB（RECON）が壊れると、IMS 起動自体が不可能。RECON は 3 重化（PRIMARY / SECONDARY / SPARE）が標準、それでも年に 1 回はバックアップ確認必要。
- **IMS Connect 経由の通信タイムアウト**: 外部から IMS にアクセスする時、IMS Connect のタイムアウト設定 (`MAXSESS`, `INACT_TIMEOUT`) を間違うとセッション枯渇。Java EE → IMS Connect → IMS の連携は設定 4 箇所揃えないと不可解な切断。

## 6. examples（具体例）

```ims
* DBD 定義例（HDAM）
DBD   NAME=CUSTDB,ACCESS=(HDAM,VSAM),
      RMNAME=(DFSHDC40,5,80,30)
DATASET DD1=CUSTDB,SIZE=4096
SEGM  NAME=CUSTOMER,BYTES=200,PTR=T
FIELD NAME=(CUSTID,SEQ,U),BYTES=10,START=1,TYPE=C
SEGM  NAME=ORDER,PARENT=CUSTOMER,BYTES=100,PTR=T
FIELD NAME=(ORDERID,SEQ,U),BYTES=10,START=1,TYPE=C
SEGM  NAME=ITEM,PARENT=ORDER,BYTES=80,PTR=T
DBDGEN
END
```

```cobol
       CALL 'CBLTDLI' USING 'GU      ',
                            PCB-MASK,
                            CUSTOMER-IO-AREA,
                            SSA-CUSTOMER.
       IF STATUS-CODE = '  '
          DISPLAY 'FOUND: ' CUSTOMER-IO-AREA
       ELSE
          DISPLAY 'STATUS: ' STATUS-CODE.
```

## 7. decision_axes（採否を分ける判断軸）

- **IMS vs Db2**: 既存 IMS 資産があり業務ルールが DBD/PSB に染み込んでるなら据え置き、新規開発で SQL/JOIN/ACID/分散環境連携が要なら Db2。**「IMS のまま機能追加」は短期コスト低・長期コスト高、「Db2 移行」は短期コスト高・長期柔軟性大**。
- **HDAM vs HIDAM**: 主キー検索だけならハッシュの HDAM が高速、副キー / 範囲検索が必要なら HIDAM。**運用 20 年の DB なら設計時は HDAM だったが、副キー検索ニーズ追加で HISAM/HIDAM を後付けして妥協してる事例多し**。
- **MPP vs BMP の使い分け**: オンライン即時応答は MPP、バッチ処理は BMP。**「リアルタイム性は要らないが大量更新したい」を BMP でやるとオンラインが詰まる**、夜間バッチ窓に押し込むのが原則。
- **IMS Fast Path (DEDB) 採用**: 銀行系の超高速 OLTP（秒間 1 万 TPS 越え）が必要な場合のみ。**普通の OLTP は MPP + 一般 DB で十分**、Fast Path 必要な現場は限定的。
- **IMS Open Database (ODBM) の活用**: Java/REST から IMS へのアクセスを開放する仕組み。レガシー IMS をモダン化したいなら導入価値あり。**完全 Db2 移行が無理なら ODBM で API 化**、が中庸案。
