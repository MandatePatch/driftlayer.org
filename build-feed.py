#!/usr/bin/env python3
"""Build site/feed.xml from site/feed-items.json.

Adding a paper is one object at the top of feed-items.json, then rerun this.
No dependencies outside the standard library.

Dates: an entry's date is when the item became AVAILABLE. Atom <published>
    and <updated> are availability, not the version date, which is what the
    ratified date rule assigns to citation_publication_date and DC.date. Where a
    paper's version date differs from its availability date, put it in
    "version_date" and it rides on the category label.

    Times: the papers carry dates, not timestamps, so every entry is emitted at
T00:00:00Z. That is date granularity made explicit, not a measured time.
"""
import json, pathlib, sys
from xml.sax.saxutils import escape, quoteattr

SITE = "https://driftlayer.org"
TITLE = "The Drift Layer"
SUBTITLE = "A series on the life of a payment mandate."
AUTHOR = "Matthew T. Kirby"
EMAIL = "matthew.kirby@driftlayer.org"

here = pathlib.Path(__file__).parent
items = json.loads((here / "feed-items.json").read_text())
items.sort(key=lambda i: i["date"], reverse=True)

def ts(d): return f"{d}T00:00:00Z"

out = ['<?xml version="1.0" encoding="utf-8"?>',
       '<feed xmlns="http://www.w3.org/2005/Atom">',
       f'  <title>{escape(TITLE)}</title>',
       f'  <subtitle>{escape(SUBTITLE)}</subtitle>',
       f'  <id>{SITE}/</id>',
       f'  <link href="{SITE}/" rel="alternate" type="text/html"/>',
       f'  <link href="{SITE}/feed.xml" rel="self" type="application/atom+xml"/>',
       f'  <updated>{ts(items[0]["date"])}</updated>',
       '  <author>',
       f'    <name>{escape(AUTHOR)}</name>',
       f'    <email>{EMAIL}</email>',
       '  </author>',
       '  <rights>CC BY 4.0</rights>']

for it in items:
    url = f'{SITE}/{it["path"]}'
    out += ['  <entry>',
            f'    <title>{escape(it["title"])}</title>',
            f'    <id>{url}</id>',
            f'    <link href="{url}" rel="alternate" type="text/html"/>',
            f'    <updated>{ts(it["date"])}</updated>',
            f'    <published>{ts(it["date"])}</published>',
            f'    <category term={quoteattr(it["kind"] + (", " + it["version_date"] if it.get("version_date") else ""))}/>',
            f'    <summary type="text">{escape(it["summary"])}</summary>',
            '  </entry>']

out.append('</feed>')
(here / "feed.xml").write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"feed.xml written — {len(items)} entries, newest {items[0]['date']}")
