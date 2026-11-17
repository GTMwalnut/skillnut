# Won-deal analysis through the CRM connector (option W)

Load this when the user picks W, or when a CRM connector is live and the context layer needs the won deals. It covers five steps in order: connect, ask, pull, segment, then turn the patterns into the next list.

Why this exists: most teams build their first lists on guesses. Their own CRM already holds the best answer to "who responds to us": the deals they won. Start there and work backwards to the list, instead of starting from a database's filter form.

## 1. Connect, read-only

- The CRM is reached through its connector (an MCP server for Attio, HubSpot, Salesforce, Pipedrive or similar). Confirm it with one identity call (who am I, which workspace, access level) and say what came back.
- This whole analysis only reads. Nothing in the CRM changes unless the user names the change and says go (see step 4).
- No connector: ask for a CSV export of won deals with their company and contact columns. Everything below still works except the live title back-fill.
- Never print API keys or tokens, even if a config file holding them is open.

## 2. Ask the clarifying questions first, then wait

Ask these in one message before pulling anything. A wrong won stage or the wrong size buckets means the whole report gets thrown away, and the user loses trust in the method.

| # | Question | Why it matters | Default if they shrug |
|---|---|---|---|
| 1 | What is the "won" stage called in your pipeline? Or should I list the pipeline stages first and you point at it? | Stage names differ in every CRM ("Closed Won", "Won", "Converted") | List the stages and ask |
| 2 | Which time window: all won deals ever, or a recent window such as the last 6 or 12 months? | Old wins can describe a company you no longer are | All-time, with a note to re-run on a recent window |
| 3 | Size buckets: should I use my default bands, or do you already have a size field or categories? Employees or revenue? | Your own bands make the report comparable with your plans | Small 1 to 50, Mid-market 51 to 1,000, Enterprise 1,000+ employees |
| 4 | How fine should geography be: regions (North America, Europe, APAC) or countries? | Too fine and every cell holds one deal | Regions, with countries listed under any region that dominates |
| 5 | Where is the deal source or lead source recorded, and is it filled in? | Source is often a free-text field or missing | Use the source field as is; flag the blanks |
| 6 | Will this report be shared or recorded? If so, should I hide company names and show only shares, not counts? | Lets the report be shown on a screen or sent around safely | Hide names, show shares |
| 7 | Anything I should leave out (test deals, partner deals, internal accounts)? | Keeps the shares honest | Ask once, then proceed |

Questions 1 to 4 come from the real run; 5 to 7 are the gaps that run exposed. Play back the answers in one line, then pull.

## 3. Pull and segment

**Pull:** the won deals in the window, then their companies and their people (in parallel where the connector allows). Count what came in and say it.

**Two denominators, always.** Where a field is missing on some deals, show each share two ways: "% of deals where this is known" and "% of all deals", with an "Unknown / not enriched" row. A pattern built on the half of deals that happen to have a title is not the same as a pattern across all deals; showing both makes that visible.

**Read the fields before trusting them.**
- Industry is often a catch-all: check the top accounts in each industry by name and correct the vertical before quoting it.
- Renewals, support and other installed-base deals can swamp the count. Report net-new product wins separately, and note when a few large accounts make up much of the total.
- Buyers are rarely titled by the problem you solve. If solution words barely appear in won titles, build title filters from role and function plus seniority, not from product words.

**Merge the tail.** Sources or regions that each hold only a deal or two are merged into "Other (n sources, each under the threshold)", so the table shows the pattern, not the noise.

Report in this order, each section with a table, one key takeaway, and a data-gap line:

| # | Section | What it shows | Feeds which targeting field |
|---|---|---|---|
| 1 | Lead source / channel | Share of won deals by source category (partnership, community, referral, outbound, inbound, paid, events) | Which channel the next motion leans on; a source that wins is a source to feed |
| 2 | Company size | Share of wins by size band, on the agreed buckets (employees or revenue) | Employee and revenue bands |
| 3 | Geography | Share of wins by region or country, by the company's location | Company location filter |
| 4 | Buyer titles | Share of wins by title group of the primary contact: C-suite and founders, VP and Director, Manager and below | Titles and seniority |
| 5 | Customer stage | Whether each customer was before or after product-market fit when it bought (or, for buyers that are not startups, how established the business was) | Company stage filters such as funding stage, founding year or headcount growth |
| 6 | Summary | The few patterns that hold across sections, and the gaps that limit them | The "next list" block below |

Read sparse sections as directional and say so. A segment that only ever produces small deals is a deprioritize signal, not a cut.

## 4. Back-fill missing titles before trusting section 4

Title is the field most often blank on deals. Fill it before the title section counts:

1. List the deal contacts with no title (and deals with no contact at all; those are a separate gap).
2. Read each contact's record through the CRM's API for an email address or a LinkedIn URL.
3. Reverse-look-up the person: LinkedIn profile or an enrichment tool (email-to-person or LinkedIn-to-person) for current title and seniority.
4. Mark each back-filled title "back-filled, current title" in the report: the title today may not be the title when they bought, and a person who has since changed companies is noted, not counted as the buyer's title.
5. Re-run section 4 with the back-filled titles and show the before and after.
6. Writing the titles back to the CRM is a separate step: show the list of records and fields, and write only when the user says go. Fill empty fields only; never overwrite a title someone entered.

## 5. Turn the patterns into the next list

Close with a "next list" block, one line per field, each with the section it came from:

| Field | Value | From |
|---|---|---|
| Company size | the band(s) holding most wins | Section 2 |
| Location | the leading region(s), in order | Section 3 |
| Titles and seniority | the title groups that close | Section 4 (after back-fill) |
| Company stage | the stage most buyers were at | Section 5 |
| Channel | the source(s) that win, and how to feed them | Section 1 |
| Gaps to fix first | the fields too thin to trust | Data-gap lines |

These values go straight into the targeting spec (Section B of the ICP document) and into whatever database builds the next list (Prospeo, Apollo, Clay or another). The next steps are building the list itself (a tight, in-motion list, or the whole market) and checking who already sits in the CRM before sending.

Close with the habit: re-run the same analysis each quarter on the same buckets and compare. The ICP should move when the wins move.
