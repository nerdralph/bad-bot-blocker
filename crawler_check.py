#!/usr/bin/env python3
# nerdralph bad bot blocker
# rewrite map program to whitelist good crawlers
import sys
import socket

BOT_SUFFIXES = {
    "google": ".googlebot.com",
    "bingbot": ".search.msn.com",
    "facebook": ".fbsv.net",
    "duck": ".duckduckgo.com",
    "petalbot": ".petalsearch.com",
}

for line in sys.stdin:
    ip, bot = line.strip().split('|', 1)
    suffix = BOT_SUFFIXES[bot.lower()]

    try:
        host = socket.gethostbyaddr(ip)[0]
        ok = host.lower().endswith(suffix)
    except Exception:
        ok = False

    print("1" if ok else "0")
    sys.stdout.flush()
