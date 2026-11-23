# Research, verified mode (loaded on demand)

Verified mode is the Research module with three extra passes bolted on: an evidence tier per account, a re-verify-or-downgrade pass before anything ships, and a structural audit that proves itself with a planted mistake. Everything in the main Research method still applies (signal map, process state over events, receipts, freshness gate, the hygiene passes).

Use it when any of these is true:
- The list goes out under a client's name, or to senior readers in a regulated field.
- Openers name a competitor tool or a specific portal.
- The research was done by sub-agents, a prior session, or in many batches. Agent-sourced is not verified.
- The list is large enough that nobody will read every row by hand.

---

## 1. The three evidence tiers (one per account)

| Tier | What it means | How the opener reads |
|---|---|---|
| Named tool | A specific vendor or product is identified for the process: the portal's own domain or subdomain, a page footer, the processor named in the privacy policy, a job post naming the tool, a vendor case study | Names the tool, what they use it for, and how the work is split around it |
| Own portal | Their own branded portal, form, committee or intake page is confirmed, but the vendor behind it is not pinned | Names the portal or form and how intake is split, never guesses the vendor |
| No public sign | No public intake point or tool found. Remember: no visible tool does not mean no tool | Claims no tool. Says where the work likely lands ("likely through the operations team", "likely through a shared inbox"), as curiosity, not as a certainty |

Expect most accounts in a broad list to land in the third tier. That is normal, and an honest softer opener beats a fake specific one. Say the split out loud in the handover, so the user knows how many openers are named-tool zingers and how many are gentle.

## 2. The two-line opener per tier

Account-level, two lines, then the user's own bridge and ask (or the Write module's) as line 3.

- **Line 1:** the named tool (or portal), what they use it for, and how the work is split (portal versus email, first step versus second step, by division, by country, separate tracks). Stated plainly, out of curiosity. Never the words "inefficient" or "fragmented": the plain statement is the lightbulb ("huh, we really do have three front doors").
- **Line 2:** a consolidation question ("Ever thought about one portal for the intake and all those approvals?") **only** when the account is genuinely split, or in the no-public-sign tier. If they already run one end-to-end system, line 2 is a genuine curiosity line instead. Never ask "one portal?" of someone who already has one.
- Agree the exact wording of the recurring question with the user once and keep it fixed. Ambiguous metaphors ("front door") read oddly when repeated across hundreds of rows; a plain noun ("one portal") does not.

Example (invented company and tools):
> Hi Priya,
> Noticed Calder Foods takes new supplier applications through VendorHub, then splits them out to each region's approval team.
> Ever thought about one portal for the intake and all those regional approvals?

## 3. The re-verify-or-downgrade pass

Run it after the openers are written and before the person-level expansion. The rule for every row: **confirm with a source quote, or downgrade to the no-public-sign tier.**

1. Take every account whose opener makes a specific claim (the named-tool and own-portal tiers). Named-tool accounts are checked one by one; own-portal accounts in batches of about 30.
2. Re-open the actual page live. Not the research notes, not memory, not a sub-agent's summary.
3. Record one verdict per account:

| Verdict | When | What happens to the opener |
|---|---|---|
| CONFIRMED | The page still says it | Unchanged. The verbatim quote goes in a Verify Quote column |
| CORRECTED | The page says something different (a different vendor, a portal retired, the page is for another function) | Rewritten to what the page actually says, re-tagged |
| DOWNGRADED | Cannot be confirmed (page gone, will not render, blocked) | Rewritten to the no-public-sign tier: claims no tool |

4. Add a freshness note when a change is announced but not yet live ("intake moving to a new vendor around [date]"). The claim stays only if it will still be true on the send date.

Traps that this pass catches (all seen in real runs):
- **One vendor hosts different functions.** A vendor-hosted portal on the account's subdomain may be for something else entirely (patent submissions, job applications) rather than the process you sell into. Check what the page is for, not just whose domain it is.
- **A page that does not render is "tentative", not confirmed.** A blocked page (403) is dropped unless another source confirms the same fact.
- **A claim that was true last year.** A retired portal, a closed acquisition, a program that was paused and restarted. Durable facts hold; anything with a date needs the date gate.

Illustrative outcome, to set expectations: in a run of this pass on a few hundred accounts, roughly two in three own-portal claims were confirmed, about one in four needed correcting, and about one in eight had to be downgraded. A pass that confirms everything was probably not live.

Tool order for the pass: your own knowledge first, then the built-in web search and fetch, then paid search tools only when the built-in one is exhausted or a page blocks it. Tell any sub-agent to follow the same order.

## 4. The structural audit, with a planted swap

After the account openers are expanded to one row per person (greeting swapped per contact), prove the file is wired correctly. Four checks:

1. **Counts reconcile.** Every researched account appears exactly once in the master: none missing, none duplicated.
2. **Every opener names its own company.** Compare the opener text against the company name: a significant word of the name (four letters or more, not a generic suffix like "group" or "health"), or the core of the domain, or the acronym near the start. This check is strong because it compares two independent fields.
3. **Every contact got their own domain's opener.** Zero cross-wiring between accounts.
4. **The company label matches the source list** for each domain.

Then the part most audits skip: **the negative control.** Copy the file, swap the openers between two unrelated accounts, relabel one company to nonsense, and run the same checks on the copy. They must flag exactly the planted rows. If they do not, the check is broken, and the real file's "0 problems" means nothing.

Finish with a reproducible random sample: pick about 12 accounts with a fixed seed, so anyone can draw the same sample again, and trace each one by hand from opener to source page.

Be honest in the report about which checks are strong (they compare independent fields) and which are circular (they re-check something the build step produced deterministically).

## 5. Other things verified mode handles

- **Source-list artifacts.** When a contact's email domain does not match the company on the list (a big-company email labeled as a small startup), write the opener to the actual email-domain employer, because that is who receives it, and note the row.
- **Acquired or defunct accounts** go to a review file, not the send file. Their old-domain emails will likely bounce; retarget the parent if the user wants.
- **Non-fit accounts found during research** (suppliers, consultancies, competitors) are flagged and the flag is sticky: it survives every rebuild of the send list, so a removed account cannot quietly come back.

## 6. Output additions

Add these columns to the openers file: Evidence Tier, Verify Verdict, Verify Quote, Confirmed/Inferred, Line 2. Add a short verification log per tier, and the audit output (the planted-swap result, the four checks, the sample) as a section of the handover.
