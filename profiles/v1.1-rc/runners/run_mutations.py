#!/usr/bin/env python3
"""Run all 27 validated mutations against the RC namespace, vocabulary, and shapes."""
from rc_common import (
    PROTOTYPE,
    RC,
    STRICT,
    STRICT_TERMS,
    candidate_shapes,
    configure_prototype_module,
    migrated_parse_union,
)

configure_prototype_module()

import run_prototype_mutations as mutations  # noqa: E402


def main() -> int:
    mutations.EXP = STRICT_TERMS
    mutations.FIX = PROTOTYPE / "fixtures"
    mutations.EXPERIMENTAL_VOCAB = RC / "ontology/resonatus-strict-vocabulary.ttl"
    mutations.parse_union = migrated_parse_union
    mutations.profile_shapes = candidate_shapes
    return mutations.main()


if __name__ == "__main__":
    raise SystemExit(main())
