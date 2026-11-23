# Book meetings at an event you attend (Option E)

Load this when the user picks Option E. The speaker play (A to D) works events the user does not attend. This one is the opposite: the user's team will be in the building, and the goal is booked coffee meetings there, or a full room for a small event the user hosts.

## The audiences

Split the people into separate audiences, each with its own copy and its own campaigns:

| Audience | Source | Why it is separate |
|---|---|---|
| This year's speakers | The live speaker page (re-pull it: speaker lists change in the last days) | They will certainly be there; the opener can name their session |
| Last year's registrants | Last year's attendee export | Likely returners; the opener asks if they are coming again |
| This year's registrants | A registrant list from the organiser or a partner, when one exists | Known to be coming; the opener says you will be there too |

## Filtering (reuse the three gates, with event-specific traps)

- **Company and title gates** as in the main play. Classify companies by hand: the source sheet's own type tags (for example "buyer" vs "not a buyer") are often wrong in both directions.
- **Size floor:** apply the user's minimum company size, and ask before applying it to a list of people known to be attending; the user may want small companies in when the meeting is in person.
- **Unknown titles:** look them up (last year's list, the CRM, an enrichment lookup by email then by LinkedIn) before dropping anyone.
- **Customers and open deals:** hold them for the user's decision; never put them in the cold invite.
- **Partner-supplied fields** (scores, account notes, owner names in a partner's list) are never used in outreach copy.
- **Identity:** check every email and LinkedIn URL against the person's name and company. A shared surname is not enough (relatives work in the same industry). Watch for **guests registered under the main attendee's email**: a fill "by email" hands the guest the main attendee's title. Match on email plus last name.
- **Loose CRM matches create false customers.** Matching on a shared word in the company name, or on an email domain that a parent company shares, flags prospects as customers and the reverse. Accept only a person-email match, a website-domain match, or a strong fuzzy name match, and read every flagged row.

- **When sources disagree on who is a customer** (the partner list's flag, the file's own "customer" column, the CRM), write a company-level discrepancy file and hold those people. The usual cause is a duplicate in the CRM: the same company stored twice, once as a customer and once as a prospect, or a person filed under a parent company. List the CRM duplicates for the user to merge; don't fix the CRM yourself.
- **Run a full audit of everyone in the event campaigns** before launch: CRM export, the source sheet's own suppress, competitor and association marks, replies, unsubscribes, bounces, LinkedIn conversations, and duplicates across audiences. Most flags will be false matches; list the few that need a decision.

## Before you add anyone

1. **Stop them in any live cold campaign first** (email and LinkedIn), then add them to the event campaign. Two campaigns writing to one person in the same week reads badly. If a LinkedIn sequence has already started, a connection request may already be out; pausing doesn't undo it, so say so.
2. People already in an event campaign are left as they are.
3. **Verify every email before upload**, even on an attendee list. In one run nothing was verified (the verification tool was blocked) and about one in nine first emails bounced, most of them at the largest companies.
4. **Do the capacity maths at build time, not at T-minus.** Count the mailboxes and LinkedIn seats the event campaigns share with cold campaigns, their daily limits, and the sending days left. If every first touch and follow-up can't land before the event at those limits, propose pausing the cold campaigns from the start (for the user's go), rather than discovering a starved campaign a week out.

## Copy

| Audience | Opener idea |
|---|---|
| Speakers | "I look forward to attending your session at [Event]." |
| Last year's registrants | "Are you attending [Event] again this year?" |
| This year's registrants | "We're looking forward to [Event] and I hope you'll be there too." |

Then one line on what the company does, using only claims from the user's own material (no savings figures or customer names unless the user supplies them), and a light ask: "We'd love to meet up sometime during the event." A coffee ask works; make it easy to say no: "If this is not your thing, I totally understand."

- **Opener tied to their week:** an optional first line about how busy the week must be given their role and company, written per person.
- **Spintax** on subjects, greetings and small phrases. Some tools cannot spin text stored in a per-person variable, so keep spun text in the template.
- **Email:** two steps, the follow-up in the same thread ("Just following up in case my earlier message didn't reach you. This is regarding meeting up at [Event]."). Plain text, no open tracking, about 3 sends per receiving domain a day, business hours in the recipient's time zone on weekdays.
- **LinkedIn:** check if already connected (message straight away); otherwise a blank connection request, the message a day after acceptance, a follow-up a few days later, and an InMail after an unaccepted request. People already connected to one of the team's senders go in a separate campaign per sender, so the message comes from the person they know.
- **Don't imply a booth you don't have.** "We'll be at the conference" drew "what's your booth number?" replies. If there is no booth, say "meet up during the event" and have a place-and-time answer ready.
- **Schedule the end.** Set the campaigns to stop on the event's first day and switch weekends off. Some tools read the end date in UTC, which can cut the last afternoon short; check it in the app.
- **Hosting your own small event:** the same flow with an RSVP link (Luma or similar), a reminder before the day, and the same soft opt-out.

### The dinner-invite cadence on LinkedIn

A cadence that has worked for dinner invites around conferences the team attends, run from a LinkedIn automation tool. It branches on the connection state, so nobody waits on a request they will never accept:

| Situation | What happens |
|---|---|
| Not connected | Send a connection request |
| Request not accepted within 3 days | Switch channel: offer the invite by email instead |
| Request accepted | The invite message goes within 1 day |
| No reply to the invite | Wait a couple of days, then one follow-up message |
| Already connected | Skip the request and the waits; send the invite message directly |

- The email branch needs a verified email for that person; if there is none, the person stays LinkedIn-only and you note it, rather than guessing an address.
- Keep every date inside the window before the dinner: if a 3-day wait plus a follow-up would land after the RSVP date, shorten the waits (the T-minus check below applies here too).
- The same branch logic works for any in-person invite (a dinner, a breakfast, a side session), not only dinners.

## The T-minus check (the step people skip)

Run a read-only status check about a week out, and again two or three days out. The question: **is the event campaign actually sending?**

| What you find | Why | Fix (each one needs the user's explicit go) |
|---|---|---|
| The event campaign sent little or nothing for days | It shares mailboxes and LinkedIn seats with cold campaigns, which take the capacity | Pause the cold campaigns until the event; resume them after |
| Follow-ups land after the event | The wait between steps is too long | Shorten the wait to one sending day |
| People who did not accept a connection request never hear from you | The InMail delay is days long | Cut the InMail delay to about 3 hours and widen the daily window so it lands the same day |
| InMails fail with "no credits" | A sender's premium LinkedIn seat disconnected | The user reconnects it in the tool |
| Many first emails bounce with "message blocked" at the largest companies | A mail gateway is blocking your sending domains, not the addresses | Write a manual-send file: those people get the approved copy by hand from the team's primary mailboxes |

| LinkedIn requests go out every day but almost none to event leads | The same seats serve the cold campaigns, which use up the daily request limit | Pause the cold LinkedIn campaigns; the user raises each sender's daily limits in the app (tools often can't change limits by API) |

Before changing a live sequence, save a copy of it, change only the one setting, and compare before and after. Keep a log of every write you make to the outreach tools. Some tool settings (schedules, sender limits) cannot be read back or changed by API; confirm them in the app. After removing someone from a LinkedIn list, the tool's per-person lookup can show a stale "pending" for a while; trust the list, not the lookup.

**The approval rule:** no campaign, sequence, lead, copy, setting, schedule, limit or pause is created or changed without the user naming that action and saying go. A broad goal ("reach as many people as possible") is not approval for a specific build. Answer "how do we speed this up?" with a plan of exact changes and their effect, then wait.

## After the event

- Reply to everyone who answered, with a place and time if they are still around. Before the event, forward replies that landed in the sending domains to the team's main inboxes, and read the auto-replies: "retired, contact X" and "I've moved to Y" are a referral and a job mover, both worth a note.
- Log who you met in the CRM.
- Resume the cold campaigns you paused, delete unused drafts, and decide what to do with any spare lead records.
- Post-event follow-up to people you did not meet: the speaker play's past-talk opener works for months.

## Model narration (illustrative numbers only)

> Three audiences: 8 of 40 speakers pass the gates, 160 of 1,800 last-year registrants, 60 of 450 this-year registrants. 22 customers and open-deal people held for your call. Two people were in a live cold campaign; I'll stop them there before adding them here, once you say go.
> T-minus 5 days: the last-year campaign has sent nothing for eight days because the cold campaigns share its mailboxes. Proposed, for your go: pause the 9 cold campaigns until Monday, shorten the follow-up wait to 1 day, cut the InMail delay to 3 hours. 14 first emails were blocked by one company's mail gateway; they are in the manual-send file.
