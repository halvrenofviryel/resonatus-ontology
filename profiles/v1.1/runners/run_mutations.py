#!/usr/bin/env python3
"""Run all 27 validated mutations against the v1.1 namespace, vocabulary, and shapes."""
from package_common import (
    PROTOTYPE,
    PACKAGE,
    STRICT,
    STRICT_TERMS,
    package_shapes,
    configure_prototype_module,
    migrated_parse_union,
)

configure_prototype_module()

import run_prototype_mutations as mutations  # noqa: E402


def main() -> int:
    mutations.EXP = STRICT_TERMS
    mutations.FIX = PROTOTYPE / "fixtures"
    mutations.EXPERIMENTAL_VOCAB = PACKAGE / "ontology/resonatus-strict-vocabulary.ttl"
    mutations.parse_union = migrated_parse_union
    mutations.profile_shapes = package_shapes
    return mutations.main()


if __name__ == "__main__":
    raise SystemExit(main())
