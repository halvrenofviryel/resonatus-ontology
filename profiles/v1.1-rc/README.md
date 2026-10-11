# Resonatus optional strict profiles — local RC 1

**Candidate version:** `1.1.0-rc.1`

**Status:** local, provisional, and non-published

**Engineering disposition:** `CONDITIONAL GO` for owner inspection; `NO-GO` for publication

This directory is a self-contained release-candidate package for the optional Resonatus Strict Linear
and Strict Assessment profiles. It turns the bounded v1.1 prototype results into inspectable candidate
artefacts without changing the published v1.0.0 core ontology or its default SHACL profile.

The namespace `https://w3id.org/resonatus/strict#`, its version IRI, and the profile identifiers in this
package are **provisional**. Local preparation does not authorize a tag, release, DOI deposit, namespace
registration, or public claim of scientific validation.

## Package contents

- `ontology/`: the additive optional vocabulary.
- `shapes/`: independently selectable structural, temporal, scope, claim, ontic-linkage, and evidence
  validation dimensions.
- `fixtures/`: positive, negative, insufficient-data, and out-of-scope examples in the candidate
  namespace.
- `schemas/`: the machine-readable multidimensional result contract and one example.
- `runners/`: candidate integrity, scenario, mutation, module-integration, and full regression runners.
- `CONFORMANCE_CONTRACT.md`: profile activation and result-composition rules.
- `MIGRATION_GUIDE.md`: opt-in migration from v1.0.0 or the v1.1 experimental prototype.
- `RELEASE_CANDIDATE_MANIFEST.md`: provenance, inventory, and release boundaries.
- `VERIFICATION_REPORT.md`: executed evidence and known unverified items.
- `TEMPORAL_PORTABILITY_REPORT.md`: independent pySHACL/Jena temporal comparison.
- `IRI_PUBLICATION_PLAN.md`: prepared permanent-identifier and redirect plan; not applied.
- `OWNER_NORMATIVE_APPROVAL.md`: explicit owner sign-off gate.
- `CHECKSUMS.sha256`: SHA-256 checksums for every package artefact except the checksum file itself.

## Reproduce the checks

Run from the repository root with the pinned project environment:

```bash
env PYTHONDONTWRITEBYTECODE=1 \
  /mnt/data/claude/resonatus-ontology/.venv/bin/python \
  profiles/v1.1-rc/runners/verify_package.py

env PYTHONDONTWRITEBYTECODE=1 \
  /mnt/data/claude/resonatus-ontology/.venv/bin/python \
  profiles/v1.1-rc/runners/run_all.py

env PYTHONDONTWRITEBYTECODE=1 \
  JENA_SHACL=/path/to/apache-jena-6.2.0/bin/shacl \
  /mnt/data/claude/resonatus-ontology/.venv/bin/python \
  profiles/v1.1-rc/runners/run_temporal_portability.py
```

`run_all.py` executes the candidate gates, the underlying experimental comparison, and the existing
repository regressions. It does not write release state or contact a publication service.

## Interpretation boundary

Passing these checks establishes only that the candidate implements its stated formal and structural
contract in the pinned local environment. It does not establish that Resonatus is a scientifically
validated natural kind, that a cited evidence record is adequate, or that an asserted causal relation
is true. Branch/merge identity, engines beyond the recorded two-engine temporal matrix, stable public
IRI resolution, and domain evidence thresholds remain outside or incomplete for this candidate.
