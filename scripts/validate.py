#!/usr/bin/env python3
from pathlib import Path
import sys
from rdflib import Graph, Namespace, RDF

RES = Namespace('https://w3id.org/resonatus#')
CRITERIA = [RES.TraceCriterion, RES.DelayCriterion, RES.PropagationCriterion, RES.SelectivityCriterion, RES.TransformationFeedbackCriterion]
VALID_VERDICTS = {RES.PASS, RES.FAIL, RES.NOT_MEASURED, RES.INCONCLUSIVE, RES.ERROR}

def classify(vs):
    if any(v == RES.FAIL for v in vs):
        return 'NON_MEMBERSHIP_SUPPORTED'
    if all(v == RES.PASS for v in vs):
        return 'MEMBERSHIP_SUPPORTED'
    return 'UNDETERMINED'

def main(root):
    root = Path(root)
    # Syntax parse all shipped Turtle artefacts. This is syntax validation only, not OWL reasoning or SHACL conformance.
    # Skip environment / VCS directories so `validate.py .` reports only tracked artefacts regardless of any local .venv.
    _SKIP = {'.venv', '.git', '__pycache__'}
    ttl_files = sorted(f for f in root.rglob('*.ttl') if not any(part in _SKIP for part in f.parts))
    for f in ttl_files:
        Graph().parse(f, format='turtle')
    print(f'PARSE {len(ttl_files)} Turtle files: OK')
    total = passed = 0
    failures = []
    for f in sorted((root/'examples').glob('*.ttl')):
        total += 1
        g = Graph(); g.parse(root/'ontology'/'resonatus.ttl', format='turtle'); g.parse(f, format='turtle')
        assessments = list(g.subjects(RDF.type, RES.ResonatusAssessment))
        if len(assessments) != 1:
            failures.append((f.name, f'expected one assessment, found {len(assessments)}')); continue
        a = assessments[0]
        subjects = list(g.objects(a, RES.assesses))
        cas = list(g.objects(a, RES.hasCriterionAssessment))
        if len(subjects) != 1 or len(cas) != 5:
            failures.append((f.name, 'cardinality failure')); continue
        by_crit = {}
        malformed = False
        for ca in cas:
            crits = list(g.objects(ca, RES.criterion)); verdicts = list(g.objects(ca, RES.verdict))
            if len(crits)!=1 or len(verdicts)!=1 or crits[0] not in CRITERIA or verdicts[0] not in VALID_VERDICTS:
                malformed = True; break
            if crits[0] in by_crit:
                malformed = True; break
            by_crit[crits[0]] = verdicts[0]
        if malformed or set(by_crit) != set(CRITERIA):
            failures.append((f.name, 'criterion uniqueness/completeness failure')); continue
        predicted = classify([by_crit[c] for c in CRITERIA])
        expected = str(next(g.objects(subjects[0], RES.expectedClassification)))
        if predicted != expected:
            failures.append((f.name, f'{predicted} != {expected}')); continue
        passed += 1
        print(f'PASS {f.name}: {predicted}')
    print(f'\nSUMMARY {passed}/{total} fixtures matched expected classification')
    if failures:
        for f,msg in failures: print('FAIL',f,msg)
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parents[1]))
