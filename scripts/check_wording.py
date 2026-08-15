#!/usr/bin/env python3
"""Wording lint (doc-discipline gate, not a formal gate).

This lint guards against UNSCOPED over-broad claims about OWL 2 DL
expressivity. The demonstrated result is narrow: the co-reference constraint is not captured by the
ontology's OWL 2 DL role pattern (the chain-plus-functionality encoding leaves OWL 2 DL). Any occurrence
of a broad phrase MUST carry a scoping qualifier on the same line, or this lint fails.

Usage: python scripts/check_wording.py    (exit 1 on any unscoped occurrence)
"""
from __future__ import annotations

import glob
import re
import sys

BROAD = re.compile(
    r"beyond OWL 2 DL|cannot express|cannot force|in-DL binding is impossible|"
    r"not OWL 2 DL[- ]expressible|only approach.*OWL 2 DL|no OWL 2 DL encoding (can|could)",
    re.IGNORECASE,
)
SCOPE = re.compile(
    r"role pattern|pattern used here|not a (general )?claim|not available|reduce to it|scoped|"
    r"used in this ontology|not captured by|do not claim|could (ever )?relate such witnesses",
    re.IGNORECASE,
)
EXCLUDE_PATHS = (".venv/", ".git/", "scripts/check_wording.py")


def main() -> int:
    hits: list[str] = []
    for f in glob.glob("**/*", recursive=True):
        if not f.endswith((".ttl", ".md", ".py", ".rq")) or any(x in f for x in EXCLUDE_PATHS):
            continue
        try:
            lines = open(f, encoding="utf-8").read().splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for n, line in enumerate(lines, 1):
            if BROAD.search(line) and not SCOPE.search(line):
                hits.append(f"{f}:{n}: {line.strip()[:120]}")
    if hits:
        print("UNSCOPED OWL-expressivity claim(s) — add a scoping qualifier:")
        for h in hits:
            print("  " + h)
        print(f"\nSUMMARY: {len(hits)} unscoped claim(s) FAIL")
        return 1
    print("SUMMARY: no unscoped OWL-expressivity claims (wording lint PASS)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
