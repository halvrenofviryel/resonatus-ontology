# Licensing — Resonatus Ontology v1.0.0

This repository uses a **split licence** by file type. Both licence texts are included in full.

## Ontology, documentation, examples, shapes, and competency material — CC BY 4.0

Licensed under the **Creative Commons Attribution 4.0 International License** (`LICENSE-CC-BY-4.0.txt`,
<https://creativecommons.org/licenses/by/4.0/>). This covers:

- `ontology/` — the OWL 2 DL ontology (`resonatus.ttl`)
- `shapes/` — the SHACL Graph Shape Validation Profile
- `alignments/` — the BFO 2020 bridge and alignment notes (the vendored BFO 2020 file under
  `alignments/vendor/` is a third‑party artefact distributed under **its own** BFO licence — see below)
- `examples/` — the worked example graphs / fixtures
- `tests/` — the OWL/SHACL adversarial fixtures and the reasoner‑gate specification
- `competency-queries/`, `competency-questions.md`
- all Markdown documentation (`README.md`, `CHANGELOG.md`, `DESIGN_RATIONALE.md`,
  `FORMAL_VERIFICATION_REPORT.md`, `THIRD_PARTY_NOTICES.md`) and `docs/`
- repository metadata files: `CITATION.cff`, `SHA256SUMS.txt`, `.gitignore`

To attribute: cite the ontology by its DOI (below) and version.

## Executable validation code and scripts — Apache-2.0

Licensed under the **Apache License, Version 2.0** (`LICENSE-APACHE-2.0.txt`,
<https://www.apache.org/licenses/LICENSE-2.0>). This covers:

- `scripts/` — all Python runner and validation scripts
- `requirements.txt` — the pinned dependency list for those scripts

Every tracked file is covered by exactly one of the two licences above, except the third-party
component below.

## Third‑party components

- `alignments/vendor/bfo-2020-core.owl` — Basic Formal Ontology (BFO) 2020, redistributed unmodified
  for offline reproducibility. It remains under its upstream BFO licence (Creative Commons Attribution
  4.0 International) and is **not** relicensed here; see `THIRD_PARTY_NOTICES.md` and the BFO project
  (<http://purl.obolibrary.org/obo/bfo/2020/bfo.owl>).

## Scope

These licences apply **only** to this repository (the Resonatus ontology research artefact). They do
not apply to, and imply no licence over, any other project or repository.
