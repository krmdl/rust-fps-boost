# NVIDIA GeForce RTX 5060 Ti

In the top of the Steam Hardware Survey (September 2026) [[H1]](../../docs/sources.md#h1).

## Specs

| | |
|---|---|
| Architecture | Blackwell (GB206) |
| VRAM | 8 GB |
| Memory bus | 128-bit |
| Bandwidth | ~448 GB/s |
| NVIDIA Reflex | Yes |
| DLSS | Yes |

Source: TechPowerUp GPU database [[H2]](../../docs/sources.md#h2).

## Recommended setup

| Resolution | Profile | Command |
|---|---|---|
| 1080p | `quality` | `tools\apply.ps1 -Profile quality -Gpu rtx-5060-ti` |
| 1440p | `balanced` | `tools\apply.ps1 -Profile balanced -Gpu rtx-5060-ti` |

Profile choice is an **estimate** from this card's performance tier (rule R5). It hasn't been benchmarked yet. If you're on this card, a [benchmark report](../../benchmarks/README.md) is the most useful thing you can contribute.

**DLSS:** set it in **Options → Graphics** (not in the overlay, because the convar's value mapping is unverified). DLSS helps when you're GPU-bound. At 1080p use *Quality* at most; at 1440p *Quality* or *Balanced*.

## What this overlay sets, and why

| Convar | Value | Why | Src |
|---|---|---|---|
| `graphics.reflexmode` | 1 | R2: NVIDIA Reflex lowers input latency (GTX 900 series and newer). | [N1](../../docs/sources.md#n1) |
| `graphicssettings.globaltexturemipmaplimit` | 0 | R1: 8 GB VRAM → full resolution textures. Overrides the profile value. | [U1](../../docs/sources.md#u1) |
| `graphics.af` | 16 | R4: anisotropic filtering is cheap on a discrete card's memory bandwidth. | reasoning |

Rules R1–R5 are explained in [the card overlay README](README.md#what-a-card-overlay-changes-and-the-rules-behind-it).

## Card-specific notes

- Sold with 8 GB and 16 GB. Same overlay for both: full-res textures either way (R1).

## Benchmark status

No reports yet.
