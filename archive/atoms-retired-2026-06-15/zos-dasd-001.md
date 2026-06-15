---
id: ZOS-DASD-001
title: DASD（直接アクセス記憶装置）
status: stable
last_reviewed: 2026-05-09
authors: [agent]
rag_verified: partially
---

# ZOS-DASD-001: DASD

## 1. purpose（なぜ存在するか）

DASD（Direct Access Storage Device）は、メインフレームのストレージ概念。「ハードディスク」と訳されがちだが厳密には違う。z/OS が「ファイル」ではなく「データセット」を扱う哲学（→ ZOS-DATASET-001）の **物理基盤**。

Linux/Windows なら「ストレージ = バイトアドレス可能なブロックデバイス（FBA: Fixed Block Architecture, 512 or 4096 バイト固定）」だが、メインフレームは歴史的に **CKD（Count-Key-Data）** という可変長レコードを物理層で扱う方式を採用した。現代の物理 HDD/SSD は内部的には FBA だが、ストレージコントローラ（DS8000 等）が CKD をエミュレーションして z/OS に見せる。**この「物理の上に論理 CKD 層」が CKD/FBA 対立軸の正体**。

存在理由は性能。バイト単位アクセスより「次のレコード」「次のキー」というデータ語彙でアクセスする方が、メインフレーム時代の chained I/O（SSCH = Start SubChannel）と相性が良い。

## 2. mechanism（どう動くか）

- **物理階層**: ボリューム → シリンダ → トラック → レコード
  - 1 ボリューム = 数千〜数万シリンダ（3390 model 9 = 約 10,000 シリンダ）
  - 1 シリンダ = 15 トラック
  - 1 トラック ≈ 56,664 バイト（half-track block = 27,998 バイト最大）
- **CKD レコード**: 1 レコード = Count（メタ） + Key（任意） + Data（本体）
- **VTOC**: ボリューム冒頭、当該ボリュームの全データセット DSCB を保持
- **VVDS**: VSAM Volume Data Set。VSAM データセットのメタを保持
- **アロケーション単位**: TRK / CYL / BLK / MB / GB / KB
- **EAS / EAV**: Extended Address Space 対応データセットは EAV（65,520 シリンダ超）に置ける

## 3. prerequisites（理解の前提）

- ストレージ I/O の一般概念（チャネル）
- ブロック整数倍の意義
- 一般 IT 知識: HDD のシリンダ・トラック概念

## 4. relations（他アトムとの繋がり）

- `depends_on`: なし（基盤アトム）
- `specialized_by`: なし
- `contrasts_with`: （未作成）LINUX-FBA-DEVICE-001
- `used_by`: ZOS-DATASET-001, ZOS-CATALOG-001, ZOS-VSAM-001, ZOS-SMS-001 (StorageGroup), ZOS-RECOVERY-001 (DSS DUMP 対象)

## 5. pitfalls（実装・運用での落とし穴）

- **3390 ジオメトリ前提のハードコード**: 「1 トラック 27,998 バイト」を前提に BLKSIZE 計算するコード/JCL が大量にある。3380（旧モデル: 1 トラック 23,476 バイト）対応サイトの遺物が混ざると、移行時にブロック効率が劇的に悪化する事案。BLKSIZE=0 で大半は救われるが、ベンダーツールが 0 を許さない場合あり。
- **EAV 移行で旧プログラム停止**: ボリュームを EAV（54GB 超）化したら、EAS 非対応のロードモジュールが `IGD17054I PROGRAM IS NOT EAS-ELIGIBLE` で ABEND。古い ENTERPRISE COBOL（V3 以前）でビルドされたロードモジュールが引っかかる。再 BIND 必要。
- **VTOC 容量枯渇で新規アロケート不能**: VTOC 自体のサイズが足りなくなると、ボリュームに空きシリンダがあっても新規データセット作れない。`B14` 系 ABEND or `IGD17103I` で気付く。VTOC 拡張は ICKDSF REFORMAT で可能だが OFFLINE 必要。
- **TRK アロケート要求でセカンダリ拡張ループ**: `SPACE=(TRK,(1,1))` のような小さい primary でセカンダリを 16 回まで使い切る挙動を理解せず、`SD37`（拡張限度超え）で止まる。
- **オフライン化忘れの ICKDSF**: ICKDSF でボリューム初期化等やる時、対象ボリュームを VARY OFFLINE せずに走らせると `IGI031I device busy` で失敗、最悪は半端な状態でボリューム破損。**運用 DASD には絶対やらない**、保守用の隔離ボリュームでのみ使う原則。
- **3 階層構造の階層が深すぎる場合**: 1 ボリューム上のディレクトリ的概念がない（VTOC は flat）。何百個もデータセットがあると LISTCAT 等の応答が劇的に遅くなる。

## 6. examples（具体例）

```jcl
//* 3390 ボリュームに 100 シリンダ取って PS データセット作成
//STEP01 EXEC PGM=IEFBR14
//DD1    DD DSN=USER.TEST.PS,DISP=(NEW,CATLG),
//          UNIT=3390,VOL=SER=DASD01,
//          SPACE=(CYL,(100,10)),
//          DCB=(RECFM=FB,LRECL=80,BLKSIZE=0)
```

```tso
LISTCAT VOLUME(DASD01) ALL
LISTVTOC VOL=3390=DASD01
```

## 7. decision_axes（採否を分ける判断軸）

- **CKD vs FBA**: z/OS 環境の DASD はほぼ全部 CKD（z/OS 自体が CKD 前提）。FBA は z/VSE 系 OS のみ。**判断の余地はほぼ無く、CKD が標準**。
- **3390-3 vs 3390-9 vs EAV**: 3390-3 (3GB) は小規模、3390-9 (10GB) が標準、EAV (54GB〜) は大量データ用。EAV は「全プログラムが EAS-eligible」確認が前提、後付け移行は古いロードモジュールの再 BIND が地獄。
- **SPACE=TRK vs CYL vs RECORDS**: 数千レコードまでなら TRK、数万〜数百万なら CYL、見積もり困難なら RECORDS。**プロダクション JCL で TRK を 1〜2 にしてる JCL は大体トラブる**。
- **SMS 配下 vs 非 SMS**: SMS 必須、非 SMS は新規不可 が現代の判断。

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_TECH_001/002) から DASD ボリューム管理の実運用知識を概念蒸留し本アトムへ反映 (ADR-0109)。逐語引用禁止、書籍は補助参考。
