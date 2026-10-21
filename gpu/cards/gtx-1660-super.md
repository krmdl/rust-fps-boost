# Best Rust settings for the NVIDIA GeForce GTX 1660 Super

**Config file:** [`gtx-1660-super.cfg`](gtx-1660-super.cfg)

## Specs

| | |
|---|---|
| Architecture | Turing (TU116) |
| VRAM | 6 GB |
| Memory bus | 192-bit |
| Bandwidth | ~336 GB/s |
| NVIDIA Reflex | Yes |
| DLSS | No |

Source: TechPowerUp GPU database [[H2]](../../docs/sources.md#h2).

## Recommended setup

Easiest: double-click **`install.bat`** in the repo folder and pick **Install**. It detects this card and suggests the profile below. Or run the command for your resolution from the repo folder:

| Resolution | Profile | Command |
|---|---|---|
| 1080p | [`low`](../../profiles/low.cfg) | `powershell -ExecutionPolicy Bypass -File tools\apply.ps1 -Preset low -Gpu gtx-1660-super` |
| 1440p | [`low`](../../profiles/low.cfg) | `powershell -ExecutionPolicy Bypass -File tools\apply.ps1 -Preset low -Gpu gtx-1660-super` |

Profile choice is an **estimate** from this card's performance tier (rule R5). It hasn't been benchmarked yet. If you're on this card, a [benchmark report](../../benchmarks/README.md) is the most useful thing you can contribute.

## What this overlay sets, and why

| Convar | Value | Why | Src |
|---|---|---|---|
| `graphics.reflexmode` | 1 | R2: NVIDIA Reflex lowers input latency (GTX 900 series and newer). | [N1](../../docs/sources.md#n1), [N3](../../docs/sources.md#n3) |
| `graphics.dlss` / `graphics.dlaa` | -1 / False | R3: this card has no tensor cores, so DLSS and DLAA are forced off. | [N2](../../docs/sources.md#n2) |
| `graphicssettings.globaltexturemipmaplimit` | 0 | R1: 6 GB VRAM → full resolution textures. Overrides the profile value. | [U1](../../docs/sources.md#u1) |
| `graphics.af` | 16 | R4: anisotropic filtering is cheap on a discrete card's memory bandwidth. | reasoning |

Rules R1–R5 are explained in [the card overlay README](README.md#what-a-card-overlay-changes-and-the-rules-behind-it).

## Card-specific notes

- Strong for its tier thanks to GDDR6 bandwidth. If `low` holds well above your target FPS, try `balanced` at 1080p.
- No tensor cores: no DLSS.

## Benchmark status

No reports yet.
