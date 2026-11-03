# Page 3 — Garden Planter Math

*A fan-made guide by Asdale Dynamics, LLC — unofficial, unaffiliated, ad-free,
no account requests, no trackers.*

Gardening is the part of housing that looks most like homework: beds, seeds,
watering, and charts. This page does the homework for you, with a calculator
you can rerun any time.

## 1. First, a very important hedge

We will say this once, in bold, and then stop:

**Bed counts, grow times, and watering rules depend on which patch you own and
on the current state of the game itself.** The math below uses a variable `N`
for the number of beds in your patch, and a worked example for a patch with
8 beds. Whatever your patch's real bed count is — read the item description in
game, or count the plantable spots yourself — the calculator still works. If a
mechanic has changed since this was written, the game wins.

## 2. The garden lifecycle (plain English)

For an outdoor patch in a housing yard:

1. **Buy a garden patch** (an outdoor furnishing) and place it in your yard.
2. **Buy seeds** from the Market Board or a vendor, or receive them from a
   neighbour (Page 4 is entirely about that social contract).
3. **Plant one seed per bed.**
4. **Water** — roughly once per real-world day. Other players can water your
   garden too (that's the etiquette economy of Page 4).
5. **Wait.** Grow times vary by crop; many common crops take a few days.
6. **Harvest.** You get the crop — and you may *also* get a new seed, thanks to
   **crossbreeding**, which happens when a seed is planted next to a different,
   compatible seed.

## 3. Indoor planters: the low-effort cousin

An indoor **planter** (a furnishing you place inside your home) lets you grow
one thing at a time, per planter.

- **What it's for:** a single seed at a time — usually flowers and simple
  projects. Check what your seed grows into before committing.
- **What it can't do:** crossbreeding. Crossbred seeds come from adjacent
  outdoor beds, not indoor pots.
- **Why non-crafters have one:** a pot of flowers on a windowsill costs little
  gil, takes little thought, and is the single cosiest item in the game.

## 4. The garden economics calculator

The whole question in one formula:

```
Cost of the project   = patch_price + (N × seed_price) + extras
Revenue from crops    = N × crop_value
Revenue from seeds    = new_seed_count × new_seed_value
Profit                = all revenue − all cost
```

Where:

- `N` = number of beds in your patch.
- `crop_value` = what one harvested crop sells for on the Market Board.
- `new_seed_count` = how many extra seeds crossbreeding produced. This is
  genuinely variable — gardeners rarely get the same count twice.

### Worked example — an 8-bed patch

Friendly placeholder numbers (the *method* matters more than the gil; your
server's Market Board will differ):

- Patch price: ~40,000 gil (one-time)
- Seed price: ~8,000 gil each → 8 beds need 8 seeds → 64,000 gil
- Crop value per bed at harvest (say, a few days later): ~18,000 gil

```
Cost   = 40,000 + (8 × 8,000) = 104,000 gil
Return = 8 × 18,000           = 144,000 gil
Profit from crops alone       =  40,000 gil
+ any crossbred seeds         = extra upside
```

Two harvests later you've paid off the patch and you're in real profit — and
that is *before* counting crossbred seeds, which is where gardens can print
real money on a server where a rare seed is in demand.

**The big caveat:** Market prices swing. If everybody on your server grew the
same crop last week, your 18k crop might sell for 6k. The classic protection is
Page 4's crop-swap circle: diversify by trading with neighbours who planted
differently.

## 5. Rules of thumb

- **Water every day.** Missed waterings slow crops down, and can annoy
  the neighbours who were counting on them (Page 4).
- **Don't fill a whole patch with one seed type** unless you're sure — a single
  seed type everywhere usually means no crossbreeding at all.
- **One seed per bed.** Beds don't share.
- **Stagger planting.** If you plant everything on the same day, you harvest
  everything on the same day, at the same Market price. Staggering by a day or
  two smooths your income.
- **Don't dismiss the "pretty" seeds.** Some rare crossbred flowers are worth a
  lot to glamour and decorating players; decoration can be a business.

## For tomorrow

Count your beds (`N`), price one seed, price one crop, and fill in the
calculator with your own real numbers. That's the whole homework.

---

Not affiliated with or endorsed by Square Enix. No account data collected, no
ads. Market numbers on this page are illustrative; your Market Board decides
the truth.

**Up:** [Index](index.html) — **Next:** [Crop-Swap Etiquette](04-crop-swap-etiquette-with-neighbours.html)
