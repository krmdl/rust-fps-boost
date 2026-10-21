# Methodology

A config claim is only as good as the measurement behind it. Rust is a hard game to benchmark because servers, player counts, time of day and weather all change, so we keep the method strict.

## What we measure

- **Average FPS**: least important on its own
- **1% low FPS**: the number you actually *feel*, since stutter lives here
- **Frame time graph**: spikes show GC hitches, shader compilation, streaming

Use [CapFrameX](https://www.capframex.com/) or [PresentMon](https://github.com/GameTechDev/PresentMon) to capture. The in-game `perf 1` overlay works for quick checks but can't record. Rust also has a built-in logger: `fps.startlogging` in the F1 console "outputs a csv of frametimes" [[F7]](sources.md#f7), which needs no extra software.

## Test procedure

1. **Same server, same build.** Use a low-pop or local server (`Rust Staging` / your own) so player count doesn't vary. Note the Rust build number (main menu, bottom corner).
2. **Fixed time & weather.** On your own server, as admin: `env.time 12` and force clear weather. Otherwise note them.
3. **Three scenes**, 60 seconds each:
   - **Forest**: walk a fixed path through a dense forest (tree/grass-heavy, CPU+GPU)
   - **Town**: a large monument or base area (draw-call heavy, CPU)
   - **Coast**: looking over water toward the horizon (water/draw distance)
4. **Warm up first.** Play ~2 minutes before capturing so shaders compile and assets stream in.
5. **Three runs per scene**, report the median.
6. **One change at a time** when testing a single convar.

## Reporting

Copy [`benchmarks/TEMPLATE.md`](../benchmarks/TEMPLATE.md) to `benchmarks/<date>-<gpu>-<profile>.md` and fill it in. Include full hardware, driver version, resolution and Rust build.

## Confidence levels used in the docs

| Level | Meaning |
|---|---|
| *expected* | Reasoned from how the setting works. No data yet. |
| *measured* | At least one benchmark report in `benchmarks/` backs it up. |
| *confirmed* | Reproduced on 2+ different hardware setups. |

Until the first benchmark report lands, everything is *expected* (some rows cite third-party measurements on high-end hardware, see [convars.md](convars.md)).
