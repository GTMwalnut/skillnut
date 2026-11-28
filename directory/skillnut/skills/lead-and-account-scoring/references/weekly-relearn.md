# Module 5 - Weekly re-learn

Load for Module 5. The model gets better as deals close, without anyone tuning rules by hand.

## 1. The run (once a week)

1. Re-read the full deal snapshot (`win-loss-read.md` section 1). If the CRM read fails, skip this week's update, keep the current version, log it, and try again next week. Never learn from a partial read.
2. Count closed deals (won plus lost plus no-opportunity). If the count crosses a cold-start threshold, move to the next weight step (`scoring-model.md` section 2).
3. Recompute won and lost patterns: industries with the best win rate, size band of won accounts, titles on won deals, industries and titles on losses.
4. Write the new scoring context: won patterns, lost patterns, seed ICP, input weights, closed-deal count, and a new version (a timestamp works).
5. Flag records for re-score: Priority and Active records last scored before this version, plus any record whose matching pattern changed.
6. Write the run log and the change note.

## 2. The change note (to the named person)

Short, plain English:
- Closed deals since last week and the new total.
- What changed in the patterns and weights, and why (for example: "Three of this month's fastest new-business wins were mid-size logistics companies, so logistics rose in the industry weights").
- Records flagged for re-score and how many may change tier.
- Tier distribution this week versus last.

## 3. The run log

| Field | Content |
|---|---|
| Run mode | daily scoring or weekly re-learn |
| Records processed | count |
| Tier distribution | count per tier |
| Changelog | list of weight and pattern changes (re-learn only) |
| Change rationale | why (re-learn only) |
| Research time-box hit | yes or no, and how many finalised at pass 1 |
| Errors | list, empty if clean |
| Started, completed | timestamps |

## 4. Guardrails

- A new version scores future runs and flagged records. Old rows keep the version they were scored with, so any score can be traced to the weights that made it.
- Show the user the first few change notes before letting it run unattended.
- Score decay: rather than a timer that quietly lowers scores, re-score on the weekly run; intent and trigger signals age out through the decay rule in **buying-signals-playbook**.
- Writing re-scores back to the CRM follows `crm-write-back.md`; a standing go for weekly re-scores must be given explicitly and names the score properties only.

## 5. Running it on a schedule

Hand off to **crm-agent-autopilot** to run this as a recurring job (a scheduled routine, the CRM's own workflow agent or a self-hosted agent), with its trigger, named writes, approval point, run log and sandbox test first. Daily scoring of new leads can run the same way: score new records each day, re-learn weekly.
