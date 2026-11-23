# Module 6: Keep fresh and reactivate (load for option 6)

Two follow-ons that turn a one-off cleanup into a habit and put the cleaned database to work. Part A keeps emails fresh automatically between runs. Part B finds the dormant records worth waking up and gives each age group its own play. Both read the CRM; the only write is switching on an automatic refresh inside the user's own enrichment tool, and that needs its own go.

---

## Part A: automatic email refresh with job-changer capture

### Why
Module 3 fixes contacts once. Then data decays again: people change jobs, mailboxes close, and the next campaign bounces. An enrichment provider that watches the CRM continuously replaces the manual re-run (on the real setup it replaced a costlier Clay plus Claude Code routine).

### Set-up (in a provider with automatic CRM management, Prospeo-type; others offer the same)
1. **Connect the CRM** to the provider (HubSpot in the reference set-up).
2. **Turn on automatic CRM management** and choose what it checks: people data, email, company data.
3. **Set the cadence.** The provider polls the CRM for new and changed records every few minutes; choose how often existing records are re-enriched, from every few hours up to every seven days. Seven days or less matches the house rule that anything entering a sequence was verified within the last seven days.
4. **Write the instructions** the provider follows (which fields it may fill, which it must never overwrite). Use the same fill-empty rule as Module 4 unless the user names a field as refreshable.
5. **Read the CRM health view** the provider shows before and after, and put the before numbers in the report.

### What it should do on each pass
| Situation | Action |
|---|---|
| Email bounces or fails the check | Mark it invalid in the CRM so it leaves every sequence |
| Person changed jobs | Record the move and fetch their new work email at the new company |
| Duplicate contacts | List them for the owner (see the guard below) |

### Job changers are a lead, not a loss
A contact who moved is gone from the old account, but if they knew you, they are a warm contact at a new company: a likely champion. Capture the new company and the new verified email, keep the old record's history, and hand the movers list to the owner as its own segment. Module 3's mover rules apply: a new email is only used if it passes a live check.

### Guards (this skill's rules win over the tool's defaults)
- **No automatic deletes or merges.** If the provider offers to remove bounced contacts or merge duplicates, prefer marking bounced contacts invalid over deleting them, and turn automatic merging off or review its suggestions: the client merges from a verified list, as in Modules 2 and 4.
- **Pilot first:** switch it on for a small segment, read back the changes it made, then widen.
- **Switching it on is a write to a live tool.** Say exactly what will be enabled, at what cadence, on which records, and wait for the go.
- Record the provider's credit balance before switching on and after the first full pass.

---

## Part B: reactivate dormant records by age

### Why
Most CRMs hold years of people who were once in a conversation and then went quiet. They already know the name. Segmenting them and giving each segment its own play produces pipeline from data the company has already paid for.

### Method
1. **Split the database: active vs dormant.** Active = a recent interaction or an open deal. Dormant = no interaction since a cut-off the user picks.
2. **Check hygiene on a sample first.** Pick a batch (a thousand records in the reference workflow) and run it through Module 3's checks before planning any outreach, so you know how decayed each age band really is.
3. **Enrich where the gaps are,** through the spend gate: a multi-provider waterfall for missing emails and titles, then intent, technographics and scoring where the user has them.
4. **Segment:**

| Segment | Who |
|---|---|
| Customers | Current customers (an upsell or expansion conversation, not reactivation) |
| Dormant 1 to 3 years | Last interaction one to three years ago |
| Dormant 3 to 5 years | Three to five years ago |
| Dormant 5+ years | More than five years ago |
| High-NPS | People who scored you highly (where an NPS or survey field exists) |
| New | Recently added, never worked |

5. **Score inside each segment** on the last interaction, the number of locations, the revenue band, and any recent news about the company. Work the top of each segment first.
6. **One play per segment.** Each segment gets its own message and its own campaign; never one message for the whole database.

| Segment | Play |
|---|---|
| Customers | Upsell or expansion through the account owner |
| Dormant 1 to 3 years | Pick up the thread: refer to the last conversation and what has changed since |
| Dormant 3 to 5 years | Re-verify first (expect movers), then re-introduce the company as it is today |
| Dormant 5+ years | Treat as cold: full re-verification, job-change check, and the normal cold sequence |
| High-NPS | A referral or case-study ask, from a person, not a sequence |
| New | The standard first-touch sequence for their persona |

### Rules
- **Suppression still applies.** Anyone who replied to a cold campaign before is not put back into a cold sequence; route them to their owner for a personal note. Anyone sent to in the last 100 days without replying waits until the cooldown ends.
- Customers, open deals and their contacts go to their owners, never into a reactivation sequence.
- Movers found in step 2 belong to Part A's job-changer segment, not to the old account.
- Every record lands in exactly one segment; say the reconcile line.

### Output
`Reactivation (YYYY-MM-DD)/` with one file per segment (ranked), the hygiene-sample result, the scoring rule used, and a README naming each segment's play and owner. The outreach itself (copy, pre-send checks, loading the sequencer) is a separate job.
