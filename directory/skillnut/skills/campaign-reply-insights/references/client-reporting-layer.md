# The client-facing reporting layer (Option E, after the reply log)

Load this with `daily-reply-log.md` when the user wants more than the reply rows: a summary tab the client reads first, a morning report the team acts on, or a password-gated page the client opens instead of a sheet. It sits on top of the daily reply log; the pull, the classification and the row rules stay as that file says.

Three parts, all run by the same daily routine:

| Part | What the client or team sees | The rule that makes it trustworthy |
|---|---|---|
| The analytics tab | One summary tab in the reporting sheet: headline numbers with remarks, and small cross-tab tables | Every table reconciles to the reply rows, every run |
| The morning report | A plain-text report to the team | Stops still needed and follow-ups owed are named, not counted |
| The client dashboard (optional) | A password-gated web page with the same numbers and the replies | Decrypt, update the data, re-encrypt, deploy, verify, every day |

## 1. The analytics tab

### Layout

Agree the layout once with the user, then follow the **labels**, never remembered row numbers. If a label has moved, follow the label. Typical blocks:

| Block | Rows | Columns |
|---|---|---|
| As-of | One cell with today's date | Moves every run, even when nothing else does |
| Headline numbers | Campaigns live; contacts touched; total replies; positives (split into buckets if the client uses target-account lists); nurture; dropped or not interested | A number column and a remark column |
| Replies by signal type | One row per signal type from the fixed label list (what you knew about the person when you reached out), including a "signal not pulled" row | Human replies, Positive, Nurture, Neutral (always 0), Negative, and the channel |
| Replies by action type | One row per action within one signal type (for example, for a code-repository signal: pull request or issue, comment, star, fork, action not pulled), then a Total row | Replies, Positive, Nurture, Neutral, Negative |

### How each number is computed

- **Campaigns live:** email campaigns that are not draft, completed or archived, plus LinkedIn campaigns that are not draft. Leave out test campaigns by name. The remark states the split ("live: N email + N LinkedIn") and, when a campaign appears that was not there last run, appends "new since <date>: <name>".
- **Contacts touched:** email leads with at least one email sent, plus LinkedIn leads with a connection or message status set, counted per channel and labelled "per channel, not de-duplicated" in the remark. If the long lead pull fails part-way, keep the previous value and say so in the report; never write a partial count.
- **Total replies:** the number of data rows in the reply log.
- **Positive buckets (optional):** when the client keeps target-account lists in the sheet, look each new Positive's company up in them (case-insensitive, punctuation and suffixes such as Inc, Ltd, Group, Corporation dropped, a match when one name contains the other). Found: add one to the "in the target list" bucket and append "<Company> - <signal in two or three words>" to its remark. Not found: the other bucket, same remark format. Never move or remove an existing remark entry. Say in the report which bucket each new Positive went to and why.
- **Nurture:** count of Nurture rows. The remark lists notable companies only (large or widely known); add a new one only when it meets that bar, keep the existing names.
- **Dropped:** count of Negative rows; append each new company to the remark with a short reason in brackets when the reply gives one.
- **Signal table:** count rows by signal type, split by read. The channel column says one channel when every row shares it, otherwise "<majority> (<n> by <minority>)", or "Mixed" on an even split.
- **Action table:** count only the rows of its parent signal type, by action type.

### It must reconcile

Read the tab back after writing and check, every run:

1. The signal-type totals sum to total replies.
2. Positive + Nurture + Negative across the signal table equals each row's total, row by row.
3. The action-type rows sum to the action table's Total row, column by column, and that Total row equals the parent signal type's row in the signal table.
4. The headline Positive, Nurture and Dropped counts equal the read counts in the reply rows.

If a sum does not reconcile, fix it before finishing. If you cannot, say so at the top of the report. A summary that does not add up is worse than no summary: the client stops trusting every number on it.

### Write rules

- Write a cell only when its value changes, except the as-of date, which is written every run (a stale date is the record of a failed run).
- Numbers as integers, remarks as text, raw input mode, through a cell-level sheets connector.
- **Never add rows to a table.** If a reply needs a signal or action type that has no row, use the closest label and flag it in the report.
- Run this tab's update even when there are no new replies: the as-of date, campaigns and contacts touched still move.

## 2. The morning report

Plain text, no secrets, no raw API dumps. In this order:

1. Rows added, one line each: number, name, company, read, channel, campaign, reply date (or "none").
2. Existing rows switched to answered, with the date.
3. Analytics before and after: total replies, Positive / Nurture / Negative, campaigns, contacts touched; for each new Positive, which bucket and why.
4. **Stops still needed:** LinkedIn repliers who are still in an email sequence, by name, with the email tool's lead and campaign ids. The routine never stops them itself; stops belong to the cross-channel automation (n8n GTME Playbooks skill) or a person.
5. Possible duplicates skipped.
6. **Follow-ups owed:** Positive or Nurture repliers with no answer from our side, names only, Positives first.
7. Anomalies: API errors, counts that went down, sums that did not reconcile, labels approximated, existing people who wrote again.

## 3. The password-gated client dashboard (optional)

Some clients want a page, not a sheet. The page is one self-contained HTML file. Its data lives in a single line in the page script (`const DATA = {...};`), and the whole page is encrypted inside a small password gate page, so the hosted file holds only ciphertext. The client types the password; the browser decrypts and renders.

### The data shape (adapt to the client)

```
{"asOf": "<date>",
 "linkedin": {"campaigns": [{"name": "...", "status": "live|paused|completed|draft",
                             "v": [totalLeads, requestsSent, accepted, messagesSent, inmailsSent, replies, interested]}]},
 "email":    {"campaigns": [{"name": "...", "status": "live|paused|completed|draft",
                             "v": [contacted, replies, bounces, interested]}]},
 "responses": [{"channel": "LinkedIn|Email", "at": "<ISO UTC>", "name": "...", "role": "Title, Company",
                "tag": "...", "campaign": "...", "replies": [{"at": "<ISO UTC>", "text": "..."}]}]}
```

### The daily refresh, in order

1. **Fetch the page that is live now** through the hosting provider's API (list the production deployments, take the newest ready one, read its `index.html`). Fall back to the public URL only if the API route fails. If both fail, stop.
2. **Decrypt.** Read the salt, IV, ciphertext and iteration count from the gate page; derive the key from the password with PBKDF2-SHA256 and decrypt with AES-GCM 256. The plaintext is the dashboard HTML. Parse the `DATA` line. If decryption fails or the line is missing, stop and report; never rebuild the page from scratch.
3. **Pull** campaign stats from the email tool and the LinkedIn tool, and new human replies (same filters as the reply log: inbox type, not automated, out-of-office and "no longer with the company" auto-replies dropped).
4. **Update the data.** Rebuild each campaign row from the tools, with a fixed status mapping. Keep every existing response exactly as it is, hand-written tags included; only append new people. A LinkedIn reply counts only if it came after the campaign started. Tag each new person with one label from a fixed list agreed with the client (for example Interested, Not interested, Referral, Left company, Wrong person, Acknowledged); never invent a new tag.
5. **Keep the page code consistent.** If the page groups campaigns by name family, a clearly new family gets one new group line; otherwise leave code, CSS and layout alone.
6. **Validate.** The data parses; the page script passes a syntax check; every count is a whole number of zero or more with the right number of fields per channel. Compare with yesterday: cumulative counts (sent, accepted, contacted, replies) normally never go down; if one does, note it and continue.
7. **Re-encrypt** with the same password, a new random salt and IV, and the same iteration count. Decrypt your own output once and confirm it matches the new dashboard byte for byte.
8. **Deploy** the new gate page to production through the hosting API, and poll until it is ready (stop on error or after a few minutes).
9. **Verify.** Confirm the newest production deployment is the one you just made; then, if the public URL is reachable from the routine, fetch it, decrypt it and check it shows today's as-of date. If the routine's network blocks the public URL, say so; that is not a failure.
10. **Report:** as-of written, deployment id, verification result, per-channel totals before and after (labelled in field order), new or changed campaigns, new responses one line each, and anything skipped.

### Rules for the dashboard

- **Always deploy**, even when nothing changed. The daily deployment and the as-of date are the record that the refresh ran.
- **The password lives in one environment variable** on the routine. Never print it, log it, or write it to any file that is deployed or committed. The exact current password is required: a different one breaks the run and the client's login.
- **Write the as-of date in one fixed time zone** so consecutive runs agree.
- **The deploy is the one write outside the sheet.** It goes only to the client's own dashboard project. Confirm it with the user once at setup, run the first refresh by hand together, then enable the schedule.

## Running it as a routine

Both the sheet update and the dashboard refresh run as scheduled cloud routines (one per client), with the lessons in `daily-reply-log.md`: keys as per-host network secrets, one environment per client, the workspace guard by known campaign names, test once by hand, then enable. Two routines for one client should not run at the same minute; stagger them.

## Model report (illustrative numbers only)

> Client dashboard refreshed. As-of today, new deployment ready and verified (decrypted the live page, today's date shows). LinkedIn: requests 1,420 to 1,465, replies 61 to 63. Email: contacted 3,900 to 3,980, replies 44 to 45, bounces unchanged. 3 new responses: 2 Interested, 1 Referral. No counts went down. Sheet: 3 rows added, analytics reconciles (48 replies = 11 Positive + 26 Nurture + 11 Negative; action rows sum to their total). Stops still needed: 1. Follow-ups owed: 2.
