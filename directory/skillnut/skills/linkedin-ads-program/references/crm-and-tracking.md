# CRM wiring and tracking (HubSpot shown; adapt for other CRMs with LinkedIn lead sync)

## 1. Lead sync
- Connect the LinkedIn ad account in HubSpot (Marketing > Ads). Lead gen form submissions then flow into HubSpot automatically and each form appears by name.
- **Health check, weekly:** Marketing > Ads > Conversion Events (or the ads account page) shows "needs attention" when the connection breaks; the last-sync date tells you when leads stopped. Fix: reconnect from that screen with a user who has admin rights on both the company page and the ad account; if it says "invalid permissions", reconnect with the person who set up tracking or make them the primary ads user.
- When a sync breaks, nothing is lost on LinkedIn's side: download the leads for the gap from Campaign Manager and backfill, including campaign and form source.

## 2. Workflows keyed on form names
- One workflow per form, triggered by the form name (the stable identifier; campaign and ad-group names change when campaigns are paused, duplicated or renamed). Tell the CRM owner every new form name the day it's created.
- Content form: deliver the asset immediately (plain, personal email from the relevant AE), then the nurture timeline (lead-follow-up.md).
- Demo form: confirmation email with the booking link sent immediately (people who leave details without booking get a nudge right away), plus an alert.
- **Asset links:** upload PDFs to HubSpot Files (Content or Marketing > Files > Upload > hover the file > Details > Copy URL) so the form's thank-you screen and the email link straight to a download.
- **Alerts:** a workflow that posts each demo request to the sales Slack channel, tagging the territory owner (or "unassigned"). Key the trigger on form name, not ad-group name, so new campaigns don't silently miss alerts. Keep a manual checker for missed alerts until it's proven.

## 3. UTMs and attribution
- UTMs on every destination link (`utm_source`, `utm_medium`, `utm_campaign`, `utm_content` per ad or variant). Turn on HubSpot's LinkedIn auto-tracking where available (adds `utm_source=linkedin` and `utm_medium=paid`).
- Which HubSpot field to trust:
  - **Original Traffic Source**: first-ever source; won't change for existing contacts who come back through an ad.
  - **Record Source**: how the record was created ("Meetings" for a calendar booking); not the marketing channel.
  - **Latest Traffic Source** = Paid Social and **Drill-down 1** = LinkedIn: the segment to use. Drill-down 2 carries the campaign name; keep it for campaign reporting, not as the segment filter, so new campaigns are never missed.
  - **Source / Medium / Campaign of last booking in meetings tool**: attribution for direct-to-calendar bookings when UTMs are on the meeting link.
- Test before launch: book a test meeting and submit a test form through the real ad journey; check the fields above. Use the final meeting URL with no redirects.
- External pages (a partner's registration page, a survey tool): LinkedIn can't record conversions there. Options: UTMs plus the partner's referrer and `utm_medium` export; a dedicated collector link per campaign with `utm_content` values; a completion redirect to your own thank-you page with the Insight Tag (only if the tool's plan allows it); or a lead gen form instead (see special-campaigns.md).

## 4. Lifecycle and exclusion sync
- Sync CRM lists to LinkedIn as matched audiences: SQL contacts, Opportunity contacts, then SQL companies and Opportunity companies (company-level lists strengthen ABM and allow pipeline-acceleration campaigns).
- Exclusion lists (customers, competitors, deal-associated contacts) as synced segments, then applied as exclusions in Campaign Manager. People-level exclusion lists work too.

## 5. Account-level reporting
- Company-level engagement export for the last 90 days against the customer and open-deal lists: paid impressions, clicks, engagements, leads per company. Shows LinkedIn reaching accounts already in the pipeline even when it isn't the last click.

## 6. Revenue Attribution Report (LinkedIn)
No extra media spend. Connect the CRM to LinkedIn Business Manager through CRM Sync:
1. Install the LinkedIn CRM Sync package from the HubSpot Marketplace.
2. In HubSpot: Account Setup > Integrations > Connected Apps.
3. Under Add LinkedIn integration, choose LinkedIn CRM Sync, Connect.
4. Pick the client's LinkedIn Business Manager account.
5. Review and authorise the permissions.
6. Back in HubSpot, Start all syncs.
7. The report appears in Business Manager, typically within about 72 hours. Lifecycle stages must sync through the CRM. Start with a 90-day look-back.
It shows LinkedIn's influence on opportunities and revenue, not just form leads.

## 7. Matched Audiences by API (optional, for frequent list refreshes)
- Needs: an ad-account role allowed to use the Marketing API (Account Manager, Billing Admin, Campaign Manager or Creative Manager), a LinkedIn Developer app with Marketing Developer Platform approval, an OAuth token with `rw_dmp_segments` (plus `r_ads`).
- Flow: list of LinkedIn URLs > waterfall-enrich to emails > lowercase, trim, SHA-256 hash > POST to `/rest/dmpSegments/{id}/users`.
- Without API access: upload CSVs in Campaign Manager, or sync CRM lists.
