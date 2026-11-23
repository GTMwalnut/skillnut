# Module 1 - Portal audit (read-only)

Load this for Module 1. Nothing in this module writes to HubSpot.

## 1. Snapshot (the baseline everything is measured against)

Pull and save each table with the date. These are the "before" numbers for the handover.

| Area | What to pull | Red flags to call out |
|---|---|---|
| Contacts by lifecycle stage | Count per stage, including blank | Blank stage; a stage far larger than the motion behind it (many contacts at Opportunity but few open deals) |
| Contacts by lead status | Count per value, including blank | Blank status; typos stored as separate values; a value not in the option list; values that repeat lifecycle (for example Customer) |
| Companies | Total; with zero contacts; missing name; missing industry; missing domain | More companies than contacts; a large share with no contact and no deal |
| Contact completeness | Missing email, company, job title, LinkedIn URL, phone, country | The fields outbound and routing depend on sitting mostly empty |
| Deals and pipelines | Deals per pipeline and stage; stages with zero deals; closed stages | Duplicate stages under different IDs (two Closed Won); zero-deal clutter; a stage used to flag duplicates by hand |
| Segmentation | Is there a product or service-line field on deals? | Nothing separates products, so nothing can be reported by product |
| Owners | Records with no owner, by object | Unowned leads and companies |

Compare lifecycle against reality: contacts at Opportunity vs open deals; contacts at Customer vs companies with a Closed Won deal. A gap means the stage is set by hand.

## 2. Configuration audit

- **Custom properties:** document every custom field per object: label, internal name, type, options, fill rate, who or what writes it. Flag unused, duplicated (two fields for the same thing) and misnamed fields. Check whether a native field already exists before anyone proposes a new one (a native LinkedIn field that is simply empty needs filling, not rebuilding).
- **Workflows:** list every active workflow: name, object, trigger, the properties it writes, owner, last edited. Flag any that write to source or attribution fields (Original Source and similar), any two that write the same field, and one-time campaign workflows never switched off.
- **Data sources:** map everything feeding HubSpot: forms, imports, integrations (enrichment, call tracking, scheduling, ad platforms, sequencers, product data, billing), with frequency, volume, and whether it creates companies automatically. Draw the current-state flow.
- **Suppression and exclusion lists:** do-not-contact, customers, competitors, employees and test records. Note what is missing.
- **Marketing contact status:** check that inbound leads are not wrongly marked non-marketing, and how consent is captured.
- **Plan and limits:** plan tier, API rate limits, contact tier, workflow and custom-object availability (CHECK in Settings). These change the design.
- **Team and permissions:** users, teams, who can edit properties, pipelines and workflows.

## 3. Read the deal history (what wins)

From closed deals, read:
- **Revenue band** of companies on won vs lost deals, and how often revenue is filled.
- **Contact coverage**: how many deals have a contact attached at all. Thin coverage means titles on deals cannot be trusted as an ICP.
- **Titles and seniority** on won deals: the role and function words that recur, and where the economic buyer sits.
- **What was bought**: product or service line on won deals; separate renewals and services from new product.
- **Industry**: check the industry field against the account names. If a catch-all value holds very different companies, say so and validate vertical from the name, not the field.

This feeds the ICP, the product field in Module 2 and any lead scoring threshold in Module 3. It is a read, not a scoring model.

## 4. Findings report

One table, ranked:

| Finding | Severity (High / Medium / Low) | Evidence (count and share) | Fix (module) |
|---|---|---|---|

- High: distorts leadership reporting or blocks the next motion (inflated stages, duplicate companies, empty outbound fields).
- Medium: hurts reporting quality (stage sprawl, lead status mess, no product split).
- Low: cleanup items (records with no name, a small set with no email).

Open the report with "the five things to fix first", then the snapshot, then findings, then the recommended order (model, clean, validate and enrich, load new volume, dashboards and checks). Close with the open decisions for leadership (see `lifecycle-and-pipelines.md`).

For a leadership audience, also produce a short deck version: where things stand, the account at a glance, the top issues with one number each, what they cost (decisions on bad numbers, risky outreach, blind spend, slow reps), the plan as workstreams, the month-by-month roadmap, and the outcome.
