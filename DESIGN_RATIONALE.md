# Design Rationale — Resonatus Ontology v1.0.0

This note records the load‑bearing modelling decisions and their formal justification. It is an
academic design record; the normative artefacts are the ontology and the SHACL profile.

## 1. The membership definition

Resonatus membership is constitutive over five positions on a single causal continuation:

> ∃p [ Trace(p) ∧ Delay(p) ∧ Propagation(p) ∧ Selectivity(p) ∧ (Transformation(p) ∨ Feedback(p)) ]

The claim is not merely that a candidate exhibits the five conditions *somewhere*; it is that they hold
on **one coherent causal path** anchored to one declared originating interaction. An earlier draft placed
the five conditions as independent existential restrictions on the candidate:

```
Resonatus ≡ ResonatusCandidate ⊓ ∃hasTraceContinuation.… ⊓ ∃hasPostInteractionContinuation.… ⊓ …
```

In OWL 2 DL each existential may be satisfied by a *different* individual, so a candidate aggregating
witnesses from unrelated lineages would be entailed as Resonatus — a false reading the definition does
not intend.

## 2. The reified path (why it is the chosen structure)

Within a class‑restriction role pattern, OWL 2 DL does not let two separate existential restrictions be
forced to share the same filler individual (there is no co‑designation of existential witnesses in that
pattern). The available way to obtain same‑scope coherence *inside* OWL 2 DL is therefore to **reify**
the shared scope as an individual and hang the conditions off that one node:

```
ResonatusCandidate --hasTracePath--> ContinuationPath --> CausalTraceProcess --> ResonatusPath
Resonatus ≡ ResonatusCandidate ⊓ (∃ hasTracePath . ResonatusPath)
```

- `ContinuationPath` — an ontic, temporally extended continuation path. It is deliberately **Trace‑
  neutral**: causal status is *not* presupposed at this genus. This preserves the methodological point
  that a candidate is not typed as causal before Trace is established.
- `CausalTraceProcess` — a `ContinuationPath` that carries a Trace continuation.
- `ResonatusPath` — the qualifying path: all five conditions plus exactly one declared originating
  interaction, on one node.
- `Resonatus` is a candidate that has **some** qualifying path (≥1). It is deliberately **not** a
  subclass of `CausalTraceProcess`; that specialization lives on the path.

This prevents the tested witness‑mixing fixtures from entailing `Resonatus`: if the five conditions are
split across several paths, no single path is a `ResonatusPath`, so the candidate is not entailed
`Resonatus` (consistent non‑entailment, not unsatisfiability).

## 3. Origin and receiver coherence (why it is in SHACL, not OWL)

Reifying to one path node guarantees the five condition *types* co‑occur on one path, but not that they
refer to the **same** originating interaction and the **same** receiver. Enforcing that would require
forcing two role‑successors (e.g. the path's declared origin and the interaction the Trace is causally
attributed to) to co‑refer.

The natural in‑ontology encoding — deriving an origin through a property chain and then constraining it to
coincide with a functionally‑constrained declared origin — **leaves OWL 2 DL**: a property‑chain
super‑property is a *non‑simple* role, and OWL 2 DL permits functional and cardinality axioms only on
*simple* roles (W3C OWL 2 Structural Specification). A standard DL reasoner rejects such an ontology
outright. This is a scoped observation about the role pattern used here, **not** a general theorem that
no OWL 2 DL encoding could relate such witnesses.

Accordingly:

- **OWL 2 DL** enforces the path‑level conjunction (all five condition types on one path node).
- The **SHACL path‑coherence profile** enforces origin/receiver co‑reference — declared origin = the
  Trace's causal‑attribution target = the Delay's reference interaction, and the Propagation's receiver =
  the Selectivity's uptake receiver — together with **completeness** (a fully‑witnessed path must carry
  those references). Identity here is **canonical RDF‑node reference equality**, deliberately *not*
  `owl:sameAs` semantic equivalence, so validation is deterministic and independent of any
  materialization/reasoning mode. Two references linked only by `owl:sameAs` are treated as distinct.

The manuscript claim is scoped to match: OWL captures the path‑level semantics; origin/receiver coherence
is a validation‑profile guarantee, not an OWL entailment.

## 4. Selectivity

Selectivity requires that downstream uptake **materially depends on** a receiver context
(`res:uptakeDependsOn`), not merely that a receiver context is present. The ontology records this
dependence commitment; evidential adequacy for the dependence is an assessment‑layer matter.

## 5. Upper‑ontology placement

The optional BFO 2020 bridge places `ResonatusCandidate`, `Interaction`, and `ContinuationPath` under
BFO `process`; `CausalTraceProcess` and `ResonatusPath` inherit that placement through `ContinuationPath`.
The genus is treated as a plain process; no commitment to a more specific BFO category is made without
dedicated analysis. Core + bridge + the pinned BFO 2020 is consistent with all key classes satisfiable.

## 6. Epistemic separation

`PASS` / `FAIL` / `NOT_MEASURED` / `INCONCLUSIVE` / `ERROR` are assessment outcomes, not ontological
truth values. A criterion that is not measured or is inconclusive yields *non‑entailment* under the
open‑world assumption, never a falsehood; the assessment layer distinguishes a measured failure from an
unmeasured one, while the ontic layer treats both as non‑entailment. SHACL conformance validates record
structure and path coherence; it does not assert that a Resonatus exists in the world.
