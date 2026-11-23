# Modules 2 and 3 - The scoring model and scoring a batch

Load for Module 2 (design) and Module 3 (score a batch, sections 4 to 6).

## 1. Three inputs, weighted in order

`score (0 to 100) = deal-history fit x w1 + record signals x w2 + seed ICP (or live research) x w3`, each input scored 0 to 100 first.

| Input | What it reads | Weight |
|---|---|---|
| 1 Deal-history patterns | Does this record look like the fastest-closing, highest-value wins (industry, size or revenue band, contact title)? Does it look like losses (push it down)? | Highest, once history is deep enough |
| 2 Signals already on the record | Intent topics matched, lead source quality, appears in two or more sources, third-party intent strength or tier, signal confidence, title seniority and function, firmographic fit | Medium, always on |
| 3 Seed ICP, then live research | While history is thin: the user's ICP rows (target industries with a weight each, size band, required systems or regulatory drivers). With deep history: live research on strong-fit records | Lower once history is deep |

## 2. Cold start: let the history earn its weight

The deal-history input gets no weight until enough deals have closed, and the seed ICP gives way as they do. Count closed deals as won plus lost plus no-opportunity.

| Step | Closed deals | Deal history | Record signals | Seed ICP |
|---|---|---|---|---|
| Cold | Below the first threshold | none | medium | most |
| Warming | Between the thresholds | some | medium | some |
| Learned | Above the second threshold | most | medium | least |

Illustrative only: first threshold 15, second 30; deal history / signals / ICP weights moving from 0/45/55 to 25/45/30 to 50/35/15. Set the real values with the user and write them in the scoring sheet. Keep the second threshold in line with the calibration point in buying-signals-playbook (about 30 closed deals) if the user runs both.

If there is no scoring context yet, treat the closed-deal count as zero, skip input 1, and stamp the version `cold_start`.

## 3. Writing the rows

- **Deal-history rows** come from `win-loss-read.md`: won industries, won size band, won titles (boost); lost industries and titles (downweight).
- **Record-signal rows**: rank the lead sources by quality with the user (a first-party website visit or hand-raise usually beats bought intent, which beats a cold database). Cross-source presence is a multiplier, not an add-on (illustrative: x 1.1 to x 1.3). For intent and trigger signals, take the list, windows and decay from **buying-signals-playbook**; do not invent a second decay rule here.
- **Seed ICP rows**: one weight per target industry (illustrative: 1.0 for the best fit, lower for each weaker industry), the size or revenue band, and any system or compliance driver that makes the need real (boost per confirmed driver).
- **Negative rows**: out of market, wrong geography, competitor, agency or consultancy, student or job seeker. A hard disqualifier removes the record before scoring; run **icp-fit-filter** first for lists full of non-buyers.

## 4. Pass 1: score everything (fast)

For every record: read it, score the three inputs, combine, set the tier, write the rationale. Records missing the basics (no company or domain) are not guessed: give them the lowest tier with low confidence and list them as skipped for missing data.

**Per record, always write:**

| Field | Content |
|---|---|
| Score | 0 to 100 |
| Tier | Priority, Active or Initial (or the user's names) |
| Rationale | Two to four sentences a rep can act on: who they are, which winning pattern they match, which signal is live |
| Factors | Each factor with high, medium or low influence |
| Confidence | High, medium or low (low when fields were missing or the title pattern came from few deals) |
| Recommended action | The tier's action |
| Scored at, model version | When, and which version of the weights |
| Research done | False after pass 1 |

Example rationale (illustrative): *"Head of IT at a mid-size manufacturer. Four of your last ten new-business wins were manufacturers in this revenue band, closed by IT directors. They posted two cloud infrastructure roles this month, which points to an active modernisation project."*

## 5. Pass 2: live research on strong-fit records

- **Who qualifies:** records in the top two tiers with company and domain filled, that do not already carry plenty of intent signals. Research the ones that fit but have no behaviour yet.
- **Once per company:** group by domain, research once, apply to every lead there. That is also the account score (section 7).
- **A short fixed menu** of searches per company (illustrative: two or three, one more only if none find anything): new leader hired in the buying function, job posts for the work you support, a transformation or project announcement, then funding, acquisition or restructuring.
- **Classify each result:** Signal found, Signal not found, Signal irrelevant. Found needs a dated, public source.
- **If found:** re-score the record from scratch with the evidence in the rationale. **If not:** the pass 1 score is final.
- **Time box** the pass. When time runs out, finalise the rest at their pass 1 score and log how many.
- Mark research done on every record either way. Nothing downstream (routing, sequences, write-back) acts on a record until research is done.

## 6. Tiers and the queue

| Tier | Meaning | Action |
|---|---|---|
| Priority | Strong match to winning patterns plus an active signal | Personal outreach fast (the user sets the hours) |
| Active | Partial fit or early signals | Nurture sequence |
| Initial | Weak fit or not enough data | Monitor only, no outreach |

- **Set the tier lines from the distribution and the team's capacity**, not from a round number: Priority should be a list the team can actually work inside the response time. Show the histogram, propose lines, let the user move them.
- **Queue order:** the very top scores go first regardless of age, then the user's source order inside the same band. A new high score jumps older, lower ones.
- **For inbound and MQL models** (forms, site visits, email engagement): the same tiers map to lifecycle. Crossing the Priority or MQL line sets the stage and alerts the owner; an urgent hand-raise goes straight to a person; a disqualifier routes to suppression. Build the routing with the CRM playbooks.

## 7. Accounts versus leads

- The **account score** uses the company-level parts: industry, size, deal history at that account, company signals and research. Score it once per domain.
- The **lead score** is the account score plus the person: title fit against won titles, seniority, their own engagement.
- Show both when a rep works by account: the account tier decides whether to work it, the lead scores decide who to call first.

## 8. Back-test before sign-off

Score the last stretch of closed deals with a model built only on the deals before them. Priority should win more often than Active, and Active more than Initial. If not, show it, and adjust rows before tier lines.
