# Sequencer migration and one-time lead ingestion (Mode M)

Read this before the first write of a Migrate run. It covers three jobs that look different but run the same way: moving leads from one sequencer to another, moving them from one campaign to another, and loading a one-time list that never went through your normal pipeline.

## The one rule

**Leads never move tool to tool directly. They always go through your central lead table first.**

The central lead table is wherever your team keeps one row per person with their status and history: a database table (Supabase, Postgres), a CRM, or at the very least a master sheet. If you export from the old tool and import straight into the new one, the new tool knows nothing about who bounced, who replied, or who was already emailed. Your reporting loses them too: the analytics show a gap, and nobody can tell what happened to those people.

```
Source (old tool / old campaign / CSV / event list)
            |
            v
  Central lead table   <- dedupe, merge, verify, status, history
            |
            v
Target campaign (new tool or new campaign)
```

If the user has no central table at all, say so plainly and offer the minimum: a master CSV with one row per person, built in this run, kept after it.

## Step 0 - Classify the event

Ask once, at the start. The type decides which steps apply.

| Type | Example | Does prior status exist? |
|---|---|---|
| 1. Tool to tool | Instantly to EmailBison, Smartlead to Instantly | Yes: bounced, contacted, replied all carry over |
| 2. Campaign to campaign | one EmailBison campaign to another | Yes: status from the source campaign carries over |
| 3. One-time source | a data vendor download, a CRM export, a nurture list from the client, a conference or event list | No: nobody has emailed them yet (a nurture list is the one exception and may carry a little status) |

## Step 1 - Operator intake (the questions)

| Ask | Why it matters |
|---|---|
| Which type, 1, 2 or 3? | Types 1 and 2 carry history; type 3 does not |
| Source: which tool and campaign, or which file? | You pull status from it, or you map the file |
| Target: which tool and campaign? If it does not exist, what to call it? | House naming: `<lead source> <how it was personalized> <date>`, for example "Event list Personalized 14 Jan" |
| Input: CSV export or API pull? | API pull carries per-lead status more reliably |
| Copy: carry the existing personalization as-is, or rewrite it? | Carry-as-is maps old variables to new ones; rewrite hands the list to the Copywriting Messaging skill first |
| Suppression: confirm the matrix below | It is the user's list, so the user confirms it |
| Run id | One id per event, stamped on every row, so a re-run cannot double-load |

## Step 2 - Acquire into a staging set

Land everything in a staging file or table first. Do not write to the central table yet.

**CSV or Excel:** map columns to the field model below. Email is required; first name, last name, company and company domain are strongly recommended. Strip `https://`, `http://` and `www.` from domains. Drop any row with no email and no LinkedIn URL: it cannot be reached.

**API pull from the source campaign:** page to the end and log the total pulled. Capture each lead's status as you go (contacted, bounced, replied, reply sentiment, unsubscribed).

**Reading an Instantly export.** A real campaign export carries these columns, and two of them trip people up:

| Column | What it means for migration |
|---|---|
| Lead Status | Values like "Active / Not yet contacted", "Active / Contacted", "Completed / Contacted", "Active / Reply received", "Completed / Reply received", "Bounced". This is the column that tells you contacted, replied and bounced |
| Interest Status | Defaults to "Lead" for almost everyone. "Lead" does NOT mean interested. Only values like "Not interested" or "Wrong person" carry signal |
| Last contacted from | The sending mailbox. Keep it as the sender history; do not reuse it as the new sender unless that mailbox moves too |
| Email Security Gateway Provider | Mimecast, Proofpoint and so on. Carry it: the deliverability skills use it to choose sending domains |
| pause_until | A lead the old tool was holding back. Ask why before moving it |
| Campaign Name | Source campaign, keep it as "prior campaign" |

## Step 3 - Dedupe against the central table

Match in this order:

1. Exact email.
2. Same person, changed email: LinkedIn URL, or first name + last name + company domain.

The same person at the same company in a different country is not a conflict. Only a different company is.

**Duplicate, same company: merge, highest information wins.** Take the record with more filled, meaningful fields as the base and fill its gaps from the other. When both have a different value for a non-identity field, keep the base value. Never lose history: union the source tags, union the channels the person has been reached on, keep the earliest created date, refresh the updated date.

**Duplicate, different company: probably a job change.** Resolve it the same way every time:

1. Re-verify both emails, old and new.
2. Exactly one valid: that email and its company are current. Mark the other as former email and former company, and flag the job change.
3. Both valid: open the LinkedIn profile and read the latest experience entry. That company, with its matching email, is current.
4. Keep the former record for history. Only the current identity can go into the new campaign.

## Step 4 - Verify every email again

Re-verify even migrated leads; addresses decay. Run a verifier waterfall (for example Findymail, then Blitz, then Prospeo), record status (valid, invalid, risky, unknown), the provider that confirmed it and the date. Only `valid` goes forward. Invalid or risky people with a real `linkedin.com/in/` URL can go LinkedIn-only.

## Step 5 - The suppression matrix

Everyone is written to the central table, so history is complete. Not everyone is pushed to the new campaign. These rules follow this catalogue's shared rules (any reply excludes for good; an unanswered send starts a 100-day cooldown):

| Prior status | Write to central table? | Push to the new campaign? |
|---|---|---|
| Not contacted | Yes | Yes, if the email verifies |
| Contacted, no reply, sequence still running | Yes | User's call. If yes, resume at the next unsent step only, never from step 1, and keep the same copy so they do not get the opener twice |
| Contacted, no reply, sequence finished | Yes | No, until 100 days after the last send. Then eligible again, with "Last touched" carried |
| Contacted, no send date in the export | Yes | No. Treat the touch as recent and list them for the owner |
| Bounced (in the old tool or flagged in the CRM) | Yes, as suppressed | No, whatever re-verification says |
| Any human reply: negative, neutral or "wrong person" (an out-of-office alone is not a reply) | Yes, as suppressed | No, permanently. A "wrong person" reply is also a job-change signal: route it through Step 3 |
| Replied positive | Yes | No. Hand to sales, and take the whole company out of the new campaign |
| Unsubscribed | Yes, as suppressed | No, permanently |

## Step 6 - Personalization

- **Carry as-is (types 1 and 2):** keep the old opener and follow-up emails unchanged and map them to the new tool's variables. Show the old-variable to new-variable table and get one approval, exactly like Batch A of the normal email track.
- **Rewrite:** hand the list to the Copywriting Messaging skill, then come back here.
- **Type 3 always needs copy.** A lead with empty message fields is never pushed, so nothing un-personalized goes out by accident.

## Step 7 - Hygiene

Run the normal pre-send screens before anything is pushed: open deals and customers in the CRM (re-prospectable stages like closed-lost are allowed through), competitors and same-space vendors, and name and company normalization. If the Campaign Send Checklist already ran on this file, say so and confirm instead of re-running.

## Step 8 - Write to the central table (history-preserving upsert)

Upsert keyed on email, with the merge rules from Step 3.

**The guard you must switch off.** A daily pipeline usually writes only "if not already delivered", so it never touches people already in a campaign. A migration deliberately re-touches already-delivered people, so that guard must NOT apply here. Union the history instead: a person moved from Instantly keeps "Instantly" in their channels and gets "EmailBison" added when pushed. Type 3 people start with an empty channel list. Only overwrite message fields if Step 6 chose rewrite.

## Step 9 - Push to the target campaign

Only people who are verified valid, not suppressed, not bounced and have copy are eligible. From here the normal Email or LinkedIn track of this skill takes over: pilot of about 10, user check in the UI, collision check, scale, full QC.

Two migration-specific gotchas:

- **EmailBison will not attach a lead that sits in any other campaign, draft included.** For a campaign-to-campaign move, remove the lead ids from the old campaign first, then attach to the new one.
- **Pause the old campaign before you push.** Otherwise the same person can get a step from both tools in the same week. Read the old campaign's status back to prove it is paused.

Then write the delivery back to the central table: add the new tool to the person's channels, set the new campaign name and the active flag. For a campaign-to-campaign move inside one tool the channel does not change; update the campaign name only.

## Step 10 - Run log and idempotency

Keep one run record per event: type, source, target, input method, counts (pulled, written, pushed, suppressed, bounced), status (running, done, failed), start and finish times. Open it at the start, stamp every row with the run id, close it with the final counts. Running the same id twice must change nothing on rows already processed.

## The reconcile line (say it in the handover)

Every pulled row must land in exactly one bucket. Illustrative example:

> Pulled 2,000 from the old campaign. 1,240 pushed to the new campaign, 410 held for the 100-day cooldown, 150 bounced, 60 replied (excluded for good, 4 positive handed to sales), 90 failed verification (35 of them moved to LinkedIn-only), 50 duplicates merged into existing records. 1,240 + 410 + 150 + 60 + 90 + 50 = 2,000. Every one of them is in the central table with its old campaign kept in its history.

## End-to-end checklist

- [ ] Classified (type 1, 2 or 3) and run record opened
- [ ] Intake answered: source, target, input, copy handling, suppression confirmed
- [ ] Staged with prior status captured (types 1 and 2)
- [ ] Deduped on email, then LinkedIn URL or name + domain
- [ ] Merged, highest information wins, history unioned
- [ ] Job changes resolved: both emails re-verified, then LinkedIn latest experience
- [ ] Every email re-verified; only valid goes forward
- [ ] Suppression matrix applied; 100-day cooldown and permanent reply exclusion honoured
- [ ] Copy carried or rewritten; nobody without copy pushed
- [ ] Hygiene screens run
- [ ] Central table upserted without the "already delivered" guard
- [ ] Old campaign paused, then pushed through the normal pilot, scale and QC
- [ ] Delivery written back; reconcile line adds up; run record closed
