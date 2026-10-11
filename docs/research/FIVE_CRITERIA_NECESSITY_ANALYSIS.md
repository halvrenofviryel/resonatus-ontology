# Five-Criteria Necessity Analysis

## Scope

This document evaluates the current five-position definition without changing it:

```text
Trace ∧ Delay ∧ Propagation ∧ Receiver-conditioned Selectivity
      ∧ (Transformation ∨ Feedback)
```

The existing reasoner fixtures establish *formal separability*: omitting each position can prevent an
OWL membership entailment. That is not the same as scientific necessity, conceptual independence, or
empirical discriminating power.

## Criterion-by-criterion analysis

| Criterion | Current formal condition | What the condition actually verifies | Necessity and independence | Granularity sensitivity | Finding |
|---|---|---|---|---|---|
| Causal Trace | The path has some `TraceContinuation`; every such continuation has some `causallyAttributedTo Interaction`. | An ontic causal property assertion is present. It does not verify the evidence or mechanism behind causation. | Necessary by definition. Conceptually overlaps with Propagation if “trace continuation” already means a transmitted effect. | Changes with the chosen origin interaction and causal model. | `SEMANTIC_AMBIGUITY` about ontic fact versus causal claim. |
| Delay | The path has some typed `PostInteractionContinuation`; optional `postInteractionOf` is checked for reference agreement by SHACL. | Presence of a typed witness. It does not verify a non-zero portion after the interaction end. | Formally independent of Trace. Scientific independence is plausible but untested. | Highly sensitive to where the initiating interaction is said to end. | `VERIFIED_ERROR` between temporal prose and formal semantics. |
| Propagation | The path has some typed `PropagationEvent`. A receiver reference is required only by the full-path SHACL completeness rule. | Presence of an activity labelled propagation and a receiver reference. No transfer, movement, causal downstreamness, or carrier continuity is required. | May duplicate Trace or ordinary causal downstreamness unless propagation is operationally defined. | Sensitive to spatial, system, agent, and state boundaries. | `SEMANTIC_AMBIGUITY`. |
| Receiver-conditioned Selectivity | The path has a `ContextModulation` whose `uptakeDependsOn` some `ReceiverContext`; SHACL equates that context with the propagation receiver. | A dependency assertion and node co-reference. No comparison, intervention, alternative receiver, or observed outcome is required. | Potentially discriminating, but nearly every realized effect may depend on context at some level. It needs a contrast class and threshold. | Strongly sensitive to how finely context is described. | `SCIENTIFIC_UNCERTAINTY`. |
| Transformation or Feedback | The path has a typed `TransformationEvent` or `FeedbackEvent`. | Presence of a class assertion; both classes otherwise carry no defining restrictions. | The disjunction may be too broad. Transformation could accompany almost every propagation; feedback is conceptually different from transformation. | Sensitive to description level and what counts as a changed form, significance, policy, or state. | `SEMANTIC_AMBIGUITY` and `SCIENTIFIC_UNCERTAINTY`. |

## Formal necessity versus scientific necessity

The five negative fixtures show the following conditional fact:

> Given the v1.0.0 equivalence axiom, and given data constructed with one required existential absent,
> the reasoner does not entail `Resonatus`.

They do not show:

- that a real persistent causal phenomenon must satisfy all five positions;
- that experts can apply the positions reliably;
- that the positions are mutually independent in measured data;
- that the conjunction separates a stable scientific kind from ordinary causal processes;
- that the fifth disjunction improves classification;
- or that the chosen interaction and process granularity leave the result invariant.

The examples were designed from the definition and are appropriate regression fixtures, not an
independent validation sample.

## Redundancy hypotheses

These are hypotheses to test, not conclusions.

### H1 — Trace may subsume part of Propagation

If a Trace is “a later state, difference, representation, disposition, or process portion causally
attributable to an interaction,” then some notion of effect transmission or persistence is already
present. Propagation adds value only if it requires a change of location, bearer, state, receiver, or
causal stage that Trace alone does not require. The current `PropagationEvent` axioms do not specify
which.

### H2 — Delay may be a thresholded form of persistence

Delay is meaningful if it distinguishes effects confined to the origin interaction from effects with a
non-zero post-origin portion. Its truth changes when the origin interaction is individuated more broadly
or narrowly. A robustness study must vary that boundary rather than assume one annotation.

### H3 — Selectivity may be ubiquitous without a contrast

Every effect depends on some receiving conditions. Selectivity becomes discriminating only if the model
states which receiver features matter and shows that relevant alternatives yield different uptake. One
`uptakeDependsOn` assertion is a commitment, not a test of counterfactual or comparative dependence.

### H4 — Transformation may make the fifth position nearly vacuous

At a sufficiently fine description level, most propagation changes some state or representation.
Feedback is structurally stronger because a downstream stage influences an upstream process, but the
current disjunction allows the weaker Transformation branch. Operational thresholds are needed before
the fifth position can be shown to discriminate.

## Independently constructed probes

These probes were chosen after the formal model was inspected. They are not added as positive or negative
fixtures because their correct labels require domain evidence.

| Probe | Expected pressure on the five positions | What would decide the case |
|---|---|---|
| A healed scar caused by an injury | Clear origin and persistence; possible local propagation; receiver-conditioned selectivity and transformation depend on granularity. | Biological mechanism, chosen process boundary, and whether tissue remodelling counts as propagation. |
| A cryptographic audit log copied to cold storage and never read | Trace-like record, delay, and propagation by copying; no downstream uptake or feedback. | Evidence of actual use and causal effect, not mere storage. |
| A prion conformation spreading through susceptible cells | Strong candidate for persistence, propagation, receiver dependence, and transformation. | Molecular lineage and controls showing conformation-dependent uptake; compare existing biological-process terms. |
| A policy changed after an incident report | Plausible cross-bearer propagation and changed significance; causal attribution can be contested. | Decision provenance, counterfactual/process-tracing evidence, and explicit transformation semantics. |
| A thermostat pulse that triggers a controller but leaves no state after the pulse | Trace and propagation may occur without Delay under a narrow origin boundary. | High-resolution timing and a declared boundary rule. |
| A learned model update later affecting a different input | Persistence and selective downstream effect are plausible; identity of “the same trace” across parameters and executions is unclear. | Intervention/ablation, carrier identity, and a domain-specific lineage profile. |
| A shadow moving across a wall | Apparent propagation and transformation without a transmitted causal process in classical causal-process accounts. | A domain causal model distinguishing a pseudo-process from energy/information transfer. |

The probes are useful precisely because reasonable experts may disagree. Agreement produced only after
showing annotators the five-condition definition would test instruction following, not category validity.

## Alternative classifications to compare

The v1.0.0 model should be compared against nested alternatives rather than assumed optimal.

| Model | Conditions | Research purpose |
|---|---|---|
| M1 | Trace only | Baseline: any causally attributed continuation. |
| M2 | Trace + post-origin persistence | Tests whether Delay captures most of the intended distinction. |
| M3 | Trace + persistence + propagation | Adds lineage movement without selectivity. |
| M4 | Trace + persistence + receiver-conditioned uptake | Merges propagation/selectivity into one downstream-uptake condition. |
| M5 | Current five-position model | Tests incremental value of separate Propagation and Transformation/Feedback. |
| M6 | Graded profile | Reports the five positions without defining a necessary-and-sufficient ontological class. |

For each model, compare inter-annotator agreement, stability under granularity changes, predictive or
explanatory value in the application, and disagreement with domain-expert gold labels. M6 is important:
the criteria may be useful dimensions even if they do not jointly define a natural kind.

## Recommended study design

1. Pre-register operational definitions and boundary rules for each domain.
2. Recruit domain experts who did not construct the ontology.
3. Supply cases without revealing the intended Resonatus label.
4. Ask experts first for causal structure and evidence, then compute each model's classification.
5. Include near-miss and adversarial cases, branches, merges, latent persistence, and different
   interaction granularities.
6. Measure criterion agreement and conditional dependence; compare M1–M6 rather than only M5 accuracy.
7. Record whether disagreement concerns evidence, category meaning, or process individuation.
8. Revise the constitutive definition only after the owner reviews those results.

## Decision

No criterion should be removed, merged, or strengthened in the normative ontology at this stage. The
current five positions are suitable as a falsifiable research hypothesis and assessment profile. They
are not yet justified as necessary and sufficient conditions for a scientifically distinct process
category.

## Sources

- [Dowe 1995, Causality and Conserved Quantities](https://doi.org/10.1086/289859)
- [OBO Relation Ontology causal-relation distinctions](https://oborel.github.io/obo-relations/causal-relations/)
- [W3C OWL-Time](https://www.w3.org/TR/owl-time/)
- [Rovetto and Mizoguchi 2015, Causality and the Ontology of Disease](https://doi.org/10.3233/AO-150147)
- [Grüninger and Fox 1995, The Role of Competency Questions in Enterprise Engineering](https://doi.org/10.1007/978-0-387-34847-6_3)
