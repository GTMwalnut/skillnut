# Enterprise track: public-data account expansion and senior decision-maker mapping

Load this when Stage 2 set the **enterprise** track: the buyer is a large company (named accounts, a top-1,000 or top-2,000 style list) and the job is to grow the account list from free public data, then map the senior people at those accounts into ranked, capped waves. All numbers below are illustrative unless a line says "in one build", and even those are rounded.

Three parts, run in order or alone:

| Part | Question it answers | Paid? |
|---|---|---|
| A. Public-data account expansion | Which large companies belong on the list that are not on it yet? | No (public sources) |
| B. Decision-maker mapping | Who are the senior people at those accounts, and who goes first? | Only if a classifier or enrichment tool is used |
| C. Classifier at scale | How do I label 50,000 job titles or 3,000 companies cheaply and honestly? | A little, with a quote first |

---

## Part A. Public-data account expansion

### A1. Freeze the exclusion set before sourcing anything
One file, written first: the existing account list (domains and names), customers, open deals, competitors, the client's never-contact list, and excluded industries (typically government agencies and utilities when the buyer needs an internal software function). Every later step checks against this file, and every backfill round checks against everything ever eliminated, not just the current list. In one build, the first backfill pulled four just-removed companies straight back in from the same pool; checking the cumulative eliminated list stops that.

### A2. Source pools, in fill order
| Order | Pool | Where it comes from | Watch out for |
|---|---|---|---|
| 0 | A published ranking of the largest listed companies (global top-2,000 style) | The publisher's own data feed, often a public JSON endpoint | Public companies only; the bar (sales, profit, assets, market value) is far above most ICP floors |
| 1 | Stock-index constituent tables, large, mid and small cap, per target country | Public constituent pages (encyclopedia tables are current and free) | Some pages fail to fetch or have a different layout; record which, and say which countries are under-represented |
| 2 | Published largest-private-company lists | Same publisher feeds | Includes law firms and partnerships that rarely fit |
| 3 | Listed companies above the revenue floor that sit in no index | The securities regulator's filings data (in the US, the XBRL "frames" API) | Industry comes as a standard code (SIC), so it needs mapping |

Pools 0 to 3 usually over-supply, which is why the ranking in A10 matters more than the sourcing. Use the built-in web fetch for these pages first; paid search tools only when a page will not fetch.

### A3. Dedupe against the existing list, then within the new pools
1. **First pass:** normalised domain (strip protocol, www, path and subdomain) OR normalised name (lowercase, legal suffixes such as Inc, Corp, Ltd, Plc, Group, Holdings removed, punctuation removed, compared as a token set). Either match = already on the list.
2. **Second, stricter pass** (it always finds more): acronyms against full names (initials of the legal name), domain-root prefix matching, industry words stripped before comparing (Bank, Banking, Financial, Bancshares), renamed companies, punctuation and accent variants ("U.S." vs "US", an umlaut vs its "oe" spelling), trading name vs legal name, two share classes of one company, one entity filing at two corporate levels.
3. Confirm every second-pass match by the **official website**, not by name similarity.

### A4. Geography: judge the account and the person separately
- **Account layer** decides whether the seller can contract with and support the company. Core = HQ in an approved country. HQ elsewhere but with a contract-capable operating subsidiary in an approved country = a separate Tier 2 file, never mixed into the core.
- **Person layer** (Part B) decides who at an approved account gets outreach.
- **"Exchange country is not HQ country."** A company listed on an in-scope exchange can be headquartered anywhere. Check HQ independently; in one build an audit corrected roughly 1 in 75 country labels and found several out-of-scope HQs that the exchange had made look in scope.

### A5. Floors, applied with honesty about the data
- Typical floors for this track: a revenue floor and an employee floor (for example $500M and 1,000 staff; confirm with the user).
- **Verified figure exists:** apply the floor.
- **No verified figure:** membership of a country's flagship index (or the only flagship index of a small economy) counts as reasonable evidence of scale. Keep the row, labelled `Revenue verified = No, index membership only, enrich before use`. A small-cap or mid-cap tier inside a big market is a real risk of being under the floor: drop rather than guess.
- **Every pool needs every floor.** A pool that never carried employee data never had the employee floor applied; in one build a batch of sub-floor companies came back in exactly that way, some of them previously removed for that very reason.

### A6. Remove what is not an operating buyer
- Pooled-capital vehicles: closed-end funds, investment trusts, listed investment companies. First by name ("Trust", "Fund", "Smaller Companies", "Capital Partners", "Private Equity"), then a second pass on the description text ("is an investment trust", "listed investment company", "closed-end fund"), because many names give nothing away. Keep real-estate operating companies: treat trust language as disqualifying only when the description does not also talk about property, hotels or storage.
- Also out: central banks, pre-revenue companies that are on a ranking only by market value, partnerships with no relevant internal function (law firms), consultancies the ICP treats as channel, externally managed vehicles with no staff, and subsidiaries already consolidated by a parent on the list (keep the parent, drop the sub, unless the client treats them as separate buying centres).

### A7. Map industries into the client's own scheme
Sources classify with their own schemes (GICS, ICB, SIC). Map each into the client's categories with a lookup table **and an explicit fallback per broad sector**. Never let unknown text fall into one default bucket. In one build a broken fallback quietly tagged about 7 in 10 rows as financial services; it was caught only because a spot-check found a food company and an industrial conglomerate in that bucket. Spot-check ten rows across sectors after every mapping change. Watch code ranges that a mapping groups wrongly (gas pipelines filed next to telecoms is a classic).

### A8. Verify revenue from public filings
- **US-listed:** the regulator's XBRL frames data for the latest calendar year (fall back one year for odd fiscal years). Query several revenue tags, because companies report under different ones (banks report interest income, not revenue). Match on the registry ID where the index table gives it, else on normalised name.
- **Non-US:** an open knowledge base (Wikidata's total-revenue property) in batches. Expect thin coverage: in one build fewer than 1 in 10 non-US mid-caps had a usable figure. Say so; do not fill the gap with guesses.
- **Check every lookup ID's label before using it.** Currency IDs guessed from memory pointed at a pop star, a person's biography and a year in antiquity. Look each one up.
- **Sanity-check outliers:** a small company reporting tens of billions is a tagging error; the same revenue under two related filers is one entity. Remove or merge, and log it.

### A9. Descriptions without wrong-company matches
- Pull a short description from a free encyclopedia summary API, falling back to its search.
- Retry with backoff, at modest concurrency. Separate "this page does not exist" (a definite 404) from "this request failed" (retry it). Never cache a transient failure as a permanent "no description": in one build that bug left 4 in 5 companies blank.
- Check every search-fallback match: the significant words of the company name must overlap the matched article's title, or the description is blanked. A blank is better than a description of a different company, an actor, or a village. Expect to tighten this check more than once.

### A10. Rank, then cut
Industry is a rank, not a gate. Tier A = the verticals with the most won-deal evidence, Tier B = solid but slower, Tier C = top-up only. Inside each tier rank by the measure closest to the seller's value model (for a developer tool, estimated engineering headcount; proxies cheapest first: headcount by function from an enrichment provider, open roles naming the problem, a public code organisation, an engineering blog), with revenue as the tiebreaker. Cut at the target count and keep the next 30 to 300 as a ranked overflow buffer for backfills.

### A11. Independent second audit
Run a second pass with a source the build did not use (for example the open knowledge base for HQ country, employee count, entity type, official website and parent organisation) plus name-pattern checks. Output recommended exclusions **by category** (duplicates the matcher missed, below a floor, wrong entity type, HQ out of scope, same company twice) and HQ corrections. The client rules on each category. Log rejected suggestions too (name collisions with a village, a mountain, a town). Write files through a temporary file and re-count rows after every write: an interrupted write once truncated a merged file to its header.

### A12. The audit document (ship it with the list)
- Every step with its actual count, and the reconciliation chain from raw to final (for example 3,000 > 1,900 > 1,800 > 1,700 > 1,400 > +400 > 1,800).
- A table of what is **not** verified: scope, and which column flags it (revenue from index membership only, description blank, an unconfirmed geography extension, countries under-represented by failed fetches).
- Suggested spot-checks a reviewer can run in ten minutes: ten random rows (real, HQ right, size roughly right), a search for every named exclusion (expect zero), three revenue figures traced to their filing.

---

## Part B. Senior decision-maker mapping

Use when the people pool at named accounts is huge (tens of thousands to well over 100,000 rows from several sources). Order matters: **remove first, classify the survivors, polish last**.

### B1. Merge and dedupe
LinkedIn URL is the key (email as fallback, name never). Log merged groups. Every source row lands in exactly one place: the ready list, a removed file with a reason, or the duplicates log. Say the sum out loud.

### B2. Suppress before you classify
| Check | Rule |
|---|---|
| Customers, active deals, named exclusions, owned contacts | Company or person out, with the CRM evidence |
| Closed-lost deal under 6 months ago | Company held back (cooling off); listed so the owner can release it by company |
| Closed-lost over 6 months ago | Kept, with a note on every row |
| Prior outreach | The catalogue rule: anyone who ever replied is out for good, whatever they said; a positive reply or meeting takes the whole company out; anyone touched on any channel in the last 100 days is out |
| Already connected to a sender on LinkedIn | Own file; the owner decides |
| CRM contacts who are only newsletter or product subscribers | Read their activity first; owner decides; web-form sign-ups flagged for sales |

### B3. Company fit, then geography
Judge every company once (what it does, not its tag; Module 2 rules). Then person location against the allowlist. Countries where B2B cold email is legally restricted are kept but routed LinkedIn first. Senior individual contributors in offshore hubs who have no line control are the classic dead end: keep hub heads (the site or country head of engineering), drop the rest, and tag every contact `hq` / `other in-scope` / `hub` so meeting rates can be compared after four to six weeks.

### B4. The title rubric (classify each distinct title once, not each person)
Every distinct title gets three things: a **function code**, a **level code** and **flags**. Build the function list from the ICP; a typical shape:

| Kind of code | Examples |
|---|---|
| Function: the ICP's core functions | 2 to 4 codes for the functions that own the pain (for a developer tool: platform, AI, architecture, top technology leadership) |
| Function: adjacent but usually out | general engineering, IT, security, risk and compliance, data, packaged business apps, QA |
| Function: never | hardware and physical engineering, product, program, sales and customer-facing, business leadership with no technology function, corporate (HR, finance, legal), pure research, unknown |
| Level | C-level; EVP/SVP/MD and global heads; VP; Head; Senior Director; Director; Associate Director and AVP; Senior Manager; Manager and Lead; Fellow; Principal; Staff; Architect; Senior IC; IC; Junior; founder or board with no operating level; unreadable |
| Flags (only when clearly true) | names the pain area; software rather than physical work; not in a current role; external or interim; supports an executive; names security or risk; customer-facing role at a vendor |

Rules that keep it honest:
- **Free rules first.** Settle the obvious titles with keyword rules; send only senior or ambiguous titles to a paid classifier (Part C).
- **Policy stays in code.** The classifier only supplies the judgments. KEEP, HOLD and EXCLUDE rules live in your own script, so a rule change never means paying to re-classify.
- Read the whole title. An include keyword beats an exclude keyword. Close-to-ICP titles are "retained as related", with a note.
- A medium-confidence read goes to HOLD, never to a silent removal.
- **Hold groups go to the owner as groups**, with sizes (for example "Director of IT with no infrastructure or AI scope: 2,600 people"). The owner rules on each group; record every ruling.
- Record `Title judged by` (rules, classifier, subagent) on every row.

### B5. Segments, tracks and the concentration question
Group survivors into segments (for example Exec, Champions, Architects and senior ICs, Function leaders, Managers). Then show concentration before anyone picks a cap: a handful of giant accounts can hold over half the pool.

| Cap per company (most senior first) | All tracks | Director and above only |
|---|---:|---:|
| 5 | 7,000 | 6,200 |
| 10 | 10,500 | 8,800 |
| 25 | 15,000 | 12,000 |
| No cap | 40,000 | 21,000 |

(Illustrative.) **Wave 1** is then a named cut, for example "champion and function-leader tracks, most senior 10 per company". Leave C-level at very large companies for later: they rarely answer cold.

### B6. The priority score and P1 to P4
Score everyone who has both an email and a LinkedIn URL, so the first sends go to the people most likely to reply.

| Part | Points | What earns them |
|---|---:|---|
| Role fit | up to 35 | Core segments score highest (about 25), adjacent segments less, exec least; plus 10 when the title itself names the pain area |
| Seniority band | up to 20 | Director, Senior Director and Head 20; Senior Manager and AVP 16; Manager, Lead and senior ICs 14; VP 12; EVP/SVP/MD 6; C-level 4. Directors and Heads answer cold mail far more often than VPs and C-level at large companies, and still carry budget influence |
| Intent and timing | up to 45 | Account-level signals (for example a technology migration ranked high, medium or low, plus a few points for several open matching roles), membership of a buyer audience, new in role (about 12: the first 90 days), already a CRM contact never sequenced, in Wave 1, on the priority account list |
| Deliverability | up to 15 | Verified within 90 days 10 (180 days 7, older 4, never 2); no email flag 5, alias domain 2 |
| Geography | up to 10 | Core English-speaking markets 10; other in-scope countries 5; countries where cold email is legally restricted 0, LinkedIn first |
| Penalties | minus | Account closed-lost over 6 months ago minus 5; program, training, research, policy, governance or risk title minus 8 |

| Tier | Score | Use |
|---|---|---|
| P1, send first | 80+ | First campaign, capped at 5 per company, email plus a LinkedIn touch |
| P2 | 70 to 79 | Second campaign |
| P3 | 60 to 69 | After first results; re-score with what replied |
| P4 | under 60 | LinkedIn or a champion intro, not cold email |

Every row carries `Why` (the reasons) and `Caution` (warnings). Say plainly: **the weights are cold-outreach norms, not this client's reply data; refit them once the first batch has replies.** Hold back any address that sits on two or more people until the pair is collapsed.

### B7. Tranches
A tranche = one tier + one seniority band (for example Director to VP, no C-level, no managers) + clean email + at most 5 per company. Drop rows with a blocking caution (restricted country, program or policy title, unverified or stale email, unknown location) and list them. A company can reach up to 10 people across two tranches; say so.

### B8. Job movers, then the pre-upload re-check
- Before upload, ask an enrichment tool for each person's current employer. Ignore domain differences that are the same company (aliases, parents, old names; keep a `Known domains` list). For genuine movers, run the new company through the same ICP checks and the new title through the same rubric: re-home the ones that pass (old role kept in `Notes`), remove the rest with the reason.
- Fresh read-only re-pull of the CRM and outreach tools right before upload, re-run suppression, and list what it removed in a `removed at pre-upload check` file.
- Namesake sweep against the senders' networks and earlier lists; possible namesakes go to the owner.
- **One sender per company**, the same sender on email and LinkedIn.

### B9. Narration funnel (illustrative)

| Step | People |
|---|---:|
| Source rows across three lists | 150,000 |
| Unique people | 146,000 |
| Suppression (customers, deals, cooling off, exclusions) | -12,000 |
| Prior outreach (replied ever, touched in 100 days) | -1,500 |
| Already connected to a sender (owner's file) | -150 |
| Company not a fit, competitors | -7,000 |
| Outside serviceable countries | -6,000 |
| Title or seniority | -94,350 |
| Ready + on hold for owner rulings | 15,000 + 10,000 |

Every line reconciles: the removed files plus ready plus hold equal the unique people.

---

## Part C. Classifier at scale (cheap, confidence-scored labelling)

Use for any bulk label: job-title function and level, company type from a homepage, industry from a meta description, size band, region, reply intent.

1. **Pick the task shape:** a choice (one label from a fixed set), a score (0 to 1), or a yes/no. Write the label set before the first call.
2. **Feed it lean inputs.** For company type or industry: the homepage title, meta description and a few lines, not a crawl. For titles: the title text only. In one build, a lean input of title plus meta description was enough to sort a couple of thousand companies.
3. **Free rules first.** Drop obvious fits and non-fits with keyword rules and free signals; the paid model only sees rows that need judgment.
4. **Price it before you run it.** Requests x tokens x price; check the balance; tell the user; wait for a go. The repeated question text, not the data, is usually the cost: in one build a long question set repeated on every title cost about five times a lean version and ran the account dry mid-run.
5. **Pilot, cache, stop.** Test on a small sample, cache every answer to disk, and stop at the first out-of-credits error instead of retrying.
6. **Thresholds.** Auto-apply above a threshold, human queue below. One real set: business type accepted at confidence 0.7 or more, secondary yes/no checks at 0.5 to 0.6. Below that, the row goes to review.
7. **Swappable engine.** A typed-judgment API, a cheap model through an API key, or AI subagents using the same labels and the same policy code all work. Subagents give no probabilities, so use a fixed confidence and say the low-confidence hold applies only to rows that had a real probability. If two engines labelled different rows, say their agreement is untested.
8. **Write back with provenance.** Label, confidence, `judged by`, run date, and a cost log line per batch. Never overwrite a human ruling with a model label.
