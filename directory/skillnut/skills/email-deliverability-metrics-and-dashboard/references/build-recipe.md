# The build recipe (Claude Code, step by step)

This is the concrete construction manual. It assumes you are running inside Claude Code (or any harness with a shell, Python, and file access) in the user's working folder. Follow it in order; the section numbers match the build flow.

## 1. The setup contract

Ask the user for three things and nothing more:

1. **The sending tool and workspace.** One dashboard audits one workspace.
2. **The credential.** Two acceptable forms:
   - an MCP connector for the tool, already configured, or
   - a plain text file in the working folder (the conventional name is `API Keys.txt`) with one block per workspace:

     ```
     Instance: https://send.example.com/
     Workspace: Acme Outbound
     Acme Outbound API Key: <the key>
     ```

   Read the key from the file at runtime with a small parser (match the workspace name on the line, extract the token pattern). **Never echo the key, never paste it into chat, never write it into any output file.** Refer to it only by location ("the key on line 3 of API Keys.txt").
3. **Optionally, their own deliverability playbook** (a PDF or doc). If given, extract its thresholds and let them override the defaults in the SKILL engine (chapters 1 to 10 and the defaults table). Extract PDF text with pymupdf or pdftotext; read every line, because thresholds hide in prose.

## 2. The architecture (why it is a generator, not a live page)

Build three source files plus outputs, all in the user's folder:

```
build_dashboard.py   fetch + cache + orchestrate (entry point; --refresh flag)
render.py            analyze(): raw data -> snapshot dict of computed metrics
html_report.py       render_html(): snapshot -> the finished HTML string
assets/              self-hosted fonts (woff2), downloaded once
deliverability_snapshot.json   the audit trail, written every build
<Client>-Deliverability.html   the deliverable
```

The page is **static, generated, self-contained**. Never build a live browser dashboard that calls the API from JavaScript: the key would have to live in client-side HTML (unacceptable), and sequencer APIs are not CORS-enabled anyway. Refresh means re-running the script. Cache every raw API response as JSON in a scratch directory so that re-analyzing or re-rendering never re-pulls; only `--refresh` re-pulls.

## 3. The API pull (reference implementation: Email Bison)

Email Bison is the reference because its API is clean and its self-hosted instances are common. Base is `https://<instance>/api/`, auth is `Authorization: Bearer <key>`, pagination is Laravel-style (`meta.last_page`, `?per_page=&page=`). The endpoint map and what each gives you:

| Endpoint | What it holds | Watch for |
|---|---|---|
| `GET /sender-emails` | every inbox: `email`, `type` (google_workspace_oauth / microsoft_oauth / smtp), `status` (Connected), `daily_limit`, `warmup_enabled`, `email_signature`, `tags` (provider names), `emails_sent_count`, `bounced_count`, `unique_replied_count`, `total_leads_contacted_count`, `created_at` | per_page up to 50 works; `warmup_enabled` is a boolean, NOT the score |
| `GET /warmup/sender-emails?start_date=&end_date=` | the same warm-up fields for **every** inbox over any date window you choose (3, 7, 10, 14, 30 days), one call per window instead of one per inbox | **15 rows per page whatever per_page says**; follow `meta.last_page` or every inbox past the fifteenth silently has no score |
| `GET /warmup/sender-emails/{id}` | **the warm-up score lives here**: `warmup_score`, `warmup_emails_saved_from_spam`, `warmup_replies_received`, `warmup_bounces_received_count`, `warmup_bounces_caused_count` | one call per inbox; run 8 to 10 concurrent |
| `GET /campaigns` | `open_tracking`, `plain_text`, `include_auto_replies_in_stats`, `emails_sent`, `bounced`, `replied`, `total_leads_contacted`, `status` | campaign stats may exclude auto-replies; compute landing from /replies instead |
| `GET /campaigns/{id}/sequence-steps` | `email_subject`, `email_body` (HTML with spintax braces and {TOKEN} merge fields), `variant`, `order` | the copy audit source; some campaigns build bodies from per-lead custom variables instead, shown as tokenized templates |
| `GET /replies` | every message: `folder` (Inbox / Bounced / Sent / Spam), `automated_reply` (boolean), `sender_email_id`, `from_email_address`, `date_received` | this is the landing-proof source; count folder=Inbox split by automated_reply, unique by from_email_address, attributed per inbox via sender_email_id |
| `GET /leads` | `email`, `first_name`, `last_name`, `company`, `status` (unverified / bounced / unsubscribed), `tags`, `custom_variables` | **hard-capped at 15 per page** regardless of per_page; a 7,000-lead workspace is roughly 460 pages; pull pages concurrently (12 to 16 workers), reassemble in order |
| `GET /tags` | the taxonomy | pull FIRST; it tells you what the lead tags can say |

**The lead tags are the treasure.** Email Bison auto-detects and tags every lead with its recipient mail server or gateway (Google, Outlook, Zoho, Custom Mail Server, **Proofpoint, Mimecast, Barracuda**) and tags reply outcomes (Interested, Meeting Booked, OOO, Automated Reply, Not Interested, Person not with org, Long Leave, Nurture Later). Both attributions in the SKILL engine are computed from these tags plus the replies feed.

**Porting to another sequencer** (Instantly, Smartlead, Lemlist, Salesforge, Apollo): the map above is a shopping list, not a schema. Hunt each row's equivalent with the probe ladder from the SKILL engine: accounts or sender lists with status and limits; a warm-up or health sub-resource with a numeric score; campaign settings with a tracking flag; sequence or template bodies; a replies or events feed with an automated/OOO classification; leads with a bounce status and any ESP or gateway detection. Whatever cannot be found after the full ladder is labeled "not measured", never guessed.

**Fetch code shape:** urllib or requests, Bearer header, 45s timeout, retry 429/5xx with backoff, `ThreadPoolExecutor` for the per-id and per-page fan-outs, every raw response dumped to the cache directory before any analysis touches it.

## 4. The local enrichment (free, no keys)

For each sending domain (derive the set from the inbox email addresses):

- **SPF:** DNS TXT on the domain; find the `v=spf1` record; note `-all` vs `~all`.
- **DMARC:** DNS TXT on `_dmarc.<domain>`; find `v=DMARC1`; extract `p=` (none / quarantine / reject).
- **DKIM:** probe selectors `selector1, selector2, google, default, k1, s1, s2, dkim, mail, smtp, key1` plus the sequencer's own, as TXT then CNAME at `<selector>._domainkey.<domain>`; any hit proves DKIM is published.
- **Age, registrar, and nameservers:** RDAP, no account needed: `https://rdap.verisign.com/{tld}/v1/domain/{domain}` for .com/.net, `https://rdap.org/domain/{domain}` otherwise. Take the `registration` event date, the registrar entity's `fn`, and the `nameservers` array (fall back to a DNS NS lookup if RDAP omits it). Flag same-day same-registrar batches. Derive a friendly DNS-host name from the nameserver root (`*.ns.cloudflare.com` means Cloudflare) and show **registrar and DNS host together**: the registrar is where the domain was bought (inbox providers often purchase via a wholesale reseller such as PDR on the buyer's behalf), the DNS host is who serves the zone (providers commonly manage zones on Cloudflare). Users check WHOIS, see a reseller they never heard of plus Cloudflare nameservers, and ask; the table should answer before they do.
- **BIMI:** TXT lookup at `default._bimi.<domain>` for a `v=BIMI1` record. Optional brand-logo polish, not a deliverability lever; show presence so the user can track it, and know the answer when a checker tool nags them about it (free self-asserted record works at Yahoo; Gmail needs a paid Verified Mark Certificate, rarely worth it for cold-email domains).
- **Blacklists, with the honesty rules:** DNS A-record query for `<domain>.dbl.spamhaus.org` and `<domain>.multi.surbl.org`, three attempts with a short backoff. Four distinct outcomes, never collapsed: NXDOMAIN means **clean**; a listing code means **listed**, and **the two lists use different codes**: Spamhaus DBL answers `127.0.1.x` (for example `127.0.1.2` spam domain), while SURBL answers `127.0.0.x` as a bitmask of its lists (for example `127.0.0.64` is the ABUSE list), so a check that only looks for `127.0.1.` reads every SURBL listing as clean; **answers in `127.255.255.x` from Spamhaus, or `127.0.0.1` from SURBL, mean the resolver is blocked from querying, not that the domain is listed** (report "query blocked"); persistent failure means **unchecked**, rendered as an amber "recheck", never as clean. Prove the whole check works before trusting any clean result: query the official always-listed test names, `dbltest.com` against the DBL and `test.surbl.org` against SURBL; both must return listed, or your resolver cannot see the lists and every clean is meaningless. Store the per-list status and surface it as a tooltip on the blacklist cell.

Use dnspython if present (`import dns.resolver`), else shell out to nslookup. Six to eight domains take seconds; run them concurrently with the API pull's tail.

## 5. The analysis pass

`analyze(data)` computes the snapshot dict. The exact metrics, levels, and thresholds are in the SKILL engine's metric canon, chapters 1 to 10 and the defaults table; implementation notes that save an hour each:

- **Rates:** bounce = bounced/sent per inbox and rolled up; reply rates = unique repliers / leads contacted. Guard every division by zero; inactive inboxes (sent=0) show a dash, not 0%.
- **Landing signal:** from replies with folder=Inbox, build per-inbox sets of unique repliers, split genuine vs automated by the flag; the including-OOO rate is the union set over leads contacted. Carry **both reply rates to every level**: per inbox, rolled up per domain, and in the cross-cuts; a table with only one of the two is incomplete.
- **Performance cross-cuts:** group the per-inbox records two ways, by inbox type (Google / Microsoft / SMTP) and by provider tag, and compute per group: inbox count and share, sent, bounce rate, genuine reply rate, including-OOO reply rate, mean warm-up. Render as two small tables in the ESP section. Groups that have not sent show dashes, not zeros.
- **The pass-through matrix (sending domain x gateway):** the answer to "which of my domains actually gets past Mimecast / Proofpoint / plain Outlook / custom servers", and the computation that turns the routing advice from generic to specific. Two joins build it:
  1. **Landings:** for each inbox-folder reply, `sender_email_id` names the sending inbox (so its domain), and the replier's address looked up in the leads map names the recipient's gateway tag. Count unique (inbox, replier) pairs per (domain, gateway); keep the genuine-vs-automated split.
  2. **Bounces:** bounce-folder records carry the sending inbox but usually name the failed recipient only inside the notice text; regex the subject plus body for any address that matches a known lead, and attribute the bounce to that lead's gateway. Expect only 35 to 45 percent of notices to parse; record the rate and print it.
  Cell value = the **pass-evidence ratio**, landings divided by landings plus attributed bounces. There is no true denominator (the sequencer does not record which gateway each inbox's contacted leads sat behind), so the ratio is evidence, not measurement; say so on the card. What it typically reveals, and why it is worth the work: one gateway turns out genuinely passable at volume, aged domains show materially better pass-evidence everywhere including against the hard gateway, and against the hardest gateway no domain is good, only least-bad; those three facts are the routing plan. Recompute on every refresh so routing changes show up in the ratios.
- **Bounce autopsy:** per lead, first gateway tag wins; bucket totals and bounced by gateway; compute each gateway's bounce rate and share of all bounces; compute hard-gateway vs everywhere-else rates; compute the counterfactual lead-level bounce with the worst gateway removed.
- **Bounce reason split (gateway vs invalid address):** for every bounce notice that parses (see the pass-through matrix), classify the notice text case-insensitively: policy or gateway wording (blocked, policy, rejected, spam, reputation, "not authorized") is a gateway refusal; non-existence wording (user unknown, unknown user, mailbox not found, no such user, does not exist, address rejected as invalid) is an invalid address; everything else is "reason unknown". Report all three counts and the parse rate. These word lists are a starting point; read ten notices from the user's own feed and extend them before trusting the split.
- **Copy audit:** strip HTML tags, resolve spintax `{a|b|c}` to its first option, drop `{TOKEN}` merge fields, then count words; flag `https?://` and `www.`; scan the spam-phrase list case-insensitively; a tokenized template with under 15 real words means the copy lives in per-lead custom variables, shown as a dash with a tooltip, not as zero words.
- **Verification heuristics:** name-in-email (first, last, initial+last, first+initial, substring for 3+ char names) and company-vs-email-domain token overlap, skipping free-mail domains. Label both as heuristics on the page; they are review queues, not verifier verdicts.
- **Health score:** weighted average of 0-to-100 sub-scores (reference weights in the SKILL engine); linear clamps are fine; keep the formula stable across refreshes so the trend is real.
- **Actions:** generate from the computed flags, each carrying `sev`, `title`, `norm`, `current` (with entities named), `fix`. Sort critical > serious > warning > note.

Write the whole snapshot to `deliverability_snapshot.json` (indent it; it is the audit trail).

## 6. The render pass

`render_html(S)` produces one complete HTML document string. The design system is `design-theme.md`; the structural must-dos regardless of theme:

- A real document: `<!doctype html>`, `<html lang>`, `<meta charset>`, **`<meta name="viewport" content="width=device-width, initial-scale=1">`**. Omitting the viewport meta silently breaks phone layout at a fallback width; omitting the doctype puts browsers in quirks mode.
- Page order: header band with "last refreshed" stamp, health gauge + sub-scores, stat tiles, priority action center, the nine sections, data-sources and methodology table, footer with the refresh command.
- Every table column carries a plain-language explanation (title-attribute tooltip or a "how to read this" line under the table); colleagues open this page with nobody there to explain it.
- Wide tables live inside their own `overflow-x: auto` wrapper; the page body never scrolls horizontally.

## 7. Verification before delivery (non-negotiable)

1. **Counts reconcile:** inboxes pulled equals the API's meta total; same for campaigns, leads, replies. Say the numbers.
2. **Spot-check two or three figures** against direct API calls (a domain's bounce rate, the count of inboxes below warm-up 85) so nothing was mangled in analysis.
3. **Secret scan:** grep the HTML and the snapshot for the key, for "Bearer", for "api key". Expect zero hits.
4. **Self-containment scan:** grep the HTML for external URLs (cdn, http src, @import, link rel). Expect zero.
5. **Render check:** screenshot the page headlessly (Chrome `--headless=new --screenshot`) at a desktop width and eyeball it for broken layout. Two quirks to know: Chrome on Windows will not shrink below roughly 500px window width, so verify narrow layouts with a scrollWidth probe injected into the page, not a 390px screenshot; and CSS width/height on inline elements silently no-op, so any bar or fill element needs `display: block`.
6. Tell the user the file opens offline in any browser, and how to refresh: `python build_dashboard.py --refresh`.
7. **DNS findings go stale in both directions, fast.** A missing DMARC or DKIM flagged at the last build is often fixed by the provider within days; if the user says a checker tool shows the record exists, re-run the live lookup before standing by the old result. On any refresh, bust the enrichment cache too, not just the API cache; a dashboard confidently reporting a gap the provider closed three days ago costs more trust than the gap did.
