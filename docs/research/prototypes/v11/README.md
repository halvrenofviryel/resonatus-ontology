# Resonatus v1.1 semantic prototypes

**Status:** hardened experimental candidate; non-normative and outside the published v1.0.0 model.

This directory compares and hardens three readings without changing `ontology/resonatus.ttl` or
`shapes/resonatus.shacl.ttl`:

- **A — current profile:** five witnesses on one `ContinuationPath` plus current origin/receiver checks;
- **B — process-path:** explicit causal-spine membership, directed links, reference agreement,
  distinctness, and an optional temporal Delay profile;
- **C — separate scope:** B plus an `AssessmentScope` information object distinct from the ontic path.

The prototype also separates `CausalAttributionClaim`, the named ontic
`res:causallyAttributedTo` triple, evidence-record completeness, and scientific support.

## Run

From the repository root, using the declared dependency versions:

```bash
python docs/research/prototypes/v11/run_prototypes.py
python docs/research/prototypes/v11/run_prototype_mutations.py
python docs/research/prototypes/v11/run_owl_module_integration.py
```

Expected summaries:

```text
cases=15/15; critical_acceptance=PASS; scientific_conclusion=UNDETERMINED; overall=PASS
mutations=27/27; overall=PASS
integration_checks=26/26; overall=PASS
```

The runners report each validation dimension using `CONFORMING`, `NON_CONFORMING`,
`INSUFFICIENT_DATA`, `NOT_EVALUATED`, or `EXECUTION_ERROR`. Profile applicability is reported
separately as `IN_SCOPE` or `OUT_OF_SCOPE`; an out-of-scope finding cannot hide a simultaneous explicit
violation. Missing information is not converted into factual falsity.

## Documents

- [PROTOTYPE_COMPARISON_REPORT.md](PROTOTYPE_COMPARISON_REPORT.md) — A/B/C result overview;
- [STRICT_PROFILE_SEMANTIC_CONTRACT.md](STRICT_PROFILE_SEMANTIC_CONTRACT.md) — precise concept and
  validation contracts;
- [STRICT_PROFILE_HARDENING_REPORT.md](STRICT_PROFILE_HARDENING_REPORT.md) — scenario and mutation
  audit;
- [CAUSAL_RELATION_REUSE_DECISION.md](CAUSAL_RELATION_REUSE_DECISION.md) — RO/BFO/PROV-O and related
  comparison;
- [V11_COMPATIBILITY_AND_MIGRATION.md](V11_COMPATIBILITY_AND_MIGRATION.md) — entailment, data, BFO, and
  versioning impact;
- [V11_RELEASE_READINESS.md](V11_RELEASE_READINESS.md) — final review/decision table.
- [FINAL_NORMATIVE_REVIEW_GATE_REPORT.md](FINAL_NORMATIVE_REVIEW_GATE_REPORT.md) — four final review
  gates, activation proposal, production contract, and conditional release-candidate recommendation.

## Executable artefacts

- [experimental-vocabulary.ttl](experimental-vocabulary.ttl) — candidate vocabulary, not imported by
  the core;
- [shapes/](shapes/) — isolated lineage, Delay, scope, claim-record, ontic-linkage, and evidence-record
  shapes;
- [fixtures/](fixtures/) — positive, negative, insufficient-data, and out-of-scope cases;
- [run_prototypes.py](run_prototypes.py) — 15-case OWL/SHACL comparison;
- [run_prototype_mutations.py](run_prototype_mutations.py) — 27 adequacy mutations;
- [run_owl_module_integration.py](run_owl_module_integration.py) — A/B/C OWL module integration gates.

## Scope boundary

The initial profile covers one linear causal spine only. Delay is validated as a temporal qualification
explicitly bound to that path and is not forced into the causal spine. Branch/merge is reported as
`OUT_OF_SCOPE`; validation findings remain independently visible. The profile does not settle process
identity, carrier continuity, external-relation reuse, evidence sufficiency, or the scientific status of
the five criteria.
