# Whole-client pause and customer blacklisting (Part 9.3 and 9.4)

Load this when the owner says "we're pausing everything for `<Client>`", "the client is on hold", or "this prospect is actually a customer, block them". Both are one-command account controls that Claude runs with the owner, step by step. Neither is an automation that runs on its own.

Both make changes in a client's live tools, so the working rules in Part 11.9 apply in full: dry-run list first, an explicit yes for every write, read back after every write, and keys only by name.

---

## Part A: pause a whole client

### When

A client engagement goes on hold, ends, or needs a hard stop (a contract question, a deliverability scare, an off-boarding). The aim is that **nothing goes out and nothing runs** for that client, and that resuming later is a checklist, not an investigation.

### Step 1. Inventory everything that is live

Make one table, per tool, of everything that can send or run for this client:

| Where | What to list |
|---|---|
| Email Bison | Every campaign with its status (active, paused, draft, completed) |
| HeyReach | Every campaign with its status (`IN_PROGRESS`, paused, draft) |
| n8n | Every workflow for the client, including classifier sub-workflows, the daily sweep and conflict check, CRM syncs, and any leftover `TEMP` workflow |
| Scheduled cloud routines | Any Claude routine that reads or writes for this client (daily reply log, dashboard refresh) |
| Shared routines and dashboards | Cross-client jobs (for example a deliverability dashboard or inbox rotation) that include this client's workspace |
| Anything else scheduled | Scheduled sends, CRM workflows, webhooks pointing at n8n |

Record which items were **already paused before today**. They must stay paused when the client resumes (a test campaign, for example).

### Step 2. Show the dry-run list and get a yes

Show the owner exactly what will be paused, by name and id, and what will be left alone and why. Nothing changes until they say go.

### Step 3. Pause the campaigns

| Tool | Call |
|---|---|
| HeyReach | `POST /api/public/campaign/Pause?campaignId=<id>` for each in-progress campaign |
| Email Bison | `PATCH /api/campaigns/{id}/pause` for each active campaign |

Pause campaigns first, so nothing sends while you work through the rest.

### Step 4. Switch off the automations

- **n8n:** unpublish the client's workflows. Unpublish the workflows that receive webhooks and call others first, then the sub-workflows they call. Leave `TEMP` workflows off (or archive them).
- **Cloud routines:** disable the client's own routines.
- **Shared routines:** do not disable a routine that serves other clients. Instead take this client out of its scope (for example freeze the client's workspace in the shared dashboard, so it shows its last snapshot and is no longer refreshed or rotated).

### Step 5. Read everything back

Re-list campaigns in both tools and confirm each one reads paused; confirm each n8n workflow is unpublished; confirm each routine reads disabled. A 200 response is not proof.

### Step 6. Write the resume plan

Save a short note (in the client reference block, Appendix A) with:

- the date and who asked for the pause;
- every id that was paused, by tool, and the ones that were already paused before (stay paused);
- the order to resume: **re-enable n8n sub-workflows before the workflows that call them**, then the routines, then the campaigns last, after a read-only check that suppression and stops are still current;
- what the pause did **not** handle, so nobody assumes it did: LinkedIn connection requests already pending, inbox warm-up (usually left on so the mailboxes stay healthy), workflows in other tools (CRM syncs, enrichment tools), and tool billing.

While the client is paused, do not run their recurring analyses or syncs unless the owner asks.

---

## Part B: blacklist a customer, at company and lead level

### When

A prospect turns out to be a customer (often you learn it from their reply), or the owner names a company that must never be contacted. The owner's point that matters most: **block the individual people, not only the company.** A company entry can miss people whose company name is spelled differently.

### Why the domain block is right here (and wrong in Company Pause)

Company Pause (9.1) stops colleagues one by one and avoids the domain blocklist, because a pause is temporary and a domain block is global and hard to undo. A customer block is meant to be permanent, so the company-level block is exactly what you want, together with the per-lead block.

### Step 1. Find the company's people in both tools

- **Email Bison:** `GET /api/leads?search=<domain>`, paging through `meta.last_page` (the page is 15 leads). Also search the company name, since some leads carry a different email domain.
- **HeyReach:** there is no company search across leads. List every list with `POST /list/GetAll`, then read each with `POST /list/GetLeadsFromList {listId, offset, limit:1000}` and match on `companyName`.

### Step 2. Check sister brands and false lookalikes

Before blocking, ask two questions and show the answers to the owner:

| Question | Example (invented) | Action |
|---|---|---|
| Does the same customer own other brands or domains? | Acme Analytics and its sister brand Northwind Data, two domains, one customer | Block both, with the owner's yes |
| Is there a different company with a confusingly similar name? | Acme Analytics Services Inc., unrelated | Do **not** block; note it so nobody blocks it later |

Shared parent email domains and name tokens create false matches in both directions. Read every matched row.

### Step 3. Blacklist (needs an explicit yes; Part 11.9 rule 12)

| Tool | Company level | Lead level |
|---|---|---|
| Email Bison | `POST /api/blacklisted-domains {"domain": "<domain>"}` | `POST /api/blacklisted-emails {"email": "<email>"}` for each person |
| HeyReach | `POST /blacklist/AddCompanies {"companies":[{"name": "<name>"}]}` or `{"url": "<company page>"}`. A name entry is a broad match | `POST /blacklist/AddLeads {"leads":[{"profileUrl": "..."}]}`; an entry can carry `linkedInProfileId`, `email` or `fullName` instead |

The HeyReach company and lead blacklist endpoints were found by probing (send `{}` and read the error; see 9.2). Treat any new field as unverified until a read-back confirms it.

### Step 4. Stop anyone already in a live sequence

A blacklist protects future uploads. People already mid-sequence also need a stop: Bison `stop-future-emails` in every `in_sequence` campaign, HeyReach `StopLeadInCampaign` for active leads (Pending leads cannot be stopped by API; the lead blacklist covers them). Same method as 13.5.

### Step 5. Read back

`GET /api/blacklisted-domains` and `GET /api/blacklisted-emails` on Bison; `POST /blacklist/GetCompanies` and `POST /blacklist/GetLeads {offset, limit}` on HeyReach. Confirm every entry is there, then add the company and its sister brands to the client's reference block as "customer, blacklisted on `<date>`".

### Keys

Use the client's credential by name. **Never print a keys file to the terminal**, not even through a masking filter: a masking pattern has leaked keys before. Read keys inside a small script that never echoes them.

---

## Model report (illustrative)

> **Pause:** Client X, 14 HeyReach campaigns and 22 Bison campaigns paused (1 test campaign was already paused and stays paused). 8 n8n workflows unpublished, 1 daily routine disabled, client frozen in the shared deliverability dashboard. All read back. Not handled: 30 pending LinkedIn invites, inbox warm-up (left on). Resume plan saved.

> **Customer block:** Acme Analytics (acmeanalytics.com) and sister brand Northwind Data (northwinddata.com) blacklisted in Bison (2 domains, 9 emails) and HeyReach (2 companies, 7 leads); 3 stopped mid-sequence. Not blocked: Acme Analytics Services Inc., a different company. All entries read back.
