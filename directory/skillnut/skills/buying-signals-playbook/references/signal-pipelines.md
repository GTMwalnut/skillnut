# Signal pipelines

One section per signal. Load only the section being run, together with `signal-run-engine.md` (the shared spine, scoring, suppression and opener rules). Each section covers: what fires it, where the data comes from, how to qualify and tier it, the outreach angle, any extra suppression, and the gotchas.

| # | Pipeline | Best for | Cadence |
|---|---|---|---|
| 1 | News, filings and earnings intent | Larger accounts that get press and file reports | Daily (filings on filing dates) |
| 2 | Job postings | Almost everyone | Weekly |
| 3 | New hires and job changes | Anyone whose buyer title is clear | Weekly |
| 4 | Public records | Sellers into regulated or inspected industries | Monthly or per data release |
| 5 | Milestone events | Markets with public product or regulatory milestones | Weekly |
| 6 | RFP and tender discovery | Sellers into enterprise and public sector | Weekly digest |
| 7 | Dormant pipeline | Anyone with 1 to 2 years of CRM history | Monthly |
| 8 | Competitor displacement | Anyone with an incumbent to unseat | Quarterly, plus on news of a forced switch |
| 9 | Post engagers | Founder-led brands posting on LinkedIn | Per post batch |
| 10 | Founder and exec network | Founders and execs with big networks | Once, then quarterly |
| 11 | Website visitors (with speed-to-lead) | Sites with meaningful traffic | Daily, alerts in real time |
| 12 | Expansion and new office (lease) | Anyone who sells into a new site: fit-out, facilities, IT, security, services | Monthly per segment |
| 13 | Event attendees with a 90-day overlay | Anyone whose buyers go to the same events | Per event |
| 14 | Lookalikes with an intent overlay | Anyone with a list of best-fit accounts and room to grow it | Monthly |

The persona split (Leaders and Operators) and the LinkedIn escalation on silence apply to every pipeline; they live in `signal-run-engine.md` section 7.

---

## 1. News, filings and earnings intent

**Fires when:** an account's own news, filing or earnings call mentions a K1 phrase, a displacement phrase, or a trigger event paired with a K1 or tech-estate word.

**Data comes from:** news search and RSS, trade publications in the user's market, press-release wires, annual and quarterly filings (the sections where management discusses the business), earnings-call transcripts, public procurement portals, breach-notification trackers, and user communities for the old systems being replaced (where complaints and migration talk show up). Run it with the agent plus Exa.ai or Parallel Web Systems across the list; Clay or Deepline for research columns.

**Qualify and tier:** keyword library, source grading and scoring from the run engine. Keep only accounts in the ICP size floor. High confidence needs a named system, a named project with a timeline, a regulatory incident, or a strong source.

**Outreach angle:**
- Citable source: "I read about {Company}'s {topic, three words max} at {location} in {publication}." Then the problem it implies, then peer proof.
- Soft or uncitable (filing language, inferred): "{Company}'s move toward {verb phrase} caught my eye: {one clean clause}." Never invent an article.
- Subject line: the plain topic plus the company, three words max for the topic, no technical codes ("Legacy system transition at {Company}").

**Extra suppression:** none beyond the engine, but enforce the competitor-page drop hard. It is the most common false positive in this pipeline.

**Gotchas:**
- This pipeline never searches job boards. A job post in the results is discarded here and handled by pipeline 2, so the two never double count.
- Same account, same topic inside 7 days: skip. Only fresh intent goes through.
- Pair every keyword match with the account before scoring. A great keyword in an article about nobody in particular is noise.

---

## 2. Job postings

**Fires when:** an account posts a role whose title or description contains your K1, displacement or job-post phrases, within the last 90 days (stretch to 180 if the market is quiet).

**Data comes from:** the account's own LinkedIn jobs tab and careers page (strong), then job boards and aggregators (weak). Apify for board scrapes on a keyword list; Clay for job tracking against a fixed account list. To build the universe from the CRM, page through ALL companies with the list endpoint, because CRM search endpoints often cap at around 10,000 results.

**Qualify and tier:**
- Universe first: parse the employee band, and drop rows where the band and the real headcount disagree (a large company tagged with a tiny band is a data error, not a target).
- Negative filters straight away: adjacent-category roles, recruiter and HR postings, event roles, and roles at software vendors describing what they do for their customers.
- Read the description, not just the title. Extract: the inferred project, any named old system, the department, internal words like "decommission" or "sunset", and the source quality.
- High: named system or project with a timeline, or a strong source. Medium: on-topic but no anchor, or a weak source. Undecidable: drop.
- Several posts at one account: keep all in the posting log, use the best one for outreach (high beats medium, K1 beats broad, newest wins ties).

**Outreach angle:** "I came across {Company}'s job posting for a {normalized role} on {board}: {one-line bridge to the problem}." Bridge from the description's own keywords; if there are none, fall back to the normalized title. Normalize long titles to what a human would say ("Information Technology Enterprise Architect Software Engineer" becomes "IT Enterprise Architect").

**Extra suppression:** the four-layer funnel: competitor block list, CRM active deals, competitor homepage check, and prior sources (accounts already picked up by another pipeline this week).

**Open versus filled (two variants of the same signal):** some roles only get created once an initiative is funded, so the posting itself is the signal (for example a new head of a function that owns your problem).
- Monitor job boards and career pages for a fixed list of trigger titles.
- Corroborate: check whether the same company has another recent signal (funding, expansion news). A posting plus a corroborating signal is a Tier 1 combo.
- **While the role is open:** the message speaks to the initiative the role exists for, not to the hire.
- **60 or more days after it is filled:** a different message, to the new hire by name and title (hand the person to pipeline 3). Reaching out while the seat is open, or right after it is filled, puts you early instead of among the inbound pitches.
- This variant is written up from a play that was specified but not yet run end to end; pilot it small and say so.

**Gotchas:**
- Job wording tends to appear 3 to 6 months before a formal buying process. This is early, so the tone is curious, not "I hear you are buying".
- Pull people in the posting's region first, then the country.
- A busy recruiter account can post hundreds of roles. Count distinct relevant roles, not raw posts.

---

## 3. New hires and job changes

**Fires when:** someone with a buyer title starts at a target account, or a past champion moves to a new company.

**Data comes from:** Clay job-change tracking (the most robust option), job-change exports from data providers, and the LinkedIn "Role start" date.

**Qualify and tier:**
- Bucket by tenure from the role start date:

| Tenure | Bucket | Opener style |
|---|---|---|
| 6 months or less | New | Congratulate and offer help settling in |
| 6 to 12 months | Recent | "Noticed you've been leading {area} at {Company} for a few months" |
| Over 12 months, or unknown | Generic | No recency claim at all |

- Normalize function and seniority, and clean company names (drop legal suffixes, location tails, descriptors, "formerly" clauses).
- Spot-check 5 start dates by hand before trusting a feed.

**Outreach angle:** the new person wants early wins and is reviewing tools. Use the vocabulary of their segment, row by row.

**Extra suppression:** for any account with a dead deal, check whether this person was the named contact on that deal or a different person. Same person: they are warm history, route to the owner. Different person: a fresh contact.

**Gotchas:**
- Never guess a last name from an email pattern. Derive it only when the email local part and the LinkedIn slug agree; otherwise leave it blank and flag it.
- Apply a job change only when the name matches and the new role is plausible. A board seat or side role is not a primary employer; leave it alone.
- If campaigns are split by owner, rebuild each owner's file after every change. When loading to HeyReach, the column must be named exactly "LinkedIn Profile URL".

---

## 4. Public records

**Fires when:** public inspection, violation, permit or filing data shows an account doing measurably worse (or growing faster) than its peers, in a way your product helps with. Examples of this kind of data: transport, food or workplace safety inspections, environmental permits, building permits, public contract awards.

**Data comes from:** the government open-data portal or API for that dataset. Pull 24 months of records, joined to the account by its registry id or name and domain.

**Qualify and tier:**
- Map the record codes to the user's service lines first. Only codes the product genuinely relates to count.
- Compare each account to its own size band's peer median (for example four bands by asset count, site count or headcount). Peer median is computed only on accounts with 20 or more inspections.
- **Problem signal:** the account's rate per 100 inspections is at least 2x its band's peer median (with a floor of 0.5 per 100), with at least 3 write-ups and at least 20 inspections; OR 3 or more write-ups in the last 90 days.
- **Growth signal:** inspections up 30% or more on the previous 12 months, with at least 20 in the previous 12.
- **Expansion signal:** activity in 3 or more new states or regions in the last 9 months.
- Accounts with a signal get Version A (signal line); the rest of the same list gets Version B (generic).

**Outreach angle:** one factual line, in three shapes so it does not repeat:
- "Saw in public {agency} records that your {assets} were written up for {issue} in {region}, {region} and {region}, most recently in {region} this {month}."
- "Noticed {number in words} {issue} write-ups on your {assets} in public records over the last two years, the latest in {region}."
- "Public records show your {assets} were written up for {issue} {number in words} times in the last two years."
- A short version for LinkedIn. Up to 3 regions; numbers written as words; counted per inspection.

**Extra suppression:** parent-company domains (a parent in another line of business that happens to appear in the records) are parked for a separate campaign, not mixed in.

**Gotchas:**
- Never say the product fixes the violation. Say what it actually handles (the filing, the process, the compliance work).
- No company name in the signal line. No money maths built on their size. No currency symbols: write "dollars".
- Classify the account from its own website alone. Feeding the classifier the registry name and the label you hope for makes it agree with you.

---

## 5. Milestone events

**Fires when:** an account hits a public milestone that creates work for your buyer: a regulator approval, a formal filing, a special designation, a positive study or test result, a late-stage programme going active, a licensing or partnership deal bringing in a new product.

**Data comes from:** public registries and regulator databases for the user's market, the account's press releases and pipeline pages, and trade press. Restrict to the user's sales geography: ignore events in other jurisdictions; if that is all there is, refer to the general area of work instead.

**Qualify and tier:** pick ONE event per account using a priority ladder. Build the ladder with the user; the shape that works:

| Rank | Event | Window |
|---|---|---|
| 1 | Final approval or certification | 6 months |
| 2 | Formal filing submitted | 6 months |
| 3 | Special or fast-track designation | 12 months |
| 4 | Positive late-stage result | 6 months |
| 5 | Late-stage programme active | Current |
| 6 | Niche or priority designation | 12 months |
| 7 | Licensing or partnership deal bringing a new product | 12 months |
| 8 | Several mid or late-stage programmes running at once | Current |
| 9 | Mid-stage programme active | Current |
| 10 | Early-stage programme only | Current, last resort |

Same rank: the most recent wins. Hook tier for the tier list: A (decision pending), B (result due), portfolio, or none (standard opener).

**Outreach angle:** one sentence, 20 words max, a fact about the milestone connected to the buyer's workload, peer to peer. For example: "With the filing in, the next few months for your team are probably intense."

**Extra suppression:** none beyond the engine.

**Gotchas:**
- Product names: use the brand OR the readable generic name, never both, never an internal code, never ALL CAPS, never the full technical name. Code only? Name the category ("your lead {area} product").
- Never "I noticed", "I came across" or "I saw that". No compliments. Never say the person works on that product. Never stack phases, names and categories in one line.
- Failed results and stale facts are never used.
- Keep a source receipt (link) next to every line for review.

---

## 6. RFP and tender discovery

**Fires when:** an account publishes, or is about to publish, a request for proposal in the user's category.

**Data comes from four routes, run side by side:**

| Route | How |
|---|---|
| a) Search dorks | Via Exa.ai or Parallel Web Systems: `site:{domain} ("RFP" OR "request for proposal" OR tender OR solicitation)`, `("request for proposal" OR RFP) filetype:pdf "{category}"`, `inurl:procurement OR inurl:suppliers "RFP" "{category}"` |
| b) URL patterns | For every target domain, probe `/procurement /sourcing /suppliers /vendors /rfp /rfq /bids /tenders /about/suppliers /corporate/procurement` and supplier links in the footer or careers section. Live pages get crawled (Firecrawl, Crawl4AI or Apify); missing ones get change detection (Visualping, Distill.io) |
| c) Supplier portals | Large companies route RFPs through portals (SAP Ariba, Coupa, Jaggaer, Ivalua, GEP SMART, Oracle Supplier Network). Register the user once per category on each: register once, get many invitations. Where the user already has a login, check open opportunities on a schedule |
| d) Pre-RFP signals | Job posts saying "vendor evaluation", "RFP management" or a category role; a new procurement, category or business-unit leader (vendors get re-evaluated in the first 60 to 90 days); funding or M&A; tech stack churn (BuiltWith or Wappalyzer); earnings mentions of the category. Clay suits this route |

Target lists to point it at: the user's serviceable market list, competitor-displacement accounts, and current customers (for expansion RFPs). Public-sector portals cover the government segment.

**Qualify and tier:** the agent classifies every find with three questions: is it a real RFP? Is it in our category? Is it still open? Then dedupe and score. A real open RFP in category is Tier 1 by itself. A spike of pre-RFP signals at one account is Tier 1 for direct outreach before anything is issued.

**Outreach angle:** for a live RFP, the bid process rules (follow the issuer's instructions; cold outreach to evaluators during an open tender can disqualify you). For pre-RFP signals, normal signal outreach, tied to the change you saw.

**Extra suppression:** none beyond the engine.

**Gotchas:**
- Most private-sector RFPs are never posted publicly. Route d is how you catch them.
- Run the routes as a 4-week bake-off: week 1 set up, weeks 2 and 3 run all routes, week 4 compare coverage, accuracy and effort per real RFP found, then commit to the winner.
- Output a weekly digest: new RFPs (link, issuer, deadline), new pre-RFP accounts, and anything closing in 14 days.

---

## 7. Dormant pipeline

**Fires when:** a deal went closed-lost, or stalled with no activity for over 3 months, and something has since changed at the account.

**Data comes from:** the CRM (deals by stage and last activity, usually the last 12 to 18 months), plus job-change data, hiring, funding and tech-change checks on those accounts. The agent plus the CRM API can pull this in one pass.

**Qualify and tier:**
1. Pull closed-lost and stalled deals. Exclude any deal an owner is actively working.
2. Check what changed: did our contact leave? Is there a new leader in the buying role? New hiring, funding or tech change?
3. Re-score fit with today's ICP.
4. Rank: high-value accounts with a fresh change are Tier 1, for reps. The rest go to a sequence.
5. Start small: aim for the top 10 or so worth a rep's personal note before scaling.

**Outreach angle:** reference the past conversation and its loss reason, then what changed. Timing loss: "Last time the timing wasn't right; with {change}, worth a fresh look?" Price loss: lead with a smaller start. Lost to a competitor: see pipeline 8.

**Extra suppression (this is where the catalogue rule matters most):**
- People who replied in the old deal are not cold prospects, and they never go into an automated sequence. They go to the deal owner for a personal, human note.
- A contact who has moved to a new company and had replied before: also owner-handled, a personal note, not a sequence.
- Automated sequences go only to NEW people at the account (the replacement, the new leader) who have never replied and are outside the 100-day cooldown.
- Tag every reactivated deal in the CRM so two people do not chase it.

**Gotchas:** a stale CRM is the usual blocker. Expect a good share of old contacts to have moved on; the job-change check is not optional.

---

## 8. Competitor displacement

**Fires when:** your own CRM notes, call logs, meetings or deals show an account unhappy with, or replacing, a competitor. Also when a competitor announces it is sunsetting a product: a forced-switch trigger for every customer of it.

**Data comes from:** search every CRM engagement type (notes, calls, meetings, emails) and deals for each competitor's name and product names. Call-recording tools for the verbatim. Vendor websites to verify the landscape.

**Qualify and tier:**
- Resolve each mention to a company and contact. For mentions with no linked record, infer the company from the snippet and mark it inferred.
- Look for negative words (unhappy, clunky, complex, expensive, hard to use, rigid, overkill) and replacement words (RFP, evaluating, contract expiring, looking at options, renewal).

| Tier | Meaning |
|---|---|
| HIGH | Unhappy, or actively replacing |
| MED | Replacement signals only |
| LOW | Neutral, aware, or locked in (note the lock-in end date, it becomes a future trigger) |

- One verbatim quote per account, one line.
- Roll recurring pains into 3 to 5 positioning angles (for example: ease of use, too heavy for simpler needs, poor external-user experience, cost of ownership, no product innovation).
- Build a landscape map: platform consolidators (span two or three product lines) versus point solutions, each verified on the vendor's own site. Consolidators are the most dangerous; point solutions compete on one axis.

**Outreach angle:** HIGH accounts go to outreach with the pain angle that matches their quote (never quote them back to themselves). LOW accounts with a contract end date get a calendar reminder 3 to 6 months before it.

**Extra suppression:** active deals and customers are excluded as usual; accounts mid-renewal with the competitor are LOW, not targets.

**Gotchas:**
- A note that says a past user disliked the tool is about a person, not the account. Check whether that person is still there.
- Some contacts are partners, consultants or former employees of the competitor. Tag them as referral or intel sources, not targets.

---

## 9. Post engagers

**Fires when:** someone likes, comments on or reshares a target LinkedIn post: the founder's, a competitor's, or an influencer's in the space.

**Data comes from:** a post-engagement scraper (Clay, Triggify, Apify or similar) given the post URLs. Pull engagement type with every row.

**Qualify and tier (expect a steep funnel; illustrative: 2,000 reactions, 1,300 unique people, about 250 send-ready):**
1. Dedupe to unique profiles BEFORE any paid enrichment. Quote the cost and get a yes for the run.
2. Function filter, then enrich profile and company, then location filter.
3. Emails through a waterfall (for example Blitz, then Prospeo).
4. Remove customers, partners, competitors and the user's own staff. Very senior people (founders, C-suite at target accounts) go to a "founder tier" file for the user to contact personally.
5. CRM check (read-only): anyone with real activity comes off.
6. Exclusion list; hold anyone already in a live campaign.
7. Title-by-title screen (sales, students, unrelated roles out). Remove government, utilities and unverifiable employers.
8. Full ICP recheck with one recorded rule per person. Apply the user's overrides and note them.
9. Channel routing: email only if the email domain matches the company; otherwise LinkedIn only.
10. Pilot 10 per campaign, diff against the file, then launch on an explicit go.

**Outreach angle:** light. Two touches, at least 5 days apart, plain text, no links. LinkedIn: if already connected, end with nothing sent; otherwise a blank connection request (withdrawn after 25 days), message after accept, second message 5 days later, InMail after 7 days if not accepted (skip if the sender has no Sales Navigator).

**Extra suppression:** channel-aware. An email bounce removes the email channel only; it does not block LinkedIn.

**Gotchas:**
- Citing the engagement ("saw you liked our post") is a judgement call and often against approved-template rules. Flag it and let the user decide.
- Liking a post is the weakest signal in this skill. On its own it is Tier 3; stacked with a fit account or another signal it can move up.

---

## 10. Founder and exec network

**Fires when:** the founder or an exec has a large LinkedIn network and nobody knows which of those people matter.

**Data comes from:** the LinkedIn connections export, matched read-only against the CRM, the sequencer(s) and the LinkedIn outreach tool.

**Qualify and tier:**
- Leave the original columns untouched; add one status column.
- Match people in order of confidence: LinkedIn slug identical (definitive), email identical (definitive), first and last name plus employer (strong), name only (weak, marked "name match only - verify").
- Match companies: exact after normalising, then token subset, then similarity of 0.90 or more. Spot-check the fuzzy ones.
- Write one plain-English remark per person, the most commercially important fact first, extras after a semicolon. Qualifiers only when true: email bounced, UNSUBSCRIBED, DO NOT CONTACT, connection accepted, name match only - verify.
- Colour-code:

| Colour | Meaning |
|---|---|
| Orange | Buying signal: act on these |
| Gold | Existing customer |
| Green | Open opportunity or positive reply |
| Red | Closed-lost or explicit no |
| Blue | Known, no strong signal |
| Grey | Net-new |

- Classify net-new people by segment to find the real ICP slice.

**Outreach angle:** orange goes to the founder personally, today. The net-new ICP slice gets a warm, founder-voice note (a shared connection is the honest hook). Known contacts follow their owner's lead.

**Extra suppression:** the catalogue reply rule applies: anyone who replied before is never sequenced, only handed to their owner.

**Gotchas:**
- "Replied" mostly does not mean interested. If the earlier outreach was an event or dinner invitation, most replies are RSVPs. Read the reply text and separate real buying signals (asked for a deck, proposed a time) from RSVPs and polite thanks. Expect only a handful of real ones.
- Many tool "replies" are bounces and out-of-office messages. Count human replies only.
- Big networks are usually two populations (the industry half, already in the CRM, and the friends-and-former-colleagues half). The useful net-new slice is often under 10% of the network. Say so plainly.

---

## 11. Website visitors (with speed-to-lead)

**Fires when:** an identified person or company visits the user's site, especially key pages, or more than once. Also every inbound form, demo request and download.

**Data comes from:** a visitor-identification tool (RB2B, Kwanzoo, Warmly, Vector or Fibbler), the site analytics, form tools, and the CRM.

**Qualify and route:**
1. **Split rows.** Person rows (a name, email or LinkedIn) continue. Company-only rows are an account signal, set aside, not deleted.
2. **Company ICP check** (keep / exclude / review) on company name and domain. Most visitor exports have no description field, so use pattern rules for the obvious non-fits (agencies, consultancies, staffing, universities, distributors, service providers in your buyers' world) and review the rest.
3. **Title filter**, then normalize names and check identity.
4. **CRM, exclusion and engagement checks.**
5. **Classify the account and route:**

| Account status | Action |
|---|---|
| Active customer | Slack alert to the account owner. No automated outreach |
| Active deal | Slack alert to the deal owner. No automated outreach; an SDR wading in mid-deal kills momentum |
| Named key account | Slack alert to the owner, who decides |
| New, person identified | Cadence chosen by the page bucket they viewed |
| New, company only, ICP fit | Pull 3 to 5 senior people in the target functions; generic cadence |

6. **Page buckets.** Group pages into 3 to 5 buckets (one per product line or audience, plus a general one). A visitor goes into the cadence for their bucket. Let the user mark pages not worth tracking.
7. **Alert threshold:** 2 or more page views (or one key-page visit) before an alert fires.

**Speed-to-lead (for hand-raisers):**
- Map the funnel and measure each step: form, notification, calendar shown, booked, held. Find the step where people drop.
- Offer direct calendar booking instead of a form-then-calendar handoff. Test it on half the traffic against the current flow.
- Follow-up SLA: 15 to 60 minutes for a hand-raiser, by LinkedIn and phone, not hours later by email.
- Slack alert to the owner on every inbound, tagged by territory or account owner.
- "Not yet" leads go to nurture, not the bin. Book-ready leads go to the AE.
- Check that the booked meeting keeps its original source (paid, organic, outbound) so attribution survives.

**Outreach angle:** never say "I saw you on our website". The creepy factor is high. Write to the problem their page bucket implies. A content link back to the relevant page is fine.

**Extra suppression:** key accounts are excluded from generic cadences unless the owner opts them into a gentle two-touch.

**Gotchas:**
- The visitor tool's "Website" field is often mis-attributed. Take the company domain from the work email first, then the website; check it against the company name. A free-mail address says nothing about the employer.
- Person-level matches are rare and spread out. Expect few, and value each one.
- Few people raise their hand. The visitor feed is how you reach the ones who don't, so it pays to wire it before buying more traffic.

---

## 12. Expansion and new office (lease)

**Fires when:** a company signs a lease, breaks ground, announces a new office, headquarters, store or restaurant, or completes a renovation, inside the window. Default window: the last 30 days for a monthly run; stretch to 60 to 120 days for a first pull or a quiet market.

**Why it converts:** once a company commits to a new physical footprint, it is already mid-decision on who fits it out, equips it, secures it, connects it or runs it. You are not creating a need; you arrive while the need is being sourced.

**Data comes from:** a web-scale search API (for example Exa, run from Claude Code or orchestrated in Deepline) over real-estate and trade press, local business news and press-release wires, for expansion language in a defined geography and date window. Ask the agent for the source with every hit.

**Find and parse:**
1. One run per segment (for example offices, retail, restaurants), so each segment gets its own copy.
2. Parse every hit into one row per company and location: company, segment, signal type (lease, new office, new HQ, opening, renovation), location, city, size (square footage) when given, announcement date, **source URL, source title and a one or two sentence summary** (the cited-source rule, engine section 8).

**Validate (drop with a reason):**
- Already open or occupied (the move is done; the buying window has closed).
- Outside the geography served.
- Entity mismatch: a same-named but different company, or a landlord or developer named instead of the tenant.
- Then the engine's exclusions and suppression (section 6).

**People:**
- Pull broadly per firm from a people database (for example Prospeo), then filter to the functions the event lands on: facilities, real estate, workplace, construction, procurement, and the C-suite or founder. Keep people in the event's country.
- Cap per firm (set with the user; this play allows a higher cap than the default 5, because several functions share the decision).
- Split into Leaders and Operators (engine section 7).
- Verify emails with an email finder and verifier, and top up gaps with a second provider. Where no email is found, leave it blank, keep the LinkedIn URL, and send that person down the LinkedIn track.
- Re-join every contact to their company's subject line and opener so each person row is complete.

**Outreach angle:**
- The opener always starts with "I saw on {publication} that..." and uses the source's own details: "I saw on {publication} that {Company} is opening a {size} {type} in {place} in {month}." Then one question about the decision being sourced right now ("Have you lined up {the thing you provide} for the new {type}?").
- Subject line: the company, the place and the decision, short ("{Company}'s {city} {type}: {topic} partner?").
- A shorter LinkedIn variant of the same line.
- Leaders get the timeline and outcome version; Operators get the spec and logistics version, from the same event.

**Activation (after `campaign-send-checklist`, never from this skill):** email cadence in the user's email tool (for example Email Bison), LinkedIn in their LinkedIn tool (for example HeyReach: connection request plus two or three follow-ups). Positive replies go straight to an AE alert with the lease signal attached (engine section 10).

**Gotchas:**
- The hard part is not the prompt; it is knowing which expansion events line up with a buying window for this offer. Pilot one segment and read the replies before adding more.
- Square footage and dates in press are often approximate. Quote them as the publication states them, never round them up.
- Never invent the publication. No source URL, no row.

---

## 13. Event attendees with a 90-day overlay

**Fires when:** someone from the ICP is confirmed as an attendee or speaker at an event relevant to the offer.

**Why it converts:** shared context beats cold context, and the event date gives a natural reason to write now. Cross-point: the full conference workflow (lists, dinner invites, on-site meetings) lives in `conference-outreach`.

**Steps:**
1. **Ingest** the attendee or speaker list.
2. **Cross-reference** each attendee's company against the ICP; then the engine's suppression.
3. **Hard validation:** drop the event's sponsor-tier companies (they are there to sell), anyone outside the geography served, and stale signals.
4. **Overlay a signal:** check each company's public activity in the last 90 days for anything relevant to the offer (expansion, hiring, funding, a launch).
5. **Branch:** attendees with a real hit get the signal-based version; everyone else gets an event-only version that is still personal, just lighter.

**Outreach angle:** a 3-email sequence and a matching 3-message LinkedIn sequence for both groups, written from two rotating sender personas so the same account does not hear an identical voice on email and LinkedIn.

**Gotchas:** never imply you met them or will see them unless that is true. Attendee lists go stale fast after the event; send before it, or within days after.

---

## 14. Lookalikes with an intent overlay

**Fires when:** never on its own. This play grows the list first, then lets a live signal decide who is touched now.

**Why it converts:** lookalike expansion alone gives a bigger list to spray. The overlay spends outreach only on the slice that is in market today.

**Steps:**
1. **Seed:** a list of best-fit existing or target accounts.
2. **Expand:** find firmographic lookalikes (same industry, size band and geography). List building itself is the `tam-list-builder` skill's job.
3. **Exclude:** competitors, channel partners, existing customers, then the engine's suppression.
4. **Overlay:** check every lookalike for a live expansion, hiring or funding signal in the last 90 days, validated with a source.
5. **Rank** only the accounts with a validated signal, by signal strength and recency (and the account score, engine section 5).

**Outreach angle:** the signal line for the signal it carries (use that signal's pipeline section for the opener).

**What happens to the rest:** expect only a small share of lookalikes to carry a validated signal. The rest are not discarded; they are held for the next signal pass and get no email this round. Outreach volume drops sharply while relevance goes up.
