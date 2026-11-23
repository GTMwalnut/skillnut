#!/usr/bin/env python3
"""Check a surge data file and put it into the dashboard template.

Usage:
  python render_surge_dashboard.py --data surge_accounts_data.json --out surge-dashboard.html
  python render_surge_dashboard.py --data surge_accounts_data.json --check   (validate only)

The template is assets/surge-dashboard.html next to this script's folder. The output is one
self-contained HTML file (no external scripts) that opens in a browser or publishes as an artifact.

Validation fails loudly on anything that would make the page wrong (missing fields, monthly
arrays of the wrong length, by_channel totals that do not match monthly totals by more than the
pre-window spill). It never fills in or estimates a value: blanks stay blank and show as a dash.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "surge-dashboard.html")
PLACEHOLDER = "__SURGE_DATA__"
REQUIRED_TOP = ["generated", "months", "channels", "accounts"]
REQUIRED_ACCOUNT = ["name", "group", "priority", "people", "activities", "latest", "monthly"]


def validate(d):
    errors, warnings = [], []
    for k in REQUIRED_TOP:
        if k not in d:
            errors.append("missing top-level field: %s" % k)
    if errors:
        return errors, warnings
    months, channels = d["months"], d["channels"]
    if len(channels) > 8:
        warnings.append("%d channels; the palette has 8 colours, extra channels reuse colours" % len(channels))
    names = {}
    for i, a in enumerate(d["accounts"]):
        label = a.get("name") or "account #%d" % i
        for k in REQUIRED_ACCOUNT:
            if k not in a:
                errors.append("%s: missing %s" % (label, k))
        names[label] = names.get(label, 0) + 1
        monthly = a.get("monthly") or {}
        for ch, arr in monthly.items():
            if ch not in channels:
                errors.append("%s: monthly has unknown channel '%s'" % (label, ch))
            if len(arr) != len(months):
                errors.append("%s: monthly['%s'] has %d values, expected %d" % (label, ch, len(arr), len(months)))
        bc = a.get("by_channel") or {}
        for ch, n in bc.items():
            if ch not in channels:
                errors.append("%s: by_channel has unknown channel '%s'" % (label, ch))
                continue
            m = sum(monthly.get(ch, []))
            if n < m:
                errors.append("%s: by_channel['%s']=%s is below its monthly total %s" % (label, ch, n, m))
            elif n > m:
                warnings.append("%s: %s has %s events before the first month column (counted in totals only)" % (label, ch, n - m))
        g = str(a.get("group", "")).lower()
        if not g:
            errors.append("%s: empty group" % label)
        for p in a.get("people_list") or []:
            if not p.get("name"):
                errors.append("%s: a people_list entry has no name" % label)
    for n, c in names.items():
        if c > 1:
            warnings.append("'%s' appears %d times (duplicate CRM records? label them apart)" % (n, c))
    return errors, warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--template", default=TEMPLATE)
    args = ap.parse_args()

    with open(args.data, encoding="utf-8") as f:
        d = json.load(f)
    errors, warnings = validate(d)
    acc = d.get("accounts", [])
    nodeal = sum(1 for a in acc if "no" in str(a.get("group", "")).lower())
    print("accounts: %d  (no open deal %d, open deal %d)" % (len(acc), nodeal, len(acc) - nodeal))
    for w in warnings:
        print("warning: " + w)
    for e in errors:
        print("ERROR: " + e)
    if errors:
        sys.exit(1)
    if args.check:
        print("data OK")
        return
    if not args.out:
        sys.exit("--out is required unless --check")
    with open(args.template, encoding="utf-8") as f:
        html = f.read()
    if PLACEHOLDER not in html:
        sys.exit("template has no %s placeholder" % PLACEHOLDER)
    payload = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
    # "<" only occurs inside JSON strings; escaping it keeps </script> and <!-- inert.
    payload = payload.replace("<", "\\u003c")
    html = html.replace(PLACEHOLDER, payload, 1)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote %s (%d KB)" % (args.out, os.path.getsize(args.out) // 1024))


if __name__ == "__main__":
    main()
