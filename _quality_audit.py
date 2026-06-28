# -*- coding: utf-8 -*-
import re, glob, os, unicodedata

DIR = r"C:\kvba\zos-atoms-site\docs\breakdown\zos-v3-with-verify"
OUT = r"C:\kvba\zos-atoms-site\_quality_audit.tsv"

def is_cjk(ch):
    o = ord(ch)
    return (0x3040 <= o <= 0x30ff) or (0x3400 <= o <= 0x9fff) or (0xff00 <= o <= 0xffef and not (0xff01<=o<=0xff5e))  # hiragana/katakana/kanji + halfwidth-kana

def has_cjk(s):
    for ch in s:
        o = ord(ch)
        if (0x3040 <= o <= 0x30ff) or (0x3400 <= o <= 0x9fff) or (0xf900 <= o <= 0xfaff):
            return True
    return False

def ascii_ratio(s):
    # ratio of ASCII letters/digits over total non-space, non-punct-symbol meaningful chars
    chars = [c for c in s if not c.isspace()]
    if not chars:
        return 0.0
    asc = sum(1 for c in chars if ord(c) < 128)
    return asc / len(chars)

rows_out = []
header = ["page","total_items","verified","verify_ratio","english_ratio","jp_ratio","pure_eng_ratio","src_tag_rows","content_rows","class_spec","class_refined"]

files = sorted(glob.glob(os.path.join(DIR, "g*.md")))
for fp in files:
    page = os.path.splitext(os.path.basename(fp))[0]
    with open(fp, encoding="utf-8") as f:
        text = f.read()
    # total_items
    m = re.search(r"本ページ件数\*?\*?\s*[:：]\s*([\d,]+)\s*件", text)
    total = int(m.group(1).replace(",","")) if m else 0
    # verified: sum all "うち検証手順・確認問題 N 件"
    verified = sum(int(x.replace(",","")) for x in re.findall(r"うち検証手順・確認問題\s*([\d,]+)\s*件", text))
    # content cells = 3rd column of table rows
    content_rows = 0
    eng_rows = 0
    jp_rows = 0
    src_tag_rows = 0
    for line in text.splitlines():
        ls = line.strip()
        if not ls.startswith("|"):
            continue
        parts = ls.split("|")
        # leading and trailing empty -> parts: ['', c1, c2, c3, c4, '']
        if len(parts) < 5:
            continue
        cells = [p.strip() for p in parts[1:-1]]
        # skip header row and separator row
        joined = "".join(cells)
        if set(joined) <= set("-: "):  # separator
            continue
        if cells[0] in ("連番",) or cells[0].startswith("連番"):
            continue
        # need numeric first cell to be a data row
        if not re.match(r"^\d+$", cells[0]):
            continue
        if len(cells) < 3:
            continue
        content = cells[2]
        content_rows += 1
        if ascii_ratio(content) > 0.5:
            eng_rows += 1
        if has_cjk(content):
            jp_rows += 1
        if "原文ママ" in content:
            src_tag_rows += 1
    verify_ratio = verified/total if total else 0.0
    english_ratio = eng_rows/content_rows if content_rows else 0.0
    jp_ratio = jp_rows/content_rows if content_rows else 0.0
    pure_eng = 1.0 - jp_ratio  # rows with NO CJK at all = raw untranslated
    # class_spec: literal spec definition (english_ratio = ASCII>50%)
    if verify_ratio < 0.30 or english_ratio > 0.70:
        cls_spec = "FATAL"
    elif (0.30 <= verify_ratio < 0.70) or (0.30 < english_ratio <= 0.70):
        cls_spec = "IMPROVE"
    else:
        cls_spec = "OK"
    # class_refined: use pure_eng (truly untranslated rows) as the English-residue signal
    if verify_ratio < 0.30 or pure_eng > 0.70:
        cls_ref = "FATAL"
    elif (0.30 <= verify_ratio < 0.70) or (0.30 < pure_eng <= 0.70):
        cls_ref = "IMPROVE"
    else:
        cls_ref = "OK"
    rows_out.append([page,total,verified,round(verify_ratio,3),round(english_ratio,3),round(jp_ratio,3),round(pure_eng,3),src_tag_rows,content_rows,cls_spec,cls_ref])

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\t".join(header)+"\n")
    for r in rows_out:
        f.write("\t".join(str(x) for x in r)+"\n")

# summary
from collections import Counter
cs = Counter(r[9] for r in rows_out)
cr = Counter(r[10] for r in rows_out)
print("FILES:", len(rows_out))
print("CLASS_SPEC   :", dict(cs))
print("CLASS_REFINED:", dict(cr))
print()
print("\t".join(header))
for r in rows_out:
    print("\t".join(str(x) for x in r))
