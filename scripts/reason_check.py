#!/usr/bin/env python3
"""OWL 2 DL reasoning check (HermiT via owlready2).

Reasons over ontology/resonatus.ttl merged with a single fixture and reports the reasoned class
membership of a candidate individual. Results can be reproduced with a separate toolchain. Usage:

    python scripts/reason_check.py <fixture.ttl> <candidate_local_name> <expect: Resonatus|NotResonatus>

Merges ontology/resonatus.ttl + the fixture with rdflib, serializes to RDF/XML, loads into an
owlready2 World, runs HermiT, and reports the reasoned class membership of the candidate individual
plus which paths (if any) were classified res:ResonatusPath. Exits non-zero on mismatch/inconsistency.
"""
from __future__ import annotations

import sys
import tempfile

import rdflib
from owlready2 import World, sync_reasoner_hermit
from owlready2.base import OwlReadyInconsistentOntologyError

RES = "https://w3id.org/resonatus#"
EX = "https://example.org/resonatus/reasoner/"
ONT = "ontology/resonatus.ttl"


def load_world(fixture: str) -> World:
    g = rdflib.Graph()
    g.parse(ONT, format="turtle")
    g.parse(fixture, format="turtle")
    tmp = tempfile.NamedTemporaryFile(suffix=".owl", delete=False)
    g.serialize(destination=tmp.name, format="xml")
    w = World()
    w.get_ontology("file://" + tmp.name).load()
    return w


def indirect_class_iris(ind) -> set[str]:
    return {c.iri for c in ind.INDIRECT_is_a if hasattr(c, "iri")}


def main() -> int:
    fixture, cand_name, expect = sys.argv[1], sys.argv[2], sys.argv[3]
    w = load_world(fixture)
    try:
        with w.get_ontology("http://anonymous/"):
            sync_reasoner_hermit(w, infer_property_values=True, debug=0)
    except OwlReadyInconsistentOntologyError:
        print("RESULT: INCONSISTENT ontology+fixture (HermiT)")
        return 3

    cand = w.search_one(iri=EX + cand_name)
    if cand is None:
        print(f"RESULT: candidate {cand_name} not found")
        return 4
    classes = indirect_class_iris(cand)
    is_reso = (RES + "Resonatus") in classes
    is_cand = (RES + "ResonatusCandidate") in classes

    # which individuals were classified as a qualifying path
    reso_path_cls = w.search_one(iri=RES + "ResonatusPath")
    qualifying = sorted(i.iri.replace(EX, "ex:") for i in reso_path_cls.instances()) if reso_path_cls else []

    print(f"candidate {cand_name}: ResonatusCandidate={is_cand} Resonatus={is_reso}")
    print(f"  inferred classes: {sorted(c.replace(RES,'res:').replace(EX,'ex:') for c in classes)}")
    print(f"  paths classified res:ResonatusPath: {qualifying or '(none)'}")

    want = expect == "Resonatus"
    ok = is_reso == want
    print(f"EXPECT {expect} -> {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
