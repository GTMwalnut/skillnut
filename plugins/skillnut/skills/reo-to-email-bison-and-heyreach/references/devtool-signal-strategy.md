# Devtool signal strategy (Mode D detail)

Load this when the user picks Mode D, when a first batch shows the segments are wrong, or when Stage 3 sets the seniority and account-tier gate (section 8). It is the layer above the batch pipeline: which accounts matter, which signals count, who gets which message, and how fast. All numbers here are illustrative.

## 1. The idea in one paragraph

Developers leave public traces before a company buys: a star, a fork, an issue, a pull request, a docs visit, a copied install command. Reo.dev turns many of those into a named person at a named company. The strategy is simple: only reach people who already showed interest, split them into developers and buyers, send each a message that fits their seat, and do it while the signal is fresh. In our runs, outreach sent within about 48 hours of the activity drew the best responses, so the pipeline runs every two to three days.

## 2. Priority groups (account tiers)

| Tier | What it is | How it is gated |
|---|---|---|
| Tier 1 | The named target list (say 1,000 accounts) | Upload as a Reo list. Every signal counts |
| Tier 2 | The expansion list (say the next 2,000) | Upload as a second list. Every signal counts |
| Others | Active accounts on neither list | ICP fit plus a revenue floor (for example over $100M), and the list filter "does not include" both lists |

Things to know:
- **Count unique domains, not rows.** Target files often carry duplicate rows (blank-domain copies, several legal entities of one bank). Quote coverage against the unique count, or every percentage looks worse than it is.
- **Uploading a list reveals history.** Reo has usually been collecting activity on those accounts already. A list that looks "quiet" may simply never have been uploaded. Check presence in Reo before calling an account quiet.
- **Quiet but present accounts** are still reachable through hiring and tech-stack signals (see the agent prompt pack), which need no repo activity.
- **Account geography strict, person geography open.** Gate accounts on the regions you sell to, but leave person location open: a US bank's platform team may sit in London or Toronto. Check consent rules (for example Canada's CASL, GDPR basis) before go-live.

## 3. Segment architecture

Build one segment per tier and signal family:

| Segment | Type | List filter | Activity |
|---|---|---|---|
| Tier 1 GitHub | Advanced | Tier 1 list | Repo type: own OR competitor OR complementary |
| Tier 1 Website | Basic | Tier 1 list | Website |
| Tier 1 Docs | Basic | Tier 1 list | Docs |
| Tier 2 GitHub / Website / Docs | as above | Tier 2 list | as above |
| Others GitHub / Website / Docs | Basic | does not include either list | activity plus ICP fit plus revenue floor |

Rules that bite:
- **Basic segments have no OR.** Advanced segments have filter groups. Put the list in one group (AND) and the three repo types in a second group set to **OR**. The default is AND, which demands activity on all three types and returns almost nobody.
- **Segments, agents and audiences are UI-only.** The API can read them but not create them. Only lists can be created by API. You need the Admin role.
- **Segment type gates the API.** Buyer and developer endpoints refuse account-type segments.
- **Tags are stamped when a segment is built, not kept live.** An account that qualifies later carries no tag. So filtering people on account tags drifts, which is why the batch pipeline runs the account walk.
- **A people segment filtered on account tags returns everyone Reo knows at those accounts**, whether or not they did the activity. Check how many members actually have the activity before trusting a segment's size.
- **"Interacted with repository" has a default window (about 90 days).** Older activity drops out silently.
- **Check repo typing.** In one run "own" matched other organisations' repos until the typing was fixed. Sample a few members of the own-repo segment and confirm the repo names.
- **Retire superset segments.** A "No activity" segment that contains every member of the "GitHub" segment is a duplicate, not a separate campaign.
- **Cap people per account (2 to 4).** The failure mode is switching on too many personas and burning sending capacity on marginal people.

## 4. Typing the repos

The tag drives the message, so get it right.

| Type | What belongs | Message angle |
|---|---|---|
| Own | Your own org's repos | Can name the action (fork, issue, PR) |
| Competitor | Projects doing your product's job | Pitch what they lack, never "replace X" |
| Complementary | Frameworks, SDKs and specs that consume or create demand for what you do | "You build with X; here is the missing piece" |

- A framework that **uses** your category is complementary, not a competitor. A displacement email to its users makes no sense.
- **Rank complementary repos by engagement density (contributors, issues, PRs), not stars.** The repo with the most stars is often where people browse examples; the SDKs are where they build.
- **Don't add** a repo whose stars carry years of history from before your category existed, or one that locks users into a platform that cannot run your product.
- **Park viral but unused repos.** Huge star counts with few contributors and almost no open issues means admired, not used.
- **Watch other channels too.** GitHub surfaces open-source alternatives; community threads (Reddit and similar) surface the commercial tools buyers actually shortlist. Avoid bare acronyms as keywords (they collide with unrelated meanings); prefer phrases people really write, checked against real threads.

## 5. Developers vs buyers (two tracks)

| Track | Who | Message |
|---|---|---|
| Developer | Staff, Principal, Distinguished, Fellow, Architect in a platform, infra, cloud or AI platform team | Technical and install-focused. May name a public action on your own repo |
| Buyer | Director, VP, Head, CTO, Chief AI Officer in engineering, platform, infra or AI | Cost and risk. The signal picks who and when; it rarely appears in the copy |

- **Below-Staff developers are a signal about the account, not a target.** Email their Director instead.
- **Reo's buyer persona is broader than most companies' buyers.** Expect many architects and ICs in a "buyer" segment; filter by title.
- Out for most devtools: interns, students, consultants, product managers, data scientists, DevRel, recruiters, and security or compliance titles when security is not who starts the conversation.

## 6. Lanes: what may be cited

Only a **public action** may be named in a message: a fork, issue, PR, comment, job post or form fill. Stars, website and docs visits pick who and when, but stay out of the copy (this matches the skill's opening-line rules).

| Lane | Who | Channel |
|---|---|---|
| A | Citable action on your own repo | Developer email plus LinkedIn |
| B | Warm but not citable (competitor or complementary repos, website, docs, LinkedIn) | Buyer email and LinkedIn; signal never named |
| C | Everyone else, or the Others tier | Ads audience, not cold outreach |

## 7. Sending pattern

- **Speed:** run the delta every 48 to 72 hours. The simplest working version is one local Claude Code skill run every 48 hours: it scores everyone against the ICP, the buyers stay, students and freelancers drop out, and a person strikes out any odd exceptions by hand before the load. Once the rules settle, the same logic can run in real time as an n8n flow (Mode F, `n8n-realtime-flow.md`).
- **Why LinkedIn.** At enterprises, cold email keeps getting blocked by security gateways. LinkedIn reaches the same person without the gateway. In our runs LinkedIn replied many times better than email for complementary repos; own-repo signals were the ones that worked on email.
- **The opener cites the person's own signal.** Every message opens from what that person did (the repo, the action, roughly when), so no two messages read the same. Lane rules in section 6 still decide which signals may be named.
- **Sequence:** run two LinkedIn campaigns against each other, one **with** a connection request and one **without**, and compare them. Already connected to the sender: skip the sequence; the account owner or AE takes the conversation. No accept after about 7 days: send the InMail.
- **Low-signal people:** point them at the repo or docs, which creates a future signal you can act on.
- **Positive replies** go straight to the AE (for example a Slack alert).
- **Human in the loop:** a person strikes odd exceptions before anything loads (Stage 8).

## 8. The seniority and account-tier gate

Developer signals are plentiful; most of them come from people who will never sign. Before the first batch, agree two gates and write them into the rules file:

| Gate | Default | Why |
|---|---|---|
| Account tier | Only Tier 1 and Tier 2 accounts (the named enterprise lists) go to outreach; Others need ICP fit plus the revenue floor | Keeps sending capacity on the accounts sales actually wants |
| Seniority floor | Mid to senior engineering and tech roles. Who counts as the buyer is the user's call | A reply from a junior developer is an account signal, not a lead |

People under the seniority floor at a gated account are not dropped silently: they go on a per-account "signal" list, and the message goes to the senior contact at that account (section 5).

**The lesson from a wound-down engagement.** In one devtool engagement the bottom-up motion produced steady replies, but most came from junior developers and individual engineers, and each one was passed to the sales team as it arrived. The client sold top down (the CEO or CTO reached out to senior people) and had narrowed its focus to a smaller set of accounts, so those replies were noise to them, and the outbound work was wound down. What to do differently:
- Ask before the first batch: **who on the client's side sells, and to whom?** If executives sell to executives, raise the seniority floor and treat developer activity as the reason to reach the senior person, not as the lead.
- Ask how narrow the account list is, and gate to it. Re-ask whenever the client's focus changes.
- Agree what a "reply worth passing on" is, and batch the hand-offs (a daily or weekly digest) instead of pinging the team for every developer who answers.
- Report replies by seniority and tier, not just in total, so a mismatch shows up in week one, not month three.

## 9. Output of Mode D

Write `_Signal Strategy.md` next to the pull log: tiers and their counts, the segment table, repo typing, the two tracks, the lanes, the sending pattern, the seniority and tier gates, who handles replies, and the per-account cap. Then feed its decisions into the rules file (Stage 3 Batches A, B and D) so batches follow it.
