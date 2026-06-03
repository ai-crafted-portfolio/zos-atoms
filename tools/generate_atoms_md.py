#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正本 (`C:\\decisions\\zos-kb\\atoms\\zos-XXX-001\\index.md`) から
公開サイト (`C:\\kvba\\zos-atoms-site\\docs\\atoms\\zos-XXX-001.md`) を生成する。

変換規則:
  - 元の frontmatter (id/title/status/last_reviewed/authors/rag_verified) を破棄
  - mkdocs material 用の frontmatter (title/description/tags) を新設
  - 本文中の内部用語 / メタコメント / TODO を削除
  - 既存 20 atom (zos-dataset-001 等) は対象外 (新規 42 のみ)

呼び方:
  python tools/generate_atoms_md.py
"""
import json
import os
import re
import sys
from pathlib import Path

# ----- パス定義 -----
REPO_ROOT = Path(__file__).resolve().parent.parent
SITE_ATOMS_DIR = REPO_ROOT / "docs" / "atoms"


def _resolve_decisions_root() -> Path:
    """Windows / Linux 両対応で decisions/zos-kb のルートを返す。"""
    # 1. 環境変数 ZOS_KB_ROOT があればそれを使う
    env = os.environ.get("ZOS_KB_ROOT")
    if env:
        p = Path(env)
        if (p / "atoms").is_dir():
            return p
    # 2. 既定の Windows path
    win_default = Path(r"C:\decisions\zos-kb")
    if (win_default / "atoms").is_dir():
        return win_default
    # 3. Linux mount (Cowork sandbox 等)
    for candidate in [
        Path("/sessions/confident-gracious-brown/mnt/decisions/zos-kb"),
        Path("/mnt/decisions/zos-kb"),
    ]:
        if (candidate / "atoms").is_dir():
            return candidate
    raise RuntimeError(
        "decisions/zos-kb ルートが見つかりません。"
        " 環境変数 ZOS_KB_ROOT で指定してください。"
    )


_KB_ROOT = _resolve_decisions_root()
SRC_ATOMS_DIR = _KB_ROOT / "atoms"
ASSIGNMENTS_JSON = _KB_ROOT / "_new_atoms_assignments.json"

# ----- Tier タグ -----
TIER_TAG = {
    "alpha":  "OS-Subsystem",
    "beta":   "Middleware-Utility",
    "gamma":  "Security-Network",
    "delta":  "Storage-Monitor",
    "epsilon": "Recovery-Workload",
    "zeta":   "Sysplex-Modernization",
}

# layer 番号 -> 大分類タグ
LAYER_TAG = {
    1: "OS",
    2: "Subsystem",
    3: "Middleware",
    4: "Utility",
    5: "Security",
    6: "Network",
    7: "Storage",
    8: "Monitor",
    9: "Recovery",
    10: "Workload",
    11: "Sysplex",
    12: "Modernization",
}

# ----- 内部用語パターン (本文から除去) -----
INTERNAL_TERM_PATTERNS = [
    # ADR 言及 (例: ADR-0091, ADR-0061 §3 等)
    (re.compile(r"\(?\s*ADR[-‐-―]\d{3,4}(?:\s*§\s*\S+)?\s*\)?", re.IGNORECASE), ""),
    # Phase N / Sprint N / iter NN / round NN
    (re.compile(r"\b(?:Phase|Sprint)\s+[A-Z\d]+\b", re.IGNORECASE), ""),
    # メタコメント <!-- ... -->
    (re.compile(r"<!--.*?-->", re.DOTALL), ""),
    # TODO / FIXME / WIP 行内タグ
    (re.compile(r"\b(?:TODO|FIXME|WIP)\s*[:：]?\s*", re.IGNORECASE), ""),
    # buildtest / Cowork / ChromaDB / RAG (内部基盤名)
    (re.compile(r"\b(?:buildtest|Cowork|ChromaDB|knowledgevba|knowledge_test_v2_buildtest)\b"), ""),
    # rag_verified: partially などの参照メタ
    (re.compile(r"^\s*-\s*rag_verified\s*:.*$", re.MULTILINE), ""),
]

# 残置 frontmatter 行 (id: / title: / status: / last_reviewed: / authors: / rag_verified:)
ORIG_FRONTMATTER_RE = re.compile(
    r"^---\s*\n(?:.*?\n)*?---\s*\n",
    re.MULTILINE
)


def load_assignments():
    """assignments.json から id -> (tier_name, title, description, layer) を作る"""
    with ASSIGNMENTS_JSON.open(encoding="utf-8") as f:
        data = json.load(f)

    out = {}
    for tier in data["tiers"]:
        tier_name = tier["tier"]
        for atom in tier["atoms"]:
            out[atom["id"]] = {
                "tier": tier_name,
                "title": atom["title"],
                "description": atom["description"],
                "layer": atom.get("primary_layer", 0),
            }
    return out


def clean_body(body: str) -> str:
    """本文の内部用語 / メタコメント / TODO を削除"""
    text = body
    for pattern, repl in INTERNAL_TERM_PATTERNS:
        text = pattern.sub(repl, text)

    # 連続空白の整理 (3 行以上の連続改行 -> 2 改行)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # 行末空白除去
    text = re.sub(r"[ \t]+\n", "\n", text)
    return text


def build_frontmatter(atom_id: str, meta: dict) -> str:
    """mkdocs material 用 frontmatter を構築"""
    title = atom_id.upper()
    description = meta["description"].replace('"', "'")
    tags = []
    if meta["layer"] in LAYER_TAG:
        tags.append(LAYER_TAG[meta["layer"]])
    tags.append(TIER_TAG.get(meta["tier"], meta["tier"]))

    fm_lines = ["---"]
    fm_lines.append(f"title: {title}")
    fm_lines.append(f"description: {description}")
    fm_lines.append("tags:")
    for t in tags:
        fm_lines.append(f"  - {t}")
    fm_lines.append("---")
    fm_lines.append("")
    return "\n".join(fm_lines)


def process_atom(atom_id: str, meta: dict) -> tuple[Path, str]:
    """1 atom 分の公開 md を生成して返す。書き込みは行わない。"""
    src_file = SRC_ATOMS_DIR / atom_id / "index.md"
    if not src_file.exists():
        raise FileNotFoundError(f"source missing: {src_file}")

    raw = src_file.read_text(encoding="utf-8")

    # 元 frontmatter を 1 個だけ剥がす
    raw_no_fm = ORIG_FRONTMATTER_RE.sub("", raw, count=1)

    body = clean_body(raw_no_fm).lstrip("\n")

    # 公開 frontmatter を付与
    fm = build_frontmatter(atom_id, meta)
    out_text = fm + body
    if not out_text.endswith("\n"):
        out_text += "\n"

    out_file = SITE_ATOMS_DIR / f"{atom_id}.md"
    return out_file, out_text


def main():
    assignments = load_assignments()
    # 新規 42 atom (assignments.json 由来)
    new_atom_ids = list(assignments.keys())

    # 既存 20 atom と重なるものは skip
    existing = {p.stem for p in SITE_ATOMS_DIR.glob("zos-*-001.md")}

    SITE_ATOMS_DIR.mkdir(parents=True, exist_ok=True)

    generated = 0
    skipped = 0
    errors = []

    for atom_id_upper in new_atom_ids:
        atom_id = atom_id_upper.lower()  # ファイル名は lower
        if atom_id in existing:
            skipped += 1
            continue
        try:
            out_file, text = process_atom(atom_id, assignments[atom_id_upper])
            out_file.write_text(text, encoding="utf-8", newline="\n")
            generated += 1
        except Exception as exc:
            errors.append((atom_id, str(exc)))

    print(f"generated : {generated}")
    print(f"skipped   : {skipped} (already in site/)")
    if errors:
        print(f"errors    : {len(errors)}")
        for a, e in errors:
            print(f"  - {a}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
