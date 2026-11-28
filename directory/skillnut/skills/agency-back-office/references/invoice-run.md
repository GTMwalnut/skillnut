# Invoice run: method and layout

Module 6. The client list (names, amounts, due-day rules) is supplied at run time and never stored in this skill. This file describes the method, not the roster.

## Run steps

1. **Already raised this month? Skip.** For each client on the list, look in the invoice folder for an invoice for that client dated in the current calendar month. If one exists, skip it. Re-running in the same week must never produce duplicates.

2. **Due-date gate.** Raise the invoice only if today is on or after that client's due day this month.
   - Fixed day of month (for example the 22nd).
   - Last calendar day of the month: compute it (28, 29, 30 or 31; February in a leap year has 29).
   - Report clients not yet due with their due date.

3. **Bill-to: never invented.**
   - Default: copy the bill-to block word for word from that client's most recent invoice.
   - No previous invoice, but the client bills through the same parent company as an existing client: reuse that client's bill-to (same legal party) and flag it in the report.
   - No source: **stop and ask**. Do not guess an address.

4. **Invoice number: one global sequence, not per client.** Scan every invoice file in the folder (all clients, all years still in the folder, plus the archive folders), find the highest number in the user's scheme (for example `INV-0047`), assign highest + 1. Several invoices in one run: increment in creation order. Never reuse, never skip. If two files carry the same number already, stop and report it.

5. **Template: replicate, don't redesign.** Open the client's most recent invoice and copy its format exactly. Change only: invoice number, invoice date, service period, amount (if different). Brand-new client: copy the most recent invoice of the client that shares its bill-to party.

6. **Save** with the user's naming rule. Two rules seen in practice; use whichever the folder already follows:
   - `<Client> - <Your name> Invoice <Mon'YY>.pdf`
   - `<Client>_<InvoiceNumber>_<YYYY-MM-DD>.pdf`
   Do not send or email anything.

7. **Report.** For each invoice raised: client, number, file path, bill-to block, amount, and which fields were copied word for word versus inferred. Then clients skipped (already raised, with their number) and clients not yet due (with the date). Raised + skipped + not yet due = clients on the list.

## Hard rules

- Never reuse or skip an invoice number.
- Never invent an address. If a lookup fails, stop and ask.
- Re-running in the same month changes nothing for clients already invoiced.
- Payment details (bank, multi-currency account, tax registration number) come from the last invoice or a config file the user names. They are never hardcoded into a generator script, and never shown in full in chat.

## The layout (fixed per user; this is the common one)

```
INVOICE
BILL TO          [client legal name, address: copied word for word]
RECIPIENT        [contact person / accounts email, if the client wants one]
INVOICE DETAILS  Invoice Number: INV-XXXX    Invoice Date: DD/MM/YYYY
SERVICES
  Item # | Description                                              | Amount (USD)
  1      | Monthly Retainer - [Service name]                        | X,XXX.00
         | [Start date] to [end date]  e.g. 20th Sep'26 to 19th Oct'26 |
  Total                                                             | X,XXX.00
PAYMENT INFORMATION
  Option A: [online multi-currency account: link or details]
  Option B: Bank transfer
BANK DETAILS     [account name, bank, account number, routing/IFSC/SWIFT, tax registration number]
```

## Line-item variants

| Variant | Description line |
|---|---|
| Monthly retainer | `Monthly Retainer - [Service] / [start] to [end]` |
| Two periods on one invoice | one line per period, each with its own dates |
| Reimbursement | `Reimbursement - [what, e.g. inbox provider inboxes] / [period]`, with the receipt attached |
| One-time project fee | `[Project] - one-time fee, per Service Provider Agreement dated [date]` |
| Per-meeting performance fee | `Qualified meetings above [N]: [count] x US$[Y]`, with the meeting list attached |
| Commission earned | a table: referred person or company, start date, deal value, commission %, commission; then the total |

## Due-date arithmetic (copy into the generator)

```python
import calendar, datetime as dt
def due_day(rule, today):
    if rule == "last":
        return calendar.monthrange(today.year, today.month)[1]
    return int(rule)            # fixed day of month
def is_due(rule, today=None):
    today = today or dt.date.today()
    return today.day >= min(due_day(rule, today), calendar.monthrange(today.year, today.month)[1])
```
