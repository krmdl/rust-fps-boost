# Profile design

All four profiles touch the **same set of convars**, so you can compare them line by line:

```bash
git diff --no-index profiles/low.cfg profiles/balanced.cfg
```

Per-convar reasoning lives in [convars.md](convars.md). This page explains the overall intent of each profile.

## ultra-low

**For:** integrated graphics (Intel UHD/Iris Xe, Vega iGPU), old laptops, 4-core CPUs, 8 GB RAM, cards with ≤2 GB VRAM.

**Goal:** get Rust playable. Every setting with a measurable cost is at its minimum, except where turning it off would hurt gameplay:

- **Shadows stay at the lowest visible level** instead of off, because enemy shadows and depth cues matter.
- **Textures at quarter resolution** (`globaltexturemipmaplimit 2`). iGPUs share system RAM, so VRAM pressure and memory bandwidth are the real bottleneck.
- **Anisotropic filtering at 2×**: the only profile that lowers it, because on shared memory it isn't free.
- **No anti-aliasing.** Grass at its minimum density leaves less foliage to shimmer.

The game will look rough: buildings pop in at mid range and trees are mostly billboards. That's the trade.

**Pair with:** the [`intel-igpu`](../gpu/intel-igpu.cfg) overlay if you're on Intel graphics. It also lowers render scale.

## low

**For:** entry-level discrete GPUs (GTX 1050 Ti / 1650, RX 570 / 580 / 5500), 4–6 core CPUs, 16 GB RAM.

**Goal:** high and **stable** FPS (good 1% lows) while the world still looks like Rust.

Compared to ultra-low:

- Half-res textures instead of quarter (4 GB VRAM is enough)
- AF 8×, cheap post-AA
- Mid-range LOD for trees/meshes so forests don't look like cardboard
- Some particles, so you can still read explosions and smoke

Grass and decor stay at their minimum; AO, water reflections and all cosmetic post-processing stay **off**. Water and AO were among the larger measured costs [[C2]](sources.md#c2), and less ground clutter also makes players easier to spot.

## balanced

**For:** GTX 1660 / RTX 2060–3060 / RX 6600-class GPUs with 6 GB+ VRAM and modern 6–8 core CPUs.

**Goal:** a good-looking game without the settings that cost a lot and give little:

- Full-res textures, AO, AA, some grass at reduced distance
- Point-light shadows limited to 1
- Still off: contact shadows, impostor shadows, bloom, sun shafts, planar reflections

## quality

**For:** RTX 3070+ / RX 6800+ class.

**Goal:** best visuals. Almost everything at maximum, except effects that **only hurt**: motion blur, depth of field, lens dirt, vignette and the hurt overlay. We still skip planar reflections because their cost is wildly out of proportion to the visual gain.

## Choosing between two profiles

1. Start with the profile that matches your GPU.
2. Turn on the FPS overlay (`perf 1` in the F1 console) and play normally for a few minutes, including a populated area.
3. If you're GPU-bound (GPU usage ~95–100%), the GPU-heavy settings in [convars.md](convars.md) are where to cut. If you're CPU-bound (GPU usage well below 90%), move down a profile or lower the `CPU` rows (draw distance, trees, mesh, shadows).
