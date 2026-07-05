#!/usr/bin/env python3
"""Refresh userAgent.txt with the current latest Firefox release version."""

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

VERSIONS_URL = "https://product-details.mozilla.org/1.0/firefox_versions.json"
TARGET_FILE = Path(__file__).resolve().parent.parent / "userAgent.txt"
REQUEST_TIMEOUT = 15


def fetch_latest_major_version() -> str:
    request = urllib.request.Request(
        VERSIONS_URL,
        headers={"User-Agent": "0x12net-metadata-update-script"},
    )
    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
        data = json.load(response)

    latest = data["LATEST_FIREFOX_VERSION"]
    major = latest.split(".")[0]
    if not major.isdigit():
        raise ValueError(f"Unexpected version format: {latest!r}")
    return major


def build_user_agent(current: str, major: str) -> str:
    new_version = f"{major}.0"
    updated = re.sub(r"rv:\d+(?:\.\d+)*", f"rv:{new_version}", current)
    updated = re.sub(r"Firefox/\d+(?:\.\d+)*", f"Firefox/{new_version}", updated)
    return updated


def main() -> int:
    try:
        major = fetch_latest_major_version()
    except (urllib.error.URLError, KeyError, ValueError, json.JSONDecodeError) as exc:
        print(f"Failed to fetch latest Firefox version: {exc}", file=sys.stderr)
        return 1

    current = TARGET_FILE.read_text(encoding="utf-8")
    updated = build_user_agent(current, major)

    if updated == current:
        print(f"No change needed, already tracking Firefox {major}.0")
        return 0

    TARGET_FILE.write_text(updated, encoding="utf-8")
    print(f"Updated {TARGET_FILE.name} to Firefox {major}.0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
