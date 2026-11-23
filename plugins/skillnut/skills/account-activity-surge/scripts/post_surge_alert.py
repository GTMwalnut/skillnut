#!/usr/bin/env python3
"""Post the weekly surge message to Slack through the bot's incoming webhook, or test the webhook.

Usage:
  python post_surge_alert.py --check                 is the webhook variable set, and is Slack reachable? posts nothing
  python post_surge_alert.py --post msg.txt          post the message in msg.txt (Slack mrkdwn) to the channel

The webhook URL is read from an environment variable (default SLACK_SURGE_WEBHOOK_URL, change it
with --env). The URL is a secret: this script never prints or logs it, and neither should you.

--check sends an empty JSON body. Slack answers 400 (no_text) and posts nothing; any HTTP code
proves the network allowlist works. A proxy 403 or a connection error means it does not.
Exit codes: 0 ok, 2 variable missing, 3 network or Slack error.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def send(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default="SLACK_SURGE_WEBHOOK_URL")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--post", metavar="MSG_FILE")
    args = ap.parse_args()

    url = os.environ.get(args.env, "").strip()
    print("%s: %s" % (args.env, "set" if url else "missing"))
    if not url:
        print("The webhook variable is missing. Add it to the environment (new sessions only pick it up). Nothing was posted.")
        sys.exit(2)
    if not url.startswith("https://hooks.slack.com/"):
        print("The variable is set but does not look like a Slack incoming-webhook URL. Nothing was posted.")
        sys.exit(2)

    try:
        if args.check:
            code, _ = send(url, {})
            print("HTTP %s from Slack with an empty body. Nothing was posted." % code)
            if code == 403:
                print("403 usually means a proxy blocked hooks.slack.com: add it to the allowed domains.")
                sys.exit(3)
            print("hooks.slack.com is reachable.")
            return
        with open(args.post, encoding="utf-8") as f:
            text = f.read().strip()
        if not text:
            print("Message file is empty. Nothing was posted.")
            sys.exit(3)
        code, body = send(url, {"text": text})
        print("HTTP %s: %s" % (code, body.strip()[:80]))
        if code != 200 or body.strip() != "ok":
            print("Post failed. Do not fall back to posting from a person's Slack account.")
            sys.exit(3)
        print("Posted.")
    except (urllib.error.URLError, OSError) as e:
        print("Network error reaching Slack: %s" % type(e).__name__)
        sys.exit(3)


if __name__ == "__main__":
    main()
