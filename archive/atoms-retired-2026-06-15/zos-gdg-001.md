---
id: ZOS-GDG-001
title: GDG（Generation Data Group）
status: stable
last_reviewed: 2026-06-01
authors: [agent]
rag_verified: partially
---

# ZOS-GDG-001: GDG（Generation Data Group）

## 1. purpose（なぜ存在するか）

GDG は **同一の論理名 (base name) で世代管理されるデータセット族**。日次バッチで「昨日の sales データ」「一昨日の sales データ」「7 日前の sales データ」を **相対世代 (-0, -1, -2 ...)** で指定できる。JCL は世代番号だけ書けば、カタログが「具体的 DSN」（例: `USER.PROD.SALES.G0123V00`）を解決する。

Linux で `logrotate` が `messages` → `messages.1` → `messages.2.gz` ... と世代ローテーションしてくれる挙動の、もっと厳格・明示・カタログ統合版。Linux は「file system 上のリネーム」だが、z/OS は **カタログにメタを持って世代番号を整数で管理し、絶対 DSN にマップする**。アプリ側は世代番号だけ意識し、絶対 DSN や VOL=SER は意識しなくて良い。

これは「人間が DSN.YYYYMMDD で世代名を組み立てる」運用と対立する設計。後者はファイル名 suffix の重複ミス・桁あふれ・年越し問題で必ず破綻する。GDG はそれを **OS 機能** に格上げした。

## 2. mechanism（どう動くか）

- **GDG base**: カタログに登録される論理エントリ。物理データセットではない。`DEFINE GENERATIONDATAGROUP` で作成。
- **世代データセット (GDS)**: 実体。`USER.PROD.SALES.G0001V00`, `G0002V00`, ... `G9999V00` の形式。`Gxxxx` が世代番号、`Vnn` がバージョン番号（通常 V00 固定）。
- **相対世代番号**: JCL で `DSN=USER.PROD.SALES(0)` = 最新、`(-1)` = 1 つ前、`(+1)` = これから作る新世代。
- **base の属性**: `LIMIT(n)` = 保持する世代数上限（旧 GDG: 最大 255、Extended GDG: 最大 999）。`SCRATCH/NOSCRATCH` = 押し出された旧世代を物理削除するか、`EMPTY/NOEMPTY` = LIMIT 超過時に「最古 1 個押し出し」か「全削除」か。
- **新世代作成タイミング**: JCL ステップが `DISP=(NEW,CATLG)` でアロケートし、ステップが **正常終了** した時に世代番号が確定する。ジョブ実行中は **仮 (deferred catalog)** 状態。
- **Extended GDG (V2 GDG)**: z/OS 2.1 以降で `EXTENDED` 属性付き base、最大 999 世代、絶対 DSN 部分が 9 文字 (G000000000V00) に拡張。

## 3. prerequisites（理解の前提）

- データセット概念と DSN 命名規則 — `ZOS-DATASET-001`
- カタログのエントリ種別（NONVSAM / GDG base / GDS） — `ZOS-CATALOG-001`
- JCL の DISP パラメータ — `ZOS-JCL-001`

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-DATASET-001, ZOS-CATALOG-001
- `specialized_by`: なし（V1 GDG / V2 GDG は同一アトム内 axis）
- `contrasts_with`: 「DSN suffix に YYYYMMDD を書く」自作世代管理（脆いがツール非依存）
- `used_by`: ZOS-JCL-001（DD で相対世代指定）, ZOS-SORT-001（GDG 全世代 concatenation で集計）, ZOS-RECOVERY-001（HSM が GDS 単位で migrate）

## 5. pitfalls（実装・運用での落とし穴）

- **同一ジョブ内で `(+1)` を複数ステップ参照、各ステップで別世代になる事故**: 「`(+1)` は最初の参照で世代確定、以降の `(+1)` は確定済み世代の参照」と思いきや、**ステップ A で `DISP=(NEW,CATLG)` + ステップ B で `DISP=SHR DSN=...(+1)` の時、ステップ B は A が作ったのと同じ `(+1)` を見るが、ステップ C で `DISP=(NEW,CATLG)` で `(+2)` を作ろうとすると挙動が race**。実務的には「同一ジョブ内では `(+1)` 確定後、追加世代を作らない」のが安全。複数世代を一気に作るなら別ジョブ。
- **`(-1)` 指定で前回ジョブが作ってない世代を引きに行く**: 初回起動 / 障害復旧で前世代が無い時、`DSN=...(-1)` は `IEC130I DD STATEMENT MISSING`（NOT CATLG）で ABEND。初回判定とフォールバック JCL（IDCAMS で空 GDS を仮作成等）の備えが要る。
- **LIMIT 超過時の SCRATCH=YES でテープ世代まで消失**: SCRATCH 設定で押し出された旧世代は **物理データセットも削除** される。HSM で migrate 済の GDS は HSM 上の migrate コピーも削除される。「世代増やしたから古いの取っとこ」が、想定外に SCRATCH で消えていた事故。SCRATCH/NOSCRATCH は **base 定義時に正しく** 決める。
- **V1 GDG 上限 255 世代**: 日次世代を毎日作っていれば 1 年でほぼ枯渇。LIMIT に達した瞬間、最古が押し出される。「日次 + 月次 1 個保持」を同じ base でやろうとして 月次世代が押し出される事故。**業務世代毎に base を分ける** が原則。
- **`Vnn` の更新と `NOSCRATCH`**: 同一世代を再生成（同日リラン）すると `V00 → V01` になる。`V01` 以降は `NOSCRATCH` でも `Vnn` 累積で容量を喰い、`LISTCAT` で混乱する。`V00` 固定運用なら **古い V00 を IDCAMS DELETE** してから再生成する。
- **PDS メンバ的にアクセスできない**: 「世代の中身を覗く」のは GDS の **絶対 DSN** で 1 個ずつ。`LISTCAT GDG(USER.PROD.SALES) ALL` で世代一覧、その後 `BROWSE 'USER.PROD.SALES.G0123V00'`。base 名で BROWSE しようとすると「これはカタログ管理エントリで実体じゃない」エラー。
- **V1 と V2 の混在カタログ**: 既存 V1 GDG base を V2 (EXTENDED) に変更したい時、`DEFINE EXTENDED` で新規作成 + 旧 base からの GDS 移行が必要。**in-place の V1→V2 変換は無い**、これを知らないと「ALTER で変えられない」で詰む。

## 6. examples（具体例）

```jcl
//* GDG base 作成（IDCAMS）
//DEFGDG  EXEC PGM=IDCAMS
//SYSPRINT DD SYSOUT=*
//SYSIN    DD *
  DEFINE GENERATIONDATAGROUP -
    (NAME(USER.PROD.SALES) -
     LIMIT(30) -
     NOEMPTY -
     SCRATCH)
/*
```

```jcl
//* 新世代作成 + 既存 (-1) 参照
//STEP1 EXEC PGM=COBPROG
//IN    DD DSN=USER.PROD.SALES(-1),DISP=SHR
//OUT   DD DSN=USER.PROD.SALES(+1),DISP=(NEW,CATLG,DELETE),
//          SPACE=(CYL,(10,5)),
//          DCB=(MODEL.DSCB,RECFM=FB,LRECL=80)
```

```tso
LISTCAT GDG(USER.PROD.SALES) ALL
LISTCAT LEVEL(USER.PROD.SALES) ALL
```

## 7. decision_axes（採否を分ける判断軸）

- **V1 GDG (255 上限) vs V2 GDG (EXTENDED, 999 上限)**: 日次以上の高頻度なら V2 推奨。V1 は 30〜60 世代運用なら十分。V2 は z/OS 2.1+ 必須、古い utility や ISV ツールが V2 命名（9 桁 G）を解釈できない場合あり、互換性確認必要。
- **SCRATCH vs NOSCRATCH**: 業務として旧世代を物理保持する義務がある（監査・突合）なら NOSCRATCH + HSM migrate に任せる。日次の作業データ等は SCRATCH。**判断基準は「7 年保管義務」のような規制要件**。
- **GDG base 単位の業務分離**: 「日次・週次・月次・年次」は **別 base** にする。同 base で混ぜると LIMIT で異種が押し出される。base が増える管理コストはあるが、運用事故が少ない。
- **EMPTY vs NOEMPTY**: NOEMPTY は LIMIT 超過時に「最古 1 個」を押し出す。EMPTY は「全削除」。EMPTY は通常使わない（業務的に「全部リセット」が要件のときだけ）。
- **DSN.YYYYMMDD 直書き vs GDG**: GDG はカタログ管理コスト + DSN 桁の制約があるが、相対世代指定で JCL を**カレンダー非依存** に書ける。年越し・閏日・営業日ロジックを JCL の symbol で書く運用は破綻するため、**世代管理が必要なら GDG 一択**。

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_BASIC_001, BK_ZOS_TECH_002) から世代データセット運用パターンを概念蒸留し反映 (ADR-0109)。逐語引用禁止。
