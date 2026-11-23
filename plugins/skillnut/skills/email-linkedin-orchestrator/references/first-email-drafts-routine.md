# First-email drafts: the email half of the orchestration

The LinkedIn bridge handles the LinkedIn step. This file covers the step before it: the rep's **first email of a cadence**, written by Claude and waiting in the email tool when the rep opens the task. The rep reviews, edits and sends. Nothing is sent automatically.

Built and tested with Salesloft, HubSpot, Clay and Claude Code scheduled tasks ("routines") in the reference build (Client C, November 2026). Anything not marked **verified** must be tested read-only first.

## Why it is built this way

- **No API edits a task's email draft.** Salesloft has no endpoint to change the email inside a manual email task. So the draft lives in two **person custom fields**, and the step's template merges them in.
- **Writing is judgment work.** Research, hook choice and wording vary per person, so a Claude routine fits better than fixed n8n steps. Volume is small (a rep has a handful to a few dozen Day 1 tasks a day).
- **The rep stays in the email tool.** No Slack, no review page, no extra tool. The draft is simply there when the task is opened. Owners in the reference build were firm: reps already juggle too many tools.

## Setup

### 1. Two person fields in the email tool

| Field (exact name) | Object | Type |
|---|---|---|
| AI First Email Subject | Person | Text |
| AI First Email Body | Person | Text |

**Verified:** a 1,040-character body saved in full with line breaks kept.

Recommended third field: **AI First Email Status** (Text). The routine writes "Drafted" or the skip reason. Without it, an hourly routine re-researches every skipped person every hour, and the rep can't see why a task is blank.

### 2. The Day 1 template

Subject: `{{AI First Email Subject}}`

Body:
```
Hello {{first_name}},

{{AI First Email Body}}
```

Tips from the build:
- Salesloft's `{}` dynamic-field button always inserts into the **body**. To get a tag into the subject, insert it in the body, then cut and paste it into the Subject box, or type it.
- Don't use the tool's own "Draft with AI" or "Convert to AI dynamic email"; they replace this setup.
- The template is often a **shared team template**. Everyone on that step gets the merged fields; a rep the routine doesn't cover sees a blank subject and body. Check who has tasks on the step (group open actions by `user.id`) and get the template owner's OK before changing it.

### 3. The routine (Claude Code scheduled task)

One routine per rep, created in claude.ai/code on the client's Claude account.

| Setting | Value |
|---|---|
| Schedule | Hourly in working hours, offset per rep (e.g. :07 and :37), `CRON_TZ=<team zone> 7 7-17 * * 1-5`. Minimum interval is one hour. |
| Environment | Network access limited to the APIs it needs (`api.salesloft.com`, `api.clay.com`). Keys as **network secrets** bound to their host (Salesloft `Authorization: Bearer`, Clay header `clay-api-key` with no prefix). Never environment variables, never pasted in chat. |
| Connectors | CRM (HubSpot) for lifecycle, deals and duplicates. Add only what the prompt uses; leave Slack off for rep-facing work. |
| Notifications | Off. The run's own session holds the report. |

**Verified:** a Claude Code session with no repository reached Salesloft through the network secret (`/me`, the action listing, and a same-value write all returned 200).

Lessons:
- **Connectors must be added to each routine** on the Schedule page. Being connected on the account isn't enough.
- **New secrets and allowed domains only reach new sessions.**
- **Routines created through Claude's own tools may not show on the Schedule page until they have a schedule.** Give them one and pause them to keep them as drafts.
- There is **no confirmed webhook** that lets the email tool start a routine, so it polls hourly.
- Each run uses the account owner's Claude subscription, can come out slightly differently, and has no built-in retry: the next run picks up what failed.

## What each run does

0. **Check the fields exist.** If they don't, read only and report. Never try other fields.
1. **Find tasks.** Page through `GET /v2/actions?type=email&per_page=100`. Keep actions that are `due: true`, whose `user.id` is the rep, and whose `step.id` is one of the Day 1 steps. The `user_id` filter is ignored on this endpoint; filter client-side.
2. **Load each person** (cap about 25 per run). Skip anyone whose body field (or status field) is already filled.
3. **Checks, in order; stop at the first skip:**
   - **Contact in the CRM.** Open the contact from the email tool's CRM link and search for duplicates by name. Skip if lifecycle is Opportunity, Customer or Evangelist, or lead status is an active one (e.g. Working).
   - **Company in the CRM.** Skip if it is a customer or has an open deal.
   - **Still at the company?** LinkedIn URL from the email tool, then the CRM, then an enrichment search (Clay people search: full name plus current role at the company; if nothing, name only, with a hyphen-free surname). Skip as "left the company" and report the new company and title.
   - **Save the LinkedIn URL** to the email tool when it was empty, only for people who passed every check, never overwriting one.
4. **Research.** Career history, overlap with existing customers (a past employer that is a customer is a strong hook), hooks with source, date and High/Medium/Low confidence, and anything to avoid.
5. **Write** with the rep's own method (see below). One version per usable hook; pick the best.
6. **Save** subject and body to the two fields, then **read them back** to confirm. No High or Medium hook, or an avoid signal present: save nothing and record the reason.
7. **Report** in the run: drafts, skips grouped by reason, URLs saved, enrichment credits used.

The routine **never** sends, completes or skips a task, changes the CRM or the enrichment tool, or messages anyone.

**Reference dry run:** of 7 due contacts, 6 at one account were skipped for an open deal on that account, and 1 had left the company two years earlier (only the CRM's duplicate record and the enrichment search showed it). Those two findings are why the contact check and the still-at-company check exist.

## The rep's writing method

Ask the rep for the instructions they already use (often a Claude Project they paste name, company and title into). Paste the full text into the routine. Typical rules worth keeping explicit in the prompt:
- High-confidence hook first, Medium only if there is no High, never Low alone.
- Subject 3 to 7 words, about the hook or the pain, never the product or company name.
- Opener 3 to 4 sentences, under 80 words: hook, bridge, relevance, ask for interest (not a meeting).
- Peer-to-peer voice; banned phrases listed.
- Never invent facts, metrics, customer names or quotes. Name a customer only if the CRM confirms it, and never claim which product a customer uses.
- No greeting or sign-off (the template adds the greeting); plain text, no links.

If the rep has no method yet, the step's own template instructions are a fallback (in the reference build: take the account brief's confident "why now" signal and outreach angle, tighten to 2 to 3 sentences, end on a real question; no strong signal means start on a later touch instead of writing something generic).

## How it connects to the LinkedIn bridge

- The two automations act on **different tasks** (Day 1 email vs the LinkedIn step around day 3) and don't depend on each other. With a static LinkedIn message, nothing the routine writes needs to reach the LinkedIn tool.
- **LinkedIn URL handoff:** the routine saves the URL on day 1; the bridge reads the email tool first, so it uses that URL and rarely needs the paid enrichment waterfall.
- **Keep it in n8n:** the bridge's steps are fixed, rate-limited and need waits; moving them into a routine adds variance and more keys for no gain. A routine-to-n8n webhook adds nothing either, because LinkedIn steps come due on their own schedule.

## Known gaps to close

| Gap | Effect | Fix |
|---|---|---|
| The bridge doesn't share the routine's CRM skips (open deal, customer, active lead status) | If the rep sends Day 1 anyway, the bridge still adds them to LinkedIn on the LinkedIn step | Add the same CRM deal/lifecycle check to the bridge and hold like a job change, or have the rep remove skipped people from the cadence |
| Draft fields are never cleared | A person re-added to the cadence later is skipped by the routine and gets the old email merged in | When the bridge completes the LinkedIn task (Day 1 has been sent by then), clear both fields |
| No status field | Skipped people are re-researched every hour | Add AI First Email Status and skip on it |
| Shared template | Other reps on the step get blank emails | Confirm who uses the step; get the owner's OK |

## Giving one Claude both halves (optional)

If the routines live on the client's Claude account and n8n on the agency's:
- Never connect the agency's own n8n login to the client's Claude. n8n MCP access is per workflow but not per client, so every MCP-enabled workflow (other clients' too) would be visible. In the reference build all 46 workflows were MCP-enabled.
- Instead: a team project holding only that client's workflows, a separate n8n user who is a member of that project only, and the n8n MCP connector on the client's Claude signed in as that user. Non-Enterprise n8n API keys can't be scoped, so use the MCP connector or a single-purpose webhook, never a full API key.
- Keep one shared notes file (a small private repo attached to the client's Claude Code sessions) describing both halves, so both Claudes work from the same facts.
