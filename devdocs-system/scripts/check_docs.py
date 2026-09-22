#!/usr/bin/env python3
"""Validate a devdocs-style documentation set.

Three checks, all stdlib-only:

  1. INTERNAL LINKS   every relative markdown link resolves to a file that exists.
  2. DANGLING IDS     every identifier reference (DEBT-12, FR-3.1, TGAP-10, ...)
                      has a definition somewhere in the set.
  3. FAMILY SUMMARY   which identifier families exist and how many members.

Why check 2 matters more than it looks: a dangling reference is also how a
PREFIX COLLISION surfaces. If `C1` means "data classification level" in one doc
and "conflict #1" in another, the validator reports `C1` as dangling for
whichever family did not define it — which is exactly the signal you want.

Absence is easy to get wrong in prose and easy to get right here, so this
script is the cheap insurance for the whole doc set.

Usage:
    python check_docs.py [DOCS_DIR] [--config FILE] [--json] [--quiet]

Config (optional), placed in DOCS_DIR as `docids.json` or passed with --config:

    {
      "extra_patterns": ["\\bW\\d+\\b", "\\bM\\d+\\b"],
      "ignore": ["SHA-256", "TLS-1.2"],
      "allow": ["FR-13"]
    }

`extra_patterns` covers families that do not use the `PREFIX-NNN` shape
(e.g. single-letter workstream or milestone numbers).
`ignore` silences specific tokens that look like identifiers but are not.
`allow` permits specific references that are intentionally forward-looking
("this will become FR-13") and therefore have no definition yet.

Placeholder forms such as `DEBT-xx`, `FR-x` (used in a prefix-registry table)
are ignored automatically, as are families with no definitions at all
(so `SHA-256`, `UTF-8`, `ISO-8601` never trigger a false report).

Exit code: 0 clean, 1 problems found, 2 bad usage.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

# Identifier shape: 2-8 uppercase letters, hyphen, alnum segment, optional
# .dot.number suffixes. Examples that match: DEBT-01 FR-9.11 NFR-P.6 CF-1
# ADR-004 TGAP-10 SHA-256. Examples that deliberately do NOT match: E0 C0 G1
# (historical single-letter task numbers), v1.5 (lowercase).
TOKEN = re.compile(r"\b([A-Z]{2,8}-[A-Za-z0-9]+(?:\.[0-9]+)*)\b")
FAMILY = re.compile(r"^([A-Z]{2,8})-")

# A definition is a heading or a table cell that starts with the identifier.
DEF_HEADING = re.compile(r"^#{2,4}\s+[`*]{0,2}([A-Z]{2,8}-[A-Za-z0-9]+(?:\.[0-9]+)*)\b", re.M)
DEF_CELL = re.compile(r"^\|\s*[`*]{0,2}([A-Z]{2,8}-[A-Za-z0-9]+(?:\.[0-9]+)*)[`*]{0,2}\s*\|", re.M)

LINK = re.compile(r"\]\(([^)]+)\)")


def strip_code(text: str) -> str:
    """Drop fenced code blocks so shell/json examples do not add noise."""
    return re.sub(r"^```.*?^```", "", text, flags=re.M | re.S)


def is_placeholder(token: str) -> bool:
    """Registry placeholders, not references: `FR-x`, `DEBT-xx`, `ADR-0xx`."""
    parts = token.split("-", 1)
    return len(parts) == 2 and re.fullmatch(r"[0-9]*[xX]+", parts[1]) is not None


def defined_tokens(docs: list[str], pattern: re.Pattern | None = None) -> set[str]:
    """Collect every definition-looking token across the whole set.

    Two accepted forms: a heading (`### DEBT-01 · ...`) or a table cell
    (`| DEBT-01 | ... |`, backticks optional). Definitions are global to the
    doc set, not per-file — a reference in one file is satisfied by a
    definition in another.
    """
    found: set[str] = set()
    for body in docs:
        if pattern is None:
            found.update(DEF_HEADING.findall(body))
            found.update(DEF_CELL.findall(body))
        else:
            for token in set(pattern.findall(body)):
                if re.search(rf"^#{{2,4}}\s+[`*]{{0,2}}{re.escape(token)}\b", body, re.M) or \
                   re.search(rf"^\|\s*[`*]{{0,2}}{re.escape(token)}[`*]{{0,2}}\s*\|", body, re.M):
                    found.add(token)
    return found


def load_config(path: pathlib.Path | None) -> dict:
    if path is None or not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"config error in {path}: {exc}", file=sys.stderr)
        sys.exit(2)


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("docs_dir", nargs="?", default=".")
    ap.add_argument("--config")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--quiet", action="store_true", help="only report problems")
    args = ap.parse_args()

    root = pathlib.Path(args.docs_dir)
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    cfg_path = pathlib.Path(args.config) if args.config else root / "docids.json"
    cfg = load_config(cfg_path)
    extra = [re.compile(p) for p in cfg.get("extra_patterns", [])]
    ignore = set(cfg.get("ignore", []))
    allow = set(cfg.get("allow", []))

    files = sorted(root.glob("*.md"))
    if not files:
        print(f"no markdown files in {root}", file=sys.stderr)
        return 2

    names = {f.name for f in files}
    text = {f.name: f.read_text(encoding="utf-8") for f in files}

    # ---- 1. links ------------------------------------------------------
    broken_links: list[tuple[str, str]] = []
    for f in files:
        for raw in LINK.findall(text[f.name]):
            target = raw.split("#")[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if target not in names:
                broken_links.append((f.name, raw))

    # ---- 2. identifiers -------------------------------------------------
    bodies = [text[f.name] for f in files]
    definitions: dict[str, set[str]] = {}
    for f in files:
        body = text[f.name]
        for token in DEF_HEADING.findall(body) + DEF_CELL.findall(body):
            definitions.setdefault(token, set()).add(f.name)

    families = sorted({FAMILY.match(t).group(1) for t in definitions if FAMILY.match(t)})

    def is_known_family(token: str) -> bool:
        m = FAMILY.match(token)
        return bool(m) and m.group(1) in families

    refs: dict[str, list[str]] = {}
    for f in files:
        for token in TOKEN.findall(strip_code(text[f.name])):
            if token in ignore or token in allow or is_placeholder(token):
                continue
            if not is_known_family(token):
                continue
            refs.setdefault(token, []).append(f.name)

    dangling = {t: sorted(set(v)) for t, v in refs.items() if t not in definitions}

    # extra_patterns families (e.g. W2, M1): compare references against the
    # global set of definition-looking tokens, not against the same file.
    extra_dangling: dict[str, list[str]] = {}
    extra_counts: dict[str, int] = {}
    for pat in extra:
        defined = defined_tokens(bodies, pat)
        extra_counts[pat.pattern] = len(defined)
        for f in files:
            for token in set(pat.findall(strip_code(text[f.name]))):
                if token in ignore or token in allow or token in defined:
                    continue
                extra_dangling.setdefault(token, []).append(f.name)

    # ---- 3. report ------------------------------------------------------
    problems = bool(broken_links or dangling or extra_dangling)
    family_counts = {fam: sum(1 for t in definitions if FAMILY.match(t) and FAMILY.match(t).group(1) == fam)
                     for fam in families}

    if args.json:
        print(json.dumps({
            "docs": len(files),
            "broken_links": [{"file": f, "target": t} for f, t in broken_links],
            "dangling_identifiers": dangling,
            "extra_family_dangling": extra_dangling,
            "families": family_counts,
            "extra_families": extra_counts,
            "ok": not problems,
        }, ensure_ascii=False, indent=2))
        return 1 if problems else 0

    if not args.quiet:
        print(f"docs scanned        : {len(files)}")
        print(f"identifier families : " +
              (", ".join(f"{k}({v})" for k, v in sorted(family_counts.items())) or "none"))
        if extra_counts:
            # print the pattern as written in docids.json — it is the config the
            # reader just edited, so echoing it verbatim is the clearest label
            print(f"extra families      : " + ", ".join(f"{k}={v}" for k, v in extra_counts.items()))
        print()

    if broken_links:
        print(f"BROKEN LINKS ({len(broken_links)}):")
        for f, t in broken_links:
            print(f"  {f} -> {t}")
        print()

    if dangling:
        print(f"DANGLING IDENTIFIER REFERENCES ({len(dangling)}):")
        by_fam: dict[str, list[str]] = {}
        for token, where in sorted(dangling.items()):
            fam = FAMILY.match(token)
            by_fam.setdefault(fam.group(1) if fam else "?", []).append(f"{token} (in {', '.join(where)})")
        for fam, items in sorted(by_fam.items()):
            print(f"  family {fam}:")
            for it in items:
                print(f"    {it}")
        print("  hint: a token reported here may be a PREFIX COLLISION — the same")
        print("        token used for two different meanings. Rename the newer family.")
        print()

    if extra_dangling:
        print(f"UNRESOLVED EXTRA-FAMILY IDS ({len(extra_dangling)}):")
        for token, where in sorted(extra_dangling.items()):
            print(f"  {token} (referenced in {', '.join(sorted(set(where)))})")
        print()

    print("OK — links resolve and all identifier references are defined." if not problems
          else "FAILED — fix the items above.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
