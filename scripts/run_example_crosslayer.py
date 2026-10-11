#!/usr/bin/env python3
"""Cross-layer validation for worked examples and layer-independence counterexamples.

The 13 worked examples were intentionally authored so their epistemic assessment and ontic graph
agree. They remain useful regression fixtures, but agreement on those coupled examples is not evidence
that OWL membership and epistemic support are equivalent in general.

This runner therefore performs three separate checks:

1. the 13 aligned examples still have their declared OWL and SHACL outcomes;
2. two adversarial fixtures deliberately make the ontic and epistemic layers disagree, proving that
   neither layer silently creates a result in the other; and
3. inconsistent OWL input and execution failures retain their own outcomes instead of becoming
   ordinary non-entailment.

Usage: python scripts/run_example_crosslayer.py
"""
from __future__ import annotations

import glob
import tempfile
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import rdflib
from owlready2 import World, sync_reasoner_hermit
from owlready2.base import OwlReadyInconsistentOntologyError
from pyshacl import validate

RES = "https://w3id.org/resonatus#"
CASE = "https://example.org/resonatus/case/"
ONT = "ontology/resonatus.ttl"
SHAPES = "shapes/resonatus.shacl.ttl"
CRITERIA = (
    RES + "TraceCriterion",
    RES + "DelayCriterion",
    RES + "PropagationCriterion",
    RES + "SelectivityCriterion",
    RES + "TransformationFeedbackCriterion",
)
VALID_VERDICTS = {
    RES + "PASS",
    RES + "FAIL",
    RES + "NOT_MEASURED",
    RES + "INCONCLUSIVE",
    RES + "ERROR",
}


class OwlOutcome(str, Enum):
    ENTAILED = "ENTAILED"
    NOT_ENTAILED = "NOT_ENTAILED"
    INCONSISTENT = "INCONSISTENT"
    EXECUTION_ERROR = "EXECUTION_ERROR"


@dataclass(frozen=True)
class OwlResult:
    outcome: OwlOutcome
    detail: str = ""


INDEPENDENCE_GATES = (
    {
        "id": "CL1",
        "fixture": "tests/crosslayer/ontic-positive-epistemic-undetermined.ttl",
        "candidate": CASE + "ontic_positive_epistemic_undetermined",
        "expected_classification": "UNDETERMINED",
        "expected_owl": OwlOutcome.ENTAILED,
        "expected_shacl": True,
    },
    {
        "id": "CL2",
        "fixture": "tests/crosslayer/epistemic-supported-ontic-not-entailed.ttl",
        "candidate": CASE + "epistemic_supported_ontic_not_entailed",
        "expected_classification": "MEMBERSHIP_SUPPORTED",
        "expected_owl": OwlOutcome.NOT_ENTAILED,
        "expected_shacl": True,
    },
)


def the_candidate(example: str) -> str | None:
    """Return the single explicitly declared ResonatusCandidate in a fixture."""
    graph = rdflib.Graph()
    graph.parse(example, format="turtle")
    candidates = list(
        graph.subjects(rdflib.RDF.type, rdflib.URIRef(RES + "ResonatusCandidate"))
    )
    return str(candidates[0]) if len(candidates) == 1 else None


def owl_membership_outcome(example: str, candidate_iri: str) -> OwlResult:
    """Classify the reasoner outcome without collapsing inconsistency or errors into non-entailment."""
    try:
        graph = rdflib.Graph()
        graph.parse(ONT, format="turtle")
        graph.parse(example, format="turtle")
        with tempfile.TemporaryDirectory(prefix="resonatus-crosslayer-") as temp_dir:
            merged_path = Path(temp_dir) / "merged.owl"
            graph.serialize(destination=merged_path, format="xml")
            world = World()
            world.get_ontology(merged_path.as_uri()).load()
            try:
                sync_reasoner_hermit(world, infer_property_values=True, debug=0)
            except OwlReadyInconsistentOntologyError as exc:
                return OwlResult(OwlOutcome.INCONSISTENT, str(exc))

            individual = world.search_one(iri=candidate_iri)
            is_resonatus = bool(
                individual
                and any(
                    getattr(cls, "iri", None) == RES + "Resonatus"
                    for cls in individual.INDIRECT_is_a
                )
            )
            return OwlResult(
                OwlOutcome.ENTAILED if is_resonatus else OwlOutcome.NOT_ENTAILED
            )
    except Exception as exc:  # A broken parser, reasoner, or input is a gate failure, not non-entailment.
        return OwlResult(OwlOutcome.EXECUTION_ERROR, f"{type(exc).__name__}: {exc}")


def declared_classification(example: str, candidate_iri: str) -> str:
    """Read the declared expectedClassification bound to the selected candidate."""
    graph = rdflib.Graph()
    graph.parse(example, format="turtle")
    values = list(
        graph.objects(
            rdflib.URIRef(candidate_iri),
            rdflib.URIRef(RES + "expectedClassification"),
        )
    )
    return str(values[0]) if len(values) == 1 else "?"


def epistemic_classification(example: str, candidate_iri: str) -> str:
    """Compute the reference epistemic result from the candidate's five criterion verdicts."""
    graph = rdflib.Graph()
    graph.parse(example, format="turtle")
    candidate = rdflib.URIRef(candidate_iri)
    assesses = rdflib.URIRef(RES + "assesses")
    assessment_type = rdflib.URIRef(RES + "ResonatusAssessment")
    assessments = [
        subject
        for subject in graph.subjects(assesses, candidate)
        if (subject, rdflib.RDF.type, assessment_type) in graph
    ]
    if len(assessments) != 1:
        raise ValueError(f"expected one bound ResonatusAssessment, found {len(assessments)}")

    criterion_property = rdflib.URIRef(RES + "criterion")
    verdict_property = rdflib.URIRef(RES + "verdict")
    criterion_assessment_property = rdflib.URIRef(RES + "hasCriterionAssessment")
    by_criterion: dict[str, str] = {}
    criterion_assessments = list(
        graph.objects(assessments[0], criterion_assessment_property)
    )
    if len(criterion_assessments) != 5:
        raise ValueError(
            f"expected five criterion assessments, found {len(criterion_assessments)}"
        )
    for criterion_assessment in criterion_assessments:
        criteria = list(graph.objects(criterion_assessment, criterion_property))
        verdicts = list(graph.objects(criterion_assessment, verdict_property))
        if len(criteria) != 1 or len(verdicts) != 1:
            raise ValueError("criterion assessment must have exactly one criterion and verdict")
        criterion = str(criteria[0])
        verdict = str(verdicts[0])
        if criterion not in CRITERIA or verdict not in VALID_VERDICTS:
            raise ValueError("criterion assessment uses an unknown criterion or verdict")
        if criterion in by_criterion:
            raise ValueError(f"duplicate criterion assessment: {criterion}")
        by_criterion[criterion] = verdict
    if set(by_criterion) != set(CRITERIA):
        raise ValueError("criterion assessment set is incomplete")

    verdicts = [by_criterion[criterion] for criterion in CRITERIA]
    if RES + "FAIL" in verdicts:
        return "NON_MEMBERSHIP_SUPPORTED"
    if all(verdict == RES + "PASS" for verdict in verdicts):
        return "MEMBERSHIP_SUPPORTED"
    return "UNDETERMINED"


def shacl_conforms(example: str, shapes: rdflib.Graph) -> bool:
    data = rdflib.Graph().parse(example, format="turtle")
    conforms, _, _ = validate(
        data_graph=data,
        shacl_graph=shapes,
        inference="none",
        advanced=True,
    )
    return bool(conforms)


def run_aligned_examples(shapes: rdflib.Graph) -> tuple[bool, int, int]:
    """Check the intentionally aligned examples without generalizing their agreement into a rule."""
    passed = 0
    total = 0
    for fixture in sorted(glob.glob("examples/*.ttl")):
        total += 1
        candidate = the_candidate(fixture)
        if candidate is None:
            print(
                f"[FAIL] aligned {Path(fixture).name:44s} "
                "could not bind a single ResonatusCandidate"
            )
            continue

        declared = declared_classification(fixture, candidate)
        try:
            epistemic = epistemic_classification(fixture, candidate)
        except ValueError as exc:
            print(f"[FAIL] aligned {Path(fixture).name:44s} epistemic_error={exc}")
            continue
        expected_owl = (
            OwlOutcome.ENTAILED
            if epistemic == "MEMBERSHIP_SUPPORTED"
            else OwlOutcome.NOT_ENTAILED
        )
        owl_result = owl_membership_outcome(fixture, candidate)
        conforms = shacl_conforms(fixture, shapes)
        ok = declared == epistemic and owl_result.outcome == expected_owl and conforms
        if ok:
            passed += 1
        detail = f" detail={owl_result.detail}" if owl_result.detail and not ok else ""
        print(
            f"[{'PASS' if ok else 'FAIL'}] aligned {Path(fixture).name:44s} "
            f"epistemic={epistemic:24s} declared={declared:24s} "
            f"OWL={owl_result.outcome.value:14s} "
            f"SHACL_conforms={conforms}{detail}"
        )
    return passed == total, passed, total


def run_independence_gates(shapes: rdflib.Graph) -> tuple[bool, int, int]:
    """Verify that deliberate cross-layer disagreement remains representable and observable."""
    passed = 0
    for gate in INDEPENDENCE_GATES:
        declared = declared_classification(gate["fixture"], gate["candidate"])
        try:
            epistemic = epistemic_classification(gate["fixture"], gate["candidate"])
        except ValueError as exc:
            print(
                f"[FAIL] {gate['id']} {Path(gate['fixture']).name:48s} "
                f"epistemic_error={exc}"
            )
            continue
        owl_result = owl_membership_outcome(gate["fixture"], gate["candidate"])
        conforms = shacl_conforms(gate["fixture"], shapes)
        ok = (
            epistemic == gate["expected_classification"]
            and declared == epistemic
            and owl_result.outcome == gate["expected_owl"]
            and conforms == gate["expected_shacl"]
        )
        if ok:
            passed += 1
        detail = f" detail={owl_result.detail}" if owl_result.detail and not ok else ""
        print(
            f"[{'PASS' if ok else 'FAIL'}] {gate['id']} {Path(gate['fixture']).name:48s} "
            f"epistemic={epistemic:24s} declared={declared:24s} "
            f"OWL={owl_result.outcome.value:14s} "
            f"SHACL_conforms={conforms}{detail}"
        )
    return passed == len(INDEPENDENCE_GATES), passed, len(INDEPENDENCE_GATES)


def run_inconsistency_guard() -> bool:
    """Regression check for the former INCONSISTENT -> False collapse."""
    result = owl_membership_outcome(
        "tests/owl-two-declared-origins-inconsistent.ttl",
        CASE + "inconsistency_probe",
    )
    ok = result.outcome == OwlOutcome.INCONSISTENT
    detail = f" detail={result.detail}" if result.detail and not ok else ""
    print(
        f"[{'PASS' if ok else 'FAIL'}] CL3 inconsistent ontology outcome "
        f"OWL={result.outcome.value}{detail}"
    )
    return ok


def run_execution_error_guard() -> bool:
    """Verify that an unreadable input becomes EXECUTION_ERROR rather than NOT_ENTAILED."""
    result = owl_membership_outcome(
        "tests/crosslayer/__intentionally_missing_fixture__.ttl",
        CASE + "execution_error_probe",
    )
    ok = result.outcome == OwlOutcome.EXECUTION_ERROR
    detail = f" detail={result.detail}" if result.detail and not ok else ""
    print(
        f"[{'PASS' if ok else 'FAIL'}] CL4 execution error outcome "
        f"OWL={result.outcome.value}{detail}"
    )
    return ok


def main() -> int:
    shapes = rdflib.Graph().parse(SHAPES, format="turtle")
    aligned_ok, aligned_passed, aligned_total = run_aligned_examples(shapes)
    print()
    independence_ok, independence_passed, independence_total = run_independence_gates(shapes)
    inconsistency_ok = run_inconsistency_guard()
    execution_error_ok = run_execution_error_guard()

    all_ok = aligned_ok and independence_ok and inconsistency_ok and execution_error_ok
    print(
        "\nSUMMARY: "
        f"aligned={aligned_passed}/{aligned_total}; "
        f"layer_independence={independence_passed}/{independence_total}; "
        f"inconsistency_guard={'PASS' if inconsistency_ok else 'FAIL'}; "
        f"execution_error_guard={'PASS' if execution_error_ok else 'FAIL'}; "
        f"overall={'PASS' if all_ok else 'FAIL'}"
    )
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
