# Daily run and the morning alert email (Mode E, optional daily schedule)

Load this when the user wants the dashboard to refresh itself every day and wants to hear only about what needs action. It turns a page someone has to remember to open into a short email that comes to them.

Two parts, kept apart on purpose:

| Part | What it does | Where it runs |
|---|---|---|
| The daily refresh | Re-pulls the sending tool, re-runs the DNS, age and blacklist checks, recomputes the snapshot and the page | A scheduled cloud routine (Claude routines), so the laptop can be off |
| The alert email | Runs a handful of checks on the fresh data and emails the user one short message, only when something needs action | The same routine, as its last step before publishing, through the user's own mail connector |

The refresh and the alert never change anything in the sending tool. They are the same read-only pull as the dashboard. The autopilot (Mode F) is the only part of this skill that writes; on the reference setup it runs in the same routine, between the refresh and the alert, with its own rules.

## Setup (once)

| Item | What to settle |
|---|---|
| Schedule | Daily, at a fixed local time, with the time zone written into the schedule itself (for example `CRON_TZ=<zone> 30 7 * * *`) |
| Keys | One per-host secret in the routine's environment for the sending tool, one for the placement-test tool if the user has one, and one for any paid blacklist feed. Never in the prompt, never in the page |
| Where the page lives | A local folder the user opens, or a private hosted page. A hosted page that shows client domains goes behind a password |
| Where the alert goes | One address, normally the user's own. The email is sent **from** the user's own mailbox **to** itself |
| The mail connector | Attach the user's mail connector (Gmail, on the reference setup) to the routine, and allow only its send tool. See below |
| The checks | Start from the five defaults below; the user's own thresholds override. The optional extras are off unless asked for |

**Connecting the mail account.** A routine can only use connectors attached to it. Attach the user's Gmail connector to the routine and add only its send tool (`send_message`) to the routine's allowed tools, nothing that reads or searches mail. Then put this hard rule in the routine prompt: *the only email this routine ever sends is the alert email, only to the one agreed address; never read, search or send anything else.* Send a sample from a normal session first so the user sees exactly what will land, and whose name it comes from, before the schedule is on.

## The routine prompt (shape)

Keep the full prompt in a local file and paste it whole. It carries:

1. **Read-only, always,** for the refresh and the alert. GET and list calls only. If a call fails with 401 or 403, stop and report; never try other credentials.
2. **Secrets.** Never print, log or write a credential. Check a variable exists only with `[ -n "$NAME" ] && echo NAME set`.
3. **Workspace guard.** After the first pull, confirm one or two campaign or inbox names the user knows belong to this workspace. If they are missing, stop before writing anything: the routine is holding the wrong key.
4. **Run the generator with `--refresh`** (busts both the API cache and the DNS cache), then the verification checklist from the build recipe: counts reconcile, no key in the output, no external URL.
5. **Always stamp the run date** on the page, even when nothing moved. A stale date is how the user knows a run failed.
6. **Run the alert script**, which writes three files (`alert_subject.txt`, `alert_body.html`, `alert_body.txt`) and prints `ALERT_ITEMS: N` last. If N is 0, send nothing. Otherwise send exactly one email: subject from the subject file, `htmlBody` from the HTML file, `body` from the text file as the plain-text fallback, copied unchanged. If the script crashes or the send fails, send a push notification saying so and carry on.
7. **Report** in plain text: health score before and after, what the autopilot did if it runs, the alert count and whether the email went, anything that failed or could not be checked.

Write the alert script so the routine only copies files into the send call. The cloud agent reformatting or summarising the email is how the format drifts; the prompt says "do not add, remove, reword, summarise or reformat anything".

## The five default checks

These are what the user hears about every morning. Everything else is on the dashboard.

| # | Check | Fires when | Why this line |
|---|---|---|---|
| 1 | Warm-up falling below 60 | The inbox's score falls at **every** step, 30-day > 14-day > 10-day > 7-day > 3-day, **and** the 3-day score is under 60 | A score that only dipped once is noise. One falling at every step and already under 60 is an inbox about to burn. Use the sequencer's own windows (Email Bison returns a score for any date window), not a home-made trend |
| 2 | Spamhaus / SURBL listing | A sending domain answers listed on Spamhaus DBL or SURBL (positive controls passed) | A listing hits every inbox on the domain at once |
| 3 | Disconnected inboxes | The sending tool's connection status is anything other than connected | A disconnected inbox neither sends nor warms, and nothing else tells you |
| 4 | Bounce rate over 5% (last 7 days) | An inbox bounced more than 5% of what it sent in the last 7 days, with at least 20 sent, **after removing security-gateway bounces** | Gateway bounces (Mimecast, Proofpoint, Barracuda) are already known and routed (chapter 5); a bounce spike without them points at the list or the inbox |
| 5 | SPF / DKIM / DMARC missing | A sending domain has no SPF, DKIM or DMARC record | Without them receivers reject or spam-folder the domain's mail |

How the bounce check works, because the sending tool will not hand it over directly:
- **Sent in the last 7 days:** inbox records carry only a running total (`emails_sent_count`). Save each inbox's total in a small history file every day (`rotation/alert_history.json`, 10 days kept, shipped with the state), and take today's total minus the total from up to 7 days ago. The check starts once one day of history exists; until then the email says "Not checked yet", never "No issues".
- **Bounces:** replies in the Bounced folder from the same window, attributed per inbox by `sender_email_id`.
- **Gateway bounces removed:** drop any bounce whose notice names a gateway (mimecast, proofpoint, pphosted, barracuda) or whose recipient is a lead tagged with a gateway.
- This is a per-inbox early warning. It does not replace the ~2% campaign auto-pause in chapter 7, which stays on inside the sending tool.

**A check that could not run is itself an alert.** If the blacklist lookup failed (for example a paid Spamhaus key stopped working), the listings section says so and a note at the bottom says which check did not work. A failed check must never read as clean, and the note alone is enough to send the email.

## Optional extra checks (off unless the user asks)

The dashboard already shows these; add any to the email only on request, one row each:

| Flag | Fires when |
|---|---|
| Health below the investigate line | The weighted health score is under 80 |
| Inbox over its cap | Configured daily limit above 15 for Google or 5 for Microsoft and SMTP (moot if the autopilot sets limits) |
| Warm-up slipping | An inbox's warm-up score under 85 |
| Landing collapse | A domain's out-of-office and auto-reply rate falls toward zero while sibling domains hold |
| Dead inbox | Zero replies of any kind over two weeks of real sending while siblings reply |
| Rest split off | Fewer than about 30 percent of inboxes resting in warm-up-only |
| Copy defect | A live campaign with a link, open tracking on, no spintax, one subject for every send, or a body over 120 words |
| New gateway pool | The share of leads behind hard gateways grew since the last run |

## The email format

Built and tested with a real operator; each rule came from their feedback on a draft.

- **HTML with tables**, plus a plain-text copy as the fallback. A plain list of lines was too hard to read.
- **Subject:** the date and what fired, for example `Deliverability alert 2026-03-04: 3 warm-up falling below 60; 1 spamhaus / surbl listings`.
- **Top: a summary table of all five checks**, one row each: number, check, result. Results are colour-coded: red "N inboxes flagged", green "No issues", grey "Not checked yet", amber when a check only partly worked.
- **Then five numbered sections, one per check, divided by a rule.** Each has only its heading, then either a table of the flagged items or a one-line remark: "No issues.", or why it was not checked. **Every check always appears**, including the clean ones; the user wants to see that SPF, disconnections and bounces were checked, not guess from their absence.
- **No explanation lines under the headings.** The operator found them unnecessary; the heading says what the check is.
- **Tables:** warm-up shows client, inbox, then the 30, 14, 10, 7 and 3-day scores with the 3-day score in red, worst first. Listings show client, domain and the list. Bounces show client, inbox, bounced, sent, rate.
- **Note box at the bottom** only when a check did not work.
- **Keep the HTML small:** table `border` and `cellpadding` attributes instead of a style on every cell (a full inline-styled page ran to about 18 KB; the attribute version is about 6 KB), because the cloud agent has to pass the whole file through one tool call unchanged.
- **One email for all clients together.** Group by client inside the tables, not one email per client.

## Watcher-agent alternative

If the user does not want the routine itself to send mail, write the same items to `red_flags.json` next to the snapshot (one entry per flag: severity, entity, benchmark, current value, fix) and point their always-on agent at it. The same rules apply: only what needs action, new flags first, never act on a flag, and name the entity and the fix in one line.

## Test once, then enable

Create the routine, send one sample email from a normal session, then run the routine by hand and read the full report and the email with the user before turning the schedule on. A green run status only means no infrastructure error; it does not mean the numbers are right. Check the page date moved and two figures against the sending tool.
