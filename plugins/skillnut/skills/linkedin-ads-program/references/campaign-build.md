# Plan and build

## Plan

### 1. Goal and the honest metric
- Write the one outcome the program is judged on: booked meetings, registrations, completions, or content leads.
- If the client already has emails for most of its market, the job is surfacing intent and nurturing to a call, not net-new capture. Say so.
- Decision metric: cost per meeting (or per registration or completion). Track the chain: clicks, leads, qualified leads, meetings, opportunities.

### 2. Round 1: spend small, learn fast, then scale
- A first round of about 30 days at a modest daily budget (for example about US$100 a day), sized to prove CTR, cost per lead and lead quality before the full budget is committed.
- Each round shows what converts; scale the winners, cut the rest. Never bet the whole budget before the numbers are proven.
- LinkedIn's minimum is about US$10 a day per campaign, so the budget caps how many campaigns can run at once (for example US$50 a day supports about five). Say this when choosing the campaign count.

### 3. Competitor teardown
- Open the LinkedIn Ad Library for 3 competitors. For each: formats, offers (gated eBooks, webinars, testimonials), proof used (named customers, "N of the top 20"), and tone.
- End with "the gap we own": what none of them do that the client can (for example, direct pain-point ads where they all lead with brand and gated PDFs).

### 4. Offers by funnel stage
| Stage | Offer | Form | CTA |
|---|---|---|---|
| Middle (MOFU) | Original research or benchmark report; guide | Lead gen form, asset delivered instantly | Download |
| Middle/Bottom | Customer story with hard numbers | Lead gen form, PDF on the thank-you screen | Download the case study |
| Bottom (BOFU) | Demo or "see the platform" | Lead gen form, then the booking calendar on the thank-you screen | Book a demo / Explore the platform |
- Start mix: about 70% of budget on middle-of-funnel gated content, 30% on bottom-of-funnel demo. Move toward demo once content leads are steady.
- Keep each offer tied to one product, one pain and one campaign theme so every lead's follow-up is obvious.
- Original first-party data is the strongest middle-funnel offer; thin SEO articles don't work for expert buyers.

### 5. Projection (directional)
| Metric | MOFU | BOFU | Total |
|---|---|---|---|
| Spend | 70% | 30% | budget |
| Assumed CPC | e.g. $8 | e.g. $8 | |
| Clicks | spend / CPC | spend / CPC | |
| Conversion rate | e.g. 8% (lead form) | e.g. 3% (demo) | |
| Result | leads | demo requests | |
| Cost per lead | | | blended |
State the assumptions and replace them with real numbers after round 1.

### 6. Messaging models
- **Pain first.** Lead with the problem or an industry insight, then the fix. In a real program, problem- and insight-led ads clearly beat product-led ads for engagement and lead volume; the same principle carried into demo copy.
- **B = MAP (Fogg).** A click happens when Motivation (name the pain), Ability (pre-filled form, almost no friction) and a Prompt (one CTA) arrive together.
- **DRIVE.** Write to the dominant motivation and test challengers: Director (freedom), Relator (relationships), Intellectual (systems, process, rigour), Validator (recognition), Executive (proof, beating competitors). Technical and regulated buyers skew Intellectual and Executive; test Validator and Relator against them.
- **Positioning objections.** If part of the market resists a feature (for example AI in a regulated workflow), lead with the core platform and present the feature as optional, then A/B test feature-led versus platform-led creative rather than guessing.
- **Softer CTAs for cold audiences.** Test "Book a demo" against "Explore / See the platform"; test proof-led (a hard result) against problem-led.

## Build

### 1. Access
- Campaign Manager role: Account Manager or higher (Billing Admin, Campaign Manager, Creative Manager also work for most tasks; Account Manager is needed for some API work).
- Company page: Content Admin (follow the page, then be granted the role) to create lead gen forms and sponsored content.
- CRM admin (or a partner who has it) to connect lead sync and build workflows.

### 2. Insight Tag
- Partner ID on the site equals the Campaign Manager partner ID. Re-verify after any fix: the website-visitor audience should start filling within days.

### 3. Structure
- Three campaign groups: TOFU (awareness), MOFU (lead generation), BOFU (demo).
- Inside each, one campaign per targeting method, each layered with the same base (geography, industry, company size, seniority):
  1. Job Titles
  2. Job Functions + Seniority
  3. Skills + Seniority (if too broad, layer LinkedIn Interests to narrow it)
  4. Groups + Seniority (ask the client for the professional groups their buyers belong to; confirm they exist at setup)
  5. Remarketing
  6. Matched Accounts (company list, layered with function, title or skills)
  7. Matched Contacts (CRM list; can't be combined with interests or traits)
  8. Lifecycle audiences synced from the CRM (SQL and Opportunity contacts and companies) for pipeline acceleration
  9. A dynamic ABM audience from LinkedIn's company-engagement segments (highly engaged, brand aware, engaged prospects, surging accounts, no engagement in 30 days); new companies join as they engage
- Why split: each facet trades accuracy, volume and cost differently, and splitting shows which one books meetings.

| Facet | Accuracy | Volume | Cost |
|---|---|---|---|
| Job Title | High | Low | High |
| Job Function + Seniority | Broad | High | Lower |
| Skills + Seniority | Broad | High | Lower |
| Groups + Seniority | High | Low | Lower |

- Niche markets: tight combinations may fall below LinkedIn's minimum audience and refuse to run. Lean on Functions and Skills for reach and on matched lists for precision.
- Keep case-study and demo ads in separate campaigns; in one campaign LinkedIn tends to push only the cheaper-to-convert ad.
- A direct-to-calendar ad (no form) needs its own Website Visits campaign; it can't be split inside a lead gen campaign.

### 4. Remarketing audiences to create at setup
Website visitors; company page followers; single-image ad engagers; lead form openers (opened, didn't submit); video viewers; CRM lists. They take days to populate; add them to campaigns as they fill.

### 5. Exclusions
- Customers, competitors, and (for prospecting) open deals, SQLs and opportunities. Sync these from the CRM as lists (company and people level) rather than uploading files, so they stay current; apply the matched audiences as exclusions.
- Exceptions are campaign-specific: a survey may want customers in; pipeline-acceleration campaigns target open deals on purpose.
- Uploading contact lists: use email where you can (match rates of roughly 60-70% with email are typical) and LinkedIn URLs where you have them. A CRM contact upload must be a list or segment before it can sync.

### 6. Settings on every campaign
Audience Expansion off; LinkedIn Audience Network off; location = permanent; no lookalikes; frequency in mind (below).

### 7. Bidding
Manual CPC, enhanced off, minimum bid, raise slowly. Switch to CPM (or Maximum Delivery) only when CTR is above about 1% and there's enough conversion data; switch back if CTR falls below 1%. CTR rules of thumb from a real program: under 0.4% underperforming, about 0.45-0.65% decent, 0.6% and above good.

### 8. Ads
- Format to start: single image, both 1200 x 628 (landscape) and 1200 x 1200 (square). Document ads for reports and eBooks (page previews); testimonial ads; boosted executive posts (Thought Leader Ads) as air cover, which carry no form.
- About 7 ads per campaign: with 2 ads LinkedIn serves about 1 impression per member per 24 hours, with 7 about 2.
- Intro under 150 characters (ideally under 135), headline under 60, pain then CTA.
- One message per creative, little text on the image, CTA on the graphic matching the copy, clean layout. Share reference creatives for layout and hierarchy, not to copy.
- Customer proof only with written approval. Keep a reference sheet of who can be named, which quotes and stats are approved. For a story that must stay anonymous, attribute it ("a top [industry] company") and run it above a strip of several customer logos framed as a sampling, so no logo is tied to the story.
- Remove any customer logo the client hasn't cleared before every new creative set.

### 9. Lead gen forms
- One form per offer, named clearly and with a date when re-cut (for example `Book a Demo - Aug 26 V1`), because CRM workflows trigger on the form name.
- A privacy policy URL is mandatory, and the linked page must actually contain the policy text, or LinkedIn restricts the form.
- Ask for work email; keep fields minimal (name, email, company; title if needed). Optional qualifying question (for example membership of a professional body). Up to five custom questions.
- Thank-you screen: for content, link the asset directly (a public PDF URL, see crm-and-tracking.md); for demo, link the booking calendar so the lead gets two chances to book (screen and email).
- Changing the thank-you destination means a new form and duplicated ads associated with it; keep the old one live until the new workflow is ready.
- CTA button: pick the closest available option to the action (for example "Try now" is closer to booking than "View now").

### 10. Launch checklist (show it ticked)
- [ ] Insight Tag IDs match; website audience filling
- [ ] Campaign groups and evergreen names
- [ ] One campaign per targeting method, base layer applied
- [ ] Exclusions applied (customers, competitors, open deals as agreed)
- [ ] Audience Expansion and Audience Network off; permanent location; no lookalikes
- [ ] Manual CPC at minimum bid; daily budgets set
- [ ] About 7 ads per campaign, intros under 150 characters, CTA consistent everywhere
- [ ] Creatives and copy approved by the client in writing
- [ ] Forms active, privacy policy page valid
- [ ] CRM workflow live for every form (asset email, alert, owner)
- [ ] UTMs on every destination link
- [ ] Test submission and test booking done; contact, source and alert verified in the CRM
- [ ] Review links for every ad shared with the client
- [ ] Launch day is a Monday or Tuesday
- [ ] Weekly report day agreed
