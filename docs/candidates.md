# Candidates: convars to test

These appear in the game's own config dump and *might* improve performance, but how they behave isn't clear enough to ship in a profile yet. Each needs an A/B benchmark ([methodology.md](methodology.md)) before it moves into a profile.

| Convar | Default | Hypothesis | Risk |
|---|---|---|---|
| `shadowcaching.enabled` | False | Caches shadow maps and updates distant shadows at lower rates (`shadowcaching.updateminframerate` / `updatemaxframerate`). Could be a big CPU win, since shadows are among the highest draw-call costs. | Shadow lag / flicker on moving objects. Could hide or delay enemy shadows. |
| `indirect_instancing.enabled` | False | GPU-driven indirect instanced rendering: fewer CPU draw calls. Possibly a large win on CPU-bound systems. | Experimental, may cause artifacts or crashes. |
| `render.instancing_render_distance` | 1500 | Lowering it might cut instanced objects at distance. | Distant bases/deployables may disappear. |
| `culling.entitymaxdist` | 5000 | Lower max entity distance means fewer entities processed. | Could cull things you need to see at long range. |
| `playercull.maxplayerdist` | 2000 | Already above draw distance, so lowering it may save little. | Distant players vanish. **Gameplay risk.** |
| `grass.refresh_budget` / `lod.grid_refresh_budget` | 0.1 | Per-frame time budget for grass/LOD updates. Lowering it might smooth frame times when moving fast. | Visible pop-in / late LOD updates. |
| `mesh.reducebonecountonlowlod` | True | Already on (good). Confirm it stays on. | – |
| `system.auto_cpu_affinity` | False | Lets the game pin threads to cores. Could help on hybrid CPUs (Intel 12th gen+ P/E cores). | Could hurt on some CPUs. Hardware-dependent, so it may become a CPU overlay. |
| `graphics.collapserenderers` | True | Unclear purpose. Possibly batches renderers. Check whether False changes anything. | – |

Found something? Open a PR moving the row to [convars.md](convars.md) with a benchmark report attached.
