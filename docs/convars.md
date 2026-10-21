# Convar rationale

This page lists every convar a profile touches, the value for each profile, **why** we chose it, and **what backs the claim**.

**Column legend**

- **UL / L / B / Q**: ultra-low / low / balanced / quality
- **Cost**: the resource the setting mostly loads. Rust is often **CPU-bound** (draw calls, entity count, Unity main thread), so CPU savings are worth the most on low-end machines. Facepunch notes that most of its own optimisation work targeted CPU cost [[F1]](sources.md#f1).
  - `CPU`: draw calls, culling, animation, physics
  - `GPU`: shading, fill rate, post-processing
  - `VRAM`: texture and buffer memory
  - `RAM`: system memory / GC pressure
- **Vis.**: how the setting changes your ability to spot players. `+` helps, `−` hurts, `·` neutral.
- **Src**: evidence for the *cost* claim. See [sources.md](sources.md) for what each tag means. `U` sources describe the Unity mechanism. That the Rust convar uses it is inferred from the name unless an `F` source says so. `reasoning` = no source found yet.
- **⚠**: the exact value range is not confirmed for the current build. See [Verification backlog](#verification-backlog).

Impact numbers are **expected**, not measured, until a benchmark lands in [`benchmarks/`](../benchmarks/).

---

## Distance & LOD

| Convar | UL | L | B | Q | Cost | Vis. | Why | Src |
|---|---|---|---|---|---|---|---|---|
| `graphics.drawdistance` | 1500 | 1500 | 2000 | 2500 | CPU | · | How far the world renders. More distance means more objects culled and submitted each frame. 1500 is the in-game slider minimum. Players beyond ~1500 m are not engageable anyway. | reasoning |
| `graphics.lodbias` | 0.25 | 0.5 | 1 | 2 | CPU+GPU | · / − | Multiplies the distance at which objects switch to lower-detail meshes. Lower means simpler meshes sooner and fewer triangles. At 0.25, buildings and rocks visibly "pop" at mid range, an accepted trade for potato PCs. | [U3](sources.md#u3) |
| `graphics.hlod` | True | True | True | True | CPU | · | Hierarchical LOD merges distant objects into combined meshes, which means **fewer draw calls**. Facepunch added an HLOD system for monuments. A pure win on CPU-bound systems, so it stays on everywhere. | [F2](sources.md#f2), [F3](sources.md#f3), [G1](sources.md#g1) |
| `mesh.quality` | 0 | 50 | 100 | 200 | CPU+GPU | · | LOD quality for general meshes (deployables, props). Big triangle-count lever. Facepunch's own optimisation work included making small objects "LOD and cull quicker". | [F1](sources.md#f1), reasoning |
| `tree.quality` | 0 | 50 | 100 | 200 | CPU+GPU | + | Tree LOD distance/quality. Trees are the densest geometry in Rust, so in forests this is one of the largest FPS swings. Simpler tree silhouettes also make players easier to see. | [F1](sources.md#f1) (tree draw calls), reasoning |
| `tree.meshes` | 0 | 25 | 50 | 100 | CPU+GPU | + | Share of trees drawn as full meshes rather than billboards (shown in the menu as "Max Tree Meshes"). Billboards cost almost nothing. | [F1](sources.md#f1), reasoning |
| `terrain.quality` | 0 | 25 | 50 | 100 | GPU | · | Terrain mesh/shading detail. Mostly a GPU fill-rate cost, and very noticeable on iGPUs. | reasoning |
| `graphicssettings.enablelodcrossfade` | False | False | True | True | GPU+CPU | · | During a crossfade, Unity renders **both** LOD levels and blends them, so that object briefly costs double. Off means instant pop-in but a cheaper frame. | [U4](sources.md#u4) |

## Shadows

Shadows are expensive on **both** sides: shadow casters are drawn again into each shadow map/cascade (CPU draw calls [[U6]](sources.md#u6)), and the number of shadow casters has "a significant impact" on shadow cost [[U7]](sources.md#u7).

| Convar | UL | L | B | Q | Cost | Vis. | Why | Src |
|---|---|---|---|---|---|---|---|---|
| `graphics.shadowmode` ⚠ | 1 | 1 | 2 | 4 | CPU+GPU | − if 0 | Main shadow quality. We use the **lowest non-off** level instead of disabling shadows: players' shadows give away their position, and shadows give depth cues when building and aiming. The current build's default is 4. | [U6](sources.md#u6), [U7](sources.md#u7) |
| `graphicssettings.shadowqualitypreset` ⚠ | 0 | 1 | 2 | 3 | CPU+GPU | · | Unity shadow quality preset (resolution/cascade behaviour). Lowered together with `shadowmode`. | [U6](sources.md#u6) |
| `graphics.shadowlights` | 0 | 0 | 1 | 3 | CPU+GPU | · | Shadows cast by point lights (lanterns, ceiling lights, furnaces). Unity renders a point-light shadow in **six directions**, roughly six spot-light shadows' worth of draw calls. A huge cost in bases with many lights, for little gameplay value. | [U5](sources.md#u5) |
| `graphics.aggressiveshadowlod` | True | True | True | False | CPU | · | Uses lower LODs for shadow casters, so fewer triangles go to the shadow pass. Nearly invisible, since shadows need far less detail than the visible mesh. | [U7](sources.md#u7), reasoning |
| `graphics.aggressiveshadowlodwearable` | True | True | True | False | CPU | · | Same, for clothing/wearables on players. Helps in populated areas (Outpost, big fights). | reasoning |
| `graphics.impostorshadows` | False | False | False | True | GPU | · | Shadows for distant tree impostors. Atmosphere only, no gameplay value. | [U7](sources.md#u7) |
| `graphics.contactshadows` | False | False | False | True | GPU | · | Screen-space contact shadows: small detail shadows at contact points. Purely cosmetic post-process. | reasoning |

## Post-processing & effects

Post-processing is full-screen shading, so its cost scales with resolution. It's especially expensive on iGPUs and when you're GPU-bound. *No per-effect cost sources yet. All rows below are reasoning until benchmarked. The visibility arguments are design judgement.*

| Convar | UL | L | B | Q | Cost | Vis. | Why | Src |
|---|---|---|---|---|---|---|---|---|
| `effects.antialiasing` ⚠ | 0 | 1 | 2 | 2 | GPU | · | Off on ultra-low. Level 1 is the cheap post-AA option. AA mainly fixes shimmering on foliage, and with grass gone (low profiles) there's much less of it. | reasoning |
| `effects.ao` | False | False | True | True | GPU | · | Ambient occlusion, a full-screen effect and one of the more expensive post effects. | reasoning |
| `effects.bloom` | False | False | False | True | GPU | − | Glow around bright areas. It hurts visibility (players silhouetted against the sky/sun get washed out), so we only enable it on quality. | reasoning |
| `effects.shafts` | False | False | False | True | GPU | − | Sun shafts (god rays). Can wash out the view when looking toward the sun. | reasoning |
| `effects.lensdirt` | False | False | False | False | GPU | − | Dirt overlay on bright light. Never helps, so it's off everywhere. | reasoning |
| `effects.motionblur` | False | False | False | False | GPU | − | Blurs exactly what you are trying to track. Off everywhere. | reasoning |
| `effects.vignet` | False | False | False | False | GPU | − | Darkens screen edges, reducing peripheral visibility. Off everywhere. | reasoning |
| `effects.sharpen` | False | False | False | False | GPU | · | Optional. Off by default because an extra pass hurts the low profiles. If you use DLSS or a low render scale you may want it (see GPU overlays). | reasoning |
| `effects.hurtoverlay` | False | False | False | False | GPU | + | Red damage overlay that blocks your view while you are being shot. | reasoning |
| `effects.otherplayerslightflares` | False | False | False | False | GPU | + | Lens flares from other players' flashlights/lasers. Turning them off removes blinding glare. Note it's a mild **visibility advantage**: listed under principle 3. | reasoning |
| `graphics.dof` | False | False | False | False | GPU | − | Depth of field blurs the background. Off everywhere. | reasoning |
| `graphics.volumetric_clouds` ⚠ | 0 | 0 | 2 | 4 | GPU | · | Volumetric cloud rendering (replaced the old `graphics.vclouds`). Volumetrics are raymarched per pixel and are pure sky decoration. | [F3](sources.md#f3) (convar), reasoning (cost) |
| `graphics.parallax` | 0 | 0 | 1 | 2 | GPU | · | Parallax occlusion mapping on surfaces: extra texture samples per pixel. | reasoning |
| `sss.enabled` | False | False | False | True | GPU | · | Subsurface scattering (skin). Cosmetic. | reasoning |
| `reflection.planarreflections` | False | False | False | False | CPU+GPU | · | Planar reflections render the scene a second time. Even the quality profile skips them: the visual gain is tiny for the cost. Off by default in the game too. | [reference dump](../reference/client.default.cfg) (default), reasoning |

## Particles, gibs, foliage

| Convar | UL | L | B | Q | Cost | Vis. | Why | Src |
|---|---|---|---|---|---|---|---|---|
| `particle.quality` | 0 | 25 | 75 | 100 | GPU+CPU | · | Particle counts/quality (fire, explosions, smoke). The biggest frame drops happen during raids and fights, exactly when FPS matters most. | reasoning |
| `graphicssettings.softparticles` | False | False | True | True | GPU | · | Soft particles blend particle edges against scene depth, an extra depth read per particle pixel. | [U2](sources.md#u2) |
| `graphicssettings.particleraycastbudget` | 128 | 256 | 1024 | 1024 | CPU | · | Max raycasts per frame for particle collision testing. Lower values free main-thread time. Particles may pass through geometry more often. | [U2](sources.md#u2) |
| `effects.maxgibs` | 0 | 0 | 1 | 1 | CPU | + | Building debris (gibs) when walls are destroyed. Gibs are physics objects, which causes **CPU spikes during raids**. 0 also clears debris you could otherwise lose players in. | reasoning |
| `effects.creationeffects` | False | False | False | True | GPU | · | Effects when building/placing. Cosmetic. | reasoning |
| `grass.quality` | 0 | 0 | 50 | 100 | GPU+CPU | + | Grass is widely considered one of Rust's largest single FPS costs, and it hides prone/crouching players. On both low profiles we remove it entirely. This is the main **visibility advantage** in these configs, and the game allows it for everyone. | reasoning: **top benchmark priority** |
| `grass.distance` ⚠ | 0 | 0 | 80 | 100 | GPU+CPU | + | How far grass draws. Irrelevant when `grass.quality` is 0, but set low so that raising quality later doesn't bring back far grass. The game may clamp 0 up to its minimum. | reasoning |
| `grass.displacement` | False | False | True | True | CPU+GPU | · | Grass bending around players/entities. | reasoning |
| `decor.quality` | 0 | 0 | 50 | 100 | GPU+CPU | + | Small ground decorations (pebbles, small plants). Less clutter makes the ground easier to read. | reasoning |

## Water

| Convar | UL | L | B | Q | Cost | Vis. | Why | Src |
|---|---|---|---|---|---|---|---|---|
| `water.quality` | 0 | 0 | 1 | 2 | GPU | · | Water shading/tessellation. Matters a lot on coastal maps. | reasoning |
| `water.reflections` | 0 | 0 | 1 | 2 | GPU+CPU | · | Reflections can mean rendering parts of the scene again. Off on low. | reasoning |

## Textures & memory

| Convar | UL | L | B | Q | Cost | Vis. | Why | Src |
|---|---|---|---|---|---|---|---|---|
| `graphicssettings.globaltexturemipmaplimit` | 2 | 1 | 0 | 0 | VRAM | · | Unity documents it exactly: 0 = full, 1 = half, 2 = quarter-size textures (2D textures only). Running out of VRAM causes **stutter**, not just lower FPS. ≤2 GB cards: 2, 4 GB cards: 1, 6 GB+: 0. Note: the game's own dump ships with **1**, so stock Rust already uses half-res textures on some systems. | [U1](sources.md#u1), [reference dump](../reference/client.default.cfg) |
| `graphics.af` | 2 | 8 | 16 | 16 | GPU (bandwidth) | · | Anisotropic filtering keeps ground textures sharp at angles. Almost free on discrete GPUs, but it costs memory bandwidth on iGPUs (shared RAM), so ultra-low goes down to 2. | reasoning |

## Latency

| Convar | UL | L | B | Q | Cost | Vis. | Why | Src |
|---|---|---|---|---|---|---|---|---|
| `graphics.maxqueuedframes` | 1 | 1 | 1 | 1 | – | · | Unity: "Maximum number of frames queued up by graphics driver." Fewer queued frames means lower input latency (the same idea NVIDIA Reflex automates). On very weak CPUs, 2 can smooth frame times slightly at the cost of latency, so try it if your frame time graph is spiky. | [U2](sources.md#u2), [N1](sources.md#n1) |

`graphics.reflexmode` (NVIDIA Reflex) and `graphics.dlss` are vendor-specific and live in the [GPU overlays](../gpu/), not in the base profiles.

## Your own player / UI

| Convar | UL | L | B | Q | Cost | Vis. | Why | Src |
|---|---|---|---|---|---|---|---|---|
| `legs.enablelegs` | False | False | True | True | CPU+GPU | · | Renders your own legs in first person. A small cost with no gameplay value. | reasoning |
| `player.footik` | False | False | True | True | CPU | · | Foot IK for other players (feet adapting to terrain). The cost scales with player count, so it matters at Outpost/Bandit and in large fights. | reasoning |
| `ui.showinventoryplayer` | False | False | True | True | GPU+CPU | · | The 3D player model in the inventory screen needs an extra render while the inventory is open. Turning it off makes looting smoother on weak PCs. | reasoning |

---

## What we never touch

These are personal preferences or have no performance effect. The installer leaves them alone:

- `input.*`: sensitivity, ADS sensitivity, toggles
- `graphics.fov`, `graphics.uiscale`, `graphics.vm_fov_scale`
- `audio.*`, `crosshair.*`, binds (`keys.cfg`)
- `fps.limit`, `graphics.vsync`, `graphics.screenmode`, `graphics.resolution`. See [launch-options.md](launch-options.md) for advice.
- `gc.buffer`: depends on your RAM, not your profile. See below.

### `gc.buffer` (RAM)

**Evidence: weak.** Here's what we know for sure:

- A Unity garbage-collection run that isn't spread across frames stops the main thread and shows up as a frame-time spike [[U8]](sources.md#u8).
- Facepunch has fixed allocations in Rust that caused GC stutter [[F1]](sources.md#f1), so GC stutter in Rust is real.

What we **don't** have is an official description of `gc.buffer`. Community guides say a larger buffer makes GC run less often, giving fewer periodic hitches at the cost of more RAM [[C1]](sources.md#c1), but they disagree on the default and the units. The reference dump contains an unusual value (`1965`), which *suggests* (our inference) that the game already sizes it automatically from system memory. That's why we don't override it by default.

If you get regular hitches every few seconds, the installer can set it manually. These values are community conventions, not measured:

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
| `grass.distance` | Minimum value the game clamps to |

Unity documents that a `globaltexturemipmaplimit` value stripped at build time is moved to the nearest available mip [[U1]](sources.md#u1), so `2` is safe even if Rust ships fewer mips.

### Rows with no source (benchmark priorities)

Every row marked `reasoning` is a hypothesis. In order of expected impact, these are the ones to measure first:

1. `grass.quality` / `grass.distance`
2. `tree.quality` / `tree.meshes`
3. `graphics.drawdistance`
4. `effects.ao`, `effects.antialiasing`
5. `particle.quality`, `effects.maxgibs` (raid scenario)
6. `water.quality` / `water.reflections` (coast scene)

The reference dump also contains a few hand-appended lines (`graphics.shaderlod`, `graphics.grassshadows`, `graphics.shadowfilteringquality`, `graphicssettings.shadowcascades`, `graphicssettings.shadowresolution`) after a blank line. They are **not** written by the game itself, so they are excluded from all profiles until someone confirms they exist.
