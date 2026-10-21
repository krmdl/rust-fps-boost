# Steam launch options

Set them in Steam: right-click Rust → **Properties → General → Launch Options**.

Rust runs on a modern Unity version. A lot of launch options floating around in "FPS boost" videos come from Unity 5-era (2015–2017) Rust and **do nothing today**, or make things worse.

## Recommended

| Option | Why |
|---|---|
| `-window-mode exclusive` | Exclusive fullscreen. Bypasses the Windows compositor, which gives slightly lower latency and, on some systems, better frame pacing than borderless. Only matters if you play fullscreen. |

That's the whole list. In-game settings and convars do the real work.

## Situational

| Option | When |
|---|---|
| `-high` | Raises process priority. Can help a little on a weak CPU with heavy background apps (browser, Discord with video). Can also starve audio/voice chat. Test it; don't assume. |
| `-force-d3d11-no-singlethreaded` | A Unity flag for multithreaded D3D11 device access. Rust already renders multithreaded, so expect no gain. Listed only because it shows up in many guides. |

## Myths & not worth it

| Option | Why not |
|---|---|
| `-maxMem=XXXX` | Not a Unity runtime flag. It has no effect. |
| `-malloc=system` | Removed from Unity years ago. It does nothing, or crashed older builds. |
| `-cpuCount=N` | Unity detects cores itself. This doesn't make the game use more cores. |
| `-exThreads=N` | Same as above. Ignored. |
| `-USEALLAVAILABLECORES` | Source engine folklore, not a Unity flag. |
| `-nolog` | Saves almost nothing and makes crashes impossible to diagnose. |

If you know of a measurable benefit for any of these on the current build, open an issue with benchmark data (see [methodology.md](methodology.md)).

## Related settings outside the config

These aren't in our profiles because they're personal, but they matter:

- **FPS cap (`fps.limit`)**: on weak hardware, capping a little below your average (e.g. 60 on a laptop that swings between 55 and 80) gives **smoother** frame times and lower temperatures than running uncapped. Pick a cap you can hold in busy areas.
- **V-Sync (`graphics.vsync 0`)**: keep it off for lowest latency. Use your monitor's G-Sync/FreeSync with an FPS cap 3 below refresh instead.
- **Windows Game Mode**: leave it on (the default) on modern Windows 10/11.
- **Hardware-accelerated GPU scheduling**: results vary by GPU and driver. Measure before and after.
