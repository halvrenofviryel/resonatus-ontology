# Resonatus v1.1 strict-profile semantic contract

**Status:** candidate contract for normative review; experimental and non-normative
**Scope:** one bounded linear lineage; the five constitutive criteria are unchanged

## Result planes

The profile reports independent dimensions. No result in one column implies a result in another.

| Plane | Allowed results | Contract |
|---|---|---|
| OWL membership | `OWL_ENTAILED`, `OWL_NOT_ENTAILED`, `OWL_INCONSISTENT`, `OWL_EXECUTION_ERROR` | Model-theoretic result from the unchanged core plus case data |
| Profile applicability | `IN_SCOPE`, `OUT_OF_SCOPE` | Whether the selected bounded profile can evaluate the graph topology; independent of validation findings |
| Lineage, temporal, scope, claim record, ontic linkage, evidence record | `CONFORMING`, `NON_CONFORMING`, `INSUFFICIENT_DATA`, `NOT_EVALUATED`, `EXECUTION_ERROR` | Closed-world validation result for one named dimension |
| Causal commitment | `EXPLICIT_ONTIC_RELATION`, `EXISTENTIAL_COMMITMENT_ONLY`, `NONE_IDENTIFIED` | Whether the graph names the ontic relation or only commits to an existential filler |
| Domain evidence adequacy | `DOMAIN_EVIDENCE_UNASSESSED`, `DOMAIN_EVIDENCE_NOT_EVALUATED` | The prototype does not evaluate scientific adequacy |
| Scientific conclusion | `UNDETERMINED` in this prototype | Requires domain evidence and an external causal-evaluation procedure |

Interpretation of the validation results:

- `CONFORMING`: all activated constraints in that dimension are satisfied.
- `NON_CONFORMING`: supplied data contains a determinable structural or boundary violation.
- `INSUFFICIENT_DATA`: required facts are absent, so the dimension cannot be decided.
- `NOT_EVALUATED`: the dimension was not activated or the case is outside the bounded linear profile.
- `EXECUTION_ERROR`: the validation procedure did not produce a trustworthy result.

`INSUFFICIENT_DATA` and `NOT_EVALUATED` are not evidence of factual non-membership. Classification
precedence is `EXECUTION_ERROR`, then any `VIOLATION_`, then any `MISSING_`, then a pure
`OUT_OF_SCOPE_`. Thus applicability can be `OUT_OF_SCOPE` while validation is `NON_CONFORMING` or
`INSUFFICIENT_DATA`; all findings remain visible.

## 1. `ContinuationPath`

**Definition.** An ontic, temporally extended process proposed as one continuation from a declared
origin interaction. Under the linear strict profile it carries a directed causal spine and a separate
Delay witness.

**Necessary conditions**

- It is linked from a candidate by `res:hasTracePath`.
- It declares exactly one origin for this profile.
- It has one Trace, Delay, Propagation, Selectivity, and Transformation-or-Feedback witness.
- Trace, Propagation, Selectivity, and outcome are registered as causal-spine segments.
- The causal spine is directed origin → Trace → Propagation → Selectivity → outcome.
- Its Delay explicitly identifies this path through `exp:temporallyQualifiesPath`.
- Origin and receiver references agree, subject to the profile's canonical-node policy.

**Excluded interpretations**

- An assessment record, evidence bundle, report, provenance receipt, or arbitrary RDF container.
- A claim that the path is scientifically established merely because its RDF graph conforms.
- A general branch/merge identity policy.

**Positive example:** `fixtures/b-valid-process-path.ttl`.

**Counterexample:** CE01 groups five witnesses on one node but supplies no lineage; it is
`INSUFFICIENT_DATA` for lineage. CE02 also collapses path and roles and is `NON_CONFORMING`.

**OWL commitment:** the published IRI remains a `prov:Activity`; the optional BFO bridge maps it to
`BFO_0000015` process. Existing OWL membership semantics are unchanged.

**Required SHACL:** exact role counts for the bounded profile, segment registration, forward edges,
reference agreement, distinctness, cycle rejection, and branch/merge detection.

**Evidence requirement:** every causal edge still requires a domain-appropriate justification.
Structural conformance alone supplies none.

## 2. `AssessmentScope`

**Definition.** An information object used by one assessment to identify the ontic process path being
evaluated.

**Necessary conditions**

- Exactly one activated assessment scope is linked from its assessment.
- It denotes the assessment's `res:assessesPath` through `exp:scopesProcess`.
- It is distinct from the assessment, candidate, and process path.

**Excluded interpretations**

- The real process itself.
- A second process introduced only to carry assessment metadata.
- Evidence that the scoped process exists or is causally coherent.

**Positive example:** `fixtures/c-valid-overlay.ttl`.

**Counterexample:** `fixtures/c-invalid-scope-is-process-overlay.ttl` uses the process path as its own
scope and is `NON_CONFORMING`.

**OWL commitment:** the experimental class is a `prov:Entity` and is disjoint with
`res:ContinuationPath`. A BFO/IAO information-content alignment is not yet selected.

**Required SHACL:** one candidate, path, and scope per activated assessment; the scope must denote the
same path and must not collapse with an ontic or assessment node.

**Evidence requirement:** none for scope identity beyond record provenance; causal evidence belongs to
the claim layer.

## 3. `CausalAttributionClaim`

**Definition.** An epistemic information object whose subject/object fields express that an assessor or
method claims a causal relation between two named relata.

**Claim-record necessary conditions**

- Exactly one claim subject and object.
- At least one typed assessment method.

**Independent reported dimensions**

- `CLAIM_RECORD` checks only structural record well-formedness.
- `ONTIC_LINKAGE` checks whether the claim's relata match an explicit `res:causallyAttributedTo`
  assertion; absence is `INSUFFICIENT_DATA`, while an explicit conflicting target is `NON_CONFORMING`.
- `EVIDENCE_RECORD` checks whether at least one typed evidence record is cited.
- Domain evidence adequacy remains `DOMAIN_EVIDENCE_UNASSESSED` even when all three structural checks
  conform.

**Excluded interpretations**

- The ontic causal relation itself.
- Automatic assertion or inference of `res:causallyAttributedTo`.
- A guarantee that cited evidence is adequate.

**Positive example:** the claim in `fixtures/c-valid-overlay.ttl`.

**Counterexample:** `fixtures/claim-only-no-ontic-causation.ttl` is a conforming claim and evidence
record but has `INSUFFICIENT_DATA` for ontic linkage. It is representable as an unaccepted hypothesis.
`fixtures/claim-conflicting-linkage-overlay.ttl` is structurally conforming but `NON_CONFORMING` for
ontic linkage.

**OWL commitment:** `exp:causalSubject` and `exp:causalObject` deliberately have no ontic range axioms.
A claim assertion by itself must not infer `res:TraceContinuation` or `res:Interaction`. The mutation
gate M13 verifies this when the experimental vocabulary is loaded with the core.

**Required SHACL:** separate shapes for claim cardinality/method, evidence-record presence, and explicit
ontic linkage. No failure in the latter two retroactively makes the claim record malformed.

**Evidence requirement:** provenance, method, confidence, disagreement, and domain adequacy remain
claim-level concerns. This prototype only checks the first two structurally.

## 4. `res:causallyAttributedTo`

**Definition.** A published ontic relation asserting that a Trace continuation is causally attributable
to an Interaction. It remains distinct from a statement that somebody believes or reports this.

**Necessary conditions**

- Subject is an ontic Trace continuation and object is an Interaction under the published model.
- In the strict data profile, the named triple agrees with the path's declared origin.

**Excluded interpretations**

- A confidence score, assessor verdict, generic provenance influence, or evidence citation.
- A domain-independent procedure for discovering causation.

**Positive example:** `ex:trace res:causallyAttributedTo ex:origin` in the valid B fixture.

**Counterexample:** a matching `CausalAttributionClaim` without that named triple.

**OWL commitment:** `TraceContinuation ⊑ ∃ causallyAttributedTo.Interaction`. Consequently, typing a
node as `TraceContinuation` entails that some causal target exists, but it does not materialize a named
RDF triple or identify the target with the path's declared origin. This follows the existential
semantics of [OWL 2 Direct Semantics](https://www.w3.org/TR/owl2-direct-semantics/).

**Required SHACL:** explicit named-triple and origin-reference checks when deterministic graph-level
validation is requested.

**Evidence requirement:** a separate causal claim, method, and domain evidence are needed before any
epistemic support status is reported.

## 5. Causal lineage segment

**Definition.** A contextual role played by a Trace, Propagation, Selectivity, or outcome witness on the
declared causal spine of one path. It is not presently a new ontological class.

**Necessary conditions**

- Explicit registration by `exp:hasCausalSegment`.
- Participation in the required directed sequence.
- Distinctness from path, candidate, origin, receiver, and other role nodes under this bounded profile.

**Excluded interpretations**

- BFO occurrent parthood, temporal parthood, shared participant, or carrier continuity.
- Delay merely because Delay is another constitutive criterion.
- Transitive ancestry inferred from one direct edge.

**Positive example:** the four registered segment nodes in the valid B fixture.

**Counterexample:** the registered Transformation in
`fixtures/b-insufficient-unrelated-transformation.ttl` lacks its uptake-to-outcome edge.

**OWL commitment:** none in the published core. `exp:hasCausalSegment` is experimental profile
membership and is not aligned to BFO parthood.

**Required SHACL:** explicit registration, direction, cycle rejection, and linear-profile bounds.

**Evidence requirement:** the domain profile must say how each edge is established and at what
granularity it is considered direct.

## 6. Temporal continuation

**Definition.** A Delay witness whose interval has positive duration and a non-zero portion strictly
after the end of its referenced origin interaction. It may start before the origin ends.

**Necessary conditions**

- Exactly one `exp:temporallyQualifiesPath` target, equal to the path that carries the Delay witness.
- One Delay interval with one beginning and end.
- One origin interval end.
- `delayEnd > delayBegin` and `delayEnd > originEnd`.

**Excluded interpretations**

- A causal assertion.
- A rule requiring the Delay to begin after the origin ends.
- Success from a typed `PostInteractionContinuation` node without measurable bounds.

**Positive example:** the valid B fixture starts Delay at 10:30 while the origin ends at 11:00, and
ends Delay at 12:00.

**Counterexample:** `fixtures/b-invalid-delay-ends-at-origin-end.ttl` ends Delay exactly at 11:00.
`fixtures/b-invalid-unrelated-delay.ttl` has valid timestamps and a shared origin but explicitly
qualifies a different path. Both are `NON_CONFORMING`; a missing path link instead yields
`INSUFFICIENT_DATA`.

**OWL commitment:** the published class and `postInteractionOf` reference remain unchanged.
`exp:temporallyQualifiesPath` is an additive experimental property and does not make Delay a causal
segment. No interval inequality is expressible in the current OWL core.

**Required SHACL:** explicit OWL-Time interval paths and end-boundary comparison. The present
implementation accepts fixed-width UTC timestamps so lexical comparison is deterministic in the pinned
engine; an engine-neutral date-time comparison remains a release decision. See
[OWL-Time](https://www.w3.org/TR/owl-time/).

**Evidence requirement:** measured or otherwise justified time boundaries and a declared granularity.

## 7. Receiver-conditioned uptake

**Definition.** A downstream uptake/modulation whose occurrence or character depends on the same
receiver context reached by the propagation.

**Necessary conditions**

- Propagation identifies a receiver.
- Selectivity uses `res:uptakeDependsOn` with the same canonical receiver node.
- The causal spine links Propagation → Selectivity → outcome.

**Excluded interpretations**

- Mere co-presence of a receiver.
- An arbitrary receiver label shared only for convenience.
- Proof that the receiver condition is scientifically discriminating.

**Positive example:** the valid B fixture uses `ex:receiver` for both propagation and uptake dependence.

**Counterexample:** a different propagation and selectivity receiver, or a Transformation that is not
linked downstream of Selectivity.

**OWL commitment:** `ContextModulation` carries an existential `uptakeDependsOn.ReceiverContext`;
canonical equality with the propagation receiver remains a SHACL policy.

**Required SHACL:** explicit receiver-reference agreement and causal-spine adjacency.

**Evidence requirement:** a domain-specific comparison, intervention, mechanism, or other justified
method showing that uptake depends on the receiver condition rather than merely correlating with it.

## Linear-profile boundary

The profile evaluates one causal spine only. Any detected node with multiple in-profile causal
successors or predecessors sets applicability to `OUT_OF_SCOPE` with `OUT_OF_SCOPE_BRANCH_MERGE`. A
pure topology finding yields `NOT_EVALUATED`; simultaneous `VIOLATION_` or `MISSING_` findings remain
`NON_CONFORMING` or `INSUFFICIENT_DATA`. This does not deny that a branch or merge is a Resonatus
candidate; it says the initial profile has no branch/merge identity semantics.

The profile also does not impose BFO temporal `precedes` on causal edges. Overlapping upstream and
downstream processes remain representable, as mutation gate M14 verifies.
