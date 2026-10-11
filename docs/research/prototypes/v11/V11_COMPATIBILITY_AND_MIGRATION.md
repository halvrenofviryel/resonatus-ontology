# Resonatus v1.1 compatibility and migration analysis

**Status:** design analysis only; no normative change applied

## Compatibility objective

The safe v1.1 path is an additive, explicitly selected strict-validation profile. It must not:

- change the meaning of published `ContinuationPath` or `causallyAttributedTo`;
- change the OWL equivalence defining `Resonatus` or `ResonatusPath`;
- cause old data to fail the existing `shapes/resonatus.shacl.ttl` profile;
- import BFO into the core;
- rewrite v1.0.0 release artefacts.

Strict-profile conformance is an additional claim, not a replacement for OWL membership.

## Proposed-change impact matrix

| Proposed future change | OWL entailment impact | SHACL impact | Published IRI compatibility | Fixture migration | BFO consequence | Compatibility |
|---|---|---|---|---|---|---|
| Add `AssessmentScope` and scope properties in a separate module | New inferences only if module is loaded; disjointness can expose existing scope/path conflation as inconsistency | New scope dimension for activated assessments | Preserves all existing IRIs | Strict-scope fixtures add a distinct scope node | Information-object placement remains undecided; do not map it to process | Additive module; behaviorally stricter when selected |
| Add `CausalAttributionClaim` and claim properties | Claim objects become explicit; claim properties must not have ontic Trace/Interaction ranges | Claim record, ontic linkage, and evidence record become independent dimensions | `causallyAttributedTo` keeps its ontic meaning | Claim fixtures add subject, object, evidence, and method | Likely information-content alignment, but optional bridge needs review | Additive if kept separate |
| Add causal-spine membership property | No current membership inference changes if omitted from `ResonatusPath` OWL definition | Strict lineage requires explicit registration | New IRI required; `directlyContinues` cannot be repurposed | Strict fixtures register Trace, Propagation, Selectivity, and outcome | Must not be equated with BFO parthood without further semantics | Additive optional profile |
| Add a directed causal-spine relation | New asserted facts; domain/range or external alignment may create further types and temporal commitments | Strict lineage checks direction, cycles, and adjacency | New IRI or approved external IRI required | Strict fixtures add four directed edges | RO/BFO alignment is unresolved | Owner decision required |
| Publish optional temporal Delay profile and path binding | Experimental property adds only module-selected domain/range inferences | Missing interval/path linkage is `INSUFFICIENT_DATA`; boundary-equal or explicit different-path linkage is `NON_CONFORMING` | Reuses published time properties; adds a new production IRI for path qualification | Strict temporal fixtures add origin/Delay intervals and a Delay-to-path link | No core BFO import; Delay is not made a causal segment or BFO part | Additive optional profile |
| Publish five-state validation result protocol | No ontology inference change unless represented in RDF | Replaces Boolean reporting in the strict runner, not in W3C SHACL itself | Existing verdict IRIs remain unchanged | Test expectations become dimension-specific | None | Tooling/API behavior change; document clearly |
| Add scope/path disjointness to a loaded ontology module | Can make graphs that identify scope and path inconsistent | Mirrors current scope shape | Preserves names but rejects prior conflation | Collapsed-scope data must mint a distinct scope node | Supports ontic/information separation | Additive axiom with potentially breaking data effect |
| Change `Resonatus` or `ResonatusPath` OWL equivalence to require lineage | Removes current entailments such as CE01/CE02 | Would make strict structure part of membership | Same IRIs would gain stronger meaning | Most v1.0.0 fixtures require migration | May strengthen process reading | Breaking; requires a major version |

## Explicit versus existential causal commitments

The published core contains:

```text
TraceContinuation SubClassOf causallyAttributedTo some Interaction
```

It also gives `hasTraceContinuation` the range `TraceContinuation`. Therefore either of these modelling
choices creates an ontic existential commitment:

- explicitly typing a node as `TraceContinuation`;
- linking it as a path's `hasTraceContinuation` value.

The reasoner may satisfy the existential with an unnamed individual. A deterministic SHACL graph does
not thereby acquire a named `causallyAttributedTo` triple.

Migration rule:

- use `TraceContinuation` and `hasTraceContinuation` only when an ontic Trace commitment is intended;
- use `CausalAttributionClaim` alone for a claim that has not yet been accepted into the ontic graph;
- do not give claim-subject/object properties ontic range axioms;
- promote a claim to an ontic assertion only through an explicit, documented workflow.

Relaxing the published Trace existential would change existing semantics and is not proposed for v1.1.

## Data migration by adoption level

### Existing v1.0.0 profile only

No migration. Existing OWL and SHACL results remain the authoritative v1.0.0 results.

### Strict lineage profile selected

For each qualifying path:

1. register Trace, Propagation, Selectivity, and outcome as causal-spine segments;
2. assert the four selected directed edges;
3. ensure canonical origin and receiver references;
4. keep role nodes distinct under the initial bounded profile;
5. do not submit branch/merge cases as linear-profile membership evidence.

### Temporal profile selected

Add one OWL-Time interval to the origin and Delay witness, including the Delay beginning/end and origin
end, and explicitly link the Delay to the `ContinuationPath` it qualifies. The current implementation
requires canonical UTC second precision. A missing link or time value produces `INSUFFICIENT_DATA`; an
explicit link to a different path produces `NON_CONFORMING`.

### Separate-scope profile selected

For each assessment, mint a distinct scope information object and link it to the existing
`assessesPath` process. Do not reuse the path, candidate, assessment, or evidence node as the scope.

### Assessment/claim profiles selected

Represent the claim, subject, object, evidence, and method separately. Claim-record conformance,
explicit ontic linkage, and evidence-record presence are reported independently. A structurally
complete unaccepted hypothesis therefore remains a valid record. Domain evidence adequacy stays
`UNASSESSED`; a claim is not a replacement for the ontic causal triple.

## Existing fixture impact

- CE01: remains OWL-entailed and current-profile conforming; strict lineage/temporal data must be added
  before it can be evaluated positively.
- CE02: cannot migrate by adding edges alone because the bounded profile rejects role collapse.
- Existing positive examples: retain v1.0.0 results; strict conformance requires new segment, edge, and
  interval assertions.
- Existing assessment fixtures: remain valid under the published shape; separate scope is required only
  if the new scope profile is explicitly selected.
- Branching or merging real cases: report applicability as `OUT_OF_SCOPE`; pure topology yields
  `NOT_EVALUATED`, while simultaneous violations or missing data retain their own result.

## BFO bridge consequences

`ContinuationPath` remains mapped to BFO process in the optional bridge. The prototype does not assert
that causal-spine membership is `occurrent part of` or `temporal part of`; either mapping would add a
unity commitment that has not been justified.

`AssessmentScope` and `CausalAttributionClaim` are intended as information objects. A future BFO bridge
could place them under generically dependent continuant, potentially through an information-content
ontology, but that would require decisions about concretization and bearer relations. No such mapping
is applied here.

Adopting an RO relation may import BFO domain/range and temporal superproperty consequences. Those
effects must be tested against the optional bridge before release.

The final integration runner has now tested core-only, core plus experimental vocabulary, and core plus
experimental vocabulary plus the pinned BFO bridge. Valid B/C and claim-only graphs remain consistent;
all relevant named classes remain satisfiable; isolated claim properties do not infer ontic relata.
Scope/path collapse is consistent under core-only data but becomes intentionally inconsistent when the
experimental disjointness is loaded, with or without BFO.

## Versioning decision

| Change package | Recommended versioning |
|---|---|
| New optional strict SHACL profile, result protocol, and additive claim/scope module; core OWL unchanged | Eligible for v1.1 after owner approval |
| Import strict shapes as the default replacement for v1.0.0 validation | Potentially breaking validation change; require explicit profile/version negotiation |
| Strengthen `ResonatusPath`/`Resonatus` OWL definitions with lineage or time constraints | Major version |
| Reinterpret `ContinuationPath` as an assessment bundle or `causallyAttributedTo` as a claim | Prohibited silent change; major-version migration with new terms |
| Change the five constitutive criteria | Outside this task; semantic and scientific review required |

## Proposed packaging

If approved, publish separate artefacts rather than silently modifying defaults:

```text
ontology/resonatus.ttl                  unchanged core semantics
profiles/v1.1/strict-lineage.shacl.ttl  opt-in structural profile
profiles/v1.1/temporal-delay.shacl.ttl  opt-in temporal profile
profiles/v1.1/strict-vocabulary.ttl     additive lineage, Delay-binding, claim, and scope vocabulary
profiles/v1.1/assessment-scope.shacl.ttl opt-in scope profile
profiles/v1.1/claim-record.shacl.ttl    opt-in structural claim-record profile
profiles/v1.1/ontic-linkage.shacl.ttl   independently reported explicit-link profile
profiles/v1.1/evidence-record.shacl.ttl independently reported evidence-record presence profile
```

Exact names and production IRIs remain owner decisions. Experimental `exp:` IRIs must not be published
as stable terms by accident.
