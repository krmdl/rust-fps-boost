## What changes

<!-- profile value / new convar / new card / docs / installer -->

## Checklist

- [ ] Every changed value has a row in `docs/convars.md` with a **Src** (source tag or `reasoning`)
- [ ] New convars exist in `reference/client.dump.cfg` and were added to **all four** profiles
- [ ] Card changes were made in `tools/gen_cards.py` and regenerated (no hand edits in `gpu/cards/`)
- [ ] `python tools/validate.py` and `python tools/gen_cards.py --check` pass
- [ ] A benchmark report is attached in `benchmarks/` (only if claiming *measured*)
- [ ] `CHANGELOG.md` updated
