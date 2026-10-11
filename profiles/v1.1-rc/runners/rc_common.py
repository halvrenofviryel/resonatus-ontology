"""Shared adapters that execute the validated prototype gates against RC artefacts."""
from __future__ import annotations

import sys
from pathlib import Path

import rdflib

ROOT = Path(__file__).resolve().parents[3]
RC = ROOT / "profiles/v1.1-rc"
PROTOTYPE = ROOT / "docs/research/prototypes/v11"
sys.path.insert(0, str(PROTOTYPE))

import run_prototypes as prototype  # noqa: E402

OLD = rdflib.Namespace("https://w3id.org/resonatus/experimental/v1.1#")
STRICT = rdflib.Namespace("https://w3id.org/resonatus/strict#")


class StrictTermAdapter:
    """Map the prototype causal-edge local name to its owner-approved RC local name."""

    def __getattr__(self, local_name: str) -> rdflib.URIRef:
        if local_name == "causallyPrecedes":
            return STRICT.hasCausalNextStage
        return STRICT[local_name]


STRICT_TERMS = StrictTermAdapter()


def migrate_term(term: rdflib.term.Node) -> rdflib.term.Node:
    if not isinstance(term, rdflib.URIRef):
        return term
    if term == OLD.causallyPrecedes:
        return STRICT.hasCausalNextStage
    value = str(term)
    old_base = str(OLD)
    if value.startswith(old_base):
        return rdflib.URIRef(str(STRICT) + value[len(old_base):])
    return term


def migrate_graph(graph: rdflib.Graph) -> rdflib.Graph:
    migrated = rdflib.Graph()
    for subject, predicate, obj in graph:
        migrated.add((migrate_term(subject), migrate_term(predicate), migrate_term(obj)))
    return migrated


def migrated_parse_union(paths: tuple[Path, ...]) -> rdflib.Graph:
    graph = rdflib.Graph()
    for path in paths:
        graph.parse(path, format="turtle")
    return migrate_graph(graph)


def parse_candidate(*relative_paths: str) -> rdflib.Graph:
    graph = rdflib.Graph()
    for relative in relative_paths:
        graph.parse(RC / relative, format="turtle")
    return graph


def candidate_shapes() -> dict[str, rdflib.Graph]:
    return {
        "current": prototype.parse_union((ROOT / "shapes/resonatus.shacl.ttl",)),
        "lineage": parse_candidate("shapes/strict-linear.shacl.ttl"),
        "temporal": parse_candidate("shapes/temporal-delay.shacl.ttl"),
        "scope": parse_candidate("shapes/assessment-scope.shacl.ttl"),
        "claim_record": parse_candidate("shapes/claim-record.shacl.ttl"),
        "ontic_linkage": parse_candidate("shapes/ontic-linkage.shacl.ttl"),
        "evidence_record": parse_candidate("shapes/evidence-record.shacl.ttl"),
    }


def configure_prototype_module() -> None:
    prototype.EXP = STRICT
    prototype.parse_union = migrated_parse_union
    prototype.profile_shapes = candidate_shapes
