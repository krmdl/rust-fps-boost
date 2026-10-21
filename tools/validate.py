"""Checks the configs against the rules in CONTRIBUTING.md. Exits non-zero on failure.

1. Every profile has the same keys in the same order.
2. Every key in profiles/ and gpu/ exists in the game-written part of the reference dump.
3. Every line in a .cfg is a valid  key "value"  line.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINE = re.compile(r'^([A-Za-z0-9_.]+) "([^"]*)"$')


def read_cfg(path, errors):
    keys = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        m = LINE.match(line)
        if not m:
            errors.append(f"{path.relative_to(ROOT)}:{n}: not a 'key \"value\"' line: {line!r}")
            continue
        keys.append(m.group(1))
    return keys


def main():
    errors = []

    # Only the part the game wrote: everything before the first blank line.
    dump = (ROOT / "reference" / "client.dump.cfg").read_text(encoding="utf-8").split("\n\n")[0]
    known = {m.group(1) for m in map(LINE.match, dump.splitlines()) if m}

    profiles = sorted((ROOT / "profiles").glob("*.cfg"))
    orders = {p.name: read_cfg(p, errors) for p in profiles}
    first_name, first_keys = next(iter(orders.items()))
    for name, keys in orders.items():
        if keys != first_keys:
            errors.append(f"profiles/{name}: key order differs from profiles/{first_name}")

    for path in [*profiles, *sorted((ROOT / "gpu").rglob("*.cfg"))]:
        for key in read_cfg(path, []):
            if key not in known:
                errors.append(f"{path.relative_to(ROOT)}: '{key}' is not in reference/client.dump.cfg")

    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print(f"OK: {len(profiles)} profiles, all keys known ({len(known)} convars in reference dump)")


if __name__ == "__main__":
    main()
