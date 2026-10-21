# Steam launch options

Set them in Steam: right-click Rust → **Properties → General → Launch Options**.

Rust runs on a modern Unity version. A lot of launch options floating around in "FPS boost" videos come from Unity 5-era (2015–2017) Rust. Our yardstick is Unity's official list of player command-line arguments [[U9]](sources.md#u9): **if a flag isn't on that list and Facepunch hasn't documented it, we assume the engine ignores it.**

## Recommended

| Option | Why | Src |
|---|---|---|
| `-window-mode exclusive` | Unity documents `exclusive` and `borderless` as the accepted values (Windows only). Exclusive fullscreen bypasses the Windows compositor, which can give slightly lower latency than borderless. Only matters if you play fullscreen. | [U9](sources.md#u9) (flag), reasoning (latency) |

That's the whole list. In-game settings and convars do the real work.

## Valid but not recommended

| Option | Why not | Src |
|---|---|---|
| `-force-d3d11-no-singlethreaded` | A real Unity flag: creates the D3D11 device without the single-threaded flag. Unity's docs don't claim a performance effect, and we have no Rust benchmark showing one. | [U9](sources.md#u9) |
| `-nolog` | A real Unity flag ("Disables Player logging"). The time saved is negligible, and it makes crashes impossible to diagnose. | [U9](sources.md#u9) |
| `-systemallocator` | A real Unity flag that forces the OS memory allocator instead of Unity's own. No evidence that it helps Rust, and it may hurt. This is the modern descendant of the old `-malloc=system` advice. | [U9](sources.md#u9) |

## Not documented: almost certainly no effect

None of these appear in Unity's player argument list [[U9]](sources.md#u9), and we found no Facepunch documentation for them.

| Option | Notes |
|---|---|
| `-maxMem=XXXX` | Not a Unity argument. |
| `-malloc=system` | Not in the current Unity argument list (see `-systemallocator` above). |
| `-cpuCount=N` | Not a Unity argument. Unity detects cores itself. |
| `-exThreads=N` | Not a Unity argument. |
| `-high` | Not a Unity argument. The idea (raising process priority) can be tested with Task Manager instead, but we have no evidence it helps. |
| `-USEALLAVAILABLECORES` | A Source-engine flag, not Unity. |

If you have benchmark data showing a measurable effect for any of these on the current build, open an issue (see [methodology.md](methodology.md)). We'll move it, with the evidence.

## Related settings outside the config

These aren't in our profiles because they're personal, but they matter. *They're based on general practice, not Rust-specific sources.*

- **FPS cap (`fps.limit`)**: on weak hardware, capping a little below your average (e.g. 60 on a laptop that swings between 55 and 80) usually gives **smoother** frame times and lower temperatures than running uncapped. Pick a cap you can hold in busy areas.
- **V-Sync (`graphics.vsync 0`)**: keep it off for lowest latency. Use your monitor's G-Sync/FreeSync with an FPS cap a few frames below refresh instead.
- **Windows Game Mode**: leave it on (the default) on modern Windows 10/11.
- **Hardware-accelerated GPU scheduling**: results vary by GPU and driver. Measure before and after.
