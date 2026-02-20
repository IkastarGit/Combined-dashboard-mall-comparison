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


def _is_container() -> bool:
    """Detect if we are running inside a Docker/Railway container."""
    return (
        os.path.exists("/.dockerenv")
        or os.environ.get("RAILWAY_ENVIRONMENT") is not None
        or os.environ.get("RAILWAY_SERVICE_NAME") is not None
        or os.environ.get("DOCKER_CONTAINER") is not None
    )


def make_chrome_options(headless: bool = True, user_agent: Optional[str] = None, enable_network_logs: bool = False) -> Options:
    """
    Build Chrome options that work in both Docker/Railway containers and local Windows/Mac.
    """
    opts = Options()

    if enable_network_logs:
        opts.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    # --- Binary location (critical in containers) ---
    chrome_bin = _find_chrome_binary()
    if chrome_bin:
        opts.binary_location = chrome_bin

    # --- Core container-essential flags (always applied) ---
    opts.add_argument("--no-sandbox")                    # Required: no kernel namespaces in containers
    opts.add_argument("--disable-dev-shm-usage")         # Required: /dev/shm too small in containers
    opts.add_argument("--disable-setuid-sandbox")        # Required: no setuid support
    opts.add_argument("--disable-gpu")                   # No GPU in containers
    opts.add_argument("--disable-software-rasterizer")   # Avoid SwiftShader errors

    in_container = _is_container()

    if in_container:
        # Extra stability flags required in Railway / low-memory containers
        opts.add_argument("--single-process")                          # Run renderer in browser process (low-mem)
        opts.add_argument("--disable-features=VizDisplayCompositor")  # Avoid compositor crash
        opts.add_argument("--disable-features=AudioServiceOutOfProcess")
        opts.add_argument("--disable-background-timer-throttling")
        opts.add_argument("--disable-backgrounding-occluded-windows")
        opts.add_argument("--disable-renderer-backgrounding")
        opts.add_argument("--disable-default-apps")
        opts.add_argument("--disable-sync")
        opts.add_argument("--disable-translate")
        opts.add_argument("--metrics-recording-only")
        opts.add_argument("--mute-audio")
        opts.add_argument("--no-first-run")
        opts.add_argument("--no-default-browser-check")
        opts.add_argument("--safebrowsing-disable-auto-update")
        opts.add_argument("--password-store=basic")
        opts.add_argument("--use-mock-keychain")

    # --- CRITICAL: Give Chrome a writable temp directory ---
    chrome_user_data = os.environ.get("CHROME_USER_DATA_DIR", "/tmp/chrome-user-data")
    os.makedirs(chrome_user_data, exist_ok=True)
    opts.add_argument(f"--user-data-dir={chrome_user_data}")

    # --- Headless mode ---
    if headless:
        # Use legacy --headless for maximum container compatibility.
        # --headless=new requires more system resources and crashes in constrained envs.
        opts.add_argument("--headless")

    # --- Stability flags ---
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-notifications")
    opts.add_argument("--disable-background-networking")

    # NOTE: Do NOT add experimental_options (excludeSwitches / useAutomationExtension)
    # in headless/container mode — they cause SessionNotCreatedException on some
    # Chrome versions when combined with --headless.

    if user_agent:
        opts.add_argument(f"--user-agent={user_agent}")

    return opts


def make_chrome_driver(headless: bool = True, user_agent: Optional[str] = None, enable_network_logs: bool = False) -> webdriver.Chrome:
    """
    Create a Chrome WebDriver instance that works in Docker/Railway containers.

    Uses system chromedriver if available; falls back to selenium-manager auto-download.
    """
    opts = make_chrome_options(headless=headless, user_agent=user_agent, enable_network_logs=enable_network_logs)

    chromedriver_path = _find_chromedriver()
    if chromedriver_path:
        service = Service(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=opts)
    else:
        # selenium-manager (Selenium 4.6+) will auto-download matching chromedriver
        driver = webdriver.Chrome(options=opts)

    driver.set_page_load_timeout(30)
    driver.implicitly_wait(5)

    # Override webdriver fingerprint (only when NOT in strict headless container mode)
    if not _is_container():
        try:
            driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {"source": "Object.defineProperty(navigator,'webdriver',{get:()=>undefined});"}
            )
        except Exception:
            pass

    return driver
