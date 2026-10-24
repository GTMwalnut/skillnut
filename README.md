# Skillnut by GTM Walnut

Agent Skills built from real GTM client work. Each one is a guided run: it asks a few questions, shows a plan, and does the work with you. Read-only by default; nothing is sent or written without your yes.

Store: https://skills.gtmwalnut.com

## Skillnut Free (`skillnut-free`)

A guide that points you to the right skill, plus three free skills to try the depth.

| Skill | What it does |
|---|---|
| `skillnut-start` | The front door to Skillnut, the GTM skills by GTM Walnut. |
| `icp-builder` | Build the user's Ideal Customer Profile from a deep context layer, not guesswork. |
| `cold-call-openers` | Open a cold call so the prospect stays on the line. |
| `linkedin-post-generator` | Writes, rewrites and diagnoses LinkedIn posts in three modules run alone or together. |

```
/plugin marketplace add gtmwalnut/skillnut
/plugin install skillnut-free@skillnut
```

## Other ways to install

- Any agent that reads `SKILL.md`: `npx skills add gtmwalnut/skillnut`
- Claude.ai or Claude Desktop: download the zip from the store, then Customize > Skills > Upload a skill.

## Updates

Run `claude plugin update <plugin>@skillnut`. Auto-update is off by default for third-party marketplaces: turn it on under /plugin > Marketplaces.
