#!/usr/bin/env python3
from pathlib import Path
import sys
from rdflib import Graph, Namespace, RDF, RDFS, OWL

ROOT = Path(__file__).resolve().parents[1]
RES = Namespace('https://w3id.org/resonatus#')
BFO_PROCESS = 'http://purl.obolibrary.org/obo/BFO_0000015'

def die(msg):
    print('FAIL', msg)
    sys.exit(1)

g=Graph().parse(ROOT/'ontology/resonatus.ttl', format='turtle')
bfo=Graph().parse(ROOT/'alignments/resonatus-bfo.ttl', format='turtle')

checks=[]
def check(name, cond):
    checks.append((name,bool(cond)))

check('TraceContinuation has explicit causallyAttributedTo restriction', any(
    (r, OWL.onProperty, RES.causallyAttributedTo) in g and
    (r, OWL.someValuesFrom, RES.Interaction) in g
    for r in g.objects(RES.TraceContinuation, RDFS.subClassOf)
))
check('Delay class is not subclass of TraceContinuation', (RES.PostInteractionContinuation, RDFS.subClassOf, RES.TraceContinuation) not in g)
check('Delay property is not subproperty of Trace property', (RES.hasPostInteractionContinuation, RDFS.subPropertyOf, RES.hasTraceContinuation) not in g)
check('directlyContinues is asymmetric', (RES.directlyContinues, RDF.type, OWL.AsymmetricProperty) in g)
check('directlyContinues is irreflexive', (RES.directlyContinues, RDF.type, OWL.IrreflexiveProperty) in g)
check('directlyContinues is not declared transitive', (RES.directlyContinues, RDF.type, OWL.TransitiveProperty) not in g)
# Selectivity tightening: ContextModulation now commits to uptake DEPENDENCE on a receiver
# context (res:uptakeDependsOn), not mere co-presence (res:hasReceiverContext). Migrated accordingly.
check('ContextModulation has uptake-dependence restriction (tightened Selectivity)', any(
    (r, OWL.onProperty, RES.uptakeDependsOn) in g and
    (r, OWL.someValuesFrom, RES.ReceiverContext) in g
    for r in g.objects(RES.ContextModulation, RDFS.subClassOf)
))
from rdflib import URIRef
check('BFO bridge maps candidate to BFO process', (RES.ResonatusCandidate, RDFS.subClassOf, URIRef(BFO_PROCESS)) in bfo)
check('BFO bridge maps interaction to BFO process', (RES.Interaction, RDFS.subClassOf, URIRef(BFO_PROCESS)) in bfo)
criteria={RES.TraceCriterion, RES.DelayCriterion, RES.PropagationCriterion, RES.SelectivityCriterion, RES.TransformationFeedbackCriterion}
check('Exactly five canonical criteria are instantiated', set(g.subjects(RDF.type, RES.Criterion)) == criteria)
verdicts={RES.PASS,RES.FAIL,RES.NOT_MEASURED,RES.INCONCLUSIVE,RES.ERROR}
check('Exactly five canonical verdicts are instantiated', set(g.subjects(RDF.type, RES.Verdict)) == verdicts)
check('AssessmentMethod class exists', (RES.AssessmentMethod,RDF.type,OWL.Class) in g)
check('CriterionAssessment can record method', (RES.usesAssessmentMethod,RDF.type,OWL.ObjectProperty) in g)

bad=[n for n,v in checks if not v]
for n,v in checks:
    print(('PASS' if v else 'FAIL'), n)
print(f'SUMMARY {len(checks)-len(bad)}/{len(checks)} structural checks passed')
if bad: sys.exit(1)
