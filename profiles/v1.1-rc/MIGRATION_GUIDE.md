# Migration guide for the Resonatus v1.1 local RC

Migration is opt-in. Existing v1.0.0 users who do not select a strict profile have no migration
requirement, and their existing OWL and repository-level SHACL results remain the relevant results.

## From the v1.1 experimental prototype

Replace the temporary namespace and the renamed causal edge as follows:

| Experimental term | RC candidate term |
|---|---|
| `https://w3id.org/resonatus/experimental/v1.1#AssessmentScope` | `strict:AssessmentScope` |
| `...#CausalAttributionClaim` | `strict:CausalAttributionClaim` |
| `...#hasCausalSegment` | `strict:hasCausalSegment` |
| `...#causallyPrecedes` | `strict:hasCausalNextStage` |
| `...#temporallyQualifiesPath` | `strict:temporallyQualifiesPath` |
| `...#hasAssessmentScope` | `strict:hasAssessmentScope` |
| `...#scopesProcess` | `strict:scopesProcess` |
| `...#causalSubject` | `strict:causalSubject` |
| `...#causalObject` | `strict:causalObject` |
| `...#usesCausalAssessmentMethod` | `strict:usesCausalAssessmentMethod` |

where:

```turtle
@prefix strict: <https://w3id.org/resonatus/strict#> .
```

Do not publish the experimental IRIs as aliases. The RC runner adapters perform this mapping in memory
only to replay the validated prototype oracles against the candidate artefacts.

## Adopt Strict Linear

For each qualifying `res:ContinuationPath`:

1. Register the Trace, Propagation, Selectivity, and outcome witnesses with
   `strict:hasCausalSegment`.
2. Assert the four directed `strict:hasCausalNextStage` edges from the origin through those stages.
3. Preserve the profile's local role distinctions and canonical origin/receiver references.
4. Give the origin and Delay witness OWL-Time intervals with `xsd:dateTimeStamp` values formatted as
   `YYYY-MM-DDThh:mm:ssZ`.
5. Link the Delay to this same path with `strict:temporallyQualifiesPath`.
6. Submit only a bounded single-lineage case to this profile; report branch/merge as `OUT_OF_SCOPE`.

A missing required lineage/time fact is generally `INSUFFICIENT_DATA`. A supplied reversed edge,
boundary-equal interval, explicit unrelated Delay/path binding, cycle, or local identity collapse is
`NON_CONFORMING`.

The timestamp lexical restriction provides a deterministic interchange form. The SHACL comparison
casts the lexical form to `xsd:dateTime` and compares values; it does not compare timestamp strings.

## Adopt Strict Assessment

After Strict Linear requirements are met:

1. Mint a distinct `strict:AssessmentScope` node for the assessment.
2. Link the assessment to the scope and the scope to the same `res:ContinuationPath`; do not reuse the
   path, candidate, assessment, claim, method, or evidence node as the scope.
3. Represent each causal statement as a distinct `strict:CausalAttributionClaim` with exactly one
   `strict:causalSubject`, one `strict:causalObject`, and at least one typed assessment method.
4. Cite at least one typed `res:Evidence` record.
5. Report explicit ontic linkage separately. Do not infer or materialize `res:causallyAttributedTo`
   merely because a claim record exists.

An unaccepted but structurally complete hypothesis is valid as a claim record. It can have
`onticLinkage = INSUFFICIENT_DATA` without being rewritten as an ontic causal assertion.

## Compatibility classification

The package is additive and backward-compatible when it remains optional: the v1.0.0 core does not
import it, and the default shape is not replaced. It is behaviorally stricter when selected. Data that
collapses assessment scope with a process can become inconsistent when the optional vocabulary is
loaded, and data lacking explicit strict-profile facts cannot claim strict conformance.

Strengthening the published `res:ResonatusPath` or `res:Resonatus` OWL definitions, changing
`res:causallyAttributedTo`, importing the optional module into the core, or making strict shapes the
unnegotiated default is outside this migration and would require a separate versioning decision.

The namespace is provisional in this local RC. Production data should not depend on it until the owner
approves the final identifiers and their resolution is operational.
