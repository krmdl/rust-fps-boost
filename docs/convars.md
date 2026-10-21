# Rust graphics settings explained: every convar, why, and its source

This page lists every convar a profile touches, the value for each profile, **why** we chose it, and **what backs the claim**.

**Column legend**

- **UL / L / B / Q**: ultra-low / low / balanced / quality
- **Cost**: the resource the setting mostly loads. Rust is often **CPU-bound** (draw calls, entity count, Unity main thread), so CPU savings are worth the most on low-end machines. Facepunch notes that most of its own optimisation work targeted CPU cost [[F1]](sources.md#f1).
  - `CPU`: draw calls, culling, animation, physics
  - `GPU`: shading, fill rate, post-processing
  - `VRAM`: texture and buffer memory
  - `RAM`: system memory / GC pressure
- **Vis.**: how the setting changes your ability to spot players. `+` helps, `−` hurts, `·` neutral.
- **Src**: evidence for the *cost* claim. See [sources.md](sources.md) for what each tag means.
  - `U` sources describe the Unity mechanism. That the Rust convar uses it is inferred from the name unless an `F` source says so.
  - `C2` figures were **measured on an RTX 4090 + i9-12900K** [[C2]](sources.md#c2). Treat them as the *direction* of an effect, not its size on a low-end PC. Low-end gains are often larger, but that's unmeasured.
  - `reasoning` = no source found yet.
- **⚠**: the exact value range is not confirmed for the current build. See [Verification backlog](#verification-backlog).

Impact numbers are **expected**, not measured on our target hardware, until a benchmark lands in [`benchmarks/`](../benchmarks/).

---

## Distance & LOD

| Convar | UL | L | B | Q | Cost | Vis. | Why | Src |
|---|---|---|---|---|---|---|---|---|
| `graphics.drawdistance` | 1500 | 1500 | 2000 | 2500 | CPU | − below 1500 | How far the world renders. The maximum (2500) cost up to 10% in C2's test, and 1500–2000 was only ~5% slower than 500. The slider goes lower than 1500 (500 was tested), but we stop at 1500: below that you stop seeing distant bases and players. Facepunch has fixed biome fog visibility depending on draw distance [[F7]](sources.md#f7), so lowering it no longer changes fog. | [C2](sources.md#c2), [F7](sources.md#f7) |
| `graphics.lodbias` ⚠ | 0.25 | 0.5 | 1 | 2 | CPU+GPU | · / − | Multiplies the distance at which objects switch to lower-detail meshes. Lower means simpler meshes sooner. C2 measured **up to 50% more FPS** from lower values near bandit camps and compounds, by far the largest single effect measured. At low values, buildings and rocks visibly "pop" at mid range. 0.25 is below the lowest value C2 tested (0.5), and the game may clamp it. | [C2](sources.md#c2), [U3](sources.md#u3) (Unity mechanism; Rust may use its own LOD system) |
| `graphics.hlod` | True | True | True | True | CPU | · | Hierarchical LOD merges distant objects into combined meshes, which means **fewer draw calls**. Facepunch added an HLOD rendering system for monuments and later fixed HLOD convar switching. A pure win on CPU-bound systems, so it stays on everywhere. | [F2](sources.md#f2), [F3](sources.md#f3), [G1](sources.md#g1) |
| `mesh.quality` | 0 | 50 | 100 | 200 | CPU+GPU | · | LOD quality for general meshes (deployables, props). Facepunch's own optimisation work included making small objects "LOD and cull quicker". | [F1](sources.md#f1), reasoning (cost) |
| `tree.quality` | 0 | 50 | 100 | 200 | CPU+GPU | + | Tree LOD distance/quality. The maximum cost up to 5% in C2's test. Trees are the densest geometry in Rust, so on CPU-bound low-end PCs the effect is expected to be larger. Simpler tree silhouettes also make players easier to see. | [C2](sources.md#c2), [F1](sources.md#f1) |
| `tree.meshes` | 10 | 25 | 50 | 100 | CPU+GPU | · | Share of trees drawn as full meshes rather than billboards ("Max Tree Meshes" in the menu). The slider's minimum is 10 [[C4]](sources.md#c4), which is also what the most-rated Steam guides use. C2 found a "nominal" impact on high-end hardware. Kept low on low-end profiles because billboards are cheaper to draw; unmeasured there. | [C2](sources.md#c2), [C4](sources.md#c4), reasoning |
| `terrain.quality` | 0 | 25 | 50 | 100 | GPU | · | Terrain mesh/shading detail. Mostly a GPU fill-rate cost, expected to matter most on iGPUs. | reasoning |
| `graphicssettings.enablelodcrossfade` | False | False | True | True | GPU+CPU | · | During a crossfade, Unity renders **both** LOD levels and blends them, so that object briefly costs double. Off means instant pop-in but a cheaper frame. | [U4](sources.md#u4) |

## Shadows

In Unity, shadow casters are drawn again into each shadow map/cascade (CPU draw calls [[U6]](sources.md#u6)), and the number of shadow casters has "a significant impact" on shadow cost [[U7]](sources.md#u7).

In March 2026 Facepunch merged the shadow settings into a single **Shadow Quality preset** in the Graphics menu [[F8]](sources.md#f8). How `graphics.shadowmode` and `graphicssettings.shadowqualitypreset` map to that preset is unverified (⚠ below).

| Convar | UL | L | B | Q | Cost | Vis. | Why | Src |
|---|---|---|---|---|---|---|---|---|
| `graphics.shadowmode` ⚠ | 1 | 1 | 2 | 4 | CPU+GPU | − if off | Main shadow setting. We use a low level rather than trying to disable shadows: players' shadows give away their position, and shadows give depth cues when building and aiming. The reference dump has 4. | [U6](sources.md#u6), [U7](sources.md#u7) |
| `graphicssettings.shadowqualitypreset` ⚠ | 0 | 1 | 2 | 3 | GPU | · | Matches the menu's "Shadow Quality" (0–3): **0 renders hard shadows** (shadows stay on, just with sharp edges), 1–3 are soft-shadow quality, and the top value was 5–6% slower than the rest in C2's test. 0 keeps shadows visible at the lowest cost. | [C2](sources.md#c2) |
| `graphics.shadowlights` | 1 | 1 | 1 | 3 | CPU+GPU | · | Shadows cast by point lights (lanterns, ceiling lights, furnaces). Unity renders a point-light shadow in **six directions**, roughly six spot-light shadows' worth of draw calls. C2 measured 2–4% at night; the cost can be larger in light-heavy bases. Little gameplay value, so low profiles use the minimum. Facepunch raised the minimum to **1** in March 2026 "to prevent light-leaking issues", so 0 is no longer possible. | [F8](sources.md#f8), [U5](sources.md#u5), [C2](sources.md#c2) |
| `graphics.aggressiveshadowlod` | True | True | True | False | CPU | · | Uses lower LODs for shadow casters, so fewer triangles go to the shadow pass. A real, maintained Rust convar (Facepunch fixed a shadow bug "with 'graphics.aggressiveShadowLod' enabled"). | [F6](sources.md#f6) (convar), [U7](sources.md#u7), reasoning (cost) |
| `graphics.aggressiveshadowlodwearable` | True | True | True | False | CPU | · | Same, for clothing/wearables on players. Expected to help in populated areas (Outpost, big fights). | reasoning |
| `graphics.impostorshadows` | False | False | False | True | GPU | · | Shadows for distant tree impostors. Atmosphere only, no gameplay value. | [U7](sources.md#u7) |
| `graphics.contactshadows` | False | False | False | True | GPU | · | Screen-space contact shadows: small detail shadows at contact points. Cost 2–3% in C2's test. Cosmetic. | [C2](sources.md#c2) |

## Post-processing & effects

Post-processing is full-screen shading, so its cost scales with resolution. It's especially expensive on iGPUs and when you're GPU-bound. The visibility arguments in this section are design judgement.

| Convar | UL | L | B | Q | Cost | Vis. | Why | Src |
|---|---|---|---|---|---|---|---|---|
| `effects.antialiasing` | 0 | 1 | 2 | 2 | GPU | · | 0 = Off, 1 = FXAA, 2 = SMAA, 3 = TSSAA according to a 2024 menu-to-convar mapping [[C4]](sources.md#c4). So: off on ultra-low, cheap FXAA on low, SMAA on balanced/quality. We skip TSSAA: players report it blurs in motion [[C6]](sources.md#c6), although Facepunch improved it in 2025 [[F7]](sources.md#f7). DLAA (RTX only) looks best but was over 10% slower than TSSAA [[C2]](sources.md#c2). | [C4](sources.md#c4), [F7](sources.md#f7), [C2](sources.md#c2), [C6](sources.md#c6) |
| `effects.ao` | False | False | True | True | GPU | · | Ambient occlusion, a full-screen effect. Cost up to 6% in C2's test. | [C2](sources.md#c2) |
| `effects.bloom` | False | False | False | True | GPU | − | Glow around bright areas. It hurts visibility (players silhouetted against the sky/sun get washed out), so we only enable it on quality. | reasoning |
| `effects.shafts` | False | False | False | True | GPU | − | Sun shafts (god rays). Cost 3–4% in C2's test, and can wash out the view when looking toward the sun. | [C2](sources.md#c2) |
| `effects.lensdirt` | False | False | False | False | GPU | − | Dirt overlay on bright light. Never helps, so it's off everywhere. | reasoning |
| `effects.motionblur` | False | False | False | False | GPU | − | Blurs exactly what you are trying to track. Off everywhere. | reasoning |
| `effects.vignet` | False | False | False | False | GPU | − | Darkens screen edges, reducing peripheral visibility. Off everywhere. | reasoning |
| `effects.sharpen` | False | False | True | True | GPU | + | A cheap sharpening pass. The most-rated 2025–26 Steam guides and several editorial guides keep it **on** for a clearer image [[C6]](sources.md#c6); one guide puts its cost at 2–3 FPS. On for balanced/quality, off on the low profiles where every pass counts (the `intel-igpu` overlay turns it on to offset its lower render scale). | [C6](sources.md#c6) |
| `effects.hurtoverlay` | False | False | False | False | GPU | + | Red damage overlay that blocks your view while you are being shot. | reasoning |
| `effects.otherplayerslightflares` | False | False | False | False | GPU | + | Lens flares from other players' flashlights/lasers. Turning them off removes blinding glare. Note it's a mild **visibility advantage**: listed under principle 3. | reasoning |
| `graphics.dof` | False | False | False | False | GPU | − | Depth of field blurs the background. Off everywhere. | reasoning |
| `graphics.volumetric_clouds` ⚠ | 0 | 0 | 2 | 4 | GPU | · | Volumetric clouds. Facepunch renamed the convar from `graphics.vclouds` and describes levels 1–4, "with 4 being the highest quality but most taxing on your GPU". Pure sky decoration. Whether 0 means off is unverified. | [F4](sources.md#f4), [F5](sources.md#f5) |
| `graphics.parallax` | 0 | 0 | 1 | 2 | GPU | · | Parallax occlusion mapping on surfaces: extra texture samples per pixel. | reasoning |
| `sss.enabled` | False | False | False | True | GPU | · | Subsurface scattering (skin). Cosmetic. | reasoning |
| `reflection.planarreflections` | False | False | False | False | CPU+GPU | · | Planar reflections render the scene a second time. Even the quality profile skips them: the visual gain is tiny for the cost. | reasoning |
| `graphics.renderscale` | 1 | 1 | 1 | 1 | GPU | · | Native render resolution in every profile. It's set here so that switching away from an overlay that lowers it (e.g. `intel-igpu`) restores full resolution. | – |

## Particles, gibs, foliage

| Convar | UL | L | B | Q | Cost | Vis. | Why | Src |
|---|---|---|---|---|---|---|---|---|
| `particle.quality` | 0 | 25 | 75 | 100 | GPU+CPU | · | Particle counts/quality (fire, explosions, smoke). Expected to matter most during raids and fights, exactly when FPS matters most. | reasoning |
| `graphicssettings.softparticles` | False | False | True | True | GPU | · | Soft particles blend particle edges against scene depth, an extra depth read per particle pixel. | [U2](sources.md#u2) |
| `graphicssettings.particleraycastbudget` | 128 | 256 | 1024 | 1024 | CPU | · | Max raycasts per frame for particle collision testing (Unity). C2 found the impact **trivial**. We lower it anyway since there's no visible downside, but don't expect FPS from it. | [U2](sources.md#u2), [C2](sources.md#c2) |
| `effects.maxgibs` | 0 | 0 | 1 | 1 | CPU | + | Building debris (gibs) when walls are destroyed. Gibs are physics objects, expected to cause **CPU spikes during raids**. 0 also clears debris you could otherwise lose players in. | reasoning |
| `effects.creationeffects` | False | False | False | True | GPU | · | Effects when building/placing. Cosmetic. | reasoning |
| `grass.quality` ⚠ | 0 | 0 | 50 | 100 | GPU+CPU | + | Lowest grass density on both low profiles. **Grass can't be fully removed**: it still renders at the minimum, and the game may clamp 0 up to its minimum (C2's lowest tested value was 1). The measured cost was only ~2% on high-end hardware. Fewer blades at the minimum make prone players slightly easier to spot. | [C2](sources.md#c2), [C3](sources.md#c3) |
| `grass.distance` ⚠ | 0 | 0 | 80 | 100 | GPU+CPU | + | How far grass draws. Set to the lowest value; the game may clamp it to its minimum. | reasoning |
| `grass.displacement` | False | False | True | True | CPU+GPU | · | Grass bending around players/entities. | reasoning |
| `decor.quality` | 0 | 0 | 50 | 100 | GPU+CPU | + | Small ground decorations (pebbles, small plants). Less clutter makes the ground easier to read. | reasoning |

## Water

| Convar | UL | L | B | Q | Cost | Vis. | Why | Src |
|---|---|---|---|---|---|---|---|---|
| `water.quality` | 0 | 0 | 1 | 2 | GPU | · | Water shading. The highest setting cost up to 10% near water in C2's test (quality 1 was 4% slower than 0). Matters a lot on coastal maps. | [C2](sources.md#c2) |
| `water.reflections` | 0 | 0 | 1 | 2 | GPU+CPU | · | 0 disables reflections, which gave an 8% FPS boost in C2's test. | [C2](sources.md#c2) |

## Textures & memory

| Convar | UL | L | B | Q | Cost | Vis. | Why | Src |
|---|---|---|---|---|---|---|---|---|
| `graphicssettings.globaltexturemipmaplimit` | 2 | 1 | 0 | 0 | VRAM | · | Unity documents it exactly: 0 = full, 1 = half, 2 = quarter-size textures (2D textures only). Running out of VRAM causes **stutter**, not just lower FPS. ≤2 GB cards: 2, 3–6 GB cards: 1, 8 GB+: 0. Player captures show Rust filling most of whatever VRAM it finds (5–5.8 GB on 6 GB cards), so 6 GB cards get half resolution. The [card overlays](../gpu/cards/) set this from your card's actual VRAM. The game now also has an "eighth resolution" level ([candidate](candidates.md)). | [U1](sources.md#u1), [C5](sources.md#c5) |
| `graphics.af` | 2 | 8 | 16 | 16 | GPU (bandwidth) | · | Anisotropic filtering keeps ground textures sharp at angles. Almost free on discrete GPUs, but it costs memory bandwidth on iGPUs (shared RAM), so ultra-low goes down to 2. | reasoning |

## Latency

| Convar | UL | L | B | Q | Cost | Vis. | Why | Src |
|---|---|---|---|---|---|---|---|---|
| `graphics.maxqueuedframes` | 1 | 1 | 1 | 1 | – | · | Unity: "Maximum number of frames queued up by graphics driver." Fewer queued frames means lower input latency, the same idea NVIDIA Reflex automates. On very weak CPUs, 2 can smooth frame times slightly at the cost of latency, so try it if your frame time graph is spiky. | [U2](sources.md#u2), [N1](sources.md#n1) |

`graphics.reflexmode` (NVIDIA Reflex), `graphics.dlss` and `graphics.dlaa` are vendor-specific and live in the [GPU overlays](../gpu/), not in the base profiles.

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

What we **don't** have is an official description of `gc.buffer`. A 2020 community guide says a larger buffer makes GC run less often, giving fewer periodic hitches at the cost of more RAM, and gives a default of 256 [[C1]](sources.md#c1). Our reference dump contains `1965`, which doesn't match that default and *suggests* (our inference) that newer builds size it automatically. Because of that we don't override it by default.

It's now also a slider in the game's **Experimental** tab (range 64–4082 according to a 2024 mapping [[C4]](sources.md#c4)), and it's very popular in Steam guides, but nobody has published measurements [[C6]](sources.md#c6).

If you get regular hitches every few seconds, the installer can set it manually. These values are community conventions, not measured:

| System RAM | Suggested `gc.buffer` |
|---|---|
| 8 GB | 1024 |
| 16 GB | 2048 |
| 32 GB+ | 4096 |

```powershell
powershell -ExecutionPolicy Bypass -File tools\apply.ps1 -Preset low -GcBuffer 2048
```

`install.bat` → **Restore my original config** undoes it.

---

## Verification backlog

Values marked ⚠ above need a check in the current build. The most reliable method: set the option in **Options → Graphics**, quit Rust (it rewrites `client.cfg`), and diff the file. Report findings in an issue or PR.

| Convar | Open question |
|---|---|
| `graphics.shadowmode` | Meaning of each level. Does 0 disable shadows entirely? How does it map to the new Shadow Quality preset [[F8]](sources.md#f8)? |
| `graphicssettings.shadowqualitypreset` | Is it what the March 2026 Shadow Quality preset writes? |
| `effects.antialiasing` | Confirm the 2024 mapping (0 Off / 1 FXAA / 2 SMAA / 3 TSSAA) [[C4]](sources.md#c4) still holds |
| `graphics.volumetric_clouds` | Levels 1–4 are documented [[F5]](sources.md#f5). Is 0 off? |
| `graphics.lodbias` | Lowest accepted value (0.25 or clamped to 0.5?) |
| `grass.quality` / `grass.distance` | Minimum values the game clamps to |

Unity documents that a `globaltexturemipmaplimit` value stripped at build time is moved to the nearest available mip [[U1]](sources.md#u1), so `2` is safe even if Rust ships fewer mips.

### Benchmark priorities

Every row marked `reasoning`, and every `C2` row (measured only on high-end hardware), is a hypothesis for low-end PCs. In order of expected impact, these are the ones to measure first:

1. `graphics.lodbias` (C2: up to 50% near compounds)
2. `graphics.drawdistance`, `tree.quality` / `tree.meshes`
3. `water.quality` / `water.reflections` (coast scene)
4. `effects.ao`, `effects.antialiasing`, shadows
5. `particle.quality`, `effects.maxgibs` (raid scenario)
6. `grass.quality` (measured small on high-end; is it larger on low-end?)

The reference dump also contains a few hand-appended lines (`graphics.shaderlod`, `graphics.grassshadows`, `graphics.shadowfilteringquality`, `graphicssettings.shadowcascades`, `graphicssettings.shadowresolution`) after a blank line. They are **not** written by the game itself, so they're excluded from all profiles until someone confirms they exist. `graphics.grassshadows` is the most interesting: C2 measured 3–4% from disabling "Grass Shadows".
