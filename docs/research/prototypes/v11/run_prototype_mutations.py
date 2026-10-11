#!/usr/bin/env python3
"""Mutation gates for the Resonatus v1.1 experimental strict profile.

Each mutation changes one relevant fact in a known-positive graph. The test passes only when the
computed result changes for the intended constraint and reason. This guards against unused shapes,
vacuous target selection, and accidental coupling to the expected-result table in run_prototypes.py.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import rdflib
from owlready2 import World, sync_reasoner_hermit
from rdflib.collection import Collection

from run_prototypes import (
    CORE,
    EXP,
    FIX,
    RES,
    SH,
    CausalCommitment,
    OwlOutcome,
    ProfileApplicability,
    ValidationOutcome,
    causal_commitment,
    one_candidate,
    owl_outcome,
    parse_union,
    profile_shapes,
    validation_result,
)

EX = rdflib.Namespace("https://example.org/resonatus/prototype/")
TIME = rdflib.Namespace("http://www.w3.org/2006/time#")
XSD = rdflib.Namespace("http://www.w3.org/2001/XMLSchema#")
EXPERIMENTAL_VOCAB = FIX.parent / "experimental-vocabulary.ttl"


def clone(graph: rdflib.Graph) -> rdflib.Graph:
    result = rdflib.Graph()
    for triple in graph:
        result.add(triple)
    return result


def require(
    test_id: str,
    graph: rdflib.Graph,
    shapes: rdflib.Graph,
    expected: ValidationOutcome,
    message_prefix: str | tuple[str, ...] | None = None,
    expected_applicability: ProfileApplicability = ProfileApplicability.IN_SCOPE,
) -> bool:
    result = validation_result(graph, shapes)
    prefixes = (
        ()
        if message_prefix is None
        else (message_prefix,) if isinstance(message_prefix, str) else message_prefix
    )
    message_ok = all(
        any(message.startswith(prefix) for message in result.messages)
        for prefix in prefixes
    )
    ok = (
        result.outcome is expected
        and result.applicability is expected_applicability
        and message_ok
        and (
        expected is ValidationOutcome.CONFORMING or bool(result.focus_nodes)
        or expected is ValidationOutcome.EXECUTION_ERROR
        )
    )
    print(
        f"[{'PASS' if ok else 'FAIL'}] {test_id:38s} "
        f"actual={result.outcome.value:18s} applicability={result.applicability.value:12s} "
        f"expected={expected.value}"
    )
    if not ok:
        print("       messages:", " | ".join(result.messages) or "NONE")
        print("       focus_nodes:", ", ".join(result.focus_nodes) or "NONE")
    return ok


def inferred_types_with_experimental(
    graph: rdflib.Graph, individual_iri: rdflib.URIRef
) -> set[str]:
    merged = rdflib.Graph()
    merged.parse(CORE, format="turtle")
    merged.parse(EXPERIMENTAL_VOCAB, format="turtle")
    for triple in graph:
        merged.add(triple)
    with tempfile.TemporaryDirectory(prefix="resonatus-v11-claim-range-") as tmp:
        path = Path(tmp) / "merged.owl"
        merged.serialize(destination=path, format="xml")
        world = World()
        world.get_ontology(path.as_uri()).load()
        sync_reasoner_hermit(world, infer_property_values=True, debug=0)
        individual = world.search_one(iri=str(individual_iri))
        if individual is None:
            return set()
        return {
            str(getattr(cls, "iri", ""))
            for cls in individual.INDIRECT_is_a
        }


def main() -> int:
    shapes = profile_shapes()
    base = parse_union((FIX / "b-valid-process-path.ttl",))
    complete = parse_union(
        (FIX / "b-valid-process-path.ttl", FIX / "c-valid-overlay.ttl")
    )
    checks: list[bool] = []

    no_path_type = clone(base)
    no_path_type.remove((EX.path, rdflib.RDF.type, RES.ContinuationPath))
    checks.append(
        require(
            "M01 property-targeted path",
            no_path_type,
            shapes["lineage"],
            ValidationOutcome.CONFORMING,
        )
    )

    no_delay_type = clone(base)
    no_delay_type.remove((EX.delay, rdflib.RDF.type, RES.PostInteractionContinuation))
    checks.append(
        require(
            "M02 property-targeted Delay",
            no_delay_type,
            shapes["temporal"],
            ValidationOutcome.CONFORMING,
        )
    )

    missing_edge = clone(base)
    missing_edge.remove((EX.origin, EXP.causallyPrecedes, EX.trace))
    checks.append(
        require(
            "M03 removed causal edge",
            missing_edge,
            shapes["lineage"],
            ValidationOutcome.INSUFFICIENT_DATA,
            "MISSING_LINEAGE_DIRECTION",
        )
    )

    missing_segment = clone(base)
    missing_segment.remove((EX.path, EXP.hasCausalSegment, EX.trace))
    checks.append(
        require(
            "M04 removed segment membership",
            missing_segment,
            shapes["lineage"],
            ValidationOutcome.INSUFFICIENT_DATA,
            "MISSING_LINEAGE_MEMBERSHIP",
        )
    )

    reverse_edge = clone(base)
    reverse_edge.add((EX.trace, EXP.causallyPrecedes, EX.origin))
    checks.append(
        require(
            "M05 added reverse causal edge",
            reverse_edge,
            shapes["lineage"],
            ValidationOutcome.NON_CONFORMING,
            "VIOLATION_LINEAGE_DIRECTION_REVERSED",
        )
    )

    missing_outcome_link = clone(base)
    missing_outcome_link.remove((EX.selectivity, EXP.causallyPrecedes, EX.transformation))
    checks.append(
        require(
            "M06 detached Transformation",
            missing_outcome_link,
            shapes["lineage"],
            ValidationOutcome.INSUFFICIENT_DATA,
            "MISSING_LINEAGE_DIRECTION",
        )
    )

    branch = clone(base)
    branch.add((EX.origin, EXP.causallyPrecedes, EX.propagation))
    checks.append(
        require(
            "M07 branch is out of scope",
            branch,
            shapes["lineage"],
            ValidationOutcome.NOT_EVALUATED,
            "OUT_OF_SCOPE_BRANCH_MERGE",
            ProfileApplicability.OUT_OF_SCOPE,
        )
    )

    collapsed_scope = clone(complete)
    collapsed_scope.remove((EX.assessment, EXP.hasAssessmentScope, EX.scope))
    collapsed_scope.add((EX.assessment, EXP.hasAssessmentScope, EX.path))
    collapsed_scope.add((EX.path, rdflib.RDF.type, EXP.AssessmentScope))
    collapsed_scope.add((EX.path, EXP.scopesProcess, EX.path))
    checks.append(
        require(
            "M08 collapsed scope/process",
            collapsed_scope,
            shapes["scope"],
            ValidationOutcome.NON_CONFORMING,
            "VIOLATION_SCOPE_",
        )
    )

    no_evidence = clone(complete)
    no_evidence.remove((EX.claim, RES.supportedBy, EX.causalEvidence))
    checks.append(
        require(
            "M09 removed evidence record",
            no_evidence,
            shapes["evidence_record"],
            ValidationOutcome.INSUFFICIENT_DATA,
            "MISSING_EVIDENCE_RECORD",
        )
    )

    malformed_shapes = rdflib.Graph()
    malformed_shapes.parse(
        data="""
          @prefix ex: <https://example.org/broken/> .
          @prefix sh: <http://www.w3.org/ns/shacl#> .
          ex:Broken a sh:NodeShape ; sh:targetNode ex:x ;
            sh:sparql [ sh:select "SELECT ???" ] .
        """,
        format="turtle",
    )
    checks.append(
        require(
            "M10 engine error is explicit",
            base,
            malformed_shapes,
            ValidationOutcome.EXECUTION_ERROR,
        )
    )

    inconsistent = clone(base)
    inconsistent.add((EX.path, RES.hasDeclaredOriginInteraction, EX.otherOrigin))
    inconsistent.add((EX.otherOrigin, rdflib.RDF.type, RES.Interaction))
    all_different = rdflib.BNode()
    members = rdflib.BNode()
    inconsistent.add((all_different, rdflib.RDF.type, rdflib.OWL.AllDifferent))
    inconsistent.add((all_different, rdflib.OWL.distinctMembers, members))
    Collection(inconsistent, members, [EX.origin, EX.otherOrigin])
    checks.append(
        require(
            "M11a extra-origin cardinality",
            inconsistent,
            shapes["lineage"],
            ValidationOutcome.NON_CONFORMING,
            "VIOLATION_LINEAGE_CARDINALITY",
        )
    )
    candidate = one_candidate(inconsistent)
    owl = owl_outcome(inconsistent, candidate)
    owl_ok = owl is OwlOutcome.INCONSISTENT
    checks.append(owl_ok)
    print(
        f"[{'PASS' if owl_ok else 'FAIL'}] M11b inconsistency is not non-membership "
        f"actual={owl.value} expected={OwlOutcome.INCONSISTENT.value}"
    )

    claim_only = parse_union((FIX / "claim-only-no-ontic-causation.ttl",))
    commitment = causal_commitment(claim_only, one_candidate(claim_only))
    no_named_triple = not any(
        claim_only.triples((None, RES.causallyAttributedTo, None))
    )
    commitment_ok = (
        commitment is CausalCommitment.EXISTENTIAL_COMMITMENT_ONLY
        and no_named_triple
    )
    checks.append(commitment_ok)
    print(
        f"[{'PASS' if commitment_ok else 'FAIL'}] "
        "M12 existential commitment is not a named triple "
        f"actual={commitment.value} named_triple={not no_named_triple}"
    )

    isolated_claim = rdflib.Graph()
    isolated_claim.add((EX.isolatedClaim, rdflib.RDF.type, EXP.CausalAttributionClaim))
    isolated_claim.add((EX.isolatedClaim, EXP.causalSubject, EX.isolatedSubject))
    isolated_claim.add((EX.isolatedClaim, EXP.causalObject, EX.isolatedObject))
    subject_types = inferred_types_with_experimental(isolated_claim, EX.isolatedSubject)
    object_types = inferred_types_with_experimental(isolated_claim, EX.isolatedObject)
    range_ok = (
        str(RES.TraceContinuation) not in subject_types
        and str(RES.Interaction) not in object_types
    )
    checks.append(range_ok)
    print(
        f"[{'PASS' if range_ok else 'FAIL'}] "
        "M13 claim properties do not infer ontic relata "
        f"subject_trace={str(RES.TraceContinuation) in subject_types} "
        f"object_interaction={str(RES.Interaction) in object_types}"
    )

    overlapping = clone(base)
    overlapping.add((EX.trace, RES.hasTemporalExtent, EX.traceInterval))
    overlapping.add((EX.traceInterval, rdflib.RDF.type, TIME.ProperInterval))
    overlapping.add((EX.traceInterval, TIME.hasBeginning, EX.traceBegin))
    overlapping.add((EX.traceInterval, TIME.hasEnd, EX.traceEnd))
    overlapping.add((EX.traceBegin, rdflib.RDF.type, TIME.Instant))
    overlapping.add(
        (
            EX.traceBegin,
            TIME.inXSDDateTimeStamp,
            rdflib.Literal("2026-01-01T10:45:00Z", datatype=XSD.dateTimeStamp),
        )
    )
    overlapping.add((EX.traceEnd, rdflib.RDF.type, TIME.Instant))
    overlapping.add(
        (
            EX.traceEnd,
            TIME.inXSDDateTimeStamp,
            rdflib.Literal("2026-01-01T11:30:00Z", datatype=XSD.dateTimeStamp),
        )
    )
    checks.append(
        require(
            "M14 overlapping causal processes",
            overlapping,
            shapes["lineage"],
            ValidationOutcome.CONFORMING,
        )
    )

    out_plus_violation = clone(base)
    out_plus_violation.add((EX.origin, EXP.causallyPrecedes, EX.propagation))
    out_plus_violation.add((EX.trace, EXP.causallyPrecedes, EX.origin))
    checks.append(
        require(
            "M15 out-of-scope plus violation",
            out_plus_violation,
            shapes["lineage"],
            ValidationOutcome.NON_CONFORMING,
            ("OUT_OF_SCOPE_", "VIOLATION_"),
            ProfileApplicability.OUT_OF_SCOPE,
        )
    )

    out_plus_missing = clone(base)
    out_plus_missing.add((EX.trace, EXP.causallyPrecedes, EX.selectivity))
    out_plus_missing.remove((EX.path, EXP.hasCausalSegment, EX.transformation))
    checks.append(
        require(
            "M16 out-of-scope plus missing",
            out_plus_missing,
            shapes["lineage"],
            ValidationOutcome.INSUFFICIENT_DATA,
            ("OUT_OF_SCOPE_", "MISSING_"),
            ProfileApplicability.OUT_OF_SCOPE,
        )
    )

    violation_plus_missing = clone(base)
    violation_plus_missing.remove((EX.origin, EXP.causallyPrecedes, EX.trace))
    violation_plus_missing.add((EX.trace, EXP.causallyPrecedes, EX.origin))
    checks.append(
        require(
            "M17 violation plus missing",
            violation_plus_missing,
            shapes["lineage"],
            ValidationOutcome.NON_CONFORMING,
            ("VIOLATION_", "MISSING_"),
        )
    )

    # Reconstruct the pre-gate temporal profile by removing only the newly introduced Delay-to-path
    # constraints. The unrelated-Delay fixture then demonstrates the original semantic gap directly.
    pre_gate_temporal = clone(shapes["temporal"])
    for constraint, message in tuple(pre_gate_temporal.subject_objects(SH.message)):
        if str(message).startswith(("MISSING_TEMPORAL_LINEAGE_", "VIOLATION_TEMPORAL_LINEAGE_")):
            pre_gate_temporal.remove((None, None, constraint))
            pre_gate_temporal.remove((constraint, None, None))
    unrelated_delay = parse_union((FIX / "b-invalid-unrelated-delay.ttl",))
    checks.append(
        require(
            "M18a pre-gate Delay gap",
            unrelated_delay,
            pre_gate_temporal,
            ValidationOutcome.CONFORMING,
        )
    )

    missing_delay_link = clone(base)
    missing_delay_link.remove((EX.delay, EXP.temporallyQualifiesPath, EX.path))
    checks.append(
        require(
            "M18b missing Delay lineage link",
            missing_delay_link,
            shapes["temporal"],
            ValidationOutcome.INSUFFICIENT_DATA,
            "MISSING_TEMPORAL_LINEAGE_LINK",
        )
    )

    wrong_delay_link = clone(base)
    wrong_delay_link.remove((EX.delay, EXP.temporallyQualifiesPath, EX.path))
    wrong_delay_link.add((EX.delay, EXP.temporallyQualifiesPath, EX.otherPath))
    checks.append(
        require(
            "M18c contradictory Delay lineage",
            wrong_delay_link,
            shapes["temporal"],
            ValidationOutcome.NON_CONFORMING,
            ("MISSING_TEMPORAL_LINEAGE_LINK", "VIOLATION_TEMPORAL_LINEAGE_MISMATCH"),
        )
    )

    claim_only_record = parse_union((FIX / "claim-only-no-ontic-causation.ttl",))
    checks.append(
        require(
            "M20a claim-only record is valid",
            claim_only_record,
            shapes["claim_record"],
            ValidationOutcome.CONFORMING,
        )
    )
    checks.append(
        require(
            "M20b claim-only linkage is missing",
            claim_only_record,
            shapes["ontic_linkage"],
            ValidationOutcome.INSUFFICIENT_DATA,
            "MISSING_ONTIC_LINKAGE",
        )
    )

    incomplete_claim = parse_union(
        (FIX / "b-valid-process-path.ttl", FIX / "claim-incomplete-record-overlay.ttl")
    )
    checks.append(
        require(
            "M21a incomplete claim record",
            incomplete_claim,
            shapes["claim_record"],
            ValidationOutcome.INSUFFICIENT_DATA,
            "MISSING_CLAIM_RECORD_DATA",
        )
    )
    checks.append(
        require(
            "M21b incomplete record linkage",
            incomplete_claim,
            shapes["ontic_linkage"],
            ValidationOutcome.CONFORMING,
        )
    )

    conflicting_claim = parse_union(
        (FIX / "b-valid-process-path.ttl", FIX / "claim-conflicting-linkage-overlay.ttl")
    )
    checks.append(
        require(
            "M22a conflicting claim record valid",
            conflicting_claim,
            shapes["claim_record"],
            ValidationOutcome.CONFORMING,
        )
    )
    checks.append(
        require(
            "M22b conflicting ontic linkage",
            conflicting_claim,
            shapes["ontic_linkage"],
            ValidationOutcome.NON_CONFORMING,
            ("MISSING_ONTIC_LINKAGE", "VIOLATION_ONTIC_LINKAGE_CONFLICT"),
        )
    )

    passed = sum(checks)
    print(f"\nSUMMARY: mutations={passed}/{len(checks)}; overall={'PASS' if all(checks) else 'FAIL'}")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
