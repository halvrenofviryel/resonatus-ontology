# OWL reasoner release gates — v1.0.0

These gates require an OWL 2 DL reasoner. The reference runner is `scripts/run_reasoner_gates.py`
(HermiT via owlready2). Results can be reproduced with a separate toolchain (ROBOT/OWLAPI + HermiT
or another OWL 2 DL reasoner) against the frozen release tree.

Model: the five constitutive conditions are witnessed on a single reified ontic path
(`res:ContinuationPath` / `res:ResonatusPath`), not on the candidate as separable existentials. Membership:
`Resonatus ≡ ResonatusCandidate ⊓ ∃hasTracePath.ResonatusPath` (≥1 qualifying path).

## Core gates

### R1 — Core consistency
The core ontology must be consistent.

### R2 — BFO bridge consistency
Core + `alignments/resonatus-bfo.ttl` + the **official BFO 2020 core** must be consistent, with the key
classes satisfiable. **Status: RUN and PASS on the v1.0.0 frozen tree.** BFO 2020 is now **vendored and pinned**
(`alignments/vendor/bfo-2020-core.owl`, versionIRI `http://purl.obolibrary.org/obo/bfo/2020/bfo.owl`,
sha256 `9a22d466…`), and the bridge carries an `owl:imports`, so R2 runs offline
(`scripts/run_reasoner_gates.py`) and was **reproduced offline with a separate toolchain**:
consistent, zero unsatisfiable named classes,
`Resonatus`/`ResonatusPath`/`ContinuationPath`/`CausalTraceProcess` satisfiable.

### R3 — Direct-continuation non-entailment
`tests/nontransitive-chain.ttl`: given `a directlyContinues b` and `b directlyContinues c`, the reasoner
must **not** entail `a directlyContinues c`. (OWL 2 has no `NonTransitiveObjectProperty`; the property is
simply not declared transitive and the non-entailment is verified on the canonical chain.)

### R4 — Identity non-collapse
The chain must not entail `owl:sameAs` among the distinct individuals. The fixture asserts them
`owl:AllDifferent`, so any forced merge would surface as **inconsistency**; a consistent result witnesses
non-collapse.

### R5 — Resonatus satisfiability
`res:Resonatus` must remain satisfiable (with the BFO bridge loaded). Witnessed
positively by R6/R12/R13 producing `Resonatus` instances.

### R6 — Positive class entailment
`tests/owl-positive-resonatus.ttl`: one coherent path with all five conditions ⇒ `ex:candidate` is
entailed `res:Resonatus` and `ex:path` is entailed `res:ResonatusPath`.

### R7 — Missing-selectivity non-entailment (path-level)
`tests/owl-missing-selectivity.ttl`: the path carries Trace+Delay+Propagation+Transformation but no
`ContextModulation`. The **path** must be entailed `res:CausalTraceProcess` but **not** `res:ResonatusPath`,
and the candidate must **not** be entailed `res:Resonatus`. OWA non-entailment, not class complement.

### R8 — Delay without Trace non-entailment
`tests/owl-delay-without-trace.ttl`: a path with only a post-interaction continuation must **not** be
entailed `res:CausalTraceProcess` or complete a `res:ResonatusPath`; the candidate is not `res:Resonatus`.

### R9 — Causal-origin property chain
`tests/owl-causal-origin-chain.ttl`: `hasTraceContinuation ∘ causallyAttributedTo` must entail
`ex:path_co res:hasOriginInteraction ex:origin` (on the path). Distinct from the single
`res:hasDeclaredOriginInteraction` scope.

## Witness-coherence adversarial gates (release-critical)

### R10 — Mixed-path false-positive attack
`tests/owl-mixed-path-attack.ttl`: five conditions split across two paths (Trace+Delay on p1;
Propagation+Selectivity+Transformation on p2). Must **not** entail `res:Resonatus`. *(This is the case
earlier drafts wrongly admitted.)*

### R11 — Five different paths
`tests/owl-five-different-paths.ttl`: each condition on its own path. Must **not** entail `res:Resonatus`.

### R12 — Complete path + incomplete path
`tests/owl-complete-plus-incomplete.ttl`: one qualifying path plus one incomplete path. **Must** entail
`res:Resonatus` (≥1 qualifying path suffices); the incomplete path must **not** be `res:ResonatusPath`.

### R13 — Two complete independent paths
`tests/owl-two-complete-paths.ttl`: two qualifying paths under one candidate. Must entail `res:Resonatus`
with **no merge** — paths and origins asserted `owl:AllDifferent`, so a consistent result witnesses that
the model does not force `owl:sameAs`/origin equality/path equality.

### R14 — Wrong-origin Delay
`tests/owl-wrong-origin-delay.ttl`: the otherwise-complete path lacks Delay; the Delay lives on a
different-origin path. No qualifying path ⇒ must **not** entail `res:Resonatus`.

### R15 — Wrong-receiver Selectivity
`tests/owl-wrong-receiver-selectivity.ttl`: the otherwise-complete path lacks Selectivity; the
`ContextModulation` lives on a different path. No qualifying path ⇒ must **not** entail `res:Resonatus`.

## Cardinality / modelling gates

### R16 — Single declared origin per path (functional)
`tests/owl-two-declared-origins-inconsistent.ttl`: `res:hasDeclaredOriginInteraction` is functional.
**Note (precise):** functionality alone does not create inconsistency from two asserted origins — under
OWA the reasoner would take them to be the same individual. Inconsistency arises **only when the two
declared origins are explicitly `owl:differentFrom` / `owl:AllDifferent`**, which the fixture asserts.
Then functional (at most one) + two distinct values ⇒ **inconsistent**, enforcing "exactly one declared
origin per path". Justifies the functional-property use with this adversarial test.

### R17 — Domain-contamination probe
`tests/owl-domain-contamination.ttl`: using `res:hasPropagationEvent` on an untyped individual types it as
`res:ContinuationPath` (intended: witnesses belong to paths) but must **not** type it as `res:ResonatusCandidate`
or `res:Resonatus`. Candidate typing requires `res:hasTracePath`.

## Origin / receiver coherence gates (SHACL-enforced; OWL-limited)

**Demonstrated limitation of the OWL 2 DL role pattern used here (scoped, not a general theorem).**
Binding the trace-derived origin (a property-chain = *composite* role) into the functional
`hasDeclaredOriginInteraction` makes that role **non-simple**, which OWL 2 DL forbids in a
functional/cardinality axiom and HermiT rejects (`Non-simple property … appears in the cardinality
restriction`). The generic cross-witness co-reference constraint this model needs is therefore not
captured by the ontology's OWL 2 DL role pattern; we do not claim no OWL 2 DL encoding could relate such
witnesses. Accordingly OWL enforces only **path-level** coherence (all five on one path); the
**same-origin / same-receiver** coherence below is enforced in the **SHACL path-coherence profile**
(`res:PathCoherenceShape`), and the manuscript claim is narrowed accordingly. OWL alone does **not**
reject R18–R20 (documented limitation); the SHACL gate does. Run: `scripts/run_shacl_gates.py`.

### R18 — Same-path declared-origin ≠ Trace-origin  (`tests/shacl/path-r18-origin-incoherent.ttl`)
Declared origin `iA`, Trace `causallyAttributedTo iB`, all four other criteria on the same path.
SHACL: **non-conform**. (OWL: still classifies as Resonatus — the limitation above.)

### R19 — Same-path Delay reference ≠ declared origin  (`tests/shacl/path-r19-delay-incoherent.ttl`)
`res:postInteractionOf` was added so this is expressible: Delay `postInteractionOf iB`, declared origin
`iA`. SHACL: **non-conform**.

### R20 — Propagation receiver ≠ Selectivity receiver  (`tests/shacl/path-r20-receiver-incoherent.ttl`)
`res:hasPropagationReceiver` was added: Propagation reaches `rA`, Selectivity `uptakeDependsOn rB`.
SHACL: **non-conform**.

### R21 — Fully coherent path (positive regression)  (`tests/shacl/path-r21-fully-coherent.ttl`)
Same origin `iA` for declared/Trace/Delay, same receiver `rA` for Propagation/Selectivity. SHACL:
**conform**; and the OWL positive (R6) entails Resonatus for the analogous coherent path.

### R22/R23 — `owl:sameAs`-aliased references are distinct  (`tests/shacl/path-r22-origin-alias.ttl`, `path-r23-receiver-alias.ttl`)
Identity is canonical RDF-node reference equality, not `owl:sameAs` equivalence: references linked only
by `owl:sameAs` are treated as distinct. SHACL: **non-conform**.

### R24 — Completeness of coherence references  (`tests/shacl/path-r24-incomplete-refs.ttl`)
A path carrying all five witness types but missing a required coherence reference. SHACL: **non-conform**.

### R25 — Assessment must declare a path  (`tests/shacl/path-r25-assessment-missing-path.ttl`)
A five-criterion `ResonatusAssessment` that declares no `res:assessesPath`. Every assessment must be
scoped to exactly one `ContinuationPath` (`res:assessesPath` `sh:minCount 1`), so a path-less full
assessment is not a path-coherent record. SHACL: **non-conform**.

## Verification status

On the frozen release tree, `scripts/run_reasoner_gates.py` reports **all of R2–R17 behaving as
specified** under HermiT (R2 = core + bridge + the pinned official BFO 2020: consistent, zero
unsatisfiable named classes, key classes satisfiable), and `scripts/run_shacl_gates.py` reports all
assessment + path-coherence gates (R18–R25) as specified (pyShACL). R1/R5 are witnessed by consistent
reasoning + `Resonatus` instances. The origin/receiver coherence gates are **SHACL-enforced** (not
captured by the ontology's OWL 2 DL role pattern). All gates were reproduced offline from a clean tree
in a separate verification pass with a separate toolchain; see `FORMAL_VERIFICATION_REPORT.md`.
