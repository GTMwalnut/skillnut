# Follow-up SLA watch and missed-reply audit (Option D)

Load this when the user picks Option D. It answers two questions that sit next to each other:

1. **Going forward:** is every good reply getting a human answer within 24 hours?
2. **Looking back:** which replies were never answered, or answered late, and did we cold-email anyone who was already a customer?

Both halves are read-only. The output is a list for people to act on, never a change inside a tool.

## Why this matters

A reply that nobody answers is the most expensive leak in outbound. You paid for the list, the mailboxes and the copy, the prospect said yes, and then the thread went quiet. The usual causes:

| Cause | What it looks like |
|---|---|
| Slow hand-off | The reply sat in an outreach mailbox nobody checks daily |
| Qualifying before booking | The rep decided the lead was "too junior" or "uses a competitor" and never booked the call |
| Owner left | The rep's mailbox or seat was deactivated and replies landed nowhere |
| Wrong owner | The cadence belongs to one rep, but a colleague sent the email, so the reply went to the colleague |

The house rule that fixes the second cause: **book first, qualify on the call.** A short meeting costs less than a lost buyer.

## Part 1: the 24-hour follow-up watch

### What counts

Watch every reply you classified as positive, later or referral (the replies where a human answer can still win something). Negative and not-now replies are logged but not watched.

### The clock

| Time since the reply | State | What to do |
|---|---|---|
| Under 24 hours, no answer yet | Open | Nothing yet; it shows in the daily list |
| 24 hours, no answer | Nudge | Tell the owner by name, with the reply quoted and the calendar link ready to send |
| 48 hours, no answer | Escalate | Tell the owner's manager or the account lead |
| Answered | Closed | Record the hours to first answer |

"Answered" means an outgoing message from your side in the same thread (email) or a message from your sender after their message (LinkedIn), dated after the reply. Check the tool, not the CRM alone.

For a positive reply, the first answer should offer a time or a calendar link directly. Do not ask qualifying questions first.

### Where the nudge goes

This skill never posts or sends anything on its own. It prepares the nudge text and the list. If the user wants the nudge delivered automatically (a Slack message tagging the owner within 24 hours), that is a live automation: point them to the n8n GTME Playbooks skill (Playbook 1, reply alerts), which builds it.

### Weekly drop-off note

Once a week, list the positive replies that did not become a meeting, with the reason in one line each. Common reasons: no answer in time, the rep disqualified them before a call, the prospect went quiet after the first answer, wrong person (referral not followed). This note is what changes behaviour.

## Part 2: the missed-reply audit (looking back)

Use this for a rep hand-over, a rep who left, or a "we think we missed some leads" moment.

### Steps

1. **Pull the rep's cadences or campaigns** from the sending tool, then every membership and every person in them.
2. **For each person, read two timestamps:** when they last replied and when we last contacted them.
3. **Label each replier:**
   - **Missed:** no outbound contact after their reply (last contacted is on or before last replied).
   - **Slow:** we did contact them after the reply, but 5 or more days later.
   - **Handled:** answered within 5 days.
4. **Join the CRM stage** for each person (by email; by company domain for customer status).
5. **Remove the noise:** event-invite cadences (replies there are RSVPs, not buying interest), out-of-office and auto-replies, and anyone who told you they chose a competitor.
6. **Tier the list:**

| Tier | Rule | Priority |
|---|---|---|
| 1 | Missed, and the person is at an Opportunity or Customer stage | Start here |
| 2 | Missed, lower stage or no stage | Next |
| 3 | Slow (5+ days), with real pipeline | Review |

7. **Find customers who were cold-contacted.** A person is a customer when their CRM contact stage says so, or their email domain matches a customer company. List them with which cadence reached them and who actually sent the email (the cadence owner and the sender are often different people).
8. **Write the follow-up list:** one row per person with tier, reply date, days idle, stage, cadence, who sent the last email, and a suggested reply. Leave blank "Positive?" and "Action" columns for the reviewer.
9. **State the data gaps** at the top (see below).

### The traps (state them before anyone acts)

| Trap | Why it bites | What to do |
|---|---|---|
| Some sending tools are send-only | Their API records that a reply happened and when, but not the text | Look for the reply body in the CRM's logged emails; if it is not there, say so. Expect the text to be missing for most rows |
| The timestamp gap overstates misses | A rep may have answered from their own mail client without logging it, or a colleague picked it up in a new thread | Call the list "possibly missed" and ask the team before blaming anyone |
| Deactivated mailboxes | Replies to a departed rep went to a mailbox nobody can read | Name the mailbox; the fix is admin access, not more analysis |
| Cadence owner is not the sender | The reply went to whoever sent the email | Pull the sender per email and show it |
| The tool's own person stages are often unused | Every row reads "none" | Take customer and pipeline status from the CRM |

### Output

| File | What it holds |
|---|---|
| Missed and slow repliers | Every replier with label, dates, days idle, stage, cadence, sender |
| Tiered review list | Tiers 1 to 3 after noise removal, with blank review columns and a legend |
| Customers contacted | Customer people reached by cold cadences, match type, whether they replied |

The customers-contacted file is also the input for a suppression list. Hand it over as a file for the user to apply in their own tools; never write it to the CRM or the sender yourself. And remember the standing send rule from the Campaign Send Checklist skill: anyone who replied, in any way, stays out of future cold sends for good.

## Model report (illustrative numbers only)

> Pulled 14 cadences owned by the rep: 1,200 people, 60 of whom replied. 18 got no follow-up we can see, 22 more were answered 5 or more days later. After removing event-invite RSVPs and auto-replies, 21 need a look: Tier 1 has 4 (open opportunities, no answer), Tier 2 has 5, Tier 3 has 12. Separately, 40 people at existing customer companies were in cold cadences. One warning before you act: this tool does not keep reply text, and only 6 of the 21 have the words in your CRM, so treat "missed" as "possibly missed" and check with the team first.
