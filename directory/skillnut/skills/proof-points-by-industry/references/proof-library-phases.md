# The proof library, phase by phase (load for Mode A)

Load this when building or refreshing the matrix (Mode A or All). It is the full nine-phase method behind the engine's short version, plus the definition of done and the quarterly re-pass. The engine in SKILL.md already covers extraction fields, clearance, the umbrella claim and Mode B; this file adds the parts that make the library complete and keep it alive.

## The nine phases

| Phase | What happens | Output |
|---|---|---|
| 1. Source discovery | Gather everything, filter nothing yet | One raw folder or list of sources |
| 2. Extract and tier | One row per named customer, tiered A, B or C | Customer rows with tier and source |
| 3. Industry mapping | Bucket every name by industry | Five named references per vertical |
| 4. Quantified outcomes | Pull every number from every case study | Outcome table with "when to use" |
| 5. Competitive displacement | Who did we beat, where, and why they switched | Displacement catalogue and trap questions |
| 6. Quotes library | Verbatim customer quotes, five fields each | Filterable quote list |
| 7. Messaging output | Turn the raw library into usable copy | About-us intro, swap-in packs, openers, trap questions |
| 8. Competitor mining | Run phases 1 to 6 on the top three competitors | A parallel competitor file |
| 9. Version and cross-link | Update log, links to the ICP, intent and messaging files, quarterly re-pass | A living file with a definition of done |

### Phase 1: source discovery (dump all, don't filter yet)
- **Own sources:** the master sales deck, case-study PDFs, logo walls and the homepage, press releases and partner co-branded pieces.
- **External sources:** review sites (G2, Gartner Peer Insights, TrustRadius), "switched from X to Y" posts, LinkedIn posts where employees celebrate a win, and customer talks on YouTube.
- Collect first, judge later. A name dropped at this step is a name you never get back.

### Phase 2: extract and tier
- One row per named customer: name, industry, source, product.
- Tier each one:

| Tier | Meaning | Where it lands hardest |
|---|---|---|
| A | Globally iconic brand | Any persona, any vertical |
| B | Leader in its industry | Its own vertical |
| C | A full case study with numbers | Wherever the story matches |

- **Rule: public artifact only.** A customer becomes a row only if a public artifact names it. This is the same clearance rule as the engine.

### Phase 3: industry mapping
- Bucket every name by industry (for example financial services, healthcare, manufacturing, media, consumer goods, retail, telecom, energy).
- Goal: at least five named references per vertical you sell into. A vertical with fewer is a gap to report, not to fill with a weaker name.
- Output a copy-ready "by industry" section.

### Phase 4: quantified outcomes
- For every case study, pull each number of these kinds: money saved, payback period, scale (data volume, rows, users), percent reduction, percent improvement, velocity (for example items shipped per month), number of systems retired, time to value.
- Output an attribution table: **number | customer | source | when to use**. The "when to use" column says which pain or persona the number answers, so nobody pastes a cost number into a speed pitch.
- No number in the source means "to confirm". Never round up, never combine two customers' numbers.

### Phase 5: competitive displacement catalogue
- For each incumbent you replaced: the incumbent (or category: a do-it-yourself or open-source stack, a services-heavy vendor), where (customer names only where public), and why the customer switched (format or scale limits, end of life, cost, a failed earlier project, wrong tool for the job, product over services).
- **This becomes the trap-question tool.** Prospect runs incumbent A? Pull the matching displacement story and the question that exposes the limit that made the last customer switch.

### Phase 6: quotes library
- Capture verbatim, five fields per quote: **name, title, company, quote, source** (the document and page). A quote with no source is not usable.
- Mine customer-success and sales call recordings for quotes as well as published material, but only quotes cleared for use leave the library.
- Filter by tier, industry and theme (cost, performance, scale, migration). A quote is the best credibility line for the middle of an email.

### Phase 7: messaging output
- **Two-line about-us intro:** the umbrella claim plus five cleared names.
- **Industry swap-in packs:** five names per vertical, ready to drop into a `{{customer_list}}` style variable.
- **Intent-personalised opener:** "I read about [their signal]... similar to [peer in their industry]".
- **Trap questions:** each incumbent mapped to its phase 5 story.

### Phase 8: competitor mining (sub-workflow)
- For each of the top three competitors, run phases 1 to 6 on **their** material: their case-study pages, their review-site profiles, and "switched from us to them" posts.
- Extract: their named customers (any overlap with yours?), their claimed outcomes, the pains their customers quote, and loss-reason patterns. Treat "switched from us to them" mentions as objections to counter.
- Build a parallel competitor file with three lists: **their wins, who to defend**; **their gaps, where to attack**; **their named accounts, a cross-evaluation target list**.
- Public material only, and their claims stay their claims: never repeat a competitor's number as fact.

### Phase 9: version and cross-link
- The proof file is one node in a four-file system: the ICP definition (who we target and the priority verticals), the intent finder (which signals to look for) and the messaging spec (how we write and which proof slot goes where). Link each to the others.
- Every file keeps an update log: who, when, what changed.
- **Re-pass quarterly.** New logos appear, old quotes go stale, customers churn or rebrand. A quarterly re-pass runs phases 1 to 7 again on what is new since the last log entry, and re-checks that every named customer is still public and still a customer.

## Definition of done

Show this checklist at the end of every Mode A build, each line ticked or with its gap and the count found:

| Check | Target |
|---|---|
| Tier A names | 10 or more |
| Tier B names | 20 or more |
| Tier C full case studies with numbers | 5 or more |
| Named references per priority vertical | 5 or more in each |
| Quantified outcomes in the attribution table | 10 or more |
| Verbatim quotes with all five fields | 5 or more |
| Trap questions | Catalogued for every incumbent in phase 5 |

A library that misses a line is still usable; say which line is short and what would close it (usually one more case study in a thin vertical, or a call-recording pass for quotes). Never pad a line with an uncleared name or an unsourced number to reach the target.
