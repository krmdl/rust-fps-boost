# Best Rust settings for the NVIDIA GeForce GTX 1050 Ti

**Config file:** [`gtx-1050-ti.cfg`](gtx-1050-ti.cfg)

## Specs

| | |
|---|---|
| Architecture | Pascal |
| VRAM | 4 GB |
| Memory bus | 128-bit |
| Bandwidth | ~112 GB/s |
| NVIDIA Reflex | Yes |
| DLSS | No |

Source: TechPowerUp GPU database [[H2]](../../docs/sources.md#h2).

## Recommended setup

Easiest: double-click **`install.bat`** in the repo folder and pick **Install**. It detects this card and suggests the profile below. Or run the command for your resolution from the repo folder:

| Resolution | Profile | Command |
|---|---|---|
| 1080p | [`low`](../../profiles/low.cfg) | `powershell -ExecutionPolicy Bypass -File tools\apply.ps1 -Preset low -Gpu gtx-1050-ti` |
| 1440p | [`ultra-low`](../../profiles/ultra-low.cfg) | `powershell -ExecutionPolicy Bypass -File tools\apply.ps1 -Preset ultra-low -Gpu gtx-1050-ti` |

Profile choice is an **estimate** from this card's performance tier (rule R5). It hasn't been benchmarked yet. If you're on this card, a [benchmark report](../../benchmarks/README.md) is the most useful thing you can contribute.

## What this overlay sets, and why

| Convar | Value | Why | Src |
|---|---|---|---|
| `graphics.reflexmode` | 1 | R2: NVIDIA Reflex lowers input latency (GTX 900 series and newer). | [N1](../../docs/sources.md#n1), [N3](../../docs/sources.md#n3) |
| `graphics.dlss` / `graphics.dlaa` | -1 / False | R3: this card has no tensor cores, so DLSS and DLAA are forced off. | [N2](../../docs/sources.md#n2) |
| `graphicssettings.globaltexturemipmaplimit` | 1 | R1: 4 GB VRAM → half resolution textures. Overrides the profile value. | [U1](../../docs/sources.md#u1) |
| `graphics.af` | 16 | R4: anisotropic filtering is cheap on a discrete card's memory bandwidth. | reasoning |

Rules R1–R5 are explained in [the card overlay README](README.md#what-a-card-overlay-changes-and-the-rules-behind-it).

## Card-specific notes

- Often paired with older 4-core CPUs. If GPU usage stays well below 95% (Task Manager → Performance → GPU), you're CPU-bound: drop to `ultra-low` for its shorter LOD/tree distances rather than lowering resolution.
- At 1440p, try a lower render scale: press F1 in Rust, type `graphics.renderscale 0.75`, press Enter.

## Community reports

What players report on this card (Steam Community, howmanyfps). These are anecdotes: settings and location are often unknown, and we haven't reproduced them [[C5]](../../docs/sources.md#c5) [[C6]](../../docs/sources.md#c6).

- i7-2600K, 16 GB DDR3: ~100 FPS with a low-settings guide on a 200-pop server (May 2026) [[1]](https://steamcommunity.com/sharedfiles/filedetails/?id=3727010750)

## Benchmark status

No measured reports yet.
