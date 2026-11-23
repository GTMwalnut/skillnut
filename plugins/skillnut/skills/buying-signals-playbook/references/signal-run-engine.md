# Run a signal: the shared engine

Load this file when the user picks **D: Run a signal**. It holds the parts every signal pipeline shares: the run spine, the keyword library, source grading, scoring, the account score, suppression, caps and persona split, the opener rules, the output schema and reply routing. The per-signal detail lives in `signal-pipelines.md`; load only the section for the signal being run. The full account-scoring model lives in `account-scoring-model.md`.

Design (options A to C) decides WHICH signals matter. Run (option D) turns one of them into a list of real accounts and people, tiered, with a first line a rep can send. Nothing is sent from this skill. The output is a reviewed file, ready for the user's sequencer or for the `campaign-send-checklist` skill.

---

## 1. The run spine (every pipeline follows these eight steps)

| Step | What happens | Why it matters |
|---|---|---|
| 1. Scope | Name the signal, the target universe (a CRM export, a target list, or "open web"), the lookback window and the run cadence | A run with no scope finds everything and means nothing |
| 2. Find | Pull the raw events from the source in `signal-pipelines.md` | Raw volume first; filtering comes next |
| 3. Resolve | Tie every event to one company domain. No domain, no signal | A keyword with no account attached is noise |
| 4. Grade the source | Strong or weak (section 3). Weak sources demote | Where a signal came from matters more than how well the keyword matched |
| 5. Exclude | Competitors, customers, active deals, do-not-contact, prior outreach (section 6) | Every run must be safe to hand to a sequencer |
| 6. Score and tier | Signal weight sets queue order (section 4); the account score runs gates first, then fit, timing and probe, and gives a band (section 5); the Part C stacking rule sets the tier | The team works the top of the list first, at the speed the band asks for |
| 7. People | Capped per account, in the event's country, buyer titles first, split into Leaders and Operators (section 7) | The signal is about a company; the message goes to a person |
| 8. Opener and file | One first line per account, a source link on every row, a run log (sections 8 and 9) | Reps trust a line they can check |

Run a small pilot first: 10 accounts end to end, show the user, then run the rest. Any paid enrichment needs a cost quote and an explicit yes for that run (see the `crm-data-health` skill, spend gate). Never re-use a paid tool's workspace without checking it is the user's own account.

---

## 2. The keyword library (for news, filings and job-post signals)

Build it with the user from their product and their buyers' pain words. Six tiers:

| Tier | What goes in it | How it is used |
|---|---|---|
| Displacement | A named incumbent product being replaced, migrated off or sunset | Strongest signal there is |
| K1 core | The exact phrases for the problem the product solves | Can fire a signal alone |
| Tech-estate qualifier | Named systems that mean the account fits (old platforms, specific stacks) | Fit evidence, strong when paired |
| Trigger event | Mergers, divestitures, restructuring, new leader appointed, breach or fine, site closures | Fires with a K1 or qualifier nearby |
| Job-post phrase | Phrases that appear in job descriptions when the project is being staffed | Leading indicator: job wording tends to show up 3 to 6 months before a formal buying process |
| K2 broad | Fashionable umbrella terms (for example "AI readiness") | Never alone. Only when paired with K1 context. Feeds nurture, never priority outreach |

Then add two lists:

- **Exclusion phrases.** Adjacent categories that share your words but are a different market. Without them the search drowns. Example pattern: "migration" alone is not "retirement"; keep it only when paired with a K1 word or a named old system. A broad theme with no hook (for example "data governance" alone) is demoted to medium, not dropped.
- **Competitor block list.** Every vendor in your space, keyed by domain. Used twice: competitors are never targets, and a keyword match on a competitor's own product page is never intent. It is the vendor describing its product.

Seed queries are Boolean combos: (K1 phrase OR K1 phrase) AND a named company; displacement phrase AND (replacement OR migration OR sunset); trigger phrase AND a size marker.

**Market calibration.** In a niche market, lean low-filter and high-recall: let more through than you reject, and tune precision later. In a crowded market, tighten the exclusion list first.

---

## 3. Source grading

| Strong source (keeps or confirms high) | Weak source (demote or drop) |
|---|---|
| The account's own press release, annual or quarterly filing, earnings call | Competitor product or solution pages (hard drop) |
| The account's own published internal comms (memos, committee minutes, IT status pages) | Generic news or industry blogs not about a specific account (drop) |
| Job posts on the account's own careers page or company jobs tab | Topic hub or category landing pages (drop) |
| A procurement portal where the account is the issuer | Award or analyst-recognition pages (drop) |
| | Roundup articles where the account is a side mention (keep only if it is the main subject) |

The rule:

| Source | Content match | Result |
|---|---|---|
| Strong | High | High |
| Weak | High | Medium |
| Weak | Medium | Drop |

"Strong" also needs the source domain to match the account, except for filings and news with explicit attribution in the body.

**Hard drops at the find step:** events and conference marketing, award pages, generic strategy talk with no hook, a software vendor describing what it does for its customers ("vendor, not buyer"), and articles where the company is a side mention.

---

## 4. Scoring a signal (account level)

`signal score = keyword tier weight x segment weight x region weight x size multiplier`

Starting weights (tune against won and lost deals once there are enough):

| Keyword tier | Weight |
|---|---|
| Named-incumbent displacement | 1.0 |
| K1 core | 0.9 |
| Tech-estate qualifier | 0.8 |
| Trigger event | 0.7 |
| Job-post phrase | 0.5 |
| K2 broad | 0.3 |

Segment and region weights come from the user's ICP: rank their segments and give the top one 1.0, stepping down (for example 0.95, 0.85, 0.8 and so on, 0.4 for unclassified). Regions the same way (core 1.0, secondary 0.7, rest 0.5). Size multipliers mirror the ICP sweet spot: in the sweet spot 1.0, one band below 0.6, well below 0.2.

The score sets queue order. The Part C stacking rule still sets the tier. Confidence per event is **high** (named system, named project with a timeline, a regulatory incident, or a strong source) or **medium** (clearly on-topic but no named anchor, or a weak source). An event whose confidence cannot be decided is discarded, never stored.

When one account has several events, keep all of them in the event log but pick one to drive the message: high beats medium, then the higher keyword tier, then the most recent.

---

## 5. The account score (replaces the old blended lead score)

Load `account-scoring-model.md` for the full model. In short:

`score (0 to 100) = Fit (max 60) + Timing and intent (max 25, decayed by age) + Probe (max 15)`

1. **Gates, reducers and reroutes first.** A gate failure removes the account with a logged reason; it is never scored. Reducers subtract a few points. Reroutes move the account to the ICP it belongs to and score it there.
2. **Fit.** Rate each fit attribute 0 to 4 (4 Ideal to 0 Absent); `points = ICP weight x rating / 4`; multiply the sum by the sector weight; cap at 60. Missing data is rated 2 and caps the account at band B until verified.
3. **Timing.** Each trigger has points and a window. Full points in the first third of the window, 50% in the second third, 25% in the final third, zero after. Sum, cap at 25, floor at minus 10 (negative triggers such as layoffs in the buying function).
4. **Probe** (optional). A pre-outreach check that shows the gap the product closes, run only on accounts that passed the gates with fit of 35 or more. Most severe pattern, plus 1 if it repeats, cap 15.
5. **Band.** A 75+ senior-led outreach within 48 hours; B 60 to 74 rep sequence within 5 days; C 45 to 59 nurture, re-score weekly; D under 45 park, re-score quarterly.

**The research pass that finds triggers** (only for accounts that passed the gates, have a name and a domain, and fit of 35 or more). Research once per company, not per person: at most 3 web searches (new senior leader in the buying function, the K1 topic, the broader change programme), a 4th only if all three found nothing (merger, funding, restructuring). Each trigger found goes into the timing section with its date and source link. Time-box the pass (default 60 minutes); anything unfinished keeps its fit-only score and is marked done. Exports wait until every row is marked done.

**People inside an account** are ordered by persona and seniority (section 7), not scored separately; the account score is what decides speed.

**Every score carries:** the score, the band, the fit, timing and probe subtotals, gate and reducer notes, a 2 to 4 sentence rationale a rep can read, and a score version. Weights start as judgement; after about 30 closed deals, compare attribute and trigger frequency in wins versus losses and move the weights. That changes future runs only; it never re-scores old rows.

**How it meets the playbook tiers:** the Part C stacking rule sets the account tier (Tier 1 act now, Tier 2 act soon, Tier 3 nurture). The band sets how fast and who acts, and orders accounts inside a tier. A band D account drops one tier: the signal is real but the fit is not.

---

## 6. Suppression (run on every pipeline, before people are pulled)

Run in this order and log a reason for every removal:

1. **Competitor pre-filter.** Block list by name and domain. For accounts in services or consulting (or with "consulting", "solutions", "services", "partners", "integrators" in the name), check the homepage: if they SELL what you sell, exclude. If the check fails, keep the account (fail open) and say so. Cache each decision for 90 days.
2. **Customers and active deals.** Any open deal stage and any won customer is excluded from automated outreach; route it to the owner instead. Closed-lost, closed-no-opportunity and never-started accounts are eligible.
3. **Do-not-contact companies.** Match by company name AND root domain, at a word boundary: the exact brand label, brand-hyphen, or brand plus a country domain. That catches regional arms and avoids look-alike names (a brand that merely starts with the same letters is not the same company).
4. **Prior outreach (the catalogue rule, no exceptions).** Anyone who has ever replied, whatever they said, positive, negative or neutral, is excluded permanently from automated outreach. A positive reply takes the whole company off. Anyone touched on any channel in the last 100 days is excluded (cooldown). Touched more than 100 days ago and never replied: eligible, with the last-touch date carried into the file.
5. **Freshness.** If the same account was already found for the same topic in the last 7 days, skip it. A new topic, or an older find, goes through.
6. **Already queued.** Anyone already sitting in another live campaign is held, not added twice.

Read-only in the CRM and outreach tools throughout. For the full pre-send pass, hand the file to `campaign-send-checklist`.

---

## 7. People and caps

- **Default caps:** 100 accounts per daily run for open-web signals, 5 people per account. Weekly signals (job posts) run once a week. Some plays need a wider net (an expansion or new-office signal touches facilities, real estate, procurement and the C-suite at once); set a higher per-firm cap with the user, and never go above it. Tell the user the caps and let them change them.
- **Leaders and Operators.** Split every contact list into two tracks: **Leaders** (C-suite, founder, president) and **Operators** (the hands-on functions the signal lands on, for example facilities, real estate, procurement, operations, engineering). Same signal, two different openers: Leaders care about outcome, cost and timeline; Operators care about the spec, the logistics and the vendors. One opener for both undersells to each.
- **Escalate on silence.** Any account with zero engagement after a set window (default 10 days) gets the same signal reframed as a 3-message LinkedIn sequence, run in parallel with the email track, not as a resend of the email. Write that LinkedIn version in the same run so it is ready.
- **Title passes.** Pass 1 asks for the hands-on buyer titles (VP, director, architect, operator). If fewer than 3 come back, Pass 2 adds the C-suite owner titles to fill up to 5. Three to five from Pass 1 is a finished result.
- **Geography.** Keep people in the country where the event happened; for a job post, prefer the posting's state or region, then the country. Never pull people from a different continent.
- **Identity.** Name, email, LinkedIn and company must agree. A missing last name may be filled from the email local part or the LinkedIn slug only when both agree. Never guess a name from a pattern.

---

## 8. Opener rules (shared)

- One event per opener. One product or project name per sentence.
- Use a readable name, never an internal code. If only a code exists, name the category instead.
- **The cited-source rule.** Every hit carries its source URL and a one or two sentence summary of what the source says, captured at the find step. No URL and summary, no opener. When the source is public and citable, the opener names it ("I saw on {publication} that...", or the job board) together with the concrete details the source gives (place, size, date). When the signal is soft or uncitable, say what the move suggests, never invent an article.
- Never compliment. Never claim the person works on the thing you found.
- Never mention your product in the first line.
- Website visits and post engagement have their own rules (see their sections). The default is: do not mention them.
- Stale or failed events are never used (a project cancelled, a result that missed its goal).
- Signal-led copy is a Version A; a clean generic Version B goes to the rest of the same list, so you can see whether the signal earns its keep.

### Writing openers from research: the two-prompt method

For signals that come from researching each account (news, milestones, any open-web event), use two separate prompts, never one:

**Prompt 1, the researcher (per account).** Input: company name and website. Task: find the most significant event at this company in the last 12 months that relates to the user's problem area. Sources to check, in this order: the company's own website and newsroom, public registries and regulators relevant to the industry, filings, and press releases. Output: the event, its date, the source URL, a two-sentence summary, and "none found" when nothing qualifies (never a guess).

**Prompt 2, the writer (per account).** Input: the researcher's output and the user's product line. Rules to give it:
- One sentence. A hard word cap (default 20 words).
- **Event selection:** prefer the most recent event that creates work for the buyer's function; prefer a named, dated event over a general trend; skip anything stale, cancelled or failed; if two events tie, pick the one the buyer's team would be most involved in; if nothing qualifies, return blank so the account gets the plain version.
- **Do:** name the event in plain words, name the source when it is citable, keep the company's own wording for the event.
- **Don't:** compliment, claim the person worked on it, mention your product, stack two events, use internal codes or jargon the buyer would not say.
- **Give it examples.** Two or three good openers and two or three bad ones, each with one line on why. Without the bad examples and the why, the model drifts back to flattery. Illustrative (made up):
  - Good: "Saw in the {Company} newsroom that the new {site} opens in the spring." (one event, dated, sourced)
  - Bad: "Congratulations on your amazing growth and recent milestones!" (compliment, no event, no source)
  - Bad: "As the person leading the {project} rollout, you must be busy." (claims their role in it)

Read 10 openers before the full run. If more than one or two break a rule, fix the writer prompt, not the rows.

Copy itself belongs to the `copywriting-messaging` skill; this file only sets what the first line may and may not claim.

---

## 9. Output schema and run log

One row per event in the event log, then one row per person in the outreach file.

| Field | What it holds |
|---|---|
| source_url | Direct link to the article, post, filing, portal page or record |
| source_summary | One or two sentences on what the source says (the cited-source rule) |
| found_at / event_date | When we found it; when it happened (windows run on event_date) |
| signal_type | Which pipeline |
| keyword_tier / keyword_matched | The tier and the exact phrase |
| company_name / company_domain | The resolved account |
| match_confidence | How sure the entity match is, 0 to 1 |
| context_snippet | The sentence or two around the match |
| source_quality | strong or weak |
| confidence | high or medium |
| relevance_check | One sentence: which of the user's problems this event implies |
| signal_score / tier / account_score / band / fit / timing / probe / score_version | Sections 4 and 5 |
| persona_track | Leader or Operator (section 7) |
| opener / version | The first line; A (signal) or B (generic) |
| linkedin_escalation | The 3-message LinkedIn version for accounts with no engagement after the window |
| exclusion_reason | Blank, or why the row was removed (kept in a separate Removed tab) |

**Run log, every run:** events found, accounts approved, people written, removals by reason, tier counts, whether any time box was hit, and errors. One line in chat, the detail in the file.

Remember the Part B and operational guardrails in SKILL.md: create-only, dedup accounts by domain, dedup events (account + signal type + source + date), expire rather than delete, date-stamp everything.

---

## 10. After the send: reply routing (carried in the playbook)

Nothing is sent from this skill, but every run file says where replies go, because a signal that gets a yes and then waits a day is wasted.

- **Positive replies go to an AE alert at once,** with the originating signal and source link attached. The source pattern: when the email or LinkedIn tool detects a positive reply, an automation (for example Zapier) writes it to a shared sheet and notifies the assigned AE and the head of sales; the AE calls or replies with the right asset and fills in "followed up" and the outcome on the row, which feeds next month's targeting. Wiring this belongs to `gtm-automations` or `ai-responder`.
- **Negative replies get a competitor-software check.** On a "no" or "we already have something", an agent researches whether the account already uses a competing product: it searches for the product category plus the competitor names (phrase the category precisely, because competitors brand the same job differently), and checks competitor websites for the account's logo on customer pages. A confirmed competitor goes to the competitor-displacement pipeline (`signal-pipelines.md` section 8). **Wait, then compare:** after a waiting period the user sets (default: the 100-day cooldown), draft one competitor-comparison message for that person. It never goes out automatically: anyone who replied stays out of automated outreach for good, so a person reviews the draft and decides whether it is sent and whether anything follows it.
- Reply analysis over time belongs to `campaign-reply-insights`.
