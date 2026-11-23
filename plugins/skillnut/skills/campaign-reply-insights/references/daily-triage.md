# Daily cross-client reply triage (Option F)

Load this when the user picks Option F. It is a read-only morning check across one or many client workspaces: pull the last day of email and LinkedIn replies, throw out the noise, and separate real positives from everything that only looks like one, quoting the prospect's own words for every call.

It is built for agencies running several clients, and for anyone who has been burned by a "positive" that was really a polite no.

## Setup

| Item | Rule |
|---|---|
| Workspaces | One per client, for both the email tool and the LinkedIn tool |
| Credentials | **One isolated credential per client per tool.** Never use one client's key against another client's workspace, and never mix the results |
| Window | "Since yesterday at 9 am", "last 24 hours", and so on, in the user's local time |
| Calls | Read calls only. The same tokens can usually write and delete, so be strict: list and get calls only, and never mark anything read or seen |

## Each run, per client

1. **Resolve the window.** Take the user's local time, convert the cutoff to UTC, and compare provider timestamps as time-zone-aware values.
2. **Email replies.** Page the replies feed until the oldest item on a page is before the cutoff, or the last page is reached. Do not stop at page 1 unless you have confirmed the feed is sorted newest first.
3. **LinkedIn replies.** List conversations, keep those whose last message is after the cutoff and was sent by the prospect (HeyReach marks this `lastMessageSender == "CORRESPONDENT"`). The list's last-message text can be blank even when a reply exists: fetch the full thread before classifying a blank or unclear one.
4. **Run the exclusions, in order, first match wins** (below).
5. **Classify what is left** with the rejection check **before** the positive check.
6. **Report** per client.

## Exclusions (run first)

| Order | Trigger | Result |
|---|---|---|
| 1 | Sender address is a mailer-daemon, postmaster, no-reply or do-not-reply address | Excluded: automated sender |
| 2 | The tool files it as bounced | Excluded: bounced |
| 3 | The tool flags it as an automated reply | Excluded: automated |
| 4 | Bounce wording: undeliverable, mail delivery failed, delivery status notification, 550, 554, user unknown, recipient rejected, mailbox unavailable, could not be delivered, permanent failure | Excluded: bounce notice |
| 5 | Out-of-office wording: out of office, automatic reply, auto-reply, away until, on leave, returning on, will be back, limited access | Excluded: out of office |
| 6 | Mail-gateway quarantine notices (a Microsoft 365 quarantine message is the common one) | Excluded: quarantine notice |
| 7 | Auto-replies in other languages (a subject such as "Automatická odpověď:" is an auto-reply) | Excluded: automated |

Excluded items still go in the report, in their own block, so the user can audit the rules.

## Classification (after exclusions)

| Order | Trigger | Label |
|---|---|---|
| 1 | Rejection wording: not interested, no thanks, no thank you, please remove, unsubscribe, stop contacting, do not contact, wrong person | Rejection |
| 2 | Blank body, or only an email address with no other words | Unclear: read the thread by hand |
| 3 | The tool's own "interested" flag is set | Positive |
| 4 | Interest wording with no not-now wording: interested, let's chat, tell me more, book a call, schedule, would love, send me, more info, available for, happy to, open to, sounds good, yes please | Positive |
| 5 | Not-now wording: not now, not the right time, later this quarter, reach out later, circle back, down the road | Nurture |
| 6 | A real human reply that matched none of the above | Manual review |

**Why rejection runs first:** "Thanks for reaching out, but I'm not interested" contains a warm word and is a no. A classifier that fires on "thanks" alone produces false positives every week. Equally, a real positive can contain no interest phrase at all ("Sounds good, send it to my colleague at this address"), which is why unmatched human replies go to manual review rather than being dropped.

**Never call a blank thread positive,** even if the tool's template or tag suggests interest. Say it is unclear and ask for a manual look.

For a handful of replies, read every one yourself against the full text and override the rules where they are wrong; the rules are a first pass, not the verdict.

## The report

One block per client:

| Time (local) | Name | Title, company | Channel | Their words (short, verbatim) | Label |
|---|---|---|---|---|---|

Order: Positive first, then Nurture, Manual review, Unclear, Rejection. Then the "Excluded, for transparency" block with the rule that removed each item. End with one line per client: "3 human replies, 1 positive, 0 owed follow-ups older than 24 hours."

Positives with no answer from your side feed straight into the Option D follow-up watch.

## Model report (illustrative numbers only)

> Triage, since yesterday 9 am, three clients.
> Client one: 2 human replies. Positive: a head of operations, LinkedIn, "Sounds good, send me a time next week." Rejection: "Thanks for reaching out, but we're all set." Excluded: 9 (6 out of office, 2 bounces, 1 quarantine notice).
> Client two: 1 human reply, Manual review: the LinkedIn thread is blank in the list view and the full thread holds only an email address. I would not call it positive; worth a look.
> Client three: nothing human; 4 auto-replies excluded.
