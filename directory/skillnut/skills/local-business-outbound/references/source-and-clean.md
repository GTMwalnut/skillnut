# Module 1 - Source and clean

Load this when Module 1 starts. It covers only what the campaign needs. For a full local TAM build (thousands of ambiguous listings to classify by rules and hand reads, owner and manager names, franchise and roll-up traps, national-broker splits), use the tam-list-builder skill on its local track (L1 to L6) and bring its keep list back here at step 3.

## Why the source is Google listings

Local owners are mostly not on LinkedIn, and the B2B databases (which are largely built from LinkedIn) barely cover them. What nearly every local business does keep is a Google listing, and the listing carries the fields this whole play runs on: name, website, category, star rating, review count, address, phone, and sometimes an email. Delivery and booking platforms list many of the same businesses, but the Google listing is the one to rely on.

## Step 1. Pull the listings

Two ways to pull, by the size of the job:

| Way | When | Tools (any one) | How |
|---|---|---|---|
| By state, bulk | A whole state or several, one category | OpenMart (local-business database, download by category and state) | One pull per state per category. Take the state from the address, not the download filter. |
| By city, search | A few cities, or categories a bulk source handles badly | A places search API such as Serper (cheapest per thousand results in a side-by-side test, ahead of an Apify Maps scraper and Clay's own Google lookup), run directly or inside Clay | One query per keyword variant per city ("{category} in {city}, {state}"). Handle pagination until results run out. In Clay, batch 10 to 20 results per call and use conditional runs so a city is not searched twice. |

Rules for either way:
- **Several keyword variants per category.** Owners describe themselves differently ("taqueria", "Mexican restaurant", "Mexican grill"). One keyword misses a slice of the market.
- **Order the cities.** Rank cities by population, or by business density for the category, and pull and send in that order. A research agent (Claygent or similar) can return population per city when the user has no table.
- **Pilot first.** One state or two cities, then show the row count and the cost, then the go for the rest.
- **Log every pull** in `sourcing-log.csv`: source, state or city, keyword, rows returned, date.

### Fields to capture

| Field | Why the campaign needs it |
|---|---|
| Business name | Merge field, dedupe, chain detection |
| Website (and root domain) | Email finding, site scrape, already-contacted match |
| Phone | Call list when there is no email; call-back hand-off |
| Street address, city, state, ZIP | Out-of-area removal, city merge field, city priority |
| Star rating | Segment band, merge field |
| Review count | Review floor, merge field |
| Category tags (primary and all) | Venue-noise rules, short category merge field |
| Email(s) on the listing | First, free source of contact |
| Place ID and listing URL | The dedupe key |
| Service options (dine-in, takeaway, delivery), where the source gives them | Physical-location rule |

## Step 2. Dedupe and scope

1. Dedupe on place ID, then on root domain plus street address, then on normalised name plus street address. Merge keeping the most complete values.
2. Remove out-of-area rows by the address state, never by the search that found them.
3. Apply the target rules the user gave (for example: has a physical location where customers come in; not delivery-only or takeaway-only). Rows that fail go to the duplicates-and-out-of-area file with the rule that failed.

## Step 3. Remove anyone already contacted

Match against the user's sent history from every campaign in their sending tool and CRM, in this order: exact email; root domain; normalised business name plus city. A domain or name match removes the business even when the new email is different, because the owner is the same person.

- Anyone who ever replied (any reply, including neutral) is out for good.
- Anyone sent to without a reply is out until 100 days after their last send. Put the date they become eligible in the removed file.
- Report rows checked, rows hit, and one sample match per match type.

## Step 4. Strip venue noise

Google files many places under the user's category whose buyer is not a local owner. For restaurants the real noise list was: hotels, casinos, golf clubs, sports clubs (and their restaurants). Build the user's list in Stage 2 and apply it in two passes:

1. **Category pass.** Any category tag on the noise list (for example "Hotel", "Casino", "Golf club", "Sports club", "Country club").
2. **Name pass.** A noise word in the business name ("Resort", "Casino", "Golf", "Country Club", "Inn & Suites"). Name matches use word boundaries, so a short word does not match inside a longer one.

Every removed row keeps the word or tag that caught it. A row caught only by the name pass, with a clean category, goes to the owner as "check" rather than straight out.

## Step 5. Move chains to an account-based track

Very large chains are a different sale: the process is long and one cold email rarely earns a meeting, so they get their own account-based plan rather than this campaign.

Detect a chain by any of:
- the same normalised brand name at many place IDs across the pull;
- one root domain shared by many place IDs at different addresses;
- a brand the user names as a chain.

Small groups (a handful of locations under one owner) are not chains; keep them, and treat the shared domain as one business with several locations. The user sets the cut-off in Stage 2. Write `CHAINS - account-based track.csv` with brand, locations count, cities, website, and hand it to the user's account-based work (buying-signals-playbook or outbound-targeting can take it from there).

## Step 6. Shorten the category into a merge value

Raw category tags are long and read badly in an email ("Breakfast, lunch and brunch restaurant"). Build `category-map.csv`: every distinct raw tag, the short value to use in a sentence, and the row count.

How:
- Take the primary category; fall back to the first specific tag.
- Keep the word an owner would use about themselves: "brunch spot", "Korean restaurant", "taqueria", "nail salon".
- Lowercase unless it is a proper noun or a cuisine ("Thai", "Korean").
- It must read naturally in "I was looking for a {category} in {city}". Test every value in that sentence.
- Values that would read oddly or generically ("restaurant", "store", "establishment") get a better tag from the list or are flagged for the owner.

Show every distinct value with its count. Nothing goes into copy until the owner approves the map.

## Reconcile

`KEEP + already contacted + venue noise + chains + duplicates and out of area = listings in`. Print it.
