# Jobs 2 to 6 - job cards

Each job below follows the shared ground rules in SKILL.md and the safety contract in `safety-and-testing.md`. Object and stage names are examples; use the user's own, read in pre-flight.

---

## Job 2 - Booking to deal, transcript moves the stage

**What it does.** Someone books a meeting; the agent reads the booking notes and the company, creates the deal in the first stage of the lead pipeline on the right company and person, and after the meeting reads the transcript and moves the deal forward.

| Field | Value |
|---|---|
| Trigger | Part A: a booking is created (booking tool webhook, a CRM event, or a short-interval check of new bookings). Part B: a transcript for that meeting is ready. |
| Reads | Booking: attendee name and email, company, the notes typed into the booking form, time. CRM: people and companies (match by email domain first, then by name), open deals for that company. Part B: the transcript and its summary. |
| Writes (allowlist) | Part A: create one deal (fields: name, company, contact, stage = the first stage, source = booking, created-by = agent, description = booking notes); create the person or company only if no match exists. Part B: deal stage, one step forward only; a note on the deal quoting the line that justified the move. Never to Won or Lost. |
| Approval point | None for Part A on a clean match. A fuzzy or no match is parked for the user, not created. A backward move or a jump of more than one stage is proposed in chat, never made. |
| Idempotency key | Part A: booking uid. Part B: transcript id + deal id. |
| Kill switch | Turn off the booking trigger; Part B stops with it. |

**Matching rule.** Company by the attendee's email domain reduced to its registrable root; then the company name with word boundaries. A personal email domain (gmail, outlook and similar) never matches a company by domain: use the company typed in the booking form, and if that does not match exactly, park it. If an open deal already exists for that company, do not create a second one: add the booking as a note on the open deal and log `existing_deal`.

**Deal value.** Fill it only if the booking form or the CRM gives a real number (a package the person chose). Otherwise leave it blank and say so; never guess a value.

**Stage move rule.** The transcript must show the step that defines the next stage (for example an agreed next meeting with more people, a request for pricing, a scope discussion), in the buyer's words. Quote it in the note. No clear line, no move.

**Failure modes**
| Failure | What the job does |
|---|---|
| Booking rescheduled or cancelled | Reads the newest booking event; a cancel adds a note and leaves the deal as is; it never deletes a deal |
| Same person books twice | Second booking is a note on the existing deal (booking uid differs, company deal exists) |
| Attendee uses a personal email | Match on the typed company only; otherwise park |
| No transcript (call not recorded) | Part B does nothing; the deal stays put; the morning brief can list it as "no notes" |
| Transcript ambiguous | No move; the line goes in the brief's actions as "check stage" |

**Sandbox test.** Book a meeting as the test company; expect one deal in the first stage. Run again on the same booking; expect nothing new. Feed a test transcript with a clear next step; expect one forward move and a quoted note. Feed one with no next step; expect no move.

---

## Job 3 - Calls to content ideas

**What it does.** After each call, the agent reads the transcript, picks out the moments worth a post, and files each as a row in the user's content list with its source call, a suggested format and status Idea. It keeps the status honest after that: Idea, Scheduled, Published.

| Field | Value |
|---|---|
| Trigger | A transcript is ready, or a daily sweep of yesterday's transcripts. |
| Reads | Transcripts and summaries; the existing content list (to avoid duplicates); the user's owned topics if they have listed them. |
| Writes (allowlist) | Content list: create rows (title, angle, format, source call, quote, status = Idea). Status: Idea to Scheduled only when a scheduled post exists in the publishing tool; Scheduled to Published only when a live link exists. |
| Approval point | None for filing ideas inside the user's own list. Nothing is ever posted publicly by this job. |
| Idempotency key | Transcript id + the quoted line. |
| Kill switch | Turn off the transcript trigger. |

**What counts as an idea.** A line where someone names a problem, a lesson, a mistake and its fix, a number they track, or a way of working. A few per call at most; a call with nothing worth posting files nothing.

**Privacy.** Strip client, buyer and company names from the idea title and angle. The source call link stays in a private field so the user can go back to it. Never put a buyer's quote into a public draft without the user's check.

**Duplicates.** If an idea with the same angle exists, add the new call as a second source instead of a new row.

**Failure modes**
| Failure | What the job does |
|---|---|
| Internal or personal call | Skipped if the user has listed such meetings to ignore; otherwise ideas are filed but marked "internal call" |
| Same call recorded twice | Deduplicate recordings of the same meeting before reading |
| Status claimed without proof | No status change |

**Sandbox test.** Run on one past call the user picks; show the rows it would file; file them in a test view; run again and confirm no duplicates.

Next step for the user: **linkedin-post-generator** turns a picked idea into a post; **sales-call-insights** mines calls for buyer language for outreach.

---

## Job 4 - Tasks closed on evidence

**What it does.** Reads the open tasks in the CRM, looks for proof each one is done in email, team chat and call notes, and closes only the ones with proof, attaching the receipt.

| Field | Value |
|---|---|
| Trigger | Daily (or a few times a day). |
| Reads | Open CRM tasks (text, linked record, owner, due date, created date); sent and received email for the linked people since the task was created; team chat messages in channels the agent is actually a member of; call notes and recap emails since the task was created. |
| Writes (allowlist) | Task: completed = true; a comment or note with the evidence (source, date, short quote or subject line), tagged as closed by the agent and naming the source (email, chat or call). Nothing else on the task or the record. |
| Approval point | None for a closure that passes the evidence rule. A borderline match is proposed in the brief, not closed. |
| Idempotency key | Task id. A closed task is never touched again. |
| Kill switch | Turn off the schedule. |

**The evidence rule.** All of these must hold:
1. The artifact is dated after the task was created.
2. It comes from the right side: the user or their team for a task they own (a sent email, a posted message, a shared document); the other party for a task that was waiting on them.
3. It says the thing is done, not that it will be done ("sent", "attached", "countersigned", "dropped in the shared folder"), and it matches the task's object (the same document, the same company).
4. The source is one the agent can actually read. Team chat counts only if the agent has access to it.

No artifact means "no evidence found", never "not done" and never "done". Silence is not proof. Text matching between tasks and messages catches many but not all; the rest stay open for the user.

**What the user sees.** In the brief or the run report: tasks closed (one line each with the receipt), tasks left open with no evidence, tasks overdue.

**Failure modes**
| Failure | What the job does |
|---|---|
| Two tasks match one message | Close neither; propose both |
| Evidence is a promise ("will send tomorrow") | Leave open |
| Chat workspace not connected | Says that source was not checked; does not treat it as empty |
| Note taker's action items garbled through the API | Read the recap email's action-item block instead |

**Sandbox test.** On the test company create three tasks: one with a matching sent email, one with a promise only, one with nothing. Expect exactly one closure with the receipt attached, and two left open with reasons. Run again; expect no change.

---

## Job 5 - Won deal to contract, sent only after approval

**What it does.** When a call sounds like a yes, the agent asks the user once in chat, quoting the buyer. If the user says send, it marks the deal won, creates the contract from the deal record in the contract tool, sends it to the buyer, and reports delivery.

| Field | Value |
|---|---|
| Trigger | A transcript or email on a late-stage deal contains a buying signal (the buyer agrees to the terms or asks for the paperwork). |
| Reads | The transcript or email; the deal (value, contact, company, stage); the contract template and its required fields. |
| Writes (allowlist) | Before approval: a draft contract in the contract tool, not sent. After approval: deal stage = Won; contract sent to the named signer; a note on the deal with the approval and the contract link. |
| Approval point | Always. The approval request shows: the buyer's exact words with the call and time; the deal value; the template; the recipient name and email; the fields that will be filled. Buttons or replies: "Send it" and "Not yet". |
| Idempotency key | Deal id + contract template. If a contract for this deal is already sent, never send another; report its status instead. |
| Kill switch | Turn off the trigger; any pending approval requests expire. |

**Ask once.** One request per deal per buying signal. "Not yet" changes nothing: the deal stays where it is, the draft stays a draft, and the agent does not ask again until there is a new call or email on that deal. No reply means no send.

**Before the send.** Check that every required template field is filled from the deal record (value, signer, company legal name). A missing field stops the send and is reported; the agent never fills one with a guess. Check the recipient is a person on the deal, not a guessed address.

**After the send.** Read back the contract status (sent, delivered, viewed) and add it to the deal note. Report it in chat in one line.

**Failure modes**
| Failure | What the job does |
|---|---|
| A positive-sounding line that isn't a yes ("sounds good, let me check with finance") | No request; lists it in the brief as a warm signal |
| Value in the call differs from the deal value | Puts both in the request and asks which to use |
| Signer unknown or several contacts | Asks the user to pick in the request |
| Contract tool rejects a field | Stops, leaves the deal stage unchanged, reports |
| User approves twice | Second approval finds the sent contract and does nothing |

**Sandbox test.** On the test deal, with the user's own email as the signer, feed a transcript with a clear yes. Expect one approval request. Answer "Not yet": expect no change. Feed it again with no new evidence: expect no second request. Then a new test transcript, answer "Send it": expect Won, one contract to the user's own address, one note. Approve again: expect nothing.

Related: a closed-won handoff with a required-field gate inside Attio is in **attio-implementation-playbook**.

---

## Job 6 - Morning sweep of yesterday's call action items

**What it does.** At a set time each morning, the agent reads yesterday's call notes linked to deals, summarises the action items by owner, posts them to the team channel, and lines up follow-ups and sequence enrolments for the user's approval.

| Field | Value |
|---|---|
| Trigger | Daily at a fixed local time before the team starts (for example 8:00). |
| Reads | Call notes and transcripts from the previous local day, synced to deals; the deal and its contacts; email since the call (to see what was already sent); the outreach tool's history for each contact (replies and last send). |
| Writes (allowlist) | Optional: one CRM task per action item the user owns, linked to the deal (only if the user switched this on). Enrolment into the one named sequence, after approval. |
| Posts | One message to the named team channel: per call, the action items grouped as "we owe", "we chase", "they own", with owner and due date if said. |
| Approval point | Every follow-up email draft and every sequence enrolment, listed in one approval request with the contact, the sequence, the reason and the exclusions. |
| Idempotency key | Transcript id for the post; contact + sequence for enrolment. Before enrolling, check the sequence and the sent folder for the contact. |
| Kill switch | Turn off the schedule; pending enrolments are dropped. |

**On the CRM's own workflow agent.** Describe the goal in plain words (read the previous day's call notes on deals, summarise action items, post to the named channel at 8am). The agent builds the schedule, a custom agent step with a prompt it writes itself, and the post step. Then:
- Read and edit the prompt it wrote. Add the grouping (we owe, we chase, they own), the "drop empty sections" rule, and "no record ids".
- Name the channel explicitly.
- The agent may not be able to create or choose a sequence. Create the sequence by hand first, then tell the agent its exact name. Keep enrolment behind an approval step.

**Exclusions before enrolment.** Anyone who has replied (including a neutral reply) is never enrolled. Anyone with an unanswered send in the last 100 days is skipped. Anyone already in a sequence is skipped. Say who was skipped and why in the approval request.

**Failure modes**
| Failure | What the job does |
|---|---|
| No calls yesterday | Posts nothing (no "no calls" message) |
| Call not linked to a deal | Lists it separately as "not on a deal" |
| Same call recorded twice | Deduplicate before summarising |
| Action items field garbled | Use the recap email's action-item block |
| Wrong channel | Before the first post, read the channel's name and description; if unsure, ask |

**Sandbox test.** Point it at a test channel and one past call linked to the test deal. Check the post. Then a dry run of enrolment with the user's own address as the contact: expect one approval request listing it. Run the sweep again; expect no second post for the same call.
