#!/usr/bin/env python3
"""Fail unless the sitemap, the archive index, and the feed list the same papers.

The three lists are independent. papers/index.html is the archive page,
sitemap.xml is what a crawler reads, feed-items.json is what build-feed.py
reads. Nothing else reconciles them. Run this before pushing, the way
check-versions.py runs before a tag.

    python3 check-papers.py

A paper is a slug under /papers/<slug>/. The archive index itself, /papers/,
is not a paper. The check takes the union of the three sources and tests each
slug against the other two, so a paper left out of any one of them fails.
Exit status is 0 when the three sets are equal, 1 otherwise.
"""
import json
import pathlib
import re
import sys

here = pathlib.Path(__file__).parent
sitemap = (here / "sitemap.xml").read_text()
index = (here / "papers" / "index.html").read_text()
items = json.loads((here / "feed-items.json").read_text())

slug = r"[a-z0-9-]+"
in_sitemap = set(re.findall(rf"https://driftlayer\.org/papers/({slug})/", sitemap))
in_index = set(re.findall(rf'href="/papers/({slug})/"', index))
in_feed = set()
for it in items:
    m = re.fullmatch(rf"papers/({slug})/", it["path"])
    if not m:
        print(f"check-papers: feed path is not a paper: {it['path']}", file=sys.stderr)
        sys.exit(1)
    in_feed.add(m.group(1))

sources = {
    "sitemap.xml": in_sitemap,
    "papers/index.html": in_index,
    "feed-items.json": in_feed,
}
missing = []
for slug_ in sorted(set().union(*sources.values())):
    absent = [name for name, found in sources.items() if slug_ not in found]
    if absent:
        missing.append(f"papers/{slug_}/ missing from {', '.join(absent)}")

if missing:
    print("check-papers: failed", file=sys.stderr)
    for line in missing:
        print(f"  {line}", file=sys.stderr)
    sys.exit(1)
print(f"check-papers: {len(in_sitemap)} papers in sitemap, index, and feed")
