---
id: ZOS-CERTMGMT-001
title: RACDCERT + 証明書管理
status: stable
last_reviewed: 2026-06-02
authors: [Z2]
rag_verified: true
---
# ZOS-CERTMGMT-001: RACDCERT + 証明書管理

## 1. purpose（なぜ存在するか）

`RACDCERT` は RACF コマンドで X.509 証明書 / 秘密鍵 / key ring を RACF DB に格納・操作する z/OS 流の証明書管理基盤。Linux の `openssl` + Let's Encrypt + certbot やWindows の `certmgr.msc` + AD CS と違い、**RACF user profile に付帯する形で証明書を保管** し、SAF 認可と一体になっている点が独自。AT-TLS / FTP-TLS / DRDA TLS / WebSphere SSL listener / z/OSMF HTTPS、全部この key ring を参照する。

つまり「証明書管理 = RACF 管理」であり、cert renew の運用が RACF オペレータの責任範囲に入る。Linux のように rsync で /etc/ssl/private を撒く文化は z/OSには無く、site 全体 SSOT として RACF DB に閉じ込めるのが思想。

## 2. mechanism（どう動くか）

- 証明書種類: **CA** (root / intermediate)、**SITE** (site 内 trust anchor)、
  **PERSONAL** (user 又は server cert + 秘密鍵)、**CERTAUTH** (公開鍵のみ trust)
- 各 cert は **owner**: `RACDCERT ID(USER1) ADD ...`、site cert は `SITE` 指定、
  CERTAUTH 系は `CERTAUTH` 指定
- **key ring**: cert の論理束。AT-TLS / FTP-TLS 等の application は ring 名を
  指定し、ring 内の cert を listing して使う。`RACDCERT ADDRING / CONNECT` で構築
- 秘密鍵は (a) RACF DB 内 (b) ICSF PKDS (`PCICC` / `ICSF` / `DSA` 等の指定)
  に保管。ICSF 経由なら HSM 保護
- CSR: `RACDCERT GENCERT REQUEST` で生成。外部 CA に送って署名後 `RACDCERT ADD`
- 自己署名 / 内部 CA: `RACDCERT GENCERT` で root 作って `SIGNWITH(CERTAUTH ...)` で署名
- 有効期限: `NOTBEFORE`, `NOTAFTER` 指定。default は 1 年。renewal は新 cert を  ADD → ring に CONNECT → default 切替

## 3. prerequisites（理解の前提）

- RACF 基本 (user / group / class) — `ZOS-RACF-001`
- ICSF と PKDS (秘密鍵を HSM 保護する場合) — `ZOS-ICSF-001`
- 一般 IT 知識: X.509 chain, CSR, CRL, OCSP
- AT-TLS との連携 — `ZOS-AT-TLS-001`

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-RACF-001
- `specialized_by`: なし
- `contrasts_with`: Linux openssl + Let's Encrypt + certbot,
  Windows certmgr / AD Certificate Services
- `used_by`: ZOS-AT-TLS-001, ZOS-FTP-001 (Z3 起案), ZOS-ZOSMF-001 (Z6 起案),
  ZOS-WAS-001 (Z1 起案)

## 5. pitfalls（実装・運用での落とし穴）

- **Cert 期限切れで AT-TLS 通信全停止**: RACDCERT cert の `NOTAFTER` を過ぎた瞬間、AT-TLS handshake が `42`(certificate_expired) で失敗し、当該 listener 全停止。Db2 DRDA TLS / IPIC TLS / FTP-TLS 等が同時に全停止するのが site の「最悪日」。Health Checker `RACF_CERTIFICATE_EXPIRATION` を必ず active 化、warning 閾値を 60 日に設定。RACF DB unload `IRRDBU00` の CERTN record で全 cert 期限を抽出する月次 batch を仕掛けるのが site 規約として強い。
- **Key ring に同じ subject の cert 重複残置で意図しない方を使う**: renew で新 cert を ADD したが旧 cert を `REMOVE` / `DELRING` しないとkey ring に複数 cert が居座る。AT-TLS は default 属性付きを使うが、default を切り替え忘れると旧 cert を提示し続ける。`RACDCERT LISTRING(MYRING) ID(USER1)` で ring 内全件確認、`DEFAULT(YES)` が 1 つだけになっているか必ず確認。renewal 手順書に「ADD → DEFAULT 切替 → 旧 REMOVE」の order を明記。
- **Private key escape (export 経路)**: `RACDCERT EXPORT(LABEL('xxx')) DSN('user.export') FORMAT(PKCS12) PASSWORD(...)`で PKCS12 export すると、秘密鍵が外部 dataset に出る。site policy で **EXPORT 権限を RACF FACILITY class IRR.DIGTCERT.\* で厳格に制限** しないと、operator が誤って本番秘密鍵を平文 (password 弱)で抜き出す事故が起きる。EXPORT 系コマンドは SMF type 80 で監査ログを取り、四半期レビューする運用が監査要件として強い。
- **CRL / OCSP 取得失敗時の挙動が site 設定で異なる**: client cert 検証で CRL チェック有効化 (`CrlDistPoints On`) してると、CRL 配信元への HTTP 接続が落ちている時、AT-TLS が「fail open (検証スキップ)」か「fail close (拒否)」かは site policy 次第。fail open のままだとCRL サーバ DDoS された瞬間に失効 cert が通る穴。fail close なら CRL 配信元障害で本番停止。**OCSP stapling** で middle groundに倒すのが現代的だが site 整備に工数。
- **署名 algorithm SHA-1 残存で TLS 1.3 client から拒否**: 古い site では root CA が SHA-1 RSA で署名されていて、TLS 1.3 strict modeの client (Java 17+, Chrome 最新) が cert chain を拒否する。AT-TLS handshake は成功してるように見えるが client 側で reject されるため z/OS 側ログでは原因がわからない。`RACDCERT LISTCHAIN(LABEL('xxx'))` で chain 全件の signature algorithm を棚卸し、SHA-256 以上に再発行する移行計画が必要。

## 6. examples（具体例）

```
* 自己署名 root CA を作る
  RACDCERT CERTAUTH GENCERT                                  +
    SUBJECTSDN(CN('Internal Root CA')                        +
               O('Acme Corp') C('JP'))                       +
    WITHLABEL('INTROOT')                                     +
    NOTAFTER(DATE(2036-12-31))                               +
    SIZE(4096)
```

```
* server cert を生成して root で署名
  RACDCERT ID(DB2PROD) GENCERT                               +
    SUBJECTSDN(CN('db2.acme.jp')                             +
               O('Acme Corp') C('JP'))                       +
    WITHLABEL('DB2PROD-SRV')                                 +
    SIGNWITH(CERTAUTH LABEL('INTROOT'))                      +
    NOTAFTER(DATE(2027-06-02))

* key ring 構築
  RACDCERT ID(DB2PROD) ADDRING(DB2KR)
  RACDCERT ID(DB2PROD) CONNECT(LABEL('DB2PROD-SRV')          +
                              RING(DB2KR)                    +
                              DEFAULT)
  RACDCERT ID(DB2PROD) CONNECT(CERTAUTH LABEL('INTROOT')     +
                              RING(DB2KR))
```

```
* 棚卸し
  RACDCERT LIST(LABEL('DB2PROD-SRV')) ID(DB2PROD)
  RACDCERT LISTRING(DB2KR) ID(DB2PROD)
  RACDCERT LISTCHAIN(LABEL('DB2PROD-SRV')) ID(DB2PROD)
```

## 7. decision_axes（採否を分ける判断軸）

- **RACF DB 内秘密鍵 vs ICSF PKDS**: default は RACF DB に秘密鍵が clear 保管 (RACF DB 自体は暗号化されるsite policy 次第)。`PCICC` / `ICSF` 指定で PKDS に保管すると HSM 内secure key として漏洩経路を絞れる。だが ICSF 経路は handshake 演算ごとにPCI dispatch があり TLS 接続数が多い site で性能ボトルネック。**機密性最優先なら PKDS、throughput 優先なら RACF DB**、混在 ring も可。
- **内部 CA 自営 vs 外部 public CA**: 内部 mainframe 間通信なら自己署名 root + RACDCERT GENCERT で完結しコスト低 + 期限自由。外部 client (web ブラウザ等) が見るなら public CAが必須だが、年契約 + DNS-01 / HTTP-01 validation の運用工数。中規模の現実解: 内部 mainframe 間は自己 CA、border facing は public CA、の二段構成。1 つの key ring に両方乗せる。
- **renewal 自動化 vs 手動オペレータ運用**: RACDCERT は CLI で全部できるので Ansible (`zos_*` collection) で自動化可。だが renewal は cert chain trust 変動を含むため、自動化失敗時のロールバックが難しい。**1 年 cert は自動化、5 年 root は手動 + 立会**、という頻度別運用が site 規約として現実的。
- **key ring per application vs site 共通 ring**: application ごとに key ring を分けると認可が綺麗だが、cert renewal で全 ring を巡回更新する工数が増える。site 共通 ring に集約すると工数低いが application 間 cert 漏れ (用途違いの cert が見える) のリスク。規模 100 application 以上なら絶対 per-app、それ未満なら共通 ring + certlabel による論理分離が現実的。

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_TECH_001) から証明書管理 (RACDCERT) 運用知識を概念蒸留 (ADR-0109)。書籍は概念補助。
