# Nurture sequences and behaviour workflows

Module 5, loaded when the user wants HubSpot to follow up with people automatically at each funnel stage. Build only after lifecycle stages, lead status and routing work (Modules 3 and 5), because every sequence starts from a stage change or a behaviour.

## 1. Templates first

- Audit the existing email templates. Rewrite for: light HTML (or plain text for the most engaged), mobile first, one clear call to action, stronger subject line and preview text.
- Build a small template library: meeting reminder, meeting prep (what to bring), post-meeting follow-up, proposal follow-up, contract reminder, onboarding, educational nurture, webinar invite and replay, referral request.
- Personalisation tokens only from fields that are reliably filled (first name, location, product or service interest). Test subject lines and calls to action.

## 2. The sequence library, by stage

| Stage | Who | Sequences |
|---|---|---|
| Top of funnel | Subscribers, new leads, low-score contacts | Educational drip (welcome, myths, cost guide, comparison, a customer story, then an event invite); lead-magnet follow-up (deliver, related article, case study, short FAQ video, offer); research-traffic follow-up for people who came from search, AI assistants or ads |
| Middle | Qualified leads who engaged but have not booked | Meeting nurture (how to start, what the meeting covers, intro video with booking link, a matching testimonial, a direct ask); meeting booked prep (confirmation, checklist, reminder, final reminder); abandoned booking recovery (within the hour, next day, a few days later) |
| Bottom | Meeting held, proposal or contract sent | Post-meeting follow-up in branches: proposal sent / still thinking / not a fit (point them to the right resource and stop); contract pending signature (how to sign, questions, reminder, then a call task for the owner) |
| Customers | Signed clients | Welcome and onboarding, periodic review reminder, referral request after a good outcome |

Spacing is set per business; a typical drip runs a few days to a week between emails (illustrative). Every sequence has an exit: a reply, a booking, a stage change or an unsubscribe stops it.

## 3. Behaviour workflows

- **Interest detection:** repeated visits to one product or service page tag the interest, switch the content and alert the right owner.
- **High intent:** pricing plus booking pages in one session alerts the owner quickly (chat or email) and sends a follow-up within the hour.
- **Re-engagement:** no opens, clicks or visits for a long stretch gets one re-engagement email and a new offer; still nothing after that, suppress from active marketing.
- **Events and webinars:** registered gets reminders; attended gets the replay and a booking link; no-show gets the replay. Every event lead is tagged with the event as source.
- **Location or segment personalisation:** owner bios, local proof, signatures and booking links follow the contact's location or segment.
- **Joint or household contacts:** when two people buy together, link both records, tag them as one matter, send to both, capture both on the booking, and count them as one deal.

## 4. Campaigns and documentation

- Create a HubSpot campaign per event series, referral program, seasonal push and content initiative; attach every email, page and ad, and report cost > leads > meetings > revenue.
- Keep a sequence library sheet: each sequence's trigger, audience, timing, exit rule, suppression logic and test results.
- QA every sequence and workflow on test contacts before switching it on, and check suppression (customers, open deals, unsubscribes) first. Cold outbound sequences belong in the sequencer, not here; see campaign-send-checklist.
