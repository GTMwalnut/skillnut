# CRM queries

HubSpot is the tested path (through the HubSpot connector's `query_crm_data` tool). Other CRMs follow the same logic with their own objects; see the table at the end.

## HubSpot

Before the first query in a session: call `tool_guidance` for `query_crm_data`, and confirm the property names with `search_properties` (portals rename and add properties). Replace `<YYYY-MM-DD>` with the window start (default: 180 days before today for the alert, 12 months for the dashboard).

Rules that save time:
- `EMAIL` is queried as engagement data automatically; cross-object `COMPANY.<prop>` works in SELECT, WHERE and GROUP BY.
- Raise `LIMIT` so results aren't cut off, and check the "Showing X of Y" line on every result. A truncated result read as complete is the most common way this run goes wrong.
- Duplicate company records exist (two records for one company, or no-name records). Group by `COMPANY.hs_object_id`, not only by name, and check every record of a company you raise.

### Candidates

People who replied, by company:
```sql
SELECT COMPANY.hs_object_id, COMPANY.name, COMPANY.lifecyclestage, COUNT(*)
FROM CONTACT WHERE hs_sales_email_last_replied >= '<YYYY-MM-DD>'
GROUP BY COMPANY.hs_object_id, COMPANY.name, COMPANY.lifecyclestage
ORDER BY COUNT(*) DESC LIMIT 1000
```

People who filled a form, by company:
```sql
SELECT COMPANY.hs_object_id, COMPANY.name, COMPANY.lifecyclestage, COUNT(*)
FROM CONTACT WHERE recent_conversion_date >= '<YYYY-MM-DD>'
GROUP BY COMPANY.hs_object_id, COMPANY.name, COMPANY.lifecyclestage
ORDER BY COUNT(*) DESC LIMIT 1000
```

Meetings, by company (catches accounts with no replies or forms):
```sql
SELECT COMPANY.hs_object_id, COMPANY.name, COUNT(*) FROM MEETING
WHERE hs_timestamp >= '<YYYY-MM-DD>'
GROUP BY COMPANY.hs_object_id, COMPANY.name ORDER BY COUNT(*) DESC LIMIT 1000
```

Identified website visitors, by company:
```sql
SELECT COMPANY.hs_object_id, COMPANY.name, COUNT(*)
FROM CONTACT WHERE hs_analytics_last_visit_timestamp >= '<YYYY-MM-DD>'
GROUP BY COMPANY.hs_object_id, COMPANY.name ORDER BY COUNT(*) DESC LIMIT 1000
```

LinkedIn replies synced as notes (adjust the tool name to theirs):
```sql
SELECT COMPANY.hs_object_id, COMPANY.name, hs_timestamp, hs_note_body FROM NOTE
WHERE hs_timestamp >= '<YYYY-MM-DD>' AND hs_note_body LIKE '%HeyReach%'
ORDER BY hs_timestamp DESC LIMIT 1000
```

Then drop excluded lifecycle stages, the user's own company and vendors, and merge the lists by company ID.

### Check reply subjects (spot auto-replies)
```sql
SELECT COMPANY.name, hs_email_subject, COUNT(*) FROM EMAIL
WHERE hs_timestamp >= '<YYYY-MM-DD>' AND hs_email_direction = 'INCOMING_EMAIL'
  AND COMPANY.name IN ('<A>','<B>')
GROUP BY COMPANY.name, hs_email_subject
```

### Who engaged and how (names, titles, forms, visits)
```sql
SELECT COMPANY.name, firstname, lastname, jobtitle, recent_conversion_date,
       recent_conversion_event_name, num_conversion_events,
       hs_sales_email_last_replied, hs_analytics_num_visits, hs_analytics_last_visit_timestamp
FROM CONTACT WHERE (recent_conversion_date >= '<YYYY-MM-DD>'
   OR hs_sales_email_last_replied >= '<YYYY-MM-DD>'
   OR hs_analytics_last_visit_timestamp >= '<YYYY-MM-DD>')
  AND COMPANY.name IN ('<A>','<B>')
```

### Conversation check (Test 3)
```sql
SELECT COMPANY.name, hs_timestamp, hs_meeting_title FROM MEETING
WHERE hs_timestamp >= '<YYYY-MM-DD>' AND COMPANY.name IN ('<A>','<B>')

SELECT COMPANY.name, hs_timestamp, hs_call_title, hs_call_body FROM CALL
WHERE COMPANY.name IN ('<A>','<B>')

SELECT COMPANY.name, hs_timestamp, hs_email_subject, hs_email_direction, hubspot_owner_id
FROM EMAIL WHERE hs_timestamp >= '<YYYY-MM-DD>' AND COMPANY.name IN ('<A>','<B>')
ORDER BY hs_timestamp DESC
```
Read the email list per company, newest first: a non-auto `INCOMING_EMAIL` followed by an outgoing email from a rep owner ID in the same thread (same subject, minus `Re:`) is a conversation.

### Deal status (Test 2)
```sql
SELECT COMPANY.name, dealname, pipeline, dealstage, amount, hs_is_closed, createdate, closedate,
       hs_lastmodifieddate, notes_last_updated, hubspot_owner_id
FROM DEAL WHERE COMPANY.name IN ('<A>','<B>')
```
`hs_lastmodifieddate` moves on any edit, so it is not "days in stage". Use the stage-entered date property for the current stage (`hs_v2_date_entered_<stageId>` or the portal's `hs_date_entered_<stageId>`; confirm with `search_properties`). Read the pipelines and stage IDs once in pre-flight and keep them in the run notes.

### Record link
`https://app.hubspot.com/contacts/<portal-id>/record/0-2/<companyId>`. Read the portal ID from the connector in pre-flight; never guess it.

## Other CRMs (same logic, their objects)

| Need | Attio | Salesforce | Pipedrive |
|---|---|---|---|
| Inbound replies | Emails on the company or person record (connected inboxes), direction inbound | `EmailMessage` with `Incoming = true`, or `Task` of type Email | Mail messages linked to the person or org |
| Form fills | Whatever list or attribute the form tool writes to | `CampaignMember` (responded), lead source fields | Leads, web-form fields, or the form tool's notes |
| Meetings and calls | Meeting records, call recordings | `Event`, `Task` (TaskSubtype = Call) | Activities (type meeting / call) with `done` |
| Website visits | Only if a visitor tool writes to the record | Marketing tool fields (Pardot / Account Engagement) | Usually not available |
| Open deal and stage age | Deals list entries, stage attribute and its history | `Opportunity` with `IsClosed = false`, `LastStageChangeDate` | Deals with `status = open`, `stage_change_time` |
| Owner IDs | Workspace members | `User` | Users |

Where the CRM can't answer a check (no visit data, no stage history), say which test is weaker and by how much, and run the rest.
