# Refresh module: rebuild campaigns from a new client brief (loaded on demand)

A client sends a new angle (a regulation change, a news hook, a deadline, a new offer) and asks for the running campaigns on that theme to change. The tempting move is to paste new copy into every live campaign. The right move is eight steps, because half the time the old campaigns were failing for reasons copy cannot fix.

Read-only until step 7. Nothing is resumed, launched or changed in a sending tool without the owner's approval.

## Step 1. Audit every campaign on the theme

Pull every campaign on that theme from each sending tool (from exports, or the tool's API if connected). One table per tool:

| Campaign | Status | Leads | Contacted | Not contacted |
|---|---|---|---|---|

Then the overall picture in plain words: how many campaigns, how many leads, how many never contacted, how many people sit in both the email and the LinkedIn tool. List the campaigns you left out and why (a different theme). Note one LinkedIn trap: leads already mid-sequence only meet the new copy from their next step, so later LinkedIn messages must work on their own.

## Step 2. Rank the brief

A brief usually holds more points than a sequence can carry. Rank them in a table:

| Rank | Angle from the brief | Used where | Why |
|---|---|---|---|
| 1 | The hook: the point that cuts against what the reader expects and hits their own numbers | Email 1, LinkedIn 1 | |
| 2 | The mechanism: the next problem the hook causes | Email 2 (same thread), LinkedIn 2 | |
| 3 | Proof and offer: real customers, a small concrete offer, a real deadline | Email 3, LinkedIn 3 | |
| Left out | True but a second idea per email, too niche, or reads as a scare | Call talking points | |

Rules:
- **Every fact in the brief is unverified until the client confirms it.** Keep a "facts to confirm with the client" list from the start, especially customer names and numbers.
- **Drop proof that does not match the audience.** A named customer from a different segment (a household-name retailer when you are writing to small independent operators, an enterprise logo when you are writing to five-person firms) proves nothing to this reader.
- **A deadline only goes in if it is real.**

## Step 3. Write the new sequence

Use the Write module. Default for a refresh is the three-touch cadence: one idea per message, one ask, plain text, no links, threading as the tool allows. LinkedIn gets a short connection note (or none) and two or three messages that each stand alone.

## Step 4. Read the old campaigns' numbers

Before blaming the old copy, read what it actually did:
- **Human replies,** excluding out-of-office and bounces. Quote any real ones.
- **Bounce rate against the 3 percent safety line.** Look for firewall or gateway blocks clustered on one domain.
- **LinkedIn acceptance.** Normal is roughly 20 to 30 percent; single digits means the profile, the targeting or the sender is the problem, not the message.
- **InMail failures** (for example "no credits remaining") and leads never actioned before the pause.
- **Verification status.** If every lead shows "unverified", the list was never checked.

## Step 5. The verdict: copy problems versus everything else

Write two short lists:
- **Copy problems,** with the fix shown. The usual three: a guilt follow-up ("I've reached out a couple of times") to remove, an early meeting ask (30 minutes in email two) to soften, and packed messages that try to say four things to split up.
- **Non-copy problems** that new copy will not fix: unverified emails, low LinkedIn acceptance, inboxes below a healthy warm-up score, sender limits set above what the account can carry. Each gets an owner. Point to Email Deliverability Metrics and Dashboard and Campaign Send Checklist where they help.

## Step 6. Build the re-engagement list

Deduplicate everyone across both tools, matching on email first, then on name plus company. Then sort into keep and exclude, with a reason on every row. This catalogue's rules apply, no exceptions:

| Situation | Decision |
|---|---|
| Replied at all, ever, whatever they said | Exclude permanently (a positive reply takes the whole company off) |
| Touched on any channel in the last 100 days, no reply | Hold out until the cooldown ends; carry the date they become eligible |
| Never contacted | Keep: they can go into the new campaign now |
| Touched more than 100 days ago, no reply | Keep, with the last-touched date, so the new copy does not repeat the old |
| No usable channel (bounced email and no valid LinkedIn) | Exclude |

Add channel flags (email and LinkedIn, email only, LinkedIn only) and the source campaign. Caveat to state in the handover: name-plus-company matching can leave a few doubles where a company is written differently in each tool. For the full prior-outreach screen across the whole workspace, hand the list to Campaign Send Checklist.

## Step 7. New campaigns, as drafts

- **Copy the settings from the old campaign** (daily limits, per-domain caps, schedule, plain text, tracking off), then change only what the owner approves.
- **Detach before you attach.** Some sequencers refuse to add a lead who sits in another campaign. Remove each eligible lead from the old campaign, then add them to the new one. The old campaigns stay paused and are never resumed, so nobody gets two sequences. Their stats stay intact.
- **LinkedIn: hold out people already connected to any sender.** Many LinkedIn tools only check the sender a lead is assigned to, so someone connected to one teammate can get a cold request from another. Hold them out, or give them a campaign on the sender they already know. The owner decides.
- **Only send from healthy inboxes.** Leave out any inbox whose warm-up score is below the line the team uses (80 percent is a common one).
- Everything stays in **draft** until the owner approves the copy and the lists.

## Step 8. QC, then hand over

- **Exact membership:** for every new campaign, 0 missing, 0 extra, 0 duplicates against the keep list.
- **Read the sequences back** from the tool and compare them to the approved copy. Every message node carries the right copy; fallbacks contain no variables; every path ends.
- **The merge fields are present on every lead** (for example a custom first name, where the tool's own field holds a different enriched name).
- **A spam-word scan** on the final copy: money and refund words, regulator names, "free", currency symbols and percentages, if the team avoids them.
- **The facts still needing client confirmation,** as a list.
- Nothing launches until the owner says so.

## Model report (illustrative)

> Refresh audit done. Nine paused campaigns on this theme across your two tools, about 600 people, roughly half never contacted. The old email copy got 0 human replies from 140 people, and bounces were 3.6 percent, over the 3 percent line, with most of them blocked at one firewall. LinkedIn acceptance was about 5 percent, where 20 to 30 is normal. So yes, the copy had a guilt follow-up and a 30-minute ask in email two, and I've fixed both. But two things copy won't fix: none of the emails were verified, and acceptance points at the profile or the targeting. The new three-touch sequence is ready for your review. Your re-engagement list: 520 people kept, 14 held out until their 100-day cooldown ends, 9 excluded (4 replied, 5 have no working channel). New campaigns are built as drafts and nothing is live.
