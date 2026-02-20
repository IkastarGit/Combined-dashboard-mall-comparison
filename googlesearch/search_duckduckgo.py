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
    Returns list of {title, link, snippet}.
    """
    try:
        from duckduckgo_search import DDGS
        results = []
        
        # Clean query: Remove excessive spaces and special chars that might confuse DDG
        import re
        clean_q = re.sub(r"\s+", " ", query).strip()
        
        # Ensure we don't pass empty query
        if not clean_q: return []

        with DDGS() as ddgs:
            # region='wt-wt' is 'No Region'. For specific local searches, 'in-en' for India might be better, 
            # but 'wt-wt' is generally safest for global consistency.
            ddgs_gen = ddgs.text(clean_q, max_results=max_results, region='wt-wt')
            if not ddgs_gen:
                return []
                
            for r in ddgs_gen:
                link = (r.get("href") or r.get("url") or "").strip()
                # Skip DDG internal links
                if not link or "duckduckgo.com" in link:
                    continue
                
                results.append({
                    "title": (r.get("title") or "").strip(),
                    "link": link,
                    "snippet": (r.get("body") or r.get("snippet") or "").strip(),
                })
        return results
    except Exception as e:
        # Avoid crashing the pipeline if DDG is intermittent
        print(f"[DDG search] Warning: Error searching for '{query}': {e}")
        return []
