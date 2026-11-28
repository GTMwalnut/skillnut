# Module 5 - Workflows and automations

Load this for Module 5. Audit what runs today before adding anything new.

## 1. Workflow audit first

- Map every active workflow that touches core properties: trigger, enrollment criteria, re-enrollment, the properties it writes, owner, purpose.
- Fix any that overwrite Original Source or other attribution fields.
- Find conflicts: two workflows writing the same field, or one workflow's action re-triggering another.
- Switch off one-time campaign workflows that were never turned off, with the owner's go.
- Rename to the convention `[Object] Trigger > Outcome` and draw a dependency map (which workflow feeds which).

## 2. Build and test rules

- Write a one-page spec per workflow before building: trigger, enrollment and suppression criteria, re-enrollment, actions in order, branches, what it writes, owner, how to know it worked.
- Build in the editor; the admin clicks, you give the steps.
- Test on test records first, then on a small real segment, then open it up. Check enrollment history and the records it touched.
- **Suppression is part of the trigger.** Every email or task workflow excludes customers, disqualified contacts, do-not-email and test records unless it is meant for them.
- **Incident drill.** If a workflow fires on the wrong people: switch it off, list everyone it touched, quarantine that segment (a static list, suppressed from sends), find the trigger condition at fault, fix it, add a safeguard (a suppression list, a narrower filter), retest, then switch it back on. Write the incident up in the change log.

## 3. Recipes

**Owner routing (owner assignment)**
- Trigger: contact or company created, or owner unknown.
- Precedence: an owner already on the company record wins (it carries named-account exceptions); else the territory rule on the record's geography (country, or state for the US); else the enriched HQ location. National subsidiaries route by their own country, not the parent's. Anything routed by a default for an unmapped geography is flagged for review.
- Other routing keys the business may use: product, segment, office or location, service line, rep capacity (round robin within a team).
- For bulk owner assignment on existing records, use the **CRM Data Health** skill (Owner assignment).

**New lead**
- Trigger: lifecycle becomes Lead (or a form submission from a new contact).
- Actions: assign owner (above), create the first-contact task with a due date, notify the owner (email or Slack), set lead status New, start the follow-up clock.

**Response deadline (SLA) and escalation**
- If lead status is still New after the agreed deadline, alert the owner; after a longer one, alert the manager; keep escalating at later checkpoints. The deadlines are the user's (an illustrative ladder: two business hours, one day, one week, one month).
- Report response time by owner and by location so slow spots are visible.

**Lifecycle advance**
- Reply or engagement: Lead to MQL. Meeting booked: MQL to SQL and create a discovery task. Deal created: Opportunity. Deal Closed Won: Customer on the contacts and company.
- Any stage to Disqualified or Unqualified: remove from sequences, require a reason, suppress from marketing.

**Deal stage automation**
- On entering a stage: create the next task, update the deal's probability, notify where needed.
- Required fields at key stages (amount and close date at Proposal; reason at Closed lost).
- Stuck-deal alert: no stage change or activity for an agreed number of days (illustrative: two weeks) creates a task for the owner.
- Deal created from a qualifying event (for example a consultation completed), so no deal exists before sales-accepted.

**New form or ad lead form**
- Before any campaign that uses a new form goes live: the HubSpot workflow for that form exists and is tested, with the lead notification (for example Slack) and the same routing as the campaign it replaces. Keep the old setup live until the new one is confirmed.
- When a meeting is booked straight from an ad through a HubSpot meetings link, check that the source and UTM values are captured on the contact before scaling.

**Attribution correction**
- When an integration (for example call tracking) lands leads with the wrong source, a workflow on contact creation reads the integration's own tag and sets the correct source, without touching contacts whose source was already right. Test on a sample and count the corrections.

**Program or tier onboarding**
- For memberships or customer programs with tiers: one enrollment workflow per tier (welcome, invite, member-only content), each suppressing the other tier.

**Ad audience sync**
- Sync lifecycle-based lists (SQL contacts, Opportunity contacts and their companies) to ad platforms for account-based ads, and exclusion lists (contacts at SQL or Opportunity, contacts with one or more deals, customers, competitors) from net-new acquisition campaigns. Use dynamic lists so exclusions stay current.

**Outbound activity**
- If sending happens outside HubSpot, sends, replies, bounces and LinkedIn touches must land on the contact timeline and update the outbound state fields. Use the **CRM Outreach Sync and Manual Upload** skill for that.

**Data hygiene**
- Recurring checks (duplicates, blanks in required fields, invalid values) as lists and alerts; scheduled AI-assisted jobs on the CRM go to the **CRM Agent Autopilot** skill.

## 4. Integrations (API) rules

- Field mappings match the existing schema exactly; deduplicate on email, then company plus name, then LinkedIn URL.
- Respect rate limits: queue, retry with backoff, and send failures to a review list rather than dropping them.
- Every integration and its token are recorded in the documentation pack by name, owner and purpose.
