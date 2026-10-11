# Resonatus v1.1 strict-profile release readiness

**Assessment:** final four engineering gates pass; conditionally ready to prepare an optional v1.1
strict-profile release candidate after explicit owner approval of the remaining production decisions.

## Gate summary

| Gate | Result | Evidence |
|---|---|---|
| Original eight-case acceptance | Pass | CE01/CE02 do not conform; valid B/C fixtures conform in their activated dimensions |
| Expanded targeted cases | Pass | 15/15 scenario expectations, including unrelated Delay and split claim outcomes |
| Mutation adequacy | Pass | 27/27 mutations, including pre-gate gap reproduction, mixed outcomes, Delay binding, and claim/link separation |
| Combined OWL module integration | Pass | 26/26 checks across core-only, core+experimental, and core+experimental+BFO |
| Current regression suite | Pass | 69 Turtle files parse; OWL R2–R17, SHACL R18–R26, 13/13 examples, 2/2 layer-independence cases, inconsistency/error guards, and 7/7 executable CQs pass |
| Core OWL unchanged | Pass | No changes under `ontology/` |
| Normative SHACL unchanged | Pass | No changes to `shapes/resonatus.shacl.ttl` |
| Five criteria unchanged | Pass | No definition or criterion vocabulary change |
| Branch/merge semantics | Intentionally not implemented | Applicability is `OUT_OF_SCOPE`; simultaneous validation findings remain visible |
| External causal relation | Unresolved | No exact reuse candidate selected |
| Scientific validation | Not performed | Every prototype run reports `scientific_conclusion=UNDETERMINED` |

## Decision table

### `READY_FOR_NORMATIVE_REVIEW`

| Item | Review package |
|---|---|
| Five-state validation protocol | Definitions, output precedence, error handling, and executable cases |
| Bounded linear lineage profile | Segment registration, directed spine, reference agreement, cycles, role collapse, and branch detection |
| Optional Delay profile | Positive overlap, exact-boundary failure, missing-data outcome, and explicit same-path qualification |
| Separate assessment scope | Distinct information-object pattern and collapse test |
| Claim/ontic/evidence separation | Claim-record, ontic-linkage, evidence-record, existential-only, conflict, and isolated-range tests |
| Compatibility model | Additive opt-in profile proposal that leaves current OWL membership unchanged |

“Ready for normative review” means reviewers have a precise contract and tests. It does not mean the
item is approved for the production namespace.

### `REQUIRES_OWNER_DECISION`

| Decision | Options/impact |
|---|---|
| Production causal-edge IRI | Mint a narrow Resonatus relation, revise the contract to reuse RO, or align only to a broad compatible superproperty |
| Directness/granularity | Define when no intermediate stage exists and who declares the operative granularity |
| Segment membership semantics | Keep profile membership only, or add justified BFO parthood/participation axioms |
| Pairwise role distinctness | Adopt the bounded policy, weaken it to selected distinctions, or permit multi-role processes |
| Information-object alignment | PROV-only, optional BFO generically dependent continuant, or an IAO/CCO information-content term |
| Production Delay-binding IRI | Approve a stable equivalent of experimental `temporallyQualifiesPath` |
| Profile activation | Approve Strict Linear = lineage+temporal and Strict Assessment = Strict Linear+scope+claim-record; ontic linkage and evidence status reported separately |
| Timestamp portability | Keep canonical UTC lexical normalization or require an engine-neutral comparison implementation |
| Profile packaging/version identifiers | Final paths, ontology/profile IRIs, import policy, and conformance vocabulary |
| Published Trace existential | Preserve for v1.1 as recommended, or schedule a breaking redesign in a major version |

### `SCIENTIFICALLY_UNRESOLVED`

| Question | Why unresolved |
|---|---|
| Truth of any asserted causal edge | SHACL checks graph structure, not the world |
| Domain evidence sufficiency | No biological, software, cognitive, or social evidence protocol was validated |
| Necessity and joint discrimination of five criteria | Formal separability is not empirical validation |
| Resonatus as an independent process kind | No comparative empirical study against simpler models |
| Cross-domain stability of “direct” causation | Granularity and mechanism differ by domain |
| Branch/merge process identity | Explicitly outside the linear profile |
| Carrier/participant continuity | No shared bearer or transmission criterion selected |
| Transformation/Feedback boundary | Preserved unchanged and still scientifically under-specified |

## Overall release decision

| Decision class | Overall result |
|---|---|
| `READY_FOR_NORMATIVE_REVIEW` | **Yes**, for the bounded profile components listed above |
| `REQUIRES_OWNER_DECISION` | **Yes**, before any production vocabulary/profile publication |
| `SCIENTIFICALLY_UNRESOLVED` | **Yes**, and must remain explicit in public claims |

Recommendation: **CONDITIONAL GO** for preparing an optional v1.1 strict-profile release candidate,
not for publishing it. Conditions are explicit owner approval of production IRIs, causal-edge
granularity, necessary local role distinctions, timestamp portability, profile identifiers, and the
activation contract. Scientific causal validity remains outside the release claim.

## Proposed owner approval record

```text
Profile name and version:
Production module/profile IRIs:
Causal-edge decision:
Segment/parthood decision:
Role-distinctness policy:
Mandatory validation dimensions:
Timestamp policy:
BFO/information-object alignment:
Compatibility classification:
Approved implementation scope:
```

Only after that record is complete should experimental terms move out of
`docs/research/prototypes/v11/`.
