# Module 5 - Launch and learn

Load this when Module 5 starts. Nothing here runs in a live tool without the user naming the action and saying go.

## Sending tool and mailboxes

- **Tool.** This play was built on Instantly, which handled sending to owners' Gmail and Yahoo addresses well. Email Bison, Smartlead or similar also work; use what the user has.
- **Mailbox types.** Google and Microsoft mailboxes. Where the tool supports it, match the sender's provider to the recipient's (Google to Google, Microsoft to Microsoft).
- **Warm-up.** At least 14 days before the first send.
- **Persona.** Send from the person the email signs off as.

## Send checklist (walk it before the pilot; show what passed)

| Check | Rule |
|---|---|
| Daily cap per inbox | About 15 sends a day per Google inbox, about 5 per Microsoft inbox |
| Inbox rotation | Roughly 70 percent of inboxes sending, 30 percent resting |
| Schedule | Weekdays only, inside the recipient's business hours in their time zone |
| Sequence length | About four steps over 12 to 15 days |
| Spintax | On greetings and a few phrases, so emails are not identical |
| Open tracking | Off |
| Variables | Every variable in the copy is filled on every row |
| Exclusions | Already contacted, replied ever, and the 100-day rule applied (Module 1) |

For full infrastructure work (domains, DNS, warm-up health, placement tests, gateway mix), use email-deliverability-metrics-and-dashboard.

## Launch

1. Pilot: one segment, the top cities, a small batch per inbox (size agreed with the user).
2. Check after the first days: bounces (valid and valid-risky apart), spam complaints, replies.
3. Scale by segment and city rank only after the check passes and the user says go.

## Reply hand-offs

| Reply | Hand-off |
|---|---|
| Shares a phone number or asks for a call | A person calls the same day. Log it in the CRM. Openers: cold-call-openers. |
| Books a call | Calendar and CRM; the deal owner gets the listing facts (category, rating, reviews, city) for the call |
| Interested, asks a question | Answer within the day; drafts: ai-responder (a human approves every send) |
| Not now | Note it; they count as replied, so they never re-enter a cold list |
| Not interested or unsubscribe | Permanent exclusion file, synced back to the sending tool and CRM (crm-outreach-sync-and-manual-upload) |
| Bounce | Remove; if valid-risky bounces run high, pause that list |
| Out of office | No action; leave in sequence |

The call-back hand-off is the heart of this play: the ask is "share your number", so the team must be ready to call.

## Learn: the readout

After the readout window, per segment and per valid-risky list: sends, bounces, replies, positive replies, call-backs and booked calls, and which first line and ask earned them. Then by city rank. Say in words which segment was strongest and what to change next (copy, ask, segment rules, review floor, cities). For reply classification and step-level analysis, use campaign-reply-insights.

Before the next state or city batch: refresh the sent history so Module 1 removes everyone this campaign touched.
