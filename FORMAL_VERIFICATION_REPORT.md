# Formal Verification Report — Resonatus Ontology v1.0.0

> This is the historical report for the frozen `v1.0.0` tag. Current `main` adds stricter negative-test
> isolation, SHACL report assertions, layer-independence fixtures, and an explicit inconsistent-ontology
> outcome guard; see `docs/review-feedback-remediation-2026-10-11.md`.

**Scope:** formal / tool / reproducibility verification of the artefact only. This report makes **no**
claim of empirical or scientific validation of Resonatus; it records what standard reasoning and
validation tools report for the frozen release tree.

**Artefact:** Resonatus Ontology v1.0.0 — ontology IRI `https://w3id.org/resonatus`, version IRI
`https://w3id.org/resonatus/1.0.0`, DOI `10.5281/zenodo.21939903`. The frozen source tree is Git commit
`f7be377d3b355f1dbe1911f12bf597d62355619d`, referenced by the GitHub `v1.0.0` release tag.

## Environment

- OWL 2 DL reasoning: **HermiT** (via owlready2 0.51), OpenJDK 21.
- SHACL: **pyShACL 0.40.1** (closed‑world, no inference — canonical‑node identity).
- RDF/SPARQL: rdflib 7.6.0.
- Upper ontology: official **BFO 2020**, vendored and pinned at `alignments/vendor/bfo-2020-core.owl`
  (versionIRI `http://purl.obolibrary.org/obo/bfo/2020/bfo.owl`, sha256
  `9a22d4668110a9b87c97bbcff28fb8dd6aa398fdbf869004f53e71694908deee`); all reasoning runs offline.
- Separate verification pass: the gates were reproduced from a clean tree using a separate toolchain.

## Gate results

All gates behaved as specified in `tests/reasoner-release-gates.md`.

**OWL 2 DL (HermiT):**

- **R1** core consistency — consistent.
- **R2** core + bridge + official BFO 2020 — **consistent, zero unsatisfiable named classes**;
  `Resonatus`, `ResonatusPath`, `ContinuationPath`, `CausalTraceProcess` all satisfiable.
- **R3** direct‑continuation non‑entailment; **R4** identity non‑collapse.
- **R5** `Resonatus` satisfiable; **R6** positive entailment.
- **R7** missing‑selectivity → path is `CausalTraceProcess`, not `ResonatusPath`; candidate not
  `Resonatus`. **R8** delay‑without‑Trace → not `CausalTraceProcess`.
- **R9** causal‑origin property chain entailed.
- **R10** mixed‑path, **R11** five‑paths, **R14** wrong‑origin Delay (separate path), **R15**
  wrong‑receiver Selectivity (separate path) → **not** `Resonatus`.
- **R12** complete + incomplete path → `Resonatus`; **R13** two complete paths → `Resonatus`, no merge.
- **R16** two explicitly distinct declared origins on one path → **inconsistent** (functional origin).
- **R17** domain‑contamination → typed `ContinuationPath`, not `ResonatusCandidate`/`Resonatus`.

**SHACL (pyShACL):**

- Assessment‑record structure (exactly one candidate, five distinct criterion positions, allowed verdict
  vocabulary, path‑scope consistency); malformed records are non‑conforming.
- **R18–R20** origin / delay‑reference / receiver **incoherence** → non‑conforming; **R21** fully
  coherent → conforming.
- **R22/R23** references linked only by `owl:sameAs` are treated as **distinct** (canonical‑node
  identity) → non‑conforming.
- **R24** a fully‑witnessed path missing a coherence reference → non‑conforming (completeness).
- **R25** a five‑criterion assessment declaring no `res:assessesPath` → non‑conforming (every
  assessment must be scoped to exactly one `ContinuationPath`; `res:assessesPath` `sh:minCount 1`).

**Cross‑layer:** 13/13 worked examples satisfy `OWL Resonatus ⇔ expectedClassification ==
MEMBERSHIP_SUPPORTED`. This records the behavior of those intentionally aligned release fixtures; it is
not a general equivalence between ontic membership and epistemic support.

**Reference / structural / documentation:** reference classifier 13/13; structural audit 13/13;
documentation wording lint pass.

## Key formal finding (scoped)

Origin/receiver co‑reference coherence is enforced by the **SHACL** path‑coherence profile, not by OWL.
The natural in‑ontology encoding (a property‑chain‑derived origin forced to coincide with a
functionally‑constrained declared origin) leaves OWL 2 DL because the super‑property becomes non‑simple,
which the reasoner rejects. This is scoped to the ontology's role pattern; it is not a claim that no
OWL 2 DL encoding could relate such witnesses.

## Reproducibility

From a clean tree, install `requirements.txt` and run the scripts listed in `README.md`. No network is
required (BFO 2020 is vendored). Integrity of the release files is recorded in `SHA256SUMS.txt`.

## Boundary

These results are formal/tool/reproducibility outcomes only. They do not establish that Resonatus is
true, empirically validated, or independently scientifically validated.
