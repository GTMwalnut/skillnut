# Module 4 - Writing scores to the CRM

Load for Module 4. Every step here is behind a write gate.

## 1. The property plan (show it, get a go)

Create new properties in a group of their own (for example "AI score"). Never reuse a field that exists.

| Property | Type | Object |
|---|---|---|
| AI score | Number 0 to 100 | Contact and/or company |
| AI score tier | Dropdown: Priority, Active, Initial | Same |
| AI score reason | Multi-line text | Same |
| AI score confidence | Dropdown: High, Medium, Low | Same |
| AI score action | Dropdown or text | Same |
| AI score version | Single-line text | Same |
| AI scored at | Date | Same |

- HubSpot: create in Settings or via `POST /crm/v3/properties/{object}` once the user says go. Write the owner ("scoring model, weekly") in each description, in line with the field-mapping rules in **hubspot-implementation-playbook**.
- Attio: add attributes on People and Companies (number, select, text, date); see **attio-implementation-playbook** for attribute types and permissions.
- Other CRMs: same fields, their native types.
- If the CRM already has a native or third-party score, leave it and say so. A side-by-side of the two is a useful report, not a reason to overwrite.

## 2. Before any write

1. Show the distribution: count per tier, the score histogram in bands of ten, the skipped-for-missing-data count.
2. Show ten sample rows with their reasons, across all three tiers.
3. Get a go naming the object and the record count.

## 3. Test, then batch

- Write a handful of records. Read them back from the CRM and show the values as stored.
- Then batch (HubSpot batch update, up to 100 per call; Attio record updates, paced). Pause briefly between calls and back off on rate-limit responses.
- After each batch: written + skipped + failed = batch size. At the end, the same for the whole run.
- Log every write: record ID, old value of the score fields (blank on first write), new value, version, time. Keep it in `write-log.csv`.

## 4. After the write

- Routing, views and alerts off the new tier (Priority to an owner task or alert, Active to nurture, Initial to no outreach) are built with the CRM playbooks, each behind its own go and tested on test records first.
- Re-scores overwrite only the score properties this skill created.
