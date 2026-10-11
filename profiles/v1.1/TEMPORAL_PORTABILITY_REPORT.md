# Resonatus v1.1.0 temporal SHACL portability report

**Date:** 2026-10-11

**Result:** `PASS` for the bounded two-engine matrix

## Engines and provenance

| Engine | Version | Role |
|---|---|---|
| pySHACL / RDFLib | pySHACL 0.40.1 / RDFLib 7.6.0 | Pinned project environment |
| Apache Jena SHACL | 6.2.0 | Independent implementation |

Apache Jena was obtained from the official `apache-jena-6.2.0.tar.gz` binary distribution and used
from a temporary directory; it was not added as a repository or system dependency. The downloaded
archive passed the publisher-provided SHA-512 check:

```text
2b467d2ff940c207aea935e012ecbb0f0ab3e6bf59b3fc4b3fbc6cf9cea11f1428e97882ec078a5ffc57e114e0f5c88ea98c4575e687cc1dd232f99324b7b2a2
```

## Executed matrix

Both engines evaluated the same in-memory RDF graph for every case and the final v1.1.0
`shapes/temporal-delay.shacl.ttl` shape.

| Case | Expected | pySHACL | Jena |
|---|---|---|---|
| `VALID_OVERLAPPING_INTERVAL` | `CONFORMING` | `CONFORMING` | `CONFORMING` |
| `VALID_DATE_ROLLOVER` | `CONFORMING` | `CONFORMING` | `CONFORMING` |
| `BOUNDARY_EQUAL` | `NON_CONFORMING` | `NON_CONFORMING` | `NON_CONFORMING` |
| `END_BEFORE_BEGIN` | `NON_CONFORMING` | `NON_CONFORMING` | `NON_CONFORMING` |
| `UTC_OFFSET_REJECTED` | `NON_CONFORMING` | `NON_CONFORMING` | `NON_CONFORMING` |
| `FRACTIONAL_SECONDS_REJECTED` | `NON_CONFORMING` | `NON_CONFORMING` | `NON_CONFORMING` |
| `MISSING_DELAY_END` | `INSUFFICIENT_DATA` | `INSUFFICIENT_DATA` | `INSUFFICIENT_DATA` |
| `UNRELATED_PATH` | `NON_CONFORMING` | `NON_CONFORMING` | `NON_CONFORMING` |

Summary: `8/8 PASS`, two engines.

The matrix covers permitted overlap, UTC-second normalization, a date rollover, strict boundary and
ordering failures, missing data, and Delay-to-path mismatch. It exercises the value casts and temporal
comparisons rather than substituting expected values for engine output.

## Reproduction

The Apache Jena `shacl` executable is deliberately external to the repository:

```bash
env PYTHONDONTWRITEBYTECODE=1 \
  JENA_SHACL=/path/to/apache-jena-6.2.0/bin/shacl \
  /mnt/data/claude/resonatus-ontology/.venv/bin/python \
  profiles/v1.1/runners/run_temporal_portability.py
```

If the executable is absent, the runner reports `NOT_RUN` and returns a non-zero status. It never
silently converts a missing second engine into a pass.

## Decision and limit

The portability blocker is closed for pySHACL 0.40.1/RDFLib 7.6.0 and Apache Jena SHACL 6.2.0 under
the eight-case matrix. v1.1.0 may normatively require canonical UTC second precision and value-based
comparison while listing these versions as the verified implementation baseline.

This is not a universal guarantee for every SHACL-SPARQL implementation or future engine version.
Engine upgrades and any change to the temporal shape require rerunning this matrix. The result is
formal interoperability evidence only; it does not validate domain timing evidence scientifically.
