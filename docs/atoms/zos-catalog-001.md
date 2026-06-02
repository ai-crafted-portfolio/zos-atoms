---
id: ZOS-CATALOG-001
title: カタログ（ICF, マスター + ユーザ）
status: stable
last_reviewed: 2026-05-09
---


# ZOS-CATALOG-001: カタログ

## 1. purpose（なぜ存在するか）

カタログは「DSN（44 文字のデータセット名）からボリューム serial を引く対応表」。これが無いと、JCL や TSO で全データセットに毎回 `VOL=SER=xxxxx` を書く必要がある。地獄。

Linux/Windows なら「パス名 = 階層構造そのものに位置情報が入ってる」（`/var/log/messages` で物理位置はファイルシステムが解決）。z/OS は **DSN とボリュームを完全分離** した。データセットを別ボリュームに移しても DSN は変えない（カタログを更新するだけ）。これが大規模運用の前提条件。

DSN は flat な 44 文字（ドット階層は規約で、OS にとっては単なる検索キー）。だから当該 DSN がどこにあるか知るには、別途インデックスが要る。それがカタログ。

## 2. mechanism（どう動くか）

- カタログの実体は **VSAM KSDS**（→ [ZOS-VSAM-001](zos-vsam-001.md)）。「カタログ自体が VSAM」という再帰
- 種別:
  - **マスターカタログ**: システムに 1 つ。`SYS1.MCAT.xxx` 等。z/OS IPL 時に LOADxx で指定
  - **ユーザカタログ**: 複数 OK
- マスターから「**alias**」エントリでユーザカタログに分岐:
  - 例: マスターに「`USER` という HLQ は USER.UCAT にある」と alias 登録
  - `USER.PROD.SALES` を引く時、OS はマスターを見て `USER` alias を辿り、USER.UCAT を読みに行き、本体メタを得る
- **VVDS**: 各ボリュームに置かれる VSAM ボリュームデータセット
- **CSI** (Catalog Search Interface): プログラムからカタログ検索する API

## 3. prerequisites（理解の前提）

- DASD の VTOC（→ [ZOS-DASD-001](zos-dasd-001.md)）
- VSAM KSDS（→ [ZOS-VSAM-001](zos-vsam-001.md)）
- 一般 IT 知識: 階層 DNS のような「ルートからユーザ領域への委譲」モデル

## 4. relations（他アトムとの繋がり）

- `depends_on`: [ZOS-DASD-001](zos-dasd-001.md)
- `specialized_by`: なし
- `contrasts_with`: なし（メインフレーム独自）
- `used_by`: [ZOS-DATASET-001](zos-dataset-001.md), [ZOS-VSAM-001](zos-vsam-001.md), [ZOS-JCL-001](zos-jcl-001.md), [ZOS-SMS-001](zos-sms-001.md) (SMS-managed はカタログ必須), [ZOS-GDG-001](zos-gdg-001.md) (GDG base + GDS は catalog 管理)

## 5. pitfalls（実装・運用での落とし穴）

- **alias 未登録で DSN が「見えない」**: 新しい HLQ で初データセット作成時、マスターカタログに alias 登録忘れると `IDC3009I VSAM CATALOG RETURN CODE 8 - REASON CODE 42` (alias 不在)。新規プロジェクト立ち上げ時の頻発トラブル。`DEFINE ALIAS (NAME(NEWHLQ) RELATE(USER.UCAT))` で登録。
- **ユーザカタログの破損で全データセット行方不明**: 1 つのユーザカタログに 10,000+ DSN を寄せる構成は事故時の影響が巨大。バックアップ取って無いとリカバリ不能。EXPORT/IMPORT の定期取得は **必須**、半年に 1 回はリストアテストもしておく。
- **DELETE NOSCRATCH の混乱**: `DELETE 'USER.X' NOSCRATCH` は「カタログからは消すが VTOC（実体）は残す」。`SCRATCH`（既定）は両方消す。逆を覚えてる人が多く、復旧時に混乱する。
- **マスターカタログ切替の影響範囲**: マスター変更 (LOADxx の MASTERCAT 行) は IPL 必要。「ユーザカタログ追加」は無停止可だが、マスター差し替えは計画停電クラス。失敗するとシステム再起動不可、保守用 console から復旧。
- **ICF カタログの「マルチレベル alias」の罠**: `USER.PROD` だけ別カタログ、`USER.TEST` も別、`USER.x.y.z` もまた別、と多階層 alias を作ると、検索時に全カタログ traversal が発生し性能劣化。HLQ レベル（最大でも 2 階層）で alias 切るのが原則。
- **catalog lock の dead lock**: 大量バッチで同時に同じユーザカタログを更新すると、ENQ contention で待ち合いが発生し、最悪 dead lock。CICS/Db2 系のビジー時間帯にバッチで巨大データセット作る運用は要監視。

## 6. examples（具体例）

```idcams
DEFINE ALIAS (NAME(NEWHLQ) RELATE(USER.UCAT))

LISTCAT CATALOG(USER.UCAT) ALL
LISTCAT ENT(USER.PROD.SALES) ALL

DEFINE USERCATALOG (
    NAME(USER.UCAT)
    VOLUME(DASD01)
    CYLINDERS(50,10)
    ICFCATALOG
    STRNO(3))
```

```jcl
//* 未カタログ DSN を VOL 直指定で OPEN
//DD1 DD DSN=USER.UNCAT.OLD,DISP=SHR,
//       UNIT=3390,VOL=SER=DASD05
```

## 7. decision_axes（採否を分ける判断軸）

- **マスターに全部寄せる vs ユーザカタログ多用**: マスター肥大化は IPL 時の読み込み遅延 + バックアップサイズ膨張 + 障害時影響範囲拡大を招く。**HLQ 単位で複数ユーザカタログに分割**（ユーザカタログ単体で最大 1 万件目安）。マスターは alias の中継器に徹する。
- **ICF 標準 vs ベンダー製カタログ管理**: CA-1, BMC Catalog Manager 等。標準 IDCAMS で頑張れる規模なら不要、データセット数が 10 万超えるなら導入検討。**判断軸は「人間が手で IDCAMS 叩けるか」**。
- **alias の階層深さ**: HLQ レベル alias（1 階層）が標準。深い alias は検索コスト増 + 移行困難、推奨しない。
- **EXPORT 頻度**: 日次 EXPORT が標準。CICS/Db2 系の頻繁に DEFINE/DELETE が走るカタログは数時間に 1 回。**頻度は「リカバリ時間目標 RTO」と「EXPORT 自体のコスト」のトレードオフ**。
