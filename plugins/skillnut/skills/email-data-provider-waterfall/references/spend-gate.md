# Spend gate: triage, quote, pilot, then the big run

Load this before any paid step: every provider call in the bake-off and in the waterfall run. The gate has five steps. Never skip to step 5.

| Step | What happens | Costs credits? |
|---|---|---|
| 1. Free triage | Decide which rows need a paid check at all | No |
| 2. Cost estimate | Price the rows that are left, by bucket | No |
| 3. Pilot | Run a small random sample through the real providers | A little, with a hard cap |
| 4. Quote and go | Extrapolate, show the quote, set a ceiling, get the go | No |
| 5. Residual run | Send only the rows that still need it; report credits saved | Yes, capped |

The rule behind it: **if the answer is already in the file, or can be found for free, do it locally and say it cost zero credits.** Paid tools are for real lookups only: emails, phones and people that are not in the data yet.

---

## Step 1. Free triage (credit triage)

Goal: split every row into **confirmed** (no paid check needed), **skip** (exclude, no check needed) or **needs a paid check**. Only the last group goes to a paid tool.

1. **Unify the files under one key.** If the work spans several files, give each row a stable key (CRM record id, or file name plus row number) and a source tag. Dedupe domains before any scan, so a domain shared by many rows is checked once.
2. **Liveness scan.** Run a domain liveness scan (resumable, with a second DNS pass on every dead or error result). Only a name that no longer resolves counts as conclusive. A raw connection failure is not proof a company is dead: on one real run the first-pass "dead" rate was three to four times higher for Japan, China and Argentina than for the US, because of geo-blocking and TLS quirks, not closures.
3. **Cheap description scrape.** For domains with no profile match, fetch the homepage yourself (plain HTTP, browser User-Agent, short timeout, read the first ~150 KB) and pull the `<title>`, the meta description and the og:description. No LLM and no per-page tool, so it costs nothing. On a real run about half of the domains returned usable text, which more than doubled description coverage when added to a paid profile source. Two guards:
   - Judge exclusions on the title and meta description only (the company's own words), never on the meta keywords blob, which is SEO stuffing.
   - Detect parked and spam pages (gambling and casino words in the title) as dead for outreach. Match these patterns on the title, never on body text: a real product page can contain "shield" or "coming soon".
4. **Known status and knowledge pass.** Apply the known-status file (acquired, defunct, renamed) first. Then a model knowledge pass over company names in priority tiers, largest revenue bands first, in batches of about 200 rows. Write only confident verdicts (large confirmed, active confirmed, recognised, acquired, defunct); absent means unknown.
   - **Watch the knowledge cliff.** Model knowledge falls off sharply below mid-size companies. After the top tiers, test a random sample of about 80 rows from the rest. If fewer than about 1 in 10 are recognised, stop row-by-row judging: it would spend a large token budget to write "unknown" thousands of times. Use the known-status file and a name-to-domain mismatch check for the long tail instead.
   - **A hedged verdict is not a verdict.** If the model's own note says "verify", downgrade it to needs a paid check.
5. **Verdict per row,** with an action code so the client can see why:

| Action | Meaning |
|---|---|
| `SKIP_CONFIDENT` | Known and active; no paid check |
| `SKIP_DATA_COMPLETE` | Site live and the fields you need are already filled |
| `FIX_DOMAIN_FREE` | Company is fine, domain is wrong; fixed without a paid call |
| `EXCLUDE_FREE` | Conclusively gone (domain no longer resolves, or parked) |
| `PAID_VERIFY` | Needs the full paid check |
| `PAID_FIELD_ONLY` | Only one field is missing (for example revenue); ask for that field alone |

Traps that triage must not fall into (each one happened on a real run):
- **A dead domain is not a dead company.** A dead subdomain of a large, healthy company must route to "fix domain", never "exclude". Assert that no large-confirmed row can be excluded.
- **An acquisition is not a dead account.** An acquired company that still runs its own brand, site and team is still sellable. Exclude only when the domain redirects to the acquirer or is gone, and only when knowledge backs the redirect: a redirect alone can be a partner link.
- **A paid tool's "success" flag is not success.** One scrape tool reported success on rows whose body held its own error payload. Read the content, not the status column.
- **The paid tool's resolver can be worse than yours.** If the paid tool says "DNS gone" but your scan resolved the domain, the row goes to a conflict check, not to delete.

Report triage in one line with the split, for example: *"Of 8,000 rows, 5,100 need no paid check, 300 are conclusively gone, and 2,600 go to the paid step."* (Illustrative numbers.)

---

## Step 2. Cost estimate

Price the residual by bucket, because the buckets cost very different amounts:

| Bucket | What it is | Relative cost (rule of thumb from real runs) |
|---|---|---|
| Verify email | Live mailbox check on an email you already have | Lowest |
| Verify mobile | Line-type and identity check on a number you already have | Several times an email check |
| Find email | Waterfall for a new email | Low to medium; one expensive provider can dominate |
| Find mobile | Waterfall for a new mobile | Highest; often about ten times finding an email |

- **Verifying is usually cheaper than finding,** so verify what you have before you look for anything new, and only run finders on the rows that failed.
- **Use providers the client already pays for first.** A provider on the client's own key can lead the waterfall at no extra platform cost; on one real pilot it found about half of the replacements at no extra cost.
- **Know how each provider charges a miss.** Some charge only when they find something, even where their docs say a miss still costs a credit. Measure it in the pilot instead of trusting the docs.
- **Prerequisites change the price.** Many phone providers need a LinkedIn URL. If the export has none, either budget a profile lookup first or accept lower phone coverage.

---

## Step 3. Pilot

- **Sample.** Draw a random sample from the rows that qualify (for a contact test, the rows that have an email, a mobile and a domain), with a fixed seed so it can be re-drawn. Size: 100 to 200 contacts for a client-facing cost test; 5 rows per provider or about 25 domains for a quick usage check before a bulk lookup (the shared ground rules).
- **Phase 1: verify only,** on the whole sample, with a hard ceiling set in the runner.
- **Phase 2: find only on the failures,** quoted precisely after phase 1 is in. Optionally a deeper pass with extra providers on what is still missing, if the user asks to push coverage.
- **Measure real usage.** Read each provider's balance before and after, or, when two scripts share a key, read the per-call usage field in each response: a balance delta is confounded by the other script.
- **Checkpoint every call** (shared ground rules), so a re-run never pays twice.

Report the pilot as a funnel, one column per channel:

| Stage | Mobile | Email |
|---|---|---|
| Tested | 150 | 150 |
| Valid and kept | 128 | 104 |
| Invalid or bad | 22 | 46 |
| New one found | 17 | 39 |
| Still missing | 5 | 7 |
| **Final usable** | **145** | **143** |

Then the cost split, verify against find, mobile against email, and the per-contact cost. All figures here are illustrative.

**Explain every miss in plain words.** Common reasons: the person left the company; a low digital footprint; a truncated name in the CRM (a last initial only); a personal email domain, where no work email exists to find; no LinkedIn URL in the export, so phone providers could not run; a strict enterprise mail server that will not confirm any address. Say clearly: **"missing" means no provider we ran had it, not that the person has no phone or email.**

**Check line type, not just validity.** A number can be valid and still be an office line or VoIP. Report the split (mobile, landline, VoIP, stale, invalid): it answers the question most clients actually have, "are these real mobiles?"

---

## Step 4. Quote and go

- **Extrapolate** from the pilot to the full set: verify cost for every row, plus find cost for the expected failure rate. Name the expected counts too (for example "about 1 in 4 emails will need replacing").
- **Haircut pilot hit rates.** A finder that hit about two thirds of a small pilot fell to about half at full scale on a real run. Quote the find side with a margin.
- **Show the quote** with the ceiling, then wait for the go. Model:

> Here's what the full run would cost, based on the pilot. Verifying all 3,400 contacts: about 1,500 credits. Finding replacements for the roughly 900 that will fail: about 400 more. Your own finder key covers most of the finding for free. I'll set a hard stop at 2,000 credits. Want me to go?

(Illustrative numbers.) Never start without an approved ceiling or an explicit go.

---

## Step 5. Residual run and report

- Run only the rows marked for a paid check, in the order verify, then find on failures.
- Set the hard budget stop in the runner, not just in your head.
- At the end, report credits used per provider (before and after), the credits **avoided** by triage (rows that never went to a paid tool), and the funnel at full scale. Compare it with the pilot and say plainly where the two differ.
- Deliverables: the contact-level result with a `source` column per value (existing CRM data, which provider found it, found but not confirmed, or missing), and a short summary. Anything found but not verified is marked and kept out of the client sheet.
