# Module 6: Master people list (consolidate, cut to eligible, segment by revenue)

Load this when the user has many people exports (lead databases, campaign exports, event lists, old CRM pulls) and wants one master list, and then the answer to "who can we contact today?". Three parts, in order. Nothing here sends anything; every outreach-tool and CRM call is read-only. All numbers are illustrative.

| Part | What it gives you |
|---|---|
| 6a. Consolidate | One import-ready master with a shared schema, stable IDs and a fill-rate report |
| 6b. Eligibility | The master cut to people you may contact today, with every exclusion in its own file |
| 6c. Revenue segments | A company-level revenue band on every eligible person, with its basis and confidence |

---

## 6a. Consolidate many exports into one master

1. **Inventory.** List every source with its row count. Check whether any tab is just the union of other tabs (a combined sheet often contains the per-tool sheets in full); ingesting both is harmless once identities are merged, but say so.
2. **Core schema first** (about 40 columns), everything else kept as extras. A typical core: Lead ID, Source, Source Record ID, Full Name, First Name, Last Name, Title, Email, Email Status, Company Name, Company Domain, Company Website, LinkedIn URL, Company LinkedIn URL, Location, City, State, Country, Phone (Direct), Mobile Phone, Company Phone, Industry, Employees, Revenue, Department, Seniority.
3. **Clean null tokens** in text fields: `nan`, `none`, `not revealed`, `n/a`, `na`, `null`, and a lone `0` (one tool exports `0` for an empty website). Blank them; do not keep them as values.
4. **Normalise LinkedIn URLs** to `https://www.linkedin.com/in/<slug>`: add the scheme, URL-decode the slug, lowercase, drop query strings and trailing slashes. Unnormalised URLs make every later match fail silently.
5. **Company domain fallback:** the explicit domain field, else the domain of the company website, else the email domain unless it is a free-mail provider (gmail, yahoo, hotmail, outlook, aol, icloud and similar). Mark the derived ones (`derived_from_email`).
6. **Split phones** into Direct, Mobile and Company. Most campaign exports carry only company switchboards; say what share is a real personal number.
7. **Keep leftover columns**, prefixed by a short source tag (`[AP]`, `[TR]`, `[GA]`), so nothing is lost and nobody confuses two tools' fields.
8. **Stable IDs:** every row gets `LEAD-#####`; the provider's own ID goes in `Source Record ID`.
9. **Overlap check before dedupe:** count shared emails across sources (and, as an optional second check, name plus company). Drop junk template columns (a column that is all zeros, fields from an unrelated template).
10. **Deliver:** an XLSX with a Read Me sheet (sources, counts, decisions), core columns shaded one colour and extras another, frozen and filterable header; a CSV saved as UTF-8 with BOM so spreadsheets open accents correctly; the rebuild scripts next to the files; a fill-rate table (name, email, company, domain, LinkedIn, location, any phone); an open-items log (mixed revenue formats, rows with no email, an optional name-plus-company dedupe).
11. **CRM import rules**, if it goes into a CRM: match against existing records first; merge fields into a company that already exists; for duplicate domains, keep the record with the most information as the parent and merge the lighter one into it (Module 5d write-safety still applies).

---

## 6b. Eligibility: who can be contacted today

### Stage 1. Identity and merge
- **Key:** LinkedIn URL first, email as fallback. **A name is never a key.** Rows with neither are dropped as unidentifiable and counted.
- Merge duplicate profiles when two LinkedIn identities share an email and overlapping name tokens.
- **Field merge: newest file wins.** Rank sources newest to oldest before merging.
- Conflicts (two domains, two emails, two names for one identity) go to a `CONFLICTS - review by hand` file with a side-by-side detail file, never resolved silently.
- Repair on the way in: mojibake and encoding damage, credential tokens stuck to last names, and spreadsheet date corruption in employee bands (`Nov-20` means 11-20, `01-Oct` means 1-10).
- Assertions that must pass: ingested rows = clustered + dropped; buckets sum to identities; no candidate has two LinkedIn URLs or shares an email with another.

### Stage 2. ICP filter, and the vetted-company split
Apply the ICP's title and geography rules to every person, whether or not the company is in the CRM yet. Every identity lands in exactly one bucket:

| Bucket | Status |
|---|---|
| Title not ICP | Out by policy |
| Out of geography | Out by design |
| No email | Recoverable by enrichment (often the biggest prize) |
| No LinkedIn URL | Recoverable, smaller job |
| Unverified department | Review by hand |
| Conflicts | Review by hand |
| Candidates at a vetted company | Continue |
| Candidates at an unvetted company | Continue, but must pass the service-firm screen in Stage 3 |

The **vetted-company allowlist** is the union of the CRM's ICP-company export and any hand-vetted company workbook's KEEP rows. The real unlock is usually the candidates at companies nobody has vetted at all, and that bucket is where agencies and service firms hide.

### Stage 3. Permanent exclusions
1. **Active or won deal** in the CRM: the company is out.
2. **Bounce list: exact email only.** Matching a bounce list by domain blocks everyone at a company because one mailbox died; in one build a single dead address was excluding several hundred colleagues.
3. **Named do-not-contact companies: name and domain stem.** A name match alone misses subsidiaries, regional entities and country domains of the same parent (one parent showed up under a dozen country domains). Run the domain-stem match too, and flag rather than silently drop the borderline affiliates.
4. **Agencies, service firms, competitors, academics and associations** (the `.org` trade bodies and research institutes). Keyword screens miss firms whose names give nothing away; add a domain list for the ones you find.

### Stage 4. Prior outreach (the catalogue rule)
| What happened | Rule |
|---|---|
| Anyone who ever replied, on any tool, whatever they said (positive, negative, neutral, "later") | Person out permanently |
| A positive reply or a booked meeting | The whole company out (someone there is already talking to you) |
| Sent with no reply in the last 100 days, any channel | Person out for now |
| Last touch more than 100 days ago, never replied | Eligible again; carry `Last touched` date and channel forward so the copy does not repeat itself |

How to read the tools:
- Pull every platform with a **last-touch timestamp**, not just a yes/no.
- Pull the **full universe** of positive replies, not only your candidates: a positive reply from someone outside your list still blocks their company.
- LinkedIn tools often store no email on a conversation: match on the **normalised LinkedIn slug**, and resolve the company from your own data, because the tool's company field can be a LinkedIn company page rather than a domain.
- If a sequencer has no per-send timestamp, use the lead's last-updated date as a proxy and say so. If a tool has no reply endpoint, treat its touches as no-reply sends under the 100-day rule.
- Marketing emails from the CRM are not an outreach touch; logged one-to-one emails are.

### Stage 5. Identity check (flags, removes no one)
Check every survivor: name against LinkedIn slug, name against email local part (nickname-aware), company against email domain. If the Campaign Send Checklist is installed, its Identity module has the full rules. Verdicts PASS / MOVED / YELLOW / RED; the owner decides what to do with each.

### Staleness and re-runs
- Stage 4 goes stale daily (the 100-day window moves). Re-running only the platform pulls and the combine step refreshes the final list.
- Stage 3 goes stale as deals open and close and the exclusion files are edited.
- Stages 1 and 2 go stale only when the raw exports are refreshed.
- Cache raw pulls to disk so a same-day re-run is cheap; delete the cache to force a fresh pull.

### The segment map (hand this over)
| Status | Example people |
|---|---:|
| Ready now | 4,800 |
| Recoverable by enrichment (no email, no LinkedIn) | 15,000 |
| Recoverable over time (inside the 100 days) | 600 |
| Needs a human (unverified department, conflicts) | 900 |
| Out by design (title, geography, deals, exclusions, replied) | 40,000 |

---

## 6c. Revenue segments

Nothing is removed here; it adds a company-level band so campaigns can be cut by size.

1. **Bands:** default under $50M / $50M to $1B / over $1B. Confirm with the user.
2. **Parse every vendor format into a (low, high) range:** lower-bound buckets (`500M` meaning $500M to $1B), text ranges (`$1 bil. - $5 bil.`, `Over $5 bil.`), point values (`300.1M`). Check that no range straddles a band edge.
3. **Resolve per company domain, in this order:**

| Basis | Confidence |
|---|---|
| Every vendor row at the domain agrees | High |
| Rows disagree: majority vote (ties to the range-style vendor, else the smaller band) | Medium or Low |
| Vendor values on other rows at the same domain in the full master | High or Medium |
| CRM revenue, only when at least $100K | Medium |
| Employee-band proxy, calibrated on your own data | Estimate: Medium at the extremes, Low in the middle |

4. **Why CRM revenue is last:** CRM revenue fields are full of truncated entries (well-known companies stored as $1, $5 or $500) and default range buckets. Use it only as a fallback and only above $100K.
5. **Calibrate the employee proxy** on the companies where vendors agree, then assign each band its majority class. In one build: up to 100 staff was almost always under $50M; 201 to 500 was a coin flip between the two lower bands; 501 to 2,000 was mostly $50M to $1B; 5,000+ was always over $1B. Your market will differ; recalibrate.
6. **Every row carries** `Revenue Segment`, `Revenue (best available)`, `Revenue Segment Basis` and `Revenue Segment Confidence`, so no estimate is silent.
7. **Flag, do not remove:** affiliates of do-not-contact parents that slipped past a name match, associations and institutes (a revenue band is meaningless for them), and suspected agencies. Keep the vote mechanical and transparent, and list the companies where the vote looks wrong from general knowledge for a manual check.
8. **Say what the segments look like:** large-company bands are concentrated (few companies, many people each), the small band is a long tail (median one person per company), and seniority is flatter at small companies.
