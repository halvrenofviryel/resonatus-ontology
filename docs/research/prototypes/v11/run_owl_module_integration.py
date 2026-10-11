#!/usr/bin/env python3
"""Integration gates for the optional Resonatus v1.1 experimental OWL module.

The script compares observed HermiT results under three explicit configurations:

  A. published core only
  B. core + experimental vocabulary
  C. core + experimental vocabulary + optional BFO bridge and pinned BFO 2020

It does not alter the published ontology, infer expected values from fixtures, or publish the
experimental namespace.
"""
from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path

import rdflib
from owlready2 import World, sync_reasoner_hermit
from owlready2.base import OwlReadyInconsistentOntologyError

from run_prototypes import (
    CORE,
    EXP,
    FIX,
    RES,
    CausalCommitment,
    causal_commitment,
    one_candidate,
    parse_union,
)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
EXPERIMENTAL_VOCAB = HERE / "experimental-vocabulary.ttl"
BFO_BRIDGE = ROOT / "alignments/resonatus-bfo.ttl"
BFO_PINNED = ROOT / "alignments/vendor/bfo-2020-core.owl"
BFO_IMPORT = rdflib.URIRef("http://purl.obolibrary.org/obo/bfo/2020/bfo.owl")
EX = rdflib.Namespace("https://example.org/resonatus/prototype/")


@dataclass(frozen=True)
class Configuration:
    name: str
    experimental: bool
    bfo: bool


@dataclass(frozen=True)
class Observation:
    consistent: bool | None
    unsatisfiable: tuple[str, ...]
    types: dict[str, frozenset[str]]
    error: str | None = None


CONFIGURATIONS = (
    Configuration("A_CORE", experimental=False, bfo=False),
    Configuration("B_CORE_EXP", experimental=True, bfo=False),
    Configuration("C_CORE_EXP_BFO", experimental=True, bfo=True),
)

CASES = {
    "VALID_B": parse_union((FIX / "b-valid-process-path.ttl",)),
    "VALID_C": parse_union((FIX / "b-valid-process-path.ttl", FIX / "c-valid-overlay.ttl")),
    "COLLAPSED_SCOPE": parse_union(
        (FIX / "b-valid-process-path.ttl", FIX / "c-invalid-scope-is-process-overlay.ttl")
    ),
    "CLAIM_ONLY": parse_union((FIX / "claim-only-no-ontic-causation.ttl",)),
}

ISOLATED_CLAIM = rdflib.Graph()
ISOLATED_CLAIM.add((EX.isolatedClaim, rdflib.RDF.type, EXP.CausalAttributionClaim))
ISOLATED_CLAIM.add((EX.isolatedClaim, EXP.causalSubject, EX.isolatedSubject))
ISOLATED_CLAIM.add((EX.isolatedClaim, EXP.causalObject, EX.isolatedObject))
CASES["ISOLATED_CLAIM"] = ISOLATED_CLAIM

EXPECTED_CONSISTENCY = {
    (case, config.name): not (
        case == "COLLAPSED_SCOPE" and config.experimental
    )
    for case in CASES
    for config in CONFIGURATIONS
}

RELEVANT_CLASSES = (
    str(RES.Resonatus),
    str(RES.ResonatusPath),
    str(RES.ContinuationPath),
    str(RES.CausalTraceProcess),
    str(EXP.AssessmentScope),
    str(EXP.CausalAttributionClaim),
)

WATCHED_INDIVIDUALS = (
    str(EX.candidate),
    str(EX.trace),
    str(EX.isolatedSubject),
    str(EX.isolatedObject),
)


def configured_graph(config: Configuration, data: rdflib.Graph) -> rdflib.Graph:
    graph = rdflib.Graph()
    graph.parse(CORE, format="turtle")
    if config.experimental:
        graph.parse(EXPERIMENTAL_VOCAB, format="turtle")
    if config.bfo:
        graph.parse(BFO_BRIDGE, format="turtle")
        graph.parse(BFO_PINNED, format="xml")
        # The pinned axioms are already present; removing only the redundant import prevents a network
        # lookup and leaves the logical content unchanged.
        graph.remove((None, rdflib.OWL.imports, BFO_IMPORT))
    for triple in data:
        graph.add(triple)
    return graph


def observe(config: Configuration, data: rdflib.Graph) -> Observation:
    try:
        graph = configured_graph(config, data)
        with tempfile.TemporaryDirectory(prefix="resonatus-v11-module-") as tmp:
            path = Path(tmp) / "merged.owl"
            graph.serialize(destination=path, format="xml")
            world = World()
            world.get_ontology(path.as_uri()).load()
            try:
                sync_reasoner_hermit(world, infer_property_values=True, debug=0)
            except OwlReadyInconsistentOntologyError:
                return Observation(False, (), {})
            unsatisfiable = tuple(
                sorted(
                    str(getattr(cls, "iri", ""))
                    for cls in world.inconsistent_classes()
                    if getattr(cls, "iri", None)
                    and str(getattr(cls, "iri", ""))
                    != "http://www.w3.org/2002/07/owl#Nothing"
                )
            )
            types: dict[str, frozenset[str]] = {}
            for iri in WATCHED_INDIVIDUALS:
                individual = world.search_one(iri=iri)
                types[iri] = frozenset(
                    str(getattr(cls, "iri", ""))
                    for cls in getattr(individual, "INDIRECT_is_a", ())
                    if getattr(cls, "iri", None)
                )
            return Observation(True, unsatisfiable, types)
    except Exception as exc:
        return Observation(None, (), {}, f"{type(exc).__name__}: {exc}")


def has_type(observation: Observation, individual: rdflib.URIRef, cls: rdflib.URIRef) -> bool:
    return str(cls) in observation.types.get(str(individual), frozenset())


def main() -> int:
    observations: dict[tuple[str, str], Observation] = {}
    checks: list[tuple[str, bool]] = []

    print("CASE             CONFIG           CONSISTENCY   RESONATUS  UNSAT_NAMED")
    print("-" * 76)
    for case_name, data in CASES.items():
        for config in CONFIGURATIONS:
            observation = observe(config, data)
            observations[(case_name, config.name)] = observation
            expected_consistent = EXPECTED_CONSISTENCY[(case_name, config.name)]
            consistency_ok = observation.consistent is expected_consistent
            checks.append((f"{case_name}/{config.name} consistency", consistency_ok))

            candidate_membership = (
                "N/A"
                if case_name == "ISOLATED_CLAIM" or observation.consistent is not True
                else "YES" if has_type(observation, EX.candidate, RES.Resonatus) else "NO"
            )
            status = (
                "ERROR"
                if observation.consistent is None
                else "CONSISTENT" if observation.consistent else "INCONSISTENT"
            )
            print(
                f"[{'PASS' if consistency_ok else 'FAIL'}] {case_name:16s} {config.name:16s} "
                f"{status:13s} {candidate_membership:10s} "
                f"{len(observation.unsatisfiable)}"
            )
            if observation.error:
                print(f"       ERROR: {observation.error}")

    # All relevant named classes must remain satisfiable in each configuration where they are loaded.
    for config in CONFIGURATIONS:
        observation = observations[("VALID_C", config.name)]
        class_iris = RELEVANT_CLASSES if config.experimental else RELEVANT_CLASSES[:4]
        satisfiable = observation.consistent is True and not any(
            cls in observation.unsatisfiable for cls in class_iris
        )
        checks.append((f"{config.name} relevant named classes satisfiable", satisfiable))
        print(
            f"[{'PASS' if satisfiable else 'FAIL'}] {config.name} relevant named classes "
            f"satisfiable; unsatisfiable={observation.unsatisfiable or 'NONE'}"
        )

    # Adding the optional modules must not change published Resonatus membership for consistent cases.
    for case_name in ("VALID_B", "VALID_C", "CLAIM_ONLY"):
        membership = []
        for config in CONFIGURATIONS:
            observation = observations[(case_name, config.name)]
            membership.append(has_type(observation, EX.candidate, RES.Resonatus))
        invariant = len(set(membership)) == 1
        checks.append((f"{case_name} membership invariant", invariant))
        print(
            f"[{'PASS' if invariant else 'FAIL'}] {case_name} published membership by config: "
            + ", ".join(
                f"{config.name}={value}" for config, value in zip(CONFIGURATIONS, membership)
            )
        )

    # Claim properties alone must not turn their fillers into ontic Trace/Interaction individuals.
    for config in CONFIGURATIONS:
        observation = observations[("ISOLATED_CLAIM", config.name)]
        subject_trace = has_type(observation, EX.isolatedSubject, RES.TraceContinuation)
        object_interaction = has_type(observation, EX.isolatedObject, RES.Interaction)
        clean = observation.consistent is True and not subject_trace and not object_interaction
        checks.append((f"{config.name} isolated claim no ontic typing", clean))
        print(
            f"[{'PASS' if clean else 'FAIL'}] {config.name} isolated claim ontic typing: "
            f"subject_trace={subject_trace} object_interaction={object_interaction}"
        )

    claim_only = CASES["CLAIM_ONLY"]
    commitment = causal_commitment(claim_only, one_candidate(claim_only))
    no_named_relation = not any(claim_only.triples((None, RES.causallyAttributedTo, None)))
    existential_ok = (
        commitment is CausalCommitment.EXISTENTIAL_COMMITMENT_ONLY and no_named_relation
    )
    checks.append(("claim-only existential commitment", existential_ok))
    print(
        f"[{'PASS' if existential_ok else 'FAIL'}] claim-only commitment={commitment.value} "
        f"named_relation={not no_named_relation}"
    )

    # Record the only intended configuration difference: experimental disjointness exposes collapse.
    collapse_states = tuple(
        observations[("COLLAPSED_SCOPE", config.name)].consistent
        for config in CONFIGURATIONS
    )
    intended_difference = collapse_states == (True, False, False)
    checks.append(("collapsed-scope configuration difference", intended_difference))
    print(
        f"[{'PASS' if intended_difference else 'FAIL'}] COLLAPSED_SCOPE difference "
        f"A/B/C={collapse_states} (experimental disjointness active only in B/C)"
    )

    passed = sum(ok for _, ok in checks)
    print(
        f"\nSUMMARY: integration_checks={passed}/{len(checks)}; "
        f"overall={'PASS' if all(ok for _, ok in checks) else 'FAIL'}"
    )
    return 0 if all(ok for _, ok in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
