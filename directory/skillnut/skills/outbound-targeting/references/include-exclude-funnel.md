# The include-then-exclude funnel

Load this in Mode A when the fit layer is being built inside a people-and-company database (Prospeo, Apollo, Clay, or similar), and in Mode C when checking how a weak list was built. The filter names are plain English; map them to the tool's own fields.

The idea in one line: **start wide, then chip away.** Nobody can guess every title and keyword a market uses. A wide include shows you what is really out there; reading the results tells you what to exclude. Five things decide a clean list: the people (titles and personas, in and out), the industry, the kind of company, its size, and its location.

## 1. Titles: include with "contains", then exclude by reading

| Step | What to do | Why |
|---|---|---|
| 1 | Enter every title you want, in "contains" mode | Many people do not write their title the way the industry norm does; exact match drops them |
| 2 | Open the results and read the titles on the first couple of pages and the last couple of pages (five or six pages in total is plenty; you do not need to read them all) | The top shows the obvious matches; the end shows what the loose match dragged in |
| 3 | Every title that does not fit your ICP goes onto the title exclusion list | Contains-matching pulls in titles that share a word with yours |
| 4 | Re-run and read again until a page reads clean | Each pass shrinks the junk |

Match mode, in short: **exact** gives the tightest match and the fewest surprises, use it when the title itself is the qualifier; **contains** gives the widest net, use it with an exclusion list; **smart / similar** expands for you, use it only after reading what it matched. The boolean traps in the main engine (unquoted acronyms matching inside other words) still apply.

Narrate it: "Included 'operations' and 'head of finance' with contains. Read pages 1, 2 and the last two. Excluded 'IT Operations' and 'Operations Assistant': wrong function and too junior."

## 2. Departments and seniority

- **Departments:** either include the departments you want, or exclude the ones you never want. Then spot-check: some databases file people under the wrong department, so a filter on department alone can silently drop real buyers or let in strangers. Read a page from each included department.
- **Seniority:** most outbound goes to the top table or to middle management. Exclude **intern** and **entry** as a default. Exclude manager and director as well when only the senior team buys.

## 3. Company keywords: include and exclude

This is the filter to get right, and it works like the title funnel.

- **Include** the keywords target companies use to describe themselves (on their site, their profile, their listings).
- **Exclude** the keywords of companies that look like the target but are not. The classic trap: **vendors tag themselves into the target industry.** A software, advertising, lead-generation or recruiting firm that sells to the industry lists the industry's keywords for search visibility, so it lands in your list. Exclude by their keywords ("software", "SaaS", "advertising", "lead generation", "recruitment", "staffing", "consulting", and the market's own equivalents).
- **Small adjacent operators** also tag themselves into the bigger category: a one-person trade contractor listed under a big industry tag is not the kind of firm the ICP means. Exclude by their trade words when the ICP is the larger company.
- **Keywords over the industry picklist.** The picklist (a couple of hundred fixed industries) is coarse and self-reported. Use it as an outer fence if you like; let the keywords do the real control.

## 4. Size: headcount and revenue together

- Headcount is the natural measure when the buyer's own revenue scales with people (services, agencies, staffing).
- Revenue is the natural measure otherwise.
- **Use both where the tool allows,** because headcount and revenue do not always agree for a given company at a given moment.

## 5. Upload lists: named accounts in, never-ICP companies out

- **Named-account upload:** paste domains or upload a CSV of companies, and search people only inside them. Save it as a reusable list so the next campaign starts from it.
- **Exclusion upload:** a list of company names or domains that are never ICP (the large players you do not sell to, companies already in a competitor's contract, any customer list). Uploading it beats remembering it.
- Location: decide whether the filter is on the **person's** location or the **company's**; they answer different questions.

## 6. Check the newer filters before building a scraper

Several databases now carry fields that used to need a custom crawler or an AI research column: company type and business model (marketplace, e-commerce, consulting, B2B or B2C), headcount by department, headcount by location, offers a demo or a free trial, technologies used, website traffic, integrations, operating languages, plus plain-English search and lookalikes of a named company. Look for the field in the tool first; build the crawler only if it is not there. (The main engine's "filters nobody opens" covers how to use them.)

## 7. Filter before export, and again after

The database filters never catch everything. After the download:

1. Sweep the exported rows on the exclusion keywords (company name, description, industry text) and on the off-ICP titles found in step 1.
2. Read what the sweep flags before deleting; remove the true misses (vendors, consultancies, tiny subcontractors, wrong-function titles).
3. Keep a removed-rows file with the reason for each removal, so nothing vanishes silently and the count reconciles: exported = kept + removed.

The point of the second pass is simple: the wrong company should never receive the email.

## 8. Plan for the losses after export

Not every exported person can be emailed. Two losses are normal:

- **No email at all:** the database has the person but no address.
- **Invalid on verification:** an address exists but the verifier rejects it.

Rule of thumb from list-building practice: some people will have no email at all, and a larger share will come back invalid at verification, so the usable list can be well under the export. Measure your own loss rate on the first export and plan every later pull with it. Then size the pull so the usable count still meets the campaign target, and if the losses run much higher, test another data source on the same filters before blaming the market.

## 9. Report shape

| Stage | Count | What happened |
|---|---:|---|
| Wide include | n | Titles (contains), departments, seniority, keywords, size, location |
| After exclusions | n | Titles and keywords excluded from reading result pages, with the lists |
| Exported | n | The download |
| After the post-export sweep | n | Off-ICP companies and titles removed, reasons in the removed file |
| With an email | n | Rows with no email set aside |
| Verified usable | n | Invalid addresses set aside |

Every row of the table reconciles with the one above it.
