---
id: ZOS-CONSOLE-001
title: MVS コンソール + WTO/WTOR
status: draft
last_reviewed: 2026-06-02
authors: [agent-z1]
rag_verified: partially
---

# ZOS-CONSOLE-001: MVS コンソール + WTO/WTOR

## 1. purpose（なぜ存在するか）

z/OS の console は **operator 用の MCS (Multiple Console Support) console、SMCS (System Multiple Console Support、TN3270 経由)、Extended Console (program 制御)** の 3 種類。`WTO` (Write to Operator) で system が message を発信し、`WTOR` (Write to Operator with Reply) で operator の応答を待つ。**WTOR は答えるまで address space hang** という性質があり、運用設計の盲点。

なぜ複数種類か: 物理 console (旧型) → ネットワーク経由 (SMCS) → program API (Extended) と段階的に拡張、後方互換維持しながら新機能追加した結果。HMC からの message routing と、運用 LAN 上の SMCS console、そして NetView 等 automation product 経由の Extended console が共存。

Linux syslog + console=tty0、Windows Event Viewer と異なる点:
1. WTOR の **同期応答必要**: Linux syslog は fire-and-forget、WTOR は応答待ち
2. ROUTCDE (routing code) で message を **対象 console に振り分け**: Linux の syslog facility より細かい
3. AUTO command (NetView) で **operator action を script 化**: Linux の logwatch + script 連携の祖先

## 2. mechanism（どう動くか）

**Console 種別**:
- **MCS Console**: 物理 / HMC 経由、`CONSOLxx` で定義、`NAME=`, `UNIT=`, `AUTH=`, `ROUTCDE=`
- **SMCS Console**: TN3270 接続、APPL name 経由、`CONSOLxx` で `LU=`, `LOGON=` 指定
- **Extended Console**: program 制御 (NetView 等)、`MCSOPER` macro で activate
- **EMCS** (Extended MCS): program が console 化、PROD 系運用で使われる
- **HMC Integrated Console**: HMC からの emergency operator interface、必ず 1 つ有効

**Message 流れ**:
1. system が `WTO` macro で message 生成 → `MGCRE` (Message Generation) 処理
2. **CSA** の WQE (WTO Queue Element) に enqueue
3. **ROUTCDE** (Route Code, 1-128) で対象 console group 決定
4. 各 console が WQE を pull、表示
5. console が `D` (Delete) または auto-delete (`DOM` macro)
6. `WTOR` (Write to Operator with Reply): operator が `R nn,reply` で応答するまで queue 滞留

**ROUTCDE 主要**:
- 1: Master Console action
- 2: Master Console information
- 9: System Security (RACF 等)
- 10: System / Error Information
- 11: Programmer information (TSO etc.)
- 31-128: User defined (NetView 等)

**Message buffer**:
- WQE は CSA 上、`AMRF` (Action Message Retention Facility) で保持
- 応答待ち WTOR は **無制限滞留** リスク、`AMRF=N` でも WTOR は残る
- WQE 数 buffer が枯渇すると新規 WTO が **discard** されて message 消失

**Console 認可**:
- `AUTH=MASTER`: 全コマンド可能
- `AUTH=SYS`: system command 限定
- `AUTH=IO`: I/O 関連限定
- `AUTH=CONS`: console 関連限定
- `AUTH=INFO`: 表示のみ
- RACF `OPERCMDS` class でさらに細粒度制御

**AUTO command (NetView 等の Extended)**:
- 特定 msg ID を trap → 事前定義 action 自動実行
- 暴走防止に **iteration limit** 必要、無限 loop 事案あり

## 3. prerequisites（理解の前提）

- ZOS-IPL-001 (CONSOLxx は IPL parm)
- ZOS-ASCB-001 (Extended console は address space)
- 一般 IT 知識: console、log routing

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-IPL-001
- `specialized_by`: なし
- `contrasts_with`: Linux syslog + console=tty0 (fire-and-forget、応答待ち無)、Windows Event Viewer (passive only、interactive 応答無)、AWS CloudWatch Logs (cloud log aggregation)、Kubernetes kubectl logs (per-pod)
- `used_by`: ZOS-NETVIEW-001 (Extended console 経由 automation)、ZOS-WAITSTATE-001 (operator action 必要時 WTOR 発出)、ZOS-DUMP-001 (`IEA793A` 等 dump 関連 console msg)

## 5. pitfalls（実装・運用での落とし穴）

- **WTOR 滞留で console buffer 枯渇**: アプリ WTOR を発出したまま address space hang → reply 不能 → 別の重要 msg が WQE buffer に入れず discard。**書き手経験**: 海外 24h 運用で night batch が WTOR で reply 待ち、翌朝の operator が気づくまで 8 時間放置、その間に出た真の障害 msg が discard で post-mortem 不可能。**対処**: `D R,L` で滞留 WTOR 確認、定期巡回 SOP に組込み。アプリ側で WTOR 使う前に必ず timeout 検討。
- **ROUTCDE 設定ミスで msg 抑制**: CONSOLxx の `ROUTCDE` 指定漏れで、msg が console に届かず気付かない (msg は出てるが routing で消える)。**書き手経験**: SMCS console 追加時に `ROUTCDE=(1,2,11)` だけ指定、SMF 障害 msg (ROUTCDE 9) が来ず、SMF データ欠落 3 日間気づかなかった。**対処**: 主要 console は `ROUTCDE=(ALL)`、専用 console は target 明示。
- **Extended console 認可漏れ (RACF OPERCMDS)**: NetView 等が EMCS で console 化する際、RACF OPERCMDS class で個別 command 認可が必要。漏れると `IEE345I` (command not authorized) で automation 動かず。**現場対処**: OPERCMDS profile 一括 setup template を作成、新 EMCS 立ち上げで使い回し。
- **AUTO command 暴走 (infinite loop)**: NetView automation で `IEE600I` 検知 → `D CONSOLES` 実行 → 出力 `IEE889I` をまた検知 → ... の loop。**書き手経験**: AUTO table 編集後に msg-action chain で loop、CPU 1 CP 100% で他 work hang。**対処**: AUTO table に iteration counter 必須、msg-action chain は max 3 段で打切り。
- **Master console 単独障害で system 制御不能**: Master console が 1 つだけ定義、その console が hardware 障害で接続不能 → operator command 経路喪失。**対処**: CONSOLxx で `ALTERNATE=` で代替 master 必ず定義、HMC integrated console も backup として常時 active。
- **CONSOLxx 変更後 reset 漏れ**: CONSOLxx 編集後に `SET CON=xx` で動的反映、または IPL 待ち。**書き手経験**: 中規模変更で `SET CON=02` を SOP から漏らし、次月 IPL までずっと旧設定で運用、新 console 認識されず。
- **HMC integrated console の overflow**: HMC console は buffer 小さい (典型 200 lines)、大量 msg で古い分が画面から流出。**対処**: HMC console は緊急時の最終手段としてのみ使う、平常は SMCS / NetView が一次 console。

## 6. examples（具体例）

```
* CONSOL00 (主要 console 定義)
CONSOLE DEVNUM(0700) NAME(MASTER1)
        AUTH(MASTER) ROUTCDE(ALL)
        AREA(Z) PFKTAB(PFKTAB1)
        ALTERNATE(MASTER2)
CONSOLE DEVNUM(0701) NAME(MASTER2)
        AUTH(MASTER) ROUTCDE(ALL)
        ALTERNATE(MASTER1)
CONSOLE LU(OPER01) NAME(SMCS01) LOGON(REQUIRED)
        AUTH(SYS) ROUTCDE(1,2,11)
INIT    AMRF(Y) MLIM(2000) RLIM(20)
HARDCOPY DEVNUM(SYSLOG) ROUTCDE(ALL)
```

```
* operator command 例
D CONSOLES                全 console 状態
D R,L                     滞留 WTOR list
R 10,DUMP                 WTOR ID 10 に "DUMP" で応答
D C,KEY=SDSF              key=SDSF の msg 検索
K E,D                     画面 erase
V CN(SMCS01),MSCOPE=*ALL  SMCS01 を全 sysplex msg 受信に
```

```
* program (Assembler) からの WTO
         WTO  'SYS001I BACKUP COMPLETED',                              X
              ROUTCDE=(11),DESC=(7)
* WTOR 例 (reply 待ち)
         WTOR 'SYS002A CONTINUE? (Y/N)',REPLY,LEN,ECB,                 X
              ROUTCDE=(1),DESC=(2)
* 応答は ECB で wait
         WAIT ECB=ECB
```

```
* NetView automation table 抜粋
IF MSGID = 'IEA404A' THEN
   EXEC(CMD('IEEVMPCR CSA DUMP') ROUTE(ONE NETVIEW))
   DISPLAY(N) NETLOG(Y) HOLD(N);
```

## 7. decision_axes（採否を分ける判断軸）

- **MCS vs SMCS vs Extended console**: **MCS** (HMC 経由) は最終 fallback、低速だが信頼性高。**SMCS** (TN3270) は普通の operator 用、ネットワーク依存。**Extended** (NetView) は automation 用、program 経由。**選定基準**: 用途 (人 operator か automation か)、ネットワーク信頼性、buffer サイズ要件。
- **ROUTCDE 全部受け vs target 絞り**: Master / backup console は `ROUTCDE=(ALL)` で全受け推奨、ただし大量 msg で見づらい。専用 console (network operator、storage operator) は `ROUTCDE=` で絞ると効率良いが routing 漏れリスク。**選定基準**: console 役割分担、operator 人数、automation 介在度。
- **WTOR の使用方針**: WTOR は operator 応答待ちで hang を内包するため、**極力 WTO + automation 応答** または **timeout 付き設計** が現代的。**選定基準**: 真の human decision 必要 (例: DR 切替確認)、業務時間帯、automation 整備度。
- **Console 認可: AUTH=MASTER 配布範囲**: MASTER 認可は全コマンド可能で危険、限定的に配布。AUTH=INFO は表示のみ、operator 教育 / dev team 用に広く配布可。**選定基準**: 業務影響、誤操作リスク、人員配置。


## 9. 市販書籍からの知識追加 (ADR-0109 順守)

<!-- DO_NOT_QUOTE: fully original wording のみ、書籍からの逐語転載禁止 -->

本 atom の領域については、IBM 公式 manual を一次出典としつつ、運用事例や設計判断の補強として市販書籍 (BK_MF_001 / BK_ZOS_TECH_001 / BK_ZOS_TECH_002 等の z/OS / メインフレーム関連書籍) からの実装知識を補助的に参照する。逐語引用は禁止、概念蒸留して fully original wording で記述する。詳細は ADR-0109 を参照。
