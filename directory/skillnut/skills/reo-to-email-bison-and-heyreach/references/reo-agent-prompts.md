# Reo.dev agent prompt pack

Copy-paste prompts for Reo.dev agents, plus the setup ritual that turns each one into a weekly feed. Fill the `<placeholders>` from the user's ICP and rules file. Agents find accounts that have **no repo activity yet**, so they complement the batch pipeline. Credit prices below were correct when written; check Reo's current pricing before spending.

## 1. How agents and audiences fit together

| Thing | What it does | Cost (at time of writing) |
|---|---|---|
| Chat agent, "Enrich existing accounts" | Runs a prompt across one list or segment and tags matching accounts | Running the prompt is free. Credits only on **Enrich Now / Deploy**: 1 per matching account |
| Chat agent, "Discover new accounts" | Same, but searches outside your lists | 3 per new company, 1 per company already in Reo |
| Data source toggle | **Reo data** (hiring, tech, people) or **Public data** (news, filings, blogs) | none |
| Pre-built agents | New Key Hire, Champion Job Switch, Hiring for specific roles, Tech Stack Fit, Copilot | New Key Hire and Hiring for roles: 2 per find. Tech Stack Fit: free. Copilot: about 5 per find |
| Buyer / Developer Audience | Pulls named people (LinkedIn, email) at the accounts in a list, segment or company audience | 1 per person (LinkedIn only) or 2 (LinkedIn plus email). People already in Reo are free |

**Chat agents tag accounts, not people.** The person or job often appears in the agent's reason text, but the record is the tagged account. You get the people from an audience or a pre-built agent afterwards.

## 2. The setup ritual (every agent)

1. **Run the prompt (free).** Read the matches and tighten the prompt until they look right. Iterate here; it costs nothing.
2. **Enrich Now.** Give the agent a clear name and a tag (suggested tags below). Turn on the **weekly re-run**.
3. **Segment on the tag:** Segments, Create New, Basic, Account, filter Intel > Account Agent Tags > your tag. New matches flow in weekly.
4. **Automation:** on that segment, trigger "New Finds by Agents", send to Slack or email.
5. **Buyer Audience** on that segment to get the people (section 6).
6. **Route each match to its message** (the "Message route" line under each prompt).

**Run once across both tiers.** The scope picker takes one list or segment. Either run on Tier 1, then Deploy the same agent on Tier 2, or build one Basic account segment "Tier 1 + Tier 2" (Source > Lists > includes any of both) and point every agent at it.

## 3. Agent: job posts with your category keywords

**Why:** a job post is public, so the message can name it ("saw you're hiring a ... to build your ...").
**Setup:** Agents > Tech Role Hiring > Chat and Build > Enrich existing accounts > Tier 1 + Tier 2 > **Reo data**. Tag: `Hiring - <category> keywords`.

> Find companies in this list that have posted a job in the last 90 days whose job title or job description mentions any of these terms: <your category terms, in the words job posts actually use, for example "<category> gateway", "<category> platform", "<protocol name>">.
>
> Also match postings that name any of these tools: <your product, named competitors, adjacent tools buyers shortlist>.
>
> Focus on roles in <the functions that buy you, for example platform engineering, AI platform, developer productivity, SRE, cloud infrastructure, engineering leadership>. Ignore postings where <an ambiguous acronym> means something unrelated, and ignore sales, marketing, recruiting and customer-support roles.
>
> Rank the matches:
> 1. Highest: the posting names one of the tools above, or uses <your sharpest category phrases>.
> 2. Next: the posting pairs <your core platform term> with <your category> AND with <the pain you solve, for example governance, RBAC, audit, SSO or identity>.
> 3. Next: the posting mentions <your category> without naming a tool.
> 4. Lowest: generic <broad trend> language only.
>
> For each company, return the job title, posting date, job link, the exact phrase from the posting that matched, the team or function, the seniority, the location, and the rank.

**Cross-check for free:** deploy the pre-built **Tech Stack Fit** agent (tech stack = your category terms, job-post recency = 90 days).
**Message route:** one line per rank. Your own product named: skip awareness. A competitor named: their gap. A complementary tool named: "better together". No tool named: your strongest category line.

## 4. Agent: new hires in buyer seats

**Why:** someone new in a leadership seat is building a plan and choosing vendors in the first 90 days.

**Option A, pre-built (people-level, best):** Agent library > **New Key Hire** > Configure. Persona = your Buyers persona (build it first, section 6). Recency 90 days. Deploy on Tier 1 + Tier 2. Tag `New hire - buyer 90d`. Run **Champion Job Switch** with the same persona to catch people who left a target account for another.

**Option B, chat agent (more title control):** Chat and Build > Enrich existing accounts > **Reo data**.

> Find companies in this list where someone started a new role in the last 90 days in one of the titles below, or a close equivalent. Count it only if the start date in the new role falls in the last 90 days, either because they joined from another company or because they moved internally into this role. Do not count profile edits, work anniversaries or title tidy-ups.
>
> Executive buyers: <for example CTO, Chief AI Officer, SVP or VP of Engineering, VP of Platform Engineering, VP of Infrastructure>.
>
> Director-level champions: <for example Director or Head of Platform Engineering, Developer Productivity, Developer Experience, AI Platform, Infrastructure, SRE>.
>
> Senior engineers (only in <your teams>): <for example Distinguished Engineer, Fellow, Principal Engineer, Principal Architect, Senior Staff Engineer>.
>
> Exclude: <below-Staff engineers, functions that do not buy you, IT support, DevRel, sales, marketing, HR, finance, interns, contractors, consultants>.
>
> For each match return the person's name, new title, start date, previous company and title, whether they came from outside the company, location, and LinkedIn URL. List executive buyers first, then directors, then senior engineers.

**Check before sending:** profile-update dates cause false "new hires". **Spot-check 5 start dates on LinkedIn.** If they look noisy, use a people-data provider's job start date field instead.
**Message route:** a new-in-seat opener, not a signal quote ("congrats on the move to X; most leaders we talk to in their first quarter are working out ..."), plus the closest proof point for their vertical.

## 5. Agent: mergers and acquisitions (your account is the acquirer)

**Why:** an acquirer inherits a second engineering estate (second identity provider, second toolset). This tells you **when** to reach out, not **whether**; it is stronger stacked with a job post or repo activity.
**Setup:** Enrich existing accounts > **Public data** (Reo's hiring data will not see deals). Tag `M&A - acquirer 12m`. Monthly re-run is enough.

> Using news, press releases, regulatory filings and company blogs, find companies in this list that have announced, signed or completed an acquisition of another company, or a merger, in the last 12 months (on or after <date>). The company in this list must be the acquirer or the merging party, not the business being sold.
>
> Rank higher: the acquired company is a software, SaaS, AI, data or digital-platform business with its own engineering team; it builds <your adjacent category>; the deal was announced in the last 6 months or is still closing; the announcement mentions technology integration, platform consolidation, cloud migration or unifying systems.
>
> Include, but rank lower: acquisitions of non-software businesses.
>
> Exclude: divestitures where the company in this list is the seller, minority stakes, venture investments, joint ventures, and rumoured deals that were never announced.
>
> For each deal return: acquirer, acquired company, what it does, approximate headcount, deal value if disclosed, announcement date, close date or status, source link, and one line on the technology-integration angle.

**Message route:** name the deal (it is public). Lead with the "what do we even have now?" question and an audit-style offer.

**Optional fourth agent:** Public data, companies that publicly disclose deployments or risks in your category (earnings calls, annual reports, engineering blogs). Suits executive openers only.

## 6. Audiences: the people at matched accounts

**Step 1, personas first** (Settings > Configurations > Persona Configuration). Fields: Location, Seniority, Tech Functions, Tech Skills. "includes any of" is OR, "includes all of" is AND.
- **Buyers persona:** Director, VP, CXO (plus Head if listed). Functions: engineering leadership, platform, cloud, infrastructure, SRE, AI leadership. Leave out functions that do not start the conversation (often security). **Leave tech skills empty**: executives rarely list skills, so a skills filter deletes real buyers. Leave person location open or use your served regions.
- **Senior engineers persona:** Staff, Principal, Lead only. Functions as above plus backend. Skills: your core stack terms.

**Step 2, Buyer Audience** on the segment, persona Buyers, **Preview** (25 rows; read the titles), then save. **Max 3 buyers per company.** LinkedIn plus email. Auto-refresh on. Point the same persona at each agent segment to get, for example, "buyers at accounts posting relevant jobs".

**Step 3, Developer Audience** the same way with the Senior engineers persona. Max 3 per company (the cap goes to 20; don't use that).

**Step 4, keyword in title or profile.** Audiences have no free-text keyword filter on a person. Free route: save the audience, pull members read-only (`GET /audiences`, `GET /audiences/{id}/members`) or download the CSV, and filter titles locally. Paid route: the Copilot agent with a yes/no prompt, about 5 credits per find, which gets expensive across thousands of people.

**Credit check before you save** (illustrative): 3,000 accounts x 3 people x 2 credits = 18,000 credits per audience, minus people already in Reo (free). Start with Tier 1 only, read the quality, then extend.

**Step 5, suppress at export.** Reo does not apply your exclusions: never-contact list, competitors, open and Closed Won HubSpot deals, territory accounts another rep owns (agree ownership first), and wrong-fit titles. These people then go through the normal batch pipeline (Stages 5 to 12) like any Reo pull.
