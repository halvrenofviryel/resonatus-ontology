#!/usr/bin/env python3
"""Static and executable integrity gates for the local RC package."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import rdflib

from rc_common import RC, ROOT, STRICT, candidate_shapes, parse_candidate, prototype

OWL = rdflib.OWL
RES = prototype.RES
EX = rdflib.Namespace("https://example.org/resonatus/prototype/")
OLD_BASE = "https://w3id.org/resonatus/experimental/v1.1#"
VERSION_IRI = rdflib.URIRef("https://w3id.org/resonatus/strict/1.1.0-rc.1")
LINEAR_PROFILE = rdflib.URIRef(
    "https://w3id.org/resonatus/strict/profile/strict-linear/1.1.0-rc.1"
)
ASSESSMENT_PROFILE = rdflib.URIRef(
    "https://w3id.org/resonatus/strict/profile/strict-assessment/1.1.0-rc.1"
)


def report(checks: list[tuple[str, bool]], name: str, ok: bool) -> None:
    checks.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")


def expected_result(
    checks: list[tuple[str, bool]],
    name: str,
    graph: rdflib.Graph,
    shape_key: str,
    outcome: prototype.ValidationOutcome,
    applicability: prototype.ProfileApplicability = prototype.ProfileApplicability.IN_SCOPE,
) -> None:
    result = prototype.validation_result(graph, candidate_shapes()[shape_key])
    report(
        checks,
        name,
        result.outcome is outcome and result.applicability is applicability,
    )
    if result.outcome is not outcome or result.applicability is not applicability:
        print(f"       actual={result.outcome.value}/{result.applicability.value}")
        print("       findings=" + " | ".join(result.messages))


def main() -> int:
    checks: list[tuple[str, bool]] = []
    required = (
        "README.md",
        "RELEASE_CANDIDATE_MANIFEST.md",
        "CONFORMANCE_CONTRACT.md",
        "MIGRATION_GUIDE.md",
        "VERIFICATION_REPORT.md",
        "ontology/resonatus-strict-vocabulary.ttl",
        "profile-activation.ttl",
        "shapes/strict-linear.shacl.ttl",
        "shapes/temporal-delay.shacl.ttl",
        "shapes/assessment-scope.shacl.ttl",
        "shapes/claim-record.shacl.ttl",
        "shapes/ontic-linkage.shacl.ttl",
        "shapes/evidence-record.shacl.ttl",
        "schemas/validation-result.schema.json",
        "schemas/example-validation-result.json",
        "CHECKSUMS.sha256",
    )
    report(checks, "required candidate artefacts present", all((RC / item).is_file() for item in required))

    ttl_files = sorted(RC.rglob("*.ttl"))
    parsed: dict[Path, rdflib.Graph] = {}
    try:
        for path in ttl_files:
            parsed[path] = rdflib.Graph().parse(path, format="turtle")
        ttl_ok = True
    except Exception as exc:
        ttl_ok = False
        print(f"       parse error: {exc}")
    report(checks, f"candidate Turtle parses ({len(ttl_files)} files)", ttl_ok)

    no_old_iris = ttl_ok and all(
        OLD_BASE not in str(term)
        for graph in parsed.values()
        for triple in graph
        for term in triple
    )
    report(checks, "no experimental namespace remains in RDF artefacts", no_old_iris)

    vocab = parsed.get(RC / "ontology/resonatus-strict-vocabulary.ttl", rdflib.Graph())
    ontology_iri = rdflib.URIRef("https://w3id.org/resonatus/strict")
    report(
        checks,
        "candidate ontology and version identifiers",
        (ontology_iri, rdflib.RDF.type, OWL.Ontology) in vocab
        and (ontology_iri, OWL.versionIRI, VERSION_IRI) in vocab,
    )
    required_terms = (
        STRICT.AssessmentScope,
        STRICT.CausalAttributionClaim,
        STRICT.hasCausalSegment,
        STRICT.hasCausalNextStage,
        STRICT.temporallyQualifiesPath,
        STRICT.hasAssessmentScope,
        STRICT.scopesProcess,
        STRICT.causalSubject,
        STRICT.causalObject,
        STRICT.usesCausalAssessmentMethod,
    )
    report(
        checks,
        "only demonstrated strict terms are declared",
        all(any(vocab.triples((term, rdflib.RDF.type, None))) for term in required_terms)
        and len({subject for subject in vocab.subjects(rdflib.RDF.type, OWL.Class)}) == 2
        and len({subject for subject in vocab.subjects(rdflib.RDF.type, OWL.ObjectProperty)}) == 8,
    )
    disjoint_pairs = {
        (subject, obj)
        for subject, obj in vocab.subject_objects(OWL.disjointWith)
    }
    report(
        checks,
        "global class disjointness limited to scope versus path",
        disjoint_pairs == {(STRICT.AssessmentScope, RES.ContinuationPath)},
    )

    activation = parsed.get(RC / "profile-activation.ttl", rdflib.Graph())
    report(
        checks,
        "Strict Linear and Strict Assessment activation identifiers",
        (LINEAR_PROFILE, rdflib.RDF.type, rdflib.URIRef("http://www.w3.org/ns/prov#Plan")) in activation
        and (ASSESSMENT_PROFILE, rdflib.RDF.type, rdflib.URIRef("http://www.w3.org/ns/prov#Plan")) in activation,
    )

    core = rdflib.Graph().parse(ROOT / "ontology/resonatus.ttl", format="turtle")
    report(
        checks,
        "published core neither imports nor references strict module",
        not any(str(term).startswith(str(STRICT)) for triple in core for term in triple)
        and not any(str(obj).startswith("https://w3id.org/resonatus/strict") for obj in core.objects(None, OWL.imports)),
    )

    temporal_text = (RC / "shapes/temporal-delay.shacl.ttl").read_text(encoding="utf-8")
    report(
        checks,
        "UTC-second normalization and value-based comparison",
        "xsd:dateTime(STR(?delayEnd))" in temporal_text
        and "STR(?delayEnd) <= STR(?delayBegin)" not in temporal_text
        and temporal_text.count("T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$") == 3,
    )

    base = parse_candidate("fixtures/b-valid-process-path.ttl")
    complete = parse_candidate("fixtures/b-valid-process-path.ttl", "fixtures/c-valid-overlay.ttl")
    expected_result(checks, "valid RC lineage", base, "lineage", prototype.ValidationOutcome.CONFORMING)
    expected_result(checks, "valid RC temporal", base, "temporal", prototype.ValidationOutcome.CONFORMING)
    expected_result(checks, "valid RC assessment scope", complete, "scope", prototype.ValidationOutcome.CONFORMING)
    expected_result(checks, "valid RC claim record", complete, "claim_record", prototype.ValidationOutcome.CONFORMING)
    expected_result(checks, "valid RC ontic linkage", complete, "ontic_linkage", prototype.ValidationOutcome.CONFORMING)
    expected_result(checks, "valid RC evidence record", complete, "evidence_record", prototype.ValidationOutcome.CONFORMING)

    reversed_graph = parse_candidate("fixtures/b-valid-process-path.ttl", "fixtures/negative-reversed-edge-overlay.ttl")
    unrelated_delay = parse_candidate("fixtures/b-valid-process-path.ttl", "fixtures/negative-unrelated-delay-overlay.ttl")
    branch = parse_candidate("fixtures/b-valid-process-path.ttl", "fixtures/out-of-scope-branch-overlay.ttl")
    collapsed = parse_candidate("fixtures/b-valid-process-path.ttl", "fixtures/c-invalid-scope-is-process-overlay.ttl")
    expected_result(checks, "reversed edge rejected", reversed_graph, "lineage", prototype.ValidationOutcome.NON_CONFORMING)
    expected_result(checks, "unrelated Delay rejected", unrelated_delay, "temporal", prototype.ValidationOutcome.NON_CONFORMING)
    expected_result(
        checks,
        "branch reported out of scope",
        branch,
        "lineage",
        prototype.ValidationOutcome.NOT_EVALUATED,
        prototype.ProfileApplicability.OUT_OF_SCOPE,
    )
    expected_result(checks, "scope/path collapse rejected", collapsed, "scope", prototype.ValidationOutcome.NON_CONFORMING)

    claim_only = parse_candidate("fixtures/claim-only-no-ontic-causation.ttl")
    expected_result(checks, "claim-only record valid", claim_only, "claim_record", prototype.ValidationOutcome.CONFORMING)
    expected_result(checks, "claim-only ontic link insufficient", claim_only, "ontic_linkage", prototype.ValidationOutcome.INSUFFICIENT_DATA)
    expected_result(checks, "claim-only evidence record valid", claim_only, "evidence_record", prototype.ValidationOutcome.CONFORMING)

    schema = json.loads((RC / "schemas/validation-result.schema.json").read_text(encoding="utf-8"))
    sample = json.loads((RC / "schemas/example-validation-result.json").read_text(encoding="utf-8"))
    enum_values = set(schema["$defs"]["validationOutcome"]["enum"])
    sample_ok = (
        set(schema["required"]).issubset(sample)
        and set(sample["dimensions"]) == set(schema["properties"]["dimensions"]["required"])
        and all(value in enum_values for value in sample["dimensions"].values())
        and sample["candidateVersion"] == "1.1.0-rc.1"
    )
    report(checks, "machine-readable result schema and sample", sample_ok)

    checksum_path = RC / "CHECKSUMS.sha256"
    checksum_ok = checksum_path.is_file()
    checksum_entries: set[str] = set()
    if checksum_ok:
        for line in checksum_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            expected, relative = line.split("  ", 1)
            checksum_entries.add(relative)
            target = RC / relative
            actual = hashlib.sha256(target.read_bytes()).hexdigest() if target.is_file() else "MISSING"
            checksum_ok = checksum_ok and actual == expected
        package_files = {
            path.relative_to(RC).as_posix()
            for path in RC.rglob("*")
            if path.is_file() and path != checksum_path
        }
        checksum_ok = checksum_ok and checksum_entries == package_files
    report(checks, "candidate artefact checksums", checksum_ok)

    print("[KNOWN_BLOCKER] live w3id.org check is outside this offline runner; HTTP 404 observed 2026-10-11")
    print("[NOT_RUN] cross-engine SHACL temporal portability (only pinned pySHACL/RDFLib available)")
    passed = sum(ok for _, ok in checks)
    print(f"\nSUMMARY: rc_package_checks={passed}/{len(checks)}; overall={'PASS' if all(ok for _, ok in checks) else 'FAIL'}")
    return 0 if all(ok for _, ok in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
