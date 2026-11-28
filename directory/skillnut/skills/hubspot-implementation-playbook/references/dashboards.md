# Module 6 - Reporting and dashboards

Load this for Module 6. Two groups: the checks that keep data clean, and the views leadership steers by. Write every KPI definition down before building the report.

## 1. Data health (standing, reviewed monthly)

| Report | What it surfaces |
|---|---|
| Duplicate companies by root domain | New duplicates while they are still few |
| Empty companies (no contacts, no deals) | Progress on the cleanup, then any regrowth |
| Field completeness | Share of contacts missing email, company, job title, LinkedIn URL, owner |
| Lifecycle vs open deals | Contacts at Opportunity with no open deal (should be zero) |
| Lead status blanks and invalid values | Keeps the blank bucket from re-forming |
| Email status breakdown | Valid, risky, invalid, unknown across the base |
| Unowned records | Leads and companies with no owner |
| Workflow errors and integration sync status | Anything that stopped running quietly |

## 2. Funnel, pipeline and revenue

| Report | What it surfaces |
|---|---|
| Funnel by stage | Lead to MQL to SQL to Opportunity to Customer, with conversion at each step and drop-off |
| Funnel by product or service line | Same, split by the Product field |
| Sourced pipeline | Pipeline and revenue where source is outbound, partner, paid, and so on |
| Pipeline by product and stage | Uses the Product field across all pipelines |
| Deal stage conversion and velocity | Stage-to-stage rates and days in stage on the consolidated pipeline |
| Win and loss | Win rate and Closed lost reasons; Unqualified reasons on leads |
| Response time | Time to first contact by owner and location |
| Follow-up gaps | Leads and deals with no next task |
| Renewals and partner views | Health of the other pipelines |
| Ad and LinkedIn funnel | Request sent to connected to replied, by campaign; ad leads progressing to SQL and Opportunity |

## 3. KPI definitions to agree

- **Conversion:** lead to MQL, MQL to SQL, SQL to meeting held, meeting to opportunity, opportunity to won, and lead to customer overall.
- **Time:** lead response time, time from lead to MQL, from meeting to decision, and lead to customer.
- **Cost (if spend is known):** cost per lead, per MQL, per SQL, per meeting, per customer, by source.
- **Revenue:** revenue by source and campaign, marketing-originated revenue share, average deal size.

For each: the exact formula, the HubSpot fields it uses, the date it counts on (created date, stage-entered date, close date), and who owns it. Setting up attribution and UTMs: `attribution-and-utm.md`. Measuring it afterwards: the **Lead Attribution Analysis** skill.

## 4. Dashboards

| Dashboard | Audience | Contents |
|---|---|---|
| Executive summary | Leadership | Revenue vs target, new customers, average deal size, pipeline by product, forecast |
| Funnel and conversion | Leadership, marketing | Full funnel, conversion and time per stage, drop-offs |
| Sales performance | Sales manager | Response time, meetings, stage conversion, stuck deals, owner activity |
| Marketing performance | Marketing | Leads by source and campaign, cost per lead, lead quality by source |
| Data health | Admin, data steward | The section 1 checks |

Give each role a saved view of its own records (my open deals, my new leads, my overdue tasks) as well as the dashboards.

## 5. Review cadence

- Weekly: the sales and funnel dashboards in the team meeting.
- Monthly: data health review, workflow errors, source and campaign performance.
- Quarterly: progress against the revenue target, the attribution model, the stack, team training needs.
