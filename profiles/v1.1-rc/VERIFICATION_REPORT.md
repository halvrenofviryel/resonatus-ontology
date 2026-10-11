# Resonatus v1.1 local RC verification report

**Candidate:** `1.1.0-rc.1`

**Date:** 2026-10-11

**Environment:** pinned Python at `/mnt/data/claude/resonatus-ontology/.venv/bin/python`

## Disposition

`CONDITIONAL GO` for local owner inspection of the RC package. `NO-GO` for publication.

The candidate replays all bounded prototype oracles successfully and keeps the published core
separate. This is engineering verification, not domain validation or scientific confirmation.

## Candidate results

| Check | Observed result |
|---|---|
| Candidate scenario comparison | `15/15 PASS` |
| Candidate mutation gates | `27/27 PASS` |
| Candidate A/B/C OWL module integration | `26/26 PASS` |
| Candidate package integrity | `24/24 PASS` |
| Full local RC and repository regression | `14/14 command groups PASS` |

The scenario, mutation, and module-integration runners operate on the actual RC vocabulary and shapes.
The experimental fixtures are migrated in memory, with `exp:causallyPrecedes` deliberately renamed to
`strict:hasCausalNextStage`, so the established oracles are tested against the owner-selected
candidate contract rather than copied expected output.

The full run parsed 87 Turtle files, matched all 13 repository fixture classifications, and passed the
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

The candidate is an additive opt-in module and does not replace v1.0.0 semantics. It is behaviorally
stricter when explicitly selected. Loading the optional vocabulary intentionally exposes scope/path
identity collapse; selecting its profiles requires facts that the default v1.0.0 validation did not
require.

## Open and non-verified items

| Item | Status | Effect |
|---|---|---|
| Permanent `w3id.org` namespace resolution | `UNRESOLVED` — ontology IRI returned HTTP 404 on 2026-10-11 | Blocks publication; all candidate identifiers remain provisional |
| Cross-engine SHACL temporal comparison | `NOT_RUN` | Pinned pySHACL/RDFLib behavior is verified locally; portability claim is not made |
| Branch/merge identity semantics | `OUT_OF_SCOPE` | Strict Linear cannot be claimed for those cases |
| Information-object upper-ontology alignment | `DEFERRED` | PROV-only candidate model retained |
| Domain evidence thresholds | `UNASSESSED` | No scientific adequacy or causal truth claim |
| Independent multi-domain validation | `UNASSESSED` | No scientific validation claim |

## Publication blockers

- owner approval of permanent namespace, version, filenames, and release scope;
- operational resolution and content-negotiation checks for the approved public IRIs;
- a recorded decision on supported temporal-validation engines or a portability test matrix;
- final package review after any identifier change, followed by regenerated checksums and a complete
  regression run;
- an explicit release action separate from this local preparation task.

No commit, push, merge, tag, release, DOI deposit, manuscript edit, or change to the published core is
part of this report.

The resolution observation was made with a read-only HTTP request to
`https://w3id.org/resonatus/strict`. The offline package runner records this as a known blocker rather
than repeating a network request.
