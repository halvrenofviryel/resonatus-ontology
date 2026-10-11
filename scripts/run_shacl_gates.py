#!/usr/bin/env python3
"""Resonatus SHACL gates with expected-violation assertions.

Checking only ``conforms == False`` lets a negative fixture pass for the wrong reason. This runner
therefore verifies the exact constraint component and result path (plus the identifying message for
SPARQL constraints) expected from every negative fixture.

SHACL runs closed-world with no inference; assessment records assert their own types explicitly.
R26 separately verifies the SHACL Core targetClass rule for subclasses declared in the data graph.

Usage:  python scripts/run_shacl_gates.py
Exit:   0 = every fixture produced the expected conformance and violation report; 1 = mismatch.
"""
from __future__ import annotations

from pathlib import Path

import rdflib
from pyshacl import validate

SHAPES = "shapes/resonatus.shacl.ttl"
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
RES = rdflib.Namespace("https://w3id.org/resonatus#")

# fixture -> expected conforms
GATES = {
    "tests/shacl/valid-assessment.ttl": True,
    "tests/shacl/missing-criterion.ttl": False,
    "tests/shacl/duplicate-criterion.ttl": False,
    "tests/shacl/invalid-verdict.ttl": False,
    "tests/shacl/wrong-assessed-candidate.ttl": False,
    "tests/shacl/two-assessed-candidates.ttl": False,
    "tests/shacl/mismatched-path-scope.ttl": False,
    "tests/shacl/path-r18-origin-incoherent.ttl": False,
    "tests/shacl/path-r19-delay-incoherent.ttl": False,
    "tests/shacl/path-r20-receiver-incoherent.ttl": False,
    "tests/shacl/path-r21-fully-coherent.ttl": True,
    "tests/shacl/path-r22-origin-alias.ttl": False,
    "tests/shacl/path-r23-receiver-alias.ttl": False,
    "tests/shacl/path-r24-incomplete-refs.ttl": False,
    "tests/shacl/path-r25-assessment-missing-path.ttl": False,
    "tests/shacl/path-r26-targetclass-subclass.ttl": False,
}

# Each tuple is (sourceConstraintComponent, resultPath, identifying message fragment).
# The message fragment is used only where several SPARQL constraints share the same component and no
# resultPath. Built-in constraint messages are intentionally ignored because processors may word them
# differently while preserving standard SHACL result terms.
EXPECTED_VIOLATIONS = {
    "tests/shacl/valid-assessment.ttl": [],
    "tests/shacl/missing-criterion.ttl": [
        (SH.MinCountConstraintComponent, RES.hasCriterionAssessment, None),
        (SH.QualifiedMinCountConstraintComponent, RES.hasCriterionAssessment, None),
    ],
    "tests/shacl/duplicate-criterion.ttl": [
        (SH.QualifiedMinCountConstraintComponent, RES.hasCriterionAssessment, None),
        (SH.QualifiedMaxCountConstraintComponent, RES.hasCriterionAssessment, None),
    ],
    "tests/shacl/invalid-verdict.ttl": [
        (SH.InConstraintComponent, RES.verdict, None),
    ],
    "tests/shacl/wrong-assessed-candidate.ttl": [
        (SH.ClassConstraintComponent, RES.assesses, None),
    ],
    "tests/shacl/two-assessed-candidates.ttl": [
        (SH.MaxCountConstraintComponent, RES.assesses, None),
    ],
    "tests/shacl/mismatched-path-scope.ttl": [
        (SH.SPARQLConstraintComponent, None, "scopePath must match"),
    ],
    "tests/shacl/path-r18-origin-incoherent.ttl": [
        (SH.SPARQLConstraintComponent, None, "Origin incoherence"),
    ],
    "tests/shacl/path-r19-delay-incoherent.ttl": [
        (SH.SPARQLConstraintComponent, None, "Delay incoherence"),
    ],
    "tests/shacl/path-r20-receiver-incoherent.ttl": [
        (SH.SPARQLConstraintComponent, None, "Receiver incoherence"),
    ],
    "tests/shacl/path-r21-fully-coherent.ttl": [],
    "tests/shacl/path-r22-origin-alias.ttl": [
        (SH.SPARQLConstraintComponent, None, "Origin incoherence"),
    ],
    "tests/shacl/path-r23-receiver-alias.ttl": [
        (SH.SPARQLConstraintComponent, None, "Receiver incoherence"),
    ],
    "tests/shacl/path-r24-incomplete-refs.ttl": [
        (SH.SPARQLConstraintComponent, None, "Coherence incompleteness"),
    ],
    "tests/shacl/path-r25-assessment-missing-path.ttl": [
        (SH.MinCountConstraintComponent, RES.assessesPath, None),
    ],
    "tests/shacl/path-r26-targetclass-subclass.ttl": [
        (SH.MinCountConstraintComponent, RES.assessesPath, None),
    ],
}


def report_violations(report_graph: rdflib.Graph) -> list[tuple[object, object, str]]:
    violations = []
    for result in report_graph.objects(None, SH.result):
        component = report_graph.value(result, SH.sourceConstraintComponent)
        path = report_graph.value(result, SH.resultPath)
        message = report_graph.value(result, SH.resultMessage)
        violations.append((component, path, str(message or "")))
    return violations


def violation_matches(expected, actual) -> bool:
    component, path, message_fragment = expected
    actual_component, actual_path, actual_message = actual
    return (
        component == actual_component
        and path == actual_path
        and (message_fragment is None or message_fragment in actual_message)
    )


def compare_violations(expected, actual):
    """Return missing and unexpected violations using a one-to-one match."""
    unmatched_actual = list(actual)
    missing = []
    for expected_violation in expected:
        match_index = next(
            (
                index
                for index, actual_violation in enumerate(unmatched_actual)
                if violation_matches(expected_violation, actual_violation)
            ),
            None,
        )
        if match_index is None:
            missing.append(expected_violation)
        else:
            unmatched_actual.pop(match_index)
    return missing, unmatched_actual


def compact(violation) -> str:
    component, path, message = violation
    component_name = str(component).rsplit("#", 1)[-1] if component else "None"
    path_name = str(path).rsplit("#", 1)[-1] if path else "None"
    message_text = f", message={message!r}" if message else ""
    return f"({component_name}, path={path_name}{message_text})"


def main() -> int:
    shapes = rdflib.Graph().parse(SHAPES, format="turtle")
    all_ok = True
    for fixture, expect_conforms in GATES.items():
        # inference="none" is intentional. RDFS domain/range materialization would auto-type assessed
        # nodes and could make sh:class checks vacuous. SHACL Core targetClass subclass discovery is
        # tested independently by R26 and does not require general RDFS inference.
        data = rdflib.Graph().parse(fixture, format="turtle")
        conforms, report_graph, _ = validate(
            data_graph=data,
            shacl_graph=shapes,
            inference="none",
            advanced=True,
            debug=False,
        )
        actual = report_violations(report_graph)
        missing, unexpected = compare_violations(EXPECTED_VIOLATIONS[fixture], actual)
        good = conforms == expect_conforms and not missing and not unexpected
        all_ok = all_ok and good
        print(
            f"[{'PASS' if good else 'FAIL'}] {Path(fixture).name:40s} "
            f"conforms={conforms} expected={expect_conforms} violations={len(actual)}"
        )
        for violation in missing:
            print(f"        MISSING expected violation {compact(violation)}")
        for violation in unexpected:
            print(f"        UNEXPECTED violation {compact(violation)}")

    print(
        f"\nSUMMARY: {'ALL SHACL GATES PASS' if all_ok else 'SHACL GATE FAILURES PRESENT'}"
    )
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
