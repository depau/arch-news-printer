#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
import requests
import subprocess
import xml.etree.ElementTree as ET

from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

bold = "\u001b[1m"
cyan = "\u001b[36m"
reset = "\u001b[0m"

def prettydate(date: datetime) -> str:
    now = datetime.now(timezone.utc).astimezone()
    dtz = date.astimezone(now.tzinfo)

    hour = timedelta(hours=1)
    day = timedelta(days=1)
    week = timedelta(weeks=1)
    month = timedelta(days=30)
    year = timedelta(days=365)

    delta = now - dtz
    if delta < hour:
        return f"{delta.seconds // (60)}m ago"
    elif delta < day:
        return f"{delta.seconds // (60/60)}h ago"
    elif delta < week:
        return f"{delta.days}d ago"
    elif delta < month:
        return f"{delta.days // 7}w ago"
    elif delta < year:
        return f"{delta.days // 30}mo ago"
    else:
        return f"{delta.days // 365}y ago"


def hyperlink(url: str, text: str) -> str:
    return f'\x1b]8;;{url}\x1b\\{text}\x1b]8;;\x1b\\'


def usage():
    print("Pretty-prints Arch Linux's news RSS feed (with hyperlinks!)")
    print(f"Usage: {sys.argv[0]} [long news] [short news]")


def format_short(item) -> str:
    title = item.findall("title")[0].text
    date = parsedate_to_datetime(item.findall("pubDate")[0].text)
    link = item.findall("link")[0].text
    return f"{bold} • {cyan}{hyperlink(link, title)}{reset} - {prettydate(date)}"


def main(argv=sys.argv):
    limit = -1
    short = 0
    if len(argv) > 1:
        if argv[1] in ("-h", "--help"):
            usage()
            return
        limit = int(argv[1])
    if len(argv) > 2:
        short = int(argv[2])

    req = requests.get("https://www.archlinux.org/feeds/news/", stream=True)

    tree = ET.parse(req.raw)
    root = tree.getroot()
    items = root.findall("channel")[0].findall("item")

    for item in items[:limit]:
        print(format_short(item))
        # Flush stdout to avoid getting out-of-order-lines
        sys.stdout.flush()

        desc = item.findall("description")[0].text
        p = subprocess.Popen(["lynx", "-dump", "-stdin"], stdin=subprocess.PIPE)
        p.communicate(desc.encode())
        p.wait()
        sys.stdout.flush()
        print()

    if limit >= 0:
        short_limit = short if short < 0 else short + limit
        for item in items[limit:short_limit]:
            print(format_short(item))

if __name__ == "__main__":
    main()
