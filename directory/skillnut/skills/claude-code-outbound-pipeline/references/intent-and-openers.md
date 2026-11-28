# Find people, research intent, write openers

Load this for Steps 2 to 5.

## Step 2 - Find companies and people

1. **Companies first.** Search the prospecting API for companies with the user's filters, for example: country, employee band, industry. Save the company list.
2. **Then people.** Search those companies for the decision makers by title or function (for example sales and marketing leaders, or operations and facilities leads, whatever buys the offer).
3. Save to `data/prospects-YYYY-MM-DD.csv` with: first name, last name, title, company, company domain, LinkedIn URL, country.
4. Report companies found and people found. For list strategy, filters and bigger lists, use **tam-list-builder**.

## Step 3 - Find emails

1. Run the email finder on every person. With an orchestration layer, this can be a waterfall across several providers that stops at the first verified hit.
2. A person with no email keeps a blank email. Never fill it with a guess. Blank rows are never uploaded.
3. Reconcile: people = with email + without email.

## Step 4 - Intent research

### The question decides the quality

A basic question gets basic research. The question must match how you will pitch, because the answer becomes the opener. Build it from the offer, then show it to the user for a yes before running it.

| Weak | Sharp |
|---|---|
| "Find intent signals for these companies." | "For each company, find public evidence from the last 30 days that it needs `<offer>`: for example `<trigger 1>`, `<trigger 2>`, `<trigger 3>`. Use `<research tool>`. For each hit give the source URL, the page title, a one-line summary and the date. Rate the company HIGH, MEDIUM or LOW for how strongly the evidence points to a need for `<offer>` now, with a one-line reason. If you find nothing, say LOW: no signal found. Never invent a signal." |

What makes it sharp:
- **Tied to the offer.** "Relevant and helpful to sell `<offer>` to these companies", never news in general.
- **Named triggers.** The events that make your offer timely (a rebrand, a new office lease or headquarters, a product launch, a website rebuild, a funding round, a new leader in the buying function).
- **A time window and a place** (for example the last 30 days, and the country you sell in).
- **A source for every hit** (URL, title, summary). No source, no signal.
- **A rating with a reason**, so you can lead with the strongest accounts.
- **Permission to find nothing.** Better a LOW than a made-up reason.

### Trigger-first variant

You can also run the pipeline the other way round: ask the research tool for companies that show the trigger (for example "companies in `<country>` that signed a new office lease in the last 30 days, with the source for each"), then find the ICP people at those companies, then re-join each person to their company's signal and copy. Same columns, same rules.

### Outputs

- `data/intent-signals-YYYY-MM-DD.md`: one section per company with rating, reason, each signal with date and source link.
- New CSV columns, one value per company copied to every person there: `intent_rating` (HIGH / MEDIUM / LOW), `intent_signal` (one line), `intent_source` (URL).
- Report every company's rating in one line. Every company is researched; say so ("5 of 5 researched").

## Step 5 - Openers

Per lead, two fields: `subject` and `opener`.

| Rule | Example shape |
|---|---|
| The subject names the signal and the job you do | "`<Company>` `<event>` `<your role>` partner" |
| The opener cites where you saw it, then asks one question about what it means for them | "I read that `<Company>` `<event>`. Are you lining up a `<your role>` for `<the work it creates>`?" |
| Every person at a company gets that company's signal | Re-join contacts to the company row |
| LOW or no signal: a plain fit-based opener, never a pretend signal | Say which leads got one |
| Show 3 to 5 before writing the rest | Adjust on feedback, show again |

For the full email (body, call to action, follow-ups) and voice rules, use **copywriting-messaging**.
