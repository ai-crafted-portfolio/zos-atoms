---
id: ZOS-SAF-001
title: System Authorization Facility (SAF) callable services
status: stable
last_reviewed: 2026-06-02
authors: [Z2]
rag_verified: true
---
# ZOS-SAF-001: System Authorization Facility (SAF) callable services

## 1. purpose（なぜ存在するか）

SAF は z/OS の **認可検査の単一窓口** で、RACF / ACF2 / TSS どの製品が下に居ても、OS / subsystem / アプリケーションは同じ macro (RACROUTE) を呼ぶだけで認証・認可・監査が貫通する設計。これは「セキュリティ製品を差し替えても、Db2 / CICS / TCP/IP の SAF 呼出コードは 1 行も書き換えなくていい」という抽象化レイヤの実体。

Linux の PAM が `/etc/pam.d/<service>` の stack 設定で同等のことを狙うのに対し、SAF は **OS kernel コードパスに macro 展開で組み込まれている** ため、未認可呼出をアプリ側で迂回できない。Windows の Security Reference Monitor (SRM) と思想は近いが、SAF は **SMF type 80 監査レコードに直結** している点で監査要件 (PCI / SOX) との親和性が桁違いに高い。

## 2. mechanism（どう動くか）

- `RACROUTE REQUEST=AUTH,CLASS=...,ENTITY=...,ATTR=READ|UPDATE|CONTROL|ALTER` で
  リソース単位の認可検査。RC=0/4/8 + reason code が返る
- `RACROUTE REQUEST=VERIFY` は ACEE (Access Control Environment Element) を構築する
  認証経路 (TSO LOGON / batch JOB / started task の入口で必ず通る)
- 抽象化の hook 点は **router exit ICHRTX00**。ここで pre-processing exit が動き、
  本体の RACF / ACF2 / TSS callable に渡る前にリクエスト書換 / 拒否ができる
- post-processing は `ICHRTX01` (post-routing) 経路で、callable 返却後の SMF
  type 80 出力前に介入可能
- `RACROUTE REQUEST=STAT` でクラス定義 (RACLISTed か否か等) を問い合わせる。
  resource class が未定義だと `RC=8 reason=4` が即返り、application 側で誤った
  「拒否」と区別がつかず誤動作の温床
- ACEE は ASCB->ASXBSENV 経由で **address space 内 task 共有**。
  cross-memory mode (SRB) では home / primary / secondary の ASCB 別に ACEE が違う
  ため、`ENVIR=CREATE` の ACEE swap で誤った ID 検査になる事故が起きる
- SAF callable は **PSW key 0 / supervisor state** を前提とする。
  problem state からの誤呼出は S0C4 / S0C6 で即死

## 3. prerequisites（理解の前提）

- RACF 基本: profile / class / UACC / discrete vs generic — `ZOS-RACF-001`
- ASCB / ACEE の構造 — `ZOS-ASCB-001` (Z1 起案)
- cross-memory mode と PC routine (SRB scheduling の基礎)
- 一般 IT 知識: 認可 vs 認証の区別、reference monitor pattern

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-RACF-001, ZOS-ASCB-001
- `specialized_by`: ZOS-ACEE-001 (Z3 起案), ZOS-RACF-ADV-001 (Z3 起案)
- `contrasts_with`: Linux PAM (`/etc/pam.d/`), Windows Security Reference Monitor
- `used_by`: ZOS-DB2-001, ZOS-CICS-001, ZOS-IMS-001, ZOS-TCPIP-001 (Z3 起案),
  ZOS-WAS-001 (Z1 起案), ZOS-ICSF-001 (CSFSERV class 検査)

## 5. pitfalls（実装・運用での落とし穴）

- **ICHRTX00 exit が reentrant でなく address space 跨ぎでデータ破壊**: 自前で SAF exit を書く時、static storage (CSECT 内 DC) に working area を置くと、複数 address space から同時呼出された瞬間にデータ競合。症状は不定期 S0C4 / 異常認可結果 / SMF 80 record の ID 欄が別ジョブに化ける。原因切り分けが極めて困難で「半年経って気付く」典型例。exit 内では必ず `STORAGE OBTAIN SP=230 KEY=0 LENGTH=...` で getmain した領域を使う。CSA 起源の領域共有も禁則 (SQA / private にする)。
- **Pre/Post exit 順序勘違いで認可逆転**: pre-processing exit で `RC=0` を返すと **本体 RACF callable をスキップ**して認可 OK 扱いになる。「ログだけ取りたかった」exit が誤って RC=0 をセットして全リソースが UACC=NONE のクラスでも素通りした事例あり。exit は default で **入力を改変せず処理継続させる**。RC は触らない。コーディング規約として `STM/LM` の前後で R15=0 が居残ってないかレビューゲートを入れる必要がある。
- **Resource class が未 ACTIVE で SAF 検査が素通り**: 新規 general resource class を IRRRDB00 で定義したが、`SETROPTS CLASSACT(クラス名)` を打ち忘れたら、 `RACROUTE REQUEST=AUTH` は`RC=4 reason=4` (class not active) を返す。application が RC=4 を「access OK の意味」と誤実装すると、profile を作っても **保護されてない**。これは IBM redbook どこにも書いてない実害で、SAF return code 4 を認可 OK と扱う application 実装が SI ベンダ品に多数存在する。
- **ICHRIN03 ID propagation 不整合で started task が anonymous**: started task の ID は `ICHRIN03` テーブル (STARTED class が無い旧式) or STARTED class で決まる。両方定義があると **STARTED class が優先** だが、ICHRIN03 だけ更新して LLA 再 link しないと旧 ID で起動する。結果、SAF 認可で `USER=` が想定 task ID と違い、dataset 認可で reject。症状は `ICH408I` 連発だが「なぜか権限あるはずの ID で reject」となる。STARTED class への完全移行と ICHRIN03 廃止を強く推奨。
- **RACROUTE STAT の RC を AUTH と同じ意味で解釈**: `REQUEST=STAT` は class の登録状況を返すだけで認可結果ではない。RC=0 は「class 定義あり」、RC=4 は「class 不明 / 未 active」。ベンダ製ツール (特に 1990 年代の COBOL 製 monitoring tool) が STAT のRC=0 を「access 許可」と扱う実装ミスがあり、resource profile を作って保護したつもりが **全員 access 可** のままだったというインシデントが実在する。SAF 経路を呼ぶ自前コードは AUTH と STAT を厳密に区別する。

## 6. examples（具体例）

```assembler
* RACF authority check (READ access to dataset)
         RACROUTE REQUEST=AUTH,                              C
               CLASS='DATASET',                              C
               ENTITY=DSNAME,                                C
               ATTR=READ,                                    C
               WORKA=SAFAREA
         LTR   R15,R15
         BNZ   ACCESSDENIED      RC=0 means access permitted
```

```
* SETROPTS — class を ACTIVE にして RACLIST しないと SAF 検査が意図通り動かない
  SETROPTS CLASSACT(MYCLASS)
  SETROPTS RACLIST(MYCLASS)
  SETROPTS GENERIC(MYCLASS)
```

```
* ICH408I (拒否) 解析の鍵: INSUFFICIENT ACCESS AUTHORITY 行に
  実際に検査された CLASS / ENTITY / ATTR / 現在の access level が出る。
  ICH408I USER(...) GROUP(...) NAME(...)
    DATASET XXX.YYY.ZZZ
    INSUFFICIENT ACCESS AUTHORITY
    FROM ... (G)
    ACCESS INTENT(UPDATE)  ACCESS ALLOWED(READ)
```

## 7. decision_axes（採否を分ける判断軸）

- **自前 SAF exit を書く vs RACF profile + program control で済ます**: 自前 exit は柔軟だが (a) reentrant / addressing mode の難度が高い (b) RACF maintenance PTF で互換崩壊する (c) IPL 必要な反映が多い。profile + program control (PROGRAM class) で済むなら絶対そちらを選ぶ。exit が要るのは「監査要件で特定 ID の特定リソース access を全件 SMF 80に焼き付ける」など profile 機能で表現できないケースに限る。
- **RACROUTE REQUEST=VERIFY (新規 ACEE) vs VERIFYX (既存延伸)**: VERIFY は ACEE を新規構築する正攻法。ID/password 認証 + group 取込 + ACEE storage allocate のフルコース。VERIFYX は既存 ACEE を借りて別 task に紐付ける延伸経路で、surrogate / submit-by 系で使う。VERIFYX は速いが ENVIR=DELETE 忘れで ACEE leak しやすい。long-running daemon は ACEE 再利用設計を入念に。
- **SAF 経路で SMF 80 を出すか、application で別 log dataset を出すか**: SMF 80 経路は監査 SSOT として強力だが、SMF buffer / log stream の容量設計が必要で、高頻度認可検査の application で SMF 80 出しっぱなしにすると BUFFCRIT / LOSTDATA が出る。低頻度の認可結果は SAF、業務イベントの application log は別 dataset、と切り分けるのが定石。両方 SMF に寄せたい欲求は OPERLOG logstream と相談。
- **exit 入替 vs PTF 適用順序**: 自前 SAF exit を入れている site は、RACF PTF 適用前に exit の**control block layout 依存箇所** を再検査する必要がある。exit を抜いて素の RACF に戻すか、PTF 当てる前に exit を入れ替えるか、の段取りは site 個別判断。「とりあえず PTF 当てる」運用は ICH408I 全件通過 (= 全 access OK) の本番事故を起こす最頻パターン。


## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

本 atom の領域については、IBM 公式 manual を一次出典としつつ、運用事例や設計判断の補強として市販書籍 (BK_MF_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 等の z/OS / メインフレーム関連書籍) からの実装知識を補助的に参照する。逐語引用は禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
