# The bridge workflow, node by node

Reference build: Salesloft (email cadence) -> HeyReach (LinkedIn), with HubSpot for LinkedIn URLs, Email Bison as the other email tool, Claude for the rewrite and Slack for the summary. n8n Cloud, `executionOrder: v1`, workflow time zone set to the team's.

Every HTTP node that reads per person uses **Never Error** (and Full Response on write nodes) so each input item produces exactly one output item. Code nodes pair results by index (`$('Node').all()[i]`); one dropped item would shift every later person onto the wrong data, so never let a per-person HTTP node error out.

## Node map

| # | Node | Type | What it does |
|---|---|---|---|
| 1 | Schedule | Schedule Trigger | Cron `0 7,19 * * 1-5` |
| 2 | Settings | Code | All switches and IDs (below) |
| 3 | Get cadences | HTTP, paged | `GET /v2/cadences?per_page=100` (page until fewer than 100) |
| 4 | Get open LinkedIn tasks | HTTP, paged | `GET /v2/actions?type=integration&per_page=100` |
| 5 | Get LinkedIn campaigns | HTTP | HeyReach `campaign/GetAll` |
| 6 | Pick tasks | Code | Due, rep in map, outbound, not excluded, one per person, up to 3x the limit |
| 7 | Get person | HTTP | `GET /v2/people/{id}` |
| 8 | Get emails sent to person | HTTP | `GET /v2/activities/emails?per_page=100&person_id=` |
| 9 | Get Email 1 text | HTTP | `GET /v2/mime_email_payloads/{earliest sent email in this cadence}` |
| 10 | CRM contact | HTTP | HubSpot `GET /crm/v3/objects/contacts/{email}?idProperty=email&properties=hs_linkedin_url,firstname,lastname` |
| 11 | LinkedIn campaigns for lead | HTTP | HeyReach `campaign/GetCampaignsForLead` by profileUrl, else by email; batch 5 per second |
| 12 | Other email tool lead | HTTP | Email Bison `GET /api/leads/{email}` |
| 13 | Prepare LinkedIn lookup | Code | URL + names per person for the job-change list |
| 14 | Add to job-check list | HTTP | HeyReach `list/AddLeadsToListV2` to the job-change list; batch 5 per second |
| 15 | Wait for LinkedIn lookup | Wait | 60 seconds |
| 16 | LinkedIn profile now | HTTP | HeyReach `lead/GetLead` |
| 17 | Build lead records | Code | Decode Email 1, clean names, classify conflicts, skip reasons, build the prompt |
| 18 | Check job change | Code | Hold job changes, apply the per-rep limit |
| 19 | Ready for rewrite | Filter | `skip` is empty; Always Output Data on |
| 20 | Claude: rewrite Email 1 | HTTP | Anthropic Messages API; batch 3 per second; 120 s timeout |
| 21 | Check messages and plan actions | Code | Assemble message, run checks, emit one item per action |
| 22 | Route actions | Switch (expression `{{ $json.route }}`, 7 outputs) | 0 stop other LinkedIn, 1 pause other email, 2 and 3 free a pending lead, 4 add, 5 close task only, 6 summary |
| 23 | Stop in other LinkedIn campaign | HTTP | `campaign/StopLeadInCampaign` |
| 24 | Pause in other email tool | HTTP | Email Bison `POST /api/campaigns/{id}/leads/stop-future-emails` |
| 25 | Pause other campaign -> Remove pending lead -> Resume | HTTP x3 | Off until proven (`remove_pending`) |
| 26 | Add to rep campaign | HTTP | URL and body chosen in node 21 |
| 27 | Added OK? | Filter | `statusCode === 200 && !(body.failedLeadsCount > 0)` |
| 28 | Complete email-tool task | HTTP | Salesloft `POST /v2/activities {action_id}` |
| 29 | Write summary | Code | Builds the DM |
| 30 | Live run? | IF | `dry_run` is false |
| 31 | DM owner | Slack | Continue on error |

Group the canvas into: Find due tasks (2 to 6), Gather lead data (7 to 18), Write message (19 to 21), Free a pending lead (25), Summary (29 to 31).

## Settings

```js
// dry_run: true = read everything, write the messages, change NOTHING in campaigns, other email tools or the email tool
//          (the job-check list still gets the lookups; nothing can send from it).
// pilot_per_rep: max people per rep added per run (0 = no limit). Held and skipped people do not count.
// remove_pending: false until pause -> delete -> resume is proven on one lead.
return [{ json: {
  dry_run: true,
  pilot_per_rep: 5,
  remove_pending: false,
  jobcheck_list: <JOB_CHECK_LIST_ID>,
  reps: {
    '<EMAIL_TOOL_USER_ID_A>': { name: 'Rep A', campaignId: <CAMPAIGN_A>, listId: <LIST_A>, senderId: <SENDER_A> },
    '<EMAIL_TOOL_USER_ID_B>': { name: 'Rep B', campaignId: <CAMPAIGN_B>, listId: <LIST_B>, senderId: <SENDER_B> }
  },
  own_campaigns: [<CAMPAIGN_A>, <CAMPAIGN_B>],
  excluded_cadences: [<PARTNER_CADENCE_ID>],
  slack_user: '<OWNER_SLACK_ID>'
} }];
```

## Pick tasks

```js
const s = $('Settings').first().json;
const cads = {};
for (const p of $('Get cadences').all()) for (const c of ((p.json || {}).data || [])) cads[c.id] = c;
const acts = [];
for (const p of $('Get open LinkedIn tasks').all()) for (const a of ((p.json || {}).data || [])) acts.push(a);
acts.sort((a, b) => String(a.due_on || '') < String(b.due_on || '') ? -1 : 1);   // oldest due first
const out = []; const per = {}; const seen = {};
for (const a of acts) {
  const uid = String((a.user || {}).id || '');
  const rep = s.reps[uid];
  if (!rep || a.type !== 'integration' || a.due !== true) continue;          // due is a boolean; due_on is the date
  const cid = (a.cadence || {}).id;
  const c = cads[cid];
  if (!c || c.cadence_function !== 'outbound' || c.archived_at || s.excluded_cadences.indexOf(cid) !== -1) continue;
  const pid = (a.person || {}).id;
  if (!pid || seen[pid]) continue;
  seen[pid] = 1;
  per[uid] = (per[uid] || 0) + 1;
  if (s.pilot_per_rep && per[uid] > s.pilot_per_rep * 3) continue;           // limit itself is applied after the checks
  out.push({ json: { action_id: a.id, person_id: pid, cadence_id: cid, cadence_name: c.name, user_id: uid, rep: rep.name, due_on: a.due_on } });
}
return out;
```

## Get Email 1 text (URL expression)

```
https://api.salesloft.com/v2/mime_email_payloads/{{ ((($json.data || []).filter(e => e.cadence && e.cadence.id == $('Pick tasks').item.json.cadence_id && e.sent_at).sort((a, b) => (a.sent_at < b.sent_at ? -1 : 1))[0]) || {}).id || 0 }}
```
Id 0 returns an error body (Never Error), which becomes "Email 1 not found" downstream.

## Prepare LinkedIn lookup

```js
const s = $('Settings').first().json;
const T = $('Pick tasks').all(), P = $('Get person').all(), H = $('CRM contact').all();
function liUrl(u) {
  const v = String(u || '').trim();
  const i = v.toLowerCase().indexOf('linkedin.com/in/');
  if (i < 0) return '';
  const slug = v.slice(i + 16).split(/[/?#]/)[0];
  return slug ? 'https://www.linkedin.com/in/' + slug : '';
}
return T.map((t, i) => {
  const p = (((P[i] || {}).json || {}).data) || {};
  const hs = (((H[i] || {}).json || {}).properties) || {};
  const url = liUrl(p.linkedin_url) || liUrl(hs.hs_linkedin_url);
  return { json: { url: url || 'https://www.linkedin.com/in/no-profile-on-file-000', listId: url ? s.jobcheck_list : 0,
    first: String(p.first_name || hs.firstname || 'Unknown'), last: String(p.last_name || hs.lastname || 'Unknown') } };
});
```
Add body: `{ listId, leads: [{ profileUrl, firstName, lastName }] }`. listId 0 fails harmlessly and keeps the item count. GetLead body: `{ profileUrl: $('Prepare LinkedIn lookup').item.json.url }`.

## Build lead records (decode and classify)

```js
const s = $('Settings').first().json;
const T = $('Pick tasks').all(), P = $('Get person').all(), M = $('Get Email 1 text').all();
const H = $('CRM contact').all(), C = $('LinkedIn campaigns for lead').all(), B = $('Other email tool lead').all();
const camps = {};
for (const c of (($('Get LinkedIn campaigns').first().json || {}).items || [])) camps[c.id] = c;

// Repair cp1252 and broken characters to plain ASCII punctuation
function plain(t) {
  return String(t || '')
    .replace(/([A-Za-z])�([A-Za-z])/g, "$1'$2").replace(/�/g, ' ')
    .replace(/[‘’\u0091\u0092]/g, "'").replace(/[“”\u0093\u0094]/g, '"')
    .replace(/[–—\u0096\u0097]/g, '-').replace(/[…\u0085]/g, '...').replace(/ /g, ' ');
}
function hexDecode(str) { return str.replace(/=\r?\n/g, '').replace(/=([0-9A-Fa-f]{2})/g, (m, h) => String.fromCharCode(parseInt(h, 16))); }
function decodeWords(v) {   // RFC 2047 encoded subject words
  return v.replace(/=\?([^?]+)\?([QqBb])\?([^?]*)\?=/g, (m, cs, enc, txt) => {
    try {
      if (enc.toUpperCase() === 'B') return Buffer.from(txt, 'base64').toString('utf8');
      return Buffer.from(hexDecode(txt.replace(/_/g, ' ')), 'latin1').toString('utf8');
    } catch (e) { return m; }
  });
}
function mimeText(b64) {
  if (!b64) return { subject: '', body: '' };
  const raw = Buffer.from(b64, 'base64').toString('latin1');
  let he = raw.indexOf('\r\n\r\n'); if (he < 0) he = raw.indexOf('\n\n');
  const head = raw.slice(0, he).replace(/\r?\n[ \t]+/g, ' ');
  const sm = head.match(/^Subject:\s*(.*)$/im);
  const subject = plain(decodeWords(sm ? sm[1].trim() : ''));
  const idx = raw.search(/Content-Type:\s*text\/plain/i);
  let part = idx > -1 ? raw.slice(idx) : raw.slice(he);
  const pe = part.search(/\r?\n\r?\n/);
  const ph = pe > -1 ? part.slice(0, pe) : '';
  let body = pe > -1 ? part.slice(pe).replace(/^\s+/, '') : part;
  const bnd = body.search(/\r?\n--[^\r\n]{6,}/);
  if (bnd > -1) body = body.slice(0, bnd);
  const cte = ((ph.match(/Content-Transfer-Encoding:\s*([^\s;]+)/i) || [])[1] || '').toLowerCase();
  let bytes;
  if (cte === 'quoted-printable') bytes = Buffer.from(hexDecode(body), 'latin1');
  else if (cte === 'base64') bytes = Buffer.from(body.replace(/\s+/g, ''), 'base64');
  else bytes = Buffer.from(body, 'latin1');
  const lines = plain(bytes.toString('utf8')).split(/\r?\n/);
  const keep = [];
  for (const raw of lines) {
    const l = raw.trim();
    if (/^(best|thanks|thank you|regards|kind regards|warm regards|cheers|sincerely)\b[ ,.!]*$/i.test(l) || /^--\s*$/.test(l)) break;   // signature
    if (keep.length === 0 && /^(hi|hello|hey|dear)\b/i.test(l) && l.length < 40) continue;                                            // greeting
    keep.push(l);
  }
  return { subject, body: keep.join('\n').replace(/\n{3,}/g, '\n\n').trim() };
}
function cleanFirst(f) {
  let x = String(f || '').replace(/^\s*(dr|mr|mrs|ms|prof)\.?\s*/i, '').replace(/[^A-Za-z' -]/g, ' ').trim().split(/\s+/)[0] || '';
  if (x.length < 2) return '';
  if (x === x.toUpperCase() || x === x.toLowerCase()) x = x.charAt(0).toUpperCase() + x.slice(1).toLowerCase();
  return x;
}
// liUrl as in Prepare LinkedIn lookup

const out = [];
for (let i = 0; i < T.length; i++) {
  const t = T[i].json;
  const p = ((P[i] || {}).json || {}).data || {};
  const mail = mimeText((((M[i] || {}).json || {}).data || {}).raw || '');
  const hs = ((H[i] || {}).json || {}).properties || {};
  const url = liUrl(p.linkedin_url) || liUrl(hs.hs_linkedin_url);
  const first = cleanFirst(p.first_name || hs.firstname);
  const rep = s.reps[t.user_id];
  const r = { action_id: t.action_id, person_id: t.person_id, rep: t.rep, cadence_name: t.cadence_name,
    first_name: first, last_name: String(p.last_name || '').split(',')[0].trim(), company: p.person_company_name || '',
    title: p.title || '', email: p.email_address || '', linkedin_url: url,
    email1_subject: mail.subject, email1_body: mail.body,
    campaignId: rep.campaignId, listId: rep.listId, senderId: rep.senderId,
    already_in_own: false, hr_stop: [], hr_pending: [], bison_stop: [], skip: '' };
  for (const c of (((C[i] || {}).json || {}).items || [])) {
    if (s.own_campaigns.indexOf(c.campaignId) !== -1) { r.already_in_own = true; continue; }
    const camp = camps[c.campaignId] || {};
    if (camp.status === 'FINISHED' || c.campaignStatus === 'FINISHED') continue;
    if (['InSequence', 'InProgress'].indexOf(c.leadStatus) !== -1) r.hr_stop.push({ campaignId: c.campaignId, name: c.campaignName });
    else if (c.leadStatus === 'Pending') r.hr_pending.push({ campaignId: c.campaignId, name: c.campaignName, listId: camp.linkedInUserListId, running: camp.status === 'IN_PROGRESS' });
  }
  const bl = ((B[i] || {}).json || {}).data || {};
  for (const lc of (bl.lead_campaign_data || [])) if (lc && lc.status === 'in_sequence') r.bison_stop.push({ campaign_id: lc.campaign_id, lead_id: bl.id });
  if (!mail.body) r.skip = 'Email 1 not found in the email tool';
  else if (!url) r.skip = 'No LinkedIn URL in the email tool or CRM (enrichment lookup needed)';
  else if (!first) r.skip = 'First name unusable: ' + (p.first_name || '(blank)');
  r.prompt = 'Prospect: ' + first + ' ' + r.last_name + ', ' + r.title + ' at ' + r.company + '\n' +
    'Email subject: ' + mail.subject + '\n\nEmail body:\n' + mail.body;
  out.push({ json: r });
}
return out;
```

## Check job change

```js
const s = $('Settings').first().json;
const G = $('LinkedIn profile now').all();
const STOP = ['inc','incorporated','llc','ltd','limited','corp','corporation','co','company','the','and','of','pharmaceuticals','pharmaceutical','pharma','therapeutics','biosciences','bioscience','bio','biotech','biotherapeutics','sciences','science','group','holdings','plc','gmbh','ag','sa','nv','bv','lp','health','healthcare','labs','laboratories','medical','international','global','us','usa','america','north','com','www'];
// Adjust STOP to the client's industry: generic words of that industry must not count as a match.
const toks = x => String(x || '').toLowerCase().replace(/&/g, ' and ').replace(/[^a-z0-9 ]/g, ' ').split(/\s+/).filter(t => t.length >= 3 && STOP.indexOf(t) === -1);
const compact = x => String(x || '').toLowerCase().replace(/[^a-z0-9]/g, '');
const initials = x => String(x || '').toLowerCase().replace(/[^a-z0-9 ]/g, ' ').split(/\s+/).filter(w => w && ['the','and','of','inc'].indexOf(w) === -1).map(w => w.charAt(0)).join('');
const coSlug = u => { const m = String(u || '').match(/linkedin\.com\/company\/([^/?#]+)/); return m ? m[1].replace(/-/g, ' ') : ''; };
function currentCos(g) {
  const names = [g.companyName, coSlug(g.companyUrl)];
  let ex = g.experiences;
  if (typeof ex === 'string') { try { ex = JSON.parse(ex); } catch (e) { ex = []; } }
  if (!Array.isArray(ex)) ex = [];                                   // sometimes "0"
  for (const e of ex) if (e && !e.end) { names.push(e.companyName); names.push(coSlug(e.companyUrl)); }
  return names.filter(n => n && String(n).trim());
}
function sameCo(slCo, email, liNames) {
  const em = String(email || '');
  const dom = em.indexOf('@') > -1 ? em.split('@')[1].split('.')[0] : '';
  for (const x of [slCo, dom]) for (const y of liNames) {
    if (!x || !y) continue;
    const tx = toks(x), ty = toks(y);
    if (tx.some(t => ty.indexOf(t) > -1)) return true;
    const cx = compact(x), cy = compact(y);
    if (cx.length >= 4 && cy.length >= 4 && (cx.indexOf(cy) > -1 || cy.indexOf(cx) > -1)) return true;
    const ix = initials(x), iy = initials(y);
    if ((ix.length >= 2 && ix === cy) || (iy.length >= 2 && iy === cx)) return true;
  }
  return false;
}
const recs = $input.all(); const out = [];
for (let i = 0; i < recs.length; i++) {
  const r = Object.assign({}, recs[i].json);
  const g = ((G[i] || {}).json) || {};
  const li = currentCos(g);
  r.li_company = g.companyName || li[0] || '';
  r.li_checked = li.length > 0;
  r.job_change = false;
  if (!r.skip && li.length && !sameCo(r.company, r.email, li)) {
    r.job_change = true;
    r.skip = 'Company changed: email tool ' + (r.company || '?') + ', LinkedIn now ' + r.li_company;
  }
  out.push({ json: r });
}
const per = {};
for (const o of out) {
  const r = o.json;
  if (r.skip) continue;
  per[r.rep] = (per[r.rep] || 0) + 1;
  if (s.pilot_per_rep && per[r.rep] > s.pilot_per_rep) { r.skip = 'Deferred to next run'; r.deferred = true; }
}
return out;
```

## Claude: rewrite Email 1 (HTTP body)

Headers: `anthropic-version` (current), credential type `anthropicApi`. Use the current Claude model, `output_config: { effort: 'low' }`, `max_tokens: 4000`, and the server-side refusal fallback where the account supports it.

```
system:
You rewrite a sales rep's first cold email into one LinkedIn message from the same rep to the same person.
Rules:
- Keep the same specific facts, angle and question as the email. Do not add new claims, numbers, names or offers.
  If the email has many details, keep the one or two strongest.
- Strictly under 60 words. Plain and conversational, first person, like a short note on LinkedIn.
- No greeting and no sign-off: they are added separately. Start with the first sentence.
- Plain ASCII only: straight quotes and apostrophes, hyphens instead of dashes, no emoji, no bullet points, no links, no email addresses.
- Some characters in the email may be garbled; infer the intended word.
- Two or three short paragraphs separated by one blank line. End with the email's question or a soft ask to talk.
Return only the message text.
user: {{ $json.prompt }}
```
The 60-word target keeps the 80-word check passing; at "under 80" one in ten came back at 89.

## Check messages and plan actions

```js
const s = $('Settings').first().json;
const recs = $('Check job change').all().map(i => i.json);
const ready = $('Ready for rewrite').all();
const R = $input.all();
const rw = {};
for (let i = 0; i < ready.length; i++) {
  const r = (R[i] || {}).json || {};
  const text = (r.content || []).filter(b => b.type === 'text').map(b => b.text).join('\n').trim();
  rw[ready[i].json.action_id] = { text, stop: r.stop_reason || '', err: r.error ? (r.error.message || JSON.stringify(r.error)) : '' };
}
const plain = t => String(t || '').replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/[–—]/g, '-').replace(/…/g, '...').replace(/ /g, ' ');
const out = []; const done = [];
for (const r of recs) {
  if (!r.skip) {
    const x = rw[r.action_id] || {};
    const body = plain(x.text).replace(/^(hi|hello|hey)\b[^\n]*\n+/i, '').trim();
    const msg = 'Hi ' + r.first_name + ',\n\n' + body;
    const words = msg.split(/\s+/).filter(Boolean).length;
    if (x.err) r.skip = 'Claude error: ' + x.err;
    else if (x.stop === 'refusal') r.skip = 'Claude declined the rewrite';
    else if (!body) r.skip = 'Claude returned no text';
    else if (words >= 80) r.skip = 'Rewrite too long (' + words + ' words)';
    else if (!/^[\x0A\x0D\x20-\x7E]*$/.test(msg)) r.skip = 'Rewrite has non-ASCII characters';
    else if (/https?:|www\.|@/.test(msg)) r.skip = 'Rewrite contains a link or email';
    r.li_msg_1 = msg; r.words = words;
    r.inmail_subject = (r.email1_subject || 'Quick question').slice(0, 200);
  }
  done.push(r);
  if (r.skip || s.dry_run) continue;
  for (const h of r.hr_stop) out.push({ json: { route: 0, action_id: r.action_id, campaignId: h.campaignId, leadUrl: r.linkedin_url } });
  for (const b of r.bison_stop) out.push({ json: { route: 1, action_id: r.action_id, campaign_id: b.campaign_id, lead_id: b.lead_id } });
  if (s.remove_pending) for (const h of r.hr_pending) out.push({ json: { route: h.running ? 2 : 3, action_id: r.action_id, campaignId: h.campaignId, listId: h.listId, leadUrl: r.linkedin_url } });
  if (r.already_in_own) { out.push({ json: { route: 5, action_id: r.action_id } }); continue; }
  const camp = (($('Get LinkedIn campaigns').first().json || {}).items || []).filter(c => c.id === r.campaignId)[0] || {};
  const lead = { profileUrl: r.linkedin_url, firstName: r.first_name, lastName: r.last_name, companyName: r.company, position: r.title, emailAddress: r.email,
    customUserFields: [{ name: 'li_msg_1', value: r.li_msg_1 }, { name: 'inmail_subject', value: r.inmail_subject }] };
  const running = camp.status === 'IN_PROGRESS';
  out.push({ json: { route: 4, action_id: r.action_id,
    hr_url: 'https://api.heyreach.io/api/public/' + (running ? 'campaign/AddLeadsToCampaignV2' : 'list/AddLeadsToListV2'),
    hr_body: running ? { campaignId: r.campaignId, accountLeadPairs: [{ linkedInAccountId: r.senderId, lead }] } : { listId: r.listId, leads: [lead] } } });
}
out.push({ json: { route: 6, records: done } });
return out;
```
A running campaign takes leads through `AddLeadsToCampaignV2`; a draft campaign takes them through its list. The Complete-task node reads `$('Route actions').item.json.action_id`, so it works from both the add path and route 5.

## Write summary

```js
const s = $('Settings').first().json;
const safe = n => { try { return $(n).all(); } catch (e) { return []; } };
const okCount = n => safe(n).filter(i => { const c = (i.json || {}).statusCode; return c >= 200 && c < 300; }).length;
const all = $input.first().json.records || [];
const recs = all.filter(r => !r.deferred);
const NL = '\n';
const lines = ['*LinkedIn -> HeyReach' + (s.dry_run ? ' (DRY RUN: nothing changed)' : '') + '*'];
for (const rep of Object.values(s.reps).map(r => r.name)) {
  const ok = recs.filter(r => r.rep === rep && !r.skip);
  lines.push('*' + rep + ':* ' + ok.length + (s.dry_run ? ' ready to send' : ' sent to HeyReach'));
}
if (!s.dry_run) lines.push('HeyReach adds OK: ' + safe('Added OK?').length + ', tasks completed: ' + okCount('Complete email-tool task'));
lines.push('*Moved:* ' + recs.filter(r => !r.skip && r.hr_stop.length).length + ' from other HeyReach campaigns, ' +
  recs.filter(r => !r.skip && r.bison_stop.length).length + ' paused in the other email tool');
const held = recs.filter(r => r.job_change);
if (held.length) lines.push('*Held, company changed (' + held.length + '):*' + NL + held.map(r => '- ' + r.first_name + ' ' + r.last_name + ' (' + r.rep + '): email tool says ' + (r.company || '?') + ', LinkedIn says ' + r.li_company + ' ' + r.linkedin_url).join(NL) +
  NL + '_Not sent. The task stays open, so they show here each run until the record is fixed or the step is skipped._');
const unchecked = recs.filter(r => !r.skip && !r.li_checked);
if (unchecked.length) lines.push('*Company not checked, sent anyway (' + unchecked.length + '):*' + NL + unchecked.map(r => '- ' + r.first_name + ' ' + r.last_name + ', ' + r.company + ' (' + r.rep + ') ' + r.linkedin_url).join(NL));
const need = recs.filter(r => r.skip && !r.job_change).map(r => '- ' + r.first_name + ' ' + r.last_name + ', ' + r.company + ' (' + r.rep + '): ' + r.skip);
if (!s.remove_pending) for (const r of recs.filter(r => !r.skip && r.hr_pending.length)) need.push('- ' + r.first_name + ' ' + r.last_name + ': waiting in ' + r.hr_pending.map(h => h.name).join(', ') + ', remove by hand');
if (need.length) lines.push('*Needs you (' + need.length + '):*' + NL + need.join(NL));
if (all.length > recs.length) lines.push((all.length - recs.length) + ' more due LinkedIn tasks wait for the next run (limit ' + s.pilot_per_rep + ' per rep).');
return [{ json: { text: lines.join(NL), dry_run: s.dry_run, records: all } }];
```

## Reply sync branch (in Stop Outreach)

Wired from the HeyReach reply webhook, in parallel with the existing paths:

1. **Code "Bridge lead?"**: return nothing unless `body.campaign.id` is one of the rep campaigns; email = `lead.custom_email || lead.email_address || lead.enriched_email`, lowercased.
2. **HTTP** `GET /v2/people?email_addresses[]=<email>` (Salesloft returns exact matches).
3. **Code**: keep the row whose `email_address` equals the email exactly; else stop.
4. **HTTP** `GET /v2/cadence_memberships?person_id=<id>&per_page=100`.
5. **Code**: rows with `currently_on_cadence` true.
6. **HTTP** `DELETE /v2/cadence_memberships/<id>.json`.

The HeyReach reply payload carries `campaign {id, name}`, `lead {profile_url, first_name, last_name, company_name, email_address, custom_email, enriched_email}`, `recent_messages` or `recent_inmails` with `is_reply`, and `event_type`.

## Daily Conflict Check exclusions

In the node that lists campaign lists: add the rep lists to `EXCLUDED_LISTS`. In the node that plans stops: add the rep campaigns to `EXCLUDED_HR_CAMPAIGNS`, and make queued people never blacklisted when they sit in a rep campaign:
```js
const inBridge = allCamps.some(c => OWN_CAMPAIGNS.indexOf(c.campaignId) !== -1);
const queued = inBridge ? [] : camps.filter(c => c.leadStatus === 'Pending');
```
The job-change list needs no exclusion: it belongs to no campaign, and the check only reads lists of running campaigns.

## Client reference block

| Item | Value |
|---|---|
| Bridge workflow | name, ID, link |
| Schedule and time zone | |
| Reps | email-tool user ID, LinkedIn sender ID, campaign ID, list ID |
| Job-change list ID | |
| Excluded cadences | |
| Credentials (names only) | email tool, LinkedIn tool, CRM, other email tool, Claude, Slack |
| Stop Outreach branch | workflow ID, date live |
| Conflict Check exclusions | date published |
| Settings now | dry_run, pilot_per_rep, remove_pending |
| Open items | |
