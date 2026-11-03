#!/usr/bin/env python3
"""Local link and integrity tests for the FFXIV Housing for Non-Crafters site.

Run:  python3 tests/test_links.py

Uses only the standard library. Tests, in order:

  1. every docs/*.md page has a rendered site/<name>.html counterpart
  2. markdown sources are sane (H1 present, code fences balanced, non-empty)
  3. every relative link inside generated HTML resolves to a local file
  4. every in-page anchor (file.html#fragment) points at a real id
  5. every page links to every other page (full cross-navigation)
  6. the stylesheet exists and is referenced by every page
  7. generated pages carry the disclaimer footer and carry no scripts/trackers
  8. no stray non-ASCII garbage characters in docs or site output
  9. rebuilding is deterministic (same bytes, every time)
"""

import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITE = ROOT / "site"
BUILD = ROOT / "build.py"

failures: list[str] = []
passed: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    if ok:
        passed.append(name)
        print(f"  PASS  {name}")
    else:
        failures.append(f"{name}{': ' + detail if detail else ''}")
        print(f"  FAIL  {name}{': ' + detail if detail else ''}")


class LinkParser(HTMLParser):
    """"Collect href/src attributes and element ids from an HTML page."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.hrefs: list[str] = []
        self.srcs: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ANN001
        d = dict(attrs)
        if "href" in d:
            self.hrefs.append(d["href"])
        if "src" in d:
            self.srcs.append(d["src"])
        if "id" in d:
            self.ids.add(d["id"])


def parse_page(path: Path) -> LinkParser:
    p = LinkParser()
    p.feed(path.read_text(encoding="utf-8"))
    return p


def relative_resolve(from_html: Path, href: str) -> Path:
    base = from_html.parent / href.split("#", 1)[0]
    return base.resolve()


def main() -> int:
    md_files = sorted(DOCS.glob("*.md"))
    html_files = sorted(SITE.glob("*.html"))

    mds = {p.stem: p for p in md_files}
    htmls = {p.stem: p for p in html_files}

    print("[1] Rendered counterparts")
    check("every markdown page has a rendered .html",
          mds.keys() == htmls.keys(),
          f"docs={sorted(mds.keys())} site={sorted(htmls.keys())}")

    print("[2] Markdown sanity")
    for src in md_files:
        text = src.read_text(encoding="utf-8")
        check(f"{src.name}: non-empty", len(text) > 200)
        check(f"{src.name}: has an H1", text.lstrip().startswith("# "))
        fences = len(re.findall(r"^```", text, flags=re.M))
        check(f"{src.name}: code fences balanced", fences % 2 == 0,
              f"found {fences} fence lines")

    print("[3/4] Link and anchor resolution")
    all_ok = True
    details: list[str] = []
    for page in html_files:
        p = parse_page(page)
        for href in p.hrefs:
            if href.startswith(("http://", "https://", "mailto:")):
                details.append(f"{page.name}: unexpected external link {href}")
                all_ok = False
                continue
            if href.startswith("#"):
                frag = href[1:]
                if frag not in p.ids:
                    details.append(f"{page.name}: dead local fragment {href}")
                    all_ok = False
                continue
            target = relative_resolve(page, href)
            if not target.exists():
                details.append(f"{page.name}: missing target {href}")
                all_ok = False
                continue
            if "#" in href:
                frag = href.split("#", 1)[1]
                tp = parse_page(target)
                if frag not in tp.ids:
                    details.append(f"{page.name}: dead anchor {href}")
                    all_ok = False
        for src_attr in p.srcs:
            if src_attr.startswith(("http://", "https://")):
                details.append(f"{page.name}: external asset {src_attr}")
                all_ok = False
                continue
            if not relative_resolve(page, src_attr).exists():
                details.append(f"{page.name}: missing asset {src_attr}")
                all_ok = False
    check("all relative links/assets resolve, no external links", all_ok,
          "; ".join(details[:8]) or "clean")

    print("[5] Cross-navigation")
    nav_ok = True
    for page in html_files:
        text = page.read_text(encoding="utf-8")
        for other in html_files:
            if other.name not in text:
                nav_ok = False
                check(f"{page.name} links to {other.name}", False)
    if nav_ok:
        check("every page links to every other page", True)

    print("[6] Stylesheet")
    css = SITE / "assets" / "style.css"
    check("site/assets/style.css exists", css.exists())
    for page in html_files:
        if 'href="assets/style.css"' not in page.read_text(encoding="utf-8"):
            check(f"{page.name} references stylesheet", False)
            break
    else:
        check("every page references the stylesheet", True)

    print("[7] Disclaimer / no-scripts")
    disclaimer_key = "not affiliated with"
    for page in html_files:
        text = page.read_text(encoding="utf-8").lower()
        if disclaimer_key not in text:
            check(f"{page.name} carries disclaimer", False)
            break
        if "<script" in text:
            check(f"{page.name} script-free", False)
            break
    else:
        check("every page carries the fan-made disclaimer", True)
        check("no <script> tags anywhere", True)

    print("[8] Character hygiene")
    # Allow typical typographic punctuation; flag CJK, Cyrillic, Arabic, etc.
    allowed_extra = "—–’‘“”…×≈°§−→"
    def suspicious(text: str) -> list[str]:
        out = []
        for ch in text:
            o = ord(ch)
            if o > 127 and ch not in allowed_extra:
                out.append(ch)
        return out
    garbage = []
    for p in list(md_files) + list(html_files) + [css]:
        s = suspicious(p.read_text(encoding="utf-8"))
        if s:
            garbage.append(f"{p.name}: {s[:4]}")
    check("no stray script/foreign characters", not garbage, "; ".join(garbage))

    print("[9] Build determinism")
    def snap() -> dict:
        hashes = {}
        for p in sorted(SITE.rglob("*")):
            if p.is_file():
                hashes[str(p.relative_to(SITE))] = p.read_bytes()
        return hashes
    before = snap()
    proc = subprocess.run([sys.executable, str(BUILD)],
                          cwd=ROOT, capture_output=True, text=True)
    check("build.py re-runs cleanly", proc.returncode == 0,
          proc.stderr.strip()[:200])
    check("rebuild is byte-identical (deterministic)", snap() == before)

    print()
    print(f"{len(passed)} passed, {len(failures)} failed")
    if failures:
        print("Failures:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("ALL TESTS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
