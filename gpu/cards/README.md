# Rust config per graphics card

One overlay per popular graphics card. Find your card, then apply it on top of the profile recommended on its page:

```powershell
powershell -ExecutionPolicy Bypass -File tools\apply.ps1 -Preset low -Gpu gtx-1650
```

A card overlay **replaces** the vendor overlay (`nvidia` / `amd`). It already contains the vendor settings.

## Which cards, and why these

- **Most common on Steam:** RTX 5070, RTX 5060, RTX 5060 Ti, RTX 4060, RTX 3060, RTX 3050 and GTX 1650 are among the top 10 cards in the September 2026 Steam Hardware Survey. The RX 9070 XT is the most common AMD discrete card [[H1]](../../docs/sources.md#h1). Each card page shows its share.
- **Low-end focus:** GTX 1050 Ti, GTX 1060, GTX 1660 Super, RTX 2060, RX 580 and RX 6600 are included because this project targets low-end and older PCs, where card-specific tuning matters most (see [Where card tuning helps](#where-card-tuning-helps)).

Specs on every card page come from the TechPowerUp GPU database [[H2]](../../docs/sources.md#h2).

## What a card overlay changes, and the rules behind it

A card overlay **only** contains settings that depend on the card itself. Everything else comes from the profile. Every card page applies the same rules below, so cards can be compared fairly.

| Rule | Convar | Logic | Src |
|---|---|---|---|
| **R1: Textures by VRAM** | `graphicssettings.globaltexturemipmaplimit` | ≤2 GB → `2` (quarter), 3–4 GB → `1` (half), 6 GB+ → `0` (full). The card knows its VRAM better than a generic profile, so this **overrides** the profile value. On a 12 GB card running `low`, you get full-res textures, because texture size costs VRAM, not much FPS, as long as it fits. | [U1](../../docs/sources.md#u1), reasoning (FPS cost) |
| **R2: Latency by vendor** | `graphics.reflexmode` | NVIDIA (GTX 900 series and newer): `1`. AMD: `0` (unsupported; use Radeon Anti-Lag in the driver). | [N1](../../docs/sources.md#n1), [N3](../../docs/sources.md#n3) |
| **R3: DLSS off where impossible** | `graphics.dlss`, `graphics.dlaa` | Cards without tensor cores (all GTX, all AMD): `dlss -1` (the "off" value in the reference dump) and `dlaa False`. RTX cards: **not set**. The convar's value mapping isn't verified, so pick DLSS in the menu (guidance on each card page). | [N2](../../docs/sources.md#n2), [reference dump](../../reference/client.dump.cfg) |
| **R4: Anisotropic filtering** | `graphics.af` | `16` on every discrete card. AF costs memory bandwidth, which discrete cards have plenty of. The profiles' lower AF values exist for integrated GPUs. | reasoning |
| **R5: Recommended profile** | – (documentation only) | Each page recommends a profile for 1080p and 1440p, estimated from the card's relative performance tier. **These are estimates until benchmarked.** | reasoning |

## Where card tuning helps

- **Low-end cards (GTX 1050 Ti → GTX 1660 Super, RX 580):** Rust is often **GPU- or VRAM-bound** here, so the right texture level (R1) and profile choice make a real difference. Overflowing VRAM causes stutter, not just lower FPS.
- **Mid/high cards (RTX 4060 and up, RX 9070 XT):** Rust is frequently **CPU-bound** on these cards [[F1]](../../docs/sources.md#f1), so card settings change FPS less. The benefit is mostly latency (Reflex) and spending spare GPU power on visuals at no FPS cost.

## All cards

| Card | VRAM | Overlay | 1080p profile | 1440p profile |
|---|---|---|---|---|
<!-- cards:start -->
| [NVIDIA GeForce GTX 1050 Ti](gtx-1050-ti.md) | 4 GB | `gtx-1050-ti` | `low` | `ultra-low` |
| [NVIDIA GeForce GTX 1060 3GB](gtx-1060-3gb.md) | 3 GB | `gtx-1060-3gb` | `low` | `ultra-low` |
| [NVIDIA GeForce GTX 1060 6GB](gtx-1060-6gb.md) | 6 GB | `gtx-1060-6gb` | `low` | `ultra-low` |
| [NVIDIA GeForce GTX 1650](gtx-1650.md) | 4 GB | `gtx-1650` | `low` | `ultra-low` |
| [NVIDIA GeForce GTX 1660 Super](gtx-1660-super.md) | 6 GB | `gtx-1660-super` | `low` | `low` |
| [NVIDIA GeForce RTX 2060](rtx-2060.md) | 6 GB | `rtx-2060` | `balanced` | `low` |
| [NVIDIA GeForce RTX 3050](rtx-3050.md) | 8 GB | `rtx-3050` | `low` | `low` |
| [NVIDIA GeForce RTX 3060](rtx-3060.md) | 12 GB | `rtx-3060` | `balanced` | `balanced` |
| [NVIDIA GeForce RTX 4060](rtx-4060.md) | 8 GB | `rtx-4060` | `balanced` | `balanced` |
| [NVIDIA GeForce RTX 5060](rtx-5060.md) | 8 GB | `rtx-5060` | `balanced` | `balanced` |
| [NVIDIA GeForce RTX 5060 Ti](rtx-5060-ti.md) | 8 GB | `rtx-5060-ti` | `quality` | `balanced` |
| [NVIDIA GeForce RTX 5070](rtx-5070.md) | 12 GB | `rtx-5070` | `quality` | `quality` |
| [AMD Radeon RX 580 4GB](rx-580-4gb.md) | 4 GB | `rx-580-4gb` | `low` | `ultra-low` |
| [AMD Radeon RX 580 8GB](rx-580-8gb.md) | 8 GB | `rx-580-8gb` | `low` | `ultra-low` |
| [AMD Radeon RX 6600](rx-6600.md) | 8 GB | `rx-6600` | `balanced` | `low` |
| [AMD Radeon RX 9070 XT](rx-9070-xt.md) | 16 GB | `rx-9070-xt` | `quality` | `quality` |
<!-- cards:end -->

Laptop versions of these cards have different power limits and often less VRAM. Check your VRAM (Task Manager → Performance → GPU → "Dedicated GPU memory") and apply rule R1 yourself if it differs.

Your card isn't listed? Use the vendor overlay (`nvidia` / `amd`) and the closest card's page as a guide, or open an issue with your card. A benchmark report gets a card added fastest.
