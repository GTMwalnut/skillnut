# Inbox rotation autopilot (Mode F): the method and the routine

This file is the engine for Mode F. Read it at Stage 3 of Mode F, before the first API call. The autopilot does three jobs every morning, with nobody watching:

| Job | What it does | Section |
|---|---|---|
| Rotation | An inbox whose warm-up score is falling comes out of every live campaign to rest, and goes back into the same campaigns once it has recovered (chapter 3's "demote on signal", automated) | 1 to 3 |
| Onboarding | A brand-new inbox joins its sender's live campaigns once it has 14 days of warm-up behind it and healthy scores | 4 |
| Daily limits | Each inbox's daily sending limit follows its warm-up score, so a slipping inbox sends less before it has to come out | 5 |

Reference implementation: Email Bison, run as a scheduled Claude Code routine (a cloud task on a cron schedule; the user's laptop does not need to be on). It has run live on real client workspaces. Other sequencers qualify only if their API exposes (a) warm-up score per inbox over a date window, (b) campaign membership per inbox, (c) attach, detach, pause and resume, and (d) a writable daily limit per inbox. Probe for all four before promising the mode (engine: the probe ladder). If (a) to (c) are missing, say so and offer the daily watch-list report instead (section 10, report only). If only (d) is missing, run rotation and onboarding and leave the limits to the user.

---

## 1. The rotation rules

Read the sequencer's warm-up score for every inbox over four windows: the last **3, 7, 10 and 14 days** (Email Bison: `GET /api/warmup/sender-emails?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`; each row carries `warmup_score`, `warmup_emails_sent`, `warmup_enabled`). **This endpoint returns 15 inboxes per page whatever you ask for. Follow `meta.last_page` to the end**, or every inbox past the fifteenth silently gets no score and is treated as "no data" (seen on the reference run, where only the first page came back).

Verdict per inbox, evaluated in this order:

| Order | Condition | Verdict |
|---|---|---|
| 1 | warm-up is disabled on the inbox | `no-data` (leave alone) |
| 2 | no 3-day score, or fewer than **5** warm-up emails in the 3-day window | `no-data` (too little data to trust; report it) |
| 3 | 3-day score **below 80** | `remove` |
| 4 | **steady decline**: 3d < 7d < 14d, AND 3d at least **5** points under 14d, AND 3d under **90** | `remove` |
| 5 | 3-day **and** 7-day scores both **90 or more** | `restore-ok` |
| 6 | anything else | `hold`; if the 3-day score is under 90, put it on the **watch** list |

Defaults agreed with the operator on the reference run: `REMOVE_BELOW = 80`, `RESTORE_AT = 90`, `TREND_DROP = 5`, `TREND_CEILING = 90`, `MIN_WARMUP_SENT = 5`. Expose them as named constants at the top of the script and say them to the user before the first run; let the user change any of them.

How these relate to the chapter 3 flag: **below 85 is a flag to watch; below 80 is the action line.** The gap between them is deliberate: the watch list sees an inbox slipping days before the autopilot pulls it.

**Warm-up is never switched off.** Removal takes an inbox out of real sending only; it keeps warming, which is how it recovers.

---

## 2. What the autopilot does with each verdict

- **`remove`, inbox not already held out:** find every campaign the inbox is in whose status is live (`active`, `queued`) or idle (`paused`, `draft`, `pending`) **and** where it is actually attached (see the membership gotcha in section 3). Detach it from each one. Record in the state file which campaigns it came out of. If it is in no live or idle campaign, put it on the watch list instead ("not in any live campaign").
- **Inbox already held out, verdict `restore-ok`:** re-attach it to exactly the campaigns it came out of. Skip campaigns that have since ended (status no longer live or idle) and say so. If some re-attaches fail, keep only the failed ones in the state file and retry them tomorrow.
- **Inbox already held out, any other verdict:** keep it out. **Self-heal:** re-check each recorded campaign, and if the inbox is attached again (a removal that didn't stick, or someone re-attached it by hand), detach it again and log a `re-remove`.
- **Inboxes someone removed by hand are never restored.** The autopilot only restores what it removed, because only the state file knows where an inbox belongs.

---

## 3. Writing to the sequencer safely (the gotchas that broke the first run)

Every one of these was found on the live reference run. Build them in from the start.

1. **Email Bison only detaches senders from paused or draft campaigns.** For a live campaign: pause it, detach, verify, then resume. Calls: `PATCH /api/campaigns/{id}/pause`, `DELETE /api/campaigns/{id}/remove-sender-emails` with `{"sender_email_ids":[id]}`, `PATCH /api/campaigns/{id}/resume`. Attach is `POST /api/campaigns/{id}/attach-sender-emails` with the same body.
2. **Pausing is asynchronous.** A detach sent while the campaign is still winding down returns success and is **silently ignored** (seen in production). After the pause call, poll `GET /api/campaigns/{id}` until the status really reads `paused` (about 3-second polls, 90-second timeout), and only then detach. If it never reaches paused, raise and report.
3. **Attach and detach are asynchronous too.** Poll membership until it matches what you asked for (about 4-second polls, 45-second timeout). A call that returned 200 is not proof.
4. **Read membership from the campaign, not the inbox.** `GET /api/sender-emails/{id}/campaigns` keeps listing every campaign an inbox was **ever** in, so it cannot answer "is it attached now". Use the campaign's own sender list, `GET /api/campaigns/{id}/sender-emails` (paginated).
5. **Never leave a live campaign paused.** Wrap pause, detach and verify in a try/finally that always resumes. A failed removal must not stop a client's campaign.
6. **Restore can need the same pause window.** If a plain attach does not settle on a live campaign, retry it inside a pause, attach, resume window.
7. **Retries.** Retry 429 and 5xx, and dropped connections, with a short backoff (about 4 tries). Pause, resume, attach, detach and the limit change are idempotent, so a retry is safe.
8. **Verify, then record.** Detach, confirm it is gone, and only then write it to the state file. An inbox still attached after a removal is an error in the report, never a silent pass.

---

## 4. New-inbox onboarding

New inboxes otherwise sit in warm-up forever, because nobody remembers to add them to campaigns on the right day. The autopilot does it.

- **Wait 14 days from the inbox's creation date** (`created_at` on the inbox record), however good its score looks earlier. Chapter 3's minimum warm-up is the rule; an early high score on a few warm-up emails is not evidence.
- **From day 14, attach it once** to the live campaigns (`active`, `queued`) that the **same sender** is already sending in. "Same sender" means the same display name on the inbox (one person's new inbox joins that person's campaigns), so a new inbox never ends up in someone else's sequence.
- **Only if it is healthy that day:** 3-day and 7-day warm-up both **90 or more**, and its domain is **not** listed on Spamhaus DBL or SURBL. Otherwise it waits and is re-checked the next morning. A domain whose blacklist check failed counts as "not proven clean", so the inbox waits.
- **Onboard once, then never again.** Record every onboarded inbox in the state file (`_onboarded`, per workspace). If someone later takes it out by hand, the autopilot must not put it back.
- **Start from a cut-off date.** Set `NEW_INBOX_SINCE` to the day the autopilot goes live, so inboxes that existed before it (and were placed by hand) are never touched by this rule. Default `NEW_INBOX_WAIT_DAYS = 14`.
- Use the same safe write sequence as section 3 for the attach.

---

## 5. Daily limits follow the warm-up score

**Email Bison does not raise or lower an inbox's campaign daily limit on its own; only warm-up ramps.** An inbox left at a starter limit stays there for months, and an inbox whose reputation is slipping keeps sending at full volume until rotation pulls it. Tying the limit to the score fixes both.

**The score used is the lower of the 3-day and 7-day warm-up score.** The limit drops as soon as warm-up dips and only goes back up once the score has held for a week.

| Inbox type | Score | Daily limit |
|---|---|---|
| Google | 95 or more | 15 |
| Google | 85 to under 95 | 10 |
| Google | 80 to under 85 | 5 |
| Microsoft | 90 or more | 5 |
| Microsoft | 80 to under 90 | 2 |
| Either | under 80 | the lowest tier as a floor (5 Google, 2 Microsoft); rotation has already taken it out of its campaigns |

The top tiers are chapter 2's provider caps, so the limit never goes above what the provider tolerates. Expose the tiers as one named constant (for example `TIERS = {"google": ([(95, 15), (85, 10), (80, 5)], 5), "microsoft": ([(90, 5), (80, 2)], 2)}`) and let the user change them.

Rules:
- **Inbox type** comes from the inbox record (Email Bison `type`: `google_workspace_oauth`, `microsoft_oauth`, `smtp`). Plain SMTP inboxes keep whatever limit they have; chapter 2 says not to build on them anyway.
- **Leave alone** any inbox with warm-up off, or with fewer than 5 warm-up emails in the 3-day window (the same minimum-data rule as rotation).
- **Write only when the limit differs** from the current one, and log every change with the old limit, the new limit and both scores.
- **Write call:** `PATCH /api/sender-emails/{id}` with `{"daily_limit": N}`. **Read the response back** and confirm `data.daily_limit` equals what you asked for; anything else is an error in the report.
- Run it **after** rotation in the same daily run, so both act on the same morning's scores.

---

## 6. State, log and report (the memory between days)

A scheduled cloud run starts from nothing every day, so the autopilot's memory has to live somewhere durable and travel into the next run.

| File | Holds |
|---|---|
| `rotation/state.json` | Per workspace, per held-out inbox: email, the campaigns it came out of (id, name, status), the reason, and `removed_at`. **The only record of where to put an inbox back.** Also `_onboarded`: the inboxes already onboarded, per workspace |
| `rotation/log.jsonl` | One line per action (`remove`, `restore`, `re-remove`, `onboard`, `daily-limit`), with a UTC timestamp, the scores and the campaigns or limits. Append-only. |
| `rotation/last_run.json` | The latest rotation report: per workspace, removed, restored, onboarded, held out, watch, no-data, errors. |
| `rotation/last_limits.json` | The latest limit report: per workspace, changed, unchanged, skipped, errors. |

Save the state **after each workspace**, so a crash in the second workspace loses nothing from the first.

Where the state lives between runs: on the reference setup it travels inside the dashboard's own Vercel deployment, in a hidden `_build/` folder that the password gate always answers with a 404, even after login. Each run downloads the current deployment, works, and redeploys it, which carries the state forward. Any durable store the routine can read and write works the same way; that is the only one tested so far. **Never keep the state only on the cloud machine:** it is wiped after every run.

Before changing the code or rules locally, **pull the latest state from production first**. The cloud updates it every day, and a local deploy made from an old copy overwrites it.

---

## 7. Scope controls

- **An explicit list of workspaces the autopilot touches** (`ROTATE_WORKSPACES`, and the same list for limits), separate from the list of workspaces the dashboard refreshes. Paused clients, frozen clients and demo data never rotate. The routine prompt repeats the list and forbids editing it.
- When a client leaves scope, the autopilot stops touching it, which means anything it was holding out **stays out** until someone re-attaches it by hand. Tell the user this when they remove a workspace, and list the held-out inboxes. (On the reference run, one inbox had been taken out of 14 campaigns the day its client was taken out of scope; by the owner's choice it stayed out.)

---

## 8. The scheduled routine (how it runs every day)

Set up as a Claude Code routine: a saved prompt, a cloud environment, and a cron schedule.

**Environment:**
- Network access on (it calls the sequencer and wherever the state lives).
- **Secrets as environment variables**, one per workspace key plus any deploy token. Never inside the prompt, never in a file that ships.
- The prompt checks a variable exists only with `[ -n "$NAME" ] && echo NAME set`, and never runs `env`, `printenv` or `set`.

**Schedule:** once a day, in the operator's timezone, written explicitly in the cron (for example `CRON_TZ=America/New_York 43 5 * * *` runs at 5:43 am New York time). Run it before the working day so the morning report shows what changed overnight. On the reference setup, the autopilot runs right after the daily dashboard refresh, in the same routine; it does not depend on the dashboard, so a failed build must not skip it.

**Run order:** fetch the state, rotation (with onboarding), daily limits, the alert email if the user has one (`references/daily-routine-and-alerts.md`), carry the state forward, report.

**Where the scripts live.** Either ship them in the bundle the routine downloads, or have the routine prompt write each one fresh every run from a heredoc in the prompt. The second makes the prompt the single source of truth for that rule: changing a threshold is a prompt update and nothing else. The reference setup uses both (rotation ships in the bundle; the limits and alert scripts are written from the prompt). Pick one home per script and never keep two copies that can drift.

**The routine prompt's hard rules** (copy them; each one exists because a run went wrong without it):
- Work fully autonomously. Do not ask questions. Never improvise new rules: everything needed is in the scripts.
- Never call write endpoints on the sequencer yourself; only the scripts write.
- Do not edit the scripts. If one crashes, report the traceback; do not patch around it.
- Never end the turn before the final report. Nothing wakes the session again once it stops, so every wait must be a foreground command.
- Shell state does not persist between commands: re-source the run's environment file at the top of every block.
- If a script crashes, still save and carry the state forward (it is saved per workspace).
- The report never contains key values, passwords or lead-level personal data.

**A retry routine for the blocked mornings.** On the reference setup the final publish step is occasionally blocked in the cloud, which also means the state did not travel forward. A second routine a few hours later (for example 11:43 for a 5:43 main run) fixes this. Its Step 0 asks the deploy host for the newest production deployment's timestamp. If it is from today, it stops with one line ("retry not needed"). If not, or if the check fails, it runs the full job. Its report adds one reminder: any inbox the failed morning run removed was never recorded in the state, so it will not be restored automatically and needs re-adding by hand once it recovers.

**Changing things later:**
- Rules or thresholds: edit the script (or the prompt, if the prompt writes it), pull the latest state, then redeploy or update. The next scheduled run picks it up.
- The routine's instructions: edit the source copy, then update the routine. **An update replaces the whole prompt**, so after every update read the stored prompt back and compare it with the source copy character for character; a truncated or mistyped prompt fails silently tomorrow morning. Update the main routine and the retry routine together.
- **Never trigger a run in the same step as an update:** a run started at the same moment uses the old prompt.
- Pause everything: disable the routine.
- Run now: the routine's "Run now", or ask Claude.

---

## 9. Dry run first, always

Every script takes `--dry-run`: it reads everything, computes every verdict and every target limit, and reports what it **would** remove, restore, onboard and re-limit, changing nothing and writing no state. The first run for any new workspace is a dry run, shown to the user line by line. Live mode starts only on the user's explicit yes, per workspace. Say plainly that live mode pauses and resumes their campaigns for a few seconds while it detaches an inbox, and that it changes their inboxes' daily limits.

---

## 10. The daily report

Per workspace, in this order. Say "no changes" plainly when nothing moved.

| Section | Each line shows |
|---|---|
| REMOVED | inbox, the reason (for example "3-day warm-up 58.33 < 80" or "declining warm-up 14d 95.12 > 7d 92.59 > 3d 88.89"), the campaigns it came out of |
| RESTORED | inbox, the reason, the campaigns it went back into |
| ONBOARDED | new inbox, its age and scores, the campaigns it joined |
| WAITING (new) | new inbox, the day it becomes eligible, or why it is still waiting (score under 90, domain listed) |
| HELD OUT | inbox, the current reason, held since (date), any re-removals done today |
| WATCH | inbox, 3-day and 7-day scores (slipping but not yet at the action line) |
| LIMITS CHANGED | inbox, old limit to new limit, 3-day and 7-day scores, the score used; or "no limit changes" |
| NO DATA | count of inboxes with too little warm-up data |
| ERRORS | inbox, campaign or limit, the error. Anything still attached after a removal, or a limit that did not read back, is an error. |

Then one line for any workspace that could not run (missing key), and one line for whether the state was carried forward.

---

## 11. What this cannot do (say it in the handover)

- It acts on warm-up score (and, for onboarding, the domain blacklist check) only. Bounce rate, zero-reply inboxes and blacklist hits on existing inboxes are still read from the dashboard, an audit, or the alert email (chapter 7); the autopilot does not pull an inbox for those.
- It is not the 70/30 weekly rest rotation. That remains a schedule the operator runs (chapter 3). The autopilot handles the inboxes that need rest **now**.
- A warm-up score is the sequencer's own reputation proxy, not inbox placement. A seed test (chapter 6) is still the check before a launch.
- If the sequencer has no write API for campaign senders, the mode degrades to the daily watch-list report with removals left to the user. If it has no writable daily limit, the limit tiers become a weekly to-do list instead.
