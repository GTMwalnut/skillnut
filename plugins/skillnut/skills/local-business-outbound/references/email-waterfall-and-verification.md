# Module 2 - Find and verify emails

Load this when Module 2 starts. Input: `KEEP.csv` from Module 1 (or the user's own cleaned list).

## Why a waterfall

Small businesses rarely sit in one email database. Each finder knows a different slice, and the business's own website often lists an address no finder has. Running several finders and then a site scrape finds noticeably more emails than scraping websites alone. Stop at the first hit per business so no business is paid for twice.

## Step 0. Free first

1. Use any email already on the listing.
2. Match against the user's own verified files from earlier campaigns (respecting the Module 1 exclusions).
Rows settled here cost zero credits; say how many.

## Step 1. The waterfall (stop at the first hit)

| Order | Step | Tools (any one per step) | Notes |
|---|---|---|---|
| 1 | Email finder by domain | Icypeas | Domain search on the root domain |
| 2 | Second finder | Hunter domain search | Only rows step 1 missed |
| 3 | Third finder | Prospeo domain search | Only rows steps 1 and 2 missed |
| 4 | Website scrape | Zenrows, or a plain fetch of the home, contact and about pages | Pull mailto links and visible addresses. Many local sites show the owner's or the front desk's address here. |

The order above is the one this play was built with. If the user has other finders, run a small side-by-side on the same sample and order by hits per credit.

Pilot the whole waterfall on a random sample across states first. Report per step: rows sent, hits, credits. Then the quote for the rest and the go.

Every hit records `email_source` (listing, own file, finder name, site scrape) in `waterfall-log.csv`.

## Step 2. Clean the emails

- Dedupe emails across businesses. One address on several businesses usually means a shared agency or booking platform address: keep it on none of them, flag them.
- Drop addresses that clearly are not the business: web-agency, platform and template addresses (for example the site builder's support address), placeholder addresses (`example@`, `you@`).
- **Free-mail owner addresses (Gmail, Yahoo and similar).** Many owners run the business from one. Keep a free-mail address when it is on the business's own listing or website; it is theirs, and in practice these addresses performed well. Drop a free-mail address that cannot be tied to the business (found only by a guess or a third-party page). **Priority:** a free-mail address is second choice. When the business also has a verified address on its own domain, that one goes in the campaign and the free-mail address is kept as the backup. When the free-mail address is the only contact, it goes in the campaign: without it there is no one to reach. Record which one was chosen in an `email_source_priority` column (business-domain / free-mail-only / free-mail-backup).
- Generic inboxes (info@, contact@, hello@) are allowed; they are often the only address. If the user protects a low bounce rate, route generic inboxes to their own list (see tam-list-builder L6 for the trade-off).

## Step 3. Verify every address

Run every address through a live verifier (BriteVerify, ZeroBounce, NeverBounce, MillionVerifier or similar). Results map to:

| Verifier result | What it means | What happens |
|---|---|---|
| valid | The mailbox exists | Send |
| valid-risky (catch-all, accept-all) | The server accepts every address, so the check cannot confirm a person | By the user's policy, set in Stage 2. Default: send, in its own lead list and its own campaign |
| invalid | Mailbox does not exist | Never send. Try the next waterfall step for that business if one is left |
| unknown (timeout, greylisting) | The check could not run | Re-check once later; still unknown means do not send |

### The valid-risky policy

This play sends to valid emails and also tries valid-risky ones. Sending them is a choice the owner makes knowingly, so:
- Keep valid-risky in `EMAILS - valid-risky.csv`, never mixed into the valid file.
- Load them as their own campaign (or their own lead list) so their bounce rate is read apart from the clean list.
- If their bounce rate runs clearly above the valid list's in the pilot send, pause them and tell the user.

## Step 4. No email

- Has a phone: `CALL LIST - no email, has phone.csv`. Local owners answer the phone; this is a channel, not a loss. Point to cold-call-openers for the first twenty seconds.
- No email and no phone: `NO CONTACT.csv`.

## Reconcile

`valid + valid-risky + call list + no contact = KEEP rows in`. Print it, with credits used per tool, before and after.
