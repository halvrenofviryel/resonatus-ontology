# Competency-Question Coverage Matrix

## Coverage rules

Competency questions are functional requirements, not a count of files. Following the original
competency-question methodology, coverage means that the representation and its axioms can answer the
intended question under an identified method. A structural ASK query can verify vocabulary structure; it
cannot substitute for temporal reasoning, causal evidence, or scientific validation.

Status vocabulary:

- `VERIFIED`: the current artefacts answer the intended formal question with an appropriate oracle.
- `PARTIAL`: some structure or synthetic behavior is tested, but a material part of the question is not.
- `DEMONSTRATED`: an authored example exhibits the intended result; this is not independent validation.
- `NOT_IMPLEMENTED`: the necessary representation or oracle is absent.
- `EMPIRICAL`: the decisive step requires real-world/domain evidence outside OWL and SHACL.

## Matrix

| # | Intended distinction | Required method | Existing implementation | Actual coverage | Missing test or research requirement |
|---:|---|---|---|---|---|
| 1 | Link a candidate trace process to an originating interaction. | OWL entailment plus causal-evidence policy. | CQ01 checks the `TraceContinuation` existential; R9 checks the path property chain to `hasOriginInteraction`. | `PARTIAL` | CQ01 does not itself connect candidate → path → origin, and neither check validates causation. Add an end-to-end entailment query after causal semantics are decided. |
| 2 | Represent a candidate without presupposing that it is already a causal trace. | OWL subclass/entailment tests. | CQ02 checks absence of candidate-to-causal-trace subsumption; R17 checks domain inference does not create a candidate. | `VERIFIED` | Preserve as a regression; add a positive candidate with no path only if a direct entailment test is desired. |
| 3 | Distinguish a persistent trace from an effect ending with the initiating interaction. | Temporal model plus causal evidence. | `negative_no_delay.ttl` omits the Delay witness and receives non-membership support. | `DEMONSTRATED`, `EMPIRICAL` | No intervals or end-boundary rule are evaluated. Create an OWL-Time/SHACL temporal profile and measured cases. |
| 4 | Represent Delay independently of Trace. | OWL structural and reasoner tests. | CQ04 checks no subsumption/subproperty; R8 verifies a Delay-only path is not a causal trace. | `VERIFIED` | This proves logical independence, not that the Delay witness is temporally valid. |
| 5 | Allow overlap with the interaction while requiring a non-zero post-end portion. | Interval arithmetic or SHACL over explicit temporal bounds. | `positive_overlap_delay.ttl` supplies a typed Delay witness but no temporal data. | `NOT_IMPLEMENTED` | Represent the origin and continuation intervals and test end/overlap conditions. |
| 6 | Represent propagation without requiring a cross-system boundary. | Conceptual definition, data fixtures at multiple boundary scales, and entailment/validation. | `PropagationEvent` is an unconstrained `prov:Activity`; positive examples attach one to a path. | `PARTIAL` | Define propagation's invariant and boundary independence; test same-system and cross-system cases. |
| 7 | Represent receiver/context-modulated downstream realization. | OWL restriction, SHACL receiver coherence, and empirical dependence evidence. | CQ07 checks `uptakeDependsOn some ReceiverContext`; SHACL equates the receiver with the propagation receiver. | `VERIFIED` structurally; `EMPIRICAL` causally | Add a contrast/intervention method showing that receiver context changes uptake. |
| 8 | Distinguish Transformation from Feedback while allowing either to satisfy criterion five. | OWL union/disjoint behavior and positive cases for both branches. | `ResonatusPath` uses a union of `hasTransformationEvent` and `hasFeedbackEvent`. Existing positive fixtures use Transformation. | `PARTIAL` | Add a Feedback-only case and decide whether the classes may overlap; define both beyond labels. |
| 9 | Distinguish generic causal trace process from full Resonatus. | OWL class entailment and near-miss fixtures. | CQ09 checks subclass structure; R7/R8 and other negatives separate partial paths from full paths. | `VERIFIED` formally | Scientific usefulness of the distinction remains unverified. |
| 10 | Avoid classifying a persistent but never-used log as Resonatus. | Domain evidence plus membership/classifier result. | `negative_static_log.ttl` records missing downstream positions and the aligned runner agrees. | `DEMONSTRATED`, `EMPIRICAL` | Validate “never used” and lack of causal uptake on independently observed data. |
| 11 | Distinguish FAIL, NOT_MEASURED, INCONCLUSIVE, and ERROR. | SHACL vocabulary validation plus classifier policy tests. | Verdict enumeration, invalid-verdict fixture, and reference classifier behavior. | `VERIFIED` as record policy | Add explicit unit cases for every mixed-verdict precedence combination if policy stability becomes critical. |
| 12 | Withhold positive membership support when a criterion is not established. | Separate OWL non-entailment and epistemic policy tests. | Five negative examples, unknown/inconclusive examples, and CL1/CL2 separation. | `VERIFIED` with scope caveat | OWL open-world non-entailment is not negation; keep “membership support” distinct from ontic membership. |
| 13 | Align provenance without equating provenance with causality. | Mapping inspection, consistency/conservativity tests, and causal-evidence policy. | Classes specialize `prov:Activity`; `hasOriginInteraction` specializes `prov:wasInfluencedBy`; R2 checks bridge consistency. | `PARTIAL` | Add a mapping-specific query and a counterexample showing generic PROV influence does not create Trace. |
| 14 | Use OWL-Time for temporal placement without treating order as causal proof. | Explicit time data, temporal validation, and negative causal-entailment test. | `hasTemporalExtent` ranges over `time:TemporalEntity`; no release fixture uses temporal relations. | `NOT_IMPLEMENTED` | Build the optional temporal profile and prove timestamps/order alone do not entail Trace. |
| 15 | Allow ODRL alignment without making normativity constitutive. | Optional mapping module and import-isolation test. | ODRL is mentioned/prefixed; no alignment axioms or fixture exist. | `NOT_IMPLEMENTED` | Create only when a normative use case supplies mappings; test that core membership is unchanged. |
| 16 | Represent immutable provenance with changed downstream significance. | Model of significance/context plus provenance identity and example query. | Transformation exists, but “significance” and immutable provenance are not represented. | `NOT_IMPLEMENTED` | Define the application-level distinction or remove/rewrite the CQ. |
| 17 | Represent two receivers with different context-modulated outcomes. | Multi-receiver data, outcome representation, query, and causal evidence. | Multiple contexts are syntactically possible; no outcome class/relation or fixture answers the question. | `NOT_IMPLEMENTED` | Add outcome semantics only after Selectivity's operational definition is approved. |
| 18 | Falsify each criterion independently. | Controlled counterexamples plus reasoner/classifier checks. | Five author-built omissions are exercised by `validate.py` and cross-layer/reasoner fixtures. | `VERIFIED` formally; not scientifically | Use independently constructed cases to test empirical independence and annotation leakage. |
| 19 | Keep direct continuation non-transitive. | OWL non-entailment test. | CQ19 and R3 test A→B, B→C without A→C entailment. | `VERIFIED` | Absence of a transitivity axiom is not a global non-transitivity assertion; wording already reflects this. |
| 20 | Keep causally connected Resonatus instances distinct unless identity is established. | OWL identity/difference tests and an explicit identity policy. | `directlyContinues` is asymmetric and irreflexive, so its asserted endpoints cannot be identical; no general CQ20 fixture exists. | `PARTIAL` | Define “causally connected,” test `sameAs`/`differentFrom`, and decide branch/merge identity. OWL has no unique-name assumption. |
| 21 | Classify Resonatus as BFO process only through an optional bridge. | Modular import test and DL consistency/satisfiability. | CQ21 and R2 verify the bridge and absence of the BFO commitment from core. | `VERIFIED` logically | Revisit `ContinuationPath` placement after its process-versus-scope meaning is decided. |
| 22 | Keep a real-system assessment undetermined when key criteria lack evidence. | Evidence audit plus classifier result. | The OpenAI Agents documentation-level example is `UNDETERMINED`. | `DEMONSTRATED` | It is author-constructed from documentation, not an independent empirical assessment. Obtain a real-system study with traceable evidence. |

## Summary by method

| Method | Questions primarily covered | Main limitation |
|---|---|---|
| Structural SPARQL | 1, 2, 4, 7, 9, 19, 21 | Checks schema patterns, not all intended runtime/empirical distinctions. |
| OWL entailment/non-entailment | 1, 2, 4, 8, 9, 12, 18, 19, 20, 21 | Open-world non-entailment is not factual falsity; typed witnesses may be semantically weak. |
| SHACL validation | 7, 11, 12, 18 | Checks supplied graph structure and limited co-reference, not causal truth. |
| Reference classifier | 10, 11, 12, 18, 22 | Implements reporting policy over explicit verdicts; it does not infer evidence. |
| Temporal/empirical method | 3, 5, 6, 7, 10, 14, 17, 22 | Mostly absent or demonstrated only with authored labels. |
| Conceptual/identity analysis | 6, 8, 13, 15, 16, 20, 21 | Requires owner decisions before a valid formal oracle exists. |

Counting each question once at its strongest current status gives:

- `VERIFIED`: 8 questions (2, 4, 9, 11, 12, 18, 19, 21), with the scope qualifications above;
- `PARTIAL`: 6 questions (1, 6, 7, 8, 13, 20);
- `DEMONSTRATED` but not independently verified: 3 questions (3, 10, 22);
- `NOT_IMPLEMENTED`: 5 questions (5, 14, 15, 16, 17).

This classification is more informative than either `7/7` or `7/22`: executable file count and actual
competency coverage are different measures.

## Recommended maintenance rule

Every competency question should carry four independent fields in future documentation:

1. representation status;
2. oracle/method;
3. automated regression status;
4. empirical validation status.

A new query should be added only when it answers the intended question with an appropriate oracle. A
query that merely finds the expected vocabulary must not upgrade an empirical or temporal question to
“verified.”

## Sources

- [Grüninger and Fox 1995, The Role of Competency Questions in Enterprise Engineering](https://doi.org/10.1007/978-0-387-34847-6_3)
- [W3C SHACL validation model](https://www.w3.org/TR/shacl/#validation)
- [OWL 2 Direct Semantics](https://www.w3.org/TR/owl2-direct-semantics/)
- [W3C OWL-Time](https://www.w3.org/TR/owl-time/)
- [W3C PROV Data Model](https://www.w3.org/TR/prov-dm/)
