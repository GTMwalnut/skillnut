# Surge dashboard (Mode 3)

A 12-month view of which accounts are heating up across many channels, and which of them have no open deal. It answers at a glance: **"Which companies are engaging with us across many channels, and which of them have no open deal?"** The audience is sales leadership and account executives.

The page is a ready-made template (`assets/surge-dashboard.html`). Your job is the data: pull it, clean it, build one JSON file, check it, and render. Never write the page by hand and never edit numbers into it.

```
CRM + outreach tools  ->  activities.csv + accounts.csv  ->  build_surge_data.py  ->  surge_accounts_data.json
                                                                                         |
                                                     render_surge_dashboard.py  <--------+
                                                                |
                                                     surge-dashboard.html (one file, no external scripts)
```

## 1. Settle the definitions (Stage 2 asks)

| Setting | Default |
|---|---|
| Window | 12 months back from the pull date |
| Channels (fixed order, one colour each everywhere) | Email reply, LinkedIn reply, Meeting / demo, Survey, Website, Conference, Content / webinar. Rename, drop or add to fit (max 8) |
| Surge rule | 3+ channels in the window, OR 2+ channels with 3+ people |
| Priority 1, no open deal | 4+ channels or 4+ people, with activity in the last 90 days |
| Priority 1, open deal | 5+ channels, or an early-stage deal with 4+ people engaged |
| Priority 2 / 3 | 2 Medium if active in the last 180 days, else 3 Watch |
| Heating up | The last 3 months are the busiest 3-month block in the window |
| Group labels | "No open deal" / "Open deal" (the user can rename, for example "No HubSpot open deal") |

Exclusions are the same as the weekly alert: customers, partners, vendors, closed-won, own company.

## 2. Pull and clean the activity (one row per touch from the prospect)

Same touch definition and cleaning as `surge-rules.md` section 2, across the whole window:
- **Email reply:** inbound emails with auto-replies removed (read the subjects; non-English auto-replies leak). Pull replies from the sequencers too (Email Bison, Instantly, Smartlead, Salesloft, Outreach), because many replies never reach the CRM. Dedupe against the CRM copy.
- **LinkedIn reply:** replies from the LinkedIn tool (HeyReach and similar), synced or exported.
- **Meeting / demo:** logged meetings, plus demo-request and meeting-link forms. Keep the `type` honest ("Demo request" vs "Meeting") so the drawer never shows a request as a held meeting.
- **Survey:** completions of a named survey.
- **Website:** identified visits only (person, or company-level from a visitor tool; company-level rows have a blank person).
- **Conference:** attendee-list imports or a logged event meeting or dinner. It means they were there, not that a conversation happened.
- **Content / webinar:** gated downloads, webinar registrations, lead-gen ad forms.

Write `activities.csv`:

| company_id | company | person | title | date | channel | type | detail |
|---|---|---|---|---|---|---|---|
| 1001 | Northwind Biologics | Dana Ruiz | Senior Manager, Operations | 2026-09-14 | Email reply | Email reply | Re: workflow question |

`detail` is a short subject or form name. Never copy email bodies.

Write `accounts.csv` (one row per prospect company):

| company_id | company | segment | pipeline_status | deal | stage | amount | deal_owner | company_owner | early_stage | crm_url | suggested_action |
|---|---|---|---|---|---|---|---|---|---|---|---|

`pipeline_status` is `open_deal`, `closed_lost` or `never`. Use the open deal if there is one, else the most recent closed one. `suggested_action` is optional: leave it blank and the builder writes a rule-based one, or write a specific one per account from what you read.

Duplicate company records: keep them as separate rows but label them apart (for example "Acme (record 2)"), and say so in the caveats. No-name records: name them from their contacts' email domain and say so.

## 3. Build and check

```
python scripts/build_surge_data.py --activities activities.csv --accounts accounts.csv \
    --as-of <YYYY-MM-DD> --out surge_accounts_data.json --meta meta.json
python scripts/render_surge_dashboard.py --data surge_accounts_data.json --check
```

The builder prints every dropped row by reason and reconciles: accounts with activity = surge accounts + accounts below the rule. Read the numbers out to the user. The check fails on missing fields, monthly arrays of the wrong length, or totals that don't add up. It warns (doesn't fail) when an account has touches in the part of the window before the first month column (they count in totals but not in the monthly lanes) and when a company name repeats.

`meta.json` (optional) carries the page text:
```json
{
  "title": "Account Activity Surge - last 12 months",
  "labels": {"no_open_deal": "No open deal", "open_deal": "Open deal"},
  "channel_definitions": {"Email reply": "Inbound emails from the company, auto-replies removed."},
  "caveats": [
    "Read-only snapshot of the CRM plus sequencer replies, taken on <date>.",
    "Website visits only appear where the visitor could be identified.",
    "Conference means the person was on an attendee list or an event meeting was logged; it does not prove a conversation.",
    "Some company records have no name (labelled from their contacts).",
    "A few touches from the first days of the window count in totals but not in the monthly lanes."
  ]
}
```
Write the caveats from what you actually found, not from this example.

## 4. Render and deliver

```
python scripts/render_surge_dashboard.py --data surge_accounts_data.json --out surge-dashboard.html
```

- **In Claude with artifacts:** publish the rendered file as a private artifact (it is one self-contained page). Republish to the same artifact on each refresh so the link stays the same.
- **Otherwise:** hand over the HTML file; it opens in any browser, offline.
- The page holds names and titles of real people at prospects. Treat it like the CRM: share with the sales team, not publicly.

## 5. What the page shows (so you can explain it)

- **Header and KPI tiles:** surge accounts, no open deal (the hero tile), open deal, Priority 1, heating up. Every tile is computed from the data and filters the page when clicked.
- **Sticky filters:** deal-status toggle (default Both), priority, segment, pipeline status, owner, "has activity in" channel chips, minimum channels and people sliders, active in last 90 days, search (company or person name). Filters combine with AND.
- **Account by channel matrix (the core view):** rows are accounts, columns the channels in fixed order, each cell shaded by count with the count printed. A 6 / 12-month switch (6 months sums the last 6 monthly values). Left: name, deal-status chip (coral for no open deal, blue for open deal), priority badge and a one-line insight ("Heating up · 5 people · 4 channels · strongest: Website, Survey · previous deal closed-lost"). Right: people, latest date, deal stage and amount. Default sort: priority, channels, people, activities; every column sorts.
- **Where is the heat? scatter:** channels across, people up, bubble size = activity, colour = deal status, a "Hot, multi-threaded" corner. Hover for details, click to open.
- **Account drawer, in this order:** insight (with pipeline status, deal, stage, amount, owners, priority, suggested action, CRM link) > activity last 6 months > activity last 12 months with a monthly swim-lane per channel > people engaged with their channels > recent activity feed, newest first.
- **About this data:** definitions and caveats.
- Light and dark mode, works at phone width (the matrix scrolls with the company column frozen), money as $192K, dates as 21 Oct 2026, empty fields as a dash.

## 6. Acceptance checklist (run before handing over)

- [ ] KPI tiles match the builder's printout (total / no open deal / open deal), computed from the data.
- [ ] Only prospects: no customers, partners or vendors (spot-check 5 names against the CRM).
- [ ] By default the matrix shows every account, sorted by priority, and the 6 / 12-month switch changes the cells.
- [ ] Clicking any account opens the drawer in the order above.
- [ ] Filters combine, and searching a person's name finds their company.
- [ ] No fabricated data: blanks show a dash; no amount, title or stage was guessed.
- [ ] Open the page once (or a screenshot) and look at it before saying it's done.
