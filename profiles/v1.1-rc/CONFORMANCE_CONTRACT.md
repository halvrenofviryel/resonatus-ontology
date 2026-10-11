# Resonatus v1.1 RC conformance contract

**Applies to:** `1.1.0-rc.1`

**Status:** provisional local contract for optional profiles

## Independent result planes

A result must preserve each plane independently. No successful value in one plane implies success in
another.

| Plane | Values | Meaning |
|---|---|---|
| OWL outcome | `OWL_ENTAILED`, `OWL_NOT_ENTAILED`, `OWL_INCONSISTENT`, `OWL_EXECUTION_ERROR` | Model-theoretic result from the selected ontology configuration |
| Applicability | `IN_SCOPE`, `OUT_OF_SCOPE` | Whether the bounded single-lineage profile applies to the supplied topology |
| Validation dimension | `CONFORMING`, `NON_CONFORMING`, `INSUFFICIENT_DATA`, `NOT_EVALUATED`, `EXECUTION_ERROR` | Closed-world result for one activated dimension |
| Causal commitment | `EXPLICIT_ONTIC_RELATION`, `EXISTENTIAL_COMMITMENT_ONLY`, `NONE_IDENTIFIED` | Kind of ontic commitment visible in the graph/reasoning result |
| Scientific evidence status | `DOMAIN_EVIDENCE_UNASSESSED`, `DOMAIN_EVIDENCE_NOT_EVALUATED` | This RC does not judge scientific adequacy |

The serialized dimensions are `structural`, `temporal`, `assessmentScope`, `claimRecord`,
`onticLinkage`, and `evidenceRecord`. A non-activated dimension is `NOT_EVALUATED`; it must not be
silently reported as conforming.

## Finding precedence

All findings remain in the result. Precedence determines only the summary value within a validation
dimension:

1. engine failure → `EXECUTION_ERROR`;
2. any `VIOLATION_` finding → `NON_CONFORMING`;
3. otherwise any `MISSING_` finding → `INSUFFICIENT_DATA`;
4. otherwise a pure `OUT_OF_SCOPE_` finding → `NOT_EVALUATED`;
5. no finding → `CONFORMING`.

Applicability is orthogonal to this precedence. A result may therefore be `OUT_OF_SCOPE` while a
dimension is `NON_CONFORMING` or `INSUFFICIENT_DATA`.

## Strict Linear Conformance

The activated plan is
`https://w3id.org/resonatus/strict/profile/strict-linear/1.1.0-rc.1`.

The named conformance claim requires all of the following:

- applicability is `IN_SCOPE` for the bounded linear topology;
- `structural` is `CONFORMING` under `strict-linear.shacl.ttl`;
- `temporal` is `CONFORMING` under `temporal-delay.shacl.ttl`.

The structural profile requires explicit causal-segment registration and the directed sequence origin
→ Trace → Propagation → Selectivity → outcome, with local role distinctness, reference agreement,
cycle rejection, and no branch/merge in the selected spine. `strict:hasCausalNextStage` is directed,
asymmetric, and irreflexive; it is not declared transitive and no general OWL non-transitivity claim is
made.

The temporal profile requires the Delay to identify the same path through
`strict:temporallyQualifiesPath`. Instants use `xsd:dateTimeStamp` in canonical UTC second precision,
and ordering is evaluated by timestamp value rather than lexical order. Process overlap remains
permitted; the contract does not impose end-before-start on causal stages.

A branch or merge produces `OUT_OF_SCOPE` applicability and cannot support Strict Linear Conformance.
This is not a finding that the represented domain process is invalid.

## Strict Assessment Conformance

The activated plan is
`https://w3id.org/resonatus/strict/profile/strict-assessment/1.1.0-rc.1`.

The named conformance claim requires Strict Linear Conformance plus:

- `assessmentScope` is `CONFORMING`;
- `claimRecord` is `CONFORMING`;
- `evidenceRecord` is `CONFORMING`.

The assessment must use a distinct `strict:AssessmentScope` that denotes the same ontic
`res:ContinuationPath` selected by the assessment. A causal claim must have exactly one subject, one
object, and at least one typed method. It must cite at least one typed `res:Evidence` record.

`onticLinkage` is mandatory to report but is not a prerequisite for this named structural assessment
claim. A complete hypothesis record can therefore be Strict Assessment conforming while its ontic
linkage is `INSUFFICIENT_DATA`. An explicit conflicting ontic target is `NON_CONFORMING` in that
dimension and remains visible. A future stricter claim that requires conforming ontic linkage must use
a separate profile identifier.

## What conformance does not mean

Neither named profile:

- asserts that a cited evidence record is scientifically adequate;
- proves that a causal assertion is true;
- changes the five constitutive criteria in the published core;
- makes an out-of-scope branch/merge topology false or malformed in general;
- establishes Resonatus as a scientifically validated process kind.

The machine-readable form of this contract is
`schemas/validation-result.schema.json`.
