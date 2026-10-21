# Reference dump

[`client.dump.cfg`](client.dump.cfg) is a complete `client.cfg` written by the Rust client (October 2026 build).

**Use it for the keys, not the values.** It shows which convars exist in the current build, and every key in our profiles and overlays must appear in it. CI checks this on every commit (`tools/validate.py`).

The **values** are one player's settings (sensitivity, FOV, audio and graphics choices), **not** the game's defaults. Don't read a value here as "what Rust ships with".

The last five lines (after the blank line) were added by hand, not written by the game. They're excluded from all profiles until someone confirms the convars exist.

## Updating after a game update

1. Quit Rust, launch it, change any setting, quit again. Rust rewrites `cfg\client.cfg` with every current convar.
2. Replace `client.dump.cfg` with that file. Strip anything personal you don't want public (e.g. `client.autoconnect`).
3. Run `python tools/validate.py`. It lists any profile key that no longer exists, which means a convar was renamed or removed.
