# Spend filing: method, folders, naming, gotchas

Module 7. Scope is **spend only**: money the business paid out (software, hardware, services, travel). Invoices the business raises to its own clients are a different folder and are never touched here.

## 1. Folder structure (adapt to the user's; never restructure theirs)

| Category folder | Sub-folders | What goes here |
|---|---|---|
| Software, Websites and Domains | monthly `Mon'YY` (e.g. `Jan'26`) | SaaS subscriptions, domain renewals |
| Office Expenses | monthly `Mon'YY` | stationery, accountant or tax-filing service fees, small office items |
| Hardware and Accessories | monthly `Mon'YY` | chairs, monitors, keyboards, desk hardware |
| Food and Travel | monthly `Mon'YY` | business meals, flights, hotels (minus the user's standing exclusions) |
| Training and Learning | flat | courses, books, bootcamps |
| Phone bills | flat | mobile and internet bills |

If the user's folder names are misspelled or unusual, keep them exactly. Create new `Mon'YY` sub-folders as needed.

## 2. Naming rule

`Vendor Type Mon'YY.pdf`, for example `Acme Invoice Jan'26.pdf`, `Acme Receipt Jan'26.pdf`.
- Always month and year.
- If a vendor sends both an invoice and a receipt as separate PDFs, keep both; `Invoice` vs `Receipt` in the name.
- One-off or annual: add a qualifier, `Acme Annual Invoice Apr'26.pdf`.
- Books: `Books Mon'YY.pdf` (combined) or by title.

## 3. Which month a receipt belongs to

**By billing or service period, not the date the email arrived.**
- Invoice dated 2 Jan for service 2 Jan to 2 Feb: `Jan'26`.
- Invoice dated 6 Mar for service 6 Mar to 6 Apr: `Mar'26`.
- A period that straddles two months (for example 27 Mar to 27 Apr): file by the issue-date month. Pick this rule once and follow your own earlier filings.
- Annual upgrades: the month the upgrade happened.

## 4. Vendor catalogue (build it on the first run, reuse after)

| Vendor | Product | Typical amount | Cadence and day | Invoice number pattern | Separate receipt PDF? | Sender address |
|---|---|---|---|---|---|---|

The catalogue makes the next run fast: the email search query is built from the sender column, and the number pattern tells an invoice from a receipt.

## 5. Things that aren't software

| Source | Folder |
|---|---|
| Marketplace order: chairs, monitors, desks | Hardware and Accessories |
| Marketplace order: pens, hooks, stationery | Office Expenses |
| Marketplace order: books | Training and Learning |
| Marketplace order: personal items | **Skip** and tell the user |
| Accountant or tax-filing service fees | Office Expenses |
| Standing exclusions the user sets (for example local cab rides) | **Exclude** |
| Phone and internet bills | Phone bills |

## 6. Run steps

**Phase 1 - Audit.** List every category folder; the newest file per category marks the gap. Ask the six questions:
1. What date range? (Default: from the newest filed receipt.)
2. Any new vendors since last time?
3. Any recent marketplace orders that are business expenses?
4. Any one-offs this period: tax-filing service fees, annual upgrades, domain renewals?
5. Include food, travel and phone bills this round, or software only?
6. Anything personal that came to the work inbox to skip?

**Phase 2 - Search.** Search email for invoices since the gap date. Build the plan table: vendor, email date, service period, target folder, target file name. **Show the full plan and get a yes before touching any file.**

**Phase 3 - Download (the bottleneck).** Many email connectors can read messages but not download attachments. Then write this Apps Script to a `.txt` file (not chat, which corrupts quotes) with the query filled from the vendor catalogue:

```javascript
function saveInvoicesToDrive() {
  var q = "after:YYYY/M/D has:attachment (from:billing@vendor-a.example OR from:invoices@vendor-b.example OR (from:accountant@example.com subject:invoice))";
  var folder = DriveApp.createFolder("Spend-Invoices-" + new Date().getTime());
  var threads = GmailApp.search(q);
  var count = 0;
  for (var i = 0; i < threads.length; i++) {
    var msgs = threads[i].getMessages();
    for (var j = 0; j < msgs.length; j++) {
      var atts = msgs[j].getAttachments();
      for (var k = 0; k < atts.length; k++) {
        if (atts[k].getContentType() === "application/pdf") {
          folder.createFile(atts[k].copyBlob().setName(atts[k].getName()));
          count++;
        }
      }
    }
  }
  Logger.log("Saved " + count + " PDFs to folder: " + folder.getName());
  Logger.log("URL: " + folder.getUrl());
}
```

Give these steps word for word:
1. Open script.google.com, New project.
2. Select all, delete the default code, paste the script from the `.txt` file.
3. Save.
4. Click Run, then authorise (Advanced, Go to project, Allow).
5. Check the execution log for the folder name.
6. Open Drive, find the folder, right-click, Download (you get a zip).
7. Unzip into your Downloads folder.

**Phase 4 - What the script can't catch.**
- Receipts that arrive as a "view receipt" link with no attachment (payment-processor hosted): give the user the links from the email bodies to download by hand.
- Marketplace tax invoices: not in email; give the user the exact order numbers to download from their orders page.
- One-offs the user pays outside email: they drop the PDFs in Downloads.

**Phase 5 - File.**
1. Read each PDF to confirm vendor, invoice number and service period.
2. Create missing month folders.
3. Rename and move to the right folder with the naming rule.
4. Rename older files that break the rule as you pass them.
5. Delete duplicates from Downloads.
6. Report every new file by folder, and every skipped item with its reason. Filed + skipped = found.

## 7. Gotchas

- **Quote corruption:** scripts go to a `.txt` file, never pasted from chat.
- **Duplicate Drive folders:** each script run makes a new timestamped folder; check the timestamp before downloading.
- **Invoice vs receipt:** some vendors send both in the same email series with different number patterns; don't file a receipt as the invoice (keep both).
- **Signed vs unsigned copies:** some vendors send a signed invoice with a suffix in the file name; prefer the signed one.
- **Periods that straddle two months:** issue-date month, matching earlier filings.
- **Payment-processor senders:** receipts often come from the processor's address rather than the vendor's; include those senders in the query.
- **Old files without a month in the name:** rename as you touch them.
