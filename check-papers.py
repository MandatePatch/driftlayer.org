#!/usr/bin/env python3
"""Fail if a paper in sitemap.xml is missing from the archive index or the feed.

The three lists are independent. papers/index.html is the archive page,
sitemap.xml is what a crawler reads, feed-items.json is what build-feed.py
reads. Nothing else reconciles them. Run this before pushing, the way
check-versions.py runs before a tag.

    python3 check-papers.py

A paper is a sitemap location of the form /papers/<slug>/. The archive index
itself, /papers/, is not a paper. Exit status is 0 when every such slug is
linked from papers/index.html and present in feed-items.json, 1 otherwise.
"""
import json
import pathlib
import re
import sys

here = pathlib.Path(__file__).parent
sitemap = (here / "sitemap.xml").read_text()
index = (here / "papers" / "index.html").read_text()
items = json.loads((here / "feed-items.json").read_text())

slugs = re.findall(r"https://driftlayer\.org/papers/([a-z0-9-]+)/", sitemap)
feed_paths = {it["path"] for it in items}
missing = []
for slug in slugs:
    path = f"papers/{slug}/"
    href = f"/papers/{slug}/"
    if href not in index:
        missing.append(f"{path} not linked from papers/index.html")
    if path not in feed_paths:
        missing.append(f"{path} not in feed-items.json")

if missing:
    print("check-papers: failed", file=sys.stderr)
    for line in missing:
        print(f"  {line}", file=sys.stderr)
    sys.exit(1)
print(f"check-papers: {len(slugs)} papers in sitemap, index, and feed")
