# Connect and auth check

Load this in Stage 3, before any call to any tool. The job: every tool in the pipeline is connected one way, understood from its own docs, and proven to work with a harmless read, without a key ever appearing on screen.

## 1. Keys in local files

| Rule | Why |
|---|---|
| One plain `.txt` file per tool in a local folder (for example `api-notes/`), named after the tool | Claude Code finds the key by file name; you never paste it into the chat |
| Never in a repo, a shared drive, a CSV or a notes file | A key in GitHub or a shared file is a key anyone can use |
| Claude reads the key into memory at run time and sends it only in the auth header | The key is used, never shown |
| Never print, echo, log or summarise a key, in full or in part | A run recap once printed part of a key on screen, and it ended up in a recorded video. Recaps name the file, never the value |
| If you record your screen, mask anything sensitive before publishing | Same reason |
| If a key leaks anyway, rotate it in the tool | Saying "this key is not valid" on a video is not the same as rotating it |

How to find a key in most tools: Settings or Integrations, then API, then copy the key into its file.

## 2. API or MCP, not both

Many tools now offer both an API key and an MCP server. Pick one per tool for the whole run and tell Claude to ignore the other. Two routes into the same tool give two different views of its data and double the ways a call can go wrong.

| Use | Pick |
|---|---|
| Creating campaigns, creating and uploading leads, anything that writes | The API: you control the exact calls, and the docs tell you every field |
| Open-ended research across the web | An MCP is fine (a search or research MCP such as Exa, Parallel or Firecrawl) |
| Reading stats or lists | Either; pick one |

An orchestration layer (Deepline is one example) holds many providers behind one CLI and one account. If the user has one, it counts as the single route for every provider behind it.

## 3. Give Claude the API docs

Before the first call, fetch the tool's public API docs (every endpoint, its schema and its examples) or load a docs file the user provides. Then list, for the user, what the key can do: for an email tool, typically campaigns, leads, lead lists, sender accounts, conversations and stats. Never guess an endpoint or a field name from memory.

Read the docs like a dictionary, not a book: (1) write the job as one sentence ("create a lead with these custom fields in this campaign"); (2) find the endpoint that matches it; (3) check its sample response holds the fields you need and its inputs let you filter to what you want; (4) confirm how it authenticates. For any list call, find its paging inputs (page, limit, cursor or offset) and keep calling until the response says there is no next page; a count lower than the stated total means a page was missed.

Endpoints this pipeline needs (names differ by tool):

| Tool | Calls |
|---|---|
| Prospecting API | company search with filters; people search at those companies by title or function; email find (enrichment) per person |
| Research tool | web search or research per company |
| Email tool | campaign create; lead create (with custom fields); attach or import leads to a campaign; campaign read-back |

## 4. Auth check

One harmless read per tool before any real work: an account, credits or "list campaigns" call. Report what matters (connected, plan, credits left, workspace name) and nothing secret.

| Result | What you say |
|---|---|
| Works | "Connected. Your plan shows enough credits for this run." |
| Rejected | "The key in `<file name>` is rejected. Check it in the tool's API settings." Stop the run for that tool. |
| Two keys, one fails | Say which by position ("the second key in the file"), never by value |

Record each paid tool's credit balance before Step 2 and again at the end; both go in the handover.

## 5. Clarifying questions

When Claude Code asks clarifying questions (which file holds the key, which workspace, which route), answer them rather than letting it guess. When you are the one running, ask them yourself whenever the brief leaves something open.
