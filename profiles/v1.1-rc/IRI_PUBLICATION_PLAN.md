# Resonatus strict-profile IRI publication plan

**Status:** permanent identifier contract owner-approved; application not authorized

## Existing state verified on 2026-10-11

The live `perma-id/w3id.org` configuration under `ids/resonatus/.htaccess` contains two rules only:

- `https://w3id.org/resonatus` → the immutable v1.0.0 ontology content;
- `https://w3id.org/resonatus/1.0.0` → the same immutable v1.0.0 content.

There is no `strict` rule, which explains the observed HTTP 404. Those two existing rules must remain
unchanged.

The candidate vocabulary is already available over HTTPS from the pushed preservation commit:

```text
https://raw.githubusercontent.com/halvrenofviryel/resonatus-ontology/3e2821a6f9643234e20ac129caf509b909b924e0/profiles/v1.1-rc/ontology/resonatus-strict-vocabulary.ttl
```

The remote bytes matched the local candidate with SHA-256
`7fab06c5dc40a7e3c1431d0b88c992630c5d7eb9e0e3d8ef44a930a31862a599`.

## Recommended permanent identifier contract

The owner approved these identifiers for final v1.1.0 artefact preparation:

| Role | Identifier |
|---|---|
| Term namespace | `https://w3id.org/resonatus/strict#` |
| Ontology IRI | `https://w3id.org/resonatus/strict` |
| Final version IRI | `https://w3id.org/resonatus/strict/1.1.0` |
| Strict Linear profile | `https://w3id.org/resonatus/strict/profile/strict-linear/1.1.0` |
| Strict Assessment profile | `https://w3id.org/resonatus/strict/profile/strict-assessment/1.1.0` |
| Validation-result schema | `https://w3id.org/resonatus/strict/schema/validation-result/1.1.0` |

The `1.1.0-rc.1` identifiers in the local candidate remain prerelease identifiers. The recommended
promotion policy is to mint the final identifiers above only after owner approval, update the promoted
artefacts once, rerun all gates, and target an immutable release commit. Whether the RC identifiers
also receive archival redirects is a separate owner choice; they must not silently become final IRIs.

## Proposed w3id rule shape

The following is a review template, not an `.htaccess` change. Replace both placeholders only after the
final target exists and is byte-verified over HTTPS:

```apache
# Strict-profile versioned vocabulary -> immutable approved release content
RewriteRule ^strict/1\.1\.0/?$ https://raw.githubusercontent.com/halvrenofviryel/resonatus-ontology/<APPROVED_RELEASE_COMMIT>/profiles/v1.1/ontology/resonatus-strict-vocabulary.ttl [R=302,L]

# Versioned profile activation identifiers -> immutable approved release content
RewriteRule ^strict/profile/strict-linear/1\.1\.0/?$ https://raw.githubusercontent.com/halvrenofviryel/resonatus-ontology/<APPROVED_RELEASE_COMMIT>/profiles/v1.1/profile-activation.ttl [R=302,L]
RewriteRule ^strict/profile/strict-assessment/1\.1\.0/?$ https://raw.githubusercontent.com/halvrenofviryel/resonatus-ontology/<APPROVED_RELEASE_COMMIT>/profiles/v1.1/profile-activation.ttl [R=302,L]

# Versioned machine-readable result schema
RewriteRule ^strict/schema/validation-result/1\.1\.0/?$ https://raw.githubusercontent.com/halvrenofviryel/resonatus-ontology/<APPROVED_RELEASE_COMMIT>/profiles/v1.1/schemas/validation-result.schema.json [R=302,L]

# Canonical strict ontology IRI -> currently approved strict vocabulary
RewriteRule ^strict/?$ https://raw.githubusercontent.com/halvrenofviryel/resonatus-ontology/<APPROVED_RELEASE_COMMIT>/profiles/v1.1/ontology/resonatus-strict-vocabulary.ttl [R=302,L]
```

These rules are intended to be inserted before the existing root rule because `^$` must continue to
resolve the v1.0.0 core. They do not replace or edit either current v1.0.0 rule.

## Publication sequence

1. Owner approval of the permanent identifiers and normative profile contract — **complete**.
2. Promote the approved RC to final `1.1.0` artefacts and identifiers in a dedicated commit.
3. Rerun package, portability, and repository regression gates; regenerate checksums.
4. Push the immutable target and verify every raw HTTPS target.
5. After separate authorization, prepare a minimal `perma-id/w3id.org` pull request touching only
   `ids/resonatus/.htaccess`.
6. Run the w3id repository checks and manually test every redirect after merge.

No w3id fork, branch, commit, or pull request was created during RC preparation.
