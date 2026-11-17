# Job-change re-verification and CRM write-back

Load this for Contact re-verification whenever the user wants the results written back into the CRM (moved contacts re-homed, emails swapped, statuses set), or when the list of people to check comes from bounces and "I've left" replies rather than from a CRM export. It has four parts:

| Part | What happens | Writes to the CRM? |
|---|---|---|
| A. Build the "who to check" list | Collect every leaver signal from every tool, reconcile against each tool's own counts | No |
| B. Decide where each person is | LinkedIn current job plus email verification, read together, into one final status | No |
| C. Plan and hold | Turn each status into CRM actions, hold the judgment calls for the owner | No |
| D. Write, then verify | Apply the agreed rules, log every change, re-read every record | Yes, gated |

The rule behind it: **LinkedIn tells you where the person is; email verification tells you whether an address works. Neither alone tells you someone moved.** An address that bounces can belong to someone still in the same job (their company blocked you), and an address that verifies can belong to someone who left last year (the company accepts all mail).

---

## Part A. Build the "who to check" list (read-only)

### 1. Collect every leaver signal, from every tool
Pull each source in full, save dated local snapshots, work offline.

| Source | Signal | Strength |
|---|---|---|
| Outreach tool bounce folder (cold email platform) | Bounce messages, classified by SMTP code (step 2) | High for "mailbox does not exist" and "domain does not exist"; none for spam blocks |
| Outreach tool replies, all folders including automated | "No longer with", "has left", "retired", "my new email is", "please contact X instead" | High; also a source of replacement contacts |
| LinkedIn outreach tool conversations | The prospect's own messages: "I've moved to...", "retired" | High |
| Sales engagement tool people | `bouncing` flag, bounced-email counts | Medium |
| CRM logged incoming emails | Same reply phrases as above | High |
| CRM marketing-email bounces | Hard bounce reason (unknown user, mailbox full) and quarantine reason | High, and **easy to forget** (see trap below) |
| Tags people already set by hand | "Person left org" in the outreach tools; a "No longer with company" status in the CRM | High; a human already judged it |

Tags are a separate pass. People tagged by hand as having left are worth a full re-check even when no bounce exists, and the person who tagged them may have been wrong.

### 2. Classify bounces by SMTP code, not by words
Read the code first, the wording second, in this order, and stop at the first match:

| Order | Evidence | Bucket | Job-change signal? |
|---|---|---|---|
| 1 | `5.1.x` (5.1.1, 5.1.10), "user unknown", "does not exist", "no such mailbox", "recipient address rejected" | Mailbox does not exist | Yes |
| 2 | `5.1.2`, `5.4.31x`, "domain not found", NXDOMAIN | Domain does not exist | Yes (company may be gone) |
| 3 | "account inbounds disabled", "account disabled/suspended", `5.4.300`, `5.2.3` | Account switched off | Yes, usually a leaver |
| 4 | `5.2.2`, "mailbox full", "over quota" | Mailbox full | Weak |
| 5 | `5.7.x` (5.7.352, 5.7.1, 5.7.129, 5.7.133), `5.0.350`, "message blocked", "not authorized to relay" | Blocked by the recipient's filter or policy | **No** |
| 6 | `4.x.x`, "will retry", "temporary problem", "delivery incomplete" | Temporary | No, unless it later turns final |
| 7 | Anything else | Unclear | Re-check |

Traps (each one happened on a real run):
- **Single words are not evidence.** Matching the word "spam" sent hundreds of bounces to "blocked" because the word sits in boilerplate: a blocklist-lookup link in Gmail's retry notices and anti-spam headers in Microsoft's. Match codes and full phrases.
- **A pattern list misses wordings.** "Account inbounds disabled" (a common mail-filter message) is a dead account, but an "account disabled" pattern does not catch it. After classifying, read a sample from every bucket and fix the patterns before trusting the counts.
- **A block wave is a deliverability problem, not a job-change wave.** On one real run about 430 prospects across 169 companies bounced with the same filter code (5.7.352, "the recipient's email filtering service suspected the sender's message is spam") in a few bursts of months. People leaving show up gradually and evenly; a burst across many companies means the sending domain's reputation is the problem. Say so to the user as its own finding.
- **Re-checking blocked addresses rarely finds movers.** When the dead-looking leftovers of the block bucket were re-checked on a real run, only about 1 in 9 had actually moved. Recommend checking blocked addresses only right before they are reused, so the answer is fresh when it matters.

### 3. Reconcile against each tool's own count
Before saying "we checked all the bounces", ask each tool how many it holds and compare:
- The outreach tool's own count of leads in bounced status, workspace-wide (page through every lead if the API ignores status filters).
- The sales engagement tool's count of people flagged as bouncing.
- The CRM's count of contacts with a hard bounce or quarantine.

Report the reconcile in a table: held by the tool, checked, not checked and why. On one real run the outreach tool held about 1,000 bounced leads and only about a third had been checked: two thirds had been classified as spam blocks and left out without the user being told. Separately, close to 1,000 CRM marketing bounces sat in a side tab and were never checked at all. **Every exclusion is a decision the user must hear about, with its count, when it is made.**

### 4. Check what is actually still sending, before claiming it
Never tell the user "the tool will keep emailing these dead addresses" from inference. Check per person: the lead's status in the outreach tool (bounced leads are not emailed again), each campaign's status (active, paused, completed, draft) and the lead's status inside it, and in the sales engagement tool the bouncing flag and any active cadence membership. On a real run every bounced lead was already excluded from sending, and the earlier "they will keep sending" claim had to be withdrawn.

Lookup trap: some outreach APIs treat an empty email as "list everything". Skip rows with no email before looking anyone up, or one empty row returns a page of unrelated leads and inflates every count.

### 5. Join to the CRM
Batch-read contacts by email. Two misses to plan for:
- **Not in the CRM.** Keep these as their own group; they can't be written to until the user decides whether to add them (Part D, step 9).
- **Hidden duplicates.** Reading by email finds only primary emails. An address held as a secondary email on another contact is missed, and a later write fails with "another record already has that value". Treat that error as "merge needed", not as a bug.

---

## Part B. Decide where each person is (read-only, paid)

Run the spend gate first. A workable per-person pipeline in an enrichment orchestration tool (one run per row, from a CSV):
1. **Profile lookup**: enrich from the LinkedIn URL on file; if there is none, a name-plus-old-company search.
2. **Current job(s)** from the profile's experience list: company, company domain, title, start date. Also keep the previous job.
3. **Name check**: the profile name must match the record.
4. **Email at the current employer**: a finder waterfall (cheapest first, stop at the first hit), then a live mailbox check on the candidate.
5. **Old email check**: a live check on the old address too.

Cost on a real run: about 2.5 data credits per person on average, plus action credits. Pilot 10 rows first, measure, then quote.

### Decision rules (LinkedIn wins)
- **A confirmed new email must match the current employer on LinkedIn**, by domain, by name, or through a known alias (a parent group's domain, a brand domain, the acquirer's domain after an acquisition). No match means it is not confirmed.
- **The email is from the previous job, so LinkedIn wins.** If the found email is at the company LinkedIn lists *before* the current one, the finder is out of date: the person is at the LinkedIn company, the found email is not used, and they are treated as "moved, no email".
- **A name search must prove identity.** A profile found by name search counts only if the old company appears in that profile's history. Otherwise it is "couldn't identify", whatever it says.
- **Name mismatch means a different person.** If the profile or the found email carries a different first name (the record says Sam, the profile URL says Alex), nothing from it is used. Mark only what is factual (for example the old email bounced) and leave the rest.
- **Acquired is not moved.** If the old employer was bought and the person now shows the acquirer (or a subsidiary the acquirer owns), it is the same company: swap to the new-domain email if one verifies, keep the account.
- **Several current jobs: pick the main one.** Take the most recent full-time role. Ignore board seats, advisory roles, volunteer posts, side consultancies and stale entries that never got an end date. If the most recent role *is* the old company, it is not a move.
- **Profile current jobs that started long ago** with no recent activity usually mean a stale profile. Use the main role but say it is low confidence.

### Final statuses (exactly one per person)
| Status | Meaning |
|---|---|
| Confirmed new email | Moved; new email verifies and matches the LinkedIn employer |
| Moved, no email yet | LinkedIn shows a new employer; no verified email there |
| Same company, old email works | Still there; the old address verifies |
| Same company, new working email | Still there; a different address at the company verifies (often after a domain change or acquisition) |
| Same company, no working email | Still there per LinkedIn; no address verifies |
| Retired | Profile or reply says retired |
| No current job on LinkedIn | Profile found, no current role |
| Couldn't identify | No profile, wrong person, or old company not in the history |
| Review | LinkedIn and the email evidence disagree in a way the rules above can't settle |

Caveat to say out loud: "old email works" on an address the outreach tool bounced often means the company accepts all mail and bounces later. Treat it as "probably still there, don't trust the address".

---

## Part C. Plan and hold (read-only)

### 1. Settle the rules with the user before the first write
Ask these once, in plain English, and record the answers as the rule set. Once a case is covered, apply the rule without asking again; the user should only be asked about cases the rules don't cover.

| Question | A tested answer |
|---|---|
| Update the existing contact or create a new one for movers? | Update the existing contact |
| What happens to the old email? | Kept as a secondary email |
| New email already on another contact? | Merge the old contact into the existing one (the existing one survives) |
| New company already in the CRM? | Move there as the primary company |
| New company not in the CRM? | Create it only if it is ICP (check what it does on the web first) |
| Borderline company? | Create it, mark it not ICP on the company's ICP field, move the person there, disqualify |
| New employer is an existing non-ICP company (a university, an insurer, a consultancy)? | Move there anyway and disqualify |
| No company domain (self-employed, freelance, one-person consultancy)? | No company created; company text only; disqualify |
| Several CRM companies share the new domain? | The record with the most activity (contacts, notes, deals) |
| Owner? | The new company's owner; if it has none, keep the current owner |
| How is a dead email flagged? | An "Email status" property (below) |
| Hand-set "no longer with company" status on a re-homed contact? | Back to Active: the status describes the old employer, not the person |
| Retired? | Lead status Disqualified, a note saying retired and why, the "no longer with company" status kept |
| People not in the CRM? | Create them, linked to the existing company and its owner, with a provenance note |

### 2. Email status property
Create a contact dropdown if the CRM has none (one write, gated): **Valid**, **Invalid - left company**, **Invalid - bounced**.

| Final status | Email status | Other changes |
|---|---|---|
| Confirmed new email | Valid | New email primary, old email secondary, company and owner moved |
| Moved, no email yet | Invalid - left company | Company, owner and title moved; dead email kept as primary so history stays attached |
| Same company, old email works | Valid | Hand-set "left" status back to Active |
| Same company, new working email | Valid | Email swapped, old one secondary |
| Same company, no working email | Invalid - bounced | Hand-set "left" status kept |
| No current job / couldn't identify | Invalid - left company | Nothing else: company, owner and lead status stay, because nobody knows where they went |
| Retired | (unchanged) | Disqualified, note |

### 3. Check the CRM's real option values
Dropdown labels and stored values differ, and the difference can invert meaning. On a real run a custom contact-status field stored "No longer with company" as `true` and "Do not contact" as `false`; writing `false` to mean "not left" would have marked people do-not-contact. Read every option's value before writing.

### 4. Build the plan and the hold list
For every person: target company id (looked up by domain), its industry and ICP field, the owner it would bring, the merge target if any, and one action. Anything the rules can't settle goes to a **hold workbook** for the owner: why held, a suggested decision, the person, old and new company, the LinkedIn evidence, the CRM link. Typical holds: several current jobs, a borderline company, a company record shared by several domains, a company record with a blank name (map it by domain and say so), an email that contradicts LinkedIn. Show every held row, never a sample.

ICP calls on companies not in the CRM: a quick web search on what the company does, judged against the user's ICP rule. Employers that usually fall outside a company-focused ICP: agencies, consultancies and service vendors, staffing firms, software vendors, insurers, retailers, schools and universities, public bodies, one-person firms. Say each call and its reason in one line so the user can flip it.

---

## Part D. Write, then verify (gated)

1. **Go per batch.** Every batch of writes gets its own explicit go, unless the user has said that a rule applies going forward.
2. **Snapshot before.** For each contact: the properties you will touch plus every company association with its labels.
3. **Merge first** where needed. The merge returns a **new id**: carry on with that id. Old ids become forward references; trying to merge them again fails harmlessly, but the done-set must key on both the old and the new id so reruns skip them.
4. **Properties in one update**: email (only if the current value still equals the old email, otherwise stop and report), Email status, title, company text, owner, hand-set status back to Active, lead status Disqualified where the rules say so.
5. **Secondary email**: re-read, and if the old email is neither primary nor secondary, append it to the additional-emails field.
6. **Associations**: set the new company as primary; label every other company "Former employee" (create the custom contact-to-company label once); remove the primary flag from the old company.
7. **Retired**: a note on the contact saying why (their own reply, or the profile).
8. **Creates**: new ICP companies with name and domain (and the ICP field when created as not ICP); dedupe by domain right before creating.
9. **People not in the CRM** (if the user wants them added): create the contact with the email to use as primary and the old one as secondary, link it to the existing company by domain as primary, owner from that company, Email status, title and LinkedIn URL, plus a provenance note. Don't create companies for these from scratch, and don't create defunct ones. Skip rows whose name and email belong to different people. If the new email already belongs to a contact, update that contact instead.
10. **Log** one JSON line per contact: before, the update sent, steps taken, after, error. Append-only, so any step can be rerun and audited.
11. **Verify by re-reading every record**, not by trusting the write responses:
    - exactly one primary company, and it is the target;
    - every other company carries "Former employee";
    - owner equals the new company's owner (when it has one);
    - the old email is still on the record (primary or secondary), and the primary is the new email where one was found;
    - Email status as planned, lead status as planned, hand-set "left" status no longer set on re-homed contacts.
    Print "checked N, issues M" and list every issue.
12. **Known lag after merges.** The merged-in record's old company association can arrive a few seconds after the merge, without the "Former employee" label. The verify pass catches it; re-apply the label in a fix pass.

### What to tell the user at the end
- A table per group: how many updated, what changed, how many merges, how many companies created (and why each is ICP), owner changes by owner.
- The held rows with the hold workbook.
- The untouched groups and why (no current job, couldn't identify, not in the CRM), and that untouched is a decision they can change.
- A heads-up for the reps: contacts that changed owner, listed per owner.
- Any number you said earlier that turned out wrong, corrected in plain words.

---

## Large CRMs: free first

Re-checking every ICP contact through a paid tool can cost tens of thousands of credits. Before quoting:
- **Free filter.** Anyone emailed in the last 6 to 12 months without a bounce (outreach tool, sales engagement tool, CRM) still has a working mailbox; skip them. What's left is the real "unknown" pool.
- **Bounces first.** Inside the unknown pool, people with a hard bounce are the most likely movers.
- **Check what the user already pays for.** Some B2B data platforms don't charge for search (find a person, see current company and title) and only charge for enrich (email, phone); under other contracts search is metered. Prove it with a 5-row test: read the usage counter, run five searches, read it again, and read it once more a little later in case it lags. A CRM's own job-change detection may exist but be switched off: check whether any contact carries a job-change date before relying on it.
- **Test on people whose answer you already know.** Pick the 5 test people from contacts already verified on LinkedIn (a mix of movers and stayers), so the test measures accuracy as well as cost.
- **Free-search ladder (ZoomInfo-style contact search, tested on a real run: zero credits used over 15 searches):**
  1. Search by the **old email**. A hit returns the person's *current* record, so it shows where they are now, not where the email was. Strongest signal, but it only hits when the platform still links the old address.
  2. Search by **name plus old company website**. A hit means "still there". No hit is only a hint they left: it can also mean the platform never had them.
  3. Search by **name only**. It returns every namesake (one real search gave 54 people with the same name), so accept a result only when exactly one hit fits the person's title or industry.
  4. Anything still unresolved stays unresolved, and goes through the spend gate only if the user approves.
  On the real test, the platform placed 3 of 5 correctly (including a move only three weeks old) and missed 2: one person outside the US the platform didn't hold, and one whose new employer wasn't in the first page of namesakes. Coverage outside the US is the usual weak spot. Before trusting it on a large list, run it free on a few hundred already-verified people and report the hit rate and error rate.
  API trap: bracketed query parameters (`page[size]`) must be URL-encoded or the gateway returns a bare 400.
- **Don't use LinkedIn seats for bulk profile views.** LinkedIn outreach tools read profiles through real accounts with daily view limits; thousands of views take weeks and put the accounts at risk.
- Run the paid profile lookup only on what the free and included sources could not place, through the spend gate.

## Re-checking a whole purchased list (tested end to end)

Use this when one bought list (a data-platform export loaded into the CRM months ago) turns out to be stale. A single report like "this person changed jobs a year ago but the CRM still has the old email" is the usual trigger.

### 1. Find the source, then the CRM overlap (free)
- Search the user's local list files for the person to learn which export they came from. Contacts loaded months after the export was pulled were often stale on the day of the import.
- Count the overlap by **exact primary-email match** between the export and the CRM. Report one number (for example "7,500 of the export's 28,000 emails are in the CRM; 7,361 have no Email status yet"). Leave out rows without an email, and say so.
- Stick to the source the user names. If the file mixes sources, use a column such as the platform's own person ID to keep only that source's rows.

### 2. Free current-employer check on the whole overlap
- Run the data platform's **free contact search** for every person, using up to three searches:
  - by old email;
  - by name;
  - by name plus old company website, only when the first two don't settle it.
- **The strongest match is the platform's own person ID** from the original export. When a returned record carries the same ID, it's the same person, with no namesake risk. That settled about 78% of people on a real run.
- Results go into three buckets:
  - **same company**;
  - **moved** (same person, different company, new company known);
  - **probably left** (no ID match, old email gone, nobody by that name at the old company).
- **Run safety for a long free run:**
  - Go at 1 request per second, or whatever pace the user asks for.
  - Read the credit balance from every response's headers, and stop the run on the first drop.
  - Pause when the hourly allowance runs low, and back off on 429.
  - Refresh the token on 401.
  - Append every result to a file as it arrives, so the run can resume where it stopped. Long runs on a laptop do get killed (host memory pressure did it twice on a real run).
  - Re-read the usage counter after the run and again the next day.
  - Tell the user the account's real limits from the response headers (per second, per hour, per day). Don't quote documentation numbers.
- **Renames and acquisitions inflate "moved".** A new company ID doesn't mean a new employer:
  - a rename (Example Labs to Exemplar Systems);
  - an acquisition (Old Device Co to a division of Big Acquirer Inc.);
  - a parent company or a country subsidiary (Example Corp to Example Corp North America);
  - a spelling or accent difference.

  Compare by name tokens and a short same-company list, and confirm unclear renames with a web search. On a real run, about 20% of the raw "moves" were renames.

### 3. Trust levels learned the hard way
- **"Probably left" from the data platform is not evidence of leaving.** A LinkedIn check of that bucket found about **half still at the same company**. Only about a quarter had really moved; the rest couldn't be found. Never set "left company" or Disqualify on this signal alone.
- **"Moved" to a non-ICP employer with nothing to back it up gets held, not Disqualified.** Corroboration means a verified email at the new company. Of the held people later checked on LinkedIn, 58% had never moved; the platform had matched them to unrelated employers (a school district, a tourism site).
- **Moves to ICP companies can be written even without an email.** They only change the company and owner, and they carry Email status "Invalid - left company".

### 4. Cheapest paid order (measured)
- **New company known (the "moved" bucket): skip the profile lookup.**
  - Get the new company's domain from the CRM's company record. Match it **by domain, not by name**: names differ between sources ("Example Corp Inc." vs "Example"), and a name search missed many big companies on a real run. When the CRM doesn't have the company, the platform's free company search returns its website.
  - Run name-plus-domain finders first and the LinkedIn-URL finder last. The LinkedIn-URL finder returned the old email, or a third company's email, about half the time, and it charges for those hits.
  - **Accept only an email at the new company's domain(s)**, including alias domains the CRM holds for that company. Reject the old email and any other domain, then move on to the next finder.
  - Verify whatever passes.
  - Measured cost: about 2.5 credits per person.
- **New company unknown (the "probably left" bucket): profile lookup first, on its own.**
  - At about 1 credit per person, that step shows who really moved.
  - Then run the email search only for the people who moved, and only for those whose new employer has a domain. Self-employed people, freelancers and one-person consultancies need no search: write them as non-ICP with company text only.
  - Compared with the full per-person pipeline for everyone (about 3 credits each), this cut the cost by about 45%.
- **Alias domains.** Movers often verify at a sister domain: a country domain versus the global one, an old brand domain, or the acquirer's domain. Collect the emails the finders returned at a domain that maps to the same company (same name root, or a CRM company of the same name), and verify just those for 1 credit each.
- **Spend control:**
  - Pilot 25 people.
  - Report the real per-person cost and the projected total against the user's cap.
  - Run in chunks of 100 to 250, reading the balance between chunks.
  - Stop and ask before the projected total passes the cap.
  - Billing can arrive a few minutes after the runs finish, so leave a margin, and report the final number including the late charges.
- **Unverifiable (accept-all) emails** count as "no email". Move the person with Email status "Invalid - left company", and put the unconfirmed address in a note, not in the primary field.

### 5. CRM write additions
- Look up target companies by domain, including the alias domain from the verified email. **Before creating a company, check the alias domains as well:** on a real run, a new company was created for a country domain of a company that already existed, and it had to be merged back by hand and archived.
- A company record with a blank name leaves the contact's company text blank. List these for the user to name.

### 6. Follow through in the outreach tool
After the CRM write, look up each moved contact's **old** email in the outreach tool:
- Check campaign status and the lead's status in each campaign first. Usually nothing is still sending to these leads.
- **ICP movers with a verified new email:** update the lead in place (email, company, title) rather than deleting and re-adding it, so the lead's history stays.
- **If the new email already exists as another lead,** leave the old lead alone. An update would create a duplicate.
- **Non-ICP movers and retired people:** delete the lead, or remove it from campaigns if the user prefers. **Back up the full lead record before deleting.**
- **ICP movers without an email:** leave the lead as it is, since there's nothing to swap in.
- Re-read every changed lead afterwards.
- Many outreach tools serve their full API spec from the instance itself (an `/api/reference` page that points to the spec file). Read it there when the public docs don't list update or delete endpoints.

### 7. How to talk about it
On a large run the user gets lost in many overlapping numbers. Lead with one number that answers the question ("1,738 have left the company the CRM lists"), then a short table. Add detail only when the user asks, and never bring in a new figure in a follow-up answer without saying how it relates to the one already given.

## Re-checking CRM marketing bounces (tested end to end)

Use this for the contacts the CRM's own marketing emails bounced on (hard-bounce reason or quarantine reason set). They are easy to forget (Part A, step 3) and are usually old records: on a real run most were added three to six years earlier and many had never been contacted by sales.

### 1. Pull fresh and take out what's already handled (free)
- Re-pull from the CRM on the day; the count drifts upward as more bounces arrive. Quote today's number and say how it relates to any earlier figure.
- Take out contacts already handled in this clean-up: an Email status set, in the change log, or tagged as left.
- Profile what's left before quoting a cost: bounce reason (unknown user, mailbox full, quarantined), how many have a full name, how many have a LinkedIn URL, how many have a company record with a domain. **On a real run only about 5% had a LinkedIn URL and about 17% lacked a full name**, which changes the plan: without a LinkedIn URL you can only search at the person's current company, and without a full name you can only verify.

### 2. Split by ICP before spending anything
- Use the company record's ICP field first. Where it's blank, make the call by company domain and show it to the user as a one-row-per-company workbook they can correct.
- Typical split on a real run: about a third ICP, about half unrelated organisations (universities, government, companies outside the market), plus vendors to the ICP, companies already marked out of ICP, and personal addresses.
- **Ask before skipping a group the CRM marks as "customer".** Many of the non-ICP bounces sat on customer records; the user decides whether that group matters.
- Only the ICP group goes through the spend gate.

### 3. Verify first, search only for failures (measured)
- **Verify the current email for everyone in scope** (about 1 credit each). A bounce from years ago does not mean the address is dead today.
- **Search only for those that fail and have a full name plus a company domain**: name-plus-domain finders, the LinkedIn-URL finder only where a URL exists. Accept only addresses at the same company's domain(s), including subdomains and the root domain (a mail subdomain such as `network.example.com` maps to `example.com`). Verify what passes. Measured about 1.9 credits per person searched.
- Measured outcome: about 35% of the old addresses verified, about 7% got a new address at the same company (usually a format change such as `first.last` to `first_last2`), the rest had nothing that verified.
- Total measured cost: about 1.7 credits per contact in scope.

### 4. Traps
- **Verifier "valid" vs CRM "bounced".** When most of the "valid" results sit at one large company, check the CRM's bounce reason and delivery history for them before trusting either side. On a real run the bounces were all "mailbox full" and nearly every one of those contacts had earlier deliveries, many this year: the mailboxes exist and the company's gateway was refusing bulk marketing mail. That's "Valid" for the address, with a note to the user that the CRM may keep suppressing marketing sends to them. (Contrast Part B: "valid" on an address bounced as *unknown user* usually means accept-all.)
- **Generic inboxes.** Finders sometimes return a role address for a person (`ap@`, `info@`, a two-letter local part). Reject these even when they verify.
- **Merges into unnamed contacts.** When the found address already sits on another contact, check that contact's name first. If it has no name and the address pattern differs from the person's old address, don't merge: it may be someone else. Treat the person as "no working email" and list the possible address for the user.
- **Two records of the same person in one batch.** Both may be in scope (one bounced address, one working). After the merge, the second record's update lands on the merged record through the old id; the verify pass must follow ids through the change log, or it will report a false "not found".
- **Acquisitions show up as other-domain hits.** A same-company search can return the acquirer's or the acquired company's domain. Don't use them in a same-company run; mention them to the user as people who may have moved within a group.

### 5. CRM write
- Address still works: Email status "Valid".
- New address at the same company: swap it in, keep the old one as a secondary email, Email status "Valid"; merge first if the address is on another contact of the same person.
- Nothing works: Email status "Invalid - bounced". Don't mark them "left company": nothing here says they left.
- Re-read every written contact afterwards and report issues as a number (aim for 0).
