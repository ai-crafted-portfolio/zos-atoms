---
title: ZOS-ARM-001
description: element 登録、restart group、policy、CICS/IMS/DB2 連携
tags:
  - Recovery
  - Recovery-Workload
---
# ZOS-ARM-001: ARM (Automatic Restart Manager)

## 1. purpose（なぜ存在するか）

ARM（Automatic Restart Manager）は z/OS の **Sysplex 範囲 process supervisor**。CICS / IMS / Db2 / MQ / 自製 STC 等の重要 address space が **abend / OS hang / LPAR 喪失** したとき、ARM が policy に基づき (a) **同一 LPAR で restart**、(b) **別 LPAR に cross-system restart**、(c) **依存関係を保ったグループで一斉 restart** する。Sysplex 高可用性の核。

Linux なら `systemd Restart=on-failure` や Kubernetes の pod restart policy、Pacemaker / Corosync の resource manager が対応する。違いは ARM が **Sysplex 全体**（最大 32 LPAR）に跨り、CF（Coupling Facility）の ARM couple data set で policy / element 状態を共有し、LPAR 自体が消えても他 LPAR が拾う **cross-system failover**。Kubernetes の node failover に近いが、メインフレームの場合 1 LPAR = 1 ノード規模が遥かに大きい（数千 tx/sec の OLTP）。

なぜ subsystem 個別 restart 機能で足りないか: CICS は自己 restart 機構を持つが、CICS 単体が落ちたとき **同時に依存する Db2 / MQ が無傷で残る** とき、CICS だけ restart する vs 全部一緒に restart する vs 順序付き restart する、の判断を組織が policy として記述したい。ARM はその **policy 記述言語と enforcement engine** を提供する。

## 2. mechanism（どう動くか）

### 中核オブジェクト
- **Element**: ARM 管理対象の address space。`IXCARM REQUEST=REGISTER` で登録、Element name は 16-byte（CICS region 名等）。
- **Element type**: SYSCICS / SYSIMS / SYSDB2 / SYSMQ / SYSIWAS / SYSOTHER 等。type 毎にデフォルト restart 動作。
- **Restart group**: 複数 element を束ねた論理 group。同一 group 内の element は **同時 down → 同時 restart** が原則。
- **Restart method**: PERSIST（同 LPAR）/ ELEMTERM（element 終了通知のみ）/ STOP（明示停止扱い）。
- **TARGET_SYSTEM**: cross-system restart 先の候補 LPAR list。

### policy 構造
- **ACTIVE policy**: `IXCMIAPU` utility で ARM couple data set に書き込み、`SETXCF START,POLICY,TYPE=ARM,POLNAME=...` で active 化。
- **Policy 要素**:
  - `RESTART_GROUP(MYGROUP)`: group 定義
  - `ELEMENT(CICSPROD*)`: element name pattern
  - `RESTART_ATTEMPTS(3,300)`: 最大 3 回、300 秒 window
  - `RESTART_METHOD(PERSIST,JCL,'CICS.PROCS(START)')`
  - `RESTART_ORDER(LEVEL(1))`: 起動順序の数値
  - `RESTART_TIMEOUT(300)`: restart command 実行制限
  - `READY_TIMEOUT(600)`: READY 到達制限
  - `TARGET_SYSTEM(SYSA,SYSB,SYSC)`: cross-restart 候補

### 動作フロー
- Element abend 検出 → ARM が SDWA から restart trigger → policy 照合 → restart group 全 element に **同時 STOP** 通知 → policy の RESTART_METHOD で起動 → element 側で `IXCARM REQUEST=READY` 発行 → ARM が「element ready」と判定。
- LPAR 喪失検出（XCF が SYSGONE 検知）→ ARM policy の TARGET_SYSTEM list で残存 LPAR 順次試行 → cross-system restart。

### ARM 状態確認
- `D XCF,ARMSTATUS` で element / group / status
- `D XCF,ARMSTATUS,POLICY` で active policy 名
- `D XCF,ARMSTATUS,DETAIL,STARTED` で起動中 element
- `D XCF,POLICY,TYPE=ARM` で full policy dump

## 3. prerequisites（理解の前提）

- Parallel Sysplex / XCF — `ZOS-PARALLELSYSPLEX-001`
- CICS / IMS / Db2 等 subsystem の起動 JCL / start command
- 一般 IT 知識: 高可用性、failover、依存関係グラフ

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-PARALLELSYSPLEX-001
- `specialized_by`: なし
- `contrasts_with`: Linux systemd Restart= + Pacemaker resource manager, Kubernetes pod restart policy + Deployment / StatefulSet, AWS Auto Scaling group health check
- `used_by`: ZOS-CICS-001（CICSplex 全体の cross-system restart）, ZOS-IMS-001（IMS DBCTL restart）, ZOS-DB2-001（Db2 member restart）, ZOS-MQ-001（MQ queue manager restart）

## 5. pitfalls（実装・運用での落とし穴）

- **Element ID 命名衝突**: CICSPROD と CICSPRO* で element name pattern が重なって、policy 照合で **意図しない group** に CICS が入る。CICS が落ちて Db2 group の restart trigger が走り、無関係 Db2 が再起動される事故。**element name は明示 fully qualified（`CICSPROD1`, `CICSPROD2`）、pattern は不使用**、または pattern なら命名規約を 全 element 横断で精査。
- **Restart group 順序逆転で依存先 down**: Db2 が先に restart して、その上で CICS が restart する設計で、`RESTART_ORDER(LEVEL(...))` を逆に書いて CICS が Db2 unavailable で起動失敗 → ARM が `RESTART_ATTEMPTS` カウント消費 → maxout → CICS 起動放棄。**dependency graph を書いて RESTART_ORDER LEVEL 数値で表現**、テスト系で必ず crash test。
- **Restart 試行回数上限到達放置**: `RESTART_ATTEMPTS(3,300)` で 3 回 fail すると ARM は以降 restart しない（policy 上はそういう設計）。運用者が monitor してないと **CICS が落ちたまま** 業務停止。**ARM exhausted を NetView automation で `D XCF,ARMSTATUS` 1 分間隔監視 + alarm**、休日 / 深夜帯に CICS が落ちて気付かない事故。
- **ARM policy activate 漏れ**: `IXCMIAPU` で policy を書き込んでも `SETXCF START,POLICY,TYPE=ARM,POLNAME=NEWPOL` を実行しないと反映されない。本番投入前テストで activate 忘れて「テスト OK だったのに本番動かない」報告。**policy 更新 SOP に activate command を組込む + `D XCF,POLICY,TYPE=ARM` で確認**。
- **TARGET_SYSTEM list の自 LPAR 含み**: TARGET_SYSTEM に自身（落ちた LPAR）を入れると、LPAR 喪失時の cross-restart で **「自分自身に restart 試行 → 失敗 → 次候補」** で時間 loss。**TARGET_SYSTEM は明示的に「自身を除く健全 LPAR list」**、Sysplex 動的拡張時に list 更新も忘れない。
- **READY_TIMEOUT 過大で異常検出遅延**: `READY_TIMEOUT(3600)` で 1 時間に設定すると、CICS が起動 hang してても 1 時間気付かない。**READY_TIMEOUT は本番 CICS の通常起動時間 x3 以内**（CICS が 5 分で ready なら 15 分）、SAP のような重い application でも 30 分以内。
- **ARM couple data set の容量 / format**: ARM 用 CDS（COUPLExx の ARM CDS 定義）が小さい / format mismatch だと `IXC*` メッセージで policy load 失敗 → ARM 機能停止。**Sysplex 拡張時に CDS reformat + Spare CDS 用意 + IPL 前テスト**、CDS 不足は気付きにくい長期化障害源。

## 6. examples（具体例）

```text
* IXCMIAPU 用 policy 定義 (抜粋)
DATA TYPE(ARM) REPORT(YES)
  DEFINE POLICY NAME(PRODPOLI) REPLACE(YES)
    RESTART_GROUP(CICS_GROUP)
      RESTART_PACING(0)
      FREECSA(8,16)
      ELEMENT(CICSPROD1)
        RESTART_ATTEMPTS(3,300)
        RESTART_METHOD(BOTH,JCL,'CICS.PROCS(STARTPRD1)')
        RESTART_ORDER(LEVEL(2))
        READY_TIMEOUT(600)
        TARGET_SYSTEM(SYSA,SYSB)
      ELEMENT(CICSPROD2)
        RESTART_ATTEMPTS(3,300)
        RESTART_METHOD(BOTH,JCL,'CICS.PROCS(STARTPRD2)')
        RESTART_ORDER(LEVEL(2))
        TARGET_SYSTEM(SYSA,SYSB)
    RESTART_GROUP(DB2_GROUP)
      ELEMENT(DB2PROD)
        RESTART_ATTEMPTS(5,600)
        RESTART_METHOD(BOTH,JCL,'DB2.PROCS(STARTDB2)')
        RESTART_ORDER(LEVEL(1))
        TARGET_SYSTEM(SYSA,SYSB,SYSC)
```

```text
* policy activate
SETXCF START,POLICY,TYPE=ARM,POLNAME=PRODPOLI

* 状態確認
D XCF,ARMSTATUS
D XCF,ARMSTATUS,DETAIL,STARTED
D XCF,POLICY,TYPE=ARM

* element の手動 deregister (restart 抑止)
SETXCF DEREGISTER,ELEMENT=CICSPROD1
```

```text
* element 側 (subsystem) の IXCARM 呼出概念
* CICS / IMS / Db2 は内部で自動呼出するが、自製 STC は明示
*
* 起動時:
*   IXCARM REQUEST=REGISTER,ELEMENT=MYSTC1,ELEMTYPE=SYSOTHER
*
* ready 到達時:
*   IXCARM REQUEST=READY,ELEMENT=MYSTC1
*
* 正常停止時 (restart したくない時):
*   IXCARM REQUEST=DEREGISTER,ELEMENT=MYSTC1
```

## 7. decision_axes（採否を分ける判断軸）

- **ARM 全使用 vs 一部 subsystem のみ**: ARM は CICS / IMS / Db2 / MQ で **subsystem 既定で自動 register**（element type 経由）。これを policy で抑制すると subsystem 個別 restart 機構（CICS auto-restart 等）に戻る。**Sysplex 構成では ARM 全使用、単一 LPAR では subsystem 個別** が住み分け。
- **Restart group 粒度**: 1 group 1 element（個別管理）vs 1 group 複数 element（依存込み一括）。**CICS + Db2 のような業務依存は同 group、独立 STC は別 group**。group 大きすぎ → 1 element abend で全体 restart の波及。
- **Cross-system restart の許可範囲**: TARGET_SYSTEM に全 LPAR 入れると、どこでも restart 可能だが「テスト LPAR で本番 CICS 起動」事故。**production element は production LPAR のみ TARGET_SYSTEM**、policy に明記。
- **RESTART_ATTEMPTS 設計**: (1,60) 〜 (5,3600) の幅。**OLTP は (3,300) 短期集中、batch は (1,60) 1 度だけ、開発系は (0,0) ARM 無効化** の使い分け。
- **READY_TIMEOUT 設定**: subsystem 起動の **実測 + バッファ**。CICS 通常 5 分 → READY_TIMEOUT(900) の 3 倍バッファ。**過小で false alarm、過大で異常検知遅延** のトレードオフ。
- **ARM monitor + automation**: `D XCF,ARMSTATUS` を NetView / OMEGAMON で監視する vs しない。**監視ない ARM は「policy 動いたかどうかすら不明」**、policy 評価が運用 SOP で組まれてない組織は ARM を機能させてないのと等価。
