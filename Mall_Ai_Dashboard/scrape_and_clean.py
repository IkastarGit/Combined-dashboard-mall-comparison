from scraper import scrape_url
from cleaner import clean_raw_text  # kept for compatibility, not used below
import pandas as pd


def scrape_and_prepare(url: str, source: str = "Official Website"):
    """Scrape `url` and return a pandas DataFrame built DIRECTLY from AI-extracted shops
    (no de-duplication), plus the raw extracted count.

    This bypasses the legacy text cleaner so you get exactly what the AI extracted.

    Returns:
        tuple[pd.DataFrame, int]: (df_with_possible_duplicates, raw_extracted_count)
    """
    if not url:
        raise ValueError("url is required for scraping")

    # Scrape in-memory (do not write files) - reduced initial wait for faster startup
    try:
        shops, labeled_text = scrape_url(url, write_files=False, wait_seconds=1.0)  # Reduced from 3.0 to 1.0
    except Exception as scrape_err:
        raise Exception(f"Failed to scrape URL {url}: {str(scrape_err)}") from scrape_err

    # Raw count before ANY extra processing
    raw_count = len(shops) if shops is not None else 0

    # Build DataFrame directly from AI-extracted shops, preserving duplicates.
    if shops:
        df = pd.DataFrame(shops)
        # Ensure expected columns exist
        for col in ["shop_name", "phone", "floor"]:
            if col not in df.columns:
                df[col] = ""
        df = df[["shop_name", "phone", "floor"]]
    else:
        df = pd.DataFrame(columns=["shop_name", "phone", "floor"])

    # Add source column
    if not df.empty:
        df["source"] = source
    else:
        df = pd.DataFrame(columns=["shop_name", "phone", "floor", "source"])
        df["source"] = None

    return df, raw_count
