# Resonatus v1.1 strict-profile hardening report

**Date:** 2026-10-11
**Status:** experimental profile hardened; normative adoption not authorized

## Outcome

The comparative prototype now passes 15/15 scenario gates, 27/27 independent mutation gates, and
26/26 combined OWL-module integration checks. The
critical acceptance condition remains satisfied: CE01 and CE02 do not conform to the lineage profile,
while the coherent linear fixture conforms to lineage and temporal validation.

Formal success establishes that the shapes discriminate the tested graph structures. It does not
establish empirical causation or a scientifically novel process kind.

The unchanged repository regression suite also passes: 69 Turtle files parse; OWL gates R2–R17,
SHACL gates R18–R26, 13/13 example classifications, 2/2 layer-independence cases, explicit
inconsistency/execution-error guards, and 7/7 executable competency queries succeed.

## Runner audit

`run_prototypes.py` contains explicit expected values only as a test oracle. Actual values are computed
by four independent mechanisms:

- HermiT over the unchanged core plus case data for OWL outcome;
- pySHACL over the published profile for the current result;
- pySHACL over separately loaded lineage, temporal, scope, claim-record, ontic-linkage, and
  evidence-record shapes;
- direct graph inspection for named ontic triples versus an OWL existential commitment.

The comparison is performed after computation. No code path returns an expected value as an actual
result. `run_prototype_mutations.py` then changes individual triples in a known-positive graph; the
corresponding results change without changing the oracle table. This is the independent guard against
hardcoded or inert results.

## Shape activation and vacuous-pass controls

| Risk | Control | Gate |
|---|---|---|
| Removing `rdf:type res:ContinuationPath` prevents the lineage shape from running | `sh:targetObjectsOf res:hasTracePath` supplements `sh:targetClass` | M01 |
| Removing `rdf:type res:PostInteractionContinuation` prevents the temporal shape from running | `sh:targetObjectsOf res:hasPostInteractionContinuation` supplements `sh:targetClass` | M02 |
| Required causal edge absent but graph still passes | Missing-edge mutation must return `INSUFFICIENT_DATA` | M03 |
| Segment constraint is unused | Removing one segment membership must return `INSUFFICIENT_DATA` | M04 |
| Reverse edge is ignored | Adding the reverse edge must return `NON_CONFORMING` | M05 |
| Outcome need not be downstream of uptake | Detaching Transformation must return `INSUFFICIENT_DATA` | M06 |
| A branch is silently treated as a linear path | Applicability becomes `OUT_OF_SCOPE`; a pure branch finding returns `NOT_EVALUATED` | M07 |
| Scope and process can collapse | Scope collapse returns `NON_CONFORMING` | M08 |
| Evidence-record constraint is unused | Removing evidence returns `INSUFFICIENT_DATA` | M09 |
| Out-of-scope masks explicit violations or missing data | Applicability stays separate; validation and all findings remain visible | M15–M17 |
| Delay can qualify an unrelated same-origin continuation | Pre-gate shape accepts it; mismatch is now `NON_CONFORMING`; missing linkage is `INSUFFICIENT_DATA` | M18a–M18c |
| Claim record is conflated with ontic acceptance | Claim-only record conforms while ontic linkage is insufficient | M20a–M20b |
| Incomplete or conflicting claims contaminate all claim results | Record, linkage, and evidence dimensions change independently | M21a–M22b |

Property-based targets deliberately coexist with class targets. This is a profile-local closed-world
choice and does not modify RDFS/OWL target semantics in the published profile.

## Result taxonomy

The old Boolean result has been replaced by:

- `CONFORMING` for fully checked and satisfied data;
- `NON_CONFORMING` for an explicit determinable violation;
- `INSUFFICIENT_DATA` when required assertions are absent;
- `NOT_EVALUATED` for inactive or out-of-scope dimensions;
- `EXECUTION_ERROR` when the engine cannot return a trustworthy report.

Applicability is reported separately as `IN_SCOPE` or `OUT_OF_SCOPE`. Message precedence is
`VIOLATION_` before `MISSING_` before a pure `OUT_OF_SCOPE_`; every finding is retained. M10 injects
malformed SPARQL and verifies `EXECUTION_ERROR` rather than a pass or a false non-conformance.

## Scenario results

| Case | Current | Lineage | Temporal | Scope | Claim record | Ontic link | Evidence record |
|---|---|---|---|---|---|---|---|
| CE01 grouped/no lineage | conforming | insufficient | insufficient | not evaluated | not evaluated | not evaluated | not evaluated |
| CE02 single-node collapse | conforming | non-conforming | insufficient | not evaluated | not evaluated | not evaluated | not evaluated |
| Valid process-path | conforming | conforming | conforming | not evaluated | not evaluated | not evaluated | not evaluated |
| Reversed lineage | conforming | non-conforming | conforming | not evaluated | not evaluated | not evaluated | not evaluated |
| Delay ends at origin end | conforming | conforming | non-conforming | not evaluated | not evaluated | not evaluated | not evaluated |
| Unrelated same-origin Delay | conforming | conforming | non-conforming | not evaluated | not evaluated | not evaluated | not evaluated |
| Valid separate scope | conforming | conforming | conforming | conforming | conforming | conforming | conforming |
| Scope is process | conforming | conforming | conforming | non-conforming | conforming | conforming | conforming |
| Claim without named ontic triple | non-conforming | insufficient | conforming | conforming | conforming | insufficient | conforming |
| Missing temporal data | conforming | conforming | insufficient | not evaluated | not evaluated | not evaluated | not evaluated |
| Shared-origin fan-out | conforming | insufficient, out-of-scope | conforming | not evaluated | not evaluated | not evaluated | not evaluated |
| Unrelated Transformation | conforming | insufficient | conforming | not evaluated | not evaluated | not evaluated | not evaluated |
| Ontic relation, missing evidence | conforming | conforming | conforming | not evaluated | conforming | conforming | insufficient |
| Incomplete claim record | conforming | conforming | conforming | not evaluated | insufficient | conforming | conforming |
| Conflicting ontic linkage | conforming | conforming | conforming | not evaluated | conforming | non-conforming | conforming |

The scientific conclusion is `UNDETERMINED` for every row.

## Intended failure reasons

- **CE01:** missing causal-spine membership and edges, plus missing temporal data. This is absence of
  sufficient representation, not a factual denial of causal lineage.
- **CE02:** the same missing facts plus an explicit role-identity collapse. The explicit collapse makes
  lineage `NON_CONFORMING`.
- **Reversed lineage:** a supplied edge contradicts the required direction, so the result is
  `NON_CONFORMING` rather than merely incomplete.
- **Boundary-equal Delay:** the supplied timestamps make the temporal rule false.
- **Unrelated Delay:** equal origin and valid timestamps are insufficient; explicit qualification of a
  different path is `NON_CONFORMING`.
- **Missing time:** no order conclusion is drawn; the result is `INSUFFICIENT_DATA`.
- **Claim-only:** the epistemic record conforms, but does not substitute for a named ontic triple;
  ontic linkage is `INSUFFICIENT_DATA`.
- **Shared-origin fan-out:** applicability is `OUT_OF_SCOPE`; its simultaneous missing lineage edge
  remains visible as `INSUFFICIENT_DATA`.
- **Detached Transformation:** the graph does not establish that outcome is downstream of uptake.

## OWL inconsistency and existential witnesses

M11a verifies that the strict SHACL profile reports the second origin as a cardinality violation. M11b
adds an explicit difference assertion to the functional declared-origin property. HermiT returns
`OWL_INCONSISTENT`; the runner does not collapse this into `OWL_NOT_ENTAILED`.

The published axiom

`TraceContinuation ⊑ ∃ causallyAttributedTo.Interaction`

means Trace typing requires some causal target under OWL Direct Semantics. It does not require a named
target in the RDF graph. The claim-only case therefore reports `EXISTENTIAL_COMMITMENT_ONLY` while its
ontic-linkage result is `INSUFFICIENT_DATA`. M12 verifies that distinction.

To prevent the claim layer itself from causing the same ontic typing, the experimental
`causalSubject`/`causalObject` properties have no ontic range axioms. M13 loads the core and experimental
vocabulary together and verifies that an isolated claim does not infer `TraceContinuation` or
`Interaction` for its relata.

## Temporal and overlap behavior

The valid Delay begins before the origin ends and finishes later; it conforms. The causal edge relation
also has no end-before-start rule. M14 adds overlapping intervals to causally linked origin/Trace
processes and confirms that lineage still conforms.

This separation is deliberate:

- temporal precedence is not causation;
- causation need not require non-overlap;
- Delay is a temporal qualification witness, not automatically a causal-spine segment.

## Reproduction

From the repository root:

```bash
python docs/research/prototypes/v11/run_prototypes.py
python docs/research/prototypes/v11/run_prototype_mutations.py
python docs/research/prototypes/v11/run_owl_module_integration.py
```

The runners require the dependency versions declared by the repository. SHACL behavior is checked with
`inference="none"` so canonical-node and explicit-triple policies remain deterministic.

## Remaining limits

- The linear chain is a bounded validation design, not a theory of process identity.
- Pairwise witness-node distinctness is an experimental policy and needs owner review before adoption.
- The fixed-width UTC comparison is engine-specific operational normalization.
- Claim-record, ontic-linkage, and evidence-record checks are independent; domain evidence adequacy is
  always explicitly unassessed.
- Branch/merge, carrier continuity, mereological unity, and domain evidence thresholds remain open.
