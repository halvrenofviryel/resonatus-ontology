# Resonatus v1.1.0 local final-artifact verification report

**Version:** `1.1.0`

**Date:** 2026-10-11

**Environment:** pinned Python at `/mnt/data/claude/resonatus-ontology/.venv/bin/python`

## Disposition

`GO` for preservation of the owner-approved local final `1.1.0` artefacts. `NO-GO` for public
publication actions until the remaining publication gates are closed and separately authorized.

The final package replays all bounded prototype oracles successfully and keeps the published core
separate. This is engineering verification, not domain validation or scientific confirmation.

## Final-package results

| Check | Observed result |
|---|---|
| v1.1 scenario comparison | `15/15 PASS` |
| v1.1 mutation gates | `27/27 PASS` |
| v1.1 A/B/C OWL module integration | `26/26 PASS` |
| v1.1 package integrity | `27/27 PASS` |
| Full local v1.1 and repository regression | `14/14 command groups PASS` |
| Cross-engine temporal portability | `8/8 PASS` on two engines |

The scenario, mutation, and module-integration runners operate on the final v1.1 vocabulary and shapes.
The experimental fixtures are migrated in memory, with `exp:causallyPrecedes` deliberately renamed to
`strict:hasCausalNextStage`, so the established oracles are tested against the owner-selected
approved contract rather than copied expected output.

The full run parsed the complete repository Turtle inventory, matched all 13 repository fixture
classifications, and passed the
repository reasoner, SHACL, cross-layer, competency-query, structure-audit, and wording gates.

## Formal coverage

The executable checks cover:

- directed single-lineage membership, order, cycles, reversal, branch/merge applicability, and local
  role collapse;
- Delay-to-path linkage, missing and mismatched lineage qualification, canonical UTC-second forms,
  boundary ordering, and permitted process overlap;
- separate assessment scope and path identity;
- independent claim-record, ontic-linkage, and evidence-record results;
- mixed applicability and validation outcomes without hidden findings;
- core-only, core-plus-strict, and core-plus-strict-plus-BFO module configurations;
- absence of unintended ontic types from claim subject/object fields;
- unchanged core imports and existing repository reasoner, SHACL, cross-layer, competency, structure,
  and wording gates.

## Compatibility finding

The package is an additive opt-in module and does not replace v1.0.0 semantics. It is behaviorally
stricter when explicitly selected. Loading the optional vocabulary intentionally exposes scope/path
identity collapse; selecting its profiles requires facts that the default v1.0.0 validation did not
require.

## Open and non-verified items

| Item | Status | Effect |
|---|---|---|
| Permanent `w3id.org` namespace resolution | `UNRESOLVED` — ontology IRI returned HTTP 404 on 2026-10-11 | IRI contract is owner-approved; application awaits immutable targets and a separately authorized w3id PR |
| Cross-engine SHACL temporal comparison | `PASS` — 8/8 agreement on pySHACL 0.40.1/RDFLib 7.6.0 and Apache Jena SHACL 6.2.0 | Blocker closed for the recorded versions and matrix; rerun on engine or shape changes |
| Branch/merge identity semantics | `OUT_OF_SCOPE` | Strict Linear cannot be claimed for those cases |
| Information-object upper-ontology alignment | `DEFERRED` | PROV-only model retained |
| Domain evidence thresholds | `UNASSESSED` | No scientific adequacy or causal truth claim |
| Independent multi-domain validation | `UNASSESSED` | No scientific validation claim |

## Publication blockers

- operational resolution and content-negotiation checks for the approved public IRIs;
- byte-verification of the immutable raw HTTPS targets used by the redirect plan;
- an explicit release action separate from this local preparation task.

A preservation commit and branch push exist as recorded in the owner decision register. No merge,
tag, release, DOI deposit, manuscript edit, w3id change, or change to the published core is part of
this report.

The resolution observation was made with a read-only HTTP request to
`https://w3id.org/resonatus/strict`. The offline package runner records this as a known blocker rather
than repeating a network request.

See `TEMPORAL_PORTABILITY_REPORT.md` for the independent engine evidence,
`IRI_PUBLICATION_PLAN.md` for the non-applied redirect design, and `OWNER_NORMATIVE_APPROVAL.md` for
the completed design approval and its publication limits.
