# Real-time developer-signal flow in n8n (Mode F detail)

Load this when the user picks Mode F, or asks to run the Reo pipeline "live" instead of in batches. It is the same pipeline as Stages 4 to 12, rebuilt as one n8n workflow that fires on every Reo activity. Claude Code builds it through the n8n API: it writes the workflow, sets up the credentials, writes the filter and messaging code, fires test webhooks and reads the run logs to debug.

Batch (Modes A and B) or real time (Mode F)? Both work. Batch is easier to review and is the right start. Real time wins once the rules file has settled, because outreach goes out while the signal is fresh. Never build Mode F before at least two Mode A batches have written the rules down.

---

## 1. The flow, node group by node group

| # | Group | Nodes | What it does |
|---|---|---|---|
| 1 | Signal fires | Reo activity webhook (POST) | Reo calls the webhook when someone stars, forks or opens an issue on a tracked repo, reads the docs, or engages with a competitor repo |
| 2 | Live enrichment | Enrich latest company (Reo, GET) | Looks up the person's **current employer**, not just the account Reo matched the activity to. Reo data goes stale; this is where job changers are caught before anyone is messaged |
| 3 | Filter and second chance | Read exclusion list (sheet) > Apply filters (code) > Employee-band rescue check (IF) > Company check in an email finder such as Prospeo or QuickEnrich > Re-evaluate after the check (code) > Passed filter? (IF) | Location, company size and seniority from the rules file, plus the exclusion list. **Size rescue:** when the company size is missing, the person is not dropped; the flow asks a second provider for the company and re-runs the filter. Fails go to "Dropped (logged, no action)" |
| 4 | Dedupe | Check contacted by email (sheet) > Check contacted by LinkedIn URL (sheet) > Dedupe decision (code) > Already contacted? (IF) | Matches on **email and LinkedIn URL** against one shared dedupe sheet. Already contacted: "Stop - already contacted" |
| 5 | Route by segment | Lookup segment routing (sheet) > Get developer activities (Reo) > Signal family? (switch, with a fallback) > Segment routed? (IF) | A routing table maps every Reo segment to a signal type and to its campaigns. A segment that is not in the table stops at "Stop - segment not routed", so a new segment never sends by accident |
| 6 | Message from the signal | Build messaging, one code node per signal family (own repo, competitor, docs, website) > Messaging output | Copy is built from **which repo or which docs page, and when** (timing words from the send date, as in Stage 7) |
| 7 | Push and mark contacted | Verify email (a verifier such as TryKitt) > Email valid? > Create Email Bison lead > Attach lead to campaign > Create LinkedIn lead (HeyReach or Lemlist) > Prepare dedupe row > Append to dedupe sheet | Email goes to Email Bison, LinkedIn to the LinkedIn tool, and every person is written to the dedupe sheet the moment they are pushed, so the next webhook sees them |

The order matters: enrich before filtering (the filter needs the current employer), filter before dedupe (cheaper), dedupe before any paid lookup in step 6 or 7, and the dedupe row is written last, only after the push succeeded.

## 2. The sheets the flow reads and writes

| Sheet | Columns | Who edits it |
|---|---|---|
| Exclusion list | company name, domain, person email, LinkedIn URL, reason | The user (same content as the do-not-contact list in the rules file) |
| Segment routing | Reo segment id, segment name, signal family, Email Bison campaign id, LinkedIn campaign or list id, active yes/no | The user, after Mode D decides the segments |
| Dedupe log | email, LinkedIn URL, name, company, segment, signal, repo or page, activity date, pushed date, campaigns | The flow only (append) |

Keep the sheets in the user's drive, not inside n8n, so a person can read and correct them.

## 3. Signals worth wiring

Besides stars, forks, issues and docs reads, the stack can send higher-intent events into the same webhook, each as its own signal family with its own message branch:

| Signal | What it means |
|---|---|
| Docs pages such as a migration guide or the integrations pages | A team is reading how to move to you or plug you in |
| A Docker image pull or a package install | Someone is running the install |
| A return visit to the pricing page after a trial | The account is weighing the price after trying it |
| An active trial or free plan in the app | Someone is actually using the product |

## 4. Build steps (Claude Code with the n8n API)

1. Confirm the rules file, the routing sheet and the exclusion list exist. No rules file, no build.
2. Show the user the node plan (the table in section 1, with their segments and campaigns filled in) and get a yes before creating anything in n8n.
3. Create the workflow **inactive**. Set up credentials by name; never paste a key into a node, a code block or the chat.
4. Fire test webhooks with sample payloads, one per signal family plus one that should be dropped, one already contacted and one from an unrouted segment. Point the push nodes at a test campaign or leave them disabled for this step.
5. Read the run logs for each test and fix until every test lands on the expected branch. Report the branch per test in a small table.
6. Only on the user's named go: switch the push nodes to the live campaigns and activate the workflow.
7. Watch the first live day: every push has a dedupe row, every drop has a reason, campaign totals rise by the number pushed.

## 5. Gotchas

- Reo's webhook account match can be an old employer. The live enrichment step is not optional.
- Size is often blank. Without the rescue step, good people at good companies are silently dropped.
- Match on both email and LinkedIn URL. Reo stores LinkedIn as a member id, other tools as a vanity slug; the name check from Stage 5 still applies to anything the sheet match misses.
- Write the dedupe row only after the push succeeds, or a failed push blocks that person forever.
- Unrouted segments must stop, not fall through to a default campaign.
- The same safety rules as the rest of the skill hold: no new campaigns from this flow, live copy stays frozen, and already-connected people follow the recorded rules-file answer.
