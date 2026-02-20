"""
chrome_helper.py – Shared Chrome/Selenium setup for all scrapers.

Usage:
    from chrome_helper import make_chrome_driver

    driver = make_chrome_driver()
    # ... do scraping ...
    driver.quit()
"""
import os
import shutil
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def _find_chrome_binary() -> Optional[str]:
    """Return path to Chrome/Chromium binary, or None if not found."""
    candidates = [
        os.environ.get("CHROME_BIN", ""),          # Set by Dockerfile: /usr/bin/chromium
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
    ]
    for path in candidates:
        if path and os.path.isfile(path):
            return path
    return shutil.which("chromium") or shutil.which("google-chrome")


def _find_chromedriver() -> Optional[str]:
    """Return path to chromedriver binary, or None (selenium-manager will handle it)."""
    candidates = [
        os.environ.get("CHROMEDRIVER_PATH", ""),   # Set by Dockerfile: /usr/bin/chromedriver
        "/usr/bin/chromedriver",
        "/usr/local/bin/chromedriver",
    ]
    for path in candidates:
        if path and os.path.isfile(path):
            return path
    return shutil.which("chromedriver")


def make_chrome_options(
    headless: bool = True,
    user_agent: Optional[str] = None,
    enable_network_logs: bool = False,
) -> Options:
    """
    Build Chrome/Chromium options that work in Docker/Railway containers and locally.
    """
    opts = Options()

    if enable_network_logs:
        opts.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    # --- Binary location ---
    chrome_bin = _find_chrome_binary()
    if chrome_bin:
        opts.binary_location = chrome_bin

    # --- Mandatory flags for any containerised environment ---
    opts.add_argument("--no-sandbox")               # Required: no kernel namespaces
    opts.add_argument("--disable-dev-shm-usage")    # Required: /dev/shm is tiny in containers
    opts.add_argument("--disable-setuid-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-software-rasterizer")

    # --- Headless (new flag is more stealthy and stable) ---
    if headless:
        opts.add_argument("--headless=new")

    # --- Writable user-data directory ---
    # In Railway, we prefer a persistent volume if available (usually /data)
    # However, if multiple Chrome instances share the same user-data-dir, they will crash.
    # We use a subfolder per process/thread if many are running.
    import uuid
    instance_id = str(uuid.uuid4())[:8]
    
    default_user_data = f"/tmp/chrome-user-data-{instance_id}"
    if os.path.exists("/data") and os.access("/data", os.W_OK):
        # Even with persistent /data, we use a unique subfolder to avoid lock errors
        # if multiple scrapers run at the exact same time.
        default_user_data = f"/data/chrome-user-data-{instance_id}"
        
    chrome_user_data = os.environ.get("CHROME_USER_DATA_DIR", default_user_data)
    os.makedirs(chrome_user_data, exist_ok=True)
    opts.add_argument(f"--user-data-dir={chrome_user_data}")

    # --- General stability / resource flags ---
    opts.add_argument("--window-size=1280,720")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-notifications")
    opts.add_argument("--disable-background-networking")
    opts.add_argument("--disable-default-apps")
    opts.add_argument("--disable-sync")
    opts.add_argument("--disable-translate")
    opts.add_argument("--no-first-run")
    opts.add_argument("--no-default-browser-check")
    opts.add_argument("--mute-audio")
    opts.add_argument("--metrics-recording-only")
    opts.add_argument("--password-store=basic")
    opts.add_argument("--use-mock-keychain")

    if user_agent:
        opts.add_argument(f"--user-agent={user_agent}")

    return opts


def make_chrome_driver(
    headless: bool = True,
    user_agent: Optional[str] = None,
    enable_network_logs: bool = False,
) -> webdriver.Chrome:
    """
    Create a Chrome/Chromium WebDriver that works in Docker/Railway and locally.

    Prefers the system-installed chromedriver (guaranteed version-match when
    chromium + chromium-driver are installed from the same apt repo).
    Falls back to selenium-manager auto-download for local development.
    """
    opts = make_chrome_options(
        headless=headless,
        user_agent=user_agent,
        enable_network_logs=enable_network_logs,
    )

    chromedriver_path = _find_chromedriver()
    if chromedriver_path:
        service = Service(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=opts)
    else:
        # Local dev fallback: selenium-manager downloads matching chromedriver
        driver = webdriver.Chrome(options=opts)

    # --- Apply Stealth Settings ---
    try:
        from selenium_stealth import stealth
        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        print("[INFO] Applied selenium-stealth settings")
    except ImportError:
        # If selenium-stealth is not installed, continue without it
        pass

    driver.set_page_load_timeout(30)
    driver.implicitly_wait(5)

    return driver
