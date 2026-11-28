# Lead follow-up: from form fill to meeting

## 1. The timeline (adapt the days to the sales cycle; each touch is a CRM workflow keyed on form name)

**Content download (report, guide, case study):**
| When | Touch | From |
|---|---|---|
| Minutes | Deliver the asset (link, not attachment), plain and personal | AE |
| Day 2-3 | One sharp insight from the asset tied to their pain, link to the matching product page; or a personal note | AE |
| Day 3-5 | Ask for a meeting (only after the lead is confirmed ICP) | AE |
| Day 7-10 | Short customer proof point; soft meeting invite ("see it on your own workflow") | AE |
| Day 12-15 | Different-angle invite, then nurture email | Marketing |
| Day 20-30 | Nurture email; final personal touch | Marketing / AE |
| After | Long-cycle nurture (months) | Marketing |

Variants seen in real programs: asset immediately, nurture emails on day 15 and day 30, personal AE outreach on days 3, 10 and 25; or first touch 1-2 days out and the next around day 20. Pick one and keep it.

**Demo request:**
- Thank-you screen links the booking calendar; the confirmation email (sent immediately) links it again.
- Anyone who leaves details without booking gets a nudge email right away with the calendar link.
- Alert to sales with the territory owner tagged; sales reach out within hours on email, LinkedIn and phone.
- Use the senior person's calendar for demo links (a VP converts better than a generic contact page).

**Rules:**
- Nurture warm ad leads from the CRM, not the cold-email tool, so unsubscribes and suppressions stay in sync.
- Don't exclude people already talking to sales; tailor their follow-up instead (a CRM segment of SQLs, opportunities and open-deal contacts who aren't customers).
- Marketing emails triggered by the form (asset delivery, results email) are not outreach; they don't count toward outreach cooldowns.
- Every ad lead and post engager can get a personal connection request from the AE or founder profile. No aggressive LinkedIn automation that breaks the platform's terms.

## 2. Engager batches into outreach (email + LinkedIn)
Run each new batch of form submitters (exported from the form webhook table) through these steps. Show the funnel with counts; removed + kept = exported.

1. **Dedupe** by LinkedIn URL against every earlier batch; remove duplicate rows.
2. **Suppress:** live deals, customers, do-not-contact, recently lost deals (track a re-eligibility date per account).
3. **Prior outreach** within the cooldown window (for example 100 days) across every outreach tool and the CRM.
4. **ICP fit,** with the client's agreed exceptions for ad engagers (people who raised their hand may pass roles or regions the cold ICP excludes; record each exception as a standing rule).
5. **Already in a live campaign?** Don't double-queue; leave them where they are.
6. **"Your call" bucket** for judgment cases; the owner decides each one; record the decision for next time.
7. **Owner:** CRM contact owner first, then account owner, then the territory table.
8. **Enrich and personalise** (optional): validate email, classify industry and ICP, find a recent company trigger, then write a short LinkedIn sequence (about 3 messages), an email sequence (about 4) and an InMail that reference both the trigger and the asset they downloaded.
9. **Upload** to the live LinkedIn and email campaigns.
10. **Identity read-back:** some LinkedIn outreach tools ignore the first name you upload for profiles they already know and use their stored name. After every upload, compare the tool's stored first name with yours; stop any lead with a wrong name on LinkedIn (email can still go).
11. Write a short README for the batch: funnel, who went where, decisions made, open items with dates.

## 3. Ad-engager outbound extension (founder-led LinkedIn)

An extension of section 2 for small, high-value audiences: the people who engaged with the ads become a short, personal LinkedIn outreach list sent from the founder's own profile. It suits a narrow audience where every account matters.

| Step | What happens | Tools in the reference build |
|---|---|---|
| 1. Signal | Engaged-audience and lead-form engagers from the ads | LinkedIn Ads |
| 2. Land in the CRM | Leads sync into the CRM (the sync health checks in crm-and-tracking.md apply) | HubSpot |
| 3. Working list | A synced sheet the team works from | Google Sheets |
| 4. ICP filter | Claude (Claude Code in the reference build) filters to the ICP, with the ad-engager exceptions from section 2 | Claude Code |
| 5. Enrich | Work email for each kept person | An email finder such as Prospeo |
| 6. Buying signals | A recent company signal per account to give the message a reason | A research tool such as Exa |
| 7. Draft | Claude writes first-draft messages from the signal and the ad they engaged with; a human edits | Claude Code |
| 8. Send | LinkedIn outreach from the founder's profile | HeyReach or another LinkedIn tool |

Rules:
- Run section 2's steps (dedupe, suppress, cooldown, live-campaign check, "your call" bucket, owner, identity read-back) on every batch before step 8; this extension changes the sender and the personalisation, not the safety steps.
- The founder approves the sender set-up, the message drafts and the start of the campaign, each with an explicit go. Keep the founder's daily limits low; the account is the asset.
- Read results by reply and meeting, and report them in words or illustrative numbers outside the client's own report.
