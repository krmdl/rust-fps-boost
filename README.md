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

## Find your card

Each popular card has its own overlay and a page explaining every value. Apply it on top of the profile recommended for your resolution.

| Card | 1080p | 1440p |
|---|---|---|
| [GTX 1050 Ti](gpu/cards/gtx-1050-ti.md) | `low` | `ultra-low` |
| [GTX 1060 6GB](gpu/cards/gtx-1060-6gb.md) / [3GB](gpu/cards/gtx-1060-3gb.md) | `low` | `ultra-low` |
| [GTX 1650](gpu/cards/gtx-1650.md) | `low` | `ultra-low` |
| [GTX 1660 Super](gpu/cards/gtx-1660-super.md) | `low` | `low` |
| [RTX 2060](gpu/cards/rtx-2060.md) | `balanced` | `low` |
| [RTX 3050](gpu/cards/rtx-3050.md) | `low` | `low` |
| [RTX 3060](gpu/cards/rtx-3060.md) | `balanced` | `balanced` |
| [RTX 4060](gpu/cards/rtx-4060.md) | `balanced` | `balanced` |
| [RTX 5060](gpu/cards/rtx-5060.md) | `balanced` | `balanced` |
| [RTX 5060 Ti](gpu/cards/rtx-5060-ti.md) | `quality` | `balanced` |
| [RTX 5070](gpu/cards/rtx-5070.md) | `quality` | `quality` |
| [RX 580 8GB](gpu/cards/rx-580-8gb.md) / [4GB](gpu/cards/rx-580-4gb.md) | `low` | `ultra-low` |
| [RX 6600](gpu/cards/rx-6600.md) | `balanced` | `low` |
| [RX 9070 XT](gpu/cards/rx-9070-xt.md) | `quality` | `quality` |

```powershell
powershell -ExecutionPolicy Bypass -File tools\apply.ps1 -Profile low -Gpu gtx-1650
```

The recommendations are estimates until benchmarked. How the card overlays are built, and why these cards: [gpu/cards/README.md](gpu/cards/README.md).

Card not listed? Use a vendor overlay (`nvidia`, `amd`, `intel-igpu`). See [gpu/README.md](gpu/README.md).

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

- [docs/convars.md](docs/convars.md): **the rationale table**, every convar we touch, why, and its source
- [docs/sources.md](docs/sources.md): every source we rely on (Facepunch, Unity docs, NVIDIA), and how strong each kind of evidence is
- [docs/profiles.md](docs/profiles.md): design goals of each profile
- [docs/methodology.md](docs/methodology.md): how we measure (and how you can too)
- [docs/launch-options.md](docs/launch-options.md): Steam launch options, including which popular ones are myths
- [docs/candidates.md](docs/candidates.md): experimental convars still waiting to be tested
- [reference/client.default.cfg](reference/client.default.cfg): full convar dump from the current game build

## Principles

1. **Only real convars.** Each profile key must appear in a `client.cfg` that the game itself wrote ([reference dump](reference/client.default.cfg)). Copy-pasted folklore is out.
2. **Never touch personal preferences.** Sensitivity, FOV, audio, UI scale, crosshair, binds and FPS cap belong to you.
3. **Visibility first.** Low profiles remove clutter (grass, post-processing) that hides players. We never ship a setting just because it gives a visual advantage, and we flag any setting that does.
4. **Cited, then measured.** Every claim links to a source (Facepunch, Unity engine docs, NVIDIA) or is honestly labelled *reasoning*. Until there's benchmark data, an entry says *expected* impact, never *measured*.

## Status

`v0.1`. The profiles are built from how each convar works, not from benchmarks yet. Benchmark contributions are very welcome: see [benchmarks/README.md](benchmarks/README.md).

## License

MIT. See [LICENSE](LICENSE). Not affiliated with Facepunch Studios.
