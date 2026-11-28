# Data checks, campaign, upload, recap

Load this for Steps 6 to 8.

## Data checks before anything is uploaded

With a handful of leads you can eyeball the file. At hundreds or thousands, wrong data slips in quietly, so every upload runs checks first. Each check reports rows scanned and rows hit, so a zero is a real zero.

| Check | Rule |
|---|---|
| Email present | No blank emails in the upload file; blanks stay in the prospects file only |
| Email is the person's | The email's domain matches the company domain, or is flagged for a look |
| No duplicates | One row per email; one row per person |
| Columns filled | First name, company, subject and opener filled on every row being uploaded |
| Placeholders resolved | No `{{...}}`, `<...>`, "N/A" or "null" left in any merge field |
| Signal and person agree | The opener's company is the lead's company (the re-join worked) |
| Prior outreach | Anyone contacted in the last 100 days with no answer is held back; anyone who ever replied, including neutral, is out for good |
| Do not contact | Customers, open deals and do-not-contact lists removed |

For the full pre-send check (CRM suppression, ICP fit, name and company cleanup, identity), run **campaign-send-checklist** on the file before Step 6. Reconcile after the checks: rows in = rows to upload + rows held, with a reason per held row.

## Campaign create (needs the go)

1. Show the plan: campaign name (`<Offer> Outreach - <Segment> - <Month Year>`), workspace, the 10 pilot leads, and the custom fields that will carry `intent_rating`, `intent_signal`, `intent_source`, `subject` and `opener`.
2. On the go, create the campaign through the email tool's API. It is created in draft. Never activate, schedule or launch it.
3. Read it back and confirm the name, the workspace and the draft status.

## Pilot upload: 10 leads

1. Create the 10 leads with their custom fields (the research travels with each lead as notes or variables).
2. Attach or import them into the campaign.
3. Read back: lead count in the campaign equals 10, and every custom field is filled.
4. Ask the user to look at the leads in the email tool before anything else goes in.

## Full upload (after the user has looked and says go)

- Upload in batches. After each batch, read back the campaign's lead count.
- Checkpoint each created lead (one line per result in a local log) so a crash or re-run never creates a lead twice.
- Reconcile at the end: leads in the upload file = leads in the campaign.
- Leave the campaign in draft. What's left for the user: attach senders, set the schedule, write the sequence steps (**copywriting-messaging**, **email-and-linkedin-sequencer-lead-upload**), run **campaign-send-checklist**, then launch.

## Recap

At the end, write a numbered recap of what actually happened, one block per step: the tool, the call or MCP tool used, the file written, the counts, and any error and its fix. Name key files, never key values. If the conversation was compacted along the way, rebuild the recap from the files in `data/` and the upload log, not from memory.

## Save as a skill

Offer to turn the recap into the user's own skill, so the next campaign is one prompt. Show the draft; write it only on a yes. Shape:

| Part | Content |
|---|---|
| Frontmatter | `name`, and a `description` that says when to use it (for example "run my outbound pipeline for a new brief") |
| Inputs | Offer, targeting filters, lead count, campaign name pattern |
| Tools | Which tool for each step, API or MCP, and which key file (file name only) |
| Steps | The recap's steps, in order, with the endpoints or MCP tools that worked |
| The intent question | The approved question, word for word, as the starting point |
| Gates | Auth check first, pilot 10, draft only, the user launches |
| Lessons | What went wrong this run and the fix |

No keys, no lead data and no client names in the saved skill.
