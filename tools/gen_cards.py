"""Generates gpu/cards/<slug>.cfg and <slug>.md from the CARDS table.

The rules (R1-R5) are documented in gpu/cards/README.md. To add a card, add a
row below and run:  python tools/gen_cards.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "gpu" / "cards"
SRC = "../../docs/sources.md"

# slug, display name, vendor, architecture, VRAM (GB), bus (bit), bandwidth (GB/s),
# has DLSS, 1080p profile, 1440p profile, in Steam survey top list, notes
CARDS = [
    ("gtx-1050-ti", "NVIDIA GeForce GTX 1050 Ti", "nvidia", "Pascal", 4, 128, 112, False,
     "low", "ultra-low", False,
     ["Often paired with older 4-core CPUs. If GPU usage stays well below 95%, you're CPU-bound: "
      "drop to `ultra-low` for its shorter LOD/tree distances rather than lowering resolution.",
      "At 1440p, consider the `intel-igpu` overlay's render scale idea: run `graphics.renderscale 0.75` manually."]),
    ("gtx-1060-6gb", "NVIDIA GeForce GTX 1060 6GB", "nvidia", "Pascal", 6, 192, 192, False,
     "low", "ultra-low", False,
     ["6 GB is enough for full-resolution textures at 1080p (R1). If you see stutter when turning quickly "
      "in towns, try `graphicssettings.globaltexturemipmaplimit 1` and compare.",
      "Pascal has no tensor cores: no DLSS."]),
    ("gtx-1060-3gb", "NVIDIA GeForce GTX 1060 3GB", "nvidia", "Pascal", 3, 192, 192, False,
     "low", "ultra-low", False,
     ["Not just less VRAM: the 3 GB model also has fewer CUDA cores (1152 vs 1280) than the 6 GB model.",
      "3 GB is the main limit. Keep half-resolution textures (R1) even on `balanced`."]),
    ("gtx-1650", "NVIDIA GeForce GTX 1650", "nvidia", "Turing (TU117)", 4, 128, 128, False,
     "low", "ultra-low", False,
     ["Sold with GDDR5 (128 GB/s) and GDDR6 (192 GB/s) memory. Same overlay for both; the GDDR6 version is somewhat faster.",
      "Turing, but **no tensor cores**: DLSS is not available on GTX 16-series cards."]),
    ("gtx-1660-super", "NVIDIA GeForce GTX 1660 Super", "nvidia", "Turing (TU116)", 6, 192, 336, False,
     "low", "low", False,
     ["Strong for its tier thanks to GDDR6 bandwidth. If `low` holds well above your target FPS, try `balanced` at 1080p.",
      "No tensor cores: no DLSS."]),
    ("rtx-2060", "NVIDIA GeForce RTX 2060", "nvidia", "Turing (TU106)", 6, 192, 336, True,
     "balanced", "low", False,
     ["A 12 GB variant also exists. R1 gives full-res textures for both.",
      "First-generation RTX: DLSS works. At 1440p, DLSS *Quality* can make `balanced` viable."]),
    ("rtx-3050", "NVIDIA GeForce RTX 3050", "nvidia", "Ampere (GA106/GA107)", 8, 128, 224, True,
     "low", "low", False,
     ["Desktop 8 GB version. A slower 6 GB desktop variant exists (still full-res textures under R1).",
      "**Laptop** RTX 3050 cards often have only 4 GB: set `graphicssettings.globaltexturemipmaplimit 1` yourself.",
      "Use DLSS at 1440p."]),
    ("rtx-3060", "NVIDIA GeForce RTX 3060", "nvidia", "Ampere (GA106)", 12, 192, 360, True,
     "balanced", "balanced", True,
     ["12 GB is plenty for full-res textures even on lower profiles (R1).",
      "An 8 GB / 128-bit variant exists and is noticeably slower. If you have it, prefer `low` at 1440p.",
      "At 1440p, pair `balanced` with DLSS *Quality*."]),
    ("rtx-4060", "NVIDIA GeForce RTX 4060", "nvidia", "Ada Lovelace (AD107)", 8, 128, 272, True,
     "balanced", "balanced", True,
     ["Narrow 128-bit bus, partly offset by a large L2 cache.",
      "At this tier Rust is frequently CPU-bound at 1080p: if GPU usage is below ~90%, raising settings costs little FPS."]),
    ("rtx-5060", "NVIDIA GeForce RTX 5060", "nvidia", "Blackwell (GB206)", 8, 128, 448, True,
     "balanced", "balanced", True,
     ["GDDR7 gives much more bandwidth than older 8 GB cards on the same 128-bit bus.",
      "Likely CPU-bound at 1080p on most systems. Check GPU usage before lowering settings."]),
    ("rtx-5060-ti", "NVIDIA GeForce RTX 5060 Ti", "nvidia", "Blackwell (GB206)", 8, 128, 448, True,
     "quality", "balanced", True,
     ["Sold with 8 GB and 16 GB. Same overlay for both: full-res textures either way (R1)."]),
    ("rtx-5070", "NVIDIA GeForce RTX 5070", "nvidia", "Blackwell (GB205)", 12, 192, 672, True,
     "quality", "quality", True,
     ["The most common card on Steam right now [[H1]](" + SRC + "#h1).",
      "Rust will almost always be CPU-bound on this card at 1080p. FPS then depends on your CPU, not these settings.",
      "Consider `graphics.reflexmode 2` (On + Boost) on desktop if CPU-bound. It keeps GPU clocks up at the cost of power."]),
    ("rx-580-8gb", "AMD Radeon RX 580 8GB", "amd", "Polaris", 8, 256, 256, False,
     "low", "ultra-low", False,
     ["8 GB is a lot for a card of this speed: textures are free to max out (R1), but other settings are not.",
      "Use Radeon Anti-Lag in the Adrenalin driver for lower latency (no Reflex on AMD)."]),
    ("rx-580-4gb", "AMD Radeon RX 580 4GB", "amd", "Polaris", 4, 256, 256, False,
     "low", "ultra-low", False,
     ["Same GPU as the 8 GB model; only the VRAM differs, so textures stay at half resolution (R1).",
      "Use Radeon Anti-Lag in the Adrenalin driver."]),
    ("rx-6600", "AMD Radeon RX 6600", "amd", "RDNA 2 (Navi 23)", 8, 128, 224, False,
     "balanced", "low", False,
     ["32 MB Infinity Cache offsets the narrow bus at 1080p; the advantage shrinks at 1440p.",
      "The reference dump has no FSR convar, so on AMD the only upscaling option is `graphics.renderscale`."]),
    ("rx-9070-xt", "AMD Radeon RX 9070 XT", "amd", "RDNA 4 (Navi 48)", 16, 256, 645, False,
     "quality", "quality", True,
     ["The most common AMD card in the current Steam survey top list [[H1]](" + SRC + "#h1).",
      "Rust's reference dump contains no FSR convar, so FSR 4 can't be used in-game.",
      "Almost always CPU-bound at 1080p."]),
]


def mip_for(vram):
    if vram <= 2:
        return 2
    if vram <= 4:
        return 1
    return 0


MIP_TEXT = {0: "full resolution", 1: "half resolution", 2: "quarter resolution"}


def overlay(card):
    _, _, vendor, _, vram, _, _, dlss, *_ = card
    lines = [f'graphics.reflexmode "{1 if vendor == "nvidia" else 0}"']
    if not dlss:
        lines.append('graphics.dlss "-1"')
    lines.append(f'graphicssettings.globaltexturemipmaplimit "{mip_for(vram)}"')
    lines.append('graphics.af "16"')
    return lines


def page(card):
    slug, name, vendor, arch, vram, bus, bw, dlss, p1080, p1440, survey, notes = card
    mip = mip_for(vram)
    rows = [
        ("`graphics.reflexmode`", "1" if vendor == "nvidia" else "0",
         "R2: NVIDIA Reflex lowers input latency (GTX 900 series and newer)." if vendor == "nvidia"
         else "R2: Reflex is NVIDIA-only. Use Radeon Anti-Lag in the driver instead.",
         f"[N1]({SRC}#n1)"),
    ]
    if not dlss:
        rows.append(("`graphics.dlss`", "-1",
                     "R3: this card has no tensor cores, so DLSS is forced off.",
                     f"[N2]({SRC}#n2)"))
    rows.append(("`graphicssettings.globaltexturemipmaplimit`", str(mip),
                 f"R1: {vram} GB VRAM → {MIP_TEXT[mip]} textures. Overrides the profile value.",
                 f"[U1]({SRC}#u1)"))
    rows.append(("`graphics.af`", "16",
                 "R4: anisotropic filtering is cheap on a discrete card's memory bandwidth.",
                 "reasoning"))

    md = [f"# {name}", ""]
    if survey:
        md += [f"In the top of the Steam Hardware Survey (September 2026) [[H1]]({SRC}#h1).", ""]
    md += [
        "## Specs", "",
        "| | |", "|---|---|",
        f"| Architecture | {arch} |",
        f"| VRAM | {vram} GB |",
        f"| Memory bus | {bus}-bit |",
        f"| Bandwidth | ~{bw} GB/s |",
        f"| NVIDIA Reflex | {'Yes' if vendor == 'nvidia' else 'No'} |",
        f"| DLSS | {'Yes' if dlss else 'No'} |",
        "", f"Source: TechPowerUp GPU database [[H2]]({SRC}#h2).", "",
        "## Recommended setup", "",
        "| Resolution | Profile | Command |", "|---|---|---|",
        f"| 1080p | `{p1080}` | `tools\\apply.ps1 -Profile {p1080} -Gpu {slug}` |",
        f"| 1440p | `{p1440}` | `tools\\apply.ps1 -Profile {p1440} -Gpu {slug}` |",
        "",
        "Profile choice is an **estimate** from this card's performance tier (rule R5). It hasn't been "
        "benchmarked yet. If you're on this card, a [benchmark report](../../benchmarks/README.md) is the most "
        "useful thing you can contribute.",
        "",
    ]
    if dlss:
        md += [
            "**DLSS:** set it in **Options → Graphics** (not in the overlay, because the convar's value mapping is "
            "unverified). DLSS helps when you're GPU-bound. At 1080p use *Quality* at most; at 1440p *Quality* or "
            "*Balanced*.",
            "",
        ]
    md += [
        "## What this overlay sets, and why", "",
        "| Convar | Value | Why | Src |", "|---|---|---|---|",
        *[f"| {c} | {v} | {w} | {s} |" for c, v, w, s in rows],
        "",
        "Rules R1–R5 are explained in [the card overlay README](README.md#what-a-card-overlay-changes-and-the-rules-behind-it).",
        "",
        "## Card-specific notes", "",
        *[f"- {n}" for n in notes],
        "",
        "## Benchmark status", "",
        "No reports yet.",
        "",
    ]
    return "\n".join(md)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    table = []
    for card in CARDS:
        slug, name, _, _, vram, *_ = card
        (OUT / f"{slug}.cfg").write_text("\n".join(overlay(card)) + "\n", encoding="utf-8", newline="\n")
        (OUT / f"{slug}.md").write_text(page(card), encoding="utf-8", newline="\n")
        table.append(f"| [{name}]({slug}.md) | {vram} GB | `{slug}` | `{card[8]}` | `{card[9]}` |")

    readme = OUT / "README.md"
    text = readme.read_text(encoding="utf-8")
    start, end = "<!-- cards:start -->", "<!-- cards:end -->"
    block = "\n".join([start, *table, end])
    if start in text:
        text = text[:text.index(start)] + block + text[text.index(end) + len(end):]
    else:
        text = text.replace("CARD_TABLE", block)
    readme.write_text(text, encoding="utf-8", newline="\n")
    print(f"Generated {len(CARDS)} cards in {OUT}")


if __name__ == "__main__":
    main()
