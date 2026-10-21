<div align="center">

# Rust FPS Boost

**More FPS in Rust on low-end PCs, and every setting tells you why.**

The best Rust settings for your graphics card, as documented `client.cfg` configs for **Rust (the Facepunch game)**.<br>
4 profiles from potato PC to RTX, 16 per-GPU configs, a one-click installer with backup.<br>
No placebo tweaks, no launch-option myths, no copy-pasted folklore.

![Rust build](https://img.shields.io/badge/tested%20on-Rust%20Oct%202026-cd412b)
![GPU overlays](https://img.shields.io/badge/GPU%20overlays-16-informational)
![Sourced](https://img.shields.io/badge/every%20value-sourced%20or%20labelled-success)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

[**Install**](#install-in-2-minutes) · [Find your GPU](#find-your-card) · [Why each setting?](docs/convars.md) · [Launch option myths](docs/launch-options.md) · [FAQ](docs/faq.md)

</div>

## Install in 2 minutes

1. Click the green **Code** button → **Download ZIP**. Right-click the ZIP → **Extract All**.
2. **Quit Rust completely.** Rust saves its settings when it closes and would undo ours.
3. Open the extracted folder and double-click **`install.bat`**, then choose **1**.
   It finds Rust, **detects your graphics card**, suggests a profile, and backs up your current config first.
4. Start Rust. Changed your mind? Run `install.bat` again: **3** undoes the last install, **4** restores your original config.

Your sensitivity, FOV, binds, audio and crosshair are **never touched**.

> If Windows shows *"Windows protected your PC"*, click **More info → Run anyway**. The installer is plain text: [read it first](tools/apply.ps1) if you like.
> Prefer typing? `powershell -ExecutionPolicy Bypass -File tools\apply.ps1 -Preset low -Gpu gtx-1650`. More in [docs/install.md](docs/install.md).

## Find your card

Click your card to open its config, or a profile to open that profile. Pick the profile for your screen resolution; the card file adds a few card-specific tweaks on top. **Why?** explains every value. `install.bat` picks all of this for you.

<!-- readme-cards:start -->
#### NVIDIA GeForce

| Card | VRAM | 1080p | 1440p | |
|---|---|---|---|---|
| [**GTX 1050 Ti**](gpu/cards/gtx-1050-ti.cfg) | 4 GB | [`low`](profiles/low.cfg) | [`ultra-low`](profiles/ultra-low.cfg) | [Why?](gpu/cards/gtx-1050-ti.md) |
| [**GTX 1060 3GB**](gpu/cards/gtx-1060-3gb.cfg) | 3 GB | [`low`](profiles/low.cfg) | [`ultra-low`](profiles/ultra-low.cfg) | [Why?](gpu/cards/gtx-1060-3gb.md) |
| [**GTX 1060 6GB**](gpu/cards/gtx-1060-6gb.cfg) | 6 GB | [`low`](profiles/low.cfg) | [`ultra-low`](profiles/ultra-low.cfg) | [Why?](gpu/cards/gtx-1060-6gb.md) |
| [**GTX 1650**](gpu/cards/gtx-1650.cfg) | 4 GB | [`low`](profiles/low.cfg) | [`ultra-low`](profiles/ultra-low.cfg) | [Why?](gpu/cards/gtx-1650.md) |
| [**GTX 1660 Super**](gpu/cards/gtx-1660-super.cfg) | 6 GB | [`low`](profiles/low.cfg) | [`low`](profiles/low.cfg) | [Why?](gpu/cards/gtx-1660-super.md) |
| [**RTX 2060**](gpu/cards/rtx-2060.cfg) | 6 GB | [`balanced`](profiles/balanced.cfg) | [`low`](profiles/low.cfg) | [Why?](gpu/cards/rtx-2060.md) |
| [**RTX 3050**](gpu/cards/rtx-3050.cfg) | 8 GB | [`low`](profiles/low.cfg) | [`low`](profiles/low.cfg) | [Why?](gpu/cards/rtx-3050.md) |
| [**RTX 3060**](gpu/cards/rtx-3060.cfg) | 12 GB | [`balanced`](profiles/balanced.cfg) | [`balanced`](profiles/balanced.cfg) | [Why?](gpu/cards/rtx-3060.md) |
| [**RTX 4060**](gpu/cards/rtx-4060.cfg) | 8 GB | [`balanced`](profiles/balanced.cfg) | [`balanced`](profiles/balanced.cfg) | [Why?](gpu/cards/rtx-4060.md) |
| [**RTX 5060**](gpu/cards/rtx-5060.cfg) | 8 GB | [`balanced`](profiles/balanced.cfg) | [`balanced`](profiles/balanced.cfg) | [Why?](gpu/cards/rtx-5060.md) |
| [**RTX 5060 Ti**](gpu/cards/rtx-5060-ti.cfg) | 8 GB | [`quality`](profiles/quality.cfg) | [`balanced`](profiles/balanced.cfg) | [Why?](gpu/cards/rtx-5060-ti.md) |
| [**RTX 5070**](gpu/cards/rtx-5070.cfg) | 12 GB | [`quality`](profiles/quality.cfg) | [`quality`](profiles/quality.cfg) | [Why?](gpu/cards/rtx-5070.md) |

#### AMD Radeon

| Card | VRAM | 1080p | 1440p | |
|---|---|---|---|---|
| [**RX 580 4GB**](gpu/cards/rx-580-4gb.cfg) | 4 GB | [`low`](profiles/low.cfg) | [`ultra-low`](profiles/ultra-low.cfg) | [Why?](gpu/cards/rx-580-4gb.md) |
| [**RX 580 8GB**](gpu/cards/rx-580-8gb.cfg) | 8 GB | [`low`](profiles/low.cfg) | [`ultra-low`](profiles/ultra-low.cfg) | [Why?](gpu/cards/rx-580-8gb.md) |
| [**RX 6600**](gpu/cards/rx-6600.cfg) | 8 GB | [`balanced`](profiles/balanced.cfg) | [`low`](profiles/low.cfg) | [Why?](gpu/cards/rx-6600.md) |
| [**RX 9070 XT**](gpu/cards/rx-9070-xt.cfg) | 16 GB | [`quality`](profiles/quality.cfg) | [`quality`](profiles/quality.cfg) | [Why?](gpu/cards/rx-9070-xt.md) |
<!-- readme-cards:end -->

Recommendations are estimates until benchmarked ([how cards are tuned](gpu/cards/README.md)). Card not listed? `install.bat` falls back to a vendor overlay (`nvidia`, `amd`, `intel-igpu`); see [gpu/README.md](gpu/README.md).

## Profiles

| Profile | Built for | Goal |
|---|---|---|
| [`ultra-low`](profiles/ultra-low.cfg) | Integrated graphics, old laptops, 4-core CPUs, 8 GB RAM | Playable FPS at any cost to visuals |
| [`low`](profiles/low.cfg) | GTX 1050 Ti–1660, RX 580, 16 GB RAM | High, stable FPS while keeping the game readable |
| [`balanced`](profiles/balanced.cfg) | RTX 2060–5060, RX 6600 | Good visuals, minus the expensive effects that add little |
| [`quality`](profiles/quality.cfg) | RTX 5060 Ti and up, RX 9070 XT | Best visuals, skipping effects that hurt visibility |

Design goals of each profile: [docs/profiles.md](docs/profiles.md).

## Why trust this over an "FPS BOOST 2026" video?

- ✅ **Only real convars.** Every setting exists in a `client.cfg` written by the current game build. [CI checks this](tools/validate.py) on every commit.
- 📚 **Every value has a reason and a source:** Facepunch devblogs, Unity engine docs, NVIDIA, third-party measurements, or an honest `reasoning` label. [See the table →](docs/convars.md)
- 🎯 **Visibility first.** We keep shadows on (they give away enemies), cut effects that wash out your view (bloom, sun shafts, motion blur), and flag every setting that gives a visual edge.
- 🚫 **Myths called out.** `-maxMem`, `-malloc=system`, `-cpuCount`, `-high` aren't in Unity's argument list. [Which launch options do nothing →](docs/launch-options.md)
- 📏 **Expected vs measured.** Nothing is called "measured" without a report in [`benchmarks/`](benchmarks/). On a GTX 1650, 1050 Ti or RX 580? [Your benchmark](../../issues/new?template=benchmark.yml) is the most useful contribution.

## Safety

- The configs contain only console variables (convars) that Rust itself writes to `cfg\client.cfg`, the same file the in-game Options menu saves to.
- Nothing is injected, no game files or memory are modified, and the installer refuses to run while Rust is open.
- The installer is readable PowerShell ([tools/apply.ps1](tools/apply.ps1)) and backs up your config before every change.
- We're not affiliated with Facepunch Studios or Easy Anti-Cheat and can't make guarantees on their behalf. Changing graphics settings in `client.cfg` is what the game's own menu does.

## FAQ

<details>
<summary><b>Did it work?</b></summary>

In Rust press **F1**, type `graphics.drawdistance` and press Enter. It should show the profile's value (1500 on `low`).
</details>

<details>
<summary><b>My settings went back to normal.</b></summary>

Picking a preset in Rust's Graphics menu overwrites these values, and big game updates can too. Quit Rust and run `install.bat` again.
</details>

<details>
<summary><b>How do I undo it?</b></summary>

`install.bat` → **3** (undo the last install) or **4** (your config from before the first install). Backups live next to your config in `Rust\cfg\`.
</details>

<details>
<summary><b>Will this give me 2× FPS?</b></summary>

No honest config can promise a number. On high-end PCs Rust is mostly limited by the CPU, so settings change less. The biggest gains are expected on low-end GPUs, which is who this project is built for. Measured results will appear in [`benchmarks/`](benchmarks/).
</details>

More questions and a glossary: [docs/faq.md](docs/faq.md).

## Documentation

| | |
|---|---|
| [docs/convars.md](docs/convars.md) | **The rationale table**: every convar we touch, why, and its source |
| [docs/sources.md](docs/sources.md) | Every source we rely on, and how strong each kind of evidence is |
| [docs/install.md](docs/install.md) | Manual install, installer options, restoring backups |
| [docs/launch-options.md](docs/launch-options.md) | Steam launch options, including which popular ones do nothing |
| [docs/methodology.md](docs/methodology.md) | How we benchmark, and how you can too |
| [docs/candidates.md](docs/candidates.md) | Experimental convars waiting to be tested |
| [docs/faq.md](docs/faq.md) | FAQ and glossary |

## Contributing

Benchmarks, new cards and corrections are welcome, especially corrections backed by a source. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT, see [LICENSE](LICENSE). Not affiliated with Facepunch Studios. "Rust" is a trademark of Facepunch Studios.
