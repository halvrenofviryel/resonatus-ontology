#!/usr/bin/env python3
"""Compare the RC temporal profile on pinned pySHACL and Apache Jena SHACL."""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from importlib.metadata import version as package_version
from pathlib import Path

import rdflib

from rc_common import RC, candidate_shapes, parse_candidate, prototype


EX = rdflib.Namespace("https://example.org/resonatus/prototype/")
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
TIME = rdflib.Namespace("http://www.w3.org/2006/time#")
XSD = rdflib.Namespace("http://www.w3.org/2001/XMLSchema#")


@dataclass(frozen=True)
class Case:
    case_id: str
    expected: prototype.ValidationOutcome
    mutate: Callable[[rdflib.Graph], None]


def no_change(_: rdflib.Graph) -> None:
    return None


def replace_timestamp(graph: rdflib.Graph, instant: rdflib.URIRef, lexical: str) -> None:
    graph.remove((instant, TIME.inXSDDateTimeStamp, None))
    graph.add(
        (
            instant,
            TIME.inXSDDateTimeStamp,
            rdflib.Literal(lexical, datatype=XSD.dateTimeStamp),
        )
    )


def boundary_equal(graph: rdflib.Graph) -> None:
    replace_timestamp(graph, EX.delayEnd, "2026-01-01T11:00:00Z")


def end_before_begin(graph: rdflib.Graph) -> None:
    replace_timestamp(graph, EX.delayEnd, "2026-01-01T10:00:00Z")


def date_rollover(graph: rdflib.Graph) -> None:
    replace_timestamp(graph, EX.delayBegin, "2026-01-01T23:59:59Z")
    replace_timestamp(graph, EX.delayEnd, "2026-01-02T00:00:01Z")


def utc_offset(graph: rdflib.Graph) -> None:
    replace_timestamp(graph, EX.delayEnd, "2026-01-01T12:00:00+00:00")


def fractional_seconds(graph: rdflib.Graph) -> None:
    replace_timestamp(graph, EX.delayEnd, "2026-01-01T12:00:00.000Z")


def missing_delay_end(graph: rdflib.Graph) -> None:
    graph.remove((EX.delayEnd, TIME.inXSDDateTimeStamp, None))


def unrelated_path(graph: rdflib.Graph) -> None:
    overlay = parse_candidate("fixtures/negative-unrelated-delay-overlay.ttl")
    for triple in overlay:
        graph.add(triple)


CASES = (
    Case("VALID_OVERLAPPING_INTERVAL", prototype.ValidationOutcome.CONFORMING, no_change),
    Case("VALID_DATE_ROLLOVER", prototype.ValidationOutcome.CONFORMING, date_rollover),
    Case("BOUNDARY_EQUAL", prototype.ValidationOutcome.NON_CONFORMING, boundary_equal),
    Case("END_BEFORE_BEGIN", prototype.ValidationOutcome.NON_CONFORMING, end_before_begin),
    Case("UTC_OFFSET_REJECTED", prototype.ValidationOutcome.NON_CONFORMING, utc_offset),
    Case("FRACTIONAL_SECONDS_REJECTED", prototype.ValidationOutcome.NON_CONFORMING, fractional_seconds),
    Case("MISSING_DELAY_END", prototype.ValidationOutcome.INSUFFICIENT_DATA, missing_delay_end),
    Case("UNRELATED_PATH", prototype.ValidationOutcome.NON_CONFORMING, unrelated_path),
)


def clone_graph(source: rdflib.Graph) -> rdflib.Graph:
    result = rdflib.Graph()
    for triple in source:
        result.add(triple)
    return result


def classify_report(report: rdflib.Graph) -> prototype.ValidationOutcome:
    conforms_values = tuple(report.objects(None, SH.conforms))
    if any(bool(value.toPython()) for value in conforms_values):
        return prototype.ValidationOutcome.CONFORMING
    results = tuple(report.objects(None, SH.result))
    messages = tuple(
        str(message)
        for result in results
        for message in report.objects(result, SH.resultMessage)
    )
    components = {
        str(component)
        for result in results
        for component in report.objects(result, SH.sourceConstraintComponent)
    }
    if any(message.startswith("VIOLATION_") for message in messages):
        return prototype.ValidationOutcome.NON_CONFORMING
    if any(message.startswith("MISSING_") for message in messages):
        return prototype.ValidationOutcome.INSUFFICIENT_DATA
    if str(SH.MinCountConstraintComponent) in components:
        return prototype.ValidationOutcome.INSUFFICIENT_DATA
    if any(message.startswith("OUT_OF_SCOPE_") for message in messages):
        return prototype.ValidationOutcome.NOT_EVALUATED
    return prototype.ValidationOutcome.NON_CONFORMING


def jena_result(
    executable: Path,
    graph: rdflib.Graph,
    shapes_path: Path,
) -> tuple[prototype.ValidationOutcome, str]:
    with tempfile.TemporaryDirectory(prefix="resonatus-jena-") as directory:
        data_path = Path(directory) / "data.ttl"
        graph.serialize(destination=data_path, format="turtle")
        completed = subprocess.run(
            [
                str(executable),
                "validate",
                "--shapes",
                str(shapes_path),
                "--data",
                str(data_path),
            ],
            cwd=RC.parents[1],
            capture_output=True,
            text=True,
            check=False,
        )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        return prototype.ValidationOutcome.EXECUTION_ERROR, detail
    try:
        report = rdflib.Graph().parse(data=completed.stdout, format="turtle")
        return classify_report(report), ""
    except Exception as exc:
        return prototype.ValidationOutcome.EXECUTION_ERROR, f"{type(exc).__name__}: {exc}"


def resolve_executable(argument: str | None) -> Path | None:
    value = argument or os.environ.get("JENA_SHACL") or shutil.which("shacl")
    if not value:
        return None
    path = Path(value).expanduser().resolve()
    return path if path.is_file() else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jena-shacl", help="path to the Apache Jena shacl command")
    args = parser.parse_args()
    executable = resolve_executable(args.jena_shacl)
    if executable is None:
        print("[NOT_RUN] Apache Jena SHACL executable not found; use --jena-shacl or JENA_SHACL")
        return 2

    version_result = subprocess.run(
        [str(executable), "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    version_text = (version_result.stdout or version_result.stderr).strip()
    print(f"ENGINE_JENA: {version_text}")
    print(
        f"ENGINE_PYSHACL: pySHACL {package_version('pyshacl')} / "
        f"RDFLib {package_version('rdflib')}"
    )

    shapes = candidate_shapes()["temporal"]
    shapes_path = RC / "shapes/temporal-delay.shacl.ttl"
    base = parse_candidate("fixtures/b-valid-process-path.ttl")
    passed = 0

    for case in CASES:
        graph = clone_graph(base)
        case.mutate(graph)
        py_result = prototype.validation_result(graph, shapes).outcome
        jena_outcome, detail = jena_result(executable, graph, shapes_path)
        ok = py_result is case.expected and jena_outcome is case.expected
        print(
            f"[{'PASS' if ok else 'FAIL'}] {case.case_id:<31} "
            f"expected={case.expected.value:<18} pyshacl={py_result.value:<18} "
            f"jena={jena_outcome.value}"
        )
        if detail:
            print(f"       {detail}")
        passed += int(ok)

    overall = passed == len(CASES)
    print(
        f"\nSUMMARY: temporal_portability={passed}/{len(CASES)}; "
        f"engines=2; overall={'PASS' if overall else 'FAIL'}"
    )
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
