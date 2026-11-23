# Section E: the executable rulebook (and a sourcing guide per list)

Load this when the user chose E or All. The ICP document explains who the buyer is; the rulebook turns it into **ordered rules that any database, automation pipeline or contractor can apply and get the same answer**. Build it last, from the confirmed sections A, B and C. It has two parts: the rulebook (one per ICP) and a sourcing guide (one per list you pull). Every example value below is illustrative; fill in the user's.

How each rule is written:
- One rule, one test, one outcome: keep, drop, or route (for example "LinkedIn only").
- Applied in a fixed order: **Company rules (1 to 4), then Person rules (5 to 7), then Routing (8), then Final checks (9).** Fail any step and the row is dropped, with the reason code of the step that dropped it.
- Written so a person with no context can apply it in any tool: keyword lists spelled out, thresholds as numbers, no "use judgment" without saying what to check.

---

## Part 1. The rulebook

### 1. Geography: the country matrix
Both the **company HQ and the person's location** must be on the list. Channel can differ by country.

| Region | Countries in scope | Channel |
|---|---|---|
| North America | United States, Canada | Email and LinkedIn |
| UK and Ireland | United Kingdom, Ireland | Email and LinkedIn |
| Western Europe | the user's list | Email and LinkedIn, **except** the countries where the user has decided cold email is not allowed: LinkedIn only |
| Asia Pacific | the user's list | Email and LinkedIn |
| Everything else | out | none |

Write the out-list explicitly too ("Everything else is out, including ..."), so nobody has to guess about a country that is not mentioned. Where the evidence came from: section B geographies, the won-deal map, and the user's legal or policy view on cold email by country.

### 2. Company size
| Employees | Rule |
|---|---|
| Below the floor (for example under 11) | Drop |
| Small band, or unknown (for example 11 to 50) | Keep **only if** revenue **or** total funding is at or above a threshold (for example $3M). Otherwise drop |
| Core band (for example 51 to 5,000) | Keep |
| Above the ceiling | Drop. No exception |

The small-band exception is how a "too small" company with real money gets in, and how an unknown size is handled without guessing.

### 3. Industry and business type
State the positive test first, in one sentence (for example "the company sells its own software product, built by its own team"). Then the drop list by main business (from section C's company-type disqualifiers). Then the **manual-check classes**, each with what to check:
- Companies with a generic industry label or no label: check for an owned product; classify each as PRODUCT or SERVICES (a cheap classifier or a website read).
- Service firms that describe themselves in the buyer's words (for example consultancies calling themselves "software development"): drop.

### 4. Companies we never contact
- **4a. Customers and active trials:** a domain list, matched on exact domain.
- **4b. Competitors:** the named list by category. Names that are common words are matched on **exact domain or exact name only** (otherwise a competitor called "Anchor" drops every company that mentions an anchor). Also drop any person whose title says "... at [competitor]". A new vendor spotted in the same category is treated as a competitor. Keep a short "on hold, undecided" list rather than letting those slip through.

### 5. Person: department, email and location
- Department: the departments that buy (from section A).
- Email: work email on the company's own domain. Personal domains dropped (gmail, yahoo, outlook, hotmail, icloud, aol, protonmail, live, msn, me.com and the like).
- Location: the person must be in a country from rule 1, not just the company.

### 6. Person: titles
**6a. Titles we want, by persona.** One row per persona with its title keywords (from section A's tiers). Then a **rule of thumb** that sorts personas mechanically, for example: if the title contains Director, Head of, VP, Vice President, Chief, Founder or President, the person is a Buyer; everything else that passes is a Practitioner. Name the exceptions that never count as Buyers ("Product Owner", "Chief of Staff", "Assistant to ...").

**6b. The seniority matrix by country.** Some titles mean different things in different markets. Write the rule as a table, ignoring suffixes such as "II", "- Payments" or "(Backend)":

| Title | Country A | All other countries |
|---|---|---|
| Bare title, no seniority word | Drop | Drop |
| "Senior" version | Drop | Keep |
| Lead / Staff / Principal version | Keep | Keep |
| Architect, Manager and above | Keep | Keep |

Add two or three worked examples ("'Senior Engineer, Platform' in Country A is dropped; in Country B it's kept"). Evidence for a country row comes from the calls or won deals (for example "deep users there, but no say in the decision").

**6c. Titles we always drop.** Seniority words (intern, junior, jr), non-buying roles (assistant, chief of staff, recruiting, accounting), sales and enablement, marketing, program management, and any office-of-an-executive role. Then a softer "usually off-ICP, leave out of pulls" list (support, QA, design, analysts, contractors). These come straight from section A's wrong-fit titles.

### 7. How many people per company, and who first
| Persona | Max per company |
|---|---|
| Buyers | for example 3 |
| Practitioners | for example 5 |

Then a ranking order per persona for when there are more, most relevant first (for example Buyers: CTO, then VP or Head of the core function, then VP of the wider function, then founder at small companies, then the manager of the core team). The caps come from section A's buying-group size.

### 8. Routing (after the pull)
| Channel | Buyers | Practitioners |
|---|---|---|
| Email (sequencer) | Sender 1 | Sender 2 |
| LinkedIn tool | Sender 3 | Sender 2 for one region, Sender 3 for the rest |

Senders are roles here; the user fills in names in their own copy.

### 9. Final checks before anyone is contacted
1. **Prior outreach.** Check the dedup sheet, the email sequencer (exact email) and the LinkedIn tool (email and LinkedIn URL). Default rule: anyone who ever replied is out, a positive reply takes the company out, anyone touched in the last 100 days is out. A team can choose a stricter "never contacted before, on any channel" for a specific campaign; write whichever applies as the rule.
2. **Email verified.** "Invalid" means the person is skipped entirely: no email and no LinkedIn push either. Valid, risky and unknown are kept (or state the user's stricter line).
3. **Restricted-email countries** go LinkedIn only (rule 1).
4. **Right company.** The person's current company must be the target account. Watch for stale job history and for a different company with the same name.
5. **No placeholder companies.** Never write "Stealth" or "Self-employed" as a company name: find the real company or skip the person.

### The one-line summary
Close with one sentence that holds the whole rulebook, for example: *"In-scope-country product companies with 11 to 5,000 staff (11 to 50 only with $3M+ revenue or funding), no customers, trials, competitors or service firms; Buyers (Director+, founders) and Practitioners (core-function roles, Senior+ outside Country A), work emails, not contacted in the last 100 days and never replied, verified."*

---

## Part 2. The sourcing guide (one per list)

A short doc for one specific pull, for example "contacts at the accounts showing signal X". It never repeats the rulebook; it points at it and adds only what is specific to this list.

| Section | What it says |
|---|---|
| Input | The account file, its columns, the count, how it splits (country, signal strength), how many are LinkedIn only |
| Matching | **Match on domain, not company name** (names vary across databases) |
| Order of work | Strongest-signal accounts first |
| Do not re-filter | "These accounts already passed the company rules. Filter the people, not the companies." |
| Who to pull | Per persona, the ordered title list and the cap, from rules 6 and 7, plus one line on why these roles for this list |
| Never pull | Titles, wrong location, stale job history, placeholder companies |
| Fields to capture | First and last name (split, clean casing), title as-is and cleaned, persona, company and domain, public LinkedIn URL (not a sales-tool URN), work email, email status, city, state, country, the account's signal carried over |
| Emails | Database email first; if none, the waterfall in a stated order; verify every address; invalid means drop the person; restricted countries LinkedIn only |
| Dedup | Against the dedup sheet, the sequencer and the LinkedIn tool; one row per person even with two profiles or two emails |
| Routing | The rule 8 table |
| Output | One file, one tab per persona, plus a **Dropped** tab |
| Expected size | Accounts x caps as a ceiling, and a note that real numbers will be lower |

### The Dropped tab
Every person removed, one row each, with a reason code so the drop can be audited and argued with:

| Reason code | Meaning |
|---|---|
| GEO | Person or company outside the country matrix |
| SIZE | Company outside the size rule |
| INDUSTRY | Main business on the drop list, or SERVICES on a manual check |
| NEVER_CONTACT | Customer, trial or competitor |
| TITLE | Not a wanted title, or on the always-drop list |
| SENIORITY_COUNTRY | Dropped by the country seniority matrix |
| OVER_CAP | Beyond the persona cap after ranking |
| ALREADY_CONTACTED | Prior outreach rule |
| INVALID_EMAIL | Verification said invalid |
| WRONG_COMPANY | Stale job history or a same-name company |

Kept plus dropped equals what came in; say so at the bottom of the file.

---

## Narration (Stage 4)

Build it rule by rule, showing each with the section it came from, and confirm once at the end; it is assembled from already-confirmed sections, so it should go quickly. The model report is in the main file, Stage 4.
