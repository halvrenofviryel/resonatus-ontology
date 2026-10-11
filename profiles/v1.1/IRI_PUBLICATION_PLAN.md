# Resonatus strict-profile IRI publication plan

**Status:** permanent identifier contract and w3id pull-request submission owner-authorized

## Existing state verified on 2026-10-11

The live `perma-id/w3id.org` configuration under `ids/resonatus/.htaccess` contains two rules only:

- `https://w3id.org/resonatus` → the immutable v1.0.0 ontology content;
- `https://w3id.org/resonatus/1.0.0` → the same immutable v1.0.0 content.

There is no `strict` rule, which explains the observed HTTP 404. Those two existing rules must remain
unchanged.

The reviewed RC vocabulary is available over HTTPS from its pushed preservation commit:

```text
https://raw.githubusercontent.com/halvrenofviryel/resonatus-ontology/3e2821a6f9643234e20ac129caf509b909b924e0/profiles/v1.1-rc/ontology/resonatus-strict-vocabulary.ttl
```

The remote bytes matched the reviewed RC with SHA-256
`7fab06c5dc40a7e3c1431d0b88c992630c5d7eb9e0e3d8ef44a930a31862a599`.

## Approved permanent identifier contract

The owner approved these identifiers for final v1.1.0 artefact preparation:

| Role | Identifier |
|---|---|
| Term namespace | `https://w3id.org/resonatus/strict#` |
| Ontology IRI | `https://w3id.org/resonatus/strict` |
| Final version IRI | `https://w3id.org/resonatus/strict/1.1.0` |
| Strict Linear profile | `https://w3id.org/resonatus/strict/profile/strict-linear/1.1.0` |
| Strict Assessment profile | `https://w3id.org/resonatus/strict/profile/strict-assessment/1.1.0` |
| Validation-result schema | `https://w3id.org/resonatus/strict/schema/validation-result/1.1.0` |

The `1.1.0-rc.1` identifiers remain prerelease identifiers. The owner-approved promotion mints the
final identifiers above in `profiles/v1.1/`; redirect rules must target an immutable, byte-verified
commit containing those final artefacts. Whether the RC identifiers also receive archival redirects
is a separate owner choice; they must not silently become final IRIs.

## Verified immutable final targets

Final v1.1.0 artefacts were preserved in commit
`65918870c8cafcf64ef7d8dbace14571178829dd`. On 2026-10-11, the GitHub Raw responses were
byte-for-byte equal to the local files:

| Target | SHA-256 |
|---|---|
| `profiles/v1.1/ontology/resonatus-strict-vocabulary.ttl` | `cb704ff5c6a2376033bbb0908c387a8db18fa0025da32c5d7c87a2671dff7f0c` |
| `profiles/v1.1/profile-activation.ttl` | `1b3b2578337bf109b69933edf9608b5057aa11599da7e92b3d70d3c6f06cbf57` |
| `profiles/v1.1/schemas/validation-result.schema.json` | `584a3cbcf99911393c47a4db4d8892b2d8c5527f5ba17d54fe842e543ca99a93` |

## Proposed w3id rule shape

The following is a review-ready template, not an `.htaccess` change. It uses the verified immutable
commit above:

```apache
# Strict-profile versioned vocabulary -> immutable approved release content
RewriteRule ^strict/1\.1\.0/?$ https://raw.githubusercontent.com/halvrenofviryel/resonatus-ontology/65918870c8cafcf64ef7d8dbace14571178829dd/profiles/v1.1/ontology/resonatus-strict-vocabulary.ttl [R=302,L]

# Versioned profile activation identifiers -> immutable approved release content
RewriteRule ^strict/profile/strict-linear/1\.1\.0/?$ https://raw.githubusercontent.com/halvrenofviryel/resonatus-ontology/65918870c8cafcf64ef7d8dbace14571178829dd/profiles/v1.1/profile-activation.ttl [R=302,L]
RewriteRule ^strict/profile/strict-assessment/1\.1\.0/?$ https://raw.githubusercontent.com/halvrenofviryel/resonatus-ontology/65918870c8cafcf64ef7d8dbace14571178829dd/profiles/v1.1/profile-activation.ttl [R=302,L]

# Versioned machine-readable result schema
RewriteRule ^strict/schema/validation-result/1\.1\.0/?$ https://raw.githubusercontent.com/halvrenofviryel/resonatus-ontology/65918870c8cafcf64ef7d8dbace14571178829dd/profiles/v1.1/schemas/validation-result.schema.json [R=302,L]

# Canonical strict ontology IRI -> currently approved strict vocabulary
RewriteRule ^strict/?$ https://raw.githubusercontent.com/halvrenofviryel/resonatus-ontology/65918870c8cafcf64ef7d8dbace14571178829dd/profiles/v1.1/ontology/resonatus-strict-vocabulary.ttl [R=302,L]
```

These rules are intended to be inserted before the existing root rule because `^$` must continue to
resolve the v1.0.0 core. They do not replace or edit either current v1.0.0 rule.

## Publication sequence

1. Owner approval of the permanent identifiers and normative profile contract — **complete**.
2. Promote the approved RC to final `1.1.0` artefacts and identifiers in a dedicated commit — **complete**.
3. Rerun package, portability, and repository regression gates; regenerate checksums — **complete**.
4. Push the immutable target and verify every raw HTTPS target — **complete**.
5. Prepare a minimal `perma-id/w3id.org` pull request touching only `ids/resonatus/.htaccess` —
   **authorized; submission pending**.
6. Run the w3id repository checks and manually test every redirect after merge.

The w3id pull request is authorized but has not yet been submitted. Redirect deployment and the live
checks in step 6 depend on external review and merge.
