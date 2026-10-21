"""Generates gpu/cards/<slug>.cfg + <slug>.md and the card lists in the READMEs.

The rules (R1-R5) are documented in gpu/cards/README.md. To add a card, add an
entry to CARDS and run:

    python tools/gen_cards.py           # write files
    python tools/gen_cards.py --check   # CI: fail if anything is out of date
"""
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "gpu" / "cards"
SRC = "../../docs/sources.md"
SURVEY_MONTH = "September 2026"
PROFILES = ("ultra-low", "low", "balanced", "quality")
VENDORS = {"nvidia": "NVIDIA GeForce", "amd": "AMD Radeon"}
APPLY = "powershell -ExecutionPolicy Bypass -File tools\\apply.ps1 -Preset {preset} -Gpu {slug}"


@dataclass
class Card:
    slug: str
    name: str
    vendor: str
    arch: str
    vram: int           # GB
    bus: int            # bit
    bandwidth: int      # GB/s
    dlss: bool
    p1080: str          # recommended profile (rule R5)
    p1440: str
    survey: Optional[float] = None   # share in the Steam survey's "All video cards" table, if listed there
    notes: list = field(default_factory=list)

    @property
    def short_name(self):
        return self.name.replace(VENDORS[self.vendor] + " ", "")


CARDS = [
    Card("gtx-1050-ti", "NVIDIA GeForce GTX 1050 Ti", "nvidia", "Pascal", 4, 128, 112, False, "low", "ultra-low",
         notes=["Often paired with older 4-core CPUs. If GPU usage stays well below 95% (Task Manager → Performance → GPU), "
                "you're CPU-bound: drop to `ultra-low` for its shorter LOD/tree distances rather than lowering resolution.",
                "At 1440p, try a lower render scale: press F1 in Rust, type `graphics.renderscale 0.75`, press Enter."]),
    Card("gtx-1060-3gb", "NVIDIA GeForce GTX 1060 3GB", "nvidia", "Pascal", 3, 192, 192, False, "low", "ultra-low",
         notes=["Not just less VRAM: the 3 GB model also has fewer CUDA cores (1152 vs 1280) than the 6 GB model.",
                "3 GB is the main limit. Keep half-resolution textures (R1) even on `balanced`."]),
    Card("gtx-1060-6gb", "NVIDIA GeForce GTX 1060 6GB", "nvidia", "Pascal", 6, 192, 192, False, "low", "ultra-low",
         notes=["6 GB is enough for full-resolution textures at 1080p (R1). If you see stutter when turning quickly "
                "in towns, try `graphicssettings.globaltexturemipmaplimit 1` and compare.",
                "Pascal has no tensor cores: no DLSS."]),
    Card("gtx-1650", "NVIDIA GeForce GTX 1650", "nvidia", "Turing (TU117)", 4, 128, 128, False, "low", "ultra-low",
         survey=2.19,
         notes=["Sold with GDDR5 (128 GB/s) and GDDR6 (192 GB/s) memory. Same overlay for both; the GDDR6 version is somewhat faster.",
                "Turing, but **no tensor cores**: DLSS is not available on GTX 16-series cards."]),
    Card("gtx-1660-super", "NVIDIA GeForce GTX 1660 Super", "nvidia", "Turing (TU116)", 6, 192, 336, False, "low", "low",
         notes=["Strong for its tier thanks to GDDR6 bandwidth. If `low` holds well above your target FPS, try `balanced` at 1080p.",
                "No tensor cores: no DLSS."]),
    Card("rtx-2060", "NVIDIA GeForce RTX 2060", "nvidia", "Turing (TU106)", 6, 192, 336, True, "balanced", "low",
         notes=["A 12 GB variant also exists. R1 gives full-res textures for both.",
                "First-generation RTX: DLSS works. At 1440p, DLSS *Quality* can make `balanced` viable."]),
    Card("rtx-3050", "NVIDIA GeForce RTX 3050", "nvidia", "Ampere (GA106/GA107)", 8, 128, 224, True, "low", "low",
         survey=2.90,
         notes=["Desktop 8 GB version. A slower 6 GB desktop variant exists (still full-res textures under R1).",
                "**Laptop** RTX 3050 cards often have only 4 GB: set `graphicssettings.globaltexturemipmaplimit 1` yourself.",
                "Use DLSS at 1440p."]),
    Card("rtx-3060", "NVIDIA GeForce RTX 3060", "nvidia", "Ampere (GA106)", 12, 192, 360, True, "balanced", "balanced",
         survey=3.66,
         notes=["12 GB is plenty for full-res textures even on lower profiles (R1).",
                "An 8 GB / 128-bit variant exists and is noticeably slower. If you have it, prefer `low` at 1440p.",
                "At 1440p, pair `balanced` with DLSS *Quality*."]),
    Card("rtx-4060", "NVIDIA GeForce RTX 4060", "nvidia", "Ada Lovelace (AD107)", 8, 128, 272, True, "balanced", "balanced",
         survey=3.89,
         notes=["Narrow 128-bit bus, partly offset by a large L2 cache.",
                "At this tier Rust is frequently CPU-bound at 1080p: if GPU usage is below ~90%, raising settings costs little FPS."]),
    Card("rtx-5060", "NVIDIA GeForce RTX 5060", "nvidia", "Blackwell (GB206)", 8, 128, 448, True, "balanced", "balanced",
         survey=4.40,
         notes=["GDDR7 gives much more bandwidth than older 8 GB cards on the same 128-bit bus.",
                "Likely CPU-bound at 1080p on most systems. Check GPU usage before lowering settings."]),
    Card("rtx-5060-ti", "NVIDIA GeForce RTX 5060 Ti", "nvidia", "Blackwell (GB206)", 8, 128, 448, True, "quality", "balanced",
         survey=4.06,
         notes=["Sold with 8 GB and 16 GB. Same overlay for both: full-res textures either way (R1)."]),
    Card("rtx-5070", "NVIDIA GeForce RTX 5070", "nvidia", "Blackwell (GB205)", 12, 192, 672, True, "quality", "quality",
         survey=6.15,
         notes=["The most common card on Steam right now.",
                "Rust will almost always be CPU-bound on this card at 1080p. FPS then depends on your CPU, not these settings.",
                "Reflex **On + Boost** (in Options → Graphics) keeps GPU clocks up when CPU-bound. NVIDIA notes it "
                f"\"can mean higher power usage or a slight reduction in FPS\" [[N3]]({SRC}#n3), so test it."]),
    Card("rx-580-4gb", "AMD Radeon RX 580 4GB", "amd", "Polaris", 4, 256, 224, False, "low", "ultra-low",
         notes=["Same GPU as the 8 GB model, but reference 4 GB boards also use slower 7 Gbps memory (224 vs 256 GB/s). "
                "Textures stay at half resolution (R1).",
                "Use Radeon Anti-Lag in the Adrenalin driver (no Reflex on AMD)."]),
    Card("rx-580-8gb", "AMD Radeon RX 580 8GB", "amd", "Polaris", 8, 256, 256, False, "low", "ultra-low",
         notes=["8 GB is a lot for a card of this speed: textures are free to max out (R1), but other settings are not.",
                "Use Radeon Anti-Lag in the Adrenalin driver for lower latency (no Reflex on AMD)."]),
    Card("rx-6600", "AMD Radeon RX 6600", "amd", "RDNA 2 (Navi 23)", 8, 128, 224, False, "balanced", "low",
         notes=["32 MB Infinity Cache offsets the narrow bus at 1080p; the advantage shrinks at 1440p.",
                "Rust has no FSR convar, so in-game upscaling is limited to `graphics.renderscale`. "
                "Radeon Super Resolution in the driver is an alternative."]),
    Card("rx-9070-xt", "AMD Radeon RX 9070 XT", "amd", "RDNA 4 (Navi 48)", 16, 256, 645, False, "quality", "quality",
         survey=1.42,
         notes=["The most common AMD discrete card in the Steam survey.",
                "Rust has no FSR convar, so FSR 4 can't be used in-game.",
                "Almost always CPU-bound at 1080p."]),
]

MIP_TEXT = {0: "full resolution", 1: "half resolution", 2: "quarter resolution"}


def validate():
    errors, seen = [], set()
    for c in CARDS:
        if c.slug in seen:
            errors.append(f"duplicate slug: {c.slug}")
        seen.add(c.slug)
        if c.vendor not in VENDORS:
            errors.append(f"{c.slug}: unknown vendor {c.vendor!r}")
        for p in (c.p1080, c.p1440):
            if p not in PROFILES:
                errors.append(f"{c.slug}: unknown profile {p!r}")
    if errors:
        sys.exit("\n".join(errors))


def mip_for(vram):
    return 2 if vram <= 2 else 1 if vram <= 4 else 0


def overlay(c):
    lines = [f'graphics.reflexmode "{1 if c.vendor == "nvidia" else 0}"']
    if not c.dlss:
        lines += ['graphics.dlss "-1"', 'graphics.dlaa "False"']
    lines += [f'graphicssettings.globaltexturemipmaplimit "{mip_for(c.vram)}"', 'graphics.af "16"']
    return "\n".join(lines) + "\n"


def page(c):
    mip = mip_for(c.vram)
    nvidia = c.vendor == "nvidia"
    rows = [("`graphics.reflexmode`", "1" if nvidia else "0",
             "R2: NVIDIA Reflex lowers input latency (GTX 900 series and newer)." if nvidia
             else "R2: Reflex is NVIDIA-only. Use Radeon Anti-Lag in the driver instead.",
             f"[N1]({SRC}#n1), [N3]({SRC}#n3)")]
    if not c.dlss:
        rows.append(("`graphics.dlss` / `graphics.dlaa`", "-1 / False",
                     "R3: this card has no tensor cores, so DLSS and DLAA are forced off.", f"[N2]({SRC}#n2)"))
    rows.append(("`graphicssettings.globaltexturemipmaplimit`", str(mip),
                 f"R1: {c.vram} GB VRAM → {MIP_TEXT[mip]} textures. Overrides the profile value.", f"[U1]({SRC}#u1)"))
    rows.append(("`graphics.af`", "16", "R4: anisotropic filtering is cheap on a discrete card's memory bandwidth.",
                 "reasoning"))

    md = [f"# {c.name}", ""]
    if c.survey:
        md += [f"{c.survey:.2f}% of Steam users ({SURVEY_MONTH} Steam Hardware Survey [[H1]]({SRC}#h1)).", ""]
    md += [
        f"**Config file:** [`{c.slug}.cfg`]({c.slug}.cfg)", "",
        "## Specs", "",
        "| | |", "|---|---|",
        f"| Architecture | {c.arch} |",
        f"| VRAM | {c.vram} GB |",
        f"| Memory bus | {c.bus}-bit |",
        f"| Bandwidth | ~{c.bandwidth} GB/s |",
        f"| NVIDIA Reflex | {'Yes' if nvidia else 'No'} |",
        f"| DLSS | {'Yes' if c.dlss else 'No'} |",
        "", f"Source: TechPowerUp GPU database [[H2]]({SRC}#h2).", "",
        "## Recommended setup", "",
        "Easiest: double-click **`install.bat`** in the repo folder and pick **Install**. It detects this card and "
        "suggests the profile below. Or run the command for your resolution from the repo folder:", "",
        "| Resolution | Profile | Command |", "|---|---|---|",
        f"| 1080p | [`{c.p1080}`](../../profiles/{c.p1080}.cfg) | `{APPLY.format(preset=c.p1080, slug=c.slug)}` |",
        f"| 1440p | [`{c.p1440}`](../../profiles/{c.p1440}.cfg) | `{APPLY.format(preset=c.p1440, slug=c.slug)}` |",
        "",
        "Profile choice is an **estimate** from this card's performance tier (rule R5). It hasn't been "
        "benchmarked yet. If you're on this card, a [benchmark report](../../benchmarks/README.md) is the most "
        "useful thing you can contribute.", "",
    ]
    if c.dlss:
        md += ["**DLSS:** set it in **Options → Graphics** (not in the overlay, because the convar's value mapping is "
               "unverified). DLSS helps when you're GPU-bound. At 1080p use *Quality* at most; at 1440p *Quality* or "
               "*Balanced*. DLAA looks better but was over 10% slower than TSSAA in a third-party test "
               f"[[C2]]({SRC}#c2).", ""]
    md += [
        "## What this overlay sets, and why", "",
        "| Convar | Value | Why | Src |", "|---|---|---|---|",
        *[f"| {a} | {b} | {w} | {s} |" for a, b, w, s in rows],
        "",
        "Rules R1–R5 are explained in [the card overlay README](README.md#what-a-card-overlay-changes-and-the-rules-behind-it).",
        "", "## Card-specific notes", "",
        *[f"- {n}" for n in c.notes],
        "", "## Benchmark status", "", "No reports yet.", "",
    ]
    return "\n".join(md)


def profile_link(p):
    return f"[`{p}`](profiles/{p}.cfg)"


def cards_readme_rows():
    return "\n".join(
        f"| [{c.name}]({c.slug}.md) | {c.vram} GB | `{c.slug}` | `{c.p1080}` | `{c.p1440}` |" for c in CARDS)


def main_readme_block():
    out = []
    for vendor, title in VENDORS.items():
        out += [f"#### {title}", "", "| Card | VRAM | 1080p | 1440p | |", "|---|---|---|---|---|"]
        out += [f"| [**{c.short_name}**](gpu/cards/{c.slug}.cfg) | {c.vram} GB | {profile_link(c.p1080)} "
                f"| {profile_link(c.p1440)} | [Why?](gpu/cards/{c.slug}.md) |"
                for c in CARDS if c.vendor == vendor]
        out.append("")
    return "\n".join(out).rstrip()


def with_block(text, name, body, path):
    start, end = f"<!-- {name}:start -->", f"<!-- {name}:end -->"
    if start not in text or end not in text:
        sys.exit(f"{path}: missing {start} / {end} markers")
    return text[:text.index(start)] + f"{start}\n{body}\n{end}" + text[text.index(end) + len(end):]


def expected_files():
    files = {}
    for c in CARDS:
        files[OUT / f"{c.slug}.cfg"] = overlay(c)
        files[OUT / f"{c.slug}.md"] = page(c)
    for path, name, body in [(OUT / "README.md", "cards", cards_readme_rows()),
                             (ROOT / "README.md", "readme-cards", main_readme_block())]:
        files[path] = with_block(path.read_text(encoding="utf-8"), name, body, path)
    return files


def main():
    validate()
    files = expected_files()
    known = {f"{c.slug}.{ext}" for c in CARDS for ext in ("cfg", "md")} | {"README.md"}
    orphans = [p for p in OUT.iterdir() if p.name not in known]

    if "--check" in sys.argv:
        problems = [f"out of date: {p.relative_to(ROOT)}" for p, text in files.items()
                    if not p.exists() or p.read_text(encoding="utf-8") != text]
        problems += [f"orphan (not in CARDS): {p.relative_to(ROOT)}" for p in orphans]
        if problems:
            sys.exit("\n".join(problems) + "\nRun: python tools/gen_cards.py")
        print(f"OK: {len(CARDS)} cards up to date")
        return

    for path, text in files.items():
        path.write_text(text, encoding="utf-8", newline="\n")
    for p in orphans:
        p.unlink()
        print(f"removed orphan {p.relative_to(ROOT)}")
    print(f"Generated {len(CARDS)} cards")


if __name__ == "__main__":
    main()
