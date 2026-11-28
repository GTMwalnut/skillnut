# LinkedIn tool to CRM: the safe sync design (load for Option B or All)

Load this when the user syncs LinkedIn outreach (HeyReach or a similar tool) into a CRM. The reference build is HeyReach into Attio; the same shape works for any LinkedIn tool with an API and any CRM with record, note, task and list endpoints. It sharpens the engine's general rules for the channel where most leads have no email.

## The objective, in four lines
1. Create or reuse the person; link them to their company.
2. Fill only the missing details.
3. Log the invite, the acceptance and the messages.
4. Stay strictly scoped and non-destructive.

## The pipeline
**LinkedIn tool > resolve identity > link company > log the thread > verify and record for rollback.**

Per lead: discover the lead in the tool, resolve the identity, then either **0 matches: create the person** or **1 or more matches: reuse it and fill empty fields only**. Both paths then link the company, log the thread, verify, and record ids.

## Discovery (read-only)
- Check the key first with the tool's key-check call, then list campaigns, then pull the leads per campaign and the conversations.
- Expect what the reference tool returns: an identity made of the profile URL, name and company; an **email field that is usually empty**; and statuses such as connection sent, accepted, message sent and replied.

## The identity ladder (no email is the norm; fall through left to right)

| Step | Match on | If found |
|---|---|---|
| 1 | LinkedIn profile URL | Reuse |
| 2 | Name plus company | Reuse |
| 3 | Email (only when the tool has one) | Reuse |
| 4 | Nothing matched | Create a new person (email optional) |

- Compare URLs as decoded, lower-cased profile slugs; tools rewrite URLs (vanity slugs, encoding, member-id forms). Some CRMs store the URL case-sensitively, so search on what the CRM holds.
- A name-plus-company match with more than one candidate is not a match: hold it for the user rather than pick one.

## How the conversation is represented in the CRM

| CRM object | Holds |
|---|---|
| Note on the person record | The thread: a title plus a dated body (invite, acceptance, each message with its date and direction) |
| Task (optional) | A follow-up for the owner |
| List | The disposition bucket |

Many CRMs (Attio included) have no native LinkedIn activity type; the note carries the thread.

## Disposition: read the message, not the status

| Bucket | When |
|---|---|
| Accepted | Connected and replied positively |
| Accepted, then cancelled | Agreed, then later "can't make it" |
| Declined | An explicit no |
| Pending | Sent, no reply yet |

The tool's status says "replied"; it does not say yes or no. Read each reply's text to set the bucket, and show the user any reply you could not place.

## The seven safety rules (apply on every action)
1. **Scope-check after every single write:** confirm nothing outside this record moved.
2. **Ask before any overwrite or delete.**
3. **Create-only and additive:** never wipe a value.
4. **Existing person: fill empty fields only**, and re-check the field is still empty just before the write.
5. **No bulk calls: one record per request.**
6. **Dedupe first, then idempotent logging:** before writing a note, check the same thread note is not already there, so a re-run never logs twice.
7. **Verify by read-back and keep rollback ids.**

## CRM calls in the reference build (Attio)
- Search: query records on the people or companies object.
- Create: create a record; or upsert with a matching attribute where the CRM supports it.
- Fill empty: update the record with only the empty attributes.
- Link: set the company reference attribute on the person.
- Thread: create a note on the person. Follow-up: create a task. Disposition: add the person to the bucket's list.
- Keys go in the auth header (a bearer token for the CRM, an API-key header for the LinkedIn tool). Never print or paste either.

## Verify after each write
GET the record or note back; confirm the fields are right; confirm scope (nothing else moved); append the id to the rollback log.

## Rollback (only with the user's permission)
- Keep every created id: new people, new companies, new notes and tasks.
- Undo = delete or archive **those ids only**.
- Field fills were into empty fields, so undoing them means blanking exactly those fields on exactly those records; keep a log of record, field and value filled.
- Never roll back anything that existed before the run.
