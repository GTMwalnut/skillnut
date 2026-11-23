#!/usr/bin/env python3
"""Turn a cleaned activity log plus an account sheet into the surge dashboard JSON.

Usage:
  python build_surge_data.py --activities activities.csv --accounts accounts.csv \
      --as-of 2026-10-21 --out surge_accounts_data.json [--meta meta.json] [--all]

activities.csv (one row per touch FROM the prospect, already cleaned: no auto-replies, no
negative replies, no outbound sequence emails):
  company_id, company, person, title, date (YYYY-MM-DD), channel, type, detail
  person may be blank for company-level touches (an identified company website visit).

accounts.csv (one row per prospect account; customers, partners, vendors, closed-won and your
own company already removed):
  company_id, company, segment, pipeline_status (open_deal | closed_lost | never),
  deal, stage, amount, deal_owner, company_owner, early_stage (yes/no), crm_url, suggested_action
  Only company_id, company and pipeline_status are required; blank cells stay blank.

meta.json (optional) is merged into the top level: title, labels, channels (order),
channel_definitions, definitions, caveats, source.

Rules (defaults, each a flag):
  surge     = channels >= 3, OR channels >= 2 with people >= 3   (--all keeps every account)
  priority  1 High   no open deal: (channels >= 4 or people >= 4) and active in last 90 days
                     open deal:    channels >= 5, or early-stage deal with people >= 4
            2 Medium otherwise, if active in the last 180 days
            3 Watch  otherwise
Nothing is estimated. Counts come only from the rows given.
"""
import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import date, timedelta

DEFAULT_CHANNELS = ["Email reply", "LinkedIn reply", "Meeting / demo", "Survey", "Website",
                    "Conference", "Content / webinar"]


def d(s):
    s = (s or "").strip()[:10]
    return date.fromisoformat(s) if s else None


def minus_months(x, n):
    y, m = x.year, x.month - n
    while m <= 0:
        m += 12
        y -= 1
    last = (date(y + (m // 12), m % 12 + 1, 1) - timedelta(days=1)).day
    return date(y, m, min(x.day, last))


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return [{(k or "").strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]


def num(s):
    try:
        return float(str(s).replace(",", "").replace("$", "")) if str(s).strip() else None
    except ValueError:
        return None


def default_action(group, pstatus, early, people, heating):
    if group == "open":
        if early:
            return "Early-stage deal with wide engagement: move it to the next stage and multi-thread the engaged people."
        return "Deal is open: brief the deal owner on who else at the account is engaging."
    if pstatus == "closed_lost":
        return "Previous deal closed-lost and the account is engaging again: assign an owner and reopen with the engaged people."
    if heating or people >= 3:
        return "No deal and rising engagement: assign an owner and reach out to the engaged people this week."
    return "Watch: engaging but not yet deep. Keep in nurture and re-check next run."


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--activities", required=True)
    ap.add_argument("--accounts", required=True)
    ap.add_argument("--as-of", required=True, help="YYYY-MM-DD, the day the data was pulled")
    ap.add_argument("--months", type=int, default=12)
    ap.add_argument("--out", required=True)
    ap.add_argument("--meta")
    ap.add_argument("--all", action="store_true", help="keep accounts that miss the surge rule")
    ap.add_argument("--min-channels", type=int, default=3)
    ap.add_argument("--alt-channels", type=int, default=2)
    ap.add_argument("--alt-people", type=int, default=3)
    ap.add_argument("--max-people", type=int, default=8)
    ap.add_argument("--max-events", type=int, default=12)
    args = ap.parse_args()

    meta = {}
    if args.meta:
        with open(args.meta, encoding="utf-8") as f:
            meta = json.load(f)
    channels = meta.get("channels") or DEFAULT_CHANNELS
    as_of = d(args.as_of)
    start = minus_months(as_of, args.months)
    first_month = date(as_of.year, as_of.month, 1)
    for _ in range(args.months - 1):
        first_month = minus_months(first_month, 1)
    months, cur = [], first_month
    for _ in range(args.months):
        months.append("%04d-%02d" % (cur.year, cur.month))
        cur = date(cur.year + (cur.month // 12), cur.month % 12 + 1, 1)

    accounts = {r["company_id"]: r for r in read_csv(args.accounts) if r.get("company_id")}
    acts = read_csv(args.activities)

    seen, dropped = set(), defaultdict(int)
    by_acc = defaultdict(list)
    for r in acts:
        cid, dt, ch = r.get("company_id"), d(r.get("date")), r.get("channel")
        if cid not in accounts:
            dropped["company not in accounts sheet (excluded or unknown)"] += 1
            continue
        if ch not in channels:
            dropped["channel not in channel list: %s" % ch] += 1
            continue
        if not dt or dt < start or dt > as_of:
            dropped["outside the window"] += 1
            continue
        key = (cid, (r.get("person") or "").lower(), dt, ch)
        if key in seen:
            dropped["duplicate (same person, day and channel)"] += 1
            continue
        seen.add(key)
        r["_d"] = dt
        by_acc[cid].append(r)

    out_accounts, missed = [], 0
    for cid, rows in by_acc.items():
        a = accounts[cid]
        by_channel = defaultdict(int)
        monthly = {c: [0] * len(months) for c in channels}
        people = {}
        for r in rows:
            by_channel[r["channel"]] += 1
            mk = "%04d-%02d" % (r["_d"].year, r["_d"].month)
            if mk in months:
                monthly[r["channel"]][months.index(mk)] += 1
            p = r.get("person")
            if p:
                e = people.setdefault(p.lower(), {"name": p, "title": "", "channels": [], "n": 0, "last": r["_d"]})
                e["n"] += 1
                e["last"] = max(e["last"], r["_d"])
                if r.get("title") and not e["title"]:
                    e["title"] = r["title"]
                if r["channel"] not in e["channels"]:
                    e["channels"].append(r["channel"])
        monthly = {c: v for c, v in monthly.items() if any(v)}
        ch12 = len(by_channel)
        recent6 = minus_months(as_of, 6)
        ch6 = len({r["channel"] for r in rows if r["_d"] > recent6})
        npeople = len(people)
        if not args.all and not (ch12 >= args.min_channels or (ch12 >= args.alt_channels and npeople >= args.alt_people)):
            missed += 1
            continue
        latest = max(r["_d"] for r in rows)
        first = min(r["_d"] for r in rows)
        active90 = (as_of - latest).days <= 90
        active180 = (as_of - latest).days <= 180
        ps = (a.get("pipeline_status") or "").lower()
        group = "open" if ps in ("open", "open_deal", "open deal") else "none"
        early = (a.get("early_stage") or "").lower() in ("yes", "y", "true", "1")
        if group == "none":
            p1 = (ch12 >= 4 or npeople >= 4) and active90
        else:
            p1 = ch12 >= 5 or (early and npeople >= 4)
        priority = "1 - High" if p1 else ("2 - Medium" if active180 else "3 - Watch")
        # heating: last 3 months is the busiest 3-month block
        tot = [sum(v[i] for v in monthly.values()) for i in range(len(months))]
        blocks = [sum(tot[max(0, e - 3):e]) for e in range(len(months), 0, -3)]
        heating = blocks[0] > 0 and all(blocks[0] > b for b in blocks[1:])
        pstatus = {"open": "Open deal"}.get(group) or (
            "No open deal - previous deal closed-lost" if "lost" in ps else "No open deal - never had a deal")
        plist = sorted(people.values(), key=lambda e: (-e["n"], -e["last"].toordinal()))[: args.max_people]
        events = sorted(rows, key=lambda r: r["_d"], reverse=True)[: args.max_events]
        out_accounts.append({
            "name": a.get("company") or rows[0].get("company") or "(no name)",
            "group": "Open deal" if group == "open" else "No open deal",
            "segment": a.get("segment") or None,
            "priority": priority,
            "pipeline_status": pstatus,
            "deal": a.get("deal") or None,
            "stage": a.get("stage") or None,
            "amount": num(a.get("amount")),
            "deal_owner": a.get("deal_owner") or None,
            "company_owner": a.get("company_owner") or None,
            "channels_12m": ch12,
            "channels_6m": ch6,
            "people": npeople,
            "activities": len(rows),
            "first": first.isoformat(),
            "latest": latest.isoformat(),
            "by_channel": {c: by_channel[c] for c in channels if by_channel.get(c)},
            "monthly": monthly,
            "people_list": [{"name": e["name"], "title": e["title"] or None, "channels": e["channels"]} for e in plist],
            "events": [{"date": r["_d"].isoformat(), "channel": r["channel"], "type": r.get("type") or r["channel"],
                        "person": r.get("person") or None, "detail": r.get("detail") or None} for r in events],
            "suggested_action": a.get("suggested_action") or default_action(group, ps, early, npeople, heating),
            "crm_url": a.get("crm_url") or None,
        })

    out = {"generated": as_of.isoformat(), "window": "%s to %s" % (start.isoformat(), as_of.isoformat()),
           "months": months, "channels": channels}
    for k in ("title", "labels", "channel_definitions", "definitions", "caveats", "source"):
        if k in meta:
            out[k] = meta[k]
    out["accounts"] = sorted(out_accounts, key=lambda x: (x["priority"], -x["channels_12m"], -x["people"], -x["activities"]))
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    n = len(out_accounts)
    nd = sum(1 for x in out_accounts if x["group"] == "No open deal")
    print("activity rows in: %d, kept: %d" % (len(acts), sum(len(v) for v in by_acc.values())))
    for k, v in sorted(dropped.items()):
        print("  dropped %d: %s" % (v, k))
    print("accounts with activity: %d; surge accounts: %d (no open deal %d, open deal %d); below the surge rule: %d"
          % (len(by_acc), n, nd, n - nd, missed))
    if len(by_acc) != n + missed:
        sys.exit("reconcile failed")
    print("reconciled: %d = %d surge + %d below rule" % (len(by_acc), n, missed))


if __name__ == "__main__":
    main()
