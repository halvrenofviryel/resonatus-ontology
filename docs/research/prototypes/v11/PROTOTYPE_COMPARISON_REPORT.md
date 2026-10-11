# Resonatus v1.1 comparative semantic prototype report

**Date:** 2026-10-11
**Status:** expanded and hardened experimental result; no normative change

## Compared models

| Model | Operational reading | Added discrimination |
|---|---|---|
| A — current v1.0.0 | Five typed witnesses on one path plus current origin/receiver agreement | Baseline; no lineage edge or temporal inequality |
| B — process-path | Trace → Propagation → Selectivity → outcome causal spine, explicit segment membership, reference agreement, and separate Delay validation | Rejects reverse direction, role collapse, disconnected outcome, and invalid Delay |
| C — separate scope | B plus an assessment linked to a distinct `AssessmentScope` information object | Prevents assessment scope from becoming the ontic process |

The profile additionally distinguishes a named ontic causal triple, an epistemic claim, evidence-record
completeness, and scientific support.

## Independent result dimensions

`OWL_ENTAILED`, structural conformance, temporal conformance, scope conformance, claim-record
conformance, ontic linkage, and evidence-record presence are not interchangeable. Applicability is
separately reported as `IN_SCOPE` or `OUT_OF_SCOPE`. Each validation dimension uses:

- `CONFORMING`;
- `NON_CONFORMING`;
- `INSUFFICIENT_DATA`;
- `NOT_EVALUATED`;
- `EXECUTION_ERROR`.

The scientific conclusion remains `UNDETERMINED` for all prototype cases.

## Executed results

```bash
python docs/research/prototypes/v11/run_prototypes.py
python docs/research/prototypes/v11/run_prototype_mutations.py
python docs/research/prototypes/v11/run_owl_module_integration.py
```

Results:

- 15/15 scenario expectations;
- 27/27 mutation expectations;
- 26/26 combined OWL-module integration checks;
- critical CE01/CE02 rejection and positive B/C acceptance: pass.

| Case | Current | Lineage | Temporal | Claim/link/evidence | Main interpretation |
|---|---|---|---|---|---|
| CE01 grouped/no lineage | conforming | insufficient | insufficient | not evaluated | Current model accepts grouping; strict data cannot establish lineage |
| CE02 single-node collapse | conforming | non-conforming | insufficient | not evaluated | Explicit role collapse violates the bounded profile |
| Valid B process-path | conforming | conforming | conforming | not evaluated | Structural and temporal profile only |
| Reversed lineage | conforming | non-conforming | conforming | not evaluated | Supplied arrows contradict direction |
| Boundary-equal Delay | conforming | conforming | non-conforming | not evaluated | No positive post-end extent |
| Unrelated same-origin Delay | conforming | conforming | non-conforming | not evaluated | Time and origin do not establish path identity |
| Valid C | conforming | conforming | conforming | conforming/conforming/conforming | Complete structural record; scientific adequacy remains unassessed |
| Claim without named ontic triple | non-conforming | insufficient | conforming | conforming/insufficient/conforming | Valid hypothesis record without ontic acceptance |
| Shared-origin fan-out | conforming | insufficient, out-of-scope | conforming | not evaluated | Applicability and missing lineage are both preserved |
| Missing evidence record | conforming | conforming | conforming | conforming/conforming/insufficient | Ontic assertion does not manufacture evidence support |
| Incomplete claim record | conforming | conforming | conforming | insufficient/conforming/conforming | Record completeness is independent |
| Conflicting ontic linkage | conforming | conforming | conforming | conforming/non-conforming/conforming | Conflict does not make the record malformed |

Every row remains `OWL_ENTAILED` under the unchanged core. This is expected: SHACL validation does not
retract OWL entailments.

## Key hardening changes

- Property-based targets prevent missing `rdf:type` assertions from producing vacuous passes.
- Missing data, explicit violations, out-of-scope graphs, and engine errors are separated.
- Applicability is independent; `OUT_OF_SCOPE` never masks a simultaneous violation or missing fact.
- Reverse edges, cycles, branch/merge topology, and detached outcomes are checked.
- Delay permits overlap but requires a positive post-origin-end portion.
- Delay must explicitly qualify the same path that carries it; it remains outside the causal spine.
- Pure claim properties have no ontic range axioms; an isolated claim does not infer ontic relata.
- `TraceContinuation` typing is still reported as an OWL existential causal commitment even without a
  named RDF triple.
- OWL inconsistency is reported separately from non-entailment.

Detailed evidence is in
[STRICT_PROFILE_HARDENING_REPORT.md](STRICT_PROFILE_HARDENING_REPORT.md).

## Architectural conclusion

Model C remains the cleanest separation of ontic process, assessment scope, causal claim, and evidence.
Model B provides a bounded structural profile, not causal discovery. Delay remains a temporal witness
rather than a causal-spine segment.

No external causal relation is adopted. RO's available relations add transitivity, strict temporal
precedence, immediacy, or upstream-or-within commitments that do not exactly match the required
overlap-permitting adjacency edge. See
[CAUSAL_RELATION_REUSE_DECISION.md](CAUSAL_RELATION_REUSE_DECISION.md).

## Non-results

The experiment does not establish:

- truth of any real-world causal assertion;
- scientific necessity or discrimination of the five criteria;
- a general branch/merge identity theory;
- cross-domain evidence sufficiency;
- a production IRI, default profile, or versioned release package.
