---
title: ZOS-ICSF-001
description: CKDS / PKDS / TKDS、CCA / PKCS#11、Crypto Express 連携、master key ceremony
tags:
  - Middleware
  - Middleware-Utility
---
# ZOS-ICSF-001: ICSF (Integrated Cryptographic Service Facility) + CKDS/PKDS

## 1. purpose（なぜ存在するか）

ICSF は z/OS の **暗号鍵管理基盤 + 暗号演算ディスパッチャ** で、CKDS (対称鍵)、PKDS (公開鍵)、TKDS (PKCS#11 token) という 3 つの key dataset に master key で暗号化された鍵を保管し、application から `CSNBENC` / `CSNBDEC` / `CSNDPKE` などのcallable service が呼ばれた瞬間に Crypto Express ハードウェア (CEX5C / CEX6C / CEX7C 等) にディスパッチする。

Linux で openssl + pkcs11-tool + HSM (Thales / Utimaco) を自前で組むのに対し、ICSF は **z/OS 起動シーケンスに組み込まれ、master key ceremony を経た FIPS 140-2level 4 認証の Crypto Express と固定セット** で売られているため、鍵の漏洩経路がOS から見ても確認可能。AWS KMS のような「鍵は暗号サービス側に閉じ込める」クラウド KMS と思想は同じだが、master key を物理 ceremony で site 自身が握る点で根本的に違う (cloud KMS は AWS が master key を握る)。

## 2. mechanism（どう動くか）

- CKDS (Cryptographic Key Data Set): VSAM KSDS。対称鍵 (DES / TDES / AES) を
  master key で暗号化した形で保管。label をキーに lookup
- PKDS (PKA Key Data Set): VSAM KSDS。RSA / ECC の private key 保管
- TKDS (Token Data Set): PKCS#11 token / object 保管
- master key は **Crypto Express HSM 内** にしか平文存在しない。
  CKDS/PKDS は master key で暗号化された keytoken の集合
- master key の current / new / old の 3 register があり、change ceremony は
  new に load → CKDS 全件 reencipher → current swap、の順
- application は `CSFSERV` general resource class で個別 callable に対する
  実行認可を SAF で受け、許可されたら CSF 系プログラムが Crypto Express に
  PCI バス越しの coprocessor 命令を発行
- domain: 1 つの Crypto Express を複数 LPAR で論理分割。
  各 LPAR の `CSFPRMxx` で domain 番号を指定し、master key は domain 単位で別
- AES-NI 系の **CPACF (CPU Assist for Crypto Functions)** は HSM 不要な
  in-CPU 暗号で、ICSF callable がオフロード判断する

## 3. prerequisites（理解の前提）

- VSAM KSDS の基本 — `ZOS-VSAM-001`
- RACF general resource class の概念 — `ZOS-RACF-001`
- 対称暗号 / 公開鍵暗号 / 鍵管理ライフサイクル (一般 IT 知識)
- 略語: HSM = Hardware Security Module、CEX = Crypto Express

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-VSAM-001 (CKDS/PKDS は KSDS), ZOS-RACF-001 (CSFSERV class),
  ZOS-DATASET-001
- `specialized_by`: ZOS-PE-001 (PE は dataset 単位で ICSF を呼ぶ),
  ZOS-CERTMGMT-001 (RACDCERT は PKDS を経由)
- `contrasts_with`: Linux openssl + pkcs11 / SoftHSM, AWS KMS, Azure Key Vault
- `used_by`: ZOS-PE-001, ZOS-AT-TLS-001, ZOS-CERTMGMT-001, ZOS-DB2-001 (TDE)

## 5. pitfalls（実装・運用での落とし穴）

- **master key change で CKDS 再暗号化 (reencipher) 漏れ**: master key を change する時、ceremony は (1) new master key を HSM にload (2) CKDS 全 record を new MK で reencipher (3) new → current swap、の順。手順 (2) を飛ばして swap した瞬間、CKDS 全 keytoken が「現在の MKで復号できない」となり、本番 application 全停止。復旧は old MK が oldregister に残っている限り old に戻すしかなく、戻せなければ CKDS リストア。ceremony リハーサルで「reencipher 行のスキップ」を必ずやっておく。
- **Crypto Express domain 衝突**: 同じ CEX を 2 つの LPAR で同じ domain 番号で共有すると、片方が master keyload した瞬間にもう片方の CKDS が読めなくなる。原因は「domain 単位で masterkey が独立」という前提を運用が誤解していたケース。LPAR 設計時に domainマップ表を作り、production と DR で domain を分ける運用を徹底する。HMC の Image Profile → Crypto タブの domain assignment は IPL でしか反映されないため、誤設定の検出が IPL 後の本番異常まで遅れる。
- **CSFSERV class 不足で AT-TLS が cleartext fall-back**: AT-TLS handshake で RSA private key 演算が必要だが、Policy Agent ID に`CSFSERV CSNDDSG` (digital signature generate) の READ が無いと`ICH408I` で reject。AT-TLS は **エラーで切るのではなく無暗号 fallback**(or 完全切断、policy 次第) になる site があり、結果として cleartext通信が黙って通る。SAF 監査で CSFSERV class READ 全件を必ず確認する。ベンダ製 ICSF setup 手順書には書いてないことが多い。
- **AES vs DES 互換性で Db2 TDE が beforestyle に**: Db2 TDE (Transparent Data Encryption) で鍵 algorithm を DES → AES に切替えた後、古い backup dataset を RESTORE すると **古い algorithm で暗号化されたまま** の page が混在。Db2 は label 単位で algorithm を識別するため通常は読めるが、key label を再利用して AES 化した場合old DES backup が復号できない事故。鍵 label 命名規約に algorithm を含める (`PROD.DB2.TDE.AES256.001` 等) のが site 規約として強い。
- **ICSF 起動順序ミスで Db2 / CICS が ICSF unavailable で起動**: ICSF は IPL 直後の started task で起動するが、CSFPRMxx 読込 + CKDS open+ HSM init で 30-60 秒かかる。COMMNDxx で Db2 / CICS を ICSF より先にS(tart) すると、subsystem は「暗号機能なし」で起動し、TDE 対象 tableへの INSERT が暗号化されない / KeyRing 経由 SSL listener が無効化される。COMMNDxx で ICSF → STARTED class の DB2/CICS 起動順を厳守、ARMrestart group も依存関係を反映させる。

## 6. examples（具体例）

```
* CSFPRMxx parm (PARMLIB) 例
  CKDSN(SYS1.CSF.CKDS)        /* CKDS dataset */
  PKDSN(SYS1.CSF.PKDS)
  TKDSN(SYS1.CSF.TKDS)
  DOMAIN(3)                    /* Crypto Express domain */
  COMPAT(NO)
  SSM(YES)                     /* Special Secure Mode (test 用、本番は NO) */
```

```
* RACF CSFSERV class 設定例 (AT-TLS から RSA 署名するための最小許可)
  RDEFINE CSFSERV CSNDDSG UACC(NONE)
  PERMIT CSNDDSG CLASS(CSFSERV) ID(PAGENT) ACCESS(READ)
  SETROPTS CLASSACT(CSFSERV) RACLIST(CSFSERV)
```

```
* CKDS の key label 確認 (TSO ICSF panel or CSFKGUP utility 経由)
  // 例: CSFKEYS class で label 単位の利用認可を設定可能
  RDEFINE CSFKEYS PROD.AES256.TABLEKEY UACC(NONE)
  PERMIT PROD.AES256.TABLEKEY CLASS(CSFKEYS) ID(DB2PROD) ACCESS(READ)
```

## 7. decision_axes（採否を分ける判断軸）

- **Crypto Express (HSM offload) vs CPACF (CPU 内蔵暗号)**: CPACF は CPU 命令 (KMAES / KMC など) で AES / SHA を直接実行する高速経路だが鍵が main storage 上に平文で存在する瞬間がある (clear key)。Crypto Express は鍵が HSM 内部 (secure key) に閉じる代わりに PCIディスパッチで遅い。**FIPS 140-2 level 4 必須 / 鍵分離要件あり** なら CEX、**TLS 大量 handshake / Db2 TDE のように throughput 優先** なら CPACF 中心、という選択。混在も可。
- **CKDS share (sysplex 共有) vs LPAR 個別**: CKDS を sysplex 共有 (XCF + VSAM RLS) すると鍵集中管理で運用楽だが、1 つの破損 / encryption error が全 LPAR の暗号機能停止に伝播。LPAR 個別 CKDS は冗長性高いが、鍵 sync 運用が手動で重い (production と DR のlabel 一致を ceremony 経由で担保)。site 規模と DR RPO 要件で判断。
- **master key ceremony 担当の 2 人鍵管理 vs single custodian**: FIPS 140-2 level 4 では **2 人鍵管理** (両者の knowledge component を XORしてから入力) が事実上必須。だが ceremony 工数 (2 人スケジュール + 物理金庫から smart card 取出 + 立会監査) が増える。single custodian は速いが監査要件で却下されることが多い。small site で監査要件が緩い場合のみ single 可。
- **Key change 周期: 年 1 回固定 vs インシデント駆動**: PCI DSS は「定期的に change」と曖昧、site policy で年 1 回 / 3 年 / 暴露時など決める。年 1 回は ceremony 慣れができ事故率低いが工数高い。インシデント駆動は工数安いが「いざ」の時にリハ不足で reencipher 漏れ事故が起きる確率が跳ね上がる。site の change advisory board で年次定例とするのが結局安全。
