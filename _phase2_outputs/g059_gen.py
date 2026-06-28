# -*- coding: utf-8 -*-
"""Generate g059_fixed.json. Japanese content authored per-row, grounded in
IBM GDPS 4.7 RAG corpus (GDPS_SG24-8367_DS8000_Copy_Services.pdf and companion
Redbooks). All output Japanese; no 原文ママ English retained."""
import json, re, os

rows = json.load(open(os.path.join(os.path.dirname(__file__), 'g059_rows.json'), encoding='utf-8'))
by_id = {r['row_id']: r for r in rows}

# ---- authored content: row_id -> dict(naiyou, steps, q, choices[4], ans, expl) ----
# steps and naiyou in Japanese. Grounded in DS8000 Copy Services / GDPS knowledge.
C = {}

def add(rid, naiyou, steps, q, choices, ans, expl):
    C[rid] = dict(naiyou=naiyou, steps=steps, q=q, choices=choices, ans=ans, expl=expl)

# Default source label
SRC = "IBM DS8000 Copy Services (GDPS_SG24-8367_DS8000_Copy_Services.pdf) / IBM GDPS 4.7"
RAGHIT = "GDPS_SG24-8367_DS8000_Copy_Services.pdf"
