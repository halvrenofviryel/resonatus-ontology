# Changelog

## Unreleased

- Isolated the negative assessment SHACL fixtures so missing `assessesPath` no longer lets unrelated
  tests pass for the wrong reason. The SHACL runner now asserts expected report components, paths, and
  identifying SPARQL messages, not only `conforms = false`.
- Added R26 to verify `sh:targetClass` discovery through `rdfs:subClassOf` in the data graph while the
  runner remains on `inference="none"`.
- Replaced the cross-layer runner's Boolean OWL result with `ENTAILED`, `NOT_ENTAILED`, `INCONSISTENT`,
  and `EXECUTION_ERROR`; inconsistent input is now a hard failure rather than negative membership.
  The runner also recomputes the epistemic classification from criterion verdicts instead of trusting
  the declared expected label alone.
- Added two deliberate ontic/epistemic disagreement fixtures to verify layer independence. The 13
  existing examples remain aligned regression fixtures, not evidence of a general equivalence.
- Clarified diagram notation, witness mixing, causal-attribution semantics, and executable competency
  coverage (`7/22`; `7/7` only among the queries that exist).

## 1.0.0 — 2026-08-15 (first public release)
- First public, archival release of the Resonatus ontology research artefact.
- Persistent identifiers fixed: ontology IRI `https://w3id.org/resonatus`, namespace
  `https://w3id.org/resonatus#`, version IRI `https://w3id.org/resonatus/1.0.0`, archival DOI
  `10.5281/zenodo.21939903`.
- Assessment records must be **path-scoped**: `res:assessesPath` is now required (`sh:minCount 1`) on
  every `ResonatusAssessment`, with a new negative gate **R25** (five-criterion assessment declaring no
  path → non-conforming). Criterion-level `res:scopePath` remains optional.
- Separate clean-tree formal verification pass over the frozen tree: OWL 2 DL gates **R2–R17** (HermiT;
  R2 = core + bridge + official pinned **BFO 2020** consistent, zero unsatisfiable classes, key classes
  satisfiable), SHACL gates **R18–R25** (assessment structure + path scope, origin/receiver
  co‑reference, canonical‑node identity, completeness), cross‑layer examples **13/13**, competency
  queries **7/7**, reference classifier **13/13**, structural audit **13/13**, documentation wording
  lint pass. All reproduced offline from a clean tree with a separate toolchain. See
  `FORMAL_VERIFICATION_REPORT.md`.
- Split licensing (CC BY 4.0 for ontology/docs/examples/shapes; Apache‑2.0 for code) with canonical
  licence files and a per‑path mapping.

## 0.4 (development milestone — witness coherence)
- Introduced the **reified ontic path**: the five constitutive conditions are witnessed on one
  `ContinuationPath` (Trace‑neutral genus) → `CausalTraceProcess` → `ResonatusPath`;
  `Resonatus ≡ ResonatusCandidate ⊓ ∃hasTracePath.ResonatusPath`. This closes the earlier
  witness‑mixing gap (separate existentials could be satisfied from different causal lineages).
- **Origin/receiver co‑reference coherence** moved to the SHACL layer: OWL 2 DL enforces the
  path‑level conjunction, while declared‑origin/Trace‑origin/Delay‑reference and Propagation/Selectivity
  receiver co‑reference (plus completeness, canonical‑node identity) are enforced by the SHACL
  path‑coherence profile — the natural chain‑plus‑functionality encoding leaves OWL 2 DL under the
  adopted role pattern.
- Selectivity tightened to require *uptake dependence* on a receiver context, not mere co‑presence.
- Added adversarial fixtures/gates for mixed‑path, multi‑origin, wrong‑origin/receiver, single declared
  origin (functional), domain contamination, and origin/receiver coherence + completeness.

## 0.3 (development milestone)
- Introduced `ResonatusCandidate` so assessment subjects are not pre‑classified as causal trace
  processes; represented Delay as post‑interaction continuation with no subclass/subproperty link to
  Trace; added OWL‑Time temporal profile and the optional BFO 2020 bridge; added executable structural
  competency queries and reasoner‑targeted fixtures; clarified that SHACL is a separate validation
  profile, not OWL semantics.

## 0.1 (development milestone)
- Initial structural ontology, SHACL shapes, assessment algebra, fixtures, competency questions, and
  reference validator.
