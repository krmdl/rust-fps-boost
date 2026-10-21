# Rust Optimized Configs

Documented, reproducible `client.cfg` profiles for **Rust** (Facepunch), built mainly for **low-end and mid-range PCs**.

Every value in every profile has a written reason: what it costs (CPU, GPU, VRAM or RAM), what you lose visually, and whether it changes how well you can see other players. No "trust me bro" tweaks.

## Profiles

| Profile | Target hardware | Goal |
|---|---|---|
| [`ultra-low`](profiles/ultra-low.cfg) | iGPU / laptops / 4-core CPUs / 8 GB RAM / ≤2 GB VRAM | Playable FPS at any cost to visuals |
| [`low`](profiles/low.cfg) | GTX 1050 Ti–1650, RX 570–5500, 16 GB RAM | High, stable FPS while keeping the game readable |
| [`balanced`](profiles/balanced.cfg) | GTX 1660 / RTX 2060–3060 / RX 6600 | Good visuals, cuts the expensive effects that add little |
| [`quality`](profiles/quality.cfg) | RTX 3070+ / RX 6800+ | Best visuals, skipping effects that hurt visibility |

After a profile, you can apply an optional **GPU overlay** from [`gpu/`](gpu/) (NVIDIA Reflex/DLSS, AMD, Intel iGPU). See [gpu/README.md](gpu/README.md).

## Quick start

1. **Close Rust completely.** Rust overwrites `client.cfg` when it exits.
2. Run the installer from this repo's folder (it backs up your current config first):

   ```powershell
   powershell -ExecutionPolicy Bypass -File tools\apply.ps1 -Profile low
   ```

   Add a GPU overlay if you want one:

   ```powershell
   powershell -ExecutionPolicy Bypass -File tools\apply.ps1 -Profile low -Gpu nvidia
   ```

3. Launch Rust.

The installer only changes the convars listed in the profile. Your sensitivity, FOV, audio, binds and crosshair stay as they are. For manual install and restoring a backup, see [docs/install.md](docs/install.md).

## Documentation

- [docs/convars.md](docs/convars.md): **the rationale table**, every convar we touch and why
- [docs/profiles.md](docs/profiles.md): design goals of each profile
- [docs/methodology.md](docs/methodology.md): how we measure (and how you can too)
- [docs/launch-options.md](docs/launch-options.md): Steam launch options, including which popular ones are myths
- [docs/candidates.md](docs/candidates.md): experimental convars still waiting to be tested
- [reference/client.default.cfg](reference/client.default.cfg): full convar dump from the current game build

## Principles

1. **Only real convars.** Each profile key must appear in a `client.cfg` that the game itself wrote ([reference dump](reference/client.default.cfg)). Copy-pasted folklore is out.
2. **Never touch personal preferences.** Sensitivity, FOV, audio, UI scale, crosshair, binds and FPS cap belong to you.
3. **Visibility first.** Low profiles remove clutter (grass, post-processing) that hides players. We never ship a setting just because it gives a visual advantage, and we flag any setting that does.
4. **Measured, not guessed.** Every profile states its benchmark status. Until there's data, an entry says *expected* impact, never *measured*.

## Status

`v0.1`. The profiles are built from how each convar works, not from benchmarks yet. Benchmark contributions are very welcome: see [benchmarks/README.md](benchmarks/README.md).

## License

MIT. See [LICENSE](LICENSE). Not affiliated with Facepunch Studios.
