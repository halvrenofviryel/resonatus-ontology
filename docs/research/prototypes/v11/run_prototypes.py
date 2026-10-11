#!/usr/bin/env python3
"""Run the isolated Resonatus v1.1 semantic hardening cases.

The runner computes each result from the data and shapes, then compares it with an explicit test oracle.
It never substitutes an expected value for a computed value. The unchanged v1.0.0 core is used for OWL
reasoning, while experimental SHACL dimensions are evaluated independently:

  CURRENT     published v1.0.0 SHACL profile
  LINEAGE     bounded linear path structure
  TEMPORAL    optional Delay interval profile
  SCOPE       assessment-scope/process separation
  CLAIM_RECORD, ONTIC_LINKAGE, EVIDENCE_RECORD
              independent epistemic-record dimensions

No structural result is reported as scientific causal validation.
"""
from __future__ import annotations

import tempfile
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import rdflib
from owlready2 import World, sync_reasoner_hermit
from owlready2.base import OwlReadyInconsistentOntologyError
from pyshacl import validate

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CORE = ROOT / "ontology/resonatus.ttl"
CURRENT_SHAPES = ROOT / "shapes/resonatus.shacl.ttl"
RES = rdflib.Namespace("https://w3id.org/resonatus#")
EXP = rdflib.Namespace("https://w3id.org/resonatus/experimental/v1.1#")
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")


class OwlOutcome(str, Enum):
    ENTAILED = "OWL_ENTAILED"
    NOT_ENTAILED = "OWL_NOT_ENTAILED"
    INCONSISTENT = "OWL_INCONSISTENT"
    EXECUTION_ERROR = "OWL_EXECUTION_ERROR"


class ValidationOutcome(str, Enum):
    CONFORMING = "CONFORMING"
    NON_CONFORMING = "NON_CONFORMING"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    NOT_EVALUATED = "NOT_EVALUATED"
    EXECUTION_ERROR = "EXECUTION_ERROR"


class ProfileApplicability(str, Enum):
    IN_SCOPE = "IN_SCOPE"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"


class CausalCommitment(str, Enum):
    EXPLICIT_ONTIC_RELATION = "EXPLICIT_ONTIC_RELATION"
    EXISTENTIAL_COMMITMENT_ONLY = "EXISTENTIAL_COMMITMENT_ONLY"
    NONE_IDENTIFIED = "NONE_IDENTIFIED"


class DomainEvidenceOutcome(str, Enum):
    UNASSESSED = "DOMAIN_EVIDENCE_UNASSESSED"
    NOT_EVALUATED = "DOMAIN_EVIDENCE_NOT_EVALUATED"


@dataclass(frozen=True)
class ValidationResult:
    outcome: ValidationOutcome
    messages: tuple[str, ...] = ()
    components: tuple[str, ...] = ()
    focus_nodes: tuple[str, ...] = ()
    applicability: ProfileApplicability = ProfileApplicability.IN_SCOPE
    activated: bool = True


@dataclass(frozen=True)
class Expected:
    owl: OwlOutcome
    current: ValidationOutcome
    lineage: ValidationOutcome
    temporal: ValidationOutcome
    scope: ValidationOutcome
    claim_record: ValidationOutcome
    ontic_linkage: ValidationOutcome
    evidence_record: ValidationOutcome
    domain_evidence: DomainEvidenceOutcome
    causal_commitment: CausalCommitment


@dataclass(frozen=True)
class Actual:
    owl: OwlOutcome
    current: ValidationOutcome
    lineage: ValidationOutcome
    temporal: ValidationOutcome
    scope: ValidationOutcome
    claim_record: ValidationOutcome
    ontic_linkage: ValidationOutcome
    evidence_record: ValidationOutcome
    domain_evidence: DomainEvidenceOutcome
    causal_commitment: CausalCommitment


@dataclass(frozen=True)
class Case:
    case_id: str
    files: tuple[Path, ...]
    expected: Expected


FIX = HERE / "fixtures"
COUNTER = ROOT / "docs/research/counterexamples"
C = ValidationOutcome.CONFORMING
N = ValidationOutcome.NON_CONFORMING
I = ValidationOutcome.INSUFFICIENT_DATA
X = ValidationOutcome.NOT_EVALUATED
EXPLICIT = CausalCommitment.EXPLICIT_ONTIC_RELATION
EXISTENTIAL = CausalCommitment.EXISTENTIAL_COMMITMENT_ONLY
U = DomainEvidenceOutcome.UNASSESSED
NE = DomainEvidenceOutcome.NOT_EVALUATED

CASES = (
    Case(
        "CE01_GROUPED_NO_LINEAGE",
        (COUNTER / "ce01-grouped-witnesses-no-lineage.ttl",),
        Expected(OwlOutcome.ENTAILED, C, I, I, X, X, X, X, NE, EXPLICIT),
    ),
    Case(
        "CE02_SINGLE_NODE_COLLAPSE",
        (COUNTER / "ce02-single-node-collapse.ttl",),
        Expected(OwlOutcome.ENTAILED, C, N, I, X, X, X, X, NE, EXPLICIT),
    ),
    Case(
        "B_VALID_PROCESS_PATH",
        (FIX / "b-valid-process-path.ttl",),
        Expected(OwlOutcome.ENTAILED, C, C, C, X, X, X, X, NE, EXPLICIT),
    ),
    Case(
        "B_REVERSED_LINEAGE",
        (FIX / "b-invalid-reversed-lineage.ttl",),
        Expected(OwlOutcome.ENTAILED, C, N, C, X, X, X, X, NE, EXPLICIT),
    ),
    Case(
        "B_DELAY_ENDS_AT_ORIGIN_END",
        (FIX / "b-invalid-delay-ends-at-origin-end.ttl",),
        Expected(OwlOutcome.ENTAILED, C, C, N, X, X, X, X, NE, EXPLICIT),
    ),
    Case(
        "B_UNRELATED_DELAY",
        (FIX / "b-invalid-unrelated-delay.ttl",),
        Expected(OwlOutcome.ENTAILED, C, C, N, X, X, X, X, NE, EXPLICIT),
    ),
    Case(
        "C_VALID_SEPARATE_SCOPE",
        (FIX / "b-valid-process-path.ttl", FIX / "c-valid-overlay.ttl"),
        Expected(OwlOutcome.ENTAILED, C, C, C, C, C, C, C, U, EXPLICIT),
    ),
    Case(
        "C_SCOPE_IS_PROCESS",
        (FIX / "b-valid-process-path.ttl", FIX / "c-invalid-scope-is-process-overlay.ttl"),
        Expected(OwlOutcome.ENTAILED, C, C, C, N, C, C, C, U, EXPLICIT),
    ),
    Case(
        "CLAIM_WITHOUT_ONTIC_CAUSATION",
        (FIX / "claim-only-no-ontic-causation.ttl",),
        Expected(OwlOutcome.ENTAILED, N, I, C, C, C, I, C, U, EXISTENTIAL),
    ),
    Case(
        "B_MISSING_TEMPORAL_DATA",
        (FIX / "b-insufficient-temporal-data.ttl",),
        Expected(OwlOutcome.ENTAILED, C, C, I, X, X, X, X, NE, EXPLICIT),
    ),
    Case(
        "B_SHARED_ORIGIN_BRANCHES",
        (FIX / "b-out-of-scope-shared-origin-branches.ttl",),
        Expected(OwlOutcome.ENTAILED, C, I, C, X, X, X, X, NE, EXPLICIT),
    ),
    Case(
        "B_UNRELATED_TRANSFORMATION",
        (FIX / "b-insufficient-unrelated-transformation.ttl",),
        Expected(OwlOutcome.ENTAILED, C, I, C, X, X, X, X, NE, EXPLICIT),
    ),
    Case(
        "ONTIC_WITH_INADEQUATE_EVIDENCE",
        (FIX / "b-valid-process-path.ttl", FIX / "claim-missing-evidence-overlay.ttl"),
        Expected(OwlOutcome.ENTAILED, C, C, C, X, C, C, I, U, EXPLICIT),
    ),
    Case(
        "CLAIM_INCOMPLETE_RECORD",
        (FIX / "b-valid-process-path.ttl", FIX / "claim-incomplete-record-overlay.ttl"),
        Expected(OwlOutcome.ENTAILED, C, C, C, X, I, C, C, U, EXPLICIT),
    ),
    Case(
        "CLAIM_CONFLICTING_LINKAGE",
        (FIX / "b-valid-process-path.ttl", FIX / "claim-conflicting-linkage-overlay.ttl"),
        Expected(OwlOutcome.ENTAILED, C, C, C, X, C, N, C, U, EXPLICIT),
    ),
)


def parse_union(paths: tuple[Path, ...]) -> rdflib.Graph:
    graph = rdflib.Graph()
    for path in paths:
        graph.parse(path, format="turtle")
    return graph


def shape_union(*names: str) -> rdflib.Graph:
    return parse_union(tuple(HERE / "shapes" / name for name in names))


def profile_shapes() -> dict[str, rdflib.Graph]:
    return {
        "current": parse_union((CURRENT_SHAPES,)),
        "lineage": shape_union("strict-process-path.shacl.ttl"),
        "temporal": shape_union("temporal-delay.shacl.ttl"),
        "scope": shape_union("separate-assessment-scope.shacl.ttl"),
        "claim_record": shape_union("causal-claim-record.shacl.ttl"),
        "ontic_linkage": shape_union("causal-claim-ontic-linkage.shacl.ttl"),
        "evidence_record": shape_union("causal-claim-evidence.shacl.ttl"),
    }


def one_candidate(data: rdflib.Graph) -> rdflib.URIRef:
    candidates = sorted(set(data.subjects(rdflib.RDF.type, RES.ResonatusCandidate)))
    if len(candidates) != 1:
        raise ValueError(f"expected one explicit ResonatusCandidate, found {len(candidates)}")
    return candidates[0]


def owl_outcome(data: rdflib.Graph, candidate: rdflib.URIRef) -> OwlOutcome:
    try:
        merged = rdflib.Graph()
        merged.parse(CORE, format="turtle")
        for triple in data:
            merged.add(triple)
        with tempfile.TemporaryDirectory(prefix="resonatus-v11-prototype-") as tmp:
            path = Path(tmp) / "merged.owl"
            merged.serialize(destination=path, format="xml")
            world = World()
            world.get_ontology(path.as_uri()).load()
            try:
                sync_reasoner_hermit(world, infer_property_values=True, debug=0)
            except OwlReadyInconsistentOntologyError:
                return OwlOutcome.INCONSISTENT
            individual = world.search_one(iri=str(candidate))
            entailed = bool(
                individual
                and any(
                    getattr(cls, "iri", None) == str(RES.Resonatus)
                    for cls in individual.INDIRECT_is_a
                )
            )
            return OwlOutcome.ENTAILED if entailed else OwlOutcome.NOT_ENTAILED
    except Exception:
        return OwlOutcome.EXECUTION_ERROR


def validation_result(
    data: rdflib.Graph,
    shapes: rdflib.Graph,
    *,
    activated: bool = True,
) -> ValidationResult:
    if not activated:
        return ValidationResult(ValidationOutcome.NOT_EVALUATED, activated=False)
    try:
        conforms, report, _ = validate(
            data_graph=data,
            shacl_graph=shapes,
            inference="none",
            advanced=True,
            debug=False,
        )
        if not isinstance(report, rdflib.Graph):
            return ValidationResult(
                ValidationOutcome.EXECUTION_ERROR,
                ("validation engine did not return an RDF report graph",),
            )
        results = tuple(report.objects(None, SH.result))
        messages = tuple(
            sorted(
                {
                    str(message)
                    for result in results
                    for message in report.objects(result, SH.resultMessage)
                }
            )
        )
        components = tuple(
            sorted(
                {
                    str(component)
                    for result in results
                    for component in report.objects(result, SH.sourceConstraintComponent)
                }
            )
        )
        focus_nodes = tuple(
            sorted(
                {
                    str(node)
                    for result in results
                    for node in report.objects(result, SH.focusNode)
                }
            )
        )
        if bool(conforms):
            return ValidationResult(ValidationOutcome.CONFORMING)
        out_of_scope = any(message.startswith("OUT_OF_SCOPE_") for message in messages)
        applicability = (
            ProfileApplicability.OUT_OF_SCOPE
            if out_of_scope
            else ProfileApplicability.IN_SCOPE
        )
        # Applicability and validation are independent. An out-of-scope finding must not mask an
        # explicit violation or missing-data finding in the same SHACL report.
        if any(message.startswith("VIOLATION_") for message in messages):
            outcome = ValidationOutcome.NON_CONFORMING
        elif any(message.startswith("MISSING_") for message in messages):
            outcome = ValidationOutcome.INSUFFICIENT_DATA
        elif str(SH.MinCountConstraintComponent) in components:
            outcome = ValidationOutcome.INSUFFICIENT_DATA
        elif out_of_scope:
            outcome = ValidationOutcome.NOT_EVALUATED
        else:
            outcome = ValidationOutcome.NON_CONFORMING
        return ValidationResult(
            outcome,
            messages,
            components,
            focus_nodes,
            applicability,
        )
    except Exception as exc:
        return ValidationResult(
            ValidationOutcome.EXECUTION_ERROR,
            (f"{type(exc).__name__}: {exc}",),
        )


def causal_commitment(data: rdflib.Graph, candidate: rdflib.URIRef) -> CausalCommitment:
    has_trace = False
    for path in data.objects(candidate, RES.hasTracePath):
        origins = set(data.objects(path, RES.hasDeclaredOriginInteraction))
        traces = set(data.objects(path, RES.hasTraceContinuation))
        has_trace = has_trace or bool(traces)
        for trace in traces:
            if any((trace, RES.causallyAttributedTo, origin) in data for origin in origins):
                return CausalCommitment.EXPLICIT_ONTIC_RELATION
    # hasTraceContinuation has range TraceContinuation in the core. TraceContinuation in turn carries
    # an existential causallyAttributedTo.Interaction restriction, whether or not a named triple exists.
    if has_trace or any(data.subjects(rdflib.RDF.type, RES.TraceContinuation)):
        return CausalCommitment.EXISTENTIAL_COMMITMENT_ONLY
    return CausalCommitment.NONE_IDENTIFIED


def activated_dimensions(
    data: rdflib.Graph, candidate: rdflib.URIRef
) -> dict[str, bool]:
    has_claim = (
        any(data.subjects(rdflib.RDF.type, EXP.CausalAttributionClaim))
        or any(data.subjects(EXP.causalSubject, None))
    )
    return {
        "current": True,
        "lineage": any(data.objects(candidate, RES.hasTracePath)),
        "temporal": any(data.objects(None, RES.hasPostInteractionContinuation)),
        "scope": (
            any(data.subjects(RES.assesses, candidate))
            or any(data.subjects(rdflib.RDF.type, RES.ResonatusAssessment))
        ),
        "claim_record": has_claim,
        "ontic_linkage": has_claim,
        "evidence_record": has_claim,
    }


def evaluate_case(
    data: rdflib.Graph,
    shapes: dict[str, rdflib.Graph],
) -> tuple[Actual, dict[str, ValidationResult]]:
    candidate = one_candidate(data)
    activated = activated_dimensions(data, candidate)
    results = {
        name: validation_result(data, graph, activated=activated[name])
        for name, graph in shapes.items()
    }
    actual = Actual(
        owl_outcome(data, candidate),
        results["current"].outcome,
        results["lineage"].outcome,
        results["temporal"].outcome,
        results["scope"].outcome,
        results["claim_record"].outcome,
        results["ontic_linkage"].outcome,
        results["evidence_record"].outcome,
        (
            DomainEvidenceOutcome.UNASSESSED
            if activated["claim_record"]
            else DomainEvidenceOutcome.NOT_EVALUATED
        ),
        causal_commitment(data, candidate),
    )
    return actual, results


def short(value: ValidationOutcome) -> str:
    return {
        ValidationOutcome.CONFORMING: "CONFORM",
        ValidationOutcome.NON_CONFORMING: "NONCONF",
        ValidationOutcome.INSUFFICIENT_DATA: "INSUFF",
        ValidationOutcome.NOT_EVALUATED: "NOT_EVAL",
        ValidationOutcome.EXECUTION_ERROR: "ERROR",
    }[value]


def main() -> int:
    shapes = profile_shapes()
    passed = 0
    actuals: dict[str, Actual] = {}
    print(
        "CASE                              OWL_OUTCOME       CURRENT   LINEAGE   "
        "TEMPORAL  SCOPE     CLAIM_REC LINKAGE   EVID_REC  CAUSAL_COMMITMENT"
    )
    print("-" * 153)
    for case in CASES:
        data = parse_union(case.files)
        actual, results = evaluate_case(data, shapes)
        actuals[case.case_id] = actual
        expected_actual = Actual(
            case.expected.owl,
            case.expected.current,
            case.expected.lineage,
            case.expected.temporal,
            case.expected.scope,
            case.expected.claim_record,
            case.expected.ontic_linkage,
            case.expected.evidence_record,
            case.expected.domain_evidence,
            case.expected.causal_commitment,
        )
        ok = actual == expected_actual
        passed += int(ok)
        print(
            f"[{'PASS' if ok else 'FAIL'}] {case.case_id:28s} {actual.owl.value:17s} "
            f"{short(actual.current):9s} {short(actual.lineage):9s} "
            f"{short(actual.temporal):9s} {short(actual.scope):9s} "
            f"{short(actual.claim_record):9s} {short(actual.ontic_linkage):9s} "
            f"{short(actual.evidence_record):9s} {actual.causal_commitment.value}"
        )
        for dimension in (
            "current",
            "lineage",
            "temporal",
            "scope",
            "claim_record",
            "ontic_linkage",
            "evidence_record",
        ):
            result = results[dimension]
            if result.messages:
                print(
                    f"       {dimension.upper()} [{result.applicability.value}]: "
                    + (" | ".join(result.messages) or "no result message")
                )
        if actual.domain_evidence is DomainEvidenceOutcome.UNASSESSED:
            print("       DOMAIN_EVIDENCE: DOMAIN_EVIDENCE_UNASSESSED")

    critical_ok = (
        actuals["CE01_GROUPED_NO_LINEAGE"].lineage is not ValidationOutcome.CONFORMING
        and actuals["CE02_SINGLE_NODE_COLLAPSE"].lineage is not ValidationOutcome.CONFORMING
        and actuals["B_VALID_PROCESS_PATH"].lineage is ValidationOutcome.CONFORMING
        and actuals["B_VALID_PROCESS_PATH"].temporal is ValidationOutcome.CONFORMING
        and actuals["C_VALID_SEPARATE_SCOPE"].scope is ValidationOutcome.CONFORMING
        and actuals["CLAIM_WITHOUT_ONTIC_CAUSATION"].claim_record
        is ValidationOutcome.CONFORMING
        and actuals["CLAIM_WITHOUT_ONTIC_CAUSATION"].ontic_linkage
        is ValidationOutcome.INSUFFICIENT_DATA
    )
    all_ok = passed == len(CASES) and critical_ok
    print(
        f"\nSUMMARY: cases={passed}/{len(CASES)}; "
        f"critical_acceptance={'PASS' if critical_ok else 'FAIL'}; "
        f"scientific_conclusion=UNDETERMINED; overall={'PASS' if all_ok else 'FAIL'}"
    )
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
