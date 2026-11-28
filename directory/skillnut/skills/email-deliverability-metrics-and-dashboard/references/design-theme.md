# The Field Report theme (full implementation spec)

The dashboard should look like a beautifully printed field report, not a SaaS admin panel. The buyer opens it and it reads as something a design studio charged for. This file is the complete spec: tokens, type, components, motion, and the checks that keep it honest. Follow it as written; deviate only where the user pins their own brand.

## Tokens (define once as CSS custom properties)

| Role | Value | Notes |
|---|---|---|
| Page (paper) | `#f5f2ed` | cream, never white |
| Card | `#fbfaf6` | one step brighter than paper |
| Muted fill | `#eeeae1` | chart tracks, chips |
| Hairline | `#ddd8cd` | borders, gridlines |
| Strong line | `#c9c3b5` | section rules |
| Ink | `#161512` | headings, table values |
| Body | `#38352f` | running text |
| Muted text | `#6b665a` | dark enough for 4.5:1 on cream; lighter grays fail |
| Accent | `#df361b` | vermillion; the one signature color |
| Accent deep | `#c22a10` | accent as small text (contrast-safe) |
| Status good / warn / serious / critical | `#3f7a3f` / `#c99a2e` / `#d3711f` / `#df361b` | marks and fills only |
| Status text variants | `#2e662e` / `#8a6712` / `#9c520e` / `#c22a10` | small text on cream; bright versions fail contrast |
| Data pill | `#1b1b18` on `#f2efe6` text | black mono chips for counts |

Categorical marks (gateway charts) stay earthy, never neon: slate blue `#4f6d88`, olive `#5f7a3a`, gold `#c99a2e`, plum `#8a5a72`, gray-violet `#7a6f88`, with the hot statuses reserved for the hard gateways (Mimecast critical red, Proofpoint serious orange, Barracuda warning gold).

**Committed to light.** Set `color-scheme: light only` on `:root` and ship **no** dark-mode media query. The reference is a paper document; a dark-mode browser must still get cream. This is a deliberate commitment, not an omission.

**Where the accent goes** (and nowhere else): a 13px logo square before the title, section numerals, uppercase eyebrow labels, the 2px top-rule on stat cards, the callout left bar, the spine rail, links. If everything is red, nothing is.

## Type

Three voices, all self-hosted inside the file:

- **Display and UI:** a Helvetica-descended grotesque. Hanken Grotesk is the reference (variable weight 400 to 800, one woff2, about 35KB). Avoid the overused defaults (Inter, Roboto); they read as template.
- **Data:** a workmanlike mono for every numeral, table figure, stamp, and pill. IBM Plex Mono is the reference (400 and 600, about 30KB together). `font-variant-numeric: tabular-nums` on all tables.
- **Editorial accent:** Georgia italic (system font, no embed) for benchmark callouts. This serif voice is what makes the page read as a field guide instead of an app.

Sourcing and embedding: download the latin-subset woff2 files from Google Fonts once (request the CSS with a modern browser user-agent, take the `/* latin */` block's URL per weight; a variable font arrives as one file for all weights). Store in `assets/`, then embed at build time as `@font-face` with `src: url(data:font/woff2;base64,...)`. Total payload well under 100KB; the page then opens offline forever and never phones home.

Type detail: tight negative tracking on big numerals (around -0.03em), letter-spaced uppercase for eyebrows (10px, 0.12 to 0.15em, weight 700), section titles around 23px weight 800, body 15px, table text 12.5px. Fallback stack: `"Hanken Grotesk","Helvetica Neue",Helvetica,Arial,"Segoe UI",system-ui,sans-serif`.

## Signature components

**The spine rail is the page header.** A fixed vermillion bar down the left edge (about 128px wide; do not widen it) that carries the whole page identity, so no sticky top bar exists at all. From top: a 13px cream logo square; a **horizontal wordmark** (the report title at about 13px weight 800 cream, wrapping over up to three lines inside the rail width; a three-line lockup reads deliberately editorial, not cramped); the **"last refreshed" stamp** beneath it (about 7.5px mono uppercase cream); and at the bottom a mini table of contents: one row per section, a mono number (`!` for the action center, `01` to `09`, `i` for sources) beside a tiny uppercase label (about 7.5px, letter-spaced, cream at 85% opacity; short forms like "Sending Tool", "Burn Detection", with the full section title as a hover tooltip). Bare numbers alone fail here; users cannot tell what `04` is without the label. The rows act as scroll-spy navigation (IntersectionObserver toggles an inverted cream-on-red active state on the current row). `main` gets `margin-left` equal to the rail width. Two consequences to handle: hide the rail under about 1120px and in print, and because the rail is now the only place the title and stamp live, ship a minimal **non-sticky fallback header** (logo square + title + stamp) that shows only below that breakpoint and in print, or narrow screens and printouts lose all identity. CSS gotcha that bit once: the fallback's `display:block` media query must come after its `display:none` default in source order, or the default wins.

**The arc gauge** (health score). An SVG, about 220 by 190:

- a 240-degree arc from 210 degrees down to -30, radius about 86, stroke 10,
- track in muted fill, progress stroke colored by score band, drawn via `stroke-dasharray` = full arc length and `stroke-dashoffset` animated to `full - score fraction * full`,
- hairline ticks crossing the arc at the grade boundaries (40 / 55 / 70 / 85) and small mono grade letters (F D C B A) floated outside each band,
- the score numeral centered (weight 800, about 58px) with "Grade X · out of 100" beneath in the band's text color.

The grade ring is information, not decoration: the reader sees which band the score sits in and how far the next one is.

**The dot-matrix waffle** (gateway mix). A 10 by 10 CSS grid of 16px cells, 4px gap; **one cell = 1% of recipients**, allocated by largest-remainder rounding so the grid always sums to exactly 100. Cells colored by gateway in descending size order; the legend beside it carries the exact counts and percentages plus a "hard gateway" mono pill on Mimecast, Proofpoint, Barracuda. Caption: "One square = 1% of recipients."

**In-cell data bars.** Under key table numbers (domain share, bounce rate), a 3px hairline bar scaled to the column max, in the row's status color. Lets a column be compared without being read. Implementation: a relatively-positioned span wrapping the number with an absolutely-positioned 3px track and fill below the text; remember `display: block` on the fill.

**The compact table** (for the domain-health table and any table users will want in one view). Users dislike horizontal scrolling on the tables they read most; when a wide table matters, compress it to fit rather than letting it scroll. The moves, in order of value: drop the font a step (11px, headers 8.5px) and tighten cell padding (6px 8px); **merge columns that share a subject** (the TLD folds into the domain name as a colored suffix instead of its own column; inbox count and share become one "25 · 53%" cell over a single bar; registrar and DNS host share a cell as "NameSilo · Cloudflare"); shorten repeated long values with a mapping (registrar legal names to their short forms) and put the full value in a title tooltip; and keep the overflow wrapper as a safety net for narrow windows. A twelve-column table fits a laptop width this way with nothing lost, because every dropped pixel went into a tooltip.

**Blacklist cell states.** Three visible states, each with a per-list tooltip (Spamhaus DBL: clean, SURBL: clean): green "clean" only when every list returned a real not-listed answer, red "LISTED" when any list returned codes, amber "recheck" when any lookup was blocked or kept failing. A blacklist cell must never show clean because a query failed.

**The pass-through matrix** (in the gateways section, under the waffle). Rows = sending domains; columns = the gateways users care about (Mimecast, Proofpoint, plain Outlook, custom servers). Each cell leads with the **pass-evidence ratio** as a colored percentage (green 45%+, amber 20 to 45%, red under 20%, muted dash for no data), followed by the small evidence figures "landings · bounces" in 9.5px muted, with the genuine-vs-auto split as the hover tooltip. The card's "how to read this" note is not optional: it must state that the ratio is evidence, not measurement, name the two limits (no true denominator; the bounce-notice parse rate with its actual numbers), and flag small-sample rows. This is the one table where over-claiming would actively misroute the user's sending.

**Eyebrow-top stat tiles.** Red uppercase eyebrow label first, then the numeral (about 30px, weight 800), then one line of muted context; card with hairline border, 2px accent top-rule, 4px corner radius.

**Section headers.** Red mono numeral + bold title + a hairline bottom border with a short 44px accent underline overlapping it; the verdict chip floats right as a tinted uppercase pill.

**Benchmark callouts.** Georgia italic on the muted fill, a 3px accent left bar, bold ink for the key numbers. This is the page quoting its own field guide.

**Action cards.** A 4px severity bar at left; title with a tinted severity tag; then the Norm / Now chip pair (bordered chips, tiny uppercase mono keys, green benchmark value, ink current value); then the fix sentence; then affected entities in muted mono.

## Behavior and motion

**One authored moment: the data draws itself in.** On load, the score counts up (about 900ms, cubic ease-out, via requestAnimationFrame) while the gauge arc draws (CSS transition on stroke-dashoffset). As the reader scrolls, meter bars scale in from zero (`transform: scaleX`, transform-origin left, staggered) and waffle cells pop in (opacity + scale, 8ms incremental delays, capped at 800ms), each triggered once by an IntersectionObserver adding a `drawn` class. Nothing else moves except 150ms hover transitions.

Three gates keep it honest: all animation CSS sits behind `@media (prefers-reduced-motion: no-preference)` and the JS checks the same query, setting final states directly when reduced; initial hidden states apply only under a `.js` class the script adds, so the page is complete with JavaScript disabled; and everything renders finished when printed.

Structural rules: proper document skeleton (doctype, charset, viewport meta), wide tables scrolling inside their own wrapper, sticky table headers inside tall scrollable tables, row hover tints, `:focus-visible` rings on the rail links, and a print stylesheet (hide rail and topbar, white paper, avoid breaking cards across pages).

## Verifying the render

- Headless-screenshot the built page at a desktop width and look at it; the two classic silent failures are bars invisible because a fill span lacks `display: block`, and phone layout broken because the viewport meta is missing.
- Screenshot animation states with the browser's reduced-motion flag forced, so you verify the final state, not a mid-flight frame.
- Chrome on Windows will not open a window narrower than about 500px; verify narrow layouts by injecting a scrollWidth probe (document scrollWidth vs clientWidth, and any element whose right edge exceeds the viewport outside a scroll wrapper), not by trusting a 390px screenshot.
- Contrast: muted text and status text variants exist because the bright status hues fail 4.5:1 on cream; never put the bright versions on small text.
- Final scans from the build recipe: no key, no external URL, in either output file.
