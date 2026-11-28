# Attribution and UTM setup

Module 6, loaded when the user wants to know which channels and campaigns create leads and revenue. This sets attribution up so it can be trusted; measuring it afterwards is the **Lead Attribution Analysis** skill. Order: protect the source fields, agree the UTM rules, connect the tools, then turn on the models.

## 1. Ask first (one message)

- Do you have UTM conventions today, or do we start from scratch?
- Who creates marketing links: your team, an agency, both?
- Which campaign types must stay separable (paid search, social, email, webinars, events, partner, outbound)? Any split by location or product?
- Do you A/B test ads, and how should variants be told apart?
- Which conversions matter most (form fill, call, booking, download, video view), and are any offline (a signed contract in another system)?
- Which tools hold source data today (web analytics, call tracking, scheduling, billing or practice system)? Who can change website tags?
- Which referral sources and offline channels (events, print, radio) need their own source value?

## 2. Protect the source fields (before anything else)

- List every workflow and integration that writes to Original Source or other attribution fields (the portal audit already has the list). Fix or stop any that overwrite them. Original Source is set once and never overwritten.
- Tag imported and outbound contacts with source and campaign at import, so sourced pipeline stays separable.

## 3. UTM taxonomy

| Parameter | Rule | Example values |
|---|---|---|
| utm_source | Where the click came from, from a fixed list | google, linkedin, facebook, bing, newsletter, referral |
| utm_medium | The type of channel, from a fixed list | cpc, display, social, email, webinar, video, referral |
| utm_campaign | `YYYY-MM_campaign-name_variant` | `2026-03_pricing-guide_email-series` (illustrative) |
| utm_content | Ad variant or link position | hero-cta, sidebar-banner, text-link-1 |
| utm_term | Keyword, paid search only | |

- Lowercase, hyphens inside values, no spaces, values only from the agreed lists. Write the lists in a one-page playbook and get marketing (and any agency) to sign it off.
- Give the team a UTM builder (a shared sheet with dropdowns and a formula that builds the link is enough), so nobody types parameters by hand.
- Check old links and redirects: a redirect that drops the parameters loses the source.

## 4. Connect the tools

- Web analytics: track every conversion event (each form, call clicks, bookings, downloads, video views). Add a channel group for AI assistants (ChatGPT, Perplexity, Gemini, AI Overviews) so that traffic is not lost inside referral.
- HubSpot and web analytics: push form submissions and offline conversions (for example consultation to client) to analytics; bring session source and campaign back onto the contact.
- Call tracking: map its tags to HubSpot source values (for example maps listing, organic, paid, AI, referral) and send spam to a suppression list. Check that call details reach the contact record.
- Draw the lead journey end to end (ad or search > call or form > HubSpot > booking > signed client) and mark where data drops between tools.

## 5. Models and reports

- Turn on the attribution reports that answer the user's questions: first touch (what created awareness), last touch (what converted), linear (equal credit) and time decay (recent touches weigh more). Agree which one leadership reads by default, and the source priority when touches conflict.
- Build revenue by source and campaign, and which touch drove the booking or meeting.
- Check against a recent month: do leads by source in HubSpot roughly match analytics and call tracking? Explain any gap before anyone uses the numbers.

## 6. Keep it clean

- Monthly UTM audit: list values used in the month that are not on the agreed lists, fix the links, and map the stray values.
- Monthly review: leads and revenue by source, funnel conversion by source, cost per lead and per customer where spend is known.
- Quarterly: is the default model still the right one?
