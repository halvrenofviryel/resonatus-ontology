# Resonatus v1.1 strict-profile owner approval record

**Status:** `PENDING_OWNER_SIGN_OFF`

This record is the remaining normative gate. Engineering evidence may populate the recommendations,
but only the owner can change the status to `APPROVED` and supply the approval date.

## Evidence available to the owner

- Local RC package integrity: `24/24 PASS` before this approval record was added.
- Strict scenarios: `15/15 PASS`.
- Mutation checks: `27/27 PASS`.
- OWL module integration: `26/26 PASS`.
- Full existing regression suite: `PASS`.
- Temporal portability: `8/8 PASS` on pySHACL 0.40.1/RDFLib 7.6.0 and Apache Jena SHACL 6.2.0.
- Candidate preservation commit: `3e2821a6f9643234e20ac129caf509b909b924e0` on
  `codex/resonatus-v1.1.0-rc.1`.
- IRI plan: prepared in `IRI_PUBLICATION_PLAN.md`; no w3id change has been made.

## Decisions requiring explicit approval

| ID | Recommended selection | Owner status |
|---|---|---|
| N01 | Approve `https://w3id.org/resonatus/strict#` as the permanent term namespace and use final version identifiers ending in `/1.1.0` | `PENDING` |
| N02 | Approve `strict:hasCausalNextStage` as a narrow, directed, asymmetric, irreflexive, non-transitive-declaration-free relation at declared granularity, without automatic RO/BFO equivalence | `PENDING` |
| N03 | Retain `strict:temporallyQualifiesPath`; Delay is bound to a path but is not a causal-spine segment | `PENDING` |
| N04 | Approve Strict Linear and Strict Assessment exactly as composed in `CONFORMANCE_CONTRACT.md`; ontic linkage remains independently reported | `PENDING` |
| N05 | Approve local role-distinctness constraints and only the optional `AssessmentScope`/`ContinuationPath` OWL disjointness; no broad global disjointness regime | `PENDING` |
| N06 | Approve canonical UTC-second timestamps and value-based comparison, with the verified two-engine baseline recorded in `TEMPORAL_PORTABILITY_REPORT.md` | `PENDING` |
| N07 | Preserve the five constitutive criteria, published core semantics, default v1.0.0 shape, and branch/merge exclusion from the first strict profile | `PENDING` |
| N08 | Approve public positioning as an optional applied-ontology vocabulary and assessment framework; conformance must not be presented as scientific validation | `PENDING` |
| N09 | Do not publish the RC identifiers as final; promote approved artefacts to `1.1.0`, then create immutable targets and a separate w3id pull request | `PENDING` |

## Sign-off

```text
Owner:
Approved selections: N01–N09 / exceptions listed below
Exceptions:
Approved normative impact:
Approved publication scope:
Approval date:
Approval status: APPROVED | REJECTED | REVISION_REQUIRED
```

Until this block is completed, the engineering disposition remains `CONDITIONAL GO` for inspection
and `NO-GO` for normative publication.
