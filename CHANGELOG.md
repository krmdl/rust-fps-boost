# Changelog

## v0.2.0 – 2026-10-21

- Card overlays for 16 popular GPUs (GTX 1050 Ti → RTX 5070, RX 580 → RX 9070 XT), each with a page explaining every value
- Card list based on the September 2026 Steam Hardware Survey plus low-end cards
- `tools/gen_cards.py` generates overlays and pages from one table, using documented rules R1–R5
- `apply.ps1 -Gpu` accepts card names
- `docs/sources.md` with a source for every claim; unsourced claims marked as reasoning

## v0.1.0 – 2026-10-21

- Initial profiles: `ultra-low`, `low`, `balanced`, `quality`
- GPU overlays: `nvidia`, `amd`, `intel-igpu`
- `tools/apply.ps1` merge installer with backup and dry run
- Rationale docs for every convar, launch-option myth list, benchmark methodology
- Reference convar dump from the current game build
