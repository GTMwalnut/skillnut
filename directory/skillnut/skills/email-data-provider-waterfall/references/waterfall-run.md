# Waterfall run: the full list, in the earned order

Load this when Part 2 runs. The goal: every contact ends in exactly one bucket, every email shown to the user is verified and belongs to the right person, nothing is paid for twice, and the user can see which provider filled what.

---

## 1. Inputs

- The full list (never modified; results are appended on the right).
- The provider order: from the bake-off simulation, or from the user. If the user gives an order without a bake-off, say once that it has not been tested on their contacts and offer a five-row pilot per provider as the minimum check.
- The verifier (the same one, at the same setting, as the bake-off).
- The catch-all policy (section 5).
- An approved credit ceiling.

---

## 2. Free before paid

1. Match the list against the user's own files: earlier verified exports, delivered lists, campaign exports with verification status. Rows with a recently verified email are `VALID (own file)` at no cost. Say how old those files are. Some exports carry no email column at all; say so instead of counting them as coverage.
2. Reuse the bake-off cache: every sample contact already has every provider's answer.
3. Rows at companies known to be gone (from a `crm-data-health` Company cleanup, if one ran) are set aside before any call.

---

## 3. Spend gate and pilot

Follow `spend-gate.md`:
- Price the residual per provider position: the first provider sees every residual row; each later provider sees only what the earlier ones missed (use the bake-off simulation shares for the estimate).
- Pilot a random sample with a fixed seed through the whole waterfall, report the funnel by provider, explain the misses.
- Quote with a haircut: pilot rates usually fall at full scale.
- Set the hard stop inside the runner, not just in the plan. Get the go.

---

## 4. The run

For each contact, in order:

1. Ask provider 1 (cache first). If it returns an address the provider labels valid, verify it and name-check it.
2. If the result is `VALID`, stop. Later providers are not called for this contact.
3. If not (`NONE`, `UNBACKED`, `DECLARED_VALID_FAILED`, `WRONG_PERSON`, or `CATCH_ALL` under a policy that keeps looking), go to the next provider.
4. After the last provider, the contact keeps the best result it got, by this precedence: `VALID` > `CATCH_ALL` > nothing.

Run rules:
- **Run the best-value provider to exhaustion before the fallback**, as batches: provider 1 on the whole residual, then provider 2 on what is left, and so on. This keeps the balance checks clean and lets you stop between providers.
- **Checkpoint every call** to the cache; any step can be re-run without paying twice.
- **Concurrency** per provider limits; back off on 429; read `tam-list-builder` 3c and 3f for known quirks.
- **Report after each batch**: rows done, `VALID` found by this provider, credits used, ceiling left. Stop at the ceiling and ask.
- **Scope is the user's.** If they approved the whole list, do not quietly enrich only part of it, and the reverse.

---

## 5. Verify, name-check, catch-all

- **Verify every email** before it is shown as an email, including ones a provider calls valid.
- **Invalid usually means a wrong address, not a job change.** Before calling anyone a mover, try a finder on the same domain. Real movers are re-found at the new company and kept only if the new company is still in the ICP.
- **Name-check** every address (SKILL.md, Identity check). A mismatch goes to `WRONG_PERSON` with nothing copied from that response.
- **Free-mail and unverifiable addresses** go LinkedIn only rather than risking a bounce.
- **Capture the mail host (MX)** during verification; it drives gateway routing in `email-deliverability-metrics-and-dashboard` and `conference-outreach`.
- **Catch-all policy**, chosen by the user in Stage 2:

| Policy | What happens | When it fits |
|---|---|---|
| Valid only | Catch-alls are set aside and routed to LinkedIn; the waterfall keeps looking for a `VALID` from the next provider | Mailboxes already bounce above about 2 percent, or the domains are new |
| Valid plus catch-all, flagged | Catch-alls go out in their own segment, at a lower daily cap, watched for bounces | Healthy mailboxes, and the list is mostly large companies where catch-all is common |
| Extra check on catch-alls | Catch-alls go through a verifier that specialises in accept-all domains before deciding | The catch-all share is large enough to matter |

Record the policy and the count it touched in the report.

---

## 6. Buckets and reconcile

One bucket per contact: `VALID (own file)` · `VALID (provider name)` · `CATCH_ALL` · `WRONG_PERSON` · `GONE (company)` · `NONE`. Say the sum out loud against rows in.

Output columns appended to the list: `email`, `email_status` (valid / catch-all / none), `email_source` (own file or provider name), `email_run` (run label with date), `verifier_verdict`, `mx_host`, `identity_check` (pass / review), `note`. Blank means nothing found, never "not checked"; say so in the README.

---

## 7. Fill-rate report

| Provider (in order) | Contacts sent | `VALID` found | Share of all `VALID` | Credits used | Cost per valid |
|---|---|---|---|---|---|

Under it:
- Total coverage: `VALID` / rows in, and separately catch-all and none.
- What each later provider added on top of the earlier ones.
- Compared with the bake-off or pilot: where the full run differed and the likely reason (the list is broader than the sample, a provider was rate-limited, a key was shared).
- Credits before and after per provider, and credits avoided by free matches and the cache.

---

## 8. Files

- The enriched list (all original columns, results on the right).
- `set-aside.csv`: catch-all, wrong person, gone, none, each with its reason.
- `cache/` (raw responses, one file per provider) and `provider-notes.md`.
- `README.md` in plain English: what each file is, what blank means, what to do next, in order.
- If the owner runs their own second waterfall later (for example in their own enrichment table), merge its results by LinkedIn URL, never by name, and re-verify anything it adds.
