# Runners - where the jobs live

Pick one runner per job. Several runners can share a CRM; each job lives on exactly one, so it never runs twice.

## A. Self-hosted agent (Hermes, OpenClaw or similar)

An always-on agent on a server, talking to the user through a chat bot (Telegram, WhatsApp, Slack). Good for briefs and sweeps that read many tools, and for approvals by chat buttons.

**Set-up steps**
1. Connect the tools the job reads (CRM, calendar, inbox, note taker, chat) through the agent's connectors or keys stored in its credential store. Never in the job prompt.
2. Write the job as a short instruction file the schedule loads (the job card, the output format, the rules). Keep it short: every line is read on every run.
3. Create the schedule with the agent's cron tool. The server clock is usually UTC: convert the user's local time and write both in the job card (for example "0 2 * * * UTC = 07:30 local").
4. For checks that run every few minutes (heartbeats), tell the agent to reply with a silent acknowledgement when nothing needs attention, so the user's phone stays quiet unless something matters.
5. Run the job once by hand and show the user the output before switching the schedule on.

**Gotchas**
- The cron shell may not have the user's PATH: call command-line tools by absolute path.
- Some hosts block code execution inside cron runs, or block writing scripts to temp paths. Test the job under the cron, not only in chat.
- Credentials: if a token is revoked or expired, the scheduled job must not try an interactive sign-in. It uses its approved fallback and tells the user.
- Delivery confirmations: on a job that sends a one-way message, make sure the runner's own confirmation text is not delivered to the recipient.
- Before posting to a channel, state the channel name and id in the job's reasoning; if unsure, ask.
- Before any send on the user's behalf, check the agent's sent-items state and the mailbox's sent folder for that message; send only if both are clean, then record it.

## B. The CRM's own workflow agent

Some CRMs (for example Attio's Workflows agent) let you describe a job in chat; the agent builds the trigger, a custom agent step with its own prompt and model, and the output steps.

**Set-up steps**
1. Describe the goal in one paragraph: the trigger, the data, the output, the channel.
2. Open what it built. Check the trigger (schedule or record event), read the prompt it wrote and rewrite anything vague, and check which model it picked.
3. Name the chat channel explicitly.
4. If the job enrolls people in a sequence: the agent may not be able to create or choose one. Create the sequence by hand, then name it. Put an approval step before enrolment.
5. Use the builder's test mode on the sandbox record before publishing.

**Gotchas**
- Blocks that write or call out usually cost credits per run; agent steps cost more. Estimate runs per month times billable blocks before switching on, and put a filter before any agent step. Detail: **attio-implementation-playbook**.
- A workflow agent edits the CRM as a workspace user. Give it only the access its job card needs.

## C. Scheduled Claude routine (cloud)

A Claude task on a schedule, running in a cloud environment with connectors and network secrets. Good for daily reporting jobs that reconcile several tools and write to one destination.

**Set-up steps**
1. Create an environment. Keys go in as network secrets on the API host (the proxy attaches them), never as headers in the prompt.
2. Add only the connectors the job needs. Allow only the hosts it calls.
3. Write the prompt with hard rules at the top: what it may write and where; read-only on everything else; a workspace guard (a fact only the right workspace has, checked before any write); stop before writing on any unrecoverable failure; never print a credential.
4. Schedule with an explicit time zone (for example `CRON_TZ=<zone> 30 7 * * *`).
5. If each run asks for approval of tool use, unattended runs stall: turn on automatic approval for the task where the organisation allows it, which is why the prompt's own rules must be tight.
6. Run it once by hand ("Run now"), check the destination and the report, then check the next morning that it ran on its own.

**Gotchas**
- Each run starts fresh. State comes from the destination (the CRM, the sheet, the log), never from memory of the last run.
- Read in small slices; a very large response can be diverted and lost to the run.
- Locate records by a fresh read, never by a remembered row or position.
- End with a plain-text report: what changed, before and after, anything skipped or odd. No secrets, no raw API dumps.

## D. Webhook workflow tool (for example n8n)

Use it as the fast trigger for event jobs (a booking, a reply) that must react within seconds. Keep the judgment and the approval in the agent: the workflow catches the event and hands it on. Building reply alerts, cross-channel stops and reply classification there: **n8n-gtme-playbooks**.

## Choosing, per job

| Job | Usual runner | Why |
|---|---|---|
| 1 Revenue brief | A or C | Reads many tools on a schedule; posts to the user |
| 2 Booking to deal | B or D, with A or C for the transcript step | Must fire soon after the booking |
| 3 Calls to content ideas | A, B or C | Daily or on transcript ready |
| 4 Tasks on evidence | A or C | Needs inbox and chat access the CRM agent may not have |
| 5 Won to contract | A | Needs a chat approval with buttons and a contract tool |
| 6 Morning sweep | B (as shown in a real build) or A | Scheduled; posts to the team channel; enrolment needs approval |
