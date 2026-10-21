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

Click your card to open its config, or a profile to open that profile. Apply the card config on top of the profile for your resolution. **Why?** opens the page explaining every value.

<!-- readme-cards:start -->
#### NVIDIA GeForce

| Card | VRAM | Tier | 1080p | 1440p | |
|---|---|---|---|---|---|
| [**GTX 1050 Ti**](gpu/cards/gtx-1050-ti.cfg) | 4 GB | Entry | [`low`](profiles/low.cfg) | [`ultra-low`](profiles/ultra-low.cfg) | [Why?](gpu/cards/gtx-1050-ti.md) |
| [**GTX 1060 6GB**](gpu/cards/gtx-1060-6gb.cfg) | 6 GB | Entry | [`low`](profiles/low.cfg) | [`ultra-low`](profiles/ultra-low.cfg) | [Why?](gpu/cards/gtx-1060-6gb.md) |
| [**GTX 1060 3GB**](gpu/cards/gtx-1060-3gb.cfg) | 3 GB | Entry | [`low`](profiles/low.cfg) | [`ultra-low`](profiles/ultra-low.cfg) | [Why?](gpu/cards/gtx-1060-3gb.md) |
| [**GTX 1650**](gpu/cards/gtx-1650.cfg) | 4 GB | Entry | [`low`](profiles/low.cfg) | [`ultra-low`](profiles/ultra-low.cfg) | [Why?](gpu/cards/gtx-1650.md) |
| [**GTX 1660 Super**](gpu/cards/gtx-1660-super.cfg) | 6 GB | Entry | [`low`](profiles/low.cfg) | [`low`](profiles/low.cfg) | [Why?](gpu/cards/gtx-1660-super.md) |
| [**RTX 2060**](gpu/cards/rtx-2060.cfg) | 6 GB | Mid-range | [`balanced`](profiles/balanced.cfg) | [`low`](profiles/low.cfg) | [Why?](gpu/cards/rtx-2060.md) |
| [**RTX 3050**](gpu/cards/rtx-3050.cfg) | 8 GB | Entry | [`low`](profiles/low.cfg) | [`low`](profiles/low.cfg) | [Why?](gpu/cards/rtx-3050.md) |
| [**RTX 3060**](gpu/cards/rtx-3060.cfg) | 12 GB | Mid-range | [`balanced`](profiles/balanced.cfg) | [`balanced`](profiles/balanced.cfg) | [Why?](gpu/cards/rtx-3060.md) |
| [**RTX 4060**](gpu/cards/rtx-4060.cfg) | 8 GB | Mid-range | [`balanced`](profiles/balanced.cfg) | [`balanced`](profiles/balanced.cfg) | [Why?](gpu/cards/rtx-4060.md) |
| [**RTX 5060**](gpu/cards/rtx-5060.cfg) | 8 GB | Mid-range | [`balanced`](profiles/balanced.cfg) | [`balanced`](profiles/balanced.cfg) | [Why?](gpu/cards/rtx-5060.md) |
| [**RTX 5060 Ti**](gpu/cards/rtx-5060-ti.cfg) | 8 GB | High-end | [`quality`](profiles/quality.cfg) | [`balanced`](profiles/balanced.cfg) | [Why?](gpu/cards/rtx-5060-ti.md) |
| [**RTX 5070**](gpu/cards/rtx-5070.cfg) | 12 GB | High-end | [`quality`](profiles/quality.cfg) | [`quality`](profiles/quality.cfg) | [Why?](gpu/cards/rtx-5070.md) |

#### AMD Radeon

| Card | VRAM | Tier | 1080p | 1440p | |
|---|---|---|---|---|---|
| [**RX 580 8GB**](gpu/cards/rx-580-8gb.cfg) | 8 GB | Entry | [`low`](profiles/low.cfg) | [`ultra-low`](profiles/ultra-low.cfg) | [Why?](gpu/cards/rx-580-8gb.md) |
| [**RX 580 4GB**](gpu/cards/rx-580-4gb.cfg) | 4 GB | Entry | [`low`](profiles/low.cfg) | [`ultra-low`](profiles/ultra-low.cfg) | [Why?](gpu/cards/rx-580-4gb.md) |
| [**RX 6600**](gpu/cards/rx-6600.cfg) | 8 GB | Mid-range | [`balanced`](profiles/balanced.cfg) | [`low`](profiles/low.cfg) | [Why?](gpu/cards/rx-6600.md) |
| [**RX 9070 XT**](gpu/cards/rx-9070-xt.cfg) | 16 GB | High-end | [`quality`](profiles/quality.cfg) | [`quality`](profiles/quality.cfg) | [Why?](gpu/cards/rx-9070-xt.md) |
<!-- readme-cards:end -->

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
