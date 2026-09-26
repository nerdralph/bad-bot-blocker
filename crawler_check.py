#!/usr/bin/env python3
# nerdralph bad bot blocker
# rewrite map program to whitelist good crawlers
import sys
import socket
import time

# Named bots: verified via reverse+forward DNS against known suffix
BOT_SUFFIXES = {
    "googlebot": ".googlebot.com",
    "bingbot": ".search.msn.com",
    "externalhit_ua": ".fbsv.net",
}

# Generic bot-labeled UAs (not in BOT_SUFFIXES): rate-limited instead of
# DNS-verified. Minimum seconds between accepted hits from the same IP.
MIN_INTERVAL = 300

# In-process state; lost on Apache reload (prg: runs as one long-lived
# process, so this is acceptable and avoids sqlite/file overhead).
last_seen = {}


def dns_verified(ip, bot):
    try:
        host = socket.gethostbyaddr(ip)[0]
        return host.lower().endswith(BOT_SUFFIXES[bot]) and ip in socket.gethostbyname_ex(host)[2]
    except Exception:
        return False


def rate_ok(ip):
    now = time.monotonic()
    prev = last_seen.get(ip)
    if prev is None:
        # bots often fetch /robots.txt, then /; allow that second hit
        # immediately by starting the window one interval in the past
        last_seen[ip] = now - MIN_INTERVAL
        return True
    if now - prev >= MIN_INTERVAL:
        last_seen[ip] = now
        return True
    return False

for line in sys.stdin:
    ip, bot = line.rstrip("\n").split(",", 1)
    bot = bot.lower()
    ok = dns_verified(ip, bot) if bot in BOT_SUFFIXES else rate_ok(ip)
    print("1" if ok else "0", flush=True)
