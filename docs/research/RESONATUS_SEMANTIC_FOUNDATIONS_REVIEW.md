# Resonatus v1.1 Semantic Foundations Review

**Status:** research review for owner decision

**Date:** 2026-10-11
**Normative changes made:** none

## Executive conclusion

Resonatus v1.0.0 is a coherent OWL/SHACL artefact for recording a five-position assessment profile,
but it does not yet formally identify a single causal continuation or establish that the five positions
define a scientifically distinct process kind. The strongest defensible reading today is:

> A `Resonatus` is a process selected as a candidate and linked to a scope node on which five typed
> witnesses are recorded, with limited origin and receiver reference agreement checked by SHACL.

The stronger reading used in parts of the documentation—one coherent causal lineage persisting from an
origin through propagation, selective uptake, and transformation or feedback—is not entailed by the
current axioms. This is a verified formal gap, not an inference from the editorial decision.

The model nevertheless contains design decisions worth preserving: ontic and epistemic layers are
separate; the path reification prevents cross-path witness mixing; a candidate does not presuppose
membership; generic PROV influence is kept weaker than causal attribution; and the BFO commitment is an
optional bridge. These provide a sound base for a v1.1 decision, but not evidence that Resonatus is
already a novel natural or scientific kind.

## Finding classification

The labels below have the meanings required for this review:

- `VERIFIED_ERROR`: a reproducible mismatch between a stated guarantee and the formal semantics.
- `SEMANTIC_AMBIGUITY`: more than one materially different interpretation is consistent with the model.
- `DESIGN_TRADEOFF`: the current choice is coherent but has explicit costs.
- `SCIENTIFIC_UNCERTAINTY`: ontology engineering alone cannot settle the question.
- `NO_CHANGE_REQUIRED`: the current decision is supported for the stated scope.

| ID | Classification | Finding | Evidence | Smallest valid correction | Entailment consequence |
|---|---|---|---|---|---|
| F01 | `VERIFIED_ERROR` | “One coherent causal path” is stronger than the axioms. The model requires five witness types on one path node, not causal, temporal, mereological, or participation links among those witnesses. | CE01 entails `Resonatus` and SHACL-conforms with no lineage edges among the five witnesses. | Until lineage is formalized, call the guarantee “single-scope witness co-location plus origin/receiver reference coherence.” | Documentation-only correction changes no entailments. A real lineage constraint would reject some current positives. |
| F02 | `VERIFIED_ERROR` | Delay is described as a non-zero continuation after the origin interaction ends, but `PostInteractionContinuation` has no temporal restriction. `postInteractionOf` is only a primitive reference. | CE02 uses one self-linked individual as both origin and post-interaction continuation and remains consistent, entailed, and SHACL-conformant. | Define an executable temporal evidence/profile rule before claiming that the ontology verifies post-interaction timing. | A normative temporal constraint could reject existing fixtures that provide typed witnesses without intervals. |
| F03 | `SEMANTIC_AMBIGUITY` | `causallyAttributedTo` is described both as an ontic causal commitment and as an “asserted” relation. In OWL, an object-property assertion is true in every model of the ontology; it is not a reified claim with confidence or provenance. | OWL 2 Direct Semantics for `ObjectPropertyAssertion`; current `TraceContinuation` existential restriction. | Decide whether the property denotes real causation or a causal claim. If ontic, keep evidence/claim metadata separate and remove epistemic wording. If claim-like, reify it outside the direct ontic property. | The claim-like option changes membership triggers and therefore requires migration and owner approval. |
| F04 | `SEMANTIC_AMBIGUITY` | `ContinuationPath` is simultaneously documented as an ontic process and used structurally as a grouping/scope node. No relation says its witnesses are occurrent or temporal parts, participants, stages, or effects of that process. | Core axioms, BFO bridge, CE01. | Choose “process” or “assessment scope/bundle” as the primary meaning. If it is a process, add justified process-structure relations; if it is a scope, reconsider the BFO process mapping. | Either choice can affect BFO placement and current path entailments. |
| F05 | `DESIGN_TRADEOFF` | `ResonatusCandidate` is an ontic `prov:Activity`, not a hypothesis or assessment record. This is coherent because the separate `ResonatusAssessment` carries epistemic status, but the word “candidate” can obscure the commitment. | Core subclass axiom and optional BFO bridge. | Preserve the axiom; explicitly define candidate as “a process selected for assessment.” | No entailment change. |
| F06 | `NO_CHANGE_REQUIRED` | The weak PROV-O alignment is directionally appropriate: PROV activity is process-like and `wasInfluencedBy` is broader than causation. It must not be cited as causal proof. | W3C PROV-DM/PROV-O and the published PROV-O–BFO mapping. | Keep the alignment optional and weak; add conservativity tests if the bridge is expanded. | No current change. |
| F07 | `DESIGN_TRADEOFF` | Mapping `ContinuationPath` to BFO process is consistent but not sufficient to show that the node is a genuine process. BFO process semantics presuppose temporal parts and dependence on material entities; the core does not represent those commitments. | BFO 2020 definitions and CE01/CE02. | Retain provisionally, but mark it as conditional on resolving F04. | No current change; future remapping may alter upper-level classification. |
| F08 | `SCIENTIFIC_UNCERTAINTY` | The necessity, independence, and empirical discrimination of the five criteria have not been established on independently constructed cases. | Existing fixtures are author-designed and mirror the definition. | Run a blinded multi-domain annotation study and compare nested alternative models. | No current entailment change. |
| F09 | `NO_CHANGE_REQUIRED` | OWL membership, SHACL record conformance, and epistemic classification are correctly treated as different outcomes. | CL1–CL4 and the revised runners. | Preserve this separation. | No change. |
| F10 | `VERIFIED_ERROR` | Several competency questions currently exceed their executable or represented coverage, especially temporal overlap, ODRL alignment, changed significance, receiver-specific outcomes, and general identity preservation. | The 22-question matrix in this review. | Mark each question by method and coverage; do not count documentation or a typed witness as verification. | No ontological change; prevents invalid assurance claims. |

## Ontological commitments

### ContinuationPath

The class is causally neutral in the narrow formal sense: being a `ContinuationPath` does not entail
`CausalTraceProcess`. That decision is coherent and should be preserved. The unresolved issue is not
neutrality but category: a node can be a neutral process, yet the current restrictions use it only as the
subject of “has witness” relations. Nothing makes those witnesses parts or stages of the process.

### ResonatusCandidate

The core commits every candidate to being a `prov:Activity`; the optional bridge further commits it to
BFO `process`. This is not a contradiction if the candidate denotes the real process under assessment.
It would be a category error only if applications use the candidate IRI for a record, proposition, plan,
or possible process. The minimal response is a usage rule, not a new class.

### Causal attribution

The intended relation must be fixed before v1.1 axioms are designed:

1. **Ontic reading:** `t causallyAttributedTo i` states that `i` actually causes `t`. Evidence and method
   justify the assertion but are not its semantics.
2. **Claim reading:** the triple records that some assessor attributes `t` to `i`; it may be uncertain or
   contested.

The current direct OWL property implements the ontic reading, while the word “asserted” and the absence
of a domain-independent warrant invite the claim reading. Mixing these readings lets an unqualified RDF
triple create an ontic Trace commitment. Owner decision D02 is therefore required.

### PROV-O and BFO

`prov:Activity` is defined as something occurring over time and acting upon or with entities. The 2025
PROV-O–BFO alignment maps it to BFO process, so the candidate and interaction mappings have external
support. `prov:wasInfluencedBy`, however, is a generic dependency; specializing a causal origin relation
under it is safe only in the causal-to-influence direction. Neither PROV-O nor logical consistency proves
that a particular path is causally continuous.

## Scientific uncertainties

1. Whether post-interaction persistence and propagation are independent in real applications.
2. Whether receiver-conditioned selectivity is discriminating rather than true of nearly all realized
   effects once context is described richly enough.
3. Whether transformation/feedback adds a stable boundary or merely redescribes ordinary causal change.
4. Which interaction boundary and process granularity make Delay and Propagation invariant enough for
   cross-domain comparison.
5. Whether branches and merges preserve one path identity, create new paths, or require a lineage graph.
6. Whether the profile predicts expert classifications better than simpler two- or three-condition models.

These cannot be resolved by adding OWL axioms without prior conceptual and empirical decisions.

## Design decisions worth preserving

- Keep the v1.0.0 release and checksum manifest frozen.
- Keep assessment verdicts separate from ontic facts.
- Keep `ContinuationPath` causally neutral at the genus level.
- Keep path reification as a scoping device; it already blocks witness mixing across several path nodes.
- Keep PROV influence weaker than causal attribution.
- Keep the BFO bridge optional.
- Keep `directlyContinues` non-transitive unless a specific closure relation is separately required.
- Keep exact SHACL violation assertions and distinct reasoner failure outcomes.

## Minimal recommended v1.1 changes

No item below has been applied.

1. Correct documentation and the architecture caption so “coherent path” does not exceed the current
   single-scope/co-reference guarantee. Add `assesses`, state that `hasTracePath` does not impose an
   existential on every candidate, and say that `PathCoherenceShape` does not prove a causal chain.
2. Decide the ontic-versus-claim reading of `causallyAttributedTo`.
3. Choose a path identity policy for sequence, branch, merge, and termination before adding relations.
4. Specify Delay as a testable temporal condition, probably in an optional OWL-Time/SHACL profile rather
   than by pretending OWL alone discovers temporal evidence.
5. Evaluate whether existing BFO/RO relations such as occurrent parthood and causal-upstream relations
   can express the chosen lineage before minting Resonatus-specific relations.
6. Treat the five criteria as a provisional classification profile until independent comparison against
   simpler models is complete.
7. Adopt the competency-question matrix as the coverage contract and implement only questions with a
   meaningful formal oracle.

## Changes requiring owner approval

- Any change to the five-condition necessary-and-sufficient definition.
- Any disjointness between candidate, path, interaction, receiver, and witness classes.
- Any temporal cardinality or ordering rule for Delay.
- Any causal-chain, parthood, participation, or lineage relation used in membership.
- Any reinterpretation or reification of `causallyAttributedTo`.
- Any change to the BFO placement of `ContinuationPath`.
- Any switch from ontological class to assessment/profile positioning.

See `V11_OWNER_DECISION_REGISTER.md` for explicit alternatives and consequences.

## Does Resonatus provide a defensible distinction beyond established process ontologies?

**Not yet as a demonstrated ontological kind.** The combination of post-origin persistence,
propagation, receiver-sensitive uptake, and transformation/feedback is a potentially useful application
profile. The current formalization, however, does not supply a process-identity criterion, a causal
lineage, or independent evidence that all five conditions are necessary and jointly discriminating.
Established resources already supply processes, temporal parts, generic influence, temporal ordering,
and causal-upstream relations. Resonatus' possible contribution is the *particular cross-domain
selection and assessment policy* built from these ideas, not yet a proven new basic category.

A defensible near-term position is therefore:

> Resonatus is a provisional applied-ontology profile for evaluating persistent, propagated, and
> context-sensitive causal continuations, with a hypothesis that the five-condition conjunction marks a
> useful subtype. The hypothesis remains open to simplification or rejection.

## Preserved pre-review working-tree state

The following snapshot was taken before this semantic-review directory was added.

- Repository: `https://github.com/halvrenofviryel/resonatus-ontology.git`
- Branch: `main`
- Base commit: `119e89d127df6f9431dd22d344175a8476dfb6a6`
- Tracked binary diff stream: `git diff --binary`
- SHA-256 of that exact tracked diff stream:
  `303199efe1b9d0d4b4fa8acf028de0d1757aeb11b93bbb23a715faf4ed94867a`
- Modified tracked files: 14; untracked files: 5; old v0.4 checkout remained clean.

### Modified tracked files and captured content hashes

| File | SHA-256 |
|---|---|
| `CHANGELOG.md` | `09037fe8e5fec184d0565327f191739f6adbbec7a58d3be34e3d781e862e0bd0` |
| `DESIGN_RATIONALE.md` | `c7204c889f88442d9cccd9162bf1e2fadfca9c517dd8e53c5ac9bcf49afe9bac` |
| `FORMAL_VERIFICATION_REPORT.md` | `27f70865eb01f0fbdb1ffb1064fa6dc4b5c3b7cdbf7f541492ad5eb55dda3c82` |
| `README.md` | `c08e3e51357443c5778288f1b0079d220ebec7f8533d2e4aab2c12b9458ae3ee` |
| `docs/figures/resonatus-architecture-figure.png` | `ca5cd8d9e8665d20475cfa760ad8e29a764aa19494cc67591b446e952ebc49a5` |
| `docs/figures/resonatus-architecture-figure.svg` | `c7f75f3a3696b74c06196d8e9cbbb9a08e211a5858b4a8511651b806538f7032` |
| `scripts/run_example_crosslayer.py` | `cf44e858680729329752662a7bfc338fed01c9114f8471b54f79bebb1b6cda88` |
| `scripts/run_shacl_gates.py` | `fe4b2e42776137ea1454db1b4939a13964bd78121ebe6f1d2f302db8a0ec0f13` |
| `tests/reasoner-release-gates.md` | `c505df55acb79ac117fe342a511459690c27c8bcfa8dab3b6f8af090ad9d89b6` |
| `tests/shacl/duplicate-criterion.ttl` | `f0d76227f2174b3064e7b7090dcaee42b7eee703b1b7bee871fff64ce3fd90f6` |
| `tests/shacl/invalid-verdict.ttl` | `fcaaa738093565b9527311e29cfc240d75fb323782b6edffb34d5d28c35b9906` |
| `tests/shacl/missing-criterion.ttl` | `df79473c0ccbad10a92f8c6e89afcb07b42efbccf545a6d3a7032deaadf9be07` |
| `tests/shacl/two-assessed-candidates.ttl` | `38894ea10bea37fae0425f5c958542a99247b0620ab69ea914bf320f2ac164bb` |
| `tests/shacl/wrong-assessed-candidate.ttl` | `9f2f2a072c87537155fba3d970e356f7aaab1e00307b2fe7076bd5ec903aa6ff` |

### Untracked files and captured content hashes

| File | SHA-256 |
|---|---|
| `docs/figures/resonatus-architecture-figure.dot` | `2668999833f86623826617bf3d8ab3e21a3b5ce20b4ad324c02b2c68b7a88ee2` |
| `docs/review-feedback-remediation-2026-10-11.md` | `eba4f1cc973b3741e9bef1a3016d2ba0b9c0659cc52eea69ee21b69f26f9c6d0` |
| `tests/crosslayer/epistemic-supported-ontic-not-entailed.ttl` | `e8d097a1415dffac0314f1c8f66c1805313169d8e0fa00102d57bcf394d9e327` |
| `tests/crosslayer/ontic-positive-epistemic-undetermined.ttl` | `2ce4bf3c1260cf0d332115339b6967b17a3f6e0c557e4bb579ac41c28c237118` |
| `tests/shacl/path-r26-targetclass-subclass.ttl` | `af77a038dd603cf5a67c1791160bb259158d56263087172cb89959d69a15f088` |

### Test environment and latest outputs at capture

- Python `3.12.3`
- RDFLib `7.6.0`
- pySHACL `0.40.1`
- Owlready2 `0.51`
- OpenJDK `21.0.12.1`
- Turtle parse: `47 files: OK`
- Reference classifier: `13/13`
- SHACL gates: all pass, R18–R26
- Cross-layer: aligned `13/13`, independence `2/2`, inconsistency guard PASS, execution-error guard PASS
- OWL reasoner gates: R2–R17 all pass
- Executable competency queries: `7/7` existing queries, representing `7/22` documented questions
- Structural audit: `13/13`
- Wording lint and Python compilation: PASS
- `git diff --check`: PASS

Passing these checks establishes regression behavior, not scientific validity.

## Reproducible counterexample results

Commands:

```bash
python scripts/reason_check.py \
  docs/research/counterexamples/ce01-grouped-witnesses-no-lineage.ttl candidate Resonatus
python scripts/reason_check.py \
  docs/research/counterexamples/ce02-single-node-collapse.ttl collapsed Resonatus
```

Observed with the captured environment:

| Counterexample | HermiT | pySHACL, inference none |
|---|---|---|
| CE01 grouped witnesses, no lineage | `Resonatus=True`; `path` inferred `ResonatusPath` | conforming, 0 violations |
| CE02 single-node collapse | `Resonatus=True`; `collapsed` inferred `ResonatusPath` | conforming, 0 violations |

## Sources

- [OWL 2 Direct Semantics: assertion satisfaction](https://www.w3.org/TR/owl2-direct-semantics/#Assertions)
- [W3C PROV Data Model](https://www.w3.org/TR/prov-dm/)
- [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- [W3C OWL-Time](https://www.w3.org/TR/owl-time/)
- [BFO 2020 official repository and OWL artefacts](https://github.com/BFO-ontology/BFO-2020)
- [Prudhomme et al. 2025, PROV-O to BFO mapping](https://doi.org/10.1038/s41597-025-04580-1)
- [Borgo et al. 2022, DOLCE](https://doi.org/10.3233/AO-210259)
- [Garbacz et al., Two Approaches to the Identity of Processes in BFO](https://ceur-ws.org/Vol-3637/paper33.pdf)
- [Rovetto and Mizoguchi 2015, Causality and the ontology of disease](https://doi.org/10.3233/AO-150147)
- [OBO Relation Ontology: causal relations](https://oborel.github.io/obo-relations/causal-relations/)
