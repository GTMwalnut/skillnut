# Signal-source audit (Mode E detail)

Answers: which tracked sources (GitHub repos, segments, keywords) should we drop, which should we add, and how does each one actually perform in outreach? Run it after 6 to 8 weeks of batches, and again 4 to 6 weeks after any change. Everything here is read-only and needs no paid tools. All numbers are illustrative.

## Step 1. Pull everyone contacted, per source

- Pull the leads from every live signal campaign, read-only: Email Bison campaign leads and HeyReach list leads (engine sections).
- "Contacted" means at least one email or LinkedIn touch went out.
- **Attribute each person to the signal cited in their message**, taken from the batch `Campaign Ready` files (the `top signal` column). Do not guess from the segment name.

## Step 2. Join the replies

- Join the reply log (or the Campaign Reply Insights output) by email and LinkedIn URL.
- For each source, per channel: contacted, replies, positive, reply rate, positive rate.

| Source | Contacted | Replies | Positive | Email reply rate | LinkedIn reply rate | Verdict |
|---|---|---|---|---|---|---|
| own/main-repo | 100 | 3 | 2 | 3% | 5% | Keep |
| sdk-a | 220 | 7 | 2 | 0.5% | 15% | Keep |
| examples-repo | 900 | 12 | 2 | 0.2% | 4% | Keep, weakest |
| framework-x | 3 | 0 | 0 | none | none | Drop candidate |

Be honest about sample size: most differences rest on 1 to 3 replies. Only two kinds of finding are solid: sources that yield almost no usable people, and big structural gaps (for example "SDK repos beat example repos").

## Step 3. Trace why some sources yield nobody

Reo usually does find people on a weak repo; your filters then remove them. For each low-yield source, trace every person tied to it through the build files (raw pulls, `Not Recommended`, `Campaign Ready`) using the removal reason column.

| Source | People Reo surfaced | Reached a campaign | Main filter reasons |
|---|---|---|---|
| framework-x | 90 | 3 | outside served regions, never-contact accounts, IT services, junior titles |
| vendor-repo | 40 | 2 | the vendor's own staff, a competitor's staff |

Typical patterns: a vendor's own repo is mostly that vendor's staff; very popular frameworks pull in students, juniors and regions you do not serve. Caveat: if your Reo pulls were already limited to your tiers, you cannot see Reo's full per-repo volume from your files; Reo's per-repo view in the UI shows it.

## Step 4. Sample candidate sources for free

To size a repo you do not track yet, use the GitHub REST API with the user's own login (free; a few hundred issues and PRs per repo fits well inside the hourly limit).

1. Take the last ~300 issues and PRs plus the newest stargazers. Remove duplicates and bots.
2. Read each user's public profile (Company field, public email, website).
3. Match against the Tier 1 and Tier 2 account lists by company name and domain. Flag never-contact companies separately.
4. Record target-account share and issues plus PRs in the last 90 days.

What we learned doing this:
- **Every match came from issue and PR authors.** The stargazer step added nothing; you can skip it.
- **Read the share as a ranking, not a forecast.** Only about a third of GitHub users list an employer, and Reo matches far better (commit emails, its own data). A repo scoring under 1% here can still yield hundreds of people in Reo.
- **Compliance: GitHub's Acceptable Use Policy does not allow using GitHub data (API or scraped) to send unsolicited messages.** People from this sample never go into HeyReach, Email Bison or any list. Do not save the sampled people. Outreach only ever uses Reo-sourced people.

## Step 5. Rank and decide

Rank sources by target-account share first, then recent activity (issues and PRs in 90 days), then outreach results.

| Rule | Why |
|---|---|
| Own repos are never dropped | Owner rule; they are your strongest citable signal |
| Drop sources with near-zero target-account share | They cost review time and yield nobody |
| Drop a vendor's own repo when its people are the vendor's staff or a never-contact account | Insiders, not buyers |
| Prefer builder repos (SDKs, specs) over browse repos (examples, awesome-lists) | Builders reply and convert better |
| Tag a partial-overlap project as competitor only if it does part of your job; pitch what it lacks | Tag drives message |
| A repo maintained by a never-contact company yields mostly uncontactable people | Note it as a caveat on the add |
| Exclude maintainers and heavy contributors of complementary repos | Insiders; they reply negatively |

Write the decision as: Drop (with reason), Add (with Reo tag and reason), Considered and not chosen, Watch list (next drop if a slot is needed). Give a swap order if slots are limited.

## Step 6. Hand over

- **Changing tracked repos happens in the Reo UI** (the API cannot add or remove them) or through the Reo account team.
- **Ask whether past activity is backfilled** for a newly added repo. If not, expect 4 to 6 weeks before a usable batch builds up.
- If a competitor campaign has sent nothing, say so: competitor sources have not really been tested yet.
- Add "exclude maintainers and heavy contributors" to the rules file (Stage 3 Batch A) if it is not there.
- Set the re-review date (4 to 6 weeks after the swap) and the watch-list check.

Output: `Signal Source Review (<date>).md` plus a workbook with the per-source performance, the trace and the sample tables, saved next to the pull log. Keep the audit scripts in `Campaign Files\scripts\`, not a scratchpad.
