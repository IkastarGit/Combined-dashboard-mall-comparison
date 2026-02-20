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
        # The library renamed internal classes; DDGS is the standard entry point.
        # We suppress warnings about the rename and handle empty results.
        with DDGS() as ddgs:
            # Clean query and add region hint
            import re
            clean_q = re.sub(r"\s+", " ", query).strip()
            ddgs_gen = ddgs.text(clean_q, max_results=max_results, region='wt-wt')
            if not ddgs_gen:
                return []
                
            for r in ddgs_gen:
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
        print(f"[DDG search] Error searching for '{query}': {e}")
        return []
