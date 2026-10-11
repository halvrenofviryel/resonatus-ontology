# Review Feedback Remediation 2026 10 11

## Decision

The v1.0.0 ontology definition and its five constitutive criteria remain unchanged. The review exposed
real weaknesses in test isolation, outcome reporting, validation independence, and explanatory
notation. Those issues are corrected on `main` without changing the frozen v1.0.0 tag, the OWL class
axioms, or the SHACL profile.

## Implemented corrections

1. Negative SHACL assessment fixtures now declare a valid `assessesPath` unless missing path is the
   rule under test. Each malformed fixture therefore fails for its intended reason.
2. The SHACL gate runner checks the validation report's `sh:sourceConstraintComponent`,
   `sh:resultPath`, and identifying SPARQL message. A generic non-conforming result is no longer enough.
3. R26 verifies that `sh:targetClass` reaches instances of a subclass declared in the data graph even
   when the runner deliberately disables general RDFS inference.
4. The cross-layer runner reports `ENTAILED`, `NOT_ENTAILED`, `INCONSISTENT`, and `EXECUTION_ERROR` as
   distinct outcomes. Dedicated guards verify that neither inconsistent input nor an execution failure
   can satisfy an expected negative-membership case. The epistemic result is recomputed from the five
   criterion verdicts and checked against the declared expected label.
5. Two cross-layer counterexamples deliberately separate ontic entailment from epistemic support in
   both directions. The original 13 examples remain useful aligned regressions, but their agreement is
   no longer presented as evidence that the layers are equivalent.
6. The README and design rationale now distinguish object-property edges, subclass relations, and
   class expressions; define witness mixing; give one stable meaning for `causallyAttributedTo`; and
   state competency coverage as 7 executable queries out of 22 documented questions.

## Deliberately unchanged

- The five-position definition and Transformation-or-Feedback disjunction require scientific and
  cross-domain evaluation before revision.
- `scopePath` remains optional at criterion level; the enclosing assessment's `assessesPath` remains
  required and supplies the record scope.
- The OWL and SHACL layers remain separate. Their different semantics are intentional and tested.
- The BFO bridge and the placement of `ResonatusCandidate` remain unchanged; the available evidence
  does not establish a modelling error.
- FAIL precedence over unknown/error states remains the reference reporting policy. A supported FAIL
  can justify non-membership even when a different criterion is unresolved.

## Manuscript-only findings

Several editor comments identify presentation defects in the submitted article rather than defects in
the repository's formal artefacts: Echoism was not defined or cited at first use; unrelated scope
exclusions distracted from the ontology; key terms and symbols were introduced too late; historical
conditions such as `start(c) > end(i)` were mentioned without first establishing the earlier version;
and some bolding and prose made class, criterion, evidence, and validation language harder to
distinguish. The repository documentation now uses explicit notation and plainer definitions, but the
rejected manuscript is intentionally not revised or prepared for resubmission.

## Research backlog

The following are research questions, not safe automatic patches:

- specify and compare alternatives for causal-path identity and continuity;
- evaluate domain methods that warrant `causallyAttributedTo` without changing its core meaning;
- test whether Delay, receiver-conditioned Selectivity, and Transformation remain discriminating
  across independent applications;
- decide whether temporal boundary checks belong in an OWL-Time profile, a SHACL profile, or an
  external assessment method;
- classify all 22 competency questions by executable method and extend coverage where a formal oracle
  is meaningful;
- obtain an independently constructed dataset or reuse study rather than only author-designed examples.
