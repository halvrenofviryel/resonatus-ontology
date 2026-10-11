# Resonatus v1.1 strict-profile owner approval record

**Status:** `APPROVED`

The owner approved N01–N09 on 2026-10-11. The approval authorizes preparation and preservation of
local final `1.1.0` artefacts. It does not authorize merge, tag, GitHub Release, Zenodo publication, or
a w3id.org pull request; each remains a separate publication action.

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
| N01 | Approve `https://w3id.org/resonatus/strict#` as the permanent term namespace and use final version identifiers ending in `/1.1.0` | `APPROVED` |
| N02 | Approve `strict:hasCausalNextStage` as a narrow, directed, asymmetric, irreflexive, non-transitive-declaration-free relation at declared granularity, without automatic RO/BFO equivalence | `APPROVED` |
| N03 | Retain `strict:temporallyQualifiesPath`; Delay is bound to a path but is not a causal-spine segment | `APPROVED` |
| N04 | Approve Strict Linear and Strict Assessment exactly as composed in `CONFORMANCE_CONTRACT.md`; ontic linkage remains independently reported | `APPROVED` |
| N05 | Approve local role-distinctness constraints and only the optional `AssessmentScope`/`ContinuationPath` OWL disjointness; no broad global disjointness regime | `APPROVED` |
| N06 | Approve canonical UTC-second timestamps and value-based comparison, with the verified two-engine baseline recorded in `TEMPORAL_PORTABILITY_REPORT.md` | `APPROVED` |
| N07 | Preserve the five constitutive criteria, published core semantics, default v1.0.0 shape, and branch/merge exclusion from the first strict profile | `APPROVED` |
| N08 | Approve public positioning as an optional applied-ontology vocabulary and assessment framework; conformance must not be presented as scientific validation | `APPROVED` |
| N09 | Do not publish the RC identifiers as final; promote approved artefacts to `1.1.0`, then create immutable targets and a separate w3id pull request | `APPROVED` |

## Sign-off

```text
Owner: Ali Toygar Abak
Approved selections: N01–N09
Exceptions: None
Approved normative impact: Permanent strict-profile identity contract and preparation of final 1.1.0 artefacts
Approved publication scope: Local preparation and preservation-branch push only; merge, tag, GitHub Release, Zenodo, and w3id PR require separate approval
Approval date: 2026-10-11
Approval status: APPROVED
```

The normative design gate is closed. Public publication remains `NO-GO` until final artefacts pass all
gates, immutable HTTPS targets exist, w3id resolution is operational, and a separate publication action
is authorized.
