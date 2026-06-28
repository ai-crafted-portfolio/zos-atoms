# -*- coding: utf-8 -*-
# Usage: python _g060_acc.py <batchfile.json>
import json, sys, os
ACC = r"C:\kvba\zos-atoms-site\_phase2_outputs\_g060_acc.json"
with open(sys.argv[1], "r", encoding="utf-8") as f:
    batch = json.load(f)
data = []
if os.path.exists(ACC):
    with open(ACC, "r", encoding="utf-8") as f:
        data = json.load(f)
have = {r["row_id"] for r in data}
for r in batch:
    if r["row_id"] not in have:
        data.append(r)
        have.add(r["row_id"])
with open(ACC, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
print("total:", len(data))
