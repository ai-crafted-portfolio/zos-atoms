# z/OS 技術項目細分化ガイド

z/OS を中心に、AIX・Python・VS Code・テープ系ハードウェア等の技術項目を細分化した技術リファレンスです。各製品を大分類 (Lv1) ごとのページにまとめ、中分類 (Lv2) 単位の折り畳みテーブルで技術項目・単一焦点要約・出典を一覧できます。

画面右上の検索から全ページを横断的に全文検索できます。

## コンテンツ一覧

| 製品 | 件数 | 出典区分 | 入口 |
|---|---:|---|---|
| z/OS 全体 (v3) | 13,762 | Redbook ingest 反映済 v3 | [概要](breakdown/zos-v3/index.md) |
| z/OS System Programming | 1,804 | 初版（事前知識補完を含む） | [概要](breakdown/zos-sysprog/index.md) |
| IBM z16 ハードウェア | 1,249 | 初版（事前知識補完を含む） | [概要](breakdown/z16/index.md) |
| テープ系 (TS2280 / TS4300 / TS7770) | 1,045 | 初版（事前知識補完を含む） | [概要](breakdown/tape/index.md) |
| AIX + ksh | 2,681 | 書籍出典 | [概要](breakdown/aix-ksh/index.md) |
| Python | 1,774 | Python 公式ドキュメント出典 | [概要](breakdown/python/index.md) |
| VS Code | 2,042 | VS Code 公式ドキュメント出典 | [概要](breakdown/vscode/index.md) |
| 検証手順サンプル | 50 | 実コンソールセッション再現 | [概要](breakdown/verification-sample/index.md) |

## 信頼性区分の凡例

- **Redbook ingest 反映済 / 公式 docs 出典 / 書籍出典**: 一次資料に基づく内容。
- **初版**: 事前知識による補完を含み、一次資料との突合（再生成）を予定。出典欄に「一次資料 突合予定」と表示される項目が該当します。

## 出典コード凡例

| 出典コード | 意味 | 主な製品 |
|---|---|---|
| `(一次資料 突合予定)` | 初版項目（一次資料との突合を予定） | IBM z16、z/OS System Programming |
| `AIX1` | AIX システム管理 1（書籍） | AIX + ksh |
| `AIX2` | AIX システム管理 2（書籍） | AIX + ksh |
| `AIX73` | IBM AIX 7.3 公式マニュアル | AIX + ksh |
| `AS1` | アドバンスドスキル Vol.1（書籍） | z/OS v3 |
| `AS2` | アドバンスドスキル Vol.2（書籍） | z/OS v3 |
| `BAS` | MFOS入門（書籍） | z/OS v3 |
| `GDPS` | IBM GDPS Redbooks 一式 | z/OS v3 |
| `KORN` | 入門 Korn シェル（書籍） | AIX + ksh |
| `MF` | メインフレーム実践（書籍） | z/OS v3 |
| `MQ` | IBM MQ 9.3 マニュアル一式 | z/OS v3 |
| `NV` | IBM NetView 6.4 マニュアル一式 | z/OS v3 |
| `PHA7` | PowerHA SystemMirror 7.x マニュアル | AIX + ksh |
| `PYDOC` | Python 公式ドキュメント (docs.python.org/3) | Python |
| `TS2280DOC` | IBM TS2280 公式ドキュメント | テープ系 |
| `TS4300DOC` | IBM TS4300 公式ドキュメント | テープ系 |
| `TS7770DOC` | IBM TS7770 公式ドキュメント | テープ系 |
| `TSA` | IBM Z System Automation for z/OS 4.3 マニュアル一式 | z/OS v3 |
| `VSCAPI` | Visual Studio Code 拡張 API リファレンス | VS Code |
| `VSCCOP` | GitHub Copilot in VS Code ドキュメント | VS Code |
| `VSCDOCS` | Visual Studio Code 公式ドキュメント | VS Code |
| `VSCKB` | Visual Studio Code キーボードショートカット リファレンス | VS Code |
| `VSCREM` | Visual Studio Code リモート開発ドキュメント | VS Code |
| `VSCSET` | Visual Studio Code 設定リファレンス | VS Code |
| `ZOS31` | IBM z/OS 3.1 公式マニュアル | z/OS v3 |
