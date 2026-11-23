# Module 2 - Data model and properties

Load this for Module 2. Design first, in a sheet; build only after sign-off.

## 1. Objects

- Keep HubSpot's native spine (contacts, companies, deals) so existing reports and automation keep working.
- Separate motions with pipelines and properties, not with new objects: new business, renewals and partner-sourced deals can be three pipelines; several products are one **Product** property on deals (with a value for "both" or "multiple"), not one pipeline per product.
- Consider a custom object only for a real thing with its own lifecycle (trials, subscriptions, partners, memberships), and only if the plan allows it (CHECK).
- Decide the company key now: **domain**. Turn on automatic company creation and association by domain so new contacts attach to the existing company instead of spawning a new one.

## 2. The field-mapping sheet

One row per property the business needs. This is the source of truth for the build and for every later integration.

| Property | Object | Type | Allowed values / format | Owner (person role, workflow, integration or enrichment) | Overwrite rule | Refresh frequency | Used by (report, routing, outreach) |
|---|---|---|---|---|---|---|---|

Rules for filling it:
- **One owner per field.** If two systems write it, they will overwrite each other. Put the owner in the property description too.
- **Overwrite rules.** Decide per field: always overwrite, overwrite only if blank, or never overwrite. Values a customer gave you directly, or that come from a trusted internal system (product data, billing), are never overwritten by enrichment. Source and attribution fields are set once and locked.
- **Refresh frequency.** Fields that change (job title, seniority, company size) get a re-enrichment cadence; fields that don't, don't.
- **Every field has a consumer.** If no report, routing rule or outreach uses it, don't create it.
- **Dropdowns over free text** wherever reporting groups by the field. Values are written once, spelled once.

Before an enrichment tool writes into many records: back up the portal's affected fields, then test the enrichment on a small control sample that someone has also enriched by hand, compare per property, and only run it at scale when each property meets the accuracy bar the user sets.

## 3. Fields that usually earn their place

| Need | Fields |
|---|---|
| Segment by product | Product (deals; contacts if routing depends on it) |
| Separate outbound from inbound | Source set at import (for example Outbound) plus Campaign name |
| Read outbound state without scrolling the timeline | LinkedIn URL (native), LinkedIn connection status (Not sent / Request sent / Connected / Replied), Outbound campaign, Outbound step, Last outbound touch |
| Email validity (HubSpot only learns of bad emails from its own sends) | Email status (Valid / Risky or catch-all / Invalid / Unknown), Email verified date, Do not email flag |
| Why a lead was disqualified | Unqualified reason (No budget, No fit, No response, Competitor, Bad timing, and the user's own) |
| Why a deal was lost | Closed lost reason, required at Closed Lost |
| Routing | Territory or region, office or location, service line |

## 4. Naming conventions (write them down in week one)

| Thing | Convention |
|---|---|
| Properties | Sentence case, no abbreviations, unit in the name where it matters |
| Dropdown options | Title Case, one meaning each, no near-duplicates |
| Deals | `<Company> - <Product or service line> - <Deal type>` (suggested; agree the pattern and enforce it) |
| Workflows | `[Object] Trigger > Outcome`, for example `[Contact] New lead > Assign owner and task` |
| Lists | `<Team or motion> - <purpose>` |
| Campaigns and UTMs | utm_source, utm_medium and utm_campaign required, lowercase, no spaces; campaign names by quarter and initiative |

## 5. Imports and integrations

- Every import uses a fixed column template (first name, last name, email, company, domain, job title, LinkedIn URL, industry, country) and sets lifecycle, lead status, source and campaign on every row at import.
- No domain, no auto-created company. Normalize company names before load (strip legal suffixes and punctuation) so variants match.
- New integrations map into the existing schema exactly; no parallel fields. Deduplicate on email first, then company plus name, then LinkedIn URL.
- For loading prospect lists and accounts, use the **TAM List Builder** skill; this module only sets the template and the rules.

## 6. Decision log

Keep a log of every model decision: date, decision, reason, who approved, what it replaced. It goes into the handover pack.
