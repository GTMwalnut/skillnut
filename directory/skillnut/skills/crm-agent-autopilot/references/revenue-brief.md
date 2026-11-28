# Job 1 - Daily revenue brief

A short message in the user's chat app every morning: goal, attained, gap, meetings in the next 7 days, and the actions for today. It reads; it writes nothing to the CRM. It posts only to the user (or the channel they named).

## Job card

| Field | Value |
|---|---|
| Trigger | Daily, early morning in the user's local time, before their first meeting (for example 07:30 local). Write the cron in the runner's time zone and say the local time in words. |
| Reads | The goal source (a goals file, a CRM report, or what the user stated); the CRM deals (and the customer or subscription list if the goal is recurring revenue); the calendar for the next 7 days; call notes from the last 24 hours (widen to 72 if empty); optionally the inbox for revenue-relevant mail. |
| Writes | None. |
| Posts | One message to the user's chat (Telegram, Slack, WhatsApp or Teams). |
| Approval point | None for the brief. Any follow-up it suggests is a draft that waits for a yes. |
| Idempotency key | Job + local date. If a brief for today is in the log, a re-run edits nothing and posts nothing unless the user asks for a refresh. |
| Failure modes | See the table at the end. |
| Sandbox test | Run once by hand; print the arithmetic block and the list of deals counted; the user checks the sum against a number they trust before the brief is scheduled. |

## Step 1 - Pin down the period and the unit (once, at setup; re-check monthly)

Write these into the job's config and print them in the brief's maths line. Never infer them at run time.

| Setting | Allowed values | Why it matters |
|---|---|---|
| Goal type | **Bookings** (deals won inside the period) or **Recurring revenue** (monthly or annual recurring revenue at a point in time) | They are counted in completely different ways |
| Period | Month, quarter or year, with start and end dates | Attained must cover exactly the same dates |
| Goal amount for this period | A number the user stated for this period, or the result of a split rule the user agreed | See "Annual goals" below |
| Revenue field and its unit | The CRM field, and whether it holds a one-off value, a monthly figure or an annual figure | The commonest source of a wrong gap |
| Active stages (recurring goals only) | The customer lifecycle stages that count as paying (for example Onboarded, Steady, Expansion) | Churned and blank stages must not count |

**Confirm the unit from real records, not from the field's name.** Show the user three or four records with the field's value next to what they know the customer pays. Field names lie: a field labelled as annual revenue has been found holding monthly amounts, and a historical snapshot built by dividing that monthly field by 12 understated revenue badly. Once the unit is confirmed, record it; if it turns out to be monthly, the brief never divides it again.

**A deal's value is usually not recurring revenue.** The value on an open or won deal is often the whole project or retainer amount. Do not add deal values to a monthly recurring number, and do not call a pipeline of project values "monthly revenue". If the goal is recurring revenue, attained comes from the customer or subscription records in active stages; deals are only for names and for the pipeline line.

## Step 2 - Compute (every run, live)

Recompute everything from the CRM on every run. Saved snapshots are only for a day-over-day comparison; never reuse a number from one as today's figure.

**Bookings goal**
- Attained = sum of the confirmed revenue field over deals in the won stage whose close date falls between the period's start and end dates (inclusive, local time).
- Deals won with no close date, or with the value blank, are not guessed: list them under "not counted" with the reason.

**Recurring revenue goal**
- Attained = sum of the recurring field over customer records whose lifecycle stage is in the active set. Exclude churned. A blank or unknown stage is flagged as ambiguous and not counted.
- Convert only when the confirmed unit differs from the goal's unit: an annual recurring figure becomes monthly by dividing by 12; a monthly figure becomes annual by multiplying by 12. A one-off or total contract value is never converted into a recurring figure.

**Annual goals and shorter briefs**
- If the user set a goal per month or per quarter, use it as given.
- If there is only an annual goal and the brief tracks a shorter period, use the split rule the user agreed at setup (even split, or their weighting). If they have not agreed one, track the year to date against the annual goal and do not invent a monthly target. Print the rule in the maths line, for example "monthly goal = annual goal split evenly, as agreed".
- Never divide an annual figure by 12 just because the brief is monthly.

**Gap and pace**
- Gap = goal for the period minus attained. If attained is above goal, say "goal met, ahead by X" rather than printing a negative gap.
- Days left = period end minus today (local).
- Pace (optional, show only if the user wants it): projected = attained divided by the share of the period elapsed. Say it is a straight-line projection and that lumpy deals make it noisy.

**Pipeline line**
- Sum the open deals in the late stages the user names (for example Discovery and Negotiation), in the same unit as the goal where that is meaningful. If it is project value against a recurring goal, say so in words.
- If pipeline in flight is thinner than what the next six weeks of the goal need, raise it under Risks with the simple arithmetic. This is the only forward-looking warning the brief gives; silence here lets the user under-invest in pipeline.

**Reconcile**
- Every run, keep in the log: the deals or customer records counted (count and sum), the ones not counted and why. The brief shows one line; the log shows the parts. The parts must add up to the line.

## Step 3 - Meetings in the next 7 days

- Read every calendar the user named; calendars are additive. If one source fails, say so in one line and carry on with the rest.
- Convert every time to the user's local day. The local day starts at local midnight, which may be the previous evening in UTC.
- Cross-check reschedules: a booking tool's reschedule or cancel notice beats a video tool's "joined" notice. Deduplicate events by their calendar UID, keeping the newest version.
- For each meeting, mark it **follow-up** if a prior call note or a real email thread with that person or company exists, **first meeting** only if neither does. Never infer a relationship from the title.
- Join the CRM: company, open deal, stage. Rank by commercial weight first (late-stage deal, active customer, unanswered commercial ask), then time.

## Step 4 - Actions for today

Derive actions from deal state and recent contact, using these push rules:

| Stage | Condition | Action line |
|---|---|---|
| Late stage (for example Negotiation) | No call in 7 days or no email reply in 5 days | Send the next-step email |
| Middle stage (for example Discovery) | The last call has no action item, or the last reply is over 7 days old | Move it forward or book the next meeting |
| First stage (Lead) | No email contact in 14 days | Qualify it or book an intro call |
| Any open deal | Open over 60 days with no activity for 14 days | Move to lost or send a re-engagement note |

Deal sentiment, if shown: positive when the last email or call has explicit commitment language or a meeting is booked within 7 days; warm when they replied without commitment, the reply is over 5 days old, or scheduling is going back and forth; cold when there has been no reply for over 7 days, a clear "not now", or no contact ever.

Also add: commitments the user owes from the last 24 hours of calls (widen to 72 hours and say so in the label if the 24-hour window is empty, because the note taker only returns recorded calls). Any follow-up the brief suggests is drafted, marked "not sent", and waits for a yes.

## Step 5 - Write the brief

- One phone screen, roughly 20 to 40 lines. Drop any section that is empty.
- Lead with the answer. No record ids, job ids, tool names, retries or "I checked X then Y".
- Sections, in order: the date line; Revenue (goal, attained, gap, the maths line, days left, pipeline); Meetings in the next 7 days; Actions today; Risks (only if any); a short audit line (what was read, what was filtered, any source that failed).
- If the inbox is read: filter newsletters and platform notifications before reading bodies (sender domains of newsletter platforms, "no-reply" senders with a single promotional block, digest-style subjects). Keep lead-form notifications even from a no-reply sender: read the body. If the user runs campaigns for other businesses, a lead that belongs to someone else's account is their pipeline, not the user's revenue: label it that way.

Model (illustrative numbers):

```
Daily revenue brief - Tue 4 Nov

Revenue (Q4, 1 Oct to 31 Dec, new bookings)
- Goal 50,000 | Won 32,000 | Gap 18,000
- Maths: 50,000 - 32,000 = 18,000 (5 won deals counted, 1 not counted: no close date)
- 57 days left. Late-stage pipeline 26,000, enough to cover the gap if most of it closes.

Meetings, next 7 days (4)
- Wed 10:00 Follow-up with a Negotiation deal: bring the revised scope
- Thu 15:30 First meeting, inbound from the pricing page

Actions today
- Send the next-step email on the Negotiation deal quiet for 6 days (draft ready, not sent)
- Book the next call on a Discovery deal whose last call had no action item

Read: 1 pipeline, 2 calendars, 3 calls. Filtered 14 newsletters.
```

## Failure modes

| Failure | What the job does |
|---|---|
| Revenue field unit unknown or changed | Sends the brief without the revenue section and says the unit needs confirming; never guesses |
| A won deal with no close date or value | Not counted; listed under "not counted" in the log and the maths line |
| CRM read fails | No revenue section; one line saying the CRM could not be read; the rest still goes |
| Calendar token expired | Uses any fallback the user approved (booking confirmation emails), says so in one line; never re-runs an interactive sign-in from the schedule |
| Note taker returns nothing for 24 hours | Widens to 72 hours and labels the section accordingly |
| Note taker's action-item field comes back garbled through the API | Uses the recap email's action-item block instead |
| A note taker query with a date filter silently returns nothing | Query by count (for example the last 50) and filter dates on the agent's side |
| Brief already posted today | Does nothing unless asked to refresh |
