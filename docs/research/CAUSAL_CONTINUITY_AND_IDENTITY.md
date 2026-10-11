# Causal Continuity and Identity

## Question

Does the current representation identify one coherent causal continuation, or does it group several
witnesses under one `ContinuationPath` individual?

## Answer

It groups typed witnesses under one individual and checks three reference agreements. It does not
currently identify a causal lineage.

This distinction is formal:

```text
Current OWL guarantee
  one path node
    has a Trace witness
    has a Delay witness
    has a Propagation witness
    has a Selectivity witness
    has a Transformation-or-Feedback witness

Current SHACL guarantee for a fully witnessed path
  declared origin = Trace causal-attribution target
  declared origin = Delay reference interaction
  Propagation receiver = Selectivity receiver

Not currently guaranteed
  Trace precedes or causes Propagation
  Delay is temporally after the origin's end
  Propagation carries the same trace
  Selectivity is the uptake of that propagation
  Transformation/Feedback affects or is caused by that uptake
  witness events are parts or stages of the path process
  path identity survives or splits at branch and merge points
```

`res:directlyContinues` does not close this gap. Its domain and range are `CausalTraceProcess`, it is
not used in the `ResonatusPath` definition, and no release fixture connects the five witness individuals
with it. Its asymmetry, irreflexivity, and non-transitivity are sensible local characteristics, but it is
currently orthogonal to membership.

## Shared origin is not shared lineage

A shared origin is a fan-out condition: several later things can be attributed to the same interaction.
That does not make them stages of one continuation. A shared lineage additionally needs an account of
how each later stage inherits, transmits, realizes, or is causally downstream of the prior stage.

The current profile also has two independent reference islands:

```text
origin island                           receiver island
-------------                           ---------------
declared origin                         propagation receiver
     =                                        =
Trace attribution target                selectivity dependency target
     =
Delay reference interaction
```

There is no formal bridge from the origin island to the receiver island, and the
Transformation/Feedback witness belongs to neither. Consequently, origin agreement is necessary for
the intended reading but not sufficient for lineage.

## Minimal counterexamples

### CE01 — grouped witnesses without lineage

[`counterexamples/ce01-grouped-witnesses-no-lineage.ttl`](counterexamples/ce01-grouped-witnesses-no-lineage.ttl)
contains distinct nodes for the five witness roles. All required origin/receiver references agree, but
there are no causal, temporal, participation, parthood, or continuation assertions between the five
witnesses. HermiT nevertheless entails `candidate rdf:type res:Resonatus`, and pySHACL reports
conformance with zero violations.

This is enough to refute the claim that lineage is *required* by the current formalization. Under OWL's
open-world semantics the absence of a lineage assertion does not prove that no lineage exists in the
world; it proves that the ontology does not need one to derive membership.

### CE02 — single-node collapse

[`counterexamples/ce02-single-node-collapse.ttl`](counterexamples/ce02-single-node-collapse.ttl) uses
one individual as candidate, path, originating interaction, receiver, Trace, Delay, Propagation,
Selectivity, and Transformation. All properties are self-links. The merged ontology is consistent,
HermiT entails membership, and SHACL reports zero violations.

The example is intentionally unrealistic. Its purpose is to expose missing distinctions: the prose
requires a post-interaction continuation and downstream uptake, while the logic permits the origin and
the allegedly post-origin continuation to be the same individual.

## Comparison with established approaches

### BFO 2020

BFO defines a process as an occurrent with temporal proper parts that depends on material entities, and
provides occurrent-part and temporal-part relations. Mapping `ContinuationPath` to BFO process is
therefore plausible only if the path denotes a real unfolding process. The current bridge does not make
the witness events parts of that process or state what material entities sustain it. Logical consistency
with BFO is necessary but does not answer the identity question.

Relevant BFO options should be evaluated before creating new relations:

- `has occurrent part` / `occurrent part of` for constituent events;
- `has temporal part` / `temporal part of` for temporally delimited process portions;
- participant/dependence relations for continuity through material or information-bearing entities;
- `history` only when the intended path is the complete history of a material entity, which is usually
  stronger than Resonatus needs.

### DOLCE

DOLCE treats events/perdurants through temporal parts and participation. Its value here is diagnostic:
calling a scope node an event is not enough; participants, temporal location, parthood, and unity must be
made explicit. No DOLCE bridge should be added until the path category is settled.

### PROV-O

PROV-O `Activity` is deliberately broad. `wasInfluencedBy` represents generic dependency, and W3C PROV
does not provide a domain-independent test for causation. The current mapping is therefore useful for
provenance but cannot establish continuity or causal identity. A causal relation may safely specialize
generic influence; generic influence must not be used as evidence for the causal relation in reverse.

### OBO Relation Ontology

RO distinguishes notions such as causal upstreamness, immediate causal upstreamness, regulation, and
input provision. This shows that “causally connected” is not a single interchangeable relation. If the
owner selects a lineage semantics that matches one of these relations, reuse is preferable to a new
Resonatus-specific property. Cross-domain fit must still be checked because RO's operational distinctions
come primarily from biological process modelling.

### Causal-process and causal-chain literature

Salmon/Dowe causal-process theories require transmission or possession of a conserved quantity and were
developed for physical causation. They should not be imported as a universal rule for memories, policies,
or information systems. Their relevant warning is structural: a temporally gerrymandered aggregate is
not a causal process merely because its stages are collected under one name.

Applied-ontology work on disease causal chains explicitly models causally linked occurrents and treats
branching, fading, historical links, and identity preservation as separate problems. That literature
does not supply a ready-made cross-domain definition for Resonatus, but it confirms that common origin
and membership in one container are insufficient identity criteria.

## Candidate lineage policies

No policy is selected here.

| Policy | Identity criterion | Strength | Main cost |
|---|---|---|---|
| P0: witness bundle | One scope node carries all five witness types. | Exactly matches v1.0.0. | Does not establish lineage; terminology must be weakened. |
| P1: ordered causal chain | Each stage is causally downstream of a preceding stage, with temporal compatibility. | Captures a path rather than a bag. | Needs a causal-link semantics and branch/merge rules. |
| P2: process parthood | Witness stages are occurrent/temporal parts of one process. | Fits BFO/DOLCE process structure. | Parthood alone does not establish causation or transmission. |
| P3: bearer/participant continuity | Adjacent stages share or transform a tracked participant, information bearer, disposition, or conserved feature. | Gives a lineage carrier. | A single carrier notion may not transfer across physical, cognitive, software, and social domains. |
| P4: domain profile | Core remains a witness bundle; domain profiles define lineage evidence and identity. | Honest cross-domain modularity. | Core membership is weaker and cross-domain comparability depends on profile mappings. |

A likely minimal architecture is P4 with P1/P2/P3 supplied by a domain profile. That is a research
recommendation, not an implemented change.

## Branch, merge, and granularity decisions

Before formalizing lineage, the owner must decide:

1. Does propagation to two receivers create two paths or one branching path?
2. If two upstream paths contribute to one transformation, is the result one merged path, two continuing
   paths, or a new path?
3. Can a path survive a gap with only a disposition, record, or latent state present?
4. Which changes preserve the same path, and which terminate it?
5. Is path identity tied to origin, carrier, causal link sequence, purpose, or assessment perspective?
6. At what granularity are interactions and witness stages individuated?

Without these answers, stronger axioms risk turning a modelling preference into an unsupported identity
criterion.

## Minimal recommendation

1. Immediately constrain documentation claims to the P0 guarantee.
2. Treat CE01 and CE02 as acceptance tests for any proposed v1.1 lineage profile: a genuine lineage
   profile should reject them for the intended reason.
3. Prototype P1–P4 in a non-normative branch and compare their inferences on independently built cases.
4. Reuse OWL-Time, BFO/RO, or another established relation where semantics match; mint a new relation
   only for a documented residual requirement.

## Sources

- [BFO 2020 OWL artefact](https://github.com/BFO-ontology/BFO-2020/blob/master/21838-2/owl/bfo-core.ttl)
- [W3C PROV Data Model](https://www.w3.org/TR/prov-dm/)
- [DOLCE official documentation](https://www.loa.istc.cnr.it/wp-content/uploads/2021/11/DOLCE_FOUST_2022.pdf)
- [OBO Relation Ontology causal relations](https://oborel.github.io/obo-relations/causal-relations/)
- [Dowe 1995, Causality and Conserved Quantities](https://doi.org/10.1086/289859)
- [Rovetto and Mizoguchi 2015, Causality and the Ontology of Disease](https://doi.org/10.3233/AO-150147)
- [Kozaki et al. 2012, Identity Tracking of a Disease as a Causal Chain](https://ceur-ws.org/Vol-897/sessionJ-paper26.pdf)
- [Garbacz et al., Two Approaches to the Identity of Processes in BFO](https://ceur-ws.org/Vol-3637/paper33.pdf)
