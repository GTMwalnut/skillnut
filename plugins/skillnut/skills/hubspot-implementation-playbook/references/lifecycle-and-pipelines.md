# Module 3 - Lifecycle, lead status and pipelines

Load this for Module 3. Three different questions, three different fields. Never let one repeat another.

| Field | The one question it answers | Who sets it |
|---|---|---|
| Lifecycle stage | How far along is the relationship? | Automation, not people (except a few manual stages) |
| Lead status | What is the state of our outreach to this person right now? | Reps, with required values |
| Deal stage | Where is this specific deal? | Reps, gated by exit criteria |

## 1. Lifecycle stages

Start from HubSpot's native stages so reporting keeps working, and give each stage one definition and one entry trigger.

| Stage | Definition | Entry trigger |
|---|---|---|
| Subscriber | Opted into content, not a sales target yet | Form fill, newsletter, content download |
| Lead | Someone we intend to reach, inbound or sourced for outbound | Import as a prospect, or a raw inbound enquiry |
| Marketing qualified lead | Has engaged | Reply, click, attendance, or a score threshold |
| Sales qualified lead | Sales-accepted, discovery booked | Meeting booked or rep accepts |
| Opportunity | An open deal exists | Deal created (automation only) |
| Customer | Won | Deal reaches Closed Won |
| Evangelist | Referrer or active advocate | Manual, by sales |
| Other | Not a buyer: press, students, job seekers, vendors | Manual or rule on domain or title |

Rules:
- **Opportunity is set by automation when a deal is created, never by hand.** No deal before sales-accepted.
- Lifecycle advances on events: reply moves Lead to MQL, meeting booked to SQL, deal created to Opportunity, deal won to Customer.
- HubSpot moves lifecycle forward only by default; moving a record backward means clearing the field first (CHECK in the portal before building a "recycle" workflow).
- **Custom stages when the native names don't fit the business.** A professional-services firm may run: Subscriber > Lead > Intake qualified lead > Deal > Client, with exit stages Disqualified, Intake qualified lead lost, Deal lost and Inactive client. Every contact gets a stage; every stage has a definition; every routine transition is automated.
- Records that are not prospects at all (relatives of clients, vendors, employees, test records) are moved out of active stages and onto suppression lists so they stop distorting every report. Keep them; just take them out of the funnel.
- If scoring drives MQL, write the criteria down (fit, behaviour, engagement, source, explicit form answers, negative signals) with a threshold and a decay rule. Example point values are illustrative only until the user sets them.

## 2. Lead status (redesigned)

| Value | Meaning |
|---|---|
| New | Loaded or arrived, not yet touched |
| Attempting | Outreach started, no reply yet |
| Connected | Replied or engaged, conversation open |
| Working | Actively in discussion toward a meeting |
| Nurturing | Not now; recycle later, with a date |
| Unqualified | Out, with a required Unqualified reason |

- Remove values that are really lifecycle (Customer).
- Fix typos by migrating records to the correct value, then archiving the misspelled one.
- Turn stray values (for example Bad timing) into options of Unqualified reason.
- Make lead status required to move a contact forward, so the blank bucket cannot re-form.

## 3. Deal pipelines

- One pipeline per motion (new business, renewals, partner-sourced), not per product. Product is a deal property.
- One clean, linear stage set per pipeline. Each stage has an exit criterion a rep can check. Example for new business:

| Stage | Exit criterion to advance |
|---|---|
| Qualified | Fit confirmed, contact identified |
| Discovery | Discovery call held, need confirmed |
| Solution presentation | Demo given to the right people |
| Proposal | Proposal or quote sent |
| Verbal | Verbal yes, in procurement |
| Closed won | Signed |
| Closed lost | Lost, with a reason |
| Closed - no opportunity | Disqualified after creation, with a reason |

- **Consolidate safely:** build an old-to-new stage map (old stage ID, old label, deal count, new stage), get it approved, move deals, recount each old stage to zero, then archive it. History stays on the deal.
- Merge duplicate closed stages into one Closed won and one Closed lost.
- Require Closed lost reason and amount at the right stages; set close-date logic the team agrees.
- Decide which stages mean "in an active deal, do not prospect" and which are re-prospectable (closed lost, closed no opportunity). Outreach suppression from those stages runs through the **Campaign Send Checklist** skill.

## 4. Attribution rules (standing)

- Original source is set once and never overwritten. Audit workflows and integrations that write to it.
- Outbound-sourced contacts are tagged at import with source and campaign, so sourced pipeline is always separable.
- One owner per record, assigned on creation.
- Campaign links carry UTMs to the agreed taxonomy. Setup in `attribution-and-utm.md`; measuring it goes to the **Lead Attribution Analysis** skill.

## 5. Governance decisions list (for leadership sign-off)

Present these as a numbered list with a recommended answer and an owner for each. Nothing in Modules 4 and 5 is built until the relevant ones are answered.

1. Lifecycle definitions: what makes someone an MQL, an SQL, an opportunity and a customer (contract signed, first payment, project opened?).
2. The lead status values and the unqualified reasons.
3. The pipelines, stage list and the old-to-new stage map.
4. Product or service-line values.
5. Which deal stages block prospecting and which are re-prospectable.
6. Who counts as a marketing contact; consent rules; marketing to past customers.
7. How joint or related contacts are handled (linked records or one household).
8. Duplicates: who decides when merged records disagree, and which record wins.
9. What history is kept versus archived, and the retention window for contacts whose email is dead.
10. Which fields are critical (required) and which are nice to have.
11. Lead routing rule, response deadline, after-hours handling, and who is alerted.
12. Who moves deals, and what happens to stalled deals.
13. Which workflows are mission-critical and who owns each.
14. Who is the data steward, and how often data quality is checked.
15. The verification and enrichment provider to standardize on.
