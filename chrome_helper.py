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
        os.environ.get("CHROME_BIN", ""),
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
    ]
    for path in candidates:
        if path and os.path.isfile(path):
            return path
    # fallback: search PATH
    return shutil.which("google-chrome") or shutil.which("chromium")


def _find_chromedriver() -> Optional[str]:
    """Return path to chromedriver binary, or None (selenium-manager will handle it)."""
    candidates = [
        os.environ.get("CHROMEDRIVER_PATH", ""),
        "/usr/bin/chromedriver",
        "/usr/local/bin/chromedriver",
    ]
    for path in candidates:
        if path and os.path.isfile(path):
            return path
    return shutil.which("chromedriver")


def make_chrome_options(headless: bool = True, user_agent: Optional[str] = None) -> Options:
    """
    Build Chrome options that work in both Docker/Railway containers and local Windows/Mac.
    """
    opts = Options()

    # --- Binary location (critical in containers) ---
    chrome_bin = _find_chrome_binary()
    if chrome_bin:
        opts.binary_location = chrome_bin

    # --- Container-essential flags ---
    opts.add_argument("--no-sandbox")                   # Required: no kernel namespaces in containers
    opts.add_argument("--disable-dev-shm-usage")        # Required: /dev/shm too small in containers
    opts.add_argument("--disable-setuid-sandbox")       # Required: no setuid support
    opts.add_argument("--disable-gpu")                   # No GPU in containers
    opts.add_argument("--disable-software-rasterizer")  # Avoid SwiftShader errors

    # --- CRITICAL: Give Chrome a writable temp directory ---
    # Without this Chrome tries ~/.config/google-chrome which may be read-only
    chrome_user_data = os.environ.get("CHROME_USER_DATA_DIR", "/tmp/chrome-user-data")
    os.makedirs(chrome_user_data, exist_ok=True)
    opts.add_argument(f"--user-data-dir={chrome_user_data}")

    # --- Headless mode ---
    if headless:
        opts.add_argument("--headless=new")  # Modern headless (Chrome 112+)

    # --- Stability flags ---
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--remote-debugging-port=0")      # 0 = auto-pick free port
    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-notifications")
    opts.add_argument("--disable-background-networking")
    opts.add_argument("--disable-default-apps")
    opts.add_argument("--no-first-run")
    opts.add_argument("--no-default-browser-check")

    # --- Anti-detection ---
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)

    if user_agent:
        opts.add_argument(f"--user-agent={user_agent}")

    # Suppress password manager
    opts.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    })

    return opts


def make_chrome_driver(headless: bool = True, user_agent: Optional[str] = None) -> webdriver.Chrome:
    """
    Create a Chrome WebDriver instance that works in Docker/Railway containers.

    Uses system chromedriver if available; falls back to selenium-manager auto-download.
    """
    opts = make_chrome_options(headless=headless, user_agent=user_agent)

    chromedriver_path = _find_chromedriver()
    if chromedriver_path:
        service = Service(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=opts)
    else:
        # selenium-manager (Selenium 4.6+) will auto-download matching chromedriver
        driver = webdriver.Chrome(options=opts)

    driver.set_page_load_timeout(30)
    driver.implicitly_wait(5)

    # Override webdriver fingerprint
    try:
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": "Object.defineProperty(navigator,'webdriver',{get:()=>undefined});"}
        )
    except Exception:
        pass

    return driver
