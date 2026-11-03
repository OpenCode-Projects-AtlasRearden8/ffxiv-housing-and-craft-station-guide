# FFXIV Housing for Non-Crafters

A friendly, fan-made manual for housing in FINAL FANTASY XIV, written for
players who never plan to craft: buy-in budgets, what furniture actually
matters, garden planter math, crop-swap etiquette with neighbours, dyeing and
glamour through housing plaques, repair timer logs, move-in checklists you can
print, and server-transfer rebuild planning.

A project by **Asdale Dynamics, LLC**.

## What's here

```
docs/    Markdown source of the manual (9 pages, friendly wiki tone)
site/    Generated static HTML (open site/index.html in any browser)
build.py Local build script: docs/*.md -> site/*.html
tests/   Link, anchor, integrity, and build-determinism tests
```

## How to run it

Requirements: Python 3.8+ with the `markdown` package (`pip install markdown`).

```bash
python3 build.py            # regenerate site/ from docs/
python3 tests/test_links.py # verify links, anchors, and build determinism
```

Or just open `site/index.html` directly — the site is fully static, needs no
server, and works from the local filesystem.

## Why you can trust it with your data

You can't give it any, because it never asks.

- No account data, logins, or forms of any kind — nothing to leak.
- No analytics, no tracking scripts, no cookies, no `<script>` tags at all.
- No advertising, ever.
- Everything is local files. Delete the folder and it's gone, cleanly.

## Honest disclaimers

- **Fan-made and unofficial.** FINAL FANTASY XIV is a trademark of Square Enix
  Holdings Co., Ltd. This project and Asdale Dynamics, LLC are not affiliated
  with, endorsed by, or sponsored by Square Enix.
- **Numbers hedge on purpose.** Gil prices, bed counts, and menu names change
  between patches. Where we're unsure, we say so, and the in-game values are
  always the source of truth.
- **Not financial or gardening advice.** Well, the gardening part stands.

## License

MIT — see [`LICENSE`](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.
