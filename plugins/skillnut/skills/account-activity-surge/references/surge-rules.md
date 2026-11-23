# Surge rules (the engine for the weekly alert)

The question: which accounts are engaging with us, while the pipeline is not moving and nobody is talking to them? An account is raised only when **all three tests pass**. At most 3 accounts a week, never a flood. Never invent anything: every name, title and count comes from the CRM.

Every number below is a default. The user can change any of them in Stage 2; record their choice in the decisions log (end of this file) so the next run uses it.

---

## 1. Scope: which companies

Scan **every company** in the CRM. Do not filter by ICP or industry: tagging is usually incomplete, and the accounts that slip through the tags are exactly the ones nobody is watching. (In the real run this came from, one of the hottest accounts had no ICP status and no industry at all.)

Exclude only:
- lifecycle stage Customer, Partner, or Other / Vendor (use the user's own stage names)
- companies with a Closed/Won deal
- the user's own company, and vendors and tools whose staff email you (the CRM vendor, the email security vendor, the project tool and so on)

Duplicate company records exist in every CRM (two records for the same company, or records with no name). Check all of them, and treat a no-name record by its contacts' email domain.

## 2. Test 1: Deep activity (default window: last 180 days)

### What counts as a touch

A touch must come **from the prospect**. Our own outbound never counts.

| Signal | What to look for |
|---|---|
| Real email reply | Inbound email engagements; contact "last replied" date |
| Form fill (demo request, contact form, survey, content download) | Contact conversion date, conversion name, number of conversions |
| LinkedIn reply | Replies synced from the LinkedIn outreach tool (HeyReach, Expandi, Lemlist and similar) as notes or activities; drop ones tagged negative or "not a priority" |
| Meeting they booked | Meeting engagements |
| Website visit (identified) | Contact visit count and last-visit date |
| Event or conference | Attendee-list imports, or event meetings logged in the CRM |

**Not engagement:** our outbound sequence emails (Email Bison, Instantly, Smartlead, Salesloft, Outreach, CRM sequences), opens and clicks.

### Cleaning rules (these matter a lot)

- **Drop auto-replies.** Most CRM "replies" are out-of-office messages to sequences. Exclude subjects containing any of: `automatic reply`, `autosvar`, `automatick`, `automatski`, `automatische antwort`, `réponse automatique`, `respuesta automática`, `risposta automatica`, `out of office`, `Accepted:` (calendar receipts). Non-English auto-replies are the usual leak, so always **read the subjects** of a company's replies before counting them, and add any new phrase you find to this list.
- **One person on one day = one touch.** A single LinkedIn lead-gen form often shows up as a survey, a website visit and (for a "Book a demo" form) a meeting, all on the same day. It counts once.
- **Drop negative replies** ("remove me", "not interested", "wrong person").
- **A demo-request form is not a meeting.** Count it as a form fill (it ranks high, see section 6), but never describe it as a meeting that happened.

### Depth rule

- **3+ different people**, OR **one person on 3+ separate days**, anywhere in the window.
- Any channel or mix of channels.
- Accounts where the only signal is several people filling the same survey are allowed, but rank below any account with a demo request or a real reply.
- No "still warm" cut-off inside the window: any qualifying activity in the 180 days counts. (The source run tried a 60-day cut-off and removed it; it hid accounts that were still unworked.)

## 3. Test 2: Pipeline not moving

Qualifies if either:
- **No open deal.** Closed-lost or closed-no-opportunity history is fine; a closed-lost account that is engaging again is one of the best finds.
- **An open deal that is stuck early:** in the main sales pipeline, its stage has not changed in **30+ days**, and the stage is **no later than the cut-off stage** (default: Proposal).

Exclude deals at the cut-off's next stage or later (verbal yes, contracting, signature, onboarding, won), and anything in renewal, upsell or partner pipelines.

Pipelines have different stage names everywhere. In Stage 3, read the user's sales pipeline stages in order and show them; ask which is the last stage that still counts as "early". If their CRM has no Negotiation stage, the first stage after Proposal is the cut-off.

## 4. Test 3: No conversation happening

Since the prospect's **latest touch** there must be:
- no logged meeting,
- no logged call that was a real conversation (a call attempt or voicemail is not; read the call note),
- no real two-way email: a non-auto reply from them **and** a rep reply in the same thread.

Sequence emails alone are not a conversation. If **any rep** is in an active thread with them, skip the account. Get the list of reps (names and CRM owner IDs) in Stage 2, including people who do not own accounts but do talk to prospects (founders, solution consultants, customer success).

## 5. Don't repeat

Don't post an account that was posted in the last **4 weeks**, unless it got deeper since: a new person engaged, or a new demo request.

Check by reading the channel's history, read-only: find the channel with the Slack connector (private channels need `channel_types: "private_channel"`), read the last 4 weeks, and collect the companies named in earlier "Activity Surge" posts. If the connector can't read the channel, use the run log (Mode 1 keeps one) and say so.

## 6. Rank and pick

1. A demo request or a real reply that nobody followed up
2. More distinct people
3. More repeat touches by one person
4. Recency

Post the top **3** (fewer if fewer qualify). If none qualify, post nothing. Silence is a valid result; a padded list teaches the team to ignore the channel.

## 7. The post

Slack mrkdwn, exactly this and nothing more:

```
🔥 *Activity Surge - week of <D Mon YYYY>*

*1. <Company>* - <N people since <Mon>  |  1 person, N times since <Mon>>
<Name (Title)>, <Name (Title)>, <Name (Title)>
<CRM company record link>

*2. <Company>* - ...

*3. <Company>* - ...
```

- No dates per person, no deal line, no next steps, no @-mentions.
- At most 4 people per account: the most senior or the most active.
- "Since <Mon>" is the month of the earliest touch that counts toward depth.

Example (illustrative, fictional names):

```
🔥 *Activity Surge - week of 18 Nov 2026*

*1. Northwind Biologics* - 3 people since Aug
Dana Ruiz (Senior Manager, Operations), Priya Shah (Director, IT), Tom Becker (VP Finance)
https://app.hubspot.com/contacts/<portal-id>/record/0-2/<company-id>
```

Why so short: the channel is read by people deciding who to call. Every extra line (deal history, suggested opener) makes the post a report, and reports get skimmed. The record link is where the detail lives.

## 8. End-of-run summary (always, to the operator, not the channel)

- Accounts posted (or "none qualified").
- The next 3 to 5 runners-up and the one reason each was held back (posted 2 weeks ago, rep replied on the 4th, deal moved to Proposal last week, only auto-replies once cleaned, and so on).
- The funnel with real numbers, reconciled: companies with any touch, then passing Test 1, then Test 2, then Test 3, then not recently posted, then posted. Each step says how many dropped and why.

## 9. Known limits (say these when relevant, don't hide them)

- HubSpot keeps only each contact's **latest** form fill and a session count, not every visit date, so "3 separate days" is partly inferred. Other CRMs are similar.
- LinkedIn replies, website visits and event attendance aren't always searchable account-wide; email, forms, meetings and calls are the reliable signals.
- "Being worked" only sees activity logged in the CRM. A rep talking from a personal inbox or phone is invisible. If the team does this, say so in the summary.
- Survey-only accounts usually come from one campaign. They rank last for a reason.

## 10. Decisions log (defaults; record the user's changes here in their run notes)

| Decision | Default | Why |
|---|---|---|
| Activity window | 6 months | Shorter missed slow buyers; the source run moved from 3 to 6 |
| "Still warm" cut-off | None | A 60-day rule hid unworked accounts |
| Depth | 3+ people, or 1 person on 3+ days | One touch is noise; three is a pattern |
| Deal "not moving" | 30+ days in stage, no later than Proposal | Later stages are being worked by definition |
| ICP filter | None; everything except customers, partners, vendors | Tags are incomplete |
| Survey-only accounts | Allowed, ranked last | Real but weak signal |
| Accounts per week | Up to 3 | Raised from 2 in the source run to clear a backlog; more becomes a flood |
| Repeat cooldown | 4 weeks unless deeper | Repeats train people to ignore the channel |
| Post content | Company, people count, names and titles, record link | Short enough to act on |
| Sender | A bot (webhook), not a person | The Slack connector posts as whoever connected it |
| Channel | One private ops channel | Leaders and reps who assign the work |
| Schedule | Weekly, mid-week morning | Monday is planning; Friday nobody acts |
