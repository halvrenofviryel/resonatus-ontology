#!/usr/bin/env python3
from pathlib import Path
from rdflib import Graph
import sys
ROOT=Path(__file__).resolve().parents[1]
g=Graph()
for rel in ['ontology/resonatus.ttl','alignments/resonatus-bfo.ttl','shapes/resonatus.shacl.ttl']:
    g.parse(ROOT/rel, format='turtle')
qs=sorted((ROOT/'competency-queries').glob('*.rq'))
failed=[]
for q in qs:
    result=bool(g.query(q.read_text()).askAnswer)
    print(('PASS' if result else 'FAIL'), q.name)
    if not result: failed.append(q.name)
print(f'SUMMARY {len(qs)-len(failed)}/{len(qs)} executable structural competency queries passed')
if failed: sys.exit(1)
