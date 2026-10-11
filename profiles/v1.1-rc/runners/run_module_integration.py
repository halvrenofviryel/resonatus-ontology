#!/usr/bin/env python3
"""Run the 26 A/B/C OWL integration checks with the RC vocabulary."""
import rdflib

from rc_common import PROTOTYPE, RC, STRICT, configure_prototype_module, migrated_parse_union

configure_prototype_module()

import run_owl_module_integration as integration  # noqa: E402


def main() -> int:
    integration.EXP = STRICT
    integration.EXPERIMENTAL_VOCAB = RC / "ontology/resonatus-strict-vocabulary.ttl"
    fix = PROTOTYPE / "fixtures"
    integration.CASES = {
        "VALID_B": migrated_parse_union((fix / "b-valid-process-path.ttl",)),
        "VALID_C": migrated_parse_union(
            (fix / "b-valid-process-path.ttl", fix / "c-valid-overlay.ttl")
        ),
        "COLLAPSED_SCOPE": migrated_parse_union(
            (fix / "b-valid-process-path.ttl", fix / "c-invalid-scope-is-process-overlay.ttl")
        ),
        "CLAIM_ONLY": migrated_parse_union((fix / "claim-only-no-ontic-causation.ttl",)),
    }
    isolated = rdflib.Graph()
    isolated.add((integration.EX.isolatedClaim, rdflib.RDF.type, STRICT.CausalAttributionClaim))
    isolated.add((integration.EX.isolatedClaim, STRICT.causalSubject, integration.EX.isolatedSubject))
    isolated.add((integration.EX.isolatedClaim, STRICT.causalObject, integration.EX.isolatedObject))
    integration.CASES["ISOLATED_CLAIM"] = isolated
    integration.RELEVANT_CLASSES = (
        str(integration.RES.Resonatus),
        str(integration.RES.ResonatusPath),
        str(integration.RES.ContinuationPath),
        str(integration.RES.CausalTraceProcess),
        str(STRICT.AssessmentScope),
        str(STRICT.CausalAttributionClaim),
    )
    return integration.main()


if __name__ == "__main__":
    raise SystemExit(main())
