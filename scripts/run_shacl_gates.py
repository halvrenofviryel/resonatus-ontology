#!/usr/bin/env python3
"""Resonatus SHACL assessment-record gates (independent engine: pyShACL).

Validates each assessment fixture in tests/shacl/ against shapes/resonatus.shacl.ttl and checks the
expected conformance. pyShACL is a standard, independent SHACL engine; results can be reproduced with
any standard SHACL engine (pyShACL or Apache Jena).

SHACL runs closed-world with no inference; assessment records assert their own types explicitly.

Usage:  python scripts/run_shacl_gates.py
Exit:   0 = every fixture matched its expected conformance; 1 = mismatch.
"""
from __future__ import annotations

import rdflib
from pyshacl import validate

SHAPES = "shapes/resonatus.shacl.ttl"
ONT = "ontology/resonatus.ttl"

# fixture -> expected conforms
GATES = {
    "tests/shacl/valid-assessment.ttl": True,
    "tests/shacl/missing-criterion.ttl": False,
    "tests/shacl/duplicate-criterion.ttl": False,
    "tests/shacl/invalid-verdict.ttl": False,
    "tests/shacl/wrong-assessed-candidate.ttl": False,
    "tests/shacl/two-assessed-candidates.ttl": False,
    "tests/shacl/mismatched-path-scope.ttl": False,
    # Path-coherence gates R18-R21: origin/receiver co-reference coherence that the ontology's OWL 2 DL
    # role pattern cannot express (the chain-plus-functionality encoding leaves OWL 2 DL — non-simple-role
    # rejection by HermiT; not a claim that no OWL 2 DL encoding could). Enforced in the SHACL profile.
    "tests/shacl/path-r18-origin-incoherent.ttl": False,    # declared origin != trace origin
    "tests/shacl/path-r19-delay-incoherent.ttl": False,     # delay postInteractionOf != declared origin
    "tests/shacl/path-r20-receiver-incoherent.ttl": False,  # selectivity receiver != propagation receiver
    "tests/shacl/path-r21-fully-coherent.ttl": True,        # same origin + same receiver throughout
    # R22/R23: identity policy is CANONICAL RDF-NODE reference equality, NOT owl:sameAs semantic
    # equivalence. Aliases linked only by owl:sameAs are treated as distinct nodes -> non-conform.
    # (Deterministic: independent of any owl:sameAs materialization / reasoning mode.)
    "tests/shacl/path-r22-origin-alias.ttl": False,         # trace origin is an owl:sameAs alias of declared
    "tests/shacl/path-r23-receiver-alias.ttl": False,       # selectivity receiver is an owl:sameAs alias
    # R24 completeness: a path with all five witnesses missing a coherence reference -> non-conform.
    "tests/shacl/path-r24-incomplete-refs.ttl": False,
    # R25 scope: a five-criterion assessment that declares no assessesPath -> non-conform
    # (res:assessesPath is required: every assessment must be scoped to exactly one ContinuationPath).
    "tests/shacl/path-r25-assessment-missing-path.ttl": False,
}


def main() -> int:
    shapes = rdflib.Graph().parse(SHAPES, format="turtle")
    all_ok = True
    for fixture, expect in GATES.items():
        # SHACL is closed-world STRUCTURAL validation of the record as given. We deliberately do NOT
        # run rdfs inference: the criterion/range axioms in the ontology (e.g. res:assesses rdfs:range
        # ResonatusCandidate) would otherwise AUTO-TYPE an assessed node as a candidate and make the
        # sh:class check vacuous (the domain/range-as-inference trap). Assessment records
        # therefore assert their own types explicitly.
        data = rdflib.Graph().parse(fixture, format="turtle")
        conforms, _, _ = validate(
            data_graph=data, shacl_graph=shapes,
            inference="none", advanced=True, debug=False,
        )
        good = conforms == expect
        all_ok = all_ok and good
        print(f"[{'PASS' if good else 'FAIL'}] {fixture.split('/')[-1]:32s} conforms={conforms} expected={expect}")
    print(f"\nSUMMARY: {'ALL SHACL GATES PASS' if all_ok else 'SHACL GATE FAILURES PRESENT'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
