# GPU overlays

Overlays are small config files applied **on top of** a base profile. They hold settings that depend on the GPU vendor or class rather than overall performance tier:

```powershell
tools\apply.ps1 -Profile low -Gpu nvidia
```

The installer applies the profile first, then the overlay. If both set the same key, the overlay wins.

## Current overlays

### `nvidia.cfg`

| Convar | Value | Why |
|---|---|---|
| `graphics.reflexmode` | 1 | NVIDIA Reflex keeps the render queue near empty: **lower input latency**, especially when GPU-bound. NVIDIA claims "up to 38%" lower system latency in Rust (vendor best case). Supported on GTX 900 series or newer [[N1]](../docs/sources.md#n1). `2` (On + Boost) also keeps GPU clocks high. That costs power/heat, so on laptops stay on `1`. |

**DLSS** (`graphics.dlss`, RTX cards only; added to Rust in July 2021 [[N2]](../docs/sources.md#n2)) is not set by the overlay. The convar's value mapping isn't verified yet, and the right mode depends on your resolution. Choose it in **Options → Graphics**. Rough guide: at 1080p use *Quality* at most, at 1440p+ *Balanced* is usually fine. DLSS lowers the internal resolution, so it helps when **GPU-bound** and does almost nothing when CPU-bound, which is common in Rust.

### `amd.cfg`

| Convar | Value | Why |
|---|---|---|
| `graphics.reflexmode` | 0 | Reflex is NVIDIA-only. Setting it explicitly keeps leftovers from an old NVIDIA install from lingering. |
| `graphics.dlss` | -1 | DLSS is NVIDIA-only. -1 is the "off" value the game writes. |

For latency on AMD, use **Radeon Anti-Lag** in the Adrenalin driver panel (per-game profile).

### `intel-igpu.cfg`

Use with the `ultra-low` profile.

| Convar | Value | Why |
|---|---|---|
| `graphics.renderscale` ⚠ | 0.75 | Renders the 3D scene at 75% resolution (about 56% of the pixels) while the UI stays sharp. On iGPUs, fill rate is usually the bottleneck, so this is the single biggest lever. Try 0.5 if still too slow. *(reasoning: no source yet)* |
| `effects.sharpen` | True | A cheap sharpen pass to win back some clarity lost to the lower render scale. |
| `graphics.reflexmode` / `graphics.dlss` | 0 / -1 | Not supported on Intel. |

⚠ Confirm the valid range of `graphics.renderscale` in the F1 console (`find renderscale`).

## Card overlays

For popular cards there are dedicated overlays in [`cards/`](cards/), each with its own page explaining every value. **Prefer a card overlay** when your card is listed. The vendor overlays above are the fallback.

## Roadmap

- [ ] `intel-arc`: Arc A/B-series. DX11 driver performance has historically been weaker, so it needs testing
- [ ] `amd-apu`: Ryzen APUs (Vega / 680M / 780M). Shared memory, so dual-channel RAM is critical
- [ ] Laptop variants where VRAM differs from desktop (RTX 3050/3060/4060 Laptop)
- [ ] Benchmarks for every card in `cards/`, to replace the estimated profile recommendations

Each new overlay should come with at least one benchmark report from matching hardware. See [methodology](../docs/methodology.md).
