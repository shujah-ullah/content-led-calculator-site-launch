#!/usr/bin/env python3
"""Audit a generated static site's content and internal links.

Usage: audit_static_site.py --dist dist --manifest dist/manus-routes.json
Returns non-zero for broken links, orphan routes, stale copy, duplicate/high-similarity bodies,
empty headings, missing H1/main content, or missing generated pages.
"""
from __future__ import annotations
import argparse, json, re, sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

STALE = re.compile(r"\b(?:lorem ipsum|todo|tbd|coming soon|placeholder|first release|initial scaffold|future calculator|currently in development|calculator-ready|module in development)\b", re.I)
PAGE_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.title=""; self.links=[]; self.headings=[]; self.main_text=[]
        self.in_title=False; self.capture=None; self.main_depth=0; self.details=0; self.forms=0
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag == "title": self.in_title=True
        if tag == "a": self.links.append(attrs.get("href", ""))
        if tag in PAGE_TAGS:
            self.headings.append([tag, ""]); self.capture=("heading", len(self.headings)-1)
        if tag == "main": self.main_depth += 1
        if self.main_depth and tag not in {"script", "style"}: self.main_text.append(" ")
        if tag == "details": self.details += 1
        if tag == "form": self.forms += 1
    def handle_endtag(self, tag):
        if tag == "title": self.in_title=False
        if tag == "main" and self.main_depth: self.main_depth -= 1
        if self.capture:
            kind, index = self.capture
            if (kind == "heading" and tag == self.headings[index][0]): self.capture=None
    def handle_data(self, data):
        if self.in_title: self.title += data
        if self.capture and self.capture[0] == "heading": self.headings[self.capture[1]][1] += data.strip()
        if self.main_depth and data.strip(): self.main_text.append(data.strip())

def route_file(dist: Path, route: str) -> Path:
    return dist / "index.html" if route == "/" else dist / route.strip("/") / "index.html"

def route_for(path: str, routes: set[str]):
    if path in routes: return path
    if path.endswith("/index.html"):
        candidate = path[:-10] or "/"
        candidate = candidate if candidate.endswith("/") else candidate + "/"
        return candidate if candidate in routes else None
    return None

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--dist", default="dist"); ap.add_argument("--manifest", default="dist/manus-routes.json"); ap.add_argument("--json", action="store_true"); args=ap.parse_args()
    dist=Path(args.dist); manifest=json.loads(Path(args.manifest).read_text()); routes=[x["path"] for x in manifest["routes"]]; route_set=set(routes)
    assets={"/styles.css", "/favicon.svg", "/social-card.svg", "/manus-routes.json", "/robots.txt", "/sitemap.xml"}
    assets |= {"/"+str(p.relative_to(dist)) for p in dist.rglob("*") if p.is_file()}
    broken=[]; fragments=[]; stale=[]; orphan=[]; rows=[]; bodies={}; incoming={r:0 for r in routes}
    for route in routes:
        path=route_file(dist, route)
        if not path.is_file(): rows.append({"route":route,"missing_file":True}); continue
        raw=path.read_text(); p=Parser(); p.feed(raw); body=" ".join(p.main_text); bodies[route]=set(re.findall(r"[a-z0-9]{3,}", body.lower()))
        if not p.title.strip(): stale.append((route,"missing title"))
        if sum(t == "h1" for t,_ in p.headings) != 1: stale.append((route,"expected exactly one H1"))
        if not any(t == "h2" for t,_ in p.headings): stale.append((route,"missing H2"))
        if len(body) < 500: stale.append((route,"thin raw main content"))
        hits=sorted(set(x.lower() for x in STALE.findall(raw)))
        if hits: stale.append((route, "stale copy: " + ", ".join(hits)))
        for href in p.links:
            if href.startswith("#"):
                if not re.search(rf"(?:id|name)=[\"']{re.escape(href[1:])}[\"']", raw): fragments.append((route, href))
                continue
            if not href or href.startswith(("http:", "https:", "//", "mailto:", "tel:", "javascript:", "data:")): continue
            target=urlsplit(href).path or "/"
            if target in assets: continue
            resolved=route_for(target, route_set)
            if not resolved: broken.append((route, href))
            else: incoming[resolved] += 1
        rows.append({"route":route,"body_chars":len(body),"h1":sum(t == "h1" for t,_ in p.headings),"h2":sum(t == "h2" for t,_ in p.headings),"faq_details":p.details,"forms":p.forms,"links":len(p.links)})
    for route,count in incoming.items():
        if count == 0: orphan.append(route)
    similar=[]; exact=[]
    for i,a in enumerate(routes):
        for b in routes[i+1:]:
            if a not in bodies or b not in bodies: continue
            if bodies[a] == bodies[b]: exact.append([a,b]); continue
            if min(len(bodies[a]),len(bodies[b])) >= 30:
                score=len(bodies[a] & bodies[b])/len(bodies[a] | bodies[b])
                if score >= .82: similar.append([a,b,round(score,3)])
    result={"routes":len(routes),"broken_internal_links":broken,"broken_fragments":fragments,"stale_or_content_issues":stale,"orphan_routes":orphan,"exact_duplicate_body_pairs":exact,"high_similarity_pairs":similar,"route_rows":rows}
    print(json.dumps(result, indent=2) if args.json else f"routes={len(routes)} broken={len(broken)} fragments={len(fragments)} stale={len(stale)} orphan={len(orphan)} exact_duplicates={len(exact)} high_similarity={len(similar)}")
    if broken or fragments or stale or orphan or exact or similar or any(x.get("missing_file") for x in rows): sys.exit(1)

if __name__ == "__main__": main()
