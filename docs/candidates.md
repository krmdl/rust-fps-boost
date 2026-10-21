# Candidates: convars to test

These appear in the game's own config dump and *might* improve performance, but how they behave isn't clear enough to ship in a profile yet. Each needs an A/B benchmark ([methodology.md](methodology.md)) before it moves into a profile.

| Convar | Default | Hypothesis | Risk |
|---|---|---|---|
| `shadowcaching.enabled` | False | Facepunch added it as "an experimental shadow caching mode for improved shadow rendering performance" [[F6]](sources.md#f6). It updates distant shadows at lower rates (`shadowcaching.updateminframerate` / `updatemaxframerate`). Purpose confirmed; still experimental, so it needs an A/B test before it ships. | Shadow lag / flicker on moving objects. Could hide or delay enemy shadows. |
| `indirect_instancing.enabled` | False | GPU-driven indirect instanced rendering: fewer CPU draw calls. Possibly a large win on CPU-bound systems. | Experimental, may cause artifacts or crashes. |
| `render.instancing_render_distance` | 1500 | Lowering it might cut instanced objects at distance. | Distant bases/deployables may disappear. |
| `culling.entitymaxdist` | 5000 | Lower max entity distance means fewer entities processed. | Could cull things you need to see at long range. |
| `playercull.maxplayerdist` | 2000 | Already above draw distance, so lowering it may save little. | Distant players vanish. **Gameplay risk.** |
| `grass.refresh_budget` / `lod.grid_refresh_budget` | 0.1 | Per-frame time budget for grass/LOD updates. Lowering it might smooth frame times when moving fast. | Visible pop-in / late LOD updates. |
| `mesh.reducebonecountonlowlod` | True | Already on (good). Confirm it stays on. | – |
| `system.auto_cpu_affinity` | False | Lets the game pin threads to cores. Could help on hybrid CPUs (Intel 12th gen+ P/E cores). | Could hurt on some CPUs. Hardware-dependent, so it may become a CPU overlay. |
| `graphics.collapserenderers` | True | Unclear purpose. Possibly batches renderers. Check whether False changes anything. | – |
| `rrp.enabled` | False (in our dump) | Most likely the toggle for the new **Rust Render Pipeline**. Facepunch expects "slightly better performance in most areas" and plans to make it the default [[F10]](sources.md#f10). The convar name is our inference (Facepunch didn't name it); try the Experimental tab toggle in the meantime. **Top candidate.** | Experimental for its first month: "in case there are any issues". |
| `culling.toggle` | True | Occlusion Culling (Experimental tab) [[C4]](sources.md#c4). The most-rated Steam guides turn it off, and Facepunch noted in 2018 that its CPU cost "may overshadow the benefits" [[F1]](sources.md#f1). Off might help CPU-bound PCs. | Could cost GPU time instead; hardware-dependent, needs an A/B test. |
| `graphicssettings.globaltexturemipmaplimit 3` | – | Player captures show a new "eighth resolution" texture level [[C5]](sources.md#c5) (Unity: 3 = eighth size [[U1]](sources.md#u1)). Could help ≤2 GB cards and iGPUs. | Very blurry textures. |
| `graphics.shadowdistance` | not in dump | Some guides recommend it (50–1000), but it doesn't appear in our reference dump and players report it no longer exists [[C6]](sources.md#c6). Not usable unless it reappears. | – |

Found something? Open a PR moving the row to [convars.md](convars.md) with a benchmark report attached.
