#!/usr/bin/env python3
# nerdralph bad bot blocker
# rewrite map program to whitelist good crawlers
import sys
import socket

# Named bots: verified via reverse+forward DNS against known suffix
BOT_SUFFIXES = {
    "googlebot": ".googlebot.com",
    "bingbot": ".search.msn.com",
    "externalhit_ua": ".fbsv.net",
    "duckduckbot": ".duckduckgo.com",
}


def dns_verified(ip, bot):
    try:
        host = socket.gethostbyaddr(ip)[0]
        return host.lower().endswith(BOT_SUFFIXES[bot]) and ip in socket.gethostbyname_ex(host)[2]
    except Exception:
        return False


for line in sys.stdin:
    ip, bot = line.rstrip("\n").split(",", 1)
    ok = dns_verified(ip, bot.lower())
    print("1" if ok else "0", flush=True)
