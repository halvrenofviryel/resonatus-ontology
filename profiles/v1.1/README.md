# Resonatus optional strict profiles — v1.1.0 local final artefacts

**Version:** `1.1.0`

**Status:** owner-approved local final artefacts; not publicly published

**Engineering disposition:** `GO` for preservation; `NO-GO` for public publication

This directory is the self-contained, owner-approved local final package for the optional Resonatus
Strict Linear and Strict Assessment profiles. It promotes the bounded v1.1 prototype and RC results
without changing the published v1.0.0 core ontology or its default SHACL profile.

The namespace `https://w3id.org/resonatus/strict#`, final version IRI, and profile identifiers are
owner-approved. Public w3id resolution is not active. Local preservation does not authorize a merge,
tag, GitHub Release, DOI deposit, w3id change, or public claim of scientific validation.

## Package contents

- `ontology/`: the additive optional vocabulary.
- `shapes/`: independently selectable structural, temporal, scope, claim, ontic-linkage, and evidence
  validation dimensions.
- `fixtures/`: positive, negative, insufficient-data, and out-of-scope examples.
- `schemas/`: the machine-readable multidimensional result contract and one example.
- `runners/`: package integrity, scenario, mutation, module-integration, and full regression runners.
- `CONFORMANCE_CONTRACT.md`: profile activation and result-composition rules.
- `MIGRATION_GUIDE.md`: opt-in migration from v1.0.0 or the v1.1 experimental prototype.
- `RELEASE_MANIFEST.md`: provenance, inventory, and release boundaries.
- `VERIFICATION_REPORT.md`: executed evidence and known unverified items.
- `TEMPORAL_PORTABILITY_REPORT.md`: independent pySHACL/Jena temporal comparison.
- `IRI_PUBLICATION_PLAN.md`: prepared permanent-identifier and redirect plan; not applied.
- `OWNER_NORMATIVE_APPROVAL.md`: completed design sign-off and publication boundary.
- `CHECKSUMS.sha256`: SHA-256 checksums for every package artefact except the checksum file itself.

## Reproduce the checks

Run from the repository root with the pinned project environment:

```bash
env PYTHONDONTWRITEBYTECODE=1 \
  /mnt/data/claude/resonatus-ontology/.venv/bin/python \
  profiles/v1.1/runners/verify_package.py

env PYTHONDONTWRITEBYTECODE=1 \
  /mnt/data/claude/resonatus-ontology/.venv/bin/python \
  profiles/v1.1/runners/run_all.py

env PYTHONDONTWRITEBYTECODE=1 \
  JENA_SHACL=/path/to/apache-jena-6.2.0/bin/shacl \
  /mnt/data/claude/resonatus-ontology/.venv/bin/python \
  profiles/v1.1/runners/run_temporal_portability.py
```

`run_all.py` executes the v1.1 gates, the underlying experimental comparison, and the existing
repository regressions. It does not write release state or contact a publication service.

## Interpretation boundary

Passing these checks establishes only that the package implements its stated formal and structural
contract in the pinned local environment. It does not establish that Resonatus is a scientifically
validated natural kind, that a cited evidence record is adequate, or that an asserted causal relation
is true. Branch/merge identity, engines beyond the recorded two-engine temporal matrix, stable public
IRI resolution, and domain evidence thresholds remain outside or incomplete for this package.
