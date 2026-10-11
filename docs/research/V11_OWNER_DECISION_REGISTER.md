# Resonatus v1.1 Owner Decision Register

**State:** OWNER RESEARCH DIRECTION RECORDED — no normative change in this register has been approved or
applied.

## How to use this register

The owner recorded the v1.1 research direction on 2026-10-11. A recorded direction authorizes bounded,
non-normative prototyping; it is not authorization to edit the core ontology, normative SHACL, or
release artefacts. D01–D08 still require a separate normative approval after prototype review. D09–D11
record choices to preserve.

| ID | Decision | Options | Recommendation | Why | Consequences | Status |
|---|---|---|---|---|---|---|
| D01 | What does `ContinuationPath` primarily denote? | A: real process; B: structural scope/bundle; C: core scope with domain process profiles; D: preserve path as process and model assessment scope separately. | **D: prototype ontic process and distinct assessment scope.** Do not silently change the published IRI's meaning. | The current prose and BFO bridge intend a process; a scope information object has a different ontological role. | Requires candidate scope class/relations and migration analysis before adoption. | `OWNER_RESEARCH_DIRECTION; NORMATIVE_APPROVAL_REQUIRED` |
| D02 | What does `causallyAttributedTo` mean? | A: real ontic causal relation; B: assessor's causal claim; C: maintain both as separate constructs. | **C**, with the direct property reserved for A and a separate claim object for B. | OWL object-property assertions are ontic in the model; evidence, confidence, and disagreement belong to a claim/assessment layer. | Requires exact claim semantics and a migration design; existing triples must not silently change meaning. | `OWNER_RESEARCH_DIRECTION; NORMATIVE_APPROVAL_REQUIRED` |
| D03 | What establishes one lineage? | A: shared origin; B: ordered causal links; C: process parthood; D: tracked carrier/participant; E: common minimum plus domain evidence profiles. | **E: common directed lineage semantics plus domain-specific evidence profiles.** | Shared origin is insufficient, while evidence methods differ legitimately by domain. | Membership becomes stronger and some current positives may cease to qualify. | `OWNER_RESEARCH_DIRECTION; NORMATIVE_APPROVAL_REQUIRED` |
| D04 | How do branch and merge affect path identity? | A: identity follows origin; B: every branch creates a new path; C: lineage graph with explicit branch/merge policy; D: domain-specific. | **C**, a directed causal segment graph with explicit domain constraints. | Origin-only identity collapses divergent effects; always-split is too rigid for feedback and recombination. | Requires branch/merge fixtures, identity tests, and likely a distinction between path and segment. | `OWNER_RESEARCH_DIRECTION; PROTOTYPE_INCOMPLETE` |
| D05 | Where should Delay be validated? | A: OWL core; B: optional OWL-Time/SHACL profile; C: external assessment only. | **B**, as a separate optional temporal validation profile. | The intended non-zero post-end condition is closed-world/data-sensitive and not present in the core. | Domains without interval data cannot claim temporal-profile conformance. | `OWNER_RESEARCH_DIRECTION; BOUNDED_PROTOTYPE_RESULT_AVAILABLE` |
| D06 | Are the five positions constitutive of an ontological class? | A: retain necessary-and-sufficient class; B: treat as graded assessment dimensions; C: provisional class plus explicit research status. | **No change at this stage.** | Formal separability is established; scientific necessity and discrimination are not. | Later evidence may support the current definition, simplify it, or favor a graded profile. | `HOLD_NO_CHANGE; SCIENTIFIC_EVIDENCE_REQUIRED` |
| D07 | How should `Transformation ∨ Feedback` be handled? | A: keep disjunction; B: require Feedback; C: operationally define Transformation; D: split into profiles. | **No change at this stage.** | Transformation is currently unconstrained and may be nearly universal at fine granularity. | Define and test both branches before any strengthening. | `HOLD_NO_CHANGE; SCIENTIFIC_EVIDENCE_REQUIRED` |
| D08 | What is the public positioning of Resonatus? | A: novel process kind; B: applied ontology profile; C: vocabulary plus assessment framework. | **B/C now**; reserve A for later evidence. | Current model has a potentially useful selection/profile but no demonstrated identity criterion or independent validation. | Public claims must distinguish formal profile utility from a scientifically established new process kind. | `OWNER_RESEARCH_DIRECTION; PUBLICATION_CHANGE_NOT_APPLIED` |
| D09 | Should ontic membership and epistemic support remain separate? | A: separate; B: merge. | **A** | CL1–CL2 show both disagreement directions are coherent and useful. | Preserve current runners and wording. | `PRESERVE` |
| D10 | Should the BFO commitment remain optional? | A: optional bridge; B: import into core. | **A** | The path category remains unresolved; optionality avoids forcing an upper-ontology choice on all users. | Continue bridge consistency tests; revisit only after D01. | `PRESERVE` |
| D11 | Should v1.0.0 release artefacts be rewritten? | A: freeze; B: rewrite. | **A** | Published tags, DOI artefacts, reports, and checksums are historical records. | Put all new work under Unreleased/v1.1 research until an approved release. | `PRESERVE` |

## Proposed approval sequence

1. Approve D08 public positioning.
2. Resolve D01 and D02, because path category and causal-property semantics constrain all later choices.
3. Resolve D03–D05 with minimal prototype profiles and the two counterexamples.
4. Run the independent five-criteria study before resolving D06–D07.
5. Convert approved choices into an implementation plan with explicit migration and entailment-delta tests.

## Prototype evidence recorded after owner direction

The bounded A/B/C experiment is documented in
[`prototypes/v11/PROTOTYPE_COMPARISON_REPORT.md`](prototypes/v11/PROTOTYPE_COMPARISON_REPORT.md). It
shows that an additive strict profile can reject CE01 and CE02 while a coherent directed example passes,
without changing the v1.0.0 OWL entailments. This satisfies the immediate prototype acceptance test; it
does not settle branch/merge identity, domain evidence sufficiency, or authorize normative adoption.

The final bounded hardening pass expands this to 15/15 scenario gates, 27/27 mutation gates, and 26/26
combined OWL-module integration checks; see
[`prototypes/v11/STRICT_PROFILE_HARDENING_REPORT.md`](prototypes/v11/STRICT_PROFILE_HARDENING_REPORT.md).
It separates profile applicability from validation, binds Delay to the path it qualifies, separates
claim-record validity from ontic linkage and evidence-record presence, detects vacuous-target risks,
and distinguishes named ontic triples from OWL existential commitments. The engineering recommendation
is `CONDITIONAL GO` for preparing a release candidate only; owner approval remains required before any
production term or profile is published.

## Local RC preparation direction recorded on 2026-10-11

The owner subsequently authorized a **local-only** `1.1.0-rc.1` package under `profiles/v1.1-rc/` for
inspection, with the following bounded choices:

- provisional namespace `https://w3id.org/resonatus/strict#`;
- new causal-edge name `strict:hasCausalNextStage` and retained Delay binding name
  `strict:temporallyQualifiesPath`;
- optional Strict Linear and Strict Assessment profile identifiers;
- only the role distinctions needed by the bounded profile, without a broad new global class
  disjointness regime;
- canonical UTC-second timestamps with value-based comparison;
- no new research cycle and no change to the published core, default shape, manuscript, tag, release,
  DOI deposit, or public namespace configuration.

This direction authorizes RC engineering only. The candidate identifiers remain provisional and the
package must retain `NO-GO` publication status until a separate release decision.

## Post-RC blocker status recorded on 2026-10-11

- The RC and its supporting working tree were preserved in commit
  `3e2821a6f9643234e20ac129caf509b909b924e0` on branch
  `codex/resonatus-v1.1.0-rc.1`.
- Temporal portability now passes an eight-case comparison between pySHACL 0.40.1/RDFLib 7.6.0 and
  Apache Jena SHACL 6.2.0. This closes the bounded two-engine portability blocker, not every possible
  engine/version combination.
- A strict-IRI publication plan has been prepared without changing w3id.org. The existing v1.0.0
  redirects remain untouched.
- Normative owner sign-off remains pending in
  `profiles/v1.1-rc/OWNER_NORMATIVE_APPROVAL.md`; publication remains `NO-GO` until that record is
  explicitly approved and final immutable redirect targets exist.

## Evidence required at each gate

### Gate A — conceptual adequacy

- a necessary-and-sufficient natural-language definition;
- explicit counterexamples and non-examples;
- branch, merge, termination, and granularity policy;
- a statement of whether each relation is ontic, epistemic, or evidential.

### Gate B — formal adequacy

- model-theoretic statement of intended entailments and non-entailments;
- CE01 and CE02 rejected or explicitly accepted for a documented reason;
- consistency, satisfiability, conservativity, and competency-question tests;
- a migration analysis for existing fixtures and published IRIs.

### Gate C — scientific adequacy

- independently constructed cases from more than one domain;
- domain-expert labels produced without exposure to the target classification;
- comparison against simpler M1–M4 models and the graded M6 profile;
- analysis of inter-annotator agreement and granularity sensitivity.

Only after Gate C should the project claim a scientifically established category beyond existing process
ontologies.

## Immediate non-normative documentation actions after approval

These do not require new classes but should still follow the owner decision because wording encodes scope:

1. Update the architecture figure with `ResonatusAssessment --assesses--> ResonatusCandidate`.
2. State that `hasTracePath` is an object-property pattern; domain/range axioms do not require every
   candidate to have a path.
3. Relabel the `PathCoherenceShape` note as origin/receiver reference coherence, not proof of a full
   causal chain.
4. Replace unqualified “coherent causal path” claims with the guarantee selected in D01/D03.

## Owner sign-off template

```text
Decision ID:
Selected option:
Rationale:
Required prototype or evidence:
Approved normative impact:
Migration constraints:
Approval date:
```
