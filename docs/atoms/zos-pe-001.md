---
title: ZOS-PE-001
description: dataset encryption / DFSMS encryption / Coupling Facility encryption、key label 管理、DFP encryption
tags:
  - Middleware
  - Middleware-Utility
---
# ZOS-PE-001: Pervasive Encryption (PE)

## 1. purpose（なぜ存在するか）

Pervasive Encryption は z/OS 上のデータを **application を書き換えずに**全 dataset / Coupling Facility 構造 / zFS / log stream 単位で透過暗号化するOS-level facility。z14 で導入された CPACF 加速で「全データ暗号化しても CPU 増分が数 %」を目標にした、site 全体の暗号化義務化への OS 回答。

Linux の LUKS が block device 単位で暗号化するのに対し、PE は **dataset 単位 / CF構造単位 / log stream 単位** という z/OS の論理オブジェクトで切る。AWS S3 SSE-KMS や Azure Disk Encryption と思想は近いが、PE は鍵管理が ICSF (自社 master key) で完結し、cloud provider が master key を握らない点が独自。

## 2. mechanism（どう動くか）

- **DFSMS dataset encryption**: SMS DATACLAS に `KEYLABEL(MYLABEL)` を指定すると、
  当該 DATACLAS で allocate された dataset は CKDS の MYLABEL 鍵で透過暗号化
- 暗号化単位は VSAM RLS / extended format sequential / extended format PDSE。
  古い basic format dataset は対象外
- **CF encryption**: CFRM ポリシーに `ENCRYPT(YES) KEYLABEL(...)` を指定。
  list / cache / lock 構造のうち、cache と list の data portion が暗号化対象
  (lock control 部は対象外)
- **zFS encryption**: zFS aggregate 単位で `IOEFSPRM` の `aggrgrow_encrypt`,
  zFS の `keylabel=` 指定
- **logger encryption**: log stream 定義時 `LOGR ENCRYPT(KEYLABEL(...)) `
- 演算は CPACF 経由の AES-256 XTS が default。鍵は ICSF CKDS に存在し、
  application は鍵を意識しない
- 鍵 rotation は DATACLAS の KEYLABEL を変更 → 既存 dataset は古い label の鍵で
  読み続ける (rewrite するまで)。新規 allocate のみ新鍵

## 3. prerequisites（理解の前提）

- ICSF と CKDS の基礎 — `ZOS-ICSF-001`
- SMS DATACLAS / STORCLAS の基礎 — `ZOS-SMS-001`
- VSAM / extended format dataset — `ZOS-VSAM-001`, `ZOS-DATASET-001`
- CF 構造 (cache/list/lock) — `ZOS-PARALLELSYSPLEX-001`
- 一般 IT 知識: AES, XTS mode

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-ICSF-001, ZOS-SMS-001, ZOS-VSAM-001, ZOS-PARALLELSYSPLEX-001
- `specialized_by`: なし
- `contrasts_with`: Linux LUKS / dm-crypt, AWS S3 SSE-KMS, Azure Disk Encryption
- `used_by`: ZOS-DB2-001 (TDE と併用), ZOS-CICS-001 (永続 dataset), ZOS-HSM-001 (ML2 暗号化)

## 5. pitfalls（実装・運用での落とし穴）

- **key label 変更で既存 dataset が読めなくなる**: DATACLAS の KEYLABEL を更新するだけで既存 dataset が暗号化されたものと誤解する事例多発。**既存は古い label の鍵で暗号化されたまま、新規 allocateだけ新 label** が正しい挙動。古い label の鍵を CKDS から削除すると既存dataset 全件読めない。鍵 rotation 戦略には「古い label の鍵を一定期間保持」が必須で、ICSF 鍵ライフサイクル設計の落とし穴。
- **extended format でない dataset は暗号化されない**: DATACLAS に KEYLABEL を入れても、basic format の sequential / PDS は暗号化対象外。`IDCAMS LISTCAT ALL` で `EXTENDED FORMAT` 行を見ないと意図通り暗号化されてるか分からない。古い JCL の `RECFM=FB,LRECL=80` だけの DD はbasic format で allocate されて暗号化されないまま機密データを保管する事故。DATACLAS の `EXT(REQ)` 強制 + 全 dataset 棚卸が必須。
- **DFP encryption の性能ペナルティを過小評価**: 「CPACF があるから無視できる」と思って全データ暗号化したら、VSAM RLSの hot dataset で CPU 30% 増 (測定済) + I/O latency 15% 増の site がある。CPACF 加速でも buffer copy 経路が増えるため zero-cost ではない。本番展開前に SMF 42 / RMF Mon III の channel busy + CPU 増分を測る。「Pervasive」を文字通り全部にかけず、機密分類が low の dataset は暗号化対象外にする site 設計が現実的。
- **backup (DSS) で encryption 引き継ぎ漏れ**: DSS DUMP / DFSMShsm BACKUP は default で **元 dataset の暗号化を解除してtape に書く** ことがあり、tape side で平文化する事故。`DUMP ENCRYPT`オプションで tape 側でも encryption を維持する設定が必須。「DASD は PE で安心」だが tape backup は別個に暗号化規約が要る。監査人にこの境界を指摘されると site policy 全書き直しになる。
- **CFRM list 構造 encryption の適用範囲誤解**: CF list 構造を暗号化しても、application 側で **control info (entry name等)** と **data portion** の区別を意識しないと、entry name に機密情報(SSN 等) を埋め込んだ設計が暗号化されないまま CF に居続ける。PE 適用前に CF 構造ごとの「何が encryption の対象か」を applicationオーナーと合意することが必要。IBM 公式ドキュメントだけでは「list 暗号化」が data portion 限定と気付けないことが多い。

## 6. examples（具体例）

```
* SMS DATACLAS 定義例 (ISMF panel の DATACLAS DEFINE)
  DATACLAS NAME: ENCEX001
  EXTENDED FORMAT  : REQUIRED
  EXTENDED ADDRESSABILITY: YES
  KEY LABEL        : PROD.AES256.DATASET.001
```

```jcl
//* DATACLAS で暗号化要求 (KEYLABEL は SMS が提供)
//OUTDD DD DSN=USER.PROD.SECRET,
//      DISP=(NEW,CATLG,DELETE),
//      DATACLAS=ENCEX001,
//      SPACE=(CYL,(10,5),RLSE)
```

```
* CFRM ポリシー (IXCMIAPU) で CF 構造の暗号化
  DEFINE STRUCTURE NAME(CACHE_PROD)
    SIZE(102400)
    ENCRYPT(YES)
    KEYLABEL(PROD.AES256.CF.CACHE)
```

## 7. decision_axes（採否を分ける判断軸）

- **dataset 単位 PE vs Db2 TDE**: Db2 user data の暗号化は (a) PE で table space dataset を DATACLAS 経由暗号化 (b) Db2 TDE で page 単位暗号化、の 2 経路。(a) は Db2 から透過、運用変更ゼロ。(b) は Db2 が page 暗号化のためbuffer pool 効率が下がるが、Db2 単独で鍵管理可。両方かけると二重暗号で CPU 損失。**通常は PE 一択**、Db2 TDE は audit要件で明示的に「Db2 側で暗号化」と書かれている時のみ。
- **全 dataset 暗号化 vs 機密分類ベースの選択暗号化**: 「Pervasive」の名前通り全部かけるのが思想。だが CPU 増分 + 鍵管理工数 + 監査範囲 (鍵管理に関わる ID 全部が PCI scope に入る) を考えると、**機密分類 high のみ** という site 戦略が現実的。全部派は「漏れ穴を作らない」、選択派は「コストと範囲限定」。regulator (金融庁 / FFIEC 等) の要求文面で判断。
- **CF 構造の encryption: 全部 vs cache のみ**: CF cache 構造には Db2 buffer 共有 / VSAM RLS shared buffer が乗り、機密データが入る。lock 構造は通常 metadata のみで暗号化不要。list 構造は logger / SMF 等で機密性高 (audit log) が多い。性能影響が大きいのは cache の暗号化なので、site 規模で「cache + 一部 listのみ暗号化」が現実解。lock 暗号化はそもそも不可。
