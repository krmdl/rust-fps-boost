# Changelog

## v0.4.0 – 2026-10-22

Community research round: four research passes over Steam Community guides and threads, howmanyfps player captures, guide sites and Facepunch devblogs (Reddit blocks automated access, so it isn't covered). Key claims were verified at the source before being applied.

### Changed
- `graphics.shadowlights` 0 → 1 on ultra-low and low: Facepunch raised the minimum to 1 in March 2026
- `tree.meshes` 0 → 10 on ultra-low: the slider's minimum
- `effects.sharpen` on for balanced and quality
- Texture rule R1: 6 GB cards now get half-resolution textures (Rust fills 5–5.8 GB on 6 GB cards in player captures); affects GTX 1060 6GB, GTX 1660 Super, RTX 2060

### Added
- "Free FPS fixes outside the config" in the README: mouse polling rate (official Facepunch PSA after the Unity 6 update) and the Rust Render Pipeline toggle
- Community reports with links on every card page; player evidence for CPU-bound behaviour
- Anti-aliasing mapping (0 Off / 1 FXAA / 2 SMAA / 3 TSSAA)
- Candidates: `rrp.enabled`, `culling.toggle`, eighth-resolution textures
- New launch-option myths and a note on convars as launch options
- Sources F8–F10 (Shipshape, Built Different, Livestock) and C4–C6 (convar mapping guide, howmanyfps, Steam Community)

## v0.3.0 – 2026-10-22

Reviewed by three specialist passes (presentation, technical accuracy, installer UX). Every finding was checked against its source before being applied.

### Added
- `install.bat`: double-click installer with Install / Preview / Undo / Restore original
- GPU auto-detection (real VRAM from the driver registry, prefers the dedicated card on laptops) and an interactive mode that suggests profile + card overlay
- `-Restore` and `-Restore -Original`; `client.cfg.original.bak` is kept forever, plus the last 5 backups
- `tools/validate.py` and `gen_cards.py --check`, run by GitHub Actions on every push
- Issue templates (benchmark, card request, bug), PR template, release workflow
- `docs/faq.md` with glossary; Safety and "Why trust this" sections in the README
- New sources: Facepunch changelists for HLOD, volumetric clouds, shadow caching, DLAA/TAA; a measured third-party benchmark (C2); NVIDIA's updated Reflex figure

### Fixed
- Installer corrupted non-ASCII text in `client.cfg` (PowerShell 5.1 read it as ANSI)
- Installer couldn't find Rust when a Steam library path had non-ASCII characters
- Only the first copy of a duplicated key was updated (Rust applies the last one)
- Read-only `client.cfg` ended in a raw error; writes are now atomic and keep line endings
- Wrong citation for the `vclouds` → `volumetric_clouds` rename
- Overstated grass claim: grass can't be fully removed, and its measured cost was small
- "1500 is the draw distance minimum" was wrong; `shadowqualitypreset 0` means hard shadows, not off
- Steam survey flags and shares for GTX 1650 / RTX 3050; RX 580 4GB bandwidth
- `reference/client.default.cfg` renamed to `client.dump.cfg`: its values are one player's settings, not game defaults

### Changed
- `-Profile` renamed to `-Preset` (old name still works)
- All profiles set `graphics.renderscale 1`, so leaving the `intel-igpu` overlay restores full resolution
- GTX/AMD overlays also force `graphics.dlaa False`
- `lodbias` is now the top benchmark priority (measured up to 50% near compounds)

## v0.2.0 – 2026-10-21

- Card overlays for 16 popular GPUs (GTX 1050 Ti → RTX 5070, RX 580 → RX 9070 XT), each with a page explaining every value
- Card list based on the September 2026 Steam Hardware Survey plus low-end cards
- `tools/gen_cards.py` generates overlays and pages from one table, using documented rules R1–R5
- `apply.ps1 -Gpu` accepts card names
- `docs/sources.md` with a source for every claim; unsourced claims marked as reasoning

## v0.1.0 – 2026-10-21

- Initial profiles: `ultra-low`, `low`, `balanced`, `quality`
- GPU overlays: `nvidia`, `amd`, `intel-igpu`
- `tools/apply.ps1` merge installer with backup and dry run
- Rationale docs for every convar, launch-option myth list, benchmark methodology
- Reference convar dump from the current game build
