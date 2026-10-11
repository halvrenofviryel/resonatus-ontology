#!/usr/bin/env python3
"""Run the 15 validated scenario oracles against migrated data and v1.1 shapes."""
from package_common import configure_prototype_module, prototype


def main() -> int:
    configure_prototype_module()
    return prototype.main()


if __name__ == "__main__":
    raise SystemExit(main())
