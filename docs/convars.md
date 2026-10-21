# Convar rationale

This page lists every convar a profile touches, the value for each profile, and **why**.

**Column legend**

- **UL / L / B / Q**: ultra-low / low / balanced / quality
- **Cost**: the resource the setting mostly loads. Rust is usually **CPU-bound** (draw calls, entity count, Unity main thread), so CPU savings are worth the most on low-end machines.
  - `CPU`: draw calls, culling, animation, physics
  - `GPU`: shading, fill rate, post-processing
  - `VRAM`: texture and buffer memory
  - `RAM`: system memory / GC pressure
- **Visibility**: how the setting changes your ability to spot players. `+` helps, `−` hurts, `·` neutral.
- **⚠**: the exact value range is not confirmed for the current build. Check it in the F1 console (`find <name>` prints the current value and the help text). See [Verification backlog](#verification-backlog).

Impact numbers are **expected**, not measured, until a benchmark lands in [`benchmarks/`](../benchmarks/).

---

## Distance & LOD

| Convar | UL | L | B | Q | Cost | Visibility | Why |
|---|---|---|---|---|---|---|---|
| `graphics.drawdistance` | 1500 | 1500 | 2000 | 2500 | CPU | · | How far the world renders. More distance means more objects culled and submitted each frame. 1500 is the in-game slider minimum. Players beyond ~1500 m are not engageable anyway. |
| `graphics.lodbias` | 0.25 | 0.5 | 1 | 2 | CPU+GPU | · / − | Multiplies the distance at which objects switch to lower-detail meshes. Lower means simpler meshes sooner and fewer triangles. At 0.25, buildings and rocks visibly "pop" at mid range, an accepted trade for potato PCs. Players are not affected much because player models use their own culling (`playercull.*`). |
| `graphics.hlod` | True | True | True | True | CPU | · | Hierarchical LOD merges far-away objects into combined meshes, which means **fewer draw calls**. It's a pure win on CPU-bound systems, so it stays on everywhere. |
| `mesh.quality` | 0 | 50 | 100 | 200 | CPU+GPU | · | LOD quality for general meshes (deployables, props). Big triangle-count lever. 0 is aggressive but it's the single most effective mesh setting for weak GPUs. |
| `tree.quality` | 0 | 50 | 100 | 200 | CPU+GPU | + | Tree LOD distance/quality. Trees are the densest geometry in Rust, so in forests this is one of the largest FPS swings. Lower values also simplify tree silhouettes, which makes players easier to see. |
| `tree.meshes` | 0 | 25 | 50 | 100 | CPU+GPU | + | Share of trees drawn as full meshes rather than billboards. Billboards cost almost nothing. |
| `terrain.quality` | 0 | 25 | 50 | 100 | GPU | · | Terrain mesh/shading detail. Mostly a GPU fill-rate cost, and very noticeable on iGPUs. |
| `graphicssettings.enablelodcrossfade` | False | False | True | True | GPU+CPU | · | Crossfading draws **both** LODs during a transition (dithered), which briefly doubles the cost of that object. Off means instant pop-in, but a cheaper frame. |

## Shadows

Shadows are expensive on **both** sides: every shadow caster is drawn again for each cascade (CPU draw calls) and shadow maps cost fill rate (GPU).

| Convar | UL | L | B | Q | Cost | Visibility | Why |
|---|---|---|---|---|---|---|---|
| `graphics.shadowmode` ⚠ | 1 | 1 | 2 | 4 | CPU+GPU | − if 0 | Main shadow quality. We use the **lowest non-off** level instead of disabling shadows: players' shadows give away their position, and shadows give depth cues when building and aiming. The current build's default is 4. |
| `graphicssettings.shadowqualitypreset` ⚠ | 0 | 1 | 2 | 3 | CPU+GPU | · | Unity shadow quality preset (resolution/cascade behaviour). Lowered together with `shadowmode`. |
| `graphics.shadowlights` | 0 | 0 | 1 | 3 | CPU+GPU | · | Shadows cast by point lights (lanterns, ceiling lights, furnaces). Each shadowed light renders the scene again, up to 6× for a point light. This is a huge cost in bases with many lights, for little gameplay value. |
| `graphics.aggressiveshadowlod` | True | True | True | False | CPU | · | Uses lower LODs for shadow casters, so fewer triangles go to the shadow pass. Visually it's nearly invisible. |
| `graphics.aggressiveshadowlodwearable` | True | True | True | False | CPU | · | Same, for clothing/wearables on players. Helps in populated areas (Outpost, big fights). |
| `graphics.impostorshadows` | False | False | False | True | GPU | · | Shadows for distant tree impostors. Distant tree shadows add atmosphere but no gameplay value. |
| `graphics.contactshadows` | False | False | False | True | GPU | · | Screen-space contact shadows: small detail shadows at contact points. Purely cosmetic post-process. |

## Post-processing & effects

Post-processing is full-screen shading, so its cost scales with resolution. It's especially expensive on iGPUs and when you're GPU-bound.

| Convar | UL | L | B | Q | Cost | Visibility | Why |
|---|---|---|---|---|---|---|---|
| `effects.antialiasing` ⚠ | 0 | 1 | 2 | 2 | GPU | · | Off on ultra-low. Level 1 is the cheap post-AA option. AA mainly fixes shimmering on foliage, and with grass gone (low profiles) there's much less of it. |
| `effects.ao` | False | False | True | True | GPU | · | Ambient occlusion, a full-screen effect and one of the more expensive post effects. |
| `effects.bloom` | False | False | False | True | GPU | − | Glow around bright areas. It hurts visibility (players silhouetted against the sky/sun get washed out), so we only enable it on quality. |
| `effects.shafts` | False | False | False | True | GPU | − | Sun shafts (god rays). Can wash out the view when looking toward the sun. |
| `effects.lensdirt` | False | False | False | False | GPU | − | Dirt overlay on bright light. Never helps, so it's off everywhere. |
| `effects.motionblur` | False | False | False | False | GPU | − | Blurs exactly what you are trying to track. Off everywhere. |
| `effects.vignet` | False | False | False | False | GPU | − | Darkens screen edges, reducing peripheral visibility. Off everywhere. |
| `effects.sharpen` | False | False | False | False | GPU | · | Optional. Off by default because an extra pass hurts the low profiles. If you use DLSS or a low render scale you may want it (see GPU overlays). |
| `effects.hurtoverlay` | False | False | False | False | GPU | + | Red damage overlay that blocks your view while you are being shot. |
| `effects.otherplayerslightflares` | False | False | False | False | GPU | + | Lens flares from other players' flashlights/lasers. Turning them off removes blinding glare. Note it's a mild **visibility advantage**: listed under principle 3. |
| `graphics.dof` | False | False | False | False | GPU | − | Depth of field blurs the background. Off everywhere. |
| `graphics.volumetric_clouds` ⚠ | 0 | 0 | 2 | 4 | GPU | · | Volumetric cloud rendering. Raymarched, so it's expensive per pixel and pure sky decoration. |
| `graphics.parallax` | 0 | 0 | 1 | 2 | GPU | · | Parallax occlusion mapping on surfaces: extra texture samples per pixel. |
| `sss.enabled` | False | False | False | True | GPU | · | Subsurface scattering (skin). Cosmetic. |
| `reflection.planarreflections` | False | False | False | False | CPU+GPU | · | Planar reflections render the scene a second time. Even the quality profile skips them: the visual gain is tiny for the cost. Off by default in the game too. |

## Particles, gibs, foliage

| Convar | UL | L | B | Q | Cost | Visibility | Why |
|---|---|---|---|---|---|---|---|
| `particle.quality` | 0 | 25 | 75 | 100 | GPU+CPU | · | Particle counts/quality (fire, explosions, smoke). The biggest frame drops happen during raids and fights, exactly when FPS matters most. |
| `graphicssettings.softparticles` | False | False | True | True | GPU | · | Soft particles sample depth to fade edges near geometry, adding fill-rate cost per particle pixel. |
| `graphicssettings.particleraycastbudget` | 128 | 256 | 1024 | 1024 | CPU | · | Max raycasts per frame for particle collisions (Unity). Lower values free main-thread time. Particles may pass through geometry more often. |
| `effects.maxgibs` | 0 | 0 | 1 | 1 | CPU | + | Building debris (gibs) when walls are destroyed. Gibs are physics objects, which causes **CPU spikes during raids**. 0 also clears debris you could otherwise lose players in. |
| `effects.creationeffects` | False | False | False | True | GPU | · | Effects when building/placing. Cosmetic. |
| `grass.quality` | 0 | 0 | 50 | 100 | GPU+CPU | + | Grass is one of the largest single FPS costs in Rust and it hides prone/crouching players. On both low profiles we remove it entirely. This is the main **visibility advantage** in these configs, and the game allows it for everyone. |
| `grass.distance` ⚠ | 0 | 0 | 80 | 100 | GPU+CPU | + | How far grass draws. Irrelevant when `grass.quality` is 0, but set low so that raising quality later doesn't bring back far grass. The game may clamp 0 up to its minimum. |
| `grass.displacement` | False | False | True | True | CPU+GPU | · | Grass bending around players/entities. |
| `decor.quality` | 0 | 0 | 50 | 100 | GPU+CPU | + | Small ground decorations (pebbles, small plants). Less clutter makes the ground easier to read. |

## Water

| Convar | UL | L | B | Q | Cost | Visibility | Why |
|---|---|---|---|---|---|---|---|
| `water.quality` | 0 | 0 | 1 | 2 | GPU | · | Water shading/tessellation. Matters a lot on coastal maps. |
| `water.reflections` | 0 | 0 | 1 | 2 | GPU+CPU | · | Reflections can mean rendering parts of the scene again. Off on low. |

## Textures & memory

| Convar | UL | L | B | Q | Cost | Visibility | Why |
|---|---|---|---|---|---|---|---|
| `graphicssettings.globaltexturemipmaplimit` ⚠ | 2 | 1 | 0 | 0 | VRAM | · | Texture resolution: 0 = full, 1 = half, 2 = quarter. Running out of VRAM causes **stutter**, not just lower FPS: textures stream over PCIe. ≤2 GB cards: 2, 4 GB cards: 1, 6 GB+: 0. Note: the game's own dump ships with **1**, so stock Rust already uses half-res textures on some systems. |
| `graphics.af` | 2 | 8 | 16 | 16 | GPU (bandwidth) | · | Anisotropic filtering keeps ground textures sharp at angles. Almost free on discrete GPUs, but it costs memory bandwidth on iGPUs (shared RAM), so ultra-low goes down to 2. |

## Latency

| Convar | UL | L | B | Q | Cost | Visibility | Why |
|---|---|---|---|---|---|---|---|
| `graphics.maxqueuedframes` | 1 | 1 | 1 | 1 | – | · | How many frames the CPU may prepare ahead of the GPU. 1 means the lowest input latency. On very weak CPUs, 2 can smooth frame times slightly at the cost of latency, so try it if your frame time graph is spiky. |

`graphics.reflexmode` (NVIDIA Reflex) and `graphics.dlss` are vendor-specific and live in the [GPU overlays](../gpu/), not in the base profiles.

## Your own player / UI

| Convar | UL | L | B | Q | Cost | Visibility | Why |
|---|---|---|---|---|---|---|---|
| `legs.enablelegs` | False | False | True | True | CPU+GPU | · | Renders your own legs in first person. A small cost with no gameplay value. |
| `player.footik` | False | False | True | True | CPU | · | Foot IK for other players (feet adapting to terrain). The cost scales with player count, so it matters at Outpost/Bandit and in large fights. |
| `ui.showinventoryplayer` | False | False | True | True | GPU+CPU | · | The 3D player model in the inventory screen needs an extra camera render while the inventory is open. Turning it off makes looting smoother on weak PCs. |

---

## What we never touch

These are personal preferences or have no performance effect. The installer leaves them alone:

- `input.*`: sensitivity, ADS sensitivity, toggles
- `graphics.fov`, `graphics.uiscale`, `graphics.vm_fov_scale`
- `audio.*`, `crosshair.*`, binds (`keys.cfg`)
- `fps.limit`, `graphics.vsync`, `graphics.screenmode`, `graphics.resolution`. See [launch-options.md](launch-options.md) for advice.
- `gc.buffer`: depends on your RAM, not your profile. See below.

### `gc.buffer` (RAM)

Rust's managed memory is garbage-collected. A larger buffer means fewer GC runs and **fewer periodic stutters**, at the cost of more RAM. The reference dump contains an unusual value (`1965`), which suggests the game already sizes this automatically from your system memory. That's why we don't override it by default.

If you get regular hitches every few seconds, the installer can set it manually:

| System RAM | Suggested `gc.buffer` |
|---|---|
| 8 GB | 1024 |
| 16 GB | 2048 |
| 32 GB+ | 4096 |

```powershell
tools\apply.ps1 -Profile low -GcBuffer 2048
```

---

## Verification backlog

Values marked ⚠ above need a check in the current build. To verify, open the F1 console in-game and run `find <convar>` to read its help text. Then report the valid range in an issue or PR.

| Convar | Open question |
|---|---|
| `graphics.shadowmode` | Exact level meanings (game default is 4). Does 0 disable shadows entirely? Is 1 the lowest visible level? |
| `graphicssettings.shadowqualitypreset` | Is it overridden by `graphics.shadowmode` at runtime? |
| `effects.antialiasing` | Mapping of 0/1/2/3 to AA methods (off / FXAA / SMAA / TAA?) |
| `graphics.volumetric_clouds` | Valid range (dump shows 4) |
| `graphicssettings.globaltexturemipmaplimit` | Is 2 accepted, or is it clamped to 1? |
| `grass.distance` | Minimum value the game clamps to |

The reference dump also contains a few hand-appended lines (`graphics.shaderlod`, `graphics.grassshadows`, `graphics.shadowfilteringquality`, `graphicssettings.shadowcascades`, `graphicssettings.shadowresolution`) after a blank line. They are **not** written by the game itself, so they are excluded from all profiles until someone confirms they exist.
