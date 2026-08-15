#!/usr/bin/env python3
"""Resonatus OWL 2 DL reasoner gate runner (HermiT via owlready2).

Runs the R3-R17 release gates: merges ontology/resonatus.ttl with each fixture, reasons with HermiT,
and checks the intended entailments / non-entailments / (in)consistency.

Scope: this runner reports whether the ontology plus fixtures behave as specified under HermiT. It is a
reproducibility/tool check, not a proof of empirical or scientific validity; results can be reproduced
with a separate toolchain (e.g. ROBOT/OWLAPI + HermiT or another OWL 2 DL reasoner).

Usage:  python scripts/run_reasoner_gates.py
Exit:   0 = all gates behaved as specified; 1 = one or more gate mismatches.
"""
from __future__ import annotations

import tempfile

import rdflib
from owlready2 import World, sync_reasoner_hermit
from owlready2.base import OwlReadyInconsistentOntologyError

RES = "https://w3id.org/resonatus#"
ONT = "ontology/resonatus.ttl"

# check kinds: ("is",ind,cls) ("is-not",ind,cls) ("prop",subj,prop,obj) ("not-prop",subj,prop,obj)
GATES = [
    {"id": "R3", "fixture": "tests/nontransitive-chain.ttl", "ns": "https://example.org/resonatus/test/",
     "consistent": True, "checks": [("not-prop", "a", "directlyContinues", "c")]},
    {"id": "R4", "fixture": "tests/nontransitive-chain.ttl", "ns": "https://example.org/resonatus/test/",
     "consistent": True, "checks": []},  # AllDifferent(a,b,c) + consistent == no sameAs collapse
    {"id": "R6", "fixture": "tests/owl-positive-resonatus.ttl",
     "consistent": True, "checks": [("is", "candidate", "Resonatus"), ("is", "path", "ResonatusPath")]},
    {"id": "R7", "fixture": "tests/owl-missing-selectivity.ttl",
     "consistent": True, "checks": [("is", "path_ms", "CausalTraceProcess"),
                                    ("is-not", "path_ms", "ResonatusPath"),
                                    ("is-not", "candidate_no_selectivity", "Resonatus")]},
    {"id": "R8", "fixture": "tests/owl-delay-without-trace.ttl",
     "consistent": True, "checks": [("is-not", "path_d", "CausalTraceProcess"),
                                    ("is-not", "delay_candidate", "Resonatus")]},
    {"id": "R9", "fixture": "tests/owl-causal-origin-chain.ttl",
     "consistent": True, "checks": [("prop", "path_co", "hasOriginInteraction", "origin")]},
    {"id": "R10", "fixture": "tests/owl-mixed-path-attack.ttl",
     "consistent": True, "checks": [("is-not", "candidate", "Resonatus")]},
    {"id": "R11", "fixture": "tests/owl-five-different-paths.ttl",
     "consistent": True, "checks": [("is-not", "candidate", "Resonatus")]},
    {"id": "R12", "fixture": "tests/owl-complete-plus-incomplete.ttl",
     "consistent": True, "checks": [("is", "candidate", "Resonatus"), ("is", "full", "ResonatusPath"),
                                    ("is-not", "partial", "ResonatusPath")]},
    {"id": "R13", "fixture": "tests/owl-two-complete-paths.ttl",
     "consistent": True, "checks": [("is", "candidate", "Resonatus"),
                                    ("is", "pathA", "ResonatusPath"), ("is", "pathB", "ResonatusPath")]},
    {"id": "R14", "fixture": "tests/owl-wrong-origin-delay.ttl",
     "consistent": True, "checks": [("is-not", "candidate", "Resonatus")]},
    {"id": "R15", "fixture": "tests/owl-wrong-receiver-selectivity.ttl",
     "consistent": True, "checks": [("is-not", "candidate", "Resonatus")]},
    {"id": "R16", "fixture": "tests/owl-two-declared-origins-inconsistent.ttl",
     "consistent": False, "checks": []},  # functional declared-origin + two distinct origins => inconsistent
    {"id": "R17", "fixture": "tests/owl-domain-contamination.ttl",
     "consistent": True, "checks": [("is", "stray", "ContinuationPath"),
                                    ("is-not", "stray", "ResonatusCandidate"),
                                    ("is-not", "stray", "Resonatus")]},
]


def reason(fixture: str):
    g = rdflib.Graph()
    g.parse(ONT, format="turtle")
    g.parse(fixture, format="turtle")
    tmp = tempfile.NamedTemporaryFile(suffix=".owl", delete=False)
    g.serialize(destination=tmp.name, format="xml")
    w = World()
    w.get_ontology("file://" + tmp.name).load()
    sync_reasoner_hermit(w, infer_property_values=True, debug=0)
    return w


def run_gate(gate) -> tuple[bool, list[str]]:
    ns = gate.get("ns", "https://example.org/resonatus/reasoner/")
    msgs: list[str] = []
    try:
        w = reason(gate["fixture"])
    except OwlReadyInconsistentOntologyError:
        if gate["consistent"] is False:
            return True, ["INCONSISTENT as required"]
        return False, ["unexpected INCONSISTENT"]
    if gate["consistent"] is False:
        return False, ["expected INCONSISTENT but ontology is consistent"]

    ok = True
    for chk in gate["checks"]:
        kind = chk[0]
        if kind in ("is", "is-not"):
            _, ind_n, cls_n = chk
            ind = w.search_one(iri=ns + ind_n)
            cls_iris = {c.iri for c in ind.INDIRECT_is_a if hasattr(c, "iri")} if ind else set()
            has = (RES + cls_n) in cls_iris
            want = kind == "is"
            good = has == want
            msgs.append(f"{'PASS' if good else 'FAIL'} {ind_n} {kind} res:{cls_n} (actual={has})")
            ok = ok and good
        elif kind in ("prop", "not-prop"):
            _, s_n, p_n, o_n = chk
            subj = w.search_one(iri=ns + s_n)
            prop = w.search_one(iri=RES + p_n)
            obj = w.search_one(iri=ns + o_n)
            vals = set(prop[subj]) if (subj and prop) else set()
            has = obj in vals
            want = kind == "prop"
            good = has == want
            msgs.append(f"{'PASS' if good else 'FAIL'} {s_n} {kind} res:{p_n} -> {o_n} (actual={has})")
            ok = ok and good
    return ok, msgs


def run_r2_bfo() -> tuple[bool, list[str]]:
    """R2: core + bridge + official (vendored, pinned) BFO 2020 must be consistent, with the key classes
    satisfiable. Uses the offline pinned copy alignments/vendor/bfo-2020-core.owl."""
    import os
    bfo = "alignments/vendor/bfo-2020-core.owl"
    if not os.path.exists(bfo):
        return False, ["TOOL RESULT UNAVAILABLE: vendored BFO 2020 not found"]
    g = rdflib.Graph()
    g.parse(ONT, format="turtle")
    g.parse("alignments/resonatus-bfo.ttl", format="turtle")
    g.parse(bfo, format="xml")
    # OFFLINE: the vendored BFO axioms are already merged into `g` above, so the bridge's
    # `owl:imports <.../bfo.owl>` pointer is redundant. Drop it before serializing, otherwise a fresh
    # Owlready2 world would FOLLOW the import IRI and attempt a network download of BFO instead of using
    # the pinned vendored copy. Removing the redundant pointer keeps R2 fully offline with identical
    # logical content (all BFO axioms remain present in the merged graph).
    g.remove((None, rdflib.OWL.imports, rdflib.URIRef("http://purl.obolibrary.org/obo/bfo/2020/bfo.owl")))
    tmp = tempfile.NamedTemporaryFile(suffix=".owl", delete=False)
    g.serialize(destination=tmp.name, format="xml")
    w = World()
    w.get_ontology("file://" + tmp.name).load()
    try:
        sync_reasoner_hermit(w, debug=0)
    except OwlReadyInconsistentOntologyError:
        return False, ["INCONSISTENT with BFO bridge (BLOCKER)"]
    inc = list(w.inconsistent_classes())
    msgs = [f"consistent; unsatisfiable named classes: {[getattr(c,'iri','?') for c in inc] or 'NONE'}"]
    ok = not inc
    for cn in ("Resonatus", "ResonatusPath", "ContinuationPath", "CausalTraceProcess"):
        c = w.search_one(iri=RES + cn)
        sat = c is not None and c not in inc
        msgs.append(f"{'PASS' if sat else 'FAIL'} satisfiable res:{cn}")
        ok = ok and sat
    return ok, msgs


def main() -> int:
    all_ok = True
    r2_ok, r2_msgs = run_r2_bfo()
    all_ok = all_ok and r2_ok
    print(f"[{'PASS' if r2_ok else 'FAIL'}] R2  (core+bridge+official BFO 2020, pinned/vendored)")
    for m in r2_msgs:
        print(f"        {m}")
    for gate in GATES:
        ok, msgs = run_gate(gate)
        all_ok = all_ok and ok
        print(f"[{'PASS' if ok else 'FAIL'}] {gate['id']}  ({gate['fixture'].split('/')[-1]})")
        for m in msgs:
            print(f"        {m}")
    print(f"\nSUMMARY: {'ALL GATES PASS' if all_ok else 'GATE FAILURES PRESENT'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
