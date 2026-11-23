# Modules 3 and 4 - Segment, personalise, write and load

Load this when Module 3 or 4 starts. Input: the email files from Module 2 (valid, and valid-risky if the user chose to send it).

## Module 3 - Segment and personalise

### Segments: rating band crossed with a review floor

| Segment | Rule (defaults; the user can change them) | Goes to |
|---|---|---|
| A | Rating 4.0 and above, review count at or above the floor | Campaign, copy A |
| B | Rating below 4.0, review count at or above the floor | Campaign, copy B |
| Held | Review count below the floor (default 100), or no rating | `HELD - below review floor.csv`, not this campaign |

Why: a business with many reviews is real, open and busy; the rating tells you what it is proud of or worried about, so the two bands get different emails. The floor applies to both bands.

- Valid-risky rows keep their segment but stay in their own file per segment (`A - valid-risky.csv`).
- Rows with no rating or review count go to Held with the reason.

### City priority

Order rows inside each segment by city population (or business density for the category), largest first. The first sends go to the biggest markets; smaller cities follow as the campaign proves out. Keep a `city_rank` column.

### Merge fields

| Field | Source | Rule |
|---|---|---|
| `{{business_name}}` | Listing name | Clean for mail merge (drop legal suffixes, location tags, a leading "The"; the Clean module in campaign-send-checklist has the full rules); never a chain name |
| `{{category}}` | Approved `category-map.csv` | Short value only |
| `{{rating}}` | Star rating | One decimal, as Google shows it ("4.7") |
| `{{review_count}}` | Review count | As a plain number; optionally rounded down ("over 300") for large counts |
| `{{city}}` | Address city | As written on the listing |

Test: fill the first line for five rows from different segments and cities and show them. Any odd line means a merge value to fix, not a template to blame.

## Module 4 - Write and load

### The shape of each email

1. **A first line from their listing.** The model line: *"I was looking for a {{category}} in {{city}} and found {{business_name}}, {{rating}} stars from {{review_count}} reviews."* Swap the next sentence for the user's own line or question.
2. **A short pitch.** What the company does for owners like them, in a sentence or two, and two or three customer logos or names the owner may recognise.
3. **One low-friction ask.** Book a call, or *"Send me your number and I'll give you a call back."* Owners often prefer a call to a calendar link. A lead magnet (a short guide, a free check) is an option to test as a second ask, not the default.

Segment A and B differ in the line after the opener:
- A (4.0 and up): build on what is working ("people clearly love the place; here is how owners like you turn that into ...").
- B (below 4.0): a respectful, helpful angle on the gap, never a dig at the rating.

Keep it short and plain. For subject lines, follow-up steps and polish, use the copywriting-messaging skill. Spintax on greetings and a few phrases helps deliverability (see Module 5).

### Sequence (a starting shape that fits the sending rules in Module 5)

| Step | Day | Content |
|---|---|---|
| 1 | 1 | The email above |
| 2 | about 3 to 4 | A one-line bump with the call-back ask |
| 3 | about 7 to 8 | A different angle or proof point |
| 4 | about 12 to 15 | A short close-the-loop |

### Load plan

- One lead list per segment (and per valid-risky file), so results read by segment.
- Map merge columns to the sending tool's custom variables; check every variable used in the copy exists on every row (an empty `{{rating}}` sends a broken sentence).
- Write `load-plan.md`: campaign name per segment, file, variable map, mailboxes, schedule, daily cap, pilot size.
- **Stop for the go.** Create campaigns and upload only after the user names the action. Pilot batch first. For API loading into Email Bison or another tool, the email-and-linkedin-sequencer-lead-upload skill has the method; for a last pass on the list before upload, campaign-send-checklist.
