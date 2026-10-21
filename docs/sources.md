# Sources

Every claim in these docs is backed by one of the sources below, or is marked as **reasoning** when no source exists yet.

## How to read the evidence

Rust is built on **Unity**, so many convars are thin wrappers over Unity engine features (`graphicssettings.*` mirrors Unity's `QualitySettings`). Unity's documentation tells us **how the engine feature costs performance**. That a given Rust convar maps to that feature is an **inference from its name and behaviour** unless a Facepunch source says so. We label it that way.

| Tag | Meaning | Strength |
|---|---|---|
| `[F*]` | Facepunch: Rust devblogs, changelogs | Official, Rust-specific |
| `[U*]` | Unity engine documentation | Official for the engine mechanism. Mapping to the Rust convar is inferred. |
| `[N*]` | NVIDIA announcements | Official vendor claim (best-case numbers) |
| `[G*]` | General graphics references | Explains the technique, not Rust |
| `[C*]` | Community guides and third-party benchmarks | Weak to medium. A measured third-party test (C2) beats reasoning, but it isn't our hardware. |
| reasoning | No source found. Logic only. | Weakest. Top priority for [benchmarks](../benchmarks/). |

## Facepunch (Rust)

<a id="f1"></a>**[F1]** Facepunch, *The Performance Update* (devblog, 6 Sep 2018). Explains that LOD distances on dozens of small objects were adjusted so they "LOD and cull quicker", that allocations causing **garbage-collector stutter** were fixed, and that most of the work targeted **CPU** performance. Swamp tree draw calls were halved by merging textures.
https://rust.facepunch.com/blog/the-performance-update

<a id="f2"></a>**[F2]** Facepunch, *November Update* (Prototype 17, 3 Nov 2022): "New HLOD monument rendering system".
https://rust.facepunch.com/changelist/3935

<a id="f3"></a>**[F3]** Facepunch, *September patch* (5 Sep 2024): "Fixed a case where switching HLOD convars would result in monument geometry not rendering".
https://rust.facepunch.com/changelist/3990

<a id="f4"></a>**[F4]** Facepunch, *Maintenance* devblog (4 Sep 2025): "the graphics.vclouds convar has been replaced by graphics.volumetric_clouds".
https://rust.facepunch.com/news/maintenance · https://rust.facepunch.com/changelist/4021

<a id="f5"></a>**[F5]** Facepunch, *Harder Core* devblog (7 Aug 2025): volumetric clouds "can also be enabled through the console using graphics.vclouds 1 through 4, with 4 being the highest quality but most taxing on your GPU".
https://rust.facepunch.com/news/harder-core/

<a id="f6"></a>**[F6]** Facepunch, *Common Ground* (2 Jul 2026): "Added an experimental shadow caching mode for improved shadow rendering performance" and "Fixed hatch on the ladder hatch not rendering shadows with 'graphics.aggressiveShadowLod' enabled".
https://rust.facepunch.com/changelist/4043

<a id="f7"></a>**[F7]** Facepunch, *2025 Recap* (1 Jan 2026): "Overhauled Graphics settings", "Added DLAA option to the graphics menu", "Improved TAA implementation", "Added 'fps.startlogging', outputs a csv of frametimes", "Fixed biome fog visibility being affected by draw distance".
https://rust.facepunch.com/changelist/4031

<a id="f8"></a>**[F8]** Facepunch, *Shipshape* (5 Mar 2026): "Max Shadow Lights has also had its minimum value changed to 1 to prevent light-leaking issues." The shadow settings were "reworked to be part of a Shadow Quality preset setting" under Graphics Quality, and the separate Shadow section was removed.
https://rust.facepunch.com/news/shipshape

<a id="f9"></a>**[F9]** Facepunch, *Built Different* (4 Jun 2026): "Upgrade to Unity 6". PSA: "The Unity 6 update changed how mouse inputs are processed. High polling rate mice (1000Hz+) are now causing significant CPU overhead issues and frame drops."
https://rust.facepunch.com/news/built-different

<a id="f10"></a>**[F10]** Facepunch, *Livestock Update* (1 Oct 2026): migration to the **Rust Render Pipeline**, "a custom Scriptable Render Pipeline made specifically for Rust". It can be toggled under the Experimental tab for the first month; "you should see slightly better performance in most areas of the game, as the new pipeline comes with less overhead." It is expected to become the default after the next patch.
https://rust.facepunch.com/news/livestock

## Unity engine

<a id="u1"></a>**[U1]** `QualitySettings.globalTextureMipmapLimit`: "1" = half-size textures, "2" = quarter-size, default 0. Changing it re-uploads loaded textures. Only applies to 2D textures.
https://docs.unity3d.com/ScriptReference/QualitySettings-globalTextureMipmapLimit.html

<a id="u2"></a>**[U2]** `QualitySettings` reference:
- `maxQueuedFrames`: "Maximum number of frames queued up by graphics driver."
- `particleRaycastBudget`: "Budget for how many ray casts can be performed per frame for approximate collision testing."
- `softParticles`: "Should soft blending be used for particles?"

https://docs.unity3d.com/ScriptReference/QualitySettings.html

<a id="u3"></a>**[U3]** `QualitySettings.lodBias`: a global multiplier for LOD switch distances. Lower values switch to cheaper LODs sooner and save rendering cost.
https://docs.unity3d.com/ScriptReference/QualitySettings-lodBias.html

<a id="u4"></a>**[U4]** LOD Group manual: during cross-fade transitions Unity "renders both the current and next LOD levels separately, and then cross-fades them together".
https://docs.unity3d.com/6000.1/Documentation/Manual/class-LODGroup.html

<a id="u5"></a>**[U5]** Shadow mapping manual: a point light's shadow is captured in **six directions**, a cost similar to six spot-light shadows, and it "increases the number of draw calls significantly".
https://docs.unity.com/en-us/engine/6000.3/manual/lighting-overview/shadows/shadow-realtime/shadow-mapping

<a id="u6"></a>**[U6]** Performance impact of shadow cascades: more cascades mean more draw calls in the shadow pass. Reducing cascades "significantly" reduces shadow draw calls.
https://docs.unity3d.com/Manual/shadow-cascades-performance.html

<a id="u7"></a>**[U7]** Optimize shadow rendering: "The number of real-time shadow-casting objects has a significant impact on shadow rendering performance."
https://docs.unity3d.com/Manual/shadows-optimization.html

<a id="u8"></a>**[U8]** Garbage collection modes: a non-incremental GC run stops the main thread and shows up as frame-time spikes. Incremental mode spreads the work across frames.
https://docs.unity3d.com/Manual/performance-incremental-garbage-collection.html

<a id="u9"></a>**[U9]** Unity Player command-line arguments. Lists `-window-mode` (accepted values `exclusive` / `borderless`, Windows only), `-force-d3d11-no-singlethreaded`, `-nolog`, `-logFile`, `-systemallocator`. **Does not list** `-maxMem`, `-malloc`, `-cpuCount`, `-exThreads` or `-high`.
https://docs.unity3d.com/Manual/PlayerCommandLineArguments.html

## NVIDIA

<a id="n1"></a>**[N1]** NVIDIA, *Rust: NVIDIA Reflex Gives Players A Free Upgrade* (May 2021). Reflex in Rust, GTX 900 series or newer, "up to 38%" lower system latency (vendor figure).
https://www.nvidia.com/en-gb/geforce/news/rust-reflex-out-now/

<a id="n2"></a>**[N2]** NVIDIA, *Rust: NVIDIA DLSS out now* (1 Jul 2021): "frame rates increased by up to 50% at 4K with DLSS" (vendor figure).
https://www.nvidia.com/en-us/geforce/news/rust-nvidia-dlss-out-now

<a id="n3"></a>**[N3]** NVIDIA, Reflex optimizations for Rust and Escape from Tarkov (24 Aug 2021): after the Reflex SDK 1.5 update, Reflex in Rust "reduces system latency by up to 51%". On Reflex Boost: "these optimizations can mean higher power usage or a slight reduction in FPS".
https://www.nvidia.com/en-us/geforce/news/nvidia-reflex-rust-escape-from-tarkov-optimizations

## Hardware data

<a id="h1"></a>**[H1]** Valve, *Steam Hardware & Software Survey: September 2026*, "All video cards" table: RTX 5070 6.15%, RTX 5060 4.40%, RTX 5060 Ti 4.06%, RTX 4060 3.89%, RTX 3060 3.66%, RTX 3050 2.90%, GTX 1650 2.19%, RX 9070 XT 1.42% (the most common AMD discrete card).
https://store.steampowered.com/hwsurvey/videocard/

<a id="h2"></a>**[H2]** TechPowerUp GPU database: architecture, VRAM, memory bus and bandwidth for every card page in [`gpu/cards/`](../gpu/cards/).
https://www.techpowerup.com/gpu-specs/

## General references

<a id="g1"></a>**[G1]** Simplygon documentation, *HLOD*: hierarchical LODs merge distant objects to reduce draw calls, memory and geometry complexity. Describes the technique in general (Unreal context), not Rust's implementation.
https://documentation.simplygon.com/SimplygonSDK_10.4.199.0/ue5/concepts/hlod.html

## Community (weak)

<a id="c1"></a>**[C1]** GameRevolution, *Rust: How to fix stuttering, lag spikes, and freezing* (Dec 2020). Recommends raising `gc.buffer` (e.g. 2048) to run GC less often, and gives a default of 256. **Old, community-only, and contradicted by the value in our reference dump (1965). We found no official Facepunch documentation for `gc.buffer`.**
https://www.gamerevolution.com/guides/670682-rust-how-fix-stuttering-lag-spikes-freezing

<a id="c2"></a>**[C2]** PCOptimizedSettings, *Rust PC settings optimization guide* (14 Apr 2025). Per-setting FPS measurements on **RTX 4090 + i9-12900K**. This is a high-end, often CPU-limited system, so its percentages show the direction of an effect, not its size on low-end PCs. It predates the 2025 graphics menu overhaul [[F7]](#f7). Figures we cite: LOD bias up to 50% near compounds, draw distance up to 10% (values 500–2500 tested), water quality up to 10%, water reflections 8%, AO up to 6%, shadow quality top value 5–6% (0 = hard shadows), tree quality up to 5%, sun shafts 3–4%, grass shadows 3–4%, shadow lights 2–4%, contact shadows 2–3%, grass quality ~2%, max tree meshes "nominal", particle raycast budget "trivial", TSSAA over 10% faster than DLAA.
https://pcoptimizedsettings.com/rust-optimized-settings-performance-guide-updated-april-2025/

<a id="c3"></a>**[C3]** Corrosion Hour, *How to turn off grass in Rust* (status as of 2018): grass can't be turned off or fully removed. Old, but nothing newer or official contradicts it.
https://www.corrosionhour.com/how-to-turn-off-grass-in-rust/

<a id="c4"></a>**[C4]** Steam guide mapping every menu option to its convar and range (checked July 2024, **before** the 2025–26 menu changes). Gives `effects.antialiasing` 0 = Off, 1 = FXAA, 2 = SMAA, 3 = TSSAA; `tree.meshes` 10–100; `graphics.reflexmode` 2 = On + Boost; `culling.toggle` = Occlusion Culling; `gc.buffer` 64–4082.
https://steamcommunity.com/sharedfiles/filedetails/?id=3180714936

<a id="c5"></a>**[C5]** howmanyfps.com Rust sessions (Mar–Oct 2026): player-submitted captures with avg / 1% low FPS, CPU/GPU usage, VRAM and the in-game settings. Real recordings, but location in the game isn't recorded and we haven't reproduced them. Individual sessions are linked from the card pages.
https://howmanyfps.com/benchmarks/rust

<a id="c6"></a>**[C6]** Steam Community: Rust discussion threads and the most-rated 2025–26 FPS guides (e.g. 3727010750, 3288259810). Player anecdotes, usually without settings or location; useful for consensus and for spotting problems (e.g. high polling rate mice), not as measurements. Individual threads are linked where cited.
https://steamcommunity.com/app/252490/discussions/

---

Found a better source, or one that contradicts us? Open an issue. Contradicting evidence is the most valuable kind.

*Sources last checked: 2026-10-21.*
