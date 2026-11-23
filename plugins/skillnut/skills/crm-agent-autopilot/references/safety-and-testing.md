# Safety contract, approvals, run log and testing

## The safety contract (paste into every job's instructions)

1. You read everything you need; you write only what the job card's allowlist names (object, field, allowed values or transition). Any other write: stop, log `blocked_write`, tell the user.
2. You never send anything outside the team (contract, email, message, sequence enrolment) without an explicit yes from the user for that item. No reply means no send.
3. Before any write, run the workspace guard. If it fails, write nothing.
4. If a read your decision depends on fails, write nothing and report.
5. Before acting on a source event, check the run log and the CRM for its idempotency key. If it is already handled, skip and log `already_done`.
6. Read back every write and log the result.
7. Never print, log or store a credential. On 401 or 403, stop and report.
8. Post to the user in plain words, answer first, no ids or tool names. The log holds the detail.

## Approval request (what the user sees)

One message per item, or one message listing several items of the same kind (a batch of enrolments), each with its own yes or no.

```
Approval needed: send contract
Deal: <company> - <value>
Why now: "<buyer's exact words>" (<call name>, <date> <time>)
Will send: <template> to <signer name, email>
Fields filled: value, signer, company name
[Send it]  [Not yet]
```

Rules:
- The request names the exact action, the exact recipient and the exact content or template.
- A yes is valid for that item and that version, once. If anything changes (value, recipient, template), ask again.
- "Not yet" or no answer changes nothing. The job does not ask again on the same item until new evidence arrives.
- Log the request, the answer, who answered and when.

## Run log (one JSON line per action)

```
{"ts":"2026-11-04T07:30:12+05:30","job":"booking-to-deal","run_id":"...","key":"booking:<uid>","object":"deal","record":"<id>","action":"create","field":"stage","before":null,"after":"Lead","evidence":"booking form notes","approval":"not_required","status":"ok","read_back":true}
```

- Actions: `read`, `create`, `update`, `close_task`, `post`, `draft`, `approval_requested`, `approved`, `declined`, `send`, `skip`.
- Statuses: `ok`, `already_done`, `parked`, `blocked_write`, `failed`, `dry_run`.
- Keep the log where the user can read it (a file the agent owns, a sheet, or a CRM list). Never log secrets or full message bodies; log short evidence quotes.
- Each run ends with one summary line: reads, writes, skips, parked items, approvals pending.

## Idempotency keys

| Job | Key |
|---|---|
| 1 Brief | job + local date |
| 2 Booking to deal | booking uid; transcript id + deal id |
| 3 Content ideas | transcript id + quoted line |
| 4 Tasks | task id |
| 5 Contract | deal id + template |
| 6 Sweep | transcript id (post); contact + sequence (enrolment) |

The CRM is the final check: even with an empty log, a job that finds the deal already exists, the task already closed or the contract already sent does nothing.

## Sandbox protocol

1. **Make the sandbox.** A test company, a test contact (the user's own email, so any send lands with them), a test deal in the first stage, test tasks, and a test chat channel. Give them obvious names (for example "ZZ Autopilot Test Co") so they are never mistaken for real records and are easy to filter out of reports.
2. **Dry run.** Point the job at the sandbox. Writes and sends are printed, not made. Check the printout against the job card.
3. **Live sandbox run.** Writes go to the sandbox only. Read each back.
4. **Repeat run.** Run again with no new input. Nothing may change. This proves idempotency.
5. **Edge cases.** Feed the failure cases from the job card (no transcript, ambiguous line, duplicate booking, "Not yet"). Each must end the way the card says.
6. **Shadow run on real data.** Writes off, sends off; the job posts what it would have done. The user checks it.
7. **Go live** on the user's named go. Run once by hand, then confirm the next scheduled run fired on its own and its log line looks right.
8. **Clean up** the sandbox records, or keep them filtered out of reports for the next test.

## Kill switch and change control

- Each job card names its off switch. Turning a job off loses nothing: the log and source events remain, and a re-run after turning it back on skips anything already handled.
- Change a job's rules only by editing its instructions and re-running steps 2 to 4 of the sandbox protocol. Credential, permission or schedule changes go to the user first.
- Review the log at the end of the first week: look at the skips, the parked items and the blocked writes, not only at what was done.
