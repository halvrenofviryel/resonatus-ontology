#!/usr/bin/env python3
"""Run v1.1, prototype, and repository regression gates without modifying release state."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PYTHON = Path("/mnt/data/claude/resonatus-ontology/.venv/bin/python")

COMMANDS = (
    ("v1.1 package integrity", "profiles/v1.1/runners/verify_package.py", "."),
    ("v1.1 scenarios", "profiles/v1.1/runners/run_scenarios.py", "."),
    ("v1.1 mutations", "profiles/v1.1/runners/run_mutations.py", "."),
    ("v1.1 module integration", "profiles/v1.1/runners/run_module_integration.py", "."),
    ("Prototype scenarios", "docs/research/prototypes/v11/run_prototypes.py", "."),
    ("Prototype mutations", "docs/research/prototypes/v11/run_prototype_mutations.py", "."),
    ("Prototype module integration", "docs/research/prototypes/v11/run_owl_module_integration.py", "."),
    ("Repository parse and fixture validation", "scripts/validate.py", "."),
    ("Repository reasoner gates", "scripts/run_reasoner_gates.py", None),
    ("Repository SHACL gates", "scripts/run_shacl_gates.py", None),
    ("Repository cross-layer gates", "scripts/run_example_crosslayer.py", None),
    ("Repository competency queries", "scripts/run_competency_queries.py", None),
    ("Repository structure audit", "scripts/audit_structure.py", None),
    ("Repository wording lint", "scripts/check_wording.py", None),
)


def main() -> int:
    if not PYTHON.is_file():
        print(f"ERROR: pinned Python not found: {PYTHON}", file=sys.stderr)
        return 2

    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    passed = 0

    for label, script, argument in COMMANDS:
        command = [str(PYTHON), script]
        if argument is not None:
            command.append(argument)
        print(f"\n=== {label} ===", flush=True)
        print("$ " + " ".join(command), flush=True)
        completed = subprocess.run(command, cwd=ROOT, env=env, check=False)
        if completed.returncode != 0:
            print(f"\nFAILED: {label} (exit {completed.returncode})", file=sys.stderr)
            return completed.returncode
        passed += 1

    print(f"\nALL LOCAL v1.1 GATES PASS ({passed}/{len(COMMANDS)} command groups)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
