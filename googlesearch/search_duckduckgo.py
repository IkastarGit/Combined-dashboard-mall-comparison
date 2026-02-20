"""
search_duckduckgo.py – Browser-free web search using the duckduckgo-search library.

Drop-in replacement for Selenium-based Google search. Returns the same shape:
  [{"title": str, "link": str, "snippet": str}, ...]

This works in Railway / Docker without any browser installation.
"""

from typing import List


def search_duckduckgo(query: str, max_results: int = 15) -> List[dict]:
    """
    Search DuckDuckGo using the duckduckgo-search library (pure HTTP, no browser).
    Returns list of {title, link, snippet} — same shape as selenium_search.search_google().
    """
    try:
        from duckduckgo_search import DDGS
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                link = (r.get("href") or r.get("url") or "").strip()
                if not link or "duckduckgo.com" in link:
                    continue
                results.append({
                    "title": (r.get("title") or "").strip(),
                    "link": link,
                    "snippet": (r.get("body") or "").strip(),
                })
        return results
    except Exception as e:
        print(f"[DDG search] Error: {e}")
        return []
