#!/usr/bin/env python3
"""Build the FFXIV Housing for Non-Crafters static site.

Reads docs/*.md, renders each page with python-markdown, and writes
templated HTML into site/ alongside a generated assets/style.css.

Local-first: stdlib + the `markdown` package only. No network access,
no tracking scripts, no ads.

Usage:  python3 build.py
"""

import re
import shutil
import sys
from pathlib import Path

try:
    import markdown
except ImportError:  # pragma: no cover
    sys.exit("The 'markdown' package is required: pip install markdown")

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"

TITLE = "FFXIV Housing for Non-Crafters"
SUBTITLE = "A friendly fan-made manual"
FOOTER_DISCLAIMER = (
    "Fan-made and unofficial. FINAL FANTASY XIV is a trademark of Square Enix "
    "Holdings Co., Ltd. This site and its publisher, Asdale Dynamics, LLC, are "
    "not affiliated with, endorsed by, or sponsored by Square Enix. This site "
    "collects no account data, embeds no tracking or analytics, and contains "
    "no advertising. Content licensed MIT."
)

# Sidebar order matters: this is the reading order of the manual.
PAGES = [
    ("index.md", "index.html", "Index &amp; Disclaimer", "index", "Home"),
    ("01-buy-in-budget-breakdown.md", "01-buy-in-budget-breakdown.html",
     "Buy-In Budget Breakdown", "budget", "Page 1"),
    ("02-essential-furniture-vs-clutter.md", "02-essential-furniture-vs-clutter.html",
     "Essential Furniture vs Clutter", "furniture", "Page 2"),
    ("03-garden-planter-math.md", "03-garden-planter-math.html",
     "Garden Planter Math", "garden", "Page 3"),
    ("04-crop-swap-etiquette-with-neighbours.md",
     "04-crop-swap-etiquette-with-neighbours.html",
     "Crop-Swap Etiquette with Neighbours", "crops", "Page 4"),
    ("05-dye-and-glamour-through-housing-plaques.md",
     "05-dye-and-glamour-through-housing-plaques.html",
     "Dye &amp; Glamour Through Housing Plaques", "glamour", "Page 5"),
    ("06-repair-timer-logs.md", "06-repair-timer-logs.html",
     "Repair Timer Logs", "repair", "Page 6"),
    ("07-move-in-checklist-printables.md", "07-move-in-checklist-printables.html",
     "Move-In Checklist Printables", "checklist", "Page 7"),
    ("08-server-transfer-rebuild-planning.md",
     "08-server-transfer-rebuild-planning.html",
     "Server-Transfer Rebuild Planning", "transfer", "Page 8"),
]

MD_EXTENSIONS = ["tables", "fenced_code", "sane_lists", "toc"]


def slugify(text: str) -> str:
    """Deterministic heading ids (mirrors python-markdown's default closely
    enough that our own template and tests can rely on them)."""
    text = text.strip().lower()
    text = re.sub(r"['\"“”‘’()\[\],.#%~!*?<>|/\\:+&=-]+", "", text)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")


def heading_id(text: str, seen: dict) -> str:
    base = slugify(text) or "section"
    if base not in seen:
        seen[base] = 0
        return base
    seen[base] += 1
    return f"{base}-{seen[base]}"


def extract_h1(md_text: str) -> str:
    m = re.search(r"^#\s+(.+)$", md_text, flags=re.M)
    return m.group(1).strip() if m else TITLE


def nav_html(current_html: str) -> str:
    items = []
    for src, dst, label, href_key, kicker in PAGES:
        active = ' class="active"' if dst == current_html else ""
        items.append(f'<li{active}><a href="{dst}">{label}</a></li>')
    return "\n".join(items)


def build_page(md_src: Path, dst_name: str, current_html: str) -> None:
    md_text = md_src.read_text(encoding="utf-8")

    # Pre-assign deterministic heading ids so in-page anchors inside markdown
    # (e.g. "[...] (index.html#a-very-important-disclaimer)") resolve.
    seen: dict = {}
    lines = []
    for line in md_text.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            hid = heading_id(m.group(2), seen)
            lines.append(f'{m.group(1)} {m.group(2)} {{#{hid}}}')
        else:
            lines.append(line)
    md_text = "\n".join(lines) + "\n"

    body = markdown.markdown(
        md_text,
        extensions=MD_EXTENSIONS + ["attr_list"],
        extension_configs={"toc": {"slugify": lambda value, _: slugify(value)}},
    )

    page_title = extract_h1(md_text)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="description" content="{page_title} — {SUBTITLE}. No ads, no tracking, no account data.">
<title>{page_title} — {TITLE}</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="site-header">
  <p class="kicker">{SUBTITLE}</p>
  <h1 class="site-title"><a href="index.html">{TITLE}</a></h1>
  <p class="tagline">Fan-made, unofficial, ad-free. Runs entirely from local
  files. No account data is collected — ever.</p>
</header>
<div class="layout">
<nav aria-label="Manual pages">
  <h2 class="nav-title">Manual pages</h2>
  <ul class="nav-list">
{nav_html(current_html)}
  </ul>
</nav>
<main>
{body}
</main>
</div>
<footer class="site-footer">
  <p>{FOOTER_DISCLAIMER}</p>
</footer>
</body>
</html>
"""
    out = SITE / dst_name
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT)}")


STYLE = """/* Style for the FFXIV Housing for Non-Crafters manual. */
:root {
  --bg: #f6f3ec;
  --panel: #fffdf7;
  --ink: #2d312e;
  --accent: #6a8d5f;
  --accent-dark: #3f5a38;
  --line: #ddd6c6;
  --code-bg: #efeadb;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: Georgia, 'Times New Roman', serif;
  background: var(--bg);
  color: var(--ink);
  line-height: 1.65;
}
a { color: var(--accent-dark); }
a:hover { color: var(--accent); }
.site-header {
  background: var(--accent-dark);
  color: #fdfcf7;
  padding: 1.6rem 2rem 1.2rem;
}
.site-header .kicker {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.75rem;
  margin: 0;
  color: #cfe0c5;
}
.site-title { margin: 0.2rem 0; font-size: 1.7rem; }
.site-title a { color: #fdfcf7; text-decoration: none; }
.site-header .tagline { max-width: 60ch; margin: 0.4rem 0 0; font-size: 0.95rem; color: #e5efe0; }
.layout {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  max-width: 68rem;
  margin: 2rem auto;
  padding: 0 1.5rem;
}
nav { flex: 0 0 15rem; }
.nav-title {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--accent-dark);
  border-bottom: 1px solid var(--line);
  padding-bottom: 0.35rem;
}
.nav-list { list-style: none; margin: 0; padding: 0; font-size: 0.95rem; }
.nav-list li { margin: 0.45rem 0; }
.nav-list li.active > a { font-weight: bold; }
main { flex: 1 1 32rem; min-width: 0; }
main h1 { font-size: 1.55rem; border-bottom: 2px solid var(--accent); padding-bottom: 0.3rem; }
main h2 { font-size: 1.25rem; margin-top: 2rem; }
main h3 { font-size: 1.05rem; }
main table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: 0.95rem; }
main th, main td { border: 1px solid var(--line); padding: 0.45rem 0.6rem; text-align: left; }
main th { background: var(--code-bg); }
main pre {
  background: var(--code-bg);
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 1rem;
  overflow-x: auto;
  font-size: 0.85rem;
}
main code { background: var(--code-bg); padding: 0.1rem 0.3rem; border-radius: 3px; font-size: 0.9em; }
main pre code { background: none; padding: 0; }
main blockquote {
  margin: 1rem 0;
  padding: 0.5rem 1rem;
  border-left: 4px solid var(--accent);
  background: var(--panel);
  color: #4a5148;
}
footer.site-footer {
  max-width: 68rem;
  margin: 2rem auto 3rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--line);
  font-size: 0.85rem;
  color: #5a6157;
}
@media (max-width: 52rem) {
  nav { flex-basis: 100%; }
}
"""


def build_style() -> None:
    (SITE / "assets").mkdir(parents=True, exist_ok=True)
    (SITE / "assets" / "style.css").write_text(STYLE, encoding="utf-8")
    print("  wrote site/assets/style.css")


def clean_site() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True, exist_ok=True)


def main() -> int:
    print("Cleaning site/ ...")
    clean_site()
    print("Writing stylesheet ...")
    build_style()
    print("Rendering pages ...")
    for src_name, dst_name, _label, _key, _kicker in PAGES:
        src = DOCS / src_name
        if not src.exists():
            print(f"  ERROR: missing source {src}", file=sys.stderr)
            return 1
        build_page(src, dst_name, dst_name)
    print(f"Done: {len(PAGES)} pages rendered into site/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
