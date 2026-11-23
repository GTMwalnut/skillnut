# Webinar registrants to sales owners (load for Option D)

Load this when the user has a webinar (or virtual event) registrant export and wants it in the CRM and in front of the right rep. The goal is one sheet per owner that a rep can act on the same day, and a clean CRM import that records who came. The reference build used HubSpot; the steps fit any CRM with owners and a contact import.

For the follow-up campaigns themselves (thank-you and "sorry we missed you" tracks, cooldowns, HOLD files), use the Conference Outreach skill, Mode F. This flow is the CRM and hand-off half.

## The flow
1. **Export the registrants** from the webinar platform: name, title, registered company, company domain, self-reported industry, country, attended (yes or no), minutes watched, registration source, poll answers, questions and chat comments.
2. **Match each registrant to the CRM** (read-only) and give each one a status:

| Status | Meaning |
|---|---|
| Not in CRM | A new contact |
| In CRM, marketing contact | Already opted in |
| In CRM, non-marketing | Exists, not opted in |
| In CRM, bounced | The email on the CRM record bounces (keep the bounce reason) |
| Possible match only (unsure) | A name or company match you would not bet on; a human decides |

   Write a plain-English note on every row that needs a second look: the company is an existing customer account; the CRM record's company differs from the company the person registered with (they probably moved, so the CRM email is likely stale); a hard bounce; no email or company on the CRM record. A moved person is a job change, not a duplicate: the old record keeps its history.
3. **Assign the owner:** the CRM contact owner where the person exists; otherwise mark "Unassigned" and route by your normal rule (account owner, then territory), never by guess.
4. **Attach the hooks:** put each person's poll answer (for example their biggest blocker) and their questions or chat comments, with the time stamp, on their row. These are the opener the rep uses; a person who asked a question has told you what to talk about.
5. **Enrich and verify** where the email is missing or stale: find the work email and LinkedIn URL, then verify the email. Mark each row valid or invalid; an invalid email stays out of the import's email column.
6. **Prepare the import columns** (fill blanks only on existing contacts, exactly as in the manual upload procedure, Option C):

| Import column | What it holds |
|---|---|
| Events attended | The webinar name, only for people who attended |
| Webinars registered | The webinar name, for everyone |
| Set as marketing contact | No, unless the person opted in (consent first) |
| Timeline note text | One note: the webinar title and date, attended or registered only, minutes watched, the poll answer and the questions |

7. **Show the plan and get approval**, then import (the Option C walk-through), then read back a sample: status, owner, note, and that no populated value changed.
8. **Hand off by owner:** one view or sheet per owner, attended people first and the most engaged (longest watched, asked a question) at the top, each with the CRM link, the hook and the verified email. Unassigned and "possible match" rows go to the user, not to a rep.

## Rules
- Existing customers are flagged on the sheet and go to their account owner as context, not into a cold follow-up.
- Students, agencies and vendors who registered are labelled from the self-reported industry and the company, and left out of the sales hand-off unless the user says otherwise.
- Never mark anyone a marketing contact without consent on record.
- Every registrant lands in exactly one status; say the reconcile line (statuses add up to registrants exported).
