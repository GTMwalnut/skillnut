# Module 1 - Win-loss read (read-only)

Load this for Module 1, and before the first build of the model. Nothing here writes to the CRM.

## 1. Pull a full deal snapshot

- Read **every** deal, all pipelines, all stages, all time, into one working table. Re-read it at the start of each run; never trust last week's copy.
- Per deal: deal ID, name, stage label, pipeline, close date, create date, amount, deal type (new business, renewal, upsell) if the CRM has it.
- From the associated company: domain, name, industry, employee count, annual revenue, country.
- From the associated contact (the primary, or the first one attached): job title, seniority if present.
- HubSpot: pipelines first (`GET /crm/v3/pipelines/deals`, stage IDs can change, resolve labels every run), then deal search with paging, then association batch reads to companies and contacts. Attio: deals list or object records with the company and person relationships. Any other CRM: an export of deals with company and contact columns is enough.
- If the read fails part-way, stop and say so. Never learn from a partial snapshot.

## 2. Classify stages

| Class | What goes in it | Used for |
|---|---|---|
| Won | Closed won | Positive patterns |
| Lost | Closed lost, closed no opportunity, disqualified | Negative patterns |
| Open | Every active stage | Excluded from learning; optional open-pipeline signals |

- **The closed-deal count is won plus lost plus no-opportunity**, not wins alone. That count sets the cold-start step (scoring-model.md section 2).
- A stage label you have not seen before is not silently treated as open or closed. List it and ask.

## 3. Look for the patterns

Compare won with lost on each of these, and show the evidence as counts and shares:

| Pattern | Question |
|---|---|
| Industry | Which industries win most often, and which keep losing? |
| Size | Which employee or revenue band do the won accounts sit in? |
| Title | What titles are on won deals (role and function, then seniority)? |
| Speed | Which segments close fastest (create date to close date)? |
| Value | Which segments carry the highest amounts? |
| Product or service line | Which offer wins in which industry? |

Weight "fastest-closing and highest-value wins" above wins in general. A segment that wins often but slowly and small is a weaker pattern than one that wins quickly and big.

## 4. Data-quality checks before you trust a pattern

- **Split new business from renewals and upsells.** An installed base that renews every year can flood the wins and make the pattern "accounts we already have". Learn net-new scoring from net-new deals.
- **Contact coverage.** Often only a minority of deals have a contact with a title. Say what share do; learn title patterns only from those, and lower confidence on title-based factors.
- **Catch-all industry fields.** An industry value can be a dumping ground (big consumer, pharma and chemical accounts all tagged the same). Check the top accounts under each industry by name before quoting the pattern.
- **Concentration.** A few big accounts with many deals each can dominate the counts. Count by unique company as well as by deal.
- **Titles name the role, not the problem.** Buyers are rarely titled by what you sell. Learn on role, function and seniority, not on solution words in the title.
- **Seniority shape.** Check whether seniority changes from first stage to won. If the economic buyer rarely appears on won deals, do not give C-level titles an automatic boost; the champion level is the pattern.

## 5. Output

`win-loss-report.md`: the snapshot counts, the stage map, the pattern tables (won versus lost, by unique company and by deal), the data-quality warnings, and a short "what this means for scoring" list. This becomes `won_patterns` and `lost_patterns` in the scoring sheet.

For turning these patterns into a written ICP, hand off to **icp-builder**. For which channels and sequences led to the wins, hand off to **lead-attribution-analysis**.
