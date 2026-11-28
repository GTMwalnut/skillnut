# Skillnut: GTM and Marketing Skills

41 free GTM and marketing skills by GTM Walnut: ICP and target lists, buying signals, cold email and LinkedIn outreach, CRM and RevOps, automation, dashboards, content and ads.

Each skill is a guided run, built from real client work: it asks a few questions, shows a plan, and does the work with you. Read-only by default; nothing is sent or written without your yes.

Not sure where to start? Ask "Which Skillnut skill should I use?" and the guide (`skillnut-start`) points you to the right one.

## Install

- **Claude Code, as a plugin:** `/plugin install skillnut --marketplace gtmwalnut/skillnut`
- **Claude Code, Cursor, Codex or any agent that reads SKILL.md:** `npx skills add gtmwalnut/skillnut`
- **Claude.ai or Claude Desktop (Pro, Max, Team or Enterprise):** download `skillnut.zip` from https://skills.gtmwalnut.com, then Customize > Plugins > Add > Upload plugin. One file, every skill.
- **Free Claude plan:** download `skillnut-one-by-one.zip` from https://skills.gtmwalnut.com, unzip it, and upload each skill under Customize > Skills.

## The skills

### Core GTM skills (8)

The core GTM skills, plus a guide that points you to the right one: ICP, cold call openers, events, CRM data, a GTM dashboard, training docs and LinkedIn posts.

| Skill | What it does |
|---|---|
| `skillnut-start` | The front door to Skillnut, the GTM and marketing skills by GTM Walnut. |
| `icp-builder` | Build the user's Ideal Customer Profile from a deep context layer, not guesswork. |
| `cold-call-openers` | Open a cold call so the prospect stays on the line. |
| `linkedin-post-generator` | Writes, rewrites and diagnoses LinkedIn posts, and plans around them, in six modules run alone or together. |
| `conference-outreach` | Turns events into pipeline: conference speakers, attendees, webinars and event ROI. |
| `crm-data-health` | Diagnose, repair and keep fresh a B2B CRM's data in six modules, in a fixed order: measure first, fix companies before contacts, write to the CRM last and only with sign-off. |
| `gtm-analytics-dashboard` | Design and build a bird's-eye analytics and health dashboard for an entire AI-automated GTM workflow, from intent finding and enrichment to email deliverability: the architecture heartbeat (which sources, APIs, MCP connections and agents are working or broken, which inboxes and LinkedIn senders are connected and warming, whether reps get reply alerts), the funnel (lead volume by source daily, weekly, monthly; fit, dedup and CRM overlap; campaign and channel performance), and reply analytics (positive and negative by campaign, bounces, patterns by location and topic). |
| `meeting-to-training-doc` | Turns a recorded walkthrough, demo, onboarding call, or training session into a linear, illustrated training document. |

### GTM Engineering: Outbound Pipeline (18)

Everything from the market list to the booked meeting: targeting, buying signals, copy, campaign upload, deliverability and replies.

| Skill | What it does |
|---|---|
| `tam-list-builder` | Builds a defensible total addressable market end to end, for mainstream B2B, local or niche markets (contractors, clinics), enterprise named accounts and partner channels. |
| `outbound-targeting` | Builds a tight, in-motion, campaign-ready list instead of spraying a broad one. |
| `icp-fit-filter` | Strip non-buyers out of a campaign list, keeping only the companies and people that match the user's ICP. |
| `email-data-provider-waterfall` | Choose and order your email and contact data providers by testing them fairly, then run the waterfall on your full list. |
| `buying-signals-playbook` | Work out the events that mean an account is ready to buy, then run them. |
| `account-activity-surge` | Find the accounts that are heating up while nobody works them, in three modules. |
| `signal-to-crm-prospecting` | Runs a scheduled prospecting routine end to end: monitors chosen sources (websites, registries, news feeds, publications, job boards) for a trigger signal, qualifies the companies behind each signal against an ideal customer profile (ICP), dedupes against the CRM, creates the new companies in HubSpot with full field mapping and territory-based owners, finds the right people at each company through a data-provider waterfall (Clay, ZoomInfo, Prospeo, Oxygen), finds verified work emails, creates and links the contacts, and posts a short totals-only summary to a team Slack channel through a bot, with review items sent privately. |
| `reo-to-email-bison-and-heyreach` | Turns fresh Reo.dev developer-intent signals (GitHub repos, website, docs, LinkedIn) into outreach: pulls everyone new since the last batch, drops excluded signals and anyone already contacted (live campaigns, earlier batches, HubSpot, do-not-contact list, sender networks), applies the ICP plus seniority and account-tier gates, normalizes names, writes openers from each person's own signal, verifies emails, loads the running Email Bison and HeyReach campaigns, verifies the load, catches job changers, logs the batch. |
| `copywriting-messaging` | The one copywriting skill for cold outreach, in six modules run alone or together. |
| `proof-points-by-industry` | Turn a pile of case studies into an industry-indexed proof matrix, then pull the right proof into outreach so a pharma prospect hears a pharma story and a bank hears a bank story. |
| `campaign-send-checklist` | One pre-send check for a campaign list, in five modules run alone or together, removing people first and polishing last. |
| `crm-overlap-check` | Clean a campaign list against the user's CRM before launch: interactively walk them through removing every company in a live or won deal, every person already in an active conversation or who was on a closed-lost deal, anyone already in the system under the same name, and the team's close contacts. |
| `email-and-linkedin-sequencer-lead-upload` | Builds and loads outreach campaigns from a personalized lead list. |
| `email-linkedin-orchestrator` | Makes a separate email sequencer and LinkedIn tool behave like one multichannel sequence (the Lemlist idea, built with n8n), so a LinkedIn step in the email cadence happens on LinkedIn without a rep doing it by hand. |
| `local-business-outbound` | Runs the end-to-end cold email play for local businesses found through Google listings (restaurants, shops, clinics, trades), whose owners B2B databases barely cover. |
| `email-deliverability-metrics-and-dashboard` | Cold-email deliverability, practice and measurement. |
| `ai-responder` | Handle everything that happens after a cold email or LinkedIn message is sent, as a drafts-only AI responder with a human approving every send. |
| `campaign-reply-insights` | Analyzes cold email and LinkedIn campaign replies to learn what is working, and makes sure good replies get answered. |

### GTM Engineering & RevOps (15)

The systems behind the selling: CRM setup in HubSpot or Attio, scoring and attribution, n8n and agent automations, GTM strategy and growth programs.

| Skill | What it does |
|---|---|
| `hubspot-implementation-playbook` | Audit, rebuild and hand over a HubSpot portal in seven modules, in the order that avoids rework. |
| `attio-implementation-playbook` | Implements, audits and runs an Attio CRM workspace end to end, in the order that avoids rework: workspace settings, security and permissions, objects (standard, custom, attributes, statuses, imports, migration), lists, the workflow builder (block types, variables, testing, credits), ready-to-build automations (lead triage and round robin, closed-won handoff with a required-field gate, stale-deal sweep, form and webhook intake, MRR change routing, AI summaries, new person to LinkedIn invite), connecting tools (inbox and calendar, Slack, Typeform, Segment, n8n/Make/Zapier, REST API and webhooks), AI attributes, and one linked data model. |
| `lead-and-account-scoring` | Score and prioritise leads and accounts from your own CRM deal history (HubSpot, Attio or any CRM with an API or export), in five modules. |
| `lead-attribution-analysis` | Reconstructs the full multi-channel touch history for a set of target accounts to show what sequence of steps leads to a first appointment, and what happens to an account after a deal is lost. |
| `crm-outreach-sync-and-manual-upload` | Syncs email and LinkedIn outreach activity from sequencing tools (Email Bison, HeyReach, Instantly, Smartlead, Expandi) into a CRM (HubSpot, Salesforce, Attio, GoHighLevel, Close, Pipedrive) by API: creates or reuses the contact, attaches it to the right company, fills only empty fields, and logs each touch (sends, replies, forwards, invites, acceptances, messages) as a dated activity with direction. |
| `n8n-gtme-playbooks` | Builds and runs n8n lead-ops automations for outbound through Claude, from zero to live, even for first-time n8n users: n8n Cloud setup, the MCP link to Claude, credentials for every tool, and four playbooks. |
| `gtm-automations` | Pick and build the highest-leverage GTM automations from a catalog of thirteen: intent-based campaigns, human-in-the-loop outreach off website deanonymization, Slack approvals, social listening, local-business scraping, AI-agent orchestration, the LLM upgrade, AI note-taking, prompt-based list building, domain and inbox infrastructure, AI-native CRM workflows, flag-triggered phone and LinkedIn enrichment on the CRM via Clay, and CRM records pushed into HeyReach for LinkedIn connection requests, naming real tools for each (Clay, n8n, HeyReach, Instantly and many more). |
| `claude-code-outbound-pipeline` | Run a whole outbound campaign from Claude Code through APIs, from one brief. |
| `crm-agent-autopilot` | Sets up an AI agent to run recurring CRM jobs on its own, safely, one module at a time. |
| `gtm-strategy-plan` | Writes an AI-led GTM strategy plan framed as a diagnosis and one bet, not a menu: a correctable situation read, the one constraint, numbered decisions, an ordered lead-source mix (CRM reactivation first, signal-led outbound last), buying-group titles, a warm-up-led build order, a day-by-day cadence, a signal engine, agent rules (a reply anywhere stops every channel; a human approves every AI reply), lean measurement, a timeline, honest targets, a needs list. |
| `sales-call-insights` | Mines recorded sales conversations (demos, discovery, pricing calls) for the exact language buyers use, then turns it into outreach that gets replies. |
| `linkedin-ads-program` | Plan, launch and run a B2B LinkedIn Ads program end to end, in five modules. |
| `partner-and-creator-programs` | Build and run a partner and affiliate program and a creator program for a B2B SaaS company, or the agency running its growth, in seven modules. |
| `agency-back-office` | Run the contracts and the money admin of a small GTM, outbound or RevOps agency or consultancy, in eight modules. |
| `long-video-to-youtube-shorts` | Turns long-form videos (YouTube, Tella, Loom, Riverside, Descript, Zoom, or a local file) into 15 to 20 second vertical YouTube Shorts and publishes them. |

## What this plugin runs, sends or fetches

Skills are plain-text instructions. They run inside your own Claude session and use only the tools and connections you set up yourself (your CRM, email and LinkedIn tools, data providers, n8n). Anything that sends email, uploads leads or writes to a CRM shows you a plan first and waits for your yes. Nothing is sent to GTM Walnut.

A few skills include small scripts. Each runs on your computer only when its skill uses it:

| Script | What it does | Contacts |
|---|---|---|
| `account-activity-surge/scripts/build_surge_data.py` | Turn a cleaned activity log plus an account sheet into the surge dashboard JSON. | None (runs on your computer only) |
| `account-activity-surge/scripts/post_surge_alert.py` | Post the weekly surge message to Slack through the bot's incoming webhook, or test the webhook. | hooks.slack.com |
| `account-activity-surge/scripts/render_surge_dashboard.py` | Check a surge data file and put it into the dashboard template. | None (runs on your computer only) |
| `long-video-to-youtube-shorts/scripts/build_short.py` | Build a 1080x1920 Short: titles on top, content in the middle (top 70% together), camera strip in the bottom 30%. | None (runs on your computer only) |
| `long-video-to-youtube-shorts/scripts/transcript_words.py` | Read a YouTube auto-caption file (json3) and print word timings. | None (runs on your computer only) |
| `long-video-to-youtube-shorts/scripts/verify_sync.py` | Verify a rendered Short against its spec: is each cut the right moment, and are the lips in sync? | None (runs on your computer only) |

Privacy policy: https://gtmwalnut.com/privacy-policy
