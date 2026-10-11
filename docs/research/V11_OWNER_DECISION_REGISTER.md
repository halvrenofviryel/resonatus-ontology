# Resonatus v1.1 Owner Decision Register

**State:** OPTIONAL v1.1 STRICT-PROFILE PUBLICATION AUTHORIZED — release and w3id submission in
progress; scientific validation remains unassessed.

## How to use this register

The owner recorded the v1.1 research direction on 2026-10-11 and subsequently approved N01–N09 after
prototype and RC review. That approval closes D01–D03, D05, and D08 for the optional v1.1 strict
module only. D04, D06, and D07 remain research questions; D09–D11 remain preservation constraints.
The initial approval authorized local final-artifact preparation and preservation-branch push. On
2026-10-11 the owner separately authorized merge, the `v1.1.0` tag, GitHub Release, Zenodo versioning,
and a w3id.org pull request. This does not change the scientific-claim boundary.

| ID | Decision | Options | Recommendation | Why | Consequences | Status |
|---|---|---|---|---|---|---|
| D01 | What does `ContinuationPath` primarily denote? | A: real process; B: structural scope/bundle; C: core scope with domain process profiles; D: preserve path as process and model assessment scope separately. | **D: prototype ontic process and distinct assessment scope.** Do not silently change the published IRI's meaning. | The current prose and BFO bridge intend a process; a scope information object has a different ontological role. | Implemented by an optional `AssessmentScope` class and migration contract; the core path meaning is unchanged. | `APPROVED_FOR_OPTIONAL_V1.1_PROFILE` |
| D02 | What does `causallyAttributedTo` mean? | A: real ontic causal relation; B: assessor's causal claim; C: maintain both as separate constructs. | **C**, with the direct property reserved for A and a separate claim object for B. | OWL object-property assertions are ontic in the model; evidence, confidence, and disagreement belong to a claim/assessment layer. | Implemented with a separate causal-claim record; existing ontic triples retain their meaning. | `APPROVED_FOR_OPTIONAL_V1.1_PROFILE` |
| D03 | What establishes one lineage? | A: shared origin; B: ordered causal links; C: process parthood; D: tracked carrier/participant; E: common minimum plus domain evidence profiles. | **E: common directed lineage semantics plus domain-specific evidence profiles.** | Shared origin is insufficient, while evidence methods differ legitimately by domain. | Membership becomes stronger and some current positives may cease to qualify. | `APPROVED_FOR_BOUNDED_STRICT_LINEAR_PROFILE` |
| D04 | How do branch and merge affect path identity? | A: identity follows origin; B: every branch creates a new path; C: lineage graph with explicit branch/merge policy; D: domain-specific. | **C**, a directed causal segment graph with explicit domain constraints. | Origin-only identity collapses divergent effects; always-split is too rigid for feedback and recombination. | Requires branch/merge fixtures, identity tests, and likely a distinction between path and segment. | `OWNER_RESEARCH_DIRECTION; PROTOTYPE_INCOMPLETE` |
| D05 | Where should Delay be validated? | A: OWL core; B: optional OWL-Time/SHACL profile; C: external assessment only. | **B**, as a separate optional temporal validation profile. | The intended non-zero post-end condition is closed-world/data-sensitive and not present in the core. | Domains without interval data cannot claim temporal-profile conformance. | `APPROVED_FOR_OPTIONAL_V1.1_PROFILE` |
| D06 | Are the five positions constitutive of an ontological class? | A: retain necessary-and-sufficient class; B: treat as graded assessment dimensions; C: provisional class plus explicit research status. | **No change at this stage.** | Formal separability is established; scientific necessity and discrimination are not. | Later evidence may support the current definition, simplify it, or favor a graded profile. | `HOLD_NO_CHANGE; SCIENTIFIC_EVIDENCE_REQUIRED` |
| D07 | How should `Transformation ∨ Feedback` be handled? | A: keep disjunction; B: require Feedback; C: operationally define Transformation; D: split into profiles. | **No change at this stage.** | Transformation is currently unconstrained and may be nearly universal at fine granularity. | Define and test both branches before any strengthening. | `HOLD_NO_CHANGE; SCIENTIFIC_EVIDENCE_REQUIRED` |
| D08 | What is the public positioning of Resonatus? | A: novel process kind; B: applied ontology profile; C: vocabulary plus assessment framework. | **B/C now**; reserve A for later evidence. | Current model has a potentially useful selection/profile but no demonstrated identity criterion or independent validation. | Public claims must distinguish formal profile utility from a scientifically established new process kind. | `APPROVED_POSITIONING; PUBLICATION_AUTHORIZED` |
| D09 | Should ontic membership and epistemic support remain separate? | A: separate; B: merge. | **A** | CL1–CL2 show both disagreement directions are coherent and useful. | Preserve current runners and wording. | `PRESERVE` |
| D10 | Should the BFO commitment remain optional? | A: optional bridge; B: import into core. | **A** | Optionality avoids forcing an upper-ontology choice on all users. | Continue bridge consistency tests; revisit only if the upper-ontology decision is explicitly reopened. | `PRESERVE` |
| D11 | Should v1.0.0 release artefacts be rewritten? | A: freeze; B: rewrite. | **A** | Published tags, DOI artefacts, reports, and checksums are historical records. | Put all new work under Unreleased/v1.1 research until an approved release. | `PRESERVE` |

## Approval outcome and remaining research sequence

1. D08 public positioning — **approved**.
2. D01 and D02 ontic/epistemic separation — **approved for the optional v1.1 profile**.
3. D03 and D05 bounded strict lineage/temporal profiles — **approved and implemented**.
4. D04 branch/merge identity — **deferred to the research program**.
5. D06–D07 five-criteria and Transformation/Feedback questions — **await independent scientific study**.

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

At that stage this direction authorized RC engineering only and the candidate identifiers remained
provisional. The later normative approval and final-artifact outcome are recorded below; public
publication still requires a separate decision.

## Post-RC blocker status recorded on 2026-10-11

- The RC and its supporting working tree were preserved in commit
  `3e2821a6f9643234e20ac129caf509b909b924e0` on branch
  `codex/resonatus-v1.1.0-rc.1`.
- Temporal portability now passes an eight-case comparison between pySHACL 0.40.1/RDFLib 7.6.0 and
  Apache Jena SHACL 6.2.0. This closes the bounded two-engine portability blocker, not every possible
  engine/version combination.
- A strict-IRI publication plan has been prepared without changing w3id.org. The existing v1.0.0
  redirects remain untouched.
- The owner approved N01–N09 on 2026-10-11 in
  `profiles/v1.1-rc/OWNER_NORMATIVE_APPROVAL.md`. This authorizes permanent identity selection and
  local final `1.1.0` artefact preparation only. Merge, tag, GitHub Release, Zenodo, and w3id PR
  remain separately controlled publication actions.
- The approved final package is preserved under `profiles/v1.1/` in commit
  `65918870c8cafcf64ef7d8dbace14571178829dd`. It passed package integrity `27/27`, scenario `15/15`,
  mutation `27/27`, module integration `26/26`, two-engine temporal portability `8/8`, and the full
  `14/14` command-group regression.
- The immutable vocabulary, activation, and schema targets were byte-verified over GitHub Raw and
  pinned in the IRI plan by commit `170661b4efadc99531dd36814211db5039e876b4`.
- On 2026-10-11 the owner separately authorized merge, the `v1.1.0` tag, GitHub Release, a Zenodo
  version record, and the prepared w3id PR. Live strict IRI resolution remains dependent on external
  w3id review and deployment; scientific adequacy and causal truth remain unassessed.

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
