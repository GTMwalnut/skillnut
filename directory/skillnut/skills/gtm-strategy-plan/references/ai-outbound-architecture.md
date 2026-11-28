# The AI outbound architecture (for plans that run agents across channels)

Load this when a plan's AI layer goes beyond drafting: a scope of work with an orchestration track, a client asking "what does the whole system look like", or a plan that runs email, LinkedIn and other channels from one set of agents. The main skill's AI layer section carries the rules; this file carries the layers they sit in, so the plan can show the system as one connected flow rather than a list of tools.

Tool names are examples of what fits each layer, not requirements.

## The layers, in order

| # | Layer | What happens | Example tools |
|---|---|---|---|
| 1 | Intent sources | Watch for accounts already showing intent: funding, news, hiring, website visitors, LinkedIn engagement, plus custom signals for the client's market | Clay, RB2B, n8n agents, a visitor-identification tool |
| 2 | Database layer | One place the accounts and signals land: a warehouse or customer data platform for large teams, a sheet or a small database for small ones | Snowflake, Supabase, Google Sheets |
| 3 | Company enrichment and CRM hub | Revenue, headcount, industry, HQ location and tech stack added; the account pushed into the CRM, which stays the system of record | HubSpot, Salesforce, Attio |
| 4 | Contact enrichment | Emails, phone numbers and LinkedIn profiles found through a waterfall of providers | Prospeo, Apollo, Blitz, Clay, other email finders |
| 5 | Lead scoring and qualification | Each account and contact scored on ICP fit, intent strength and tech alignment, plus the patterns from closed-won deals, so the team only touches the strongest | n8n with a model, the ICP Builder's won-deal analysis |
| 6 | Message approval | The client approves the copy before the push; drafts reviewed with approve, edit or reject | Team chat (Slack, Google Chat), a review board |
| 7 | Multichannel outreach | Email, LinkedIn, newsletter retargeting, voicemail drops, and where in scope ads or gifting, all on one orchestration backbone | Email Bison, HeyReach, n8n, a voice tool |
| 8 | Conversation and response handling | Replies classified; interested leads alert the owner at once; AI may draft the nurture back-and-forth, a human approves every reply | n8n, the AI Responder skill's method |
| 9 | Meeting booking and handoff | Meetings auto-booked and routed to the right rep by territory, deal size or industry | Calendar booking, CRM routing |
| 10 | Pre-meeting prep | Deep company research (news, competitors, org chart, talking points) sent to the rep before the call | Claude Code, Clay |
| 11 | After the decision | Won deals into the customer-success workflow; lost deals into nurture (newsletters, mailers) until the timing is right | CRM workflows |

A compact way to present the same system to a founder: **find > clean > prep > send > replies**, run on a daily schedule early in the morning, with a human approving every message that leaves.

## The rules that ride with the layers

1. **Cross-channel stop.** A response on any channel automatically stops every other sequence to that person. Wire it once, on the orchestration backbone, not per tool.
2. **Human approval on every AI-written reply.** The AI drafts; a named person approves, edits or rejects before it sends. The same holds for first-touch copy, approved by the client per campaign.
3. **Pre-call research to the rep, every time.** The meeting is the expensive moment; the research that prepares it is cheap.
4. **Route, never share.** Every booked meeting has one owner, chosen by a rule the plan writes down.
5. **The CRM stays the system of record.** Every signal, touch and reply logs back with its source, so the next plan can be built on what actually happened.

## How much of this goes in the plan

- A lean pilot names the layers it uses in one line each and states rules 1 and 2. Most pilots run layers 1, 3, 4, 6, 7 and 8 only.
- A scope of work shows the full table, marks which layers are built in which phase, and names who owns each.
- Never draw layers the plan will not build; the what-we-won't-build list is the place to name the rest.

Point to the GTM Automations and n8n GTME Playbooks skills for the build itself, and to the AI Responder skill for reply handling.
