"""Configuration for the retail store discovery pipeline."""

import os

from dotenv import load_dotenv
load_dotenv()  # Load .env file if present

# --- Chrome / Selenium ---
# Google detects headless Chrome and often withholds AI Overview content (the main data source).
# Set False for reliable results; True only works when Google doesn't block headless.
CHROME_HEADLESS = False
CHROME_WINDOW_SIZE = "1920,1080"
CHROME_PAGE_LOAD_TIMEOUT = 30  # Increased for slow pages (e.g. Instagram)
CHROME_IMPLICIT_WAIT = 5

# --- Google Search ---
GOOGLE_SEARCH_URL = "https://www.google.com/search"
MAX_RESULTS_PER_QUERY = 20
SCROLL_PAUSE_SECONDS = 0.8  # After page load; kept low but enough for DOM to settle

# --- Scraping delays (reduced for speed; increase if data is missed) ---
SEARCH_CONSENT_SLEEP = 0.5       # After clicking Accept cookies
AI_OVERVIEW_INITIAL_WAIT = 3.0   # AI Overview loads async; 3s usually enough
AI_OVERVIEW_WAIT_AFTER_EXPAND = 1.2  # After "Show more" / "Dive deeper"
AI_OVERVIEW_SCROLL_SLEEP = 0.2   # After scroll to top for lazy load
AI_OVERVIEW_CLICK_SLEEP = 0.2    # Before/after expand button click
OFFICIAL_SITE_LOAD_SLEEP = 0.7   # After loading official mall site via Selenium
SELENIUM_FALLBACK_SLEEP = 1.2    # When requests fails and Selenium fetches page

# --- AI API (store-opening analysis) ---
# Use OpenAI if OPENAI_API_KEY is set; otherwise fall back to Gemini
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o-mini"  # Good balance of cost and quality; or use "gpt-4o" for best results
# Gemini (fallback when OpenAI key not set)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyA1g244g9ErmSpDSUgdhnkmCgxkVb09zek")
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_MAX_TOKENS = 2048

# --- Text extraction ---
REQUEST_TIMEOUT = 15
MAX_TEXT_CHUNK_FOR_AI = 12000  # chars per page sent to Gemini (to stay under context)

# --- Output ---
EXTRACTED_OUTPUT_DIR = "extracted_output"
STRUCTURED_OUTPUT_DIR = "structured_output"
