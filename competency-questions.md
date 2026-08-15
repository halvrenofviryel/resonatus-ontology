# Competency questions — Resonatus ontology v1.0.0

These questions define the intended competency boundary of the ontology. They are not claims that the ontology can empirically discover causality from arbitrary data. The questions' historical meaning is preserved from earlier drafts; only the version heading is updated.

> **Executable coverage:** of these questions, **7 currently have executable SPARQL counterparts** in
> `competency-queries/` (structural ASK checks). The remaining questions are documented
> competency boundaries without an executable query yet; broader executable coverage is Future Work.
> Semantic coherence of the five-condition path is verified by the reasoner gates (R6–R21), not by these
> structural queries.

1. Can a candidate trace process be linked to an originating interaction?
2. Can a process be represented as a Resonatus candidate without entailing that it is already a causal trace process?
3. Can the representation distinguish a persistent trace from an effect that ends with the initiating interaction?
4. Can Delay be represented as post-interaction temporal continuation without thereby entailing Trace?
5. Can Delay be satisfied when a candidate continuation begins before the interaction ends but retains a non-zero continuation after the interaction boundary?
6. Can it represent propagation into a later state, receiver, agent, or system boundary without requiring a cross-system boundary?
7. Can it represent that downstream realization is modulated by receiver/context structure?
8. Can it distinguish transformation from feedback while allowing either to satisfy the fifth criterion?
9. Can it distinguish a generic causal trace process from a Resonatus?
10. Can a static, never-used log be represented without classifying it as a Resonatus?
11. Can an assessment distinguish FAIL from NOT_MEASURED, INCONCLUSIVE, and ERROR?
12. Can a positive membership assertion be withheld when any of the five criteria is not established?
13. Can provenance of source interaction and trace derivation be aligned to PROV-O without equating provenance with causality?
14. Can temporal placement be aligned to OWL-Time without treating timestamps or interval order as causal proof?
15. Can normative applications align obligations and constraints to ODRL without making normativity constitutive of Resonatus?
16. Can the ontology represent a transformation with immutable provenance but changed downstream significance?
17. Can two receivers exposed to the same propagated trace be represented with different context-modulated outcomes?
18. Can each of the five criteria be falsified independently in a counterexample fixture?
19. Can A directly continue B and B directly continue C without the ontology entailing that A directly continues C?
20. Can causally connected Resonatus instances remain distinct individuals unless identity is independently asserted or entailed?
21. Can an upper-ontology bridge classify Resonatus as a BFO process without importing that commitment into the core ontology?
22. Can a real-system assessment remain UNDETERMINED when persistence and propagation are documented but selectivity or transformation has not been experimentally established?
