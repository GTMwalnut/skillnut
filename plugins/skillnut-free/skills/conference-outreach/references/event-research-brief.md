# Event research brief and source playbook

Load this in Stage 3. It has two parts: a brief you hand to one research agent per event (fill the braces), and the source playbook that tells the agent where the people are, what is a dead end, and how to check its own work. Everything here came from running the play across about twenty conferences.

---

## Part 1: The brief (one agent, one event)

**Role and goal.** You are a GTM research agent for {SELLER} ({ONE-LINE PITCH}). Find, as completely as public sources allow: every session at {EVENT} (talks, keynotes, panels, workshops, side events), every company involved (sponsors, exhibitors, speakers' employers, side-event hosts, companies whose staff publicly attended), and every person involved (speakers, panelists, moderators, workshop leads, organisers and programme committee, people with public evidence of attending). Editions: {EDITIONS} (default: the most recent past edition and the upcoming one). Do not filter to a named-account list; capture everything and classify fit afterwards.

**Step 0: map before you scrape.**
1. List every edition, rename and regional spin-off. Events get renamed or move under a foundation, and searching only the old name misses the new editions.
2. Check whether {SELLER} itself sponsored, exhibited or spoke at any edition (search the sponsor page and the schedule for the company and product names). If yes, say so at the top of the summary: it changes the angle, and those contacts may already be worked.
3. Decide full or light mode (Part 2).

**Token discipline (cost rules).**
1. Pages go to disk, not into context. Write a small script that downloads a page, parses names, titles, companies and sessions, and appends rows to the CSVs. Print only counts and a few sample lines.
2. For pages that need a renderer, ask the scraper for only the fields you need (a JSON schema or a targeted query), never the full markdown of a big page.
3. Leave persona tier and company fit blank. A central classifier fills them from title rules and from every company already judged at other events, and forces the exclusion list. Judge by hand only the new companies it hands back.
4. Hard budget: about 60 tool calls per event (about 40 for a small one). If a source fails, try one alternative, note it, move on. Off-site search: about 25 searches at most, keeping only people at good-fit companies or clearly large end users.
5. Tool order: built-in search and fetch first; a scraping tool for rendered, paginated or empty pages; paid search APIs only when both fail, with the reason written down. Never start deep-research runs without asking.
6. Public pages only. No logins, no paywalls, no registration-gated attendee lists.

**What to capture** (UTF-8 CSV, fixed column order, one staging folder per event; never touch the master files, which a merge script builds):

| File | Columns |
|---|---|
| `sessions.csv` | event, year, edition, date (YYYY-MM-DD, the day of the session), time, track, session_type (keynote / talk / panel / workshop / lightning / side-event), title, abstract_summary (40 words max), speakers ("Name (Company)", semicolon-separated), session_url, relevance (High / Medium / Low), relevance_reason, topic_tags |
| `companies.csv` | event, years, editions, company, domain, hq_country, industry, est_employees, relationships (for example "Gold sponsor 2026; 3 speakers 2025; side-event host"), company_type, icp_fit (Strong / Possible / Weak / Competitor / Excluded), fit_reason, evidence_urls |
| `people.csv` | event, year, edition, full_name, title, company, linkedin_url, location, spoke, moderated, panelist, workshop_lead, organizer_or_committee, side_event_host, attended, posted_about_event, audience_participation, booth_or_sponsor_staff (each Y / N), session_title, evidence_url, evidence_snippet, persona_tier, icp_company_fit, outreach_reason, personalization_hook |
| `sources.txt` | every URL used, grouped by source type, what each yielded, what failed and why, every tool escalation |
| `summary.txt` | dates and location, counts by type, fit and tier, the top 10 people to contact first with one line each, the 3 to 5 sessions most useful as outreach hooks, the date to re-run the off-site search, and the self-audit result |

Use plain `.txt` for the notes when subagents can't create markdown files; don't work around that.

**Field rules.**
- `evidence_snippet` is a verbatim quote from the evidence page, never a paraphrase. Use the name exactly as written there.
- `attended = Y` only with direct evidence for an edition that has happened: their own post written during or after the event, a recap they wrote, a photo caption, hosting a side event at the venue, or speaking. A post written before the event ("excited to be at", "see you there") sets `posted_about_event = Y` and leaves `attended = Unknown`, even after the event has passed.
- Upcoming editions: scheduled speakers are `spoke = Y`; attendance stays Unknown.
- `linkedin_url` only when a search-result title shows the same name and the same company. Blank beats a guess.
- `outreach_reason`: one plain sentence joining persona, company fit and event engagement ("VP Platform at a US bank; moderated the 'agents in production' panel").
- `personalization_hook`: one factual line you could reference. Facts only, from the evidence.
- Do-not-contact companies and people: keep the row and flag it the same way every time (`icp_company_fit = Excluded`, and `outreach_reason` starts with "DO NOT CONTACT"). Never delete. The seller's own staff: keep, tier Non-target, flagged.
- People-finding only in this pass: no emails, no phone numbers.

**Relevance bands.** Write them for the seller, and keep High narrow. In one run, "any session on our topic" marked 57 percent of sessions High, which made the band useless. High = the session is about the exact problem the seller solves, in an organisation (for example governing, securing or running it at scale). Medium = building with the underlying technology, or the broad category. Low = everything else. A session that only mentions the topic is Medium.

**Persona tiers.** Copy the tier list from the user's ICP into the brief, with the edge titles settled in writing (for example whether a plain "Staff Engineer" is a senior individual contributor or below the line). Agents resolve unstated boundaries differently, and the merge then disagrees with itself.

**Self-audit before finishing (mandatory).** Re-open a random sample of at least 25 people rows (all rows if fewer), weighted to off-site sources, and confirm the name and the quoted snippet are on the cited page. Fix or delete failures and write the result into the summary. An independent audit then checks every row against its evidence page; rows that fail are removed from the master.

---

## Part 2: Source playbook

### Light mode
Sessions, speakers and sponsors only, with no off-site attendee search, for editions outside the seller's selling region and for very broad events (general AI or big-data expos) where off-site search returns mostly noise.

### What pays, in order

| Source | What it gives | How to pull it |
|---|---|---|
| Server-rendered schedule pages (sched-style "list descriptions" pages, foundation `/program/schedule/` pages) | Every session with speaker title and company in one fetch; about 80 percent of all people rows in practice | Raw HTML with a plain HTTP request (curl or requests), parsed by script. A summarising fetch tool truncates long lists and loses rows |
| Schedule data embedded in the page (Sessionize-backed foundation pages carry the full schedule as a JSON blob in a script tag) | Sessions, abstracts, speaker titles and companies, and **speaker-supplied LinkedIn URLs** | Same raw pull; parse the embedded JSON. Make it step 1 for any event built this way |
| Public "Who's attending" pages (organisation lists) | The best company-level attendee signal available (one event listed about 400 organisations) | Raw pull; a summarising fetch cuts it short |
| Sponsor grids | Sponsor names and tiers | Tiers live in logo images. A scraper's markdown keeps the logo alt-text and links; a plain fetch loses the tiers |
| Programme committee pages | A short list of named organisers | Plain fetch |
| Talk recordings (event YouTube playlists) | Past talk titles and speakers | A plain fetch of a watch page returns nothing; a scraper query on the page returns the description, which names the speaker with title and company |
| Side-event pages (Luma and similar) | Host companies and named speakers | Event pages only; guest lists and calendars are gated or empty |
| LinkedIn posts, found through search | Attendee signal outside the agenda | Search `site:linkedin.com/posts "<event>"` with terms like "attended", "day 1", "booth", "recap", then fetch the post for its text and author. Company posts tagging several colleagues are the richest |

### Dead ends (don't spend calls on these)
- Sched-style `/list`, `/speakers` and `/venue` pages go behind a login once an event ends. Pull them early. The `/directory` and per-event pages often stay public.
- The Wayback Machine usually has no copy of schedule-platform pages; it is still useful for an event's own old agenda and sponsor pages.
- LinkedIn profile pages rate-limit almost immediately, and scrapers refuse the domain. Find LinkedIn URLs through search-result titles, never by fetching profiles.
- Only zero to two commenters are visible per LinkedIn post, and a commenter isn't evidence anyway.
- Audience participation from recording transcripts: most transcripts are unavailable and nobody asking a question introduces themselves. Expect zero; spend at most a couple of searches.
- Pre-event "see you at" posts are sparse four weeks out. Re-run the off-site search about a week after the event, when the recaps appear.
- Vendor "events" pages are mostly stale shells after the event.
- Search tools on a scraping service rate-limit after about 20 calls in a burst; pace them.
- Paid search APIs were never needed when the steps above were followed.

### What the yield tells you
About 90 percent of the people who post about attending are vendors, developer relations or founders. Off-site search mainly adds sellers, not buyers, which is why it is capped and kept only for good-fit companies. The agenda is where the buyers are.

### Parser bugs look like fabrication
When the audit fails a row, check the parser before blaming the agent. Real failures from past runs:
- "Jane Doe, PhD - Talk title" split on the comma created a phantom co-presenter called "PhD", who inherited the wrong snippet. Strip credentials before splitting names.
- A cache lookup grabbed the wrong year's copy of a page, so correct rows "failed".
- A speaker tagline rendered by JavaScript was not in the raw HTML; the snippet must come from what the page actually serves.

Fix the script and re-run the whole event rather than patching rows by hand.
