# Event ROI and attendee intel (Option G)

Load this when the user picks Option G. Three read-only analyses that decide which events deserve next year's budget and who to work at them:

1. **Event ROI scorecard:** which events produced pipeline and revenue, from the CRM.
2. **Invite outcomes:** how dinner or meeting invites at past events performed, by event, title and company size.
3. **Attendee lists year over year:** who is returning, who is new, sorted and sized, ready for outreach.

All CRM access is read-only. Every call is described to the user before it runs.

## 1. Event ROI scorecard

### Steps

1. **Discover the schema.** List deal, contact and company properties and the deal pipelines. Find the field that records which event a deal came from (an "event source" or "conference source" property). If none exists, say so: the scorecard cannot be built honestly without it.
2. **Pull every deal with that field set** (paginate), with name, stage, amount, create and close dates, and the free-text fields (description, pain, goals, use case).
3. **Pull associations:** contacts, companies and notes per deal.
4. **Pull stage history** per deal (in HubSpot, `propertiesWithHistory=dealstage`) so you can see how far each deal got, not only where it sits now. Map stage ids to readable names.
5. **Classify:**
   - Company size by revenue: Small under $100M, Medium $100M to $1B, Large over $1B.
   - Titles into function groups and seniority (C-suite, VP, Director, Manager, individual contributor).
6. **Build the scorecard per event:** deals created, pipeline value, win rate, furthest stage reached (a waterfall of how many reached each stage), seniority mix, industry mix.
7. **Find repeat companies:** accounts that show up across two or more events.
8. **Read the notes** for recurring themes: the top market signals and specific opportunities, in the prospects' words.

### Output

An 8-tab workbook (scorecard, company profiles, job titles, seniority by event, pipeline progression, notes and themes, raw deals, industry by event) and, if wanted, a short branded deck (about 12 slides: headline metrics, event ranking, funnel, stage waterfall, size split, industry, repeat companies, title split, titles by event, market signals, opportunities, recommendations).

## 2. Invite outcomes (dinners and meetings)

Per event: invited, accepted, declined, no response; response rate; acceptance rate of those invited and of those who responded. Then accepted invitees by title level and by company size, and the cross-tab of the two.

What this analysis usually shows (check it holds for the user's data before saying it):

- **Non-response is the biggest problem**, often most invitees. Once people answer, a good share accept.
- **Small, targeted invite lists beat big ones.** A short list of the right people can see close to half accept; a broad list of a hundred can see a handful.
- **Senior directors and heads of function** are the sweet spot at large companies: senior enough to decide, close enough to the work to value the conversation.
- **Location matters.** An event far from where the invitees are based can return zero acceptances.

Recommendations to test: smaller lists, earlier invites, a second channel (LinkedIn or a call) for non-responders, and invites written for the person.

## 3. Attendee lists year over year

### Steps

1. **Combine each year's exports.** Organisers often ship several sheets per year (one with emails and permissions, one with names only). Merge them and de-duplicate per year.
2. **Match the years three ways and report all three:**

| Method | Logic | Use for |
|---|---|---|
| A: first + last name | Case-insensitive, trimmed | First-timers (most complete; catches people who changed company) |
| B: email | Exact | A reliability check (many rows have no email) |
| C: first + last + organisation | Strict | Returning attendees, when you need confidence they are still at the same company |

   Strict matching misses people whose organisation is spelled differently between years ("Acme Corp" one year, "Acme Corporation" the next). Report how many that is.
3. **Categorise organisations:** buyer companies (with sub-types that matter to the user), agencies and service firms, vendors and publishers, competitors, associations and other, and your own company. Size the buyers (for example, "large" = the top 20 in the category by revenue, plus their major subsidiaries).
4. **Enrich:** LinkedIn URL, work email and domain (a table tool, then an email-from-LinkedIn lookup for the gaps). **Remove personal and free-mail addresses.** Fix malformed URLs (stray brackets).
5. **QA:** row counts against the source, URL format, email domain against the organisation's domain.

### What it tells you

- Turnover is usually heavy; often more than half of this year's attendees are first-timers. First-timers are a fresh list every year.
- Returning attendees skew toward larger companies; a company sending many first-timers is a new delegation worth noting.
- Competitors and agencies show up too; tag them, do not prospect them.

### Output

Two outreach-ready files (returning, strict match; first-timers in the buyer category, with sub-category, size, domain and email) and a short process note with the match counts, enrichment hits and data gaps (for example, email coverage around 70 percent).

Hand the files to Options A or E for the invite or outreach.

## Model narration (illustrative numbers only)

> ROI: 250 deals carry an event source across 12 events. Two events produced 60 percent of pipeline; one large event produced 40 deals but none past the second stage. 18 companies show up at three or more events.
> Invites: 140 invites across four events, 14 accepted, most never answered. The 15-person list accepted at 45 percent; the 100-person list at 4 percent.
> Attendees: 600 this year, 580 last year. Returning by name 200, by strict match 170 (30 lost to company-name variants). 400 first-timers, 150 at buyer companies.
