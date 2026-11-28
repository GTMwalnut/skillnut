# Daily reply log for a client-facing sheet (Option E)

Load this when the user picks Option E. It turns the one-off analysis into a recurring deliverable: every morning, new human replies from email and LinkedIn are classified and appended to a reporting sheet (or a small hosted dashboard), the summary numbers are recomputed so they reconcile, and the run ends with a short report of owed follow-ups.

It can run as a scheduled cloud routine, so the user's laptop does not need to be on.

## The one exception to read-only

The skill stays read-only on every sending tool and CRM. In this mode it writes to **one place only: the reporting sheet the user names, in the tabs and cells this file names**. Nothing else. Confirm the sheet and tabs with the user before the first write, and show them one sample row first.

## Setup (once)

| Item | What to settle |
|---|---|
| The sheet | Its id, the replies tab and the summary tab, and the exact header row |
| Sources | The email sending tool and the LinkedIn tool for this client, and which sender accounts to read |
| Start date | Replies on or after this date count |
| Exclusions | People to never add (manual outreach, test campaigns, your own domains, people removed on purpose) |
| Account lists | Optional: target-account lists used to bucket positives (for example "in the top accounts list" vs "other large company") |
| Schedule | Daily, at a fixed local time, with the time zone written in the schedule itself |
| Where keys live | Per-host secrets in the routine's environment, never in the prompt (see below) |

## Each run

1. **Read the sheet in column slices**, so no single read is too large. Check the header row matches exactly and that there are at least as many rows as last time. If either check fails, stop: you are looking at the wrong sheet.
2. **Workspace guard.** After listing campaigns in both tools, confirm two campaign names you know belong to this client are present. If either is missing, the routine is holding another client's keys: stop before any write and report it.
3. **Pull email replies from every folder** and merge them by reply id. Paging can return one row twice and skip another, so per-folder pulls are the reconciliation.
4. **Pull LinkedIn conversations per sender account.** A conversation counts when it has at least one message from the prospect.
5. **De-duplicate people across channels.** Same person when an email matches; otherwise when the normalised first and last names match and the companies share their first significant word.
6. **Find new repliers** since the start date who are not already in the sheet. Match names generously (fold accents, drop honorifics and credentials). When unsure, treat them as already present and list them under "possible duplicates" in the report. A person already in the sheet never gets a second row.
7. **Build one row per new replier** in the sheet's exact column order (see "Row fields").
8. **Append in raw mode** after the last row. Assert every row has the right number of cells first. Then re-apply the sheet's sort or filter, and read the tab back to confirm the row count and that each new name appears once.
9. **Update existing rows only for answered status:** if your side has since answered someone marked "not responded", set that cell and the date. Change nothing else.
10. **Recompute the summary tab** from the read-back: the as-of date (always, every run, so a stale date means the run failed), total replies, counts per read, campaigns live, unique people touched. Totals must reconcile (the per-type counts sum to the total). "People touched" is de-duplicated across channels and must never go down; if it would, keep the previous value and flag it.
11. **Report** in plain text (see below).

## Row fields (adapt to the client's sheet)

| Field | Rule |
|---|---|
| Our read | Positive, Nurture or Negative. **Never use "Neutral".** Out-of-office is never a reply |
| Their words | The lead's own words only, quoted, oldest to newest, with your outbound and signatures stripped; under about 600 characters |
| Channel, campaign, sender | As the tool shows them |
| Replied after | Which touch they answered (email number, connection note, LinkedIn message number) |
| Signal type and action | What you knew about them when you reached out, from a fixed list of labels. If a reply fits no label, use the closest and flag it; never invent a new label or add rows to the summary table |
| Answered by us? | Yes with the date of our first answer after their message, or "No reply visible" |
| Next action | One concrete step; for a positive with no answer, "Send the calendar link" |

**Mapping the five analysis buckets to the three client reads:** positive becomes Positive; later and referral become Nurture; not-now and negative become Negative.

## Hard rules

- **Read-only on the sending tools.** No stops, no unsubscribes, no tag changes. If a LinkedIn replier is still in an email sequence, list them under "needs a stop" in the report. Cross-channel stops belong to an automation (the n8n GTME Playbooks skill), not to this routine.
- **Write only through a sheets connector that edits cells**, never a whole-file replace. Replacing the file destroys multi-tab formatting.
- **Never locate a person by a remembered row number.** Sorting moves rows; always find them by name or row id from a fresh read.
- **Dates as text** in one fixed format; ids as integers.
- **Stop on any 401 or 403.** Do not try other credentials.

## Running it as a cloud routine

| Lesson | Detail |
|---|---|
| Keys as per-host network secrets | The routine's environment attaches each key to requests for its host, so the prompt and the session never see it. The routine sends plain requests and adds no auth headers of its own |
| Header shape per tool | Most tools take `Authorization: Bearer`. Some (HeyReach) take a custom `X-API-KEY` header with **no prefix**; a leftover "Bearer " prefix gives "401 Invalid API key" |
| One environment per client | One environment cannot carry two keys for the same host. Never point a client's routine at another client's environment; the workspace guard catches it if you do |
| Send the whole config on every update | A partial update of a routine's configuration can wipe the prompt, model and tool list. Keep the prompt in a local file and verify the stored prompt matches it after every update |
| Routines can be re-created under a new id | If the id in your notes returns nothing, list routines by name and re-check connector, tools, prompt and environment before trusting it |
| Test once, then enable | Create it disabled, run it by hand, read the full report (a green status only means no infrastructure error), then enable the schedule |

## Variant: hosted client page instead of a sheet

Some clients want a page, not a sheet. Same pull and classification, then one self-contained HTML page: LinkedIn section first, then email, then a one-line summary per replier. Put it behind a password, keep the password as an environment variable on the host (never in a file), and deploy it from the routine each morning. Write the as-of date from one fixed time zone so consecutive runs agree. The full refresh order (fetch the live page, decrypt, update the data, validate, re-encrypt, deploy, verify) and the analytics-tab reconciliation rules are in `client-reporting-layer.md`.

## The run report

- Rows added: number, name, company, read, channel, campaign, reply date (or "none")
- Existing rows switched to answered
- Summary before and after: replies by read, campaigns, people touched
- Needs a stop: LinkedIn repliers still in an email sequence
- Possible duplicates skipped
- Owed follow-ups: Positive or Nurture rows still "not responded", names only
- Anomalies: API errors, counts that went down, sums that did not reconcile, approximated labels

## Model report (illustrative numbers only)

> Daily reply log, run complete. Added 3 rows: 2 Nurture (LinkedIn), 1 Positive (email, campaign "Q4 platform leads"). Switched 1 existing row to answered. Totals now 48 replies: 11 Positive, 26 Nurture, 11 Negative; 31 live campaigns; 2,950 unique people touched (up 40). Needs a stop: 1 LinkedIn replier still in an email sequence. Owed follow-ups: 2 (both Positive, no answer yet). No anomalies.
