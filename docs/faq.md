# FAQ

## Installing

**"Running scripts is disabled on this system".** Use `install.bat`, or include `-ExecutionPolicy Bypass` exactly as shown in the docs. On school or work PCs an administrator may block this entirely.

**"Could not find Rust automatically".** In Steam: right-click Rust → **Manage → Browse local files**. Copy that folder path and run:

```powershell
powershell -ExecutionPolicy Bypass -File tools\apply.ps1 -RustPath "D:\SteamLibrary\steamapps\common\Rust"
```

**"Rust is running".** Quit Rust completely, not just to the main menu. Rust writes its settings to `client.cfg` when it closes, which would overwrite ours.

**Windows shows "Windows protected your PC".** That's SmartScreen warning about any file downloaded from the internet. Click **More info → Run anyway**. Both `install.bat` and `tools/apply.ps1` are plain text you can read first.

**I made `client.cfg` read-only to stop Rust overwriting it.** The installer handles that: it removes the flag, writes, and sets it back.

## After installing

**Did it work?** In Rust press **F1**, type `graphics.drawdistance` and press Enter. It should show the profile's value (for example 1500 on `low`).

**My settings went back to normal.** Picking a preset in Rust's Graphics menu overwrites these values, and big game updates can too. Quit Rust and run the installer again.

**How do I undo it?** `install.bat` → **3** undoes the last install, **4** restores the config from before your first install. Backups are in `Rust\cfg\` (`client.cfg.original.bak` plus the last 5 timestamped ones).

**Laptop with two GPUs?** The installer picks the dedicated card. Also make sure Windows runs Rust on it: **Settings → System → Display → Graphics**, add `RustClient.exe`, choose **High performance**.

**How do I know if I'm CPU- or GPU-bound?** Open Task Manager → **Performance → GPU** while playing (or the NVIDIA Alt+R / AMD Ctrl+Shift+O overlay). GPU usage near 95–100% means GPU-bound: graphics settings help a lot. Well below 90% means CPU-bound: lower draw distance, trees and LOD settings help more than resolution.

## About the project

**Why don't you set `gc.buffer`, `-high` or `-maxMem`?** `gc.buffer` has no official documentation and seems to be sized automatically now ([details](convars.md#gcbuffer-ram)). `-high` and `-maxMem` aren't Unity arguments at all ([details](launch-options.md)).

**Can I get banned for this?** These are the same settings the in-game menu writes to `client.cfg`. We can't speak for Facepunch or Easy Anti-Cheat, but nothing here modifies the game or its memory.

**Does it work on modded or community servers?** Yes. These are client-side graphics settings and don't depend on the server.

**Why is grass still there on `low`?** Rust doesn't let you turn grass off completely. The profiles set it to the minimum ([details](convars.md#particles-gibs-foliage)).

## Glossary

| Term | Meaning |
|---|---|
| convar | One setting line in `client.cfg`, e.g. `grass.quality "0"` |
| profile | The base set of settings: `ultra-low`, `low`, `balanced`, `quality` |
| overlay | A small extra file for your graphics card or vendor, applied after the profile |
| VRAM | Memory on the graphics card (Task Manager → Performance → GPU → "Dedicated GPU memory") |
| iGPU | Graphics built into the CPU, no separate card |
| CPU-bound / GPU-bound | Which part is holding your FPS back (see above) |
| 1% lows | Your worst frames. This is the stutter you feel. |
| LOD | Level of detail: distant objects switching to simpler models |
| F1 console | Rust's command box (press F1 in game) |
| render scale | Renders the 3D world at a lower resolution while menus stay sharp |
