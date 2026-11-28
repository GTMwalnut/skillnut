# Polish Pass E: messaging spec readiness audit (loaded on demand)

A messaging spec is the document (or prompt) that tells an engine how to write each email: which template fires for which lead, which variables fill which slot, where each variable comes from, and which proof goes where. Agencies ship these to clients and to AI-personalization engines. A spec can read beautifully and still fall back to static copy on every single lead, because a data feed it depends on never arrives.

This pass QAs the spec before a client or an engine sees it. A real spec failed exactly this way: the client's marketing lead read it and said it "isn't ready to run". Every failure below came from that review.

## The five failures to hunt first

| # | Failure | What it looks like | The fix |
|---|---|---|---|
| 1 | Personalized paths depend on a feed that is not arriving | The intent or signal feed the "personalized" branch needs is not connected, so every lead falls back to the static template | Name each feed, confirm it is live with a sample record, or mark the branch "not live yet" and say what share of leads will actually get personalization |
| 2 | A template slot invites fabrication | An approved opener hard-codes a slot like "[city or facility]" or "[publication]" that the data rarely has, which forces the engine to guess, against the spec's own "never fabricate" rule | Make the slot optional with a written rule for what happens when it is empty (drop the clause, or personalize off the research reasoning instead) |
| 3 | Two formats, no selection logic | Two opener shapes are both "approved", but nothing says which one fires for which lead | Add the rule (by signal type, by tier, by persona) or cut one |
| 4 | No subject-line selection logic | A list of subject lines with no rule for which goes with which body | Tie subject to body topic (personalized subject uses the topic keyword; static subject matches the static body's topic), or state it is a rotation |
| 5 | References to assets that do not exist | A proof-point selector points at a file, a table or a section that is not in the handover | Check every referenced file, section and column exists, or remove the reference |

## The eight-step audit

1. **Parse the spec.** List every variable and every template slot, and for each one, its data dependency (which column, which feed, which file).
2. **Check each dependency against the live feed.** Open a real record from each feed. A variable whose feed has no live sample is "unresolved".
3. **Simulate on 20 real leads.** Run the spec by hand on 20 actual rows. For each lead record: which path fired (static or personalized), which variables resolved, any placeholder left in the output, any detail the engine would have to invent. This is the step that finds failure 1, every time.
4. **Flag placeholders that cannot resolve or that would fabricate.** Failure 2.
5. **Check the branching covers every case.** Every lead lands on exactly one path; there is subject-line logic; there is a rule for when a signal is too thin to use. Failures 3 and 4.
6. **Check every referenced file or asset exists.** Failure 5.
7. **Write the ownership table.** What the agency delivers, what runs on the client's side, who approves.

| Piece | Built by | Runs on | Approves |
|---|---|---|---|
| Data feeds (intent, signals, job posts) | | | |
| Normalization (names, companies, titles, topics, source names) | | | |
| The engine or prompt that writes the copy | | | |
| Proof-point file (cleared names and numbers only) | | | |
| Sending tool and merge fields | | | |
| Copy approval before send | | | |

8. **Score readiness and write the fix list.** One line per check: pass, partial or fail. Then the verdict: **Ready**, **Ready with fixes** (list them, each with an owner), or **Not ready** (what blocks it). The fix list goes to the user before the client sees anything.

## Other checks worth running (taken from specs that held up)

- **Word caps per beat.** Opener about 30 words, bridge about 40, proof about 40, the whole email under 150, LinkedIn 60 to 70. A spec with no caps produces clunky paragraphs.
- **Proof only from a cleared file.** Customer names and numbers come from one cleared proof-points file, never from the engine's general knowledge. If an industry has no cleared customer, the rule falls back to a cleared marquee name. (The Proof Points by Industry skill builds that file.)
- **Account-level copy plus a merge token.** One email per company, with first name left as a merge field for the sending tool.
- **Normalization rules exist** for first name, company name, job title (three words or fewer, in the case a sentence needs), topic keyword (no technical codes in a subject line, three words or fewer) and source name. A raw domain or a long legal name inside a sentence is the commonest leak: known publications get their short form, anything long or unknown falls back to a generic phrase by source type ("a recent filing", "an industry article").
- **Honest fallback for uncitable signals.** If a source cannot be cited honestly, the opener is built from the research reasoning, with no invented article.
- **CTAs in priority order,** and the casual ones the client dislikes listed as banned.

## Model report (illustrative)

> Spec audit done. 14 variables, 3 data feeds, 2 templates. I ran it by hand on 20 of your real leads: 0 of 20 got the personalized path, because the intent feed it needs has no records yet, so everyone fell back to static. The approved opener has a "[facility]" slot that 17 of the 20 leads can't fill. There are two opener formats and no rule for choosing, no subject-line logic, and the proof selector points at a section that isn't in the handover. Verdict: Not ready. Five fixes, each with an owner, are below. The good news: the static path is clean and could ship this week on its own.
