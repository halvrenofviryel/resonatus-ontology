# Alignment notes — v1.0.0

## Alignment policy
The core ontology remains deliberately lightweight. External commitments are provided through separate bridge modules where a stable, justified mapping exists. A bridge is an interoperability module, not evidence that a Resonatus exists in the world.

## PROV-O
- `res:Interaction`, `res:ResonatusCandidate`, and the reified `res:ContinuationPath` are modeled as
  specializations of `prov:Activity`; `res:CausalTraceProcess` and `res:ResonatusPath` inherit that
  placement through `res:ContinuationPath`.
- `res:hasOriginInteraction` is a specialization of `prov:wasInfluencedBy`.
- This alignment is intentionally weak: PROV-O represents provenance/influence structures and does not by itself establish the stronger causal attribution required for Resonatus membership.

## OWL-Time
- `res:hasTemporalExtent` links modeled processes to `time:TemporalEntity`.
- Delay is defined by post-interaction continuation: some non-zero temporal part of the trace must occur strictly after the initiating interaction's end boundary.
- A trace may begin before the interaction ends and still satisfy Delay if it remains active afterward.
- OWL-Time interval relations such as `intervalOverlaps`, `intervalOverlappedBy`, `intervalMeets`, `intervalAfter`, and their inverses can describe qualitative temporal configurations. Temporal structure is support for assessment, not causal proof.

## ODRL
- ODRL is not imported into the constitutive definition of `res:Resonatus`.
- Normative applications may map obligations, prohibitions, permissions, duties, and constraints to ODRL terms.
- This is an application alignment only; a Resonatus can be non-normative.

## BFO 2020
- `alignments/resonatus-bfo.ttl` provides the concrete optional bridge, with an `owl:imports` of
  the official BFO 2020 and an offline pinned copy at `alignments/vendor/bfo-2020-core.owl`
  (versionIRI `http://purl.obolibrary.org/obo/bfo/2020/bfo.owl`, sha256 `9a22d466…`).
- Process placement: `res:ResonatusCandidate ⊑ BFO process` (`BFO_0000015`), `res:Interaction ⊑
  BFO process`, and `res:ContinuationPath ⊑ BFO process`. `res:CausalTraceProcess` and `res:ResonatusPath`
  inherit process placement **through `res:ContinuationPath`** (not through the candidate hierarchy).
  `res:Resonatus` is a `res:ResonatusCandidate` that has some `res:ResonatusPath`; it is **not** a
  subclass of `res:CausalTraceProcess`.
- The bridge is separate so the core ontology remains usable without adopting BFO.
- **R2 verified on the v1.0.0 frozen tree:** core + bridge + the vendored pinned BFO 2020 is consistent under HermiT
  with zero unsatisfiable named classes and all key classes satisfiable (reproduced offline with a
  separate toolchain). Release reasoning should load the bridge with the official BFO 2020 it imports.

## DOLCE
- Resonatus is conceptually compatible with a perdurant/process treatment in DOLCE.
- No DOLCE OWL bridge is asserted in this release because the release should not silently mix multiple upper-ontology commitments or choose among DOLCE OWL variants without a dedicated mapping analysis.

## Process chaining and identity
- `res:directlyContinues` is asymmetric and irreflexive but deliberately not transitive.
- OWL 2 provides a positive transitivity characteristic but no global `NonTransitiveObjectProperty` axiom. Accordingly, non-transitive behavior is represented by omission of a transitivity axiom plus negative-entailment tests.
- Causal connection never implies `owl:sameAs`; process identity must be established independently.

## Published PROV-O–BFO mapping context
Prudhomme et al. (2025) provide an independently published semantic alignment in which `prov:Activity` is mapped as equivalent to BFO `process` (`BFO_0000015`). Since the Resonatus core already places `Interaction` and `ResonatusCandidate` under `prov:Activity`, this gives external support for the direction of the optional BFO process bridge. The Resonatus release must still run its own consistency tests with the exact versions it imports; the published mapping is not a substitute for that release gate.

Formal cross-foundational mapping is treated as a separate task. Masolo, Compagno, and Borgo (2025) demonstrate that BFO–DOLCE alignment requires explicit methodological and formal analysis; this release therefore does not add an ad hoc DOLCE bridge.
