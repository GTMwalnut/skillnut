# The account score (gates, fit, timing, probe, bands)

Load this with `signal-run-engine.md` section 5 whenever a run scores accounts, or when the user asks for a scoring model in the playbook (Part C). It replaces a single blended 0 to 100 number with a model a rep can audit line by line: gates first, then fit, then timing that decays, then an optional probe, then a band that says how fast to act.

The structure and mechanics below come from a real scoring workbook. The attributes and triggers are written so they fit any B2B seller: build the user's own rows with them, keep the mechanics.

---

## 1. The shape

`score (0 to 100) = Fit (max 60) + Timing and intent (max 25, decayed by age) + Probe (max 15)`

Order of work, always:

1. **Gates, reducers and reroutes** (section 2). A gate failure removes the account; it is never scored.
2. **Fit** (section 3): rate each attribute 0 to 4, times its ICP weight, times the sector weight.
3. **Timing** (section 4): each trigger's points, decayed by how far into its window it is.
4. **Probe** (section 5): only for accounts that passed the gates with fit of 35 or more.
5. **Band** (section 6): A to D, each with a response time.

Every scored account carries: the score, the band, the three subtotals, the gate and reducer notes, the triggers with their dates and source links, a 2 to 4 sentence rationale a rep can read, and the score version.

---

## 2. Gates, reducers and reroutes (run first)

| Type | What it does | Generic examples (replace with the user's own) |
|---|---|---|
| **Gate** | Removes the account. Not scored, logged with the reason | No presence in the market you serve (for example no team in your selling country). A business model you cannot serve (consumer, local only). A prerequisite system you need is missing (for example no CRM when your product runs on one). A written policy that blocks what you do and will not change. Layoffs or a hiring freeze in the buying function in the last 90 days (revisit after 120). Constraints that stop them carrying out the fix. A multi-year contract with a competitor in force (locked out until renewal). Too large for your capacity, or procurement terms you cannot meet yet (minimum deal size, security certifications, single sign-on, data agreements) |
| **Reducer** | Lowers the score (typically 2 to 5 points), keeps the account | A competitor's tool signed within the last 6 months (minus 5; set a renewal reminder at month 10). A secondary prerequisite missing (minus 3). Self-serve buying with a very small deal size (minus 4). A private-equity buyout within 12 months with a cost programme (minus 3). Low exposure to the pain you fix (minus 2). Stale assets that suggest a different offer fits better (minus 2, and flag it) |
| **Reroute** | Moves the account to another ICP and scores it there | Too big for this ICP (later funding stage, more employees): move up. Too small: move down. A team already in place that this ICP assumes is absent: move to the ICP that expects it |
| **Seller-side cap** | Caps the band, does not remove | A requirement on your side not met yet (for example a certification larger buyers ask for): cap at C until it is in progress, unless a founder relationship exists |

Negative triggers (section 4) also work like a timed gate: a layoff or hiring freeze in the buying function takes the account out for 90 days.

---

## 3. Fit (max 60)

**Rate every attribute 0 to 4:** 4 Ideal, 3 Good, 2 Acceptable, 1 Poor, 0 Absent. `points = weight x rating / 4`.

**Missing data** is scored as rating 2 (half weight) and caps the account at band B until it is verified. That stops thin records from looking perfect and stops them from being thrown away.

**Fit attributes (generalised; each ICP gets its own weights):**

| Attribute | What Ideal looks like | Example weight (illustrative) |
|---|---|---|
| Size band (employees, or a revenue proxy) | Inside the ICP's sweet-spot band; edge of band rates 2; outside 0 | 6 |
| Funding stage, recency and ownership | The stage that buys most, funded inside the peak window (for example 60 to 270 days ago; 0 to 59 days: queue, do not pitch yet) | 8 |
| Considered purchase | Their own sales motion is sales-led with a deal size that makes your product worth it | 8 |
| Buying-team fit | The function you sell to exists and has the owner you need (or, for an ICP defined by its absence, the function is missing and the founder is visible) | 12 |
| Prerequisite stack | The systems your product needs are all present; only the core one rates 2 | 8 |
| Relevant operating assets | The things your product works on exist at the right scale (content, data, sites, fleet, catalogue: whatever applies to the user's offer) | 8 |
| Market position and competitiveness | A crowded category where they are a challenger or a leader under attack | 5 |
| Growth and health | Growing and hiring; layoffs rate 0 | 3 |
| Business model and offer breadth | Pure B2B in the market you serve | 2 |
| Existing competitor-tool adjustment | Enter plus 1 for none, 0 for a free or low-cost tool, minus 1 for a paid tool signed within 6 months (multiplied by its weight, so it can subtract) | 5 |

**Write each attribute as a spec row** so anyone can rate it the same way: ID, attribute, Ideal (4), Good (3), Acceptable (2), Poor (1), Disqualify, weight, data source, how to observe (the exact filter or check). A "Poor" that means "belongs in another ICP" is written as a reroute, not a low score.

**Sector weight.** Rank the sectors inside each ICP: Tier 1 (attack first) 0.9 to 1.0, Tier 2 0.7 to 0.8, Tier 3 (opportunistic) 0.5 to 0.6, Avoid 0. Write why each sector qualifies and the exact industry filter for the list tool.

`Fit = min(60, max(0, sum of attribute points x sector weight))`. The weights may add up to a little more than 60, so an account in a top sector can reach the cap and one in a weaker sector cannot.

---

## 4. Timing and intent (max 25, decayed by age)

Each trigger has points per ICP and a window in days. Detect weekly.

**Decay rule:** full points in the first third of the window, 50% in the second third, 25% in the final third, zero after. Sum every trigger, then cap the total at 25 (and floor it at minus 10, so a negative trigger can pull an account down).

Spreadsheet formula per trigger row (days since in column F, window in E, points from the ICP column):

`=IF(F="",0,IF(F>E,0,points*IF(F<=E/3,1,IF(F<=2*E/3,0.5,0.25))))`

**Trigger list (generalised; set the points and windows with the user):**

| Trigger | Example points | Window (days) | Notes |
|---|---|---|---|
| First-party hand-raise: pricing page visit, trial or free-tool use | 12 | 14 | The strongest signal in the model |
| New leader hired in the buying function | 10 | 120 | Peak around days 30 to 90 |
| Job post names your category or the problem | 8 | 60 | Explicit in-market signal |
| Funding round closed | 8 | 270 | |
| Leadership or board asked about the problem | 8 | 60 | Only scored when heard directly (a call, the founder's own post) |
| Your probe finds a live, visible problem | 8 | 30 | Re-run the probe within 72 hours before sending |
| The persona posts publicly about the problem | 8 | 30 | Reply in the thread; do not cold email off a post |
| Measurable decline in the metric you improve | 7 | 90 | Confirm it is real, not a tracking change |
| New hire or open role for the hands-on owner | 7 | 90 | A new owner needs tools |
| They publish their own content about the problem | 6 | 60 | Already convinced |
| Rebrand, repositioning or domain change | 6 | 120 | |
| Replatform or a major system change | 6 | 90 | A risk window |
| Demotion or exclusion in an analyst or review ranking | 4 to 6 | 90 | Heavier for larger accounts |
| Bought intent data on your category | 6 | 30 | Only if the user buys it |
| A competitor of theirs raises, launches or is acquired | 5 | 45 | Creates comparison pressure |
| Their category is redefined | 5 | 90 | |
| New product or segment launch | 5 | 60 | |
| An incumbent vendor or agency contract ending | 5 | 60 | Budget is moving |
| Renewal window of an adjacent tool | 4 | 90 | Budget reallocation moment |
| Persona speaks at an event or appears in a community | 4 | 45 | Warm hook |
| Subscribed to your newsletter or attended your webinar | 4 | 60 | |
| Award or growth-list listing | 1 to 5 | 120 | Heavier for small companies (revenue proof and a congratulations hook) |
| Layoffs or a hiring freeze in the buying function | minus 10 | 90 | Negative: out for 90 days |

The run engine's research pass (signal-run-engine section 5) is how most of these get found; every trigger row carries its date and source link.

---

## 5. The probe (max 15, optional)

A probe is a short, repeatable check your team runs on the account **before** outreach that shows the gap your product closes. The result both scores the account and opens the email. Depending on the offer it might be a test of their site, a public-record lookup, a benchmark against peers, or asking the questions their buyers ask in the places buyers ask them and recording who comes up.

**Probe spec:** a fixed set of checks per account, mixed by type (mostly buying-moment checks, a couple of comparisons, a couple of early-research checks, one accuracy check), run in two or three places. Run it only on accounts that passed the gates with fit of 35 or more, because it costs time or money per account.

**Score the most severe pattern found, add 1 if it repeats in 2 or more places, cap at 15:**

| Pattern | Points | Outreach use |
|---|---|---|
| P1 A competitor is chosen and the prospect is absent on most buying-moment checks | 15 | Lead with the competitor being picked where they should be |
| P2 The prospect shows up with wrong facts (price, features, "discontinued", wrong category) | 13 | Lead with the wrong claim, with the evidence, not with your product |
| P3 Present in early research, absent at the buying moment | 11 | Show both results side by side |
| P4 Their own assets do the work but someone else gets the credit | 11 | Strongest for mature teams |
| P5 Present but behind two or more competitors, or inconsistent across places | 7 | The fragility story |
| P6 The prospect already dominates | 2 | Low pain: pitch defend-and-prove, never a gap that is not there |
| P7 The probe does not apply to this category | 0 | Demote the account; recheck in 90 days |

If the user's offer has no natural probe, leave the section at zero for every account and say so; read the bands against a top score of 85.

---

## 6. Bands and response times

| Band | Score | Action |
|---|---|---|
| A | 75 or more | Senior-led (founder or exec) custom outreach within 48 hours; multi-thread the champion and the buyer |
| B | 60 to 74 | Rep sequence within 5 days, with the probe snippet or trigger line |
| C | 45 to 59 | Nurture; re-score weekly for new triggers |
| D | under 45 | Park; re-score quarterly |

**How the band meets the playbook tiers (Part C):** the stacking rule sets the tier (Tier 1 act now, Tier 2 act soon, Tier 3 nurture); the band sets how fast and who acts, and orders accounts inside a tier. A band D account drops one tier: the signal is real but the fit is not. A gated account never reaches either.

---

## 7. Calibration

- The first weights are reasoned judgement. Say so in the playbook.
- After about 30 closed deals (won plus lost), compare how often each attribute and trigger appears in wins versus losses, and move the weights toward what wins. Until then, keep the judgement weights.
- A weight change bumps the score version and affects future scoring only. Old rows keep the score and version they were given.
- Keep a calculator (one sheet per model: ICP number, sector weight, a 0 to 4 rating per attribute, days since each trigger, the probe pattern; only the inputs are editable, everything else is formulas) so a rep can re-score one account by hand and get the same answer as the run.
