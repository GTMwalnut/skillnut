# Which Claude surface does which GTM job (option E)

A map of how one GTM agency splits its work across the parts of Claude. Use it to place this pipeline in a bigger setup. Say it in plain English, as a table, then offer option A.

| Surface | GTM job | Examples |
|---|---|---|
| **Claude Code** | Builds and multi-tool runs from the terminal | Outbound campaign planning (signals to enrichment to outreach, this skill), creating lead lists sourced and enriched with your tools, invoices, videos made from code; one session can call dozens of tools |
| **Scheduled routines** | Daily jobs that run without you | Updating an analytics dashboard every day, email deliverability checks, inbox rotation, status updates, notifications to the right people |
| **Projects** | The context layer | All the documents for one client or one offer live in one project, and every conversation about it stays inside it |
| **Skills** (SKILL.md files) | Repeatable plays | Campaign planning, CRM work, the outbound process, reply analysis, deliverability, tool calls. Claude Code runs over these skills to carry out the work; the skill this pipeline saves in Step 8 is one of them |
| **The API (Console key)** | Claude inside your own automations | An API key used in an automation tool such as n8n, or an always-on assistant, for lead and reply classification and replies |
| **Design** | Visual content | Workflow diagrams, charts and short motion videos for posts, drawn from ideas in your call notes and CRM |
| **Chat** | Quick, light work | Basic conversations, parsing a few documents, general questions |

Rule of thumb: build and test a play in Claude Code; save it as a skill once it works; move it to a scheduled routine when it should run every day; keep each client's or offer's context in its own project.

For scheduled and event-driven automations, see **gtm-automations** and **n8n-gtme-playbooks**.
