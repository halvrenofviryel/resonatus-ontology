# Resonatus v1.1 local release-candidate manifest

## Identity and provenance

| Field | Value |
|---|---|
| Candidate version | `1.1.0-rc.1` |
| Preparation date | 2026-10-11 |
| Source repository revision | `119e89d127df6f9431dd22d344175a8476dfb6a6` |
| `origin/main` at preparation | `119e89d127df6f9431dd22d344175a8476dfb6a6` |
| Candidate namespace | `https://w3id.org/resonatus/strict#` (provisional) |
| Candidate ontology IRI | `https://w3id.org/resonatus/strict` (provisional) |
| Candidate version IRI | `https://w3id.org/resonatus/strict/1.1.0-rc.1` (provisional) |
| Strict Linear profile | `https://w3id.org/resonatus/strict/profile/strict-linear/1.1.0-rc.1` (provisional) |
| Strict Assessment profile | `https://w3id.org/resonatus/strict/profile/strict-assessment/1.1.0-rc.1` (provisional) |
| Working-tree condition | Pre-existing modified and untracked work preserved; no cleanup or overwrite performed |

The source revision records the common committed baseline, not a claim that the candidate package is
committed. The package was prepared in a dirty working tree and its exact file bytes are identified by
`CHECKSUMS.sha256`.

## Normative candidate artefacts

| Artefact | Role |
|---|---|
| `ontology/resonatus-strict-vocabulary.ttl` | Optional additive vocabulary; not imported by the core |
| `profile-activation.ttl` | Versioned Strict Linear and Strict Assessment activation identifiers |
| `shapes/strict-linear.shacl.ttl` | Bounded single-lineage structure and applicability checks |
| `shapes/temporal-delay.shacl.ttl` | Delay/path binding and canonical UTC-second interval checks |
| `shapes/assessment-scope.shacl.ttl` | Separate assessment-scope record checks |
| `shapes/claim-record.shacl.ttl` | Structural causal-claim checks |
| `shapes/ontic-linkage.shacl.ttl` | Independent explicit ontic-link agreement checks |
| `shapes/evidence-record.shacl.ttl` | Independent evidence-record presence checks |
| `schemas/validation-result.schema.json` | Multidimensional result serialization contract |

## Verification and support artefacts

- Ten representative candidate fixtures under `fixtures/`.
- `schemas/example-validation-result.json`.
- Shared adapter plus package, scenario, mutation, module-integration, temporal-portability, and full
  regression runners under `runners/`.
- The five required package documents, temporal portability report, IRI plan, owner approval record,
  and checksum inventory.

The complete file list is the set of paths in `CHECKSUMS.sha256` plus `CHECKSUMS.sha256` itself.

## Semantic delta from the published core

- No file under `ontology/` or the repository-level `shapes/` directory is replaced or imported by this
  package.
- `res:ContinuationPath` and `res:causallyAttributedTo` retain their published meanings.
- The package adds an opt-in directed causal spine using `strict:hasCausalNextStage` and a Delay binding
  using `strict:temporallyQualifiesPath`.
- Assessment scope and causal claims are separate information artefacts. Claim subject/object
  properties have no ontic range axioms.
- Only local distinctions needed by the bounded profiles are checked. The vocabulary does not add a
  broad global disjointness regime.
- The package makes no RO/BFO causal-property equivalence and does not treat causal-segment membership
  as BFO parthood.

## Release boundary

This manifest authorizes no commit, push, merge, tag, GitHub release, DOI/Zenodo deposit, w3id
configuration, default-profile replacement, or manuscript revision. Publication remains blocked until
the owner approves permanent identifiers and release scope, IRI resolution is operational, portability
decisions are recorded, and the package is reviewed as a whole.
