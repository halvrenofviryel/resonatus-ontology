# Resonatus Ontology v1.0.0

A structural ontology for **persistent causal trace processes**, with a SHACL validation profile,
competency questions, worked examples, and reproducible formal‑verification artefacts. A **persistent causal trace ontology** in OWL 2 DL. Companion
research artefact for the manuscript *Resonatus: An Ontology of Persistent Causal Trace Processes*
(Ali Toygar Abak, Phionyx Research).

| | |
|---|---|
| Ontology IRI | `https://w3id.org/resonatus` |
| Vocabulary namespace | `https://w3id.org/resonatus#` (prefix `res:`) |
| Version IRI | `https://w3id.org/resonatus/1.0.0` |
| Release version | `1.0.0` |
| Archival DOI | [`10.5281/zenodo.21939903`](https://doi.org/10.5281/zenodo.21939903) |
| Repository | <https://github.com/halvrenofviryel/resonatus-ontology> |

## What Resonatus is

Resonatus is a **proposed** ontological class: a causal trace that survives its initiating interaction,
persists, propagates, is taken up according to a receiving context, and is transformed or participates in
feedback. It is **not** a discovered physical law, a consciousness criterion, an AGI measure, or an
empirical universal.

## Layers

1. **OWL 2 DL semantic layer** — `ontology/resonatus.ttl` defines the class structure under open‑world
   semantics.
2. **Graph Shape Validation Profile** — `shapes/resonatus.shacl.ttl` validates assessment‑record
   structure and path‑coherence; it is not part of OWL class semantics and does not prove causality.
3. **Reference assessment policy** — `scripts/validate.py` maps explicit criterion verdicts to
   `MEMBERSHIP_SUPPORTED` / `NON_MEMBERSHIP_SUPPORTED` / `UNDETERMINED`.
4. **Optional BFO 2020 bridge** — `alignments/` (with a vendored, pinned BFO 2020 for offline reasoning).
5. **Evaluation materials** — competency questions/queries, worked examples, and adversarial fixtures.

## Constitutive definition (reified path)

The five constitutive conditions are witnessed on a single reified **ontic causal path**, not on the
candidate as separable existentials:

```
ResonatusCandidate --hasTracePath--> ContinuationPath --(has TraceContinuation)--> CausalTraceProcess --> ResonatusPath
```

- `ContinuationPath` is the Trace‑**neutral** genus (causal status is not presupposed here).
- `CausalTraceProcess` = a `ContinuationPath` that carries a Trace continuation.
- `ResonatusPath` = the qualifying path: Trace, post‑interaction Delay, Propagation, Selectivity,
  Transformation‑or‑Feedback, and exactly one declared originating interaction, all on one path.
- `Resonatus ≡ ResonatusCandidate ⊓ (∃ hasTracePath . ResonatusPath)` — a candidate with **some
  qualifying path**. It is **not** a subclass of `CausalTraceProcess`.

**Division of responsibility:**

- **OWL 2 DL** enforces the *path‑level* semantics — all five witness types on one path node.
- **SHACL** enforces *origin/receiver co‑reference coherence* (declared origin = Trace origin = Delay
  reference; Propagation receiver = Selectivity receiver) plus completeness, using canonical RDF‑node
  identity (not `owl:sameAs`). This co‑reference is not captured by the ontology's OWL 2 DL role pattern
  (the natural chain‑plus‑functionality encoding leaves OWL 2 DL); it is scoped to that role pattern, not
  a general expressivity theorem. See `DESIGN_RATIONALE.md`.
- The **epistemic classifier** is a separate layer and never asserts ontic truth.

The historical three‑of‑five rule is not an ontological membership rule.

## Reproducible offline validation

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt          # rdflib, pyshacl, owlready2 (bundles HermiT; needs a JRE)

python scripts/run_reasoner_gates.py     # OWL 2 DL gates R2–R17 (HermiT); R2 uses the vendored BFO 2020
python scripts/run_shacl_gates.py        # SHACL assessment + path‑coherence gates R18–R25 (pyShACL)
python scripts/run_example_crosslayer.py # 13 examples: OWL Resonatus ⇔ MEMBERSHIP_SUPPORTED
python scripts/run_competency_queries.py # executable structural competency queries
python scripts/validate.py .             # verdict‑based reference classifier
python scripts/audit_structure.py        # structural audit
python scripts/check_wording.py          # documentation wording lint
```

All reasoning runs **offline** — BFO 2020 is vendored at `alignments/vendor/bfo-2020-core.owl`. The full
gate specification and results are in `tests/reasoner-release-gates.md` and
`FORMAL_VERIFICATION_REPORT.md`. Integrity: `SHA256SUMS.txt`.

## Repository layout

```
ontology/          OWL 2 DL ontology
shapes/            SHACL Graph Shape Validation Profile
alignments/        BFO 2020 bridge + vendored pinned BFO
tests/             OWL + SHACL adversarial fixtures + reasoner‑gate spec
competency-queries/ executable SPARQL + competency questions
examples/          worked example graphs
scripts/           HermiT/pySHACL runners, reference classifier, wording lint
docs/figures/      architecture figure
FORMAL_VERIFICATION_REPORT.md   separate‑toolchain formal verification report
DESIGN_RATIONALE.md             design rationale
```

## Citing

Please cite the archived artefact (see `CITATION.cff`):

> Abak, A. T. (2026). *Resonatus Ontology: OWL 2 DL Model, SHACL Validation Profile, and Verification
> Artefacts* (Version 1.0.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.21939903

## Methodological limits & Future Work

- OWL class entailment is not empirical causal discovery; SHACL conformance is not ontological truth;
  missing measurement is not failure.
- The BFO bridge is optional; the core does not require an upper ontology.
- **Future Work:** a paired‑state real‑system intervention and independent external reuse are not
  established here; broader executable coverage of the competency questions is ongoing.

## Licence

Split licence — **CC BY 4.0** for ontology/documentation/examples/shapes and **Apache‑2.0** for the
validation code. Full texts and the per‑path mapping are in `LICENSE.md`, `LICENSE-CC-BY-4.0.txt`, and
`LICENSE-APACHE-2.0.txt`. These apply only to this repository.
