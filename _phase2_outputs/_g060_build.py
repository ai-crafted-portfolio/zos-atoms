# -*- coding: utf-8 -*-
import json

rows = []

def add(rid, title, naiyou, steps, q, choices, ans, expl, source, hit):
    rows.append({
        "row_id": rid, "title": title, "naiyou_jp": naiyou,
        "verify_steps": steps,
        "quiz": {"q": q, "choices": choices, "answer": ans, "explanation": expl},
        "source": source, "rag_hit": hit
    })

# ---- Batch 1: FlashCopy cascading / native commands ----
add(12119, "Multiple FlashCopy relationships in a more complex configuration",
 "MM 構成を起点に、複数ターゲットの FlashCopy 関係とカスケード FlashCopy を組み合わせると、1 つのソースボリュームから複数の独立した PiT コピーを保持できる。複数の FlashCopy 関係を作成する際は、整合性グループ (CG) 属性を付けて確立することで、対象ボリューム群への書き込み整合性を確保できる。カスケードでは、既存関係のターゲットが新たな関係のソースになる。",
 "1. dscli> lsflash -l 6100  で既存の FlashCopy 関係を一覧表示する。\n2. dscli> mkflash -cp -record -persist 6100:6200  で 1 つ目のターゲットを確立する。\n3. dscli> mkflash -cp 6200:6300  でカスケード関係を追加する（6200 がソースに昇格）。\n4. dscli> lsflash -l 6100 6200  で複数関係が並存していることを確認する。",
 "複数の FlashCopy 関係を作成するときに書き込み整合性を確保するために推奨される属性はどれか。",
 ["整合性グループ (CG) 属性を付けて確立する","nocopy オプションを必須にする","ソースを 1 つの LSS に限定する","背景コピーを無効化する"], 0,
 "正解は CG 属性。複数関係を CG 属性付きで確立することで、対象ボリューム群への書き込みが整合した状態でコピーされる。",
 "GDPS_SG24-8367_DS8000_Copy_Services.pdf p.144 (12.3.6)", "p.144/p.132 複数/カスケード FlashCopy"),

add(12121, "Multiple setups of a test system with the same contents",
 "同一内容のテストシステムを複数構築する場合、FlashCopy を用いて本番ボリュームから複数のテストボリュームへコピーを取得する。あるボリュームを 1 つの FlashCopy 関係のターゲットとし、同時に別の関係のソースにすることはできないため、背景コピー (-cp) の完了を待ってから次の段階を実行する必要がある。Part 1 と Part 2 を 1 つのジョブで実行するとスクリプトは失敗する。",
 "1. dscli> mkflash -cp 6100:6101  で Part1 の FlashCopy を確立する。\n2. dscli> lsflash -l 6100  を実行し、背景コピーが完了するまで待つ。\n3. 完了後、dscli> mkflash -cp 6101:6300  で Part2（テストボリューム作成）を実行する。\n4. 一括実行すると 6101 が同時にソースとターゲットになれず失敗することを確認する。",
 "同一内容のテストシステムを複数作成する手順で、Part1 と Part2 を 1 ジョブで実行すると失敗する理由はどれか。",
 ["同一ボリュームを同時にソースとターゲットにできないため","DS CLI がバッチ実行を許可しないため","CG 属性が必須のため","LSS をまたぐコピーが禁止のため"], 0,
 "1 つのボリュームを同じ時点で別 FlashCopy の target かつ source にはできない。背景コピー完了を待つ必要がある。",
 "GDPS_SG24-8367_DS8000_Copy_Services.pdf p.125 (12.1.2)", "p.125/p.120 テストシステム複数構築"),

add(12124, "Native VSE commands for FlashCopy",
 "z/VSE 環境では、ネイティブの IXFP SNAP コマンドを使用して FlashCopy を開始できる。また ICKDSF の Copy Services コマンドを使って VSEn のレプリケーション環境を管理することもできる。z/VSE が FlashCopy 用に持つネイティブコマンドは IXFP SNAP の 1 つである。",
 "1. z/VSE 上で IXFP SNAP コマンドを発行し、FlashCopy を開始する。\n2. ICKDSF の Copy Services コマンド（例: FLASHCPY ESTABLISH）でレプリケーション環境を管理する。\n3. DS8000 側で dscli> lsflash により関係が確立されたことを確認する。",
 "z/VSE が FlashCopy 用に持つネイティブコマンドはどれか。",
 ["IXFP SNAP","FLASHCopy (CP)","mkflash","FCESTABLISH"], 0,
 "z/VSE のネイティブ FlashCopy コマンドは IXFP SNAP。ICKDSF コマンドも併用できる。",
 "GDPS_SG24-8367_DS8000_Copy_Services.pdf p.55 (5.8)", "p.55 Native VSE/z/VM commands"),

add(12126, "Native z/VM commands for FlashCopy",
 "z/VM 環境では、ネイティブの z/VM CP FLASHCopy コマンドを使用して FlashCopy を開始できる。また ICKDSF の Copy Services コマンドを用いて z/VM CP ボリュームを管理することも可能である。VM ゲストとして稼働する場合は、ゲストディレクトリに STDEVOPT DATAMOVER=YES の指定が必要となる。",
 "1. z/VM 上で CP FLASHCopy コマンドを発行し、FlashCopy を開始する。\n2. 必要に応じて ICKDSF コマンドで z/VM CP ボリュームを管理する。\n3. VM ゲスト構成では、ディレクトリに STDEVOPT DATAMOVER=YES が設定されていることを確認する。",
 "z/VM のネイティブ FlashCopy コマンドはどれか。",
 ["z/VM CP FLASHCopy","IXFP SNAP","ANTFREXX","mkflash"], 0,
 "z/VM はネイティブの CP FLASHCopy コマンドで FlashCopy を開始する。ICKDSF も使用可能。",
 "GDPS_SG24-8367_DS8000_Copy_Services.pdf p.55 (5.7)", "p.55 Native z/VM commands"),
]

with open(r"C:\kvba\zos-atoms-site\_phase2_outputs\_g060_rows_part.json","w",encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False)
print(len(rows))
