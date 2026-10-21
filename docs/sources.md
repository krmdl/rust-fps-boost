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
| `[C*]` | Community guides | Weak. Listed for transparency, needs benchmark confirmation. |
| reasoning | No source found. Logic only. | Weakest. Top priority for [benchmarks](../benchmarks/). |

## Facepunch (Rust)

<a id="f1"></a>**[F1]** Facepunch, *The Performance Update* (devblog, 6 Sep 2018). Explains that LOD distances on dozens of small objects were adjusted so they "LOD and cull quicker", that allocations causing **garbage-collector stutter** were fixed, and that most of the work targeted **CPU** performance. Swamp tree draw calls were halved by merging textures.
https://rust.facepunch.com/blog/the-performance-update

<a id="f2"></a>**[F2]** Facepunch changelog: adds a new **HLOD** monument rendering system.
https://rust.facepunch.com/changes/9

<a id="f3"></a>**[F3]** Facepunch, September patch changelist: `graphics.vclouds` replaced by `graphics.volumetric_clouds`, plus a fix for HLOD convars that could stop monument geometry from rendering.
https://rust.facepunch.com/changelist/3990

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

<a id="n2"></a>**[N2]** NVIDIA, June 2021 RTX/DLSS game update: DLSS added to Rust (July 2021), "up to 50%" more performance at 4K (vendor figure).
https://www.nvidia.com/en-us/geforce/news/june-2021-rtx-dlss-game-update/

## General references

<a id="g1"></a>**[G1]** Simplygon documentation, *HLOD*: hierarchical LODs merge distant objects to reduce draw calls, memory and geometry complexity. Describes the technique in general (Unreal context), not Rust's implementation.
https://documentation.simplygon.com/SimplygonSDK_10.4.199.0/ue5/concepts/hlod.html

## Community (weak)

<a id="c1"></a>**[C1]** GameRevolution, *Rust: How to fix stuttering, lag spikes, and freezing*. Recommends raising `gc.buffer` (e.g. 2048) to run GC less often. **Community sources disagree on the default value and exact semantics, and we found no official Facepunch documentation for `gc.buffer`.**
https://www.gamerevolution.com/?p=670682

---

Found a better source, or one that contradicts us? Open an issue. Contradicting evidence is the most valuable kind.

*Sources last checked: 2026-10-21.*
