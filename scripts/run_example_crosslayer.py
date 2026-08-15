#!/usr/bin/env python3
"""Cross-layer consistency gate for the examples.

Each example now carries BOTH an epistemic assessment (criterion verdicts + expectedClassification)
and an ontic ContinuationPath. This runner checks the two layers agree:

    OWL entails candidate a res:Resonatus   <=>   expectedClassification == "MEMBERSHIP_SUPPORTED"

NON_MEMBERSHIP_SUPPORTED (a FAIL) and UNDETERMINED (INCONCLUSIVE/NOT_MEASURED) both map to OWL
NON-entailment — the ontic layer cannot and must not distinguish them (OWA); only the epistemic layer
does. It also confirms each migrated example conforms to the SHACL profile (paths are coherent by
construction). Uses HermiT + pyShACL; results can be reproduced with a separate toolchain.

Usage: python scripts/run_example_crosslayer.py
"""
from __future__ import annotations

import glob
import tempfile

import rdflib
from pyshacl import validate
from owlready2 import World, sync_reasoner_hermit
from owlready2.base import OwlReadyInconsistentOntologyError

RES = "https://w3id.org/resonatus#"
CASE = "https://example.org/resonatus/case/"
ONT = "ontology/resonatus.ttl"
SHAPES = "shapes/resonatus.shacl.ttl"


def the_candidate(example: str) -> str | None:
    """The single ResonatusCandidate declared in the example (the individual the check is bound to)."""
    g = rdflib.Graph(); g.parse(example, format="turtle")
    cands = list(g.subjects(rdflib.RDF.type, rdflib.URIRef(RES + "ResonatusCandidate")))
    return str(cands[0]) if len(cands) == 1 else None


def owl_is_resonatus(example: str, candidate_iri: str) -> bool:
    g = rdflib.Graph(); g.parse(ONT, format="turtle"); g.parse(example, format="turtle")
    tmp = tempfile.NamedTemporaryFile(suffix=".owl", delete=False); g.serialize(tmp.name, format="xml")
    w = World(); w.get_ontology("file://" + tmp.name).load()
    try:
        sync_reasoner_hermit(w, infer_property_values=True, debug=0)
    except OwlReadyInconsistentOntologyError:
        return False  # inconsistency is not membership
    ind = w.search_one(iri=candidate_iri)  # bind to THE candidate, not "any case individual"
    return bool(ind and any(getattr(c, "iri", None) == RES + "Resonatus" for c in ind.INDIRECT_is_a))


def expected(example: str, candidate_iri: str) -> str:
    """expectedClassification bound to the candidate individual (not 'anywhere in the file')."""
    g = rdflib.Graph(); g.parse(example, format="turtle")
    for o in g.objects(rdflib.URIRef(candidate_iri), rdflib.URIRef(RES + "expectedClassification")):
        return str(o)
    return "?"


def main() -> int:
    shapes = rdflib.Graph().parse(SHAPES, format="turtle")
    all_ok = True
    for f in sorted(glob.glob("examples/*.ttl")):
        cand = the_candidate(f)
        if cand is None:
            print(f"[FAIL] {f.split('/')[-1]:44s} could not bind a single ResonatusCandidate")
            all_ok = False
            continue
        exp = expected(f, cand)
        want_reso = exp == "MEMBERSHIP_SUPPORTED"
        got_reso = owl_is_resonatus(f, cand)
        data = rdflib.Graph().parse(f, format="turtle")
        conforms, _, _ = validate(data_graph=data, shacl_graph=shapes, inference="none", advanced=True)
        cross_ok = (want_reso == got_reso)
        ok = cross_ok and conforms
        all_ok = all_ok and ok
        print(f"[{'PASS' if ok else 'FAIL'}] {f.split('/')[-1]:44s} expected={exp:24s} OWL_Resonatus={got_reso} SHACL_conforms={conforms}")
    print(f"\nSUMMARY: {'ALL CROSS-LAYER GATES PASS' if all_ok else 'CROSS-LAYER FAILURES PRESENT'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
