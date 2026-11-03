# STATUS — FFXIV Housing and Craft-Station Guide

Last updated: 2026-11-03

## What was built

A complete, fan-made, offline-capable manual: *FFXIV Housing for Non-Crafters*,
published as a local-first static site by Asdale Dynamics, LLC.

**Content (docs/, 9 markdown pages, friendly wiki tone, heavily hedged):**

- `index.md` — index, reading order, and the project disclaimer (fan-made,
  zero account data, no ads, no tracking)
- `01-buy-in-budget-breakdown.md` — apartments vs houses, permits, fixtures,
  the real total cost of getting inside, cheapest-entry checklist
- `02-essential-furniture-vs-clutter.md` — starter kit vs anti-essentials,
  where non-crafters buy each item type
- `03-garden-planter-math.md` — garden lifecycle, indoor planters, a grow-your-
  own economics calculator (`N` beds) with a worked 8-bed example
- `04-crop-swap-etiquette-with-neighbours.md` — the gardener's compact, how a
  crop swap works, FAQ, a paste-able FC swap charter, conflict handling
- `05-dye-and-glamour-through-housing-plaques.md` — dyes end-to-end, plaques
  and signs, mannequins, glamour dressers, colour-story method
- `06-repair-timer-logs.md` — how NPC repairs work without crafting skills,
  printable repair log block, weekly totals, how to read your own log
- `07-move-in-checklist-printables.md` — three printable checklists
  (same-night move-in, tidy-up weekend, guest-visit pass), plain-text by design
- `08-server-transfer-rebuild-planning.md` — risk buckets, gil pocket plan,
  furniture packing plan, garden salvage, a T-3-weeks-to-T+1-month timeline

**Site (site/) and build (build.py):

- `build.py` renders every `docs/*.md` into templated HTML (`site/*.html`)
  using python-markdown only, adds a shared stylesheet, sidebar navigation,
  deterministic heading ids, and a full disclaimer footer on every page.
- Zero `<script>` tags, zero external requests, zero advertising, zero forms.

**Tests (tests/test_links.py):

- 37 assertions covering: every markdown page has a rendered counterpart;
  markdown sanity (H1 present, code fences balanced); every relative link and
  asset resolves; every `page.html#anchor` points at a real id; every page
  cross-links every other page; stylesheet present and referenced; disclaimer
  on every page; no `<script>` tags; no stray foreign characters; and a
  byte-identical rebuild (determinism).
- Verified the suite catches real breakage: a deliberately corrupted anchor
  made the run fail (2 failed assertions), and restoring the file made the
  suite pass again (37/37).

## How to run it

Requires Python 3.8+ and the `markdown` package (`pip install markdown`).

```bash
python3 build.py             # rebuild site/ from docs/
python3 tests/test_links.py  # run the verification suite (expects exit 0)
```

Or simply open `site/index.html` in a browser — fully static, works from the
local filesystem, no server needed.

## Verification results (this folder, 2026-11-03)

- `python3 build.py` — exit 0, renders 9 pages + `site/assets/style.css`.
- `python3 tests/test_links.py` — **37 passed, 0 failed; ALL TESTS PASSED**,
  including deterministic-rebuild check.
- Negative test anchor-corruption scenario — suite correctly failed, then
  passed again after restoration.
- LICENSE contains the exact line `Copyright (c) 2026 Asdale Dynamics, LLC`.
- README credits Asdale Dynamics, LLC (project authorship) and MIT license.
- Scanned docs/ and site/ for stray generated/CJK/Cyrillic artefacts — clean.
- No secrets, API keys, or personal data in any file (checked by inspection
  and by the character-hygiene test); no network calls anywhere in the code.

## Known gaps / limitations

1. **In-game numbers are intentionally hedged.** Gil figures, garden bed
   counts, grow times, menu names, and transfer/gil-cap specifics vary by
   patch, region, and server. The manual flags every such figure as a hedge
   and defers to in-game values; neither page should be treated as a price
   sheet.
2. **"Housing plaques" is our plain-English umbrella** for the plot placard,
   message signs, and mannequin/glamour-display items a non-crafter actually
   uses; exact item and menu names drift between patches.
3. **No search or print stylesheet.** Pages are single-file plain text, but a
   dedicated print CSS and a client-free search index could be added later.
4. **English only**, British-leaning spelling; no localisations yet.
5. **Tests are structural** (links, anchors, determinism, hygiene); they do
   not check factual accuracy of game numbers — that needs in-game
   verification each patch.
6. **Not affiliated with Square Enix**; the disclaimer footer on every page
   and the README make this explicit.

## Git and publishing posture

Git repository initialised locally with a single plain commit. Nothing has
been pushed, no remote exists, and nothing was published: this project never
pushes, never creates remote repositories, and never publishes.
