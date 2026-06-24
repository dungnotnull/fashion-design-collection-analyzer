# -*- coding: utf-8 -*-
"""
knowledge_updater.py — Production-grade SECOND-KNOWLEDGE-BRAIN crawler for
fashion-design-collection-analyzer.

Fetches authoritative fashion-domain sources, extracts structured metadata,
scores entries by recency + relevance, deduplicates by URL/title hash, and
appends dated findings to SECOND-KNOWLEDGE-BRAIN.md.

Primary fetchers (no API key required):
  - Crossref API for Journal of Fashion Marketing and Management
  - arXiv API for quantitative fashion / textile research
  - RSS/Atom feeds for Business of Fashion, Pantone, WGSN blog, Vogue Runway
  - DuckDuckGo Lite HTML results for broad trend queries
  - crawl4ai fallback for pages where RSS is unavailable

Usage:
    python tools/knowledge_updater.py --dry-run
    python tools/knowledge_updater.py --since 2024-01-01 --limit 50
    python tools/knowledge_updater.py --config tools/knowledge_sources.json
"""

import argparse
import datetime
import hashlib
import json
import logging
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Set

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
BRAIN_PATH = PROJECT_ROOT / "SECOND-KNOWLEDGE-BRAIN.md"
DEFAULT_CONFIG_PATH = HERE / "knowledge_sources.json"

LOGGER = logging.getLogger("knowledge_updater")

DOMAIN_KEYWORDS = [
    "fashion", "trend forecast", "color trend", "seasonal palette", "Pantone",
    "WGSN", "sustainable textile", "merchandising", "line plan", "SKU",
    "collection cohesion", "commercial viability", "brand fit", "silhouette",
    "price architecture", "target customer"
]


@dataclass
class KnowledgeEntry:
    """Normalized entry ready for scoring and append."""
    title: str
    authors: str = ""
    year: int = 0
    venue: str = ""
    url: str = ""
    abstract: str = ""
    source: str = ""
    query: str = ""
    fetched_at: str = field(default_factory=lambda: datetime.date.today().isoformat())

    def text_for_scoring(self) -> str:
        return f"{self.title} {self.authors} {self.venue} {self.abstract}".lower()

    def hash_key(self) -> str:
        target = (self.url or "").strip().lower() or self.title.strip().lower()
        return hashlib.sha256(target.encode("utf-8")).hexdigest()[:16]


def _today() -> datetime.date:
    return datetime.date.today()


def _http_get(url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> bytes:
    """Stdlib synchronous HTTP GET with retries and polite delays."""
    default_headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; fashion-design-collection-analyzer/1.0; "
            "+https://github.com/fashion-design-collection-analyzer)"
        ),
        "Accept": "application/json, application/rss+xml, application/xml, text/xml, text/html",
    }
    if headers:
        default_headers.update(headers)
    req = urllib.request.Request(url, headers=default_headers)
    last_error = None
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 503, 502):
                last_error = e
                wait = 2 ** attempt
                LOGGER.warning("HTTP %s for %s; sleeping %ss (attempt %s)", e.code, url, wait, attempt)
                time.sleep(wait)
                continue
            LOGGER.warning("HTTP error %s for %s: %s", e.code, url, e)
            return b""
        except Exception as e:
            last_error = e
            LOGGER.warning("Fetch error for %s: %s", url, e)
            time.sleep(2 ** attempt)
    LOGGER.error("Giving up on %s after retries: %s", url, last_error)
    return b""


def _safe_year(raw: Optional[str]) -> int:
    if not raw:
        return 0
    digits = re.findall(r"\b(19\d{2}|20\d{2})\b", raw)
    if digits:
        return int(digits[0])
    return 0


def _clean_text(text: Optional[str]) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _score_entry(entry: KnowledgeEntry) -> float:
    """Recency + keyword relevance score in [0, 1]."""
    now_year = _today().year
    year = entry.year or now_year
    recency = max(0.0, 1.0 - (now_year - year) / 10.0)
    text = entry.text_for_scoring()
    hits = sum(1 for k in DOMAIN_KEYWORDS if k.lower() in text)
    relevance = min(1.0, hits / max(1, len(DOMAIN_KEYWORDS)))
    return round(0.5 * recency + 0.5 * relevance, 3)


def load_existing_hashes(path: Path) -> Set[str]:
    """Load DOI/URL hashes already present in the knowledge base."""
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r"<!--hash:([0-9a-f]{16})-->", text))

# ---------------------------------------------------------------------------
# Fetchers
# ---------------------------------------------------------------------------

def fetch_crossref(source: Dict, since: Optional[str] = None, limit: int = 20) -> List[KnowledgeEntry]:
    """Fetch works from Crossref for a configured ISSN or query."""
    entries: List[KnowledgeEntry] = []
    query = source.get("query", "fashion merchandising")
    issn = source.get("issn", "")
    filter_parts = ["type:journal-article"]
    if since:
        filter_parts.append(f"from-pub-date:{since}")
    if issn:
        filter_parts.append(f"issn:{issn}")
    url = (
        "https://api.crossref.org/works?"
        f"query={urllib.parse.quote(query)}"
        f"&filter={','.join(filter_parts)}"
        f"&rows={limit}"
        f"&sort=published"
        f"&order=desc"
    )
    data = _http_get(url, headers={"Accept": "application/json"})
    if not data:
        return entries
    try:
        payload = json.loads(data.decode("utf-8"))
    except Exception as e:
        LOGGER.warning("Failed to parse Crossref response: %s", e)
        return entries
    for item in payload.get("message", {}).get("items", []):
        authors = ", ".join(
            f"{a.get('given', '')} {a.get('family', '')}".strip()
            for a in item.get("author", [])[:3]
        )
        year = (
            _safe_year(item.get("published-print", {}).get("date-parts", [[""]])[0][0])
            or _safe_year(item.get("published-online", {}).get("date-parts", [[""]])[0][0])
            or _safe_year(item.get("published", {}).get("date-parts", [[""]])[0][0])
        )
        entries.append(KnowledgeEntry(
            title=_clean_text(item.get("title", [""])[0]),
            authors=authors,
            year=year,
            venue=_clean_text(item.get("container-title", [""])[0]) or source.get("name", "Crossref"),
            url=item.get("URL", ""),
            abstract=_clean_text(item.get("abstract", ""))[:600],
            source=source.get("name", "Crossref"),
            query=query,
        ))
    return entries


def fetch_arxiv(source: Dict, since: Optional[str] = None, limit: int = 20) -> List[KnowledgeEntry]:
    """Fetch arXiv results for fashion/textile/merchandising topics."""
    entries: List[KnowledgeEntry] = []
    query = source.get("query", "fashion OR textile OR merchandising")
    url = (
        "http://export.arxiv.org/api/query?"
        f"search_query=all:{urllib.parse.quote(query)}"
        f"&start=0&max_results={limit}"
        f"&sortBy=submittedDate&sortOrder=descending"
    )
    data = _http_get(url)
    if not data:
        return entries
    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        LOGGER.warning("Failed to parse arXiv feed: %s", e)
        return entries
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.findall("atom:entry", ns):
        title = _clean_text(entry.findtext("atom:title", "", ns))
        if title.lower().startswith("arxiv:"):
            continue
        authors = ", ".join(
            a.findtext("atom:name", "", ns) for a in entry.findall("atom:author", ns)
        )[:200]
        published = entry.findtext("atom:published", "", ns)
        url_node = entry.find("atom:id", ns)
        url = url_node.text if url_node is not None else ""
        summary = _clean_text(entry.findtext("atom:summary", "", ns))[:600]
        entries.append(KnowledgeEntry(
            title=title,
            authors=authors,
            year=_safe_year(published),
            venue=source.get("name", "arXiv"),
            url=url,
            abstract=summary,
            source=source.get("name", "arXiv"),
            query=query,
        ))
    return entries

def fetch_rss(source: Dict, since: Optional[str] = None, limit: int = 20) -> List[KnowledgeEntry]:
    """Fetch and parse an RSS or Atom feed."""
    entries: List[KnowledgeEntry] = []
    feed_url = source.get("url", "")
    if not feed_url:
        return entries
    data = _http_get(feed_url)
    if not data:
        return entries
    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        LOGGER.warning("Failed to parse RSS feed %s: %s", feed_url, e)
        return entries
    channel = root.find("channel")
    is_atom = channel is None
    ns_atom = {"atom": "http://www.w3.org/2005/Atom"}
    items = []
    if channel is not None:
        items = channel.findall("item")[:limit]
    else:
        items = root.findall("atom:entry", ns_atom)[:limit]
    for item in items:
        if is_atom:
            title = _clean_text(item.findtext("atom:title", "", ns_atom))
            link_node = item.find("atom:link", ns_atom)
            link = link_node.attrib.get("href", "") if link_node is not None else ""
            published = item.findtext("atom:published", "", ns_atom) or item.findtext("atom:updated", "", ns_atom)
            summary = _clean_text(
                item.findtext("atom:summary", "", ns_atom) or item.findtext("atom:content", "", ns_atom)
            )[:600]
        else:
            title = _clean_text(item.findtext("title", "", None))
            link = _clean_text(item.findtext("link", "", None))
            if not link:
                link_el = item.find("link")
                if link_el is not None:
                    link = link_el.text or link_el.attrib.get("href", "")
            published = item.findtext("pubDate", "", None) or item.findtext("date", "", None)
            summary = _clean_text(item.findtext("description", "", None))[:600]
        entries.append(KnowledgeEntry(
            title=title,
            authors=source.get("name", "RSS"),
            year=_safe_year(published),
            venue=source.get("name", "RSS"),
            url=link,
            abstract=summary,
            source=source.get("name", "RSS"),
            query=source.get("query", ""),
        ))
    return entries


def fetch_duckduckgo(source: Dict, since: Optional[str] = None, limit: int = 10) -> List[KnowledgeEntry]:
    """
    Fetch DuckDuckGo Lite HTML results for a query.
    Used only as a broad signal; parses title and snippet, not the target page.
    """
    entries: List[KnowledgeEntry] = []
    query = source.get("query", "")
    if not query:
        return entries
    url = f"https://lite.duckduckgo.com/lite/?q={urllib.parse.quote(query)}"
    data = _http_get(url)
    if not data:
        return entries
    html = data.decode("utf-8", errors="replace")
    rows = re.findall(
        r'<tr[^>]*>.*?<a[^>]+class="[^"]*result-link[^"]*"[^>]+href="([^"]+)"[^>]*>(.*?)</a>.*?'
        r'<td[^>]+class="result-snippet[^"]*"[^>]*>(.*?)</td>.*?</tr>',
        html, re.DOTALL | re.IGNORECASE
    )
    for link, title, snippet in rows[:limit]:
        link = urllib.parse.unquote(link)
        title = _clean_text(title)
        snippet = _clean_text(snippet)
        if link.startswith("//"):
            link = "https:" + link
        if not link.startswith("http"):
            continue
        entries.append(KnowledgeEntry(
            title=title,
            authors="",
            year=_today().year,
            venue="DuckDuckGo",
            url=link,
            abstract=snippet,
            source=source.get("name", "DuckDuckGo"),
            query=query,
        ))
    return entries

async def fetch_crawl4ai(source: Dict, since: Optional[str] = None, limit: int = 10) -> List[KnowledgeEntry]:
    """Optional crawl4ai-based fetcher for pages without RSS or API."""
    entries: List[KnowledgeEntry] = []
    try:
        from crawl4ai import AsyncWebCrawler
    except ImportError:
        LOGGER.info("crawl4ai not installed; skipping crawl4ai fetcher.")
        return entries
    urls_to_crawl = source.get("urls", [])
    async with AsyncWebCrawler(verbose=False) as crawler:
        for target_url in urls_to_crawl[:limit]:
            try:
                res = await crawler.arun(url=target_url)
                markdown = getattr(res, "markdown", "") or ""
                title = _clean_text(markdown.splitlines()[0]) if markdown else ""
                if not title:
                    title = Path(urllib.parse.urlparse(target_url).path).name
                entries.append(KnowledgeEntry(
                    title=title,
                    authors=source.get("name", "crawl4ai"),
                    year=_today().year,
                    venue=source.get("name", "crawl4ai"),
                    url=getattr(res, "url", target_url),
                    abstract=_clean_text(markdown)[:600],
                    source=source.get("name", "crawl4ai"),
                    query=source.get("query", ""),
                ))
            except Exception as e:
                LOGGER.warning("crawl4ai failed for %s: %s", target_url, e)
    return entries


# ---------------------------------------------------------------------------
# Config and orchestration
# ---------------------------------------------------------------------------

DEFAULT_SOURCES = [
    {
        "id": "crossref-jfmm",
        "name": "Journal of Fashion Marketing and Management (Crossref)",
        "type": "crossref",
        "query": "fashion marketing management merchandising sustainability",
        "issn": "1361-2026"
    },
    {
        "id": "crossref-fashion",
        "name": "Fashion Research (Crossref)",
        "type": "crossref",
        "query": "fashion design collection trend forecast textile"
    },
    {
        "id": "arxiv-fashion",
        "name": "arXiv Fashion/Textile Research",
        "type": "arxiv",
        "query": "fashion OR textile OR merchandising OR sustainability"
    },
    {
        "id": "rss-bof",
        "name": "Business of Fashion",
        "type": "rss",
        "query": "fashion business analysis",
        "url": "https://www.businessoffashion.com/rss/"
    },
    {
        "id": "rss-vogue",
        "name": "Vogue Runway",
        "type": "rss",
        "query": "runway collection review",
        "url": "https://www.vogue.com/rss/"
    },
    {
        "id": "rss-pantone",
        "name": "Pantone Color Institute",
        "type": "rss",
        "query": "Pantone color of the year seasonal palette",
        "url": "https://www.pantone.com/articles/rss"
    },
    {
        "id": "ddg-trends",
        "name": "DuckDuckGo Trend Search",
        "type": "duckduckgo",
        "query": "fashion trend forecast season 2026"
    },
    {
        "id": "ddg-sustainable-textile",
        "name": "DuckDuckGo Sustainable Textile Search",
        "type": "duckduckgo",
        "query": "sustainable textile innovation 2026"
    },
    {
        "id": "ddg-merchandising",
        "name": "DuckDuckGo Merchandising Search",
        "type": "duckduckgo",
        "query": "merchandising line plan strategy fashion"
    }
]


FETCHERS = {
    "crossref": fetch_crossref,
    "arxiv": fetch_arxiv,
    "rss": fetch_rss,
    "duckduckgo": fetch_duckduckgo,
}


def load_config(path: Optional[Path] = None) -> List[Dict]:
    """Load source configuration. Supports either a top-level list or {"sources": [...]}."""
    raw = None
    if path and path.exists():
        with open(path, "r", encoding="utf-8-sig") as f:
            raw = json.load(f)
    elif DEFAULT_CONFIG_PATH.exists():
        with open(DEFAULT_CONFIG_PATH, "r", encoding="utf-8-sig") as f:
            raw = json.load(f)
    if raw is None:
        return DEFAULT_SOURCES
    if isinstance(raw, dict) and "sources" in raw:
        return raw["sources"]
    if isinstance(raw, list):
        return raw
    LOGGER.error("Invalid config format; expected list or dict with sources key")
    return DEFAULT_SOURCES
def run_fetchers(sources: List[Dict], since: Optional[str], limit: int) -> List[KnowledgeEntry]:
    """Run all enabled fetchers synchronously."""
    all_entries: List[KnowledgeEntry] = []
    for source in sources:
        fetcher_name = source.get("type", "")
        fetcher = FETCHERS.get(fetcher_name)
        if not fetcher:
            LOGGER.warning("Unknown fetcher type: %s", fetcher_name)
            continue
        LOGGER.info("Fetching %s via %s", source.get("name"), fetcher_name)
        try:
            if fetcher_name == "crawl4ai":
                import asyncio
                entries = asyncio.run(fetch_crawl4ai(source, since=since, limit=limit))
            else:
                entries = fetcher(source, since=since, limit=limit)
            LOGGER.info("  -> %s entries from %s", len(entries), source.get("name"))
            all_entries.extend(entries)
        except Exception as e:
            LOGGER.warning("Fetcher %s failed: %s", source.get("name"), e)
    return all_entries


def deduplicate(entries: List[KnowledgeEntry], existing_hashes: Set[str]) -> List[KnowledgeEntry]:
    """Remove duplicates by hash and near-duplicate titles."""
    seen_hashes: Set[str] = set(existing_hashes)
    seen_titles: Set[str] = set()
    unique: List[KnowledgeEntry] = []
    for entry in entries:
        h = entry.hash_key()
        title_norm = re.sub(r"[^a-z0-9]", "", entry.title.lower())
        if h in seen_hashes:
            continue
        if title_norm and title_norm in seen_titles:
            continue
        seen_hashes.add(h)
        seen_titles.add(title_norm)
        unique.append(entry)
    return unique


def append_entries(entries: List[KnowledgeEntry], path: Path) -> int:
    """Append scored, deduplicated entries to SECOND-KNOWLEDGE-BRAIN.md."""
    existing = load_existing_hashes(path)
    unique = deduplicate(entries, existing)
    if not unique:
        LOGGER.info("No new entries to append.")
        return 0
    lines = []
    today = _today().isoformat()
    for entry in sorted(unique, key=_score_entry, reverse=True):
        score = _score_entry(entry)
        lines.append(
            f"- {today} | score={score} | **{entry.title}** | {entry.authors} "
            f"| {entry.year or ''} | {entry.venue} | {entry.url} "
            f"<!--hash:{entry.hash_key()}-->"
        )
    header = f"\n### Crawl {today} (+{len(unique)})\n"
    if not path.exists():
        path.write_text("# SECOND-KNOWLEDGE-BRAIN.md\n", encoding="utf-8")
    with open(path, "a", encoding="utf-8") as f:
        f.write(header + "\n".join(lines) + "\n")
    LOGGER.info("Appended %s new entries to %s", len(unique), path)
    return len(unique)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Update SECOND-KNOWLEDGE-BRAIN.md with fresh fashion-domain knowledge."
    )
    ap.add_argument("--config", type=Path, help="Path to JSON source config")
    ap.add_argument("--since", type=str, help="Only fetch items published on or after YYYY-MM-DD")
    ap.add_argument("--limit", type=int, default=20, help="Max items per source")
    ap.add_argument("--dry-run", action="store_true", help="Crawl and score but do not append")
    ap.add_argument("--brain", type=Path, default=BRAIN_PATH, help="Target knowledge base path")
    ap.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    args = ap.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    sources = load_config(args.config)
    if not sources:
        LOGGER.error("No sources configured.")
        return 1

    LOGGER.info("Starting knowledge update with %s sources", len(sources))
    entries = run_fetchers(sources, since=args.since, limit=args.limit)

    scored = [{**asdict(e), "score": _score_entry(e)} for e in entries]
    scored.sort(key=lambda x: x["score"], reverse=True)

    if args.dry_run:
        print(json.dumps(scored[:args.limit], indent=2, ensure_ascii=False))
        LOGGER.info("Dry run complete; %s entries would be considered (not appended).", len(entries))
        return 0

    added = append_entries(entries, args.brain)
    LOGGER.info("Knowledge update complete. Appended %s new entries.", added)
    return 0


if __name__ == "__main__":
    sys.exit(main())


