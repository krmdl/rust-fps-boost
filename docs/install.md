# Install

## Where the config lives

```
<Steam library>\steamapps\common\Rust\cfg\client.cfg
```

Default Steam library: `C:\Program Files (x86)\Steam`. If Rust is on another drive, right-click Rust in Steam → **Manage → Browse local files** → `cfg`.

> **Important:** Rust reads `client.cfg` on startup and **writes it back when you quit**. Always edit it with the game closed, or your changes will be overwritten.

## Option A: installer script (recommended)

From the repo folder:

```powershell
powershell -ExecutionPolicy Bypass -File tools\apply.ps1 -Profile low
```

The script:

1. Finds your Rust install through Steam's library list (or use `-RustPath`)
2. Refuses to run while `RustClient.exe` is running
3. Backs up your current config to `cfg\client.cfg.<timestamp>.bak`
4. Changes **only** the keys in the chosen profile (and overlay); every other line stays as it is

Options:

| Parameter | Example | Meaning |
|---|---|---|
| `-Profile` | `ultra-low`, `low`, `balanced`, `quality` | Base profile (required) |
| `-Gpu` | `nvidia`, `amd`, `intel-igpu` | Optional GPU overlay, applied after the profile |
| `-GcBuffer` | `2048` | Optional manual `gc.buffer`. See [convars.md](convars.md#gcbuffer-ram) |
| `-RustPath` | `D:\SteamLibrary\steamapps\common\Rust` | Skip auto-detection |
| `-DryRun` | | Show what would change, write nothing |

## Option B: manual

1. Close Rust.
2. Back up `client.cfg`.
3. Open the profile file (e.g. [`profiles/low.cfg`](../profiles/low.cfg)). For each line, find the same key in your `client.cfg` and replace the value. Add any key that's missing.
4. Save and launch Rust.

**Don't replace the whole file** with a profile. Profiles only contain the performance settings, so replacing the file would reset everything else (sensitivity, audio, etc.) to defaults.

## Restoring a backup

Close Rust, delete `client.cfg`, rename the backup you want (e.g. `client.cfg.20261021-164300.bak`) to `client.cfg`.

You can also pick one of the game's own quality presets in **Options → Graphics** to reset, then fine-tune from there.
