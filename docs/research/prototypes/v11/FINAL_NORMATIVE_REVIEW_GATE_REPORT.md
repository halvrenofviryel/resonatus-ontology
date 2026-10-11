# Resonatus v1.1 final normative review gate report

**Date:** 2026-10-11

**Status:** bounded engineering review complete; experimental and non-normative
**Recommendation:** `CONDITIONAL GO` to prepare an optional v1.1 strict-profile release candidate;
`NO-GO` for publication until the owner approval conditions below are recorded

## Executive result

All four requested gates pass after targeted experimental changes:

| Gate | Result | Executable evidence |
|---|---|---|
| Delay lineage coherence | Pass | Pre-gate reconstruction accepts the unrelated Delay; new constraints distinguish missing linkage from explicit mismatch (M18a–M18c) |
| Mixed validation outcomes | Pass | Applicability is independent; out-of-scope plus violation/missing and violation plus missing retain every finding (M15–M17) |
| Claim record versus ontic linkage | Pass | Positive, claim-only, incomplete, missing-evidence, and conflicting cases produce independent record/link/evidence results |
| Combined OWL module integration | Pass | 26/26 checks across core-only, core+experimental, and core+experimental+BFO configurations |

The expanded comparison passes 15/15 cases and the mutation runner passes 27/27 checks. These are
formal and structural results. Domain evidence adequacy and scientific causal validity remain
`UNASSESSED`/`UNDETERMINED`.

## 1. Verified findings

### Gate 1 — Delay lineage coherence

The pre-gate temporal profile checked only the Delay's origin and timestamps. M18a reconstructs that
profile by removing only the new Delay-to-path constraints and observes `CONFORMING` for a valid causal
spine whose Delay explicitly qualifies an unrelated continuation. The semantic gap was therefore real:
same origin plus post-origin time did not establish same-lineage qualification.

The smallest added commitment is:

```text
Delay exp:temporallyQualifiesPath ContinuationPath
```

For strict temporal validation, the target must be the same path that carries the Delay through
`res:hasPostInteractionContinuation`.

- Missing qualification: `INSUFFICIENT_DATA` (`MISSING_TEMPORAL_LINEAGE_LINK`).
- Explicit qualification of another path: `NON_CONFORMING`
  (`VIOLATION_TEMPORAL_LINEAGE_MISMATCH`).
- The Delay is not added to `exp:hasCausalSegment` and no causal edge is inferred from it.
- The existing overlapping-process test still conforms; no end-before-start causal rule was added.

### Gate 2 — mixed validation outcomes

The previous classifier evaluated `OUT_OF_SCOPE_` before `VIOLATION_` and could label a mixed report
`NOT_EVALUATED`, hiding an explicit violation in the summary outcome. The runner now reports:

```text
applicability: IN_SCOPE | OUT_OF_SCOPE
validation:    CONFORMING | NON_CONFORMING | INSUFFICIENT_DATA |
               NOT_EVALUATED | EXECUTION_ERROR
findings:      every SHACL result message
```

Precedence applies only to the validation column:

1. engine failure → `EXECUTION_ERROR`;
2. any `VIOLATION_` → `NON_CONFORMING`;
3. otherwise any `MISSING_` → `INSUFFICIENT_DATA`;
4. otherwise a pure `OUT_OF_SCOPE_` → `NOT_EVALUATED`;
5. no findings → `CONFORMING`.

M15 proves `OUT_OF_SCOPE + VIOLATION` remains `OUT_OF_SCOPE / NON_CONFORMING`. M16 proves
`OUT_OF_SCOPE + MISSING` remains `OUT_OF_SCOPE / INSUFFICIENT_DATA`. M17 proves a violation is not
hidden by simultaneous missing data. M10 continues to report an engine error explicitly.

### Gate 3 — claim record versus ontic linkage

The single former evidence result is split into independent planes:

| Plane | Question | Missing/negative interpretation |
|---|---|---|
| Claim record | Are subject, object, and typed method structurally present with valid cardinality? | Malformed or incomplete record only |
| Evidence record | Does the claim cite a typed `res:Evidence` record? | Missing structural source record; not a verdict on evidence quality |
| Ontic linkage | Do the claim relata match an explicit `res:causallyAttributedTo` assertion? | Missing link is insufficient; explicit different target is non-conforming |
| Domain evidence adequacy | Is the cited evidence scientifically sufficient? | Always `DOMAIN_EVIDENCE_UNASSESSED` in this profile |

Observed cases:

| Case | Claim record | Ontic linkage | Evidence record |
|---|---|---|---|
| Valid C | `CONFORMING` | `CONFORMING` | `CONFORMING` |
| Claim-only hypothesis | `CONFORMING` | `INSUFFICIENT_DATA` | `CONFORMING` |
| Missing method | `INSUFFICIENT_DATA` | `CONFORMING` | `CONFORMING` |
| Missing evidence record | `CONFORMING` | `CONFORMING` | `INSUFFICIENT_DATA` |
| Explicitly conflicting target | `CONFORMING` | `NON_CONFORMING` | `CONFORMING` |

A valid unaccepted hypothesis is therefore representable without becoming a malformed claim record.
The experimental claim properties retain no ontic range axioms. M13 and the combined-module runner
confirm that an isolated claim does not infer `res:TraceContinuation` or `res:Interaction` for its
relata. The published meaning of `res:causallyAttributedTo` is unchanged.

### Gate 4 — combined OWL module integration

The integration runner loads and reasons over:

- A: published core only;
- B: core plus experimental vocabulary;
- C: core plus experimental vocabulary, optional BFO bridge, and pinned BFO 2020.

Observed results:

| Case | A | B | C | Intended difference |
|---|---|---|---|---|
| Valid B | consistent | consistent | consistent | None |
| Valid C | consistent | consistent | consistent | None |
| Collapsed scope/path | consistent | inconsistent | inconsistent | Experimental disjointness active only in B/C |
| Claim-only | consistent | consistent | consistent | None |
| Isolated claim | consistent | consistent | consistent | None |

All relevant named classes are satisfiable in every configuration in which they are loaded. Published
`res:Resonatus` membership for valid B, valid C, and claim-only cases is invariant across A/B/C.
Claim-only remains an `EXISTENTIAL_COMMITMENT_ONLY` case with no named ontic triple. The BFO bridge
adds no observed inconsistency or unintended claim-relata typing.

## 2. Exact experimental changes

### Vocabulary

- Added experimental `exp:temporallyQualifiesPath` with domain
  `res:PostInteractionContinuation` and range `res:ContinuationPath`.
- Kept Delay outside `exp:hasCausalSegment` and added no BFO parthood axiom.
- Retained the narrow, non-transitive, overlap-permitting experimental causal edge.
- Retained claim properties without ontic subject/object ranges.

### Shapes

- Extended the temporal shape with Delay-to-path minimum, maximum, type, and same-path checks.
- Split claim validation into claim-record, ontic-linkage, and evidence-record shape files.
- Kept scope and lineage shapes experimental and separate from the published v1.0.0 shape.

### Runners and fixtures

- Added profile applicability and mixed-result precedence to `run_prototypes.py`.
- Expanded the comparison from 12 to 15 cases.
- Expanded mutations from 15 to 27 checks, including reconstruction of the pre-gate Delay gap.
- Added `run_owl_module_integration.py` with 26 A/B/C configuration checks.
- Added unrelated-Delay, incomplete-claim, and conflicting-linkage fixtures.
- Updated positive temporal fixtures with explicit Delay-to-path qualification.

No file under `ontology/` or the repository-level `shapes/` directory was changed by this gate task.

## 3. Executed commands and observed results

Commands were run from the repository root with the pinned environment:

```bash
env PYTHONDONTWRITEBYTECODE=1 /mnt/data/claude/resonatus-ontology/.venv/bin/python \
  docs/research/prototypes/v11/run_prototypes.py
# cases=15/15; critical_acceptance=PASS; scientific_conclusion=UNDETERMINED; overall=PASS

env PYTHONDONTWRITEBYTECODE=1 /mnt/data/claude/resonatus-ontology/.venv/bin/python \
  docs/research/prototypes/v11/run_prototype_mutations.py
# mutations=27/27; overall=PASS

env PYTHONDONTWRITEBYTECODE=1 /mnt/data/claude/resonatus-ontology/.venv/bin/python \
  docs/research/prototypes/v11/run_owl_module_integration.py
# integration_checks=26/26; overall=PASS

env PYTHONDONTWRITEBYTECODE=1 /mnt/data/claude/resonatus-ontology/.venv/bin/python scripts/validate.py .
# PARSE 69 Turtle files: OK; 13/13 fixture classifications

env PYTHONDONTWRITEBYTECODE=1 /mnt/data/claude/resonatus-ontology/.venv/bin/python scripts/run_reasoner_gates.py
# ALL GATES PASS

env PYTHONDONTWRITEBYTECODE=1 /mnt/data/claude/resonatus-ontology/.venv/bin/python scripts/run_shacl_gates.py
# ALL SHACL GATES PASS

env PYTHONDONTWRITEBYTECODE=1 /mnt/data/claude/resonatus-ontology/.venv/bin/python scripts/run_example_crosslayer.py
# aligned=13/13; layer_independence=2/2; inconsistency/error guards PASS

env PYTHONDONTWRITEBYTECODE=1 /mnt/data/claude/resonatus-ontology/.venv/bin/python scripts/run_competency_queries.py
# 7/7 PASS

env PYTHONDONTWRITEBYTECODE=1 /mnt/data/claude/resonatus-ontology/.venv/bin/python scripts/audit_structure.py
# 13/13 PASS

env PYTHONDONTWRITEBYTECODE=1 /mnt/data/claude/resonatus-ontology/.venv/bin/python scripts/check_wording.py
# wording lint PASS
```

Observed results were computed before comparison with the explicit test oracles; expected values were
not substituted for actual results.

## 4. Proposed profile activation rules

### Strict Linear Conformance

The named claim requires:

- applicability `IN_SCOPE` for the bounded single-lineage profile;
- lineage `CONFORMING`;
- temporal `CONFORMING`, including the Delay-to-path link;
- no requirement that causal processes be temporally non-overlapping.

An `OUT_OF_SCOPE` branch/merge graph cannot claim Strict Linear Conformance, even when unrelated
validation dimensions conform.

### Strict Assessment Conformance

The named claim requires Strict Linear Conformance plus:

- scope `CONFORMING`;
- claim record `CONFORMING`;
- evidence record `CONFORMING` as structural source documentation.

Ontic linkage must be reported independently and must not retroactively invalidate a structurally valid
hypothesis record. A deployment may define a stricter “ontically linked assessment” claim requiring
ontic linkage `CONFORMING`, but that must be a separately named conformance claim. Domain evidence
adequacy remains `UNASSESSED`; neither level means `SCIENTIFICALLY_VERIFIED`.

## 5. Proposed production vocabulary contract

This is a design proposal, not authorization to publish the experimental namespace.

| Term family | Proposed contract |
|---|---|
| `ContinuationPath` | Remains the published ontic process; its OWL membership semantics do not change |
| `AssessmentScope` | Separate information object, disjoint from `ContinuationPath` in the optional module |
| `CausalAttributionClaim` | Epistemic claim object; no ontic range inference from claim subject/object properties |
| Causal edge | New Resonatus-specific, directed, asymmetric, irreflexive, non-transitive edge at declared granularity; no automatic RO/BFO equivalence |
| Segment membership | Profile membership only; not BFO process parthood |
| Delay binding | New stable equivalent of `exp:temporallyQualifiesPath`; binds Delay to one path without making it a causal segment |
| Published `causallyAttributedTo` | Unchanged ontic relation; claim matching is a separate validation result |

The optional production module must not be imported by the v1.0.0 core. Strict shapes must be versioned
and selected explicitly rather than silently replacing `shapes/resonatus.shacl.ttl`.

## 6. Compatibility implications

- Existing v1.0.0 OWL and SHACL results remain authoritative when the optional profile is not selected.
- Strict adopters must add causal-spine memberships and edges, Delay-to-path qualification, canonical
  origin/receiver references, and OWL-Time boundaries.
- Assessment adopters must mint a distinct scope object and structurally separate claims, methods, and
  evidence records.
- Loading the optional vocabulary can intentionally expose scope/path identity collapse as OWL
  inconsistency; this is an opt-in data-compatibility effect.
- Branch/merge data remains representable but cannot claim first-profile strict-linear conformance.
- Strengthening the core OWL membership definitions or changing the five criteria remains a breaking,
  major-version change and is outside this proposal.

## 7. Outstanding owner decisions

| Decision | Required before RC packaging? | Proposed default |
|---|---:|---|
| Stable module/profile IRIs and filenames | Yes | Versioned optional v1.1 artefacts |
| Stable causal-edge IRI and granularity wording | Yes | Narrow Resonatus relation; no equivalence mapping |
| Stable Delay-binding IRI | Yes | Production equivalent of `temporallyQualifiesPath` |
| Necessary local role-distinctness set | Yes | Require only distinctions needed to prevent category/identity collapse; do not generalize without review |
| Timestamp comparison portability | Yes | Replace or normatively document the pinned canonical-UTC lexical policy |
| Profile activation names and result serialization | Yes | Strict Linear and Strict Assessment as specified above |
| Information-object upper-ontology alignment | No for initial RC if left PROV-only | Defer optional BFO/IAO mapping |
| Branch/merge identity semantics | No | Explicitly outside the first profile |
| Domain evidence thresholds and scientific validation | No | Separate empirical workstream; never implied by conformance |

## 8. Final recommendation and owner approval table

| Item | Recommendation | Owner action |
|---|---|---|
| Four final review gates | `GO` | Accept the observed gate closures |
| Optional v1.1 strict-profile RC preparation | `CONDITIONAL GO` | Approve the six RC-required decisions above |
| Publish production vocabulary or release | `NO-GO` at this stage | First record production IRIs, activation contract, role policy, and timestamp policy |
| Claim scientific causal validation | `NO-GO` | Requires independent domain evidence and empirical evaluation |
| Change core OWL or five criteria | `NO-GO` within v1.1 task | Requires separate major-version/scientific review |

Exact minimal implementation after owner approval:

1. mint the approved production IRIs in a separate optional v1.1 vocabulary module;
2. move the tested lineage, temporal, scope, claim-record, ontic-linkage, and evidence-record shapes
   into versioned optional profile artefacts;
3. replace experimental IRIs in fixtures and runners without changing the validated contracts;
4. add machine-readable profile identifiers and applicability/validation result serialization;
5. rerun the complete gate set and generate release checksums/notes;
6. stop before tag or publication unless separately authorized.

No commit, push, merge, tag, release, or experimental-vocabulary publication is part of this review.
