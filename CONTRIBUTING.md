# Contributing

Thanks for helping. The bar for changes is simple: **every value needs a reason, and every claim needs to be honest about its evidence.**

## Changing a profile value

1. Change the value in `profiles/*.cfg` (keep the key order identical across all profiles).
2. Update the matching row in [docs/convars.md](docs/convars.md) with *why*, and fill the **Src** column: add new sources to [docs/sources.md](docs/sources.md), or write `reasoning` if you have none.
3. If you have measurements, add a report under [benchmarks/](benchmarks/).

## Adding a new convar

- It must appear in a `client.cfg` written by the current game build. If [reference/client.default.cfg](reference/client.default.cfg) is out of date, update it in the same PR (strip personal values like `client.autoconnect`).
- Add it to **all four** profiles and to `docs/convars.md`.
- If you aren't sure about its effect yet, add it to [docs/candidates.md](docs/candidates.md) instead.

## Adding a card

Card overlays and their pages are **generated**, so every card follows the same documented rules (R1–R5 in [gpu/cards/README.md](gpu/cards/README.md)):

1. Add a row to `CARDS` in [tools/gen_cards.py](tools/gen_cards.py): specs from the TechPowerUp GPU database, a profile estimate, and card-specific notes.
2. Run `python tools/gen_cards.py`. This also updates the "Find your card" list in the main README.

Don't hand-edit files in `gpu/cards/`; they get overwritten. To change a rule, change the generator and the rule table together.

## Adding a vendor overlay

See the roadmap in [gpu/README.md](gpu/README.md). Overlays should only contain vendor- or class-specific settings, plus a table explaining each one.

## After a game update

Rust updates monthly and convars sometimes get renamed or removed. After a major update:

1. Launch the game, quit, and diff your new `client.cfg` keys against `reference/client.default.cfg`.
2. Open an issue or PR listing renamed/removed convars.
