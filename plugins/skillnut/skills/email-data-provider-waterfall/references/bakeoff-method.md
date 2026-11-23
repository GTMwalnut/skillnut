# Bake-off method: test every provider fairly on the user's own contacts

Load this when Part 1 runs. The goal is a ranking the user can defend to anyone, including a provider that lost: same input, same day, one referee, weights fixed in advance, every row published.

---

## 1. Fairness rules (write them into the report before the run)

| Rule | Why |
|---|---|
| Same contacts to every provider | Different samples measure different markets, not different providers |
| Same input fields, normalized once | Every lead gets the same resolved company domain and the same cleaned name, so no provider is handicapped by a messier row than its rivals |
| Same day | Provider databases change; a week apart is two different tests |
| Each provider through its own API, its own key | Claude Code calls each API directly; no reseller layer in between that could add its own waterfall |
| One run per provider: no hints, no retries, no second passes | A retry only one provider gets is a head start |
| One verifier, one configuration, one run, judging everyone | Whatever error the verifier has lands on every provider equally, so it cannot reorder the ranking |
| The verifier is not one of the providers | A provider grading its own answers is not a test |
| Weights fixed before any result is scored, identical for every provider | Nobody can tune the scoring after seeing who is ahead |
| Every row published | The result can be audited rather than trusted |

If the test is funded or requested by one of the providers, write that on the first page of the report. The method does not change.

---

## 2. The sample

- **Source:** the user's real target list, or a random draw from it with a fixed seed so it can be re-drawn. The bake-off only speaks for contacts shaped like the sample: if the list is local businesses, do not test on enterprise contacts.
- **Size:** about 100 to 250 contacts is enough to separate providers and cheap enough to run on every one of them. Every provider gets the whole sample, not a slice of it.
- **Normalize once, before any call:** resolve each company to one domain (registrable root), clean first and last names (see `name-and-company-normalization` if available), keep the LinkedIn URL in its full `https://www.linkedin.com/in/...` form. Freeze the sample file; every provider reads the same frozen file.
- **Describe its completeness in the report:** share with a full first and last name, share with a LinkedIn URL, share with a domain. A provider that needs a full name will find less on a list of first names than one that can work from a first name and a domain; the reader needs to know which kind of list this was.
- **Optional mobile slice:** if mobiles are in scope, note which rows are eligible (many phone lookups need a LinkedIn URL) and measure mobile coverage only on those.

---

## 3. Calibrate the referee

Before trusting the verifier, run it on a control set of addresses known to be live: people who replied to a real email from the user's mailboxes recently. The verifier should return deliverable on all of them.

- The one way a verifier can distort a comparison is by marking working addresses as dead, which strips coverage from every provider. A clean pass on known-live addresses rules that out.
- If it fails some, say how many, and either pick another verifier or report the calibration result next to the scoreboard.
- Use the same verifier at the same setting for the full waterfall later, so the bake-off and the full run speak the same language.

---

## 4. Run

1. Spend gate (`spend-gate.md`, steps 2 to 4): price the sample per provider plus the verifier, quote, ceiling, go.
2. For each provider, one pass over the frozen sample through its own API. Record per call: contact key, provider, request time, raw response, the provider's own confidence label, credits used if the response reports it. Append to `cache/<provider>.jsonl`.
3. Do not re-call a provider for a contact it missed. A miss is a result.
4. Collect every distinct returned address across all providers and send each once to the verifier at one setting. Store the verdict per address (deliverable, invalid, accept-all or catch-all, unknown).
5. Balance before and after for each provider; note whether misses were charged.

---

## 5. Classify and name-check

For every provider and contact, one bucket from the SKILL.md table: `VALID`, `DECLARED_VALID_FAILED`, `CATCH_ALL`, `UNBACKED`, `WRONG_PERSON`, `NONE`.

- Read the provider's own label, not your interpretation: only its top "valid" or "verified" label counts as declared valid. "Probable", "risky", extrapolated patterns, "email found" flags and accept-all scores are `UNBACKED`: the provider is honest enough to flag them as guesses, so they are never credited and never penalized.
- Name-check every address (SKILL.md, Identity check). A deliverable mailbox for the wrong person is `WRONG_PERSON`.
- Reconcile per provider: the six buckets sum to the sample size.

---

## 6. Metrics per provider

| Metric | Definition |
|---|---|
| Find rate | Contacts where the provider returned any address / sample size |
| Valid coverage | `VALID` / sample size. The headline number. |
| Deliverability (valid rate) | `VALID` / (`VALID` + `DECLARED_VALID_FAILED`): of what it sold as valid, how much survived |
| Dead emails shipped | Count of `DECLARED_VALID_FAILED`: the bounces it would have sold you |
| Catch-all share | `CATCH_ALL` / contacts with any address returned |
| Identity accuracy | 1 - (`WRONG_PERSON` / contacts with any address returned) |
| Cost per valid email | Credits (or money at list price) actually spent on the sample / `VALID`. Uses measured miss charging, not the docs. |
| List price per 1,000 | The provider's list price at one stated commitment level, the same level for every provider, written on the report |
| Mobile coverage (optional) | Verified mobiles / eligible rows, with line type (mobile, landline, VoIP) |
| Unique finds | Contacts where this provider is the only one with a `VALID` |

Also report, across all providers: contacts at least one provider found, contacts only one provider found, contacts nobody found. "Nobody found" means none of the tested providers had them, not that the person has no email.

---

## 7. Weighted score (optional, fixed in advance)

If the user wants one number, agree the weights in Stage 2 and write them in the report before scoring. A reasonable default to propose: valid coverage 40, deliverability 30, price 15, mobile coverage 15 (drop mobile and re-spread if mobiles are out of scope). Score each measure against the best provider on that measure, so 100 on a measure means nobody did better. Show the per-measure table next to the total; never show the total alone.

---

## 8. Simulate the waterfall order offline

Because every provider ran on every contact, any order can be tested on paper at no cost:

1. For each candidate order, walk each contact through the providers in that order and stop at the first `VALID`. Count combined coverage, the share filled by each position, and the cost (sum of each provider's charge for the calls it would actually receive, using measured miss charging).
2. Lead with the provider that gives the most `VALID` per unit of cost on this sample, unless its identity accuracy or deliverability is clearly worse than the next; a provider that sells bounces or wrong people goes later, never first, even when its coverage is high.
3. Choose each next position by what it adds on the leftovers (marginal valid finds per cost), not by its standalone coverage. A provider with high coverage that overlaps the first one almost completely adds little.
4. Drop a provider from the end when its marginal finds no longer pay for its calls; say so with the numbers.
5. Show the user the top two or three orders with combined coverage and cost each, and recommend one.

---

## 9. Report layout

1. First page: what was tested, the sample and its completeness, the date, the verifier and its calibration result, the weights, who funded or asked for the test (if anyone).
2. Scoreboard: one column per provider, one row per metric, the leader on each row marked.
3. Overlap: at least one found, only one found, nobody found; unique finds per provider.
4. Waterfall simulation: the candidate orders with coverage and cost, and the recommendation.
5. Per-row evidence: one row per contact, one column per provider with its bucket letter, and on click or in a second tab the exact address, the provider's own label and the verifier's verdict. Anyone can take any provider's addresses to a verifier of their choosing and re-check.

**Publishing it.** If the user wants to share the result publicly, check each provider's terms first (some forbid named comparisons); naming the others "Provider B, C, D" keeps the comparison within those rules. Keep every number the run produced; never round up a favourite or leave out a measure where it lost.
