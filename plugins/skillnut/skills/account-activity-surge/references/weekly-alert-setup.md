# Weekly alert setup (Mode 2)

One-time setup so the scan runs on its own every week and posts to a private Slack channel as a bot. Do the steps in order; each ends with a check.

## What gets set up

| Item | Default |
|---|---|
| Scheduled task | "Activity Surge", every Wednesday 8:45am in the team's time zone (`CRON_TZ=America/New_York 45 8 * * 3` for US Eastern), a fresh session per run, push notification on finish |
| Connectors on the task | The CRM (read only) and Slack (read the ops channel's history only, never post) |
| Post destination | One private Slack channel (for example GTM Ops), through the Activity Surge bot's incoming webhook |
| Webhook secret | Environment variable `SLACK_SURGE_WEBHOOK_URL` in the task's environment |
| Network | `hooks.slack.com` on the environment's allowed domains |
| The task's prompt | The run instructions (section 5 below), with the user's decisions log filled in |

Why a bot webhook and not the Slack connector: the connector posts as the person who connected it. A weekly post from a named person reads as that person's opinion, and unattended scheduled runs are usually blocked from posting as a person anyway.

## 1. Create the Slack bot (the user does this, 3 minutes)

At api.slack.com/apps: Create New App, then From a manifest. Paste:

```yaml
display_information:
  name: Activity Surge
  description: Weekly CRM accounts with rising engagement and no conversation
  background_color: "#1f2937"
features:
  bot_user:
    display_name: Activity Surge
    always_online: false
oauth_config:
  scopes:
    bot:
      - incoming-webhook
settings:
  org_deploy_enabled: false
  socket_mode_enabled: false
  token_rotation_enabled: false
```

Then Incoming Webhooks: On, Add New Webhook, choose the private channel. The person installing must be a member of that private channel, or it won't appear in the list. Copy the webhook URL straight into the environment variable (step 2).

Tell the user plainly: **never paste the webhook URL into chat, a doc or a log.** Anyone with it can post to the channel. If it leaks, delete it under Incoming Webhooks and add a new one.

## 2. Put the secret in the environment

- Claude Code scheduled task (cloud): add `SLACK_SURGE_WEBHOOK_URL` in the environment's variables, and add `hooks.slack.com` under Network access, Allowed domains. Environment changes only reach **new** sessions, so test from a fresh session.
- Other runners (n8n, a cron box, GitHub Actions): store it as that runner's secret, never in the workflow file.

Check (posts nothing):
```
python scripts/post_surge_alert.py --check
```
It prints only "set" or "missing", then the HTTP code Slack returns for an empty body. Any HTTP code (usually 400) means `hooks.slack.com` is reachable and nothing was posted. A proxy 403 or a connection error means the allowlist isn't working.

If Python isn't available, the same check with curl (prints only the code):
```
curl -sS -o /dev/null -w "%{http_code}" -X POST -H 'Content-Type: application/json' --data '{}' "$SLACK_SURGE_WEBHOOK_URL"
```

## 3. Preview before the first real post

Run Mode 1 once from an interactive session and send the preview to the **owner's own Slack DM** with the Slack connector (that's allowed: it's the person messaging themselves). Unattended scheduled runs can't do this; they're blocked from sending as a person. Get a yes on the format and the picks before the schedule goes live.

## 4. Create the schedule

Create the scheduled task with: the name, the cron line and time zone, a fresh session per run, push notification on finish, the CRM and Slack connectors, the environment from step 2, and the prompt from section 5. Then read the saved prompt back once and compare it with what you meant to save (scheduled prompts get truncated or mangled more often than you'd think).

## 5. The run prompt (what the task executes each week)

Write it from the user's decisions, in this shape:

1. Today's date; window start = today minus <window> days.
2. Exclusions: lifecycle stages <list>, closed-won, own company <name>, vendors <list>.
3. Reps who count as "being worked": <names and owner IDs>.
4. Pipeline: <main pipeline>, stages in order <list>, early cut-off <stage>; skip pipelines <list>.
5. Run the three tests, cleaning, ranking and don't-repeat exactly as in `surge-rules.md` (paste the rules in; a scheduled session can't ask questions).
6. Read the channel's last 4 weeks with the Slack connector, read-only.
7. Write the message to `msg.txt` in the exact format, then `python scripts/post_surge_alert.py --post msg.txt`. Expect "Posted."
8. If nothing qualifies, post nothing.
9. If the variable is missing or the post fails: do **not** fall back to posting from a person's Slack account. End with an error summary.
10. Finish with the end-of-run summary (posted, runners-up and why, the funnel).

## 6. Sending without the script

If the runner has curl but not Python, build the JSON safely (the message has quotes and emoji) and post:
```
python3 -c 'import json,sys; print(json.dumps({"text": sys.stdin.read()}))' < msg.txt \
  | curl -sS -X POST -H 'Content-Type: application/json' --data @- "$SLACK_SURGE_WEBHOOK_URL"
```
Slack answers `ok`. Never echo the variable, and never run the command with shell tracing on.

## 7. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| "missing" | Variable added after the session started, or added to the wrong environment | Start a new session; check the task uses that environment |
| 403 or connection refused | `hooks.slack.com` not on the allowlist | Add it; new session |
| `no_service` / 404 | Webhook deleted or app uninstalled | Add a new webhook; replace the secret |
| `channel_not_found` / `action_prohibited` | Channel archived, or the bot was removed | Re-add the webhook to the right channel |
| Post went to the wrong channel | The webhook is bound to a channel at creation | Add a new webhook for the right channel |
| Task ran but posted nothing | Nothing qualified (fine) or the run failed; read the push notification summary | The summary always says which |
