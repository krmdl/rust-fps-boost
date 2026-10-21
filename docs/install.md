# Install

## Where the config lives

```
<Steam library>\steamapps\common\Rust\cfg\client.cfg
```

Default Steam library: `C:\Program Files (x86)\Steam`. If Rust is on another drive, right-click Rust in Steam → **Manage → Browse local files** → `cfg`.

> **Important:** Rust reads `client.cfg` on startup and **writes it back when you quit**. Always change it with the game closed, or your changes will be overwritten.

## Option A: `install.bat` (easiest)

1. Download the repo (green **Code** button → **Download ZIP**) and **Extract All**. Running it from inside the ZIP won't work.
2. Quit Rust completely.
3. Double-click `install.bat`:

| Choice | What it does |
|---|---|
| **1. Install** | Detects your graphics card, asks your resolution, suggests a profile and card overlay, and applies them (you can change the suggestion) |
| **2. Preview only** | Same questions, shows the changes, writes nothing |
| **3. Undo last install** | Restores the backup from right before your last install |
| **4. Restore original** | Restores your config from before you first used this project |

## Option B: command line

From the repo folder (Win10: Shift+right-click the folder → *Open PowerShell window here*; Win11: right-click → *Open in Terminal*):

```powershell
powershell -ExecutionPolicy Bypass -File tools\apply.ps1 -Preset low -Gpu gtx-1650
```

Run it with no `-Preset` for the interactive mode that `install.bat` uses.

| Parameter | Example | Meaning |
|---|---|---|
| `-Preset` | `ultra-low`, `low`, `balanced`, `quality` | Base profile. `-Profile` also works. |
| `-Gpu` | `gtx-1650`, `rtx-3060`, `nvidia`, `amd`, `intel-igpu` | Card overlay ([list](../gpu/cards/README.md#all-cards)) or vendor overlay, applied after the profile |
| `-GcBuffer` | `2048` | Optional manual `gc.buffer`. See [convars.md](convars.md#gcbuffer-ram) |
| `-RustPath` | `D:\SteamLibrary\steamapps\common\Rust` | Skip auto-detection |
| `-DryRun` | | Show what would change, write nothing |
| `-Restore` | | Undo the last install |
| `-Restore -Original` | | Restore the config from before the first install |

What the script does:

1. Finds your Rust install through Steam's library list (it confirms Rust is really installed there, not just a leftover folder).
2. Refuses to run while `RustClient.exe` is running.
3. Keeps `client.cfg.original.bak` (written once, never overwritten) plus the last 5 timestamped backups.
4. Changes **only** the keys in the chosen profile and overlay. Every other line, your file's line endings and any non-English text stay as they are.
5. Handles a read-only `client.cfg`, and writes via a temp file so a failure can't leave a half-written config.

## Option C: manual

1. Close Rust.
2. Back up `client.cfg`.
3. Open the profile file (e.g. [`profiles/low.cfg`](../profiles/low.cfg)). For each line, find the same key in your `client.cfg` and replace the value. Add any key that's missing. Then do the same with your card's overlay file.
4. Save and launch Rust.

**Don't replace the whole file** with a profile. Profiles only contain the performance settings, so replacing the file would reset everything else (sensitivity, audio, etc.) to defaults.

## Restoring

Use `install.bat` → **3** or **4**, or `-Restore` / `-Restore -Original` from the command line.

You can also pick one of the game's own presets in **Options → Graphics** to reset, then fine-tune from there.

More help: [faq.md](faq.md).
