# Causal-relation reuse decision

**Decision:** no external relation is adopted in this task

**Status:** `REQUIRES_OWNER_DECISION` before any production IRI or alignment
**Evidence date:** 2026-10-11

## Required relation

The bounded profile needs a directed edge between two modeled causal-spine stages:

> `x exp:causallyPrecedes y` means that x is asserted to make a causal contribution to y and is the
> selected upstream edge at the declared modelling granularity.

Required characteristics:

- direction from upstream cause/process stage to downstream effect/process stage;
- irreflexive and asymmetric;
- not declared transitive;
- no requirement that all of x ends before any of y begins;
- directness is relative to the profile's declared granularity;
- no implication of process parthood, shared participant, or carrier identity;
- assertion is ontic; the evidence and assessor's claim are separate.

The label “causally precedes” is provisional. It must not be read as BFO temporal `precedes`.

## Candidate comparison

| Candidate | Published semantics | Fit | Decision |
|---|---|---|---|
| BFO `precedes` (`BFO_0000063`) | Strict temporal order: the upstream occurrent's last instant is before or coincident with the downstream occurrent's first instant; transitive | Excludes overlapping causal processes and says nothing about causation | Reject as causal edge; usable only for a separate temporal assertion |
| BFO `occurrent part of` / `has temporal part` | Mereological relations among occurrents | Useful if path unity later uses parthood, but parthood is neither direction nor causation | Do not substitute |
| BFO participation/carrier relations | Relate processes to participants or information patterns to carriers | Relevant to a later carrier-continuity profile, not the causal edge itself | Do not substitute |
| RO `causally upstream of` (`RO_0002411`) | Transitive; subproperty of BFO `precedes`; excludes being an occurrent part of the downstream process | Strong standard candidate, but its BFO temporal parent conflicts with required overlap and it is not an adjacency relation | Do not adopt for the initial edge |
| RO `immediately causally upstream of` (`RO_0002412`) | Requires the upstream end to coincide with the downstream beginning | Too strict for overlapping processes and a different meaning of “immediate” | Reject |
| RO `causally upstream of or within` (`RO_0002418`) | Transitive causal relation allowing upstream-or-within cases and part propagation | Too broad for one selected adjacency edge and conflates upstream with within | Possible super-relation only; no alignment now |
| RO `causal relation between processes` (`RO_0002501`) | Broad grouping relation; official curator note says not to use it directly | Under the profile contract it supplies neither required direction nor adjacency | Reject for direct use |
| PROV-O `influenced` / `wasInfluencedBy` | Broad provenance influence among entities, activities, or agents | Preserves provenance interoperability but does not establish causal semantics; inverse orientation must also be handled carefully | At most a future broad superproperty mapping |
| PROV-O `wasInformedBy` | Activity dependency suggesting generation/use communication | Suitable for some information-flow cases only | Reject as cross-domain causal edge |
| `res:directlyContinues` | Published path-to-path relation whose domain/range are `CausalTraceProcess`; intentionally non-transitive | Relates complete trace processes, not internal spine stages; repurposing it would change a published IRI | Preserve unchanged |
| DOLCE temporal parts/participation | Unity tools for perdurants through temporal parts and participants | Useful for later process-identity analysis, not an exact generic direct-causal property | Do not substitute |
| Disease causal-chain approaches | Model domain-specific causal links, fading, branching, and identity | Confirm that linked occurrents need more than a shared origin, but do not supply a cross-domain drop-in relation | Reuse design lessons, not an IRI |

## Source basis

- [BFO 2020 core](https://github.com/BFO-ontology/BFO-2020/blob/master/21838-2/owl/bfo-core.ttl)
  defines process, temporal/occurrent parthood, participation, and `precedes`.
- [RO's causal-relation guide](https://oborel.github.io/obo-relations/causal-relations/) distinguishes
  directness, regulatory/non-regulatory influence, and effect direction.
- The inspected [RO release ontology](http://purl.obolibrary.org/obo/ro.owl) identifies version
  2026-09-04 and supplies the axioms and curator notes summarized above.
- [PROV-O](https://www.w3.org/TR/prov-o/) treats influence as a broad provenance relation and recommends
  more specific relations when applicable.
- The prior local comparison in
  [CAUSAL_CONTINUITY_AND_IDENTITY.md](../../CAUSAL_CONTINUITY_AND_IDENTITY.md) covers DOLCE and
  causal-chain literature, including
  [Rovetto and Mizoguchi](https://doi.org/10.3233/AO-150147) and
  [Kozaki et al.](https://ceur-ws.org/Vol-897/sessionJ-paper26.pdf).

## Why RO is not automatically selected

RO is the closest established vocabulary, but relation names are not enough. In the inspected release:

- `RO_0002411` is transitive and a subproperty of BFO `precedes`;
- `RO_0002412` fixes an end/begin coincidence;
- `RO_0002418` admits “within” cases and is transitive;
- `RO_0002501` is explicitly a grouping relation not intended for direct use.

The strict profile deliberately permits overlapping causal stages and needs a non-transitive,
granularity-relative edge. Declaring equivalence or subproperty alignment now would add temporal and
closure commitments that the prototype neither tests nor intends.

## Decision

Retain `exp:causallyPrecedes` only as an experimental test predicate. Before promotion, the owner must
choose one of:

1. mint a Resonatus production relation with the exact contract above;
2. revise the contract to match one RO relation and adopt that relation;
3. use a Resonatus narrow relation and align it only to a demonstrably compatible broad superproperty.

No equivalence, subproperty, import, or production namespace decision is made here.

## Separate dimensions that must remain separate

| Dimension | Representation candidate | Not equivalent to |
|---|---|---|
| Temporal precedence | BFO `precedes` or OWL-Time interval relation | Causation |
| Direct causal adjacency | Experimental Resonatus edge pending decision | Transitive causal ancestry |
| Indirect causal ancestry | Transitive closure/query/profile, if later approved | One asserted direct edge |
| Process parthood | BFO occurrent/temporal parthood | Causal direction |
| Participant/carrier continuity | BFO participation, carrier, or domain relation | Process identity by itself |

This separation also preserves overlapping causal processes: a causal edge may hold without BFO
`precedes`.
