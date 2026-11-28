# Website-visit attribution (Option C)

Load this when the user picks Option C. It answers one question: **did our cold email and LinkedIn touches lead to identified visits on our website?** It uses a website visitor-ID tool (RB2B or similar) as the "visit" side, and the email and LinkedIn tools as the "touch" side. Read-only throughout.

## What you need

| Input | What it is | Notes |
|---|---|---|
| Visitor-ID export | A CSV from RB2B (or similar) covering the window. One row per identified visitor, with a profile type (Person or Company), name, work email, LinkedIn URL, company name, first-seen and last-seen dates | Person rows name an individual. Company rows mean the tool only resolved the company |
| Cold-email tool | Email Bison (or similar), read access by API | Needs per-send dates, not one date per lead |
| LinkedIn tool | HeyReach (or similar), REST key and, if they have it, the MCP connection | The MCP sees individual messages that REST does not |
| Window | The period to test | Default: rolling 90 days, confirmed with the user |

Keys live in one file and are referenced by name only. Never print them.

## Step 1: Pick the window and check the export really matches it

Do not trust a file name or a "people" vs "companies" label. Check three things before you use the file:

| Check | Why |
|---|---|
| Profile-type mix | A "people" file can still mix Person and Company rows |
| Min and max of last-seen date | This is the file's real lookback window, which may not match its label |
| Row overlap with any other export (on LinkedIn URL) | If one file is a strict subset of another, they are the same report at two date cuts, not two entity types |

Say what you found in one line: *"The 'people' export covers 64 days, not 90, and 30 percent of its rows are company-only. I'll use the other file, which covers the full window."*

## Step 2: Pull every email send, not one row per lead

- List all campaigns, then all leads per campaign (paginated).
- For each candidate lead, pull **every email sent to that lead**, each with its own send date and sequence step. In Email Bison this is the per-lead sent-emails endpoint. A lead can have the first email plus several follow-ups, and each is a separate touch.
- **Cost control:** do not pull per-lead sends for the whole account (it can be thousands of leads). Pre-filter to leads whose email domain or company plausibly overlaps the visitor export, then pull detail only for that set.
- **True volume for the window:** use the campaign stats call with a start and end date (in Email Bison, the per-campaign stats endpoint takes a date range and returns emails sent and leads contacted for exactly that window). One call per campaign is much cheaper than counting leads, and it gives you the real denominator.
- A LinkedIn URL in the email tool's custom fields is very often the **company** page, not the person. Do not treat it as a person-level key.

## Step 3: Pull LinkedIn touches (REST alone under-counts)

| Source | What it gives | Use it for |
|---|---|---|
| REST campaign and lead lists | A status snapshot per lead with one last-action date | Fallback only. It collapses every touch into one date and cannot see follow-ups |
| MCP conversations (HeyReach `get_conversations_v2`) | Every message in every thread, each with a date, a sender (you or them) and an InMail flag | The real per-touch list. Keep messages sent by you, inside the window |
| MCP overall stats with a date range | Daily totals: requests, messages, InMails, replies, acceptances | Sanity-check your rebuilt touch count and get true top-line volume |
| MCP campaign sequence | Which step types a campaign uses | Knowing what you should expect to see |

Two gaps to disclose, not chase:
- **InMail cannot be tracked per lead.** InMails show up only as a daily total in the stats. They do not appear in conversation threads at all. Say so plainly and do not count them per person.
- **Connection request with no thread yet:** use the snapshot's last-action date as a single touch, and tag it approximate.

## Step 4: Normalize, then match

Normalize first:

| Field | Rule |
|---|---|
| Email | Lowercase, trim |
| LinkedIn URL | Strip protocol, `www.`, trailing slash and query string |
| Company name | Strip legal suffixes (Inc, LLC, Ltd, Corp, Co, Group, Holdings) and punctuation |

Then match in two tiers:

| Tier | When it counts | Strength |
|---|---|---|
| Person level | The visitor row is a **Person** row, and its work email or personal LinkedIn URL (`/in/...`) exactly matches a touched contact | Strong |
| Company level (fallback) | Company-name text match, or a domain taken from **the touched contact's own work email** | Weaker |

Rules that prevent false positives:
- A `/company/...` LinkedIn URL match is company level, never person level, even if the strings match.
- **Never match on the visitor tool's own website field.** It is sometimes attributed to the wrong company by the tool itself (a small agency's row listed with a big brand's domain, for example). If any domain match looks odd, check it against the row's company name, and when in doubt drop website-field matching completely.

## Step 5: Compute the timing signals

For each matched person or company, look at **all** their touches in the window, not just the latest.

| Signal | Definition | How to read it |
|---|---|---|
| New visitor after touch | First-seen date (their first identified visit ever) falls on or after the nearest earlier touch | Strongest. Same day or next day is compelling. Within about 7 days is strong. 28 to 60 days is reported but flagged weak. Past about 30 days, do not claim cause |
| Return visit after touch | Last-seen date falls after their most recent touch | Weaker. It could be normal repeat traffic, but it is directionally useful |

Known limit: the export only has first-seen and last-seen per visitor, not a log of every page view. If a company had many visits and many touches, you cannot pin a visit to one specific follow-up. Treat that level of detail as directional.

## Step 6: Report honestly, including the negatives

- **State the true denominators first:** campaigns, leads contacted and touches in the window from both tools. A small matched count without its denominator looks like a high percentage when it is not.
- **If the person-level match count is zero, say so.** It is a real finding. Visitor-ID tools identify a small slice of traffic, and the exact person you contacted turning up is rare.
- **Name the gaps:** InMail per lead, the single first-seen and last-seen dates, and any file-window mismatch from Step 1.
- Share findings with the user for review before producing any CSV export.

Example report (illustrative numbers only):

> In the 90-day window you contacted 2,400 people by email (7,100 sends) and 900 on LinkedIn (1,600 messages, plus about 120 InMails that can only be counted as a total). The visitor tool identified 380 visitors. Person-level matches: 3, two of them first visits within 2 days of an email follow-up (strong). Company-level matches: 41 companies, 12 of them new visitors within 7 days of a touch, 9 more between 28 and 60 days (weak). Gaps: InMail cannot be tied to a person; visit dates are first and last only.

## Files a run produces

| File | Purpose |
|---|---|
| Email campaigns and leads | Full pull from the email tool |
| Email touches | Per-send events, in window, for candidate leads only |
| Email window stats | True date-filtered volume per campaign |
| LinkedIn campaigns and leads | REST snapshot |
| LinkedIn conversations and messages | Full message history via MCP |
| LinkedIn touches | Real messages plus connection-request fallbacks, in window |
| Visitor export (slim) | Normalized visitor rows used for matching |
| Match results | One row per match, with tier and timing signals |

To refresh for a new period, re-run Steps 1 to 6 with a new export and window.
