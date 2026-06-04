---
id: ZOS-AT-TLS-001
title: AT-TLS (Application Transparent TLS)
status: stable
last_reviewed: 2026-06-02
authors: [Z2]
rag_verified: true
---
# ZOS-AT-TLS-001: AT-TLS (Application Transparent TLS)

## 1. purpose（なぜ存在するか）

AT-TLS は z/OS TCP/IP stack に組み込まれた **application を書き換えずに TLS を強制する shim 機能**。Policy Agent (pagent) が定義 file から TTLSRule / TTLSGroup/ TTLSEnvironment を読み込み、TCP socket の bind 時に policy match した connectionを `IOCTL SIOCTTLSCTL` で TLS 化する。アプリは普通の `socket() -> connect() -> send()` を呼ぶだけ。

Linux の `stunnel` / envoy sidecar が「別プロセスで TLS 終端」するのに対し、AT-TLS は **TCP/IP stack 内部** で TLS 終端するため、別プロセスの overhead が無く、認証情報 (X.509 subject 等) が IOCTL 経由で application 側に取得可能。service mesh の sidecar pattern と思想は近いが、stack 内蔵で zero-config よりの設計。

## 2. mechanism（どう動くか）

- **Policy Agent (pagent)**: started task として 1 つ動き、`PAGENT.CONF` を読む。
  TTLSConfig 経由で TTLSRule 一覧 + Image group 一覧を TCP/IP stack に install
- TTLSRule: 接続を match させる条件 (`LocalAddr` / `RemoteAddr` / `LocalPort` /
  `RemotePort` / `Jobname` / `Direction(Inbound|Outbound|Both)`)
- TTLSGroupAction: handshake role (Server / Client / ServerWithClientAuth)、
  TLS version 範囲、cipher suite list
- TTLSEnvironmentAction: keyring 指定、Trust 設定、SSL session cache 設定
- TTLSConnectionAction: per-connection 設定 (通常は環境設定継承)
- 一致した socket は TLS handshake を stack が自動実行し、application 視点で
  cleartext 通信のように見える
- application が IOCTL `SIOCTTLSCTL` を呼ぶと、`TTLS_QUERY_ONLY` で TLS 状態 / 相手  cert subject / session ID 取得 / `TTLS_INIT_CONNECTION` で明示 handshake 開始

## 3. prerequisites（理解の前提）

- TCP/IP stack の基礎 (PORT, BIND, listener) — Z3 起案 `ZOS-TCPIP-001`
- 証明書管理 — `ZOS-CERTMGMT-001`
- 一般 IT 知識: TLS handshake / cipher suite / X.509
- ICSF の RSA / ECC 鍵演算 — `ZOS-ICSF-001` (handshake で SAF + ICSF 経路を踏む)

## 4. relations（他アトムとの繋がり）

- `depends_on`: ZOS-TCPIP-001, ZOS-CERTMGMT-001, ZOS-ICSF-001
- `specialized_by`: なし
- `contrasts_with`: Linux stunnel / envoy sidecar / nginx TLS termination,   Windows IIS HTTPS binding
- `used_by`: ZOS-FTP-001 (FTP-TLS), ZOS-DB2-001 (DRDA TLS),
  ZOS-CICS-001 (IPIC TLS), ZOS-ZOSMF-001 (HTTPS listener)

## 5. pitfalls（実装・運用での落とし穴）

- **Policy Agent 起動忘れで cleartext 通信が黙って通る**: AT-TLS は **policy が install されてない状態では何もしない**。pagent が起動してない、または PAGENT.CONF の path 間違いで policy load 失敗してると、FTP / DRDA / IPIC が cleartext で通信し続ける。application 側からは何も見えない (TLS 期待してた socket がただの TCP)。起動チェックは `D TCPIP,,SYSPLEX,PORTS` + `pasearch -t` で全 rule が install済か確認。COMMNDxx で PAGENT を必ず TCP/IP より先に START、Health Checker `IBMTCPIP,POLICYAGENT_*` を必ず active 化。
- **TTLSRule の LocalAddr / RemoteAddr 漏れで部分的に未暗号化**: TTLSRule で `LocalAddr ALL` と書いたつもりが、実は dual-stack 環境でIPv6 listener にだけ match しない事例 (RemoteAddr ALL 指定漏れ等)。結果として IPv4 経路は暗号化、IPv6 経路は cleartext という発見しづらい穴になる。`netstat -p tcpip TTLS` で接続単位の TLS status を確認できるので、本番投入前に IPv4/IPv6 両方の actual flow を必ず確認。rule 順序 (上から match) の罠も併発する。
- **TLS 1.0 / 1.1 残存で監査 NG**: default の TTLSGroupAction は古い SSL/TLS version を許容する側に振れてることが多く、`TLSv1.0 ON` を残したまま本番運用してた site が PCI / FIPSaudit で reject される。`SSLv2 OFF SSLv3 OFF TLSv1 OFF TLSv1.1 OFF TLSv1.2 ON TLSv1.3 ON` を **明示** する。implicit default に頼るとz/OS PTF で挙動が変わったタイミングで黙って regression する。
- **Cipher suite mismatch で handshake 失敗、application は接続エラーだけ見る**: 相手が要求する cipher (例: ECDHE-RSA-AES256-GCM-SHA384) がTTLSGroupAction `V3CipherSuites` に無いと、handshake で `40` (handshake_failure)が返る。application 側は単なる接続エラー (errno=ECONNRESET) を見るだけで「相手の cert 切れた?」「証明書 chain 不一致?」と誤調査する。AT-TLS は `syslogd` 経由で詳細 trace を出すが、syslogd の facility 設定 (`AUTH.DEBUG`) を入れてないと取れない。事前に詳細 trace を有効化するランブックが必須。
- **Key ring 内に複数 cert がある時の default 選択ミス**: TTLSEnvironmentAction `Keyring USER1/MYRING` で複数 personal cert がある時、AT-TLS は `default` 属性が付いた cert を使う。`RACDCERT ALTER(LABEL('cert')) DEFAULT` で明示しないと、新規 cert が default になってクライアントの trust 設定 (CN 検査等) を壊す。renewal の運用フロー設計で「新 cert を ADD → trust 同期 → DEFAULT 切替 → 旧 cert 削除」の順序を守らないと renewal 当日に全 client 切断という事故。

## 6. examples（具体例）

```
* PAGENT.CONF 抜粋 (TTLS policy)
TTLSRule                       DB2_INBOUND
{
  LocalPortRange               446
  Direction                    Inbound
  TTLSGroupActionRef           gAct1
  TTLSEnvironmentActionRef     eAct1
}
TTLSGroupAction                gAct1
{
  TTLSEnabled                  On
  V3CipherSuites               TLS_AES_256_GCM_SHA384
  V3CipherSuites               TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
  TLSv1.2                      On
  TLSv1.3                      On
  TLSv1                        Off
  TLSv1.1                      Off
  SSLv3                        Off
  SSLv2                        Off
}
TTLSEnvironmentAction          eAct1
{
  HandshakeRole                Server
  TTLSKeyringParms
  {
    Keyring                    DB2PROD/DB2KR
  }
}
```

```
* 起動・確認コマンド
  S PAGENT
  pasearch -t                  /* TTLS policy 全件確認 */
  netstat -p tcpip TTLS        /* connection 単位の TLS status */
```

## 7. decision_axes（採否を分ける判断軸）

- **AT-TLS vs application 側 SSL ライブラリ**: AT-TLS は application 透過で運用一元化できるが、application がTLS session 詳細 (peer cert subject 等) を欲しがる場合は IOCTL で取りに行く改修が必要 (透過じゃなくなる)。application 側 SSL (System SSL / GSKit) を直接使うと cert 渡しが楽だが、cipher / version / keyring 管理がapplication ごとに分散して監査が難しい。**新規は AT-TLS 一択**、既存で GSKit 直接使ってる application は段階移行。
- **Inbound のみ TLS vs Inbound/Outbound 両方**: Inbound (mainframe が server) は明らかに必須。Outbound (mainframe がclient) は内部閉域網の場合迷うが、ゼロトラスト原則で両方 TLS 化が現代の正解。Outbound 設定漏れで internal API 呼出が cleartext のまま PCI auditで NG という site が増えている。Outbound 化は cipher suite 互換と Trust(root CA 配布) の運用が増えるコスト。
- **client cert 検証 (mTLS) vs server-only TLS**: TTLSGroupAction `HandshakeRole ServerWithClientAuth` で mTLS 化できる。金融系 / 高セキュリティでは事実上必須。但し client cert 失効管理が CA 側(CRL / OCSP) と AT-TLS 側で sync 必要、運用工数が server-only の 3 倍。client cert validation の RACF mapping (`HostIdMappings` 等) は SAF ACEEへ変換する追加設定で躓きやすい。

## 9. 市販書籍からの知識追加 (ADR-0109 順守)

市販書籍 (BK_MF_001, BK_ZOS_TECH_001) から AT-TLS 設定パターンを概念蒸留 (ADR-0109)。逐語引用禁止。
