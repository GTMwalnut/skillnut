# Module 4 - Cleanup (duplicates, empty companies, dead emails)

Load this for Module 4. This is the HubSpot-specific short version. For deeper hygiene (fill-rate scoring, company keep or delete review, live email re-verification, job movers, owner assignment, keeping data fresh and reactivating dormant records), hand off to the **CRM Data Health** skill.

Clean companies before loading or re-associating contacts. Fixing companies after contacts are attached to them is far more painful.

## 1. Why duplicates happen (say this to the user)

- People type the same name differently ("Acme Systems", "Acme Systems Ltd", "Acme Systems Limited").
- Imports and integrations create a company per row without checking for a match.
- Domain variants (subdomains, old domains, regional domains) split one firm into several.

## 2. Fix what exists

Resolve on **domain**, not name. Names vary; the registered domain rarely does.

1. Export all companies (name, domain, contact count, deal count, owner, create date) to `backups/`.
2. Cluster by root domain, so subdomains and regional variants fall into one cluster.
3. Per cluster, propose the primary: the most complete record, or the one with deals and the most contacts.
4. Same-company, different-domain cases (an old and a new domain): confirm they are one entity, then merge to the current domain.
5. Show the full merge list and the reconcile line. Wait for the go.
6. Merge one cluster, read it back (contacts, deals and history all on the primary), show it, then merge the rest in batches. Merging keeps associated contacts, deals and history; it does not delete them.
7. Empty shells (no contacts, no deals, no notes): review in bulk, keep any with a deal or note, archive the rest from a list the user has approved. Archive, never hard-delete.

Duplicate deals already flagged by the team (for example a "Closed - duplicate" stage) are reviewed with the stage map in Module 3.

## 3. Stop new ones forming

- Domain is the unique key; automatic company creation and association by domain is on.
- Company names are normalized before import; every imported row needs a clean domain.
- The monthly duplicate report (Module 6) catches new ones while they are few.

## 4. Job changes

When re-enrichment confirms someone moved:
- Update primary email, company and job title to the current ones.
- Move the old email into Additional emails rather than deleting it, so old threads still match.
- Keep the previous company association and log a dated note recording the move.
- Only apply a change enrichment has confirmed. An unconfirmed guess stays Unknown; it never overwrites good data.

## 5. Dead emails: keep and mark, never delete

| Option | Why |
|---|---|
| Delete the record | Loses deal associations, attribution and history; you can't tell you already worked them. Not recommended. |
| Keep and mark (recommended) | Email status = Invalid, Do not email on, suppressed from sequences. History stays, the record is findable, reports exclude it cleanly. |

After the retention window the user set, with no valid email found and no deal history, the true junk may be archived in one reviewed batch. Still archive, not delete.

## 6. Cleanup log

For every batch: date, action, records in, changed, skipped, failed, backup file name, who approved. The sum must match records in.
