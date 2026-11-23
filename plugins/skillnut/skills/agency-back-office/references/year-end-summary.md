# Year-end summary: method

Module 8. Built for a business that bills clients in a foreign currency and closes a financial year that may not be the calendar year (for example April to March).

## Steps

1. **Collect.** Every invoice file (PDF and Word) in the invoice folder and any archive folders whose invoice date falls in the financial year.
2. **Extract** per invoice: client, invoice number, invoice date, service period, amount, currency. Use pdfplumber for PDFs and python-docx for Word. Where a field can't be read, list the file for the user rather than guessing.
3. **Assign a month** by service period (a retainer for 20 Sep to 19 Oct is September's income), unless the accountant prefers invoice date; say which rule was used in the file.
4. **Convert currency** with the agreed source (the bank's rate on the day the money arrived, from the bank's inward remittance advice, or a published monthly reference rate). Put the rate and its source on every row.
5. **Build the table** (CSV or Excel):

| Month | Client | Amount (USD) | Rate | Amount (home currency) |
|---|---|---|---|---|
| Apr '25 | Client A | 3,000 | | |
| Apr '25 | **Month total** | | | |
| ... | | | | |
| Mar '26 | Client A (expected) | 3,000 | | |
| **Total** | | | | |

   - Monthly subtotals and a year total.
   - An "(expected)" row for any invoice due in the year but not yet raised, so the total isn't understated; the user decides whether it stays.

6. **Check the sequence.** List every invoice number in order; report gaps (a missing number), duplicates (the same number twice), and numbers out of date order. A cancelled invoice needs a note or a cancelled copy on file.
7. **Check coverage.** For each client active in the year, list months with no invoice between their first and last invoice. Ask the user: paused, free month, or missing?
8. **Separate costs.** Contractor invoices received (inward supplies) and filed spend are listed in their own tab, not mixed into income.
9. **Archive.** At year close, move the year's invoices into `FY YYYY-YY (Mon YYYY - Mon YYYY)`. Do it only after the user approves the summary.
10. **Cover note to the accountant**, drafted for the user to send:
   - the period, number of invoices, clients and currencies, and the total;
   - the exchange-rate source used;
   - gaps and coverage questions, with the user's answers;
   - the user's open questions (for example advance tax or indirect tax returns).
