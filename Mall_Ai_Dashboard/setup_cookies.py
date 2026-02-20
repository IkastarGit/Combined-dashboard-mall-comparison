import os
import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Add parent directory to path
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from chrome_helper import make_chrome_driver

def generate_facebook_cookies():
    print("\n--- Generating Facebook Cookies ---")
    load_dotenv()
    login_id = os.getenv("FB_LOGIN")
    password = os.getenv("FB_PASSWORD")
    
    if not login_id or not password:
        print("FB_LOGIN and FB_PASSWORD must be in .env")
        return

    driver = make_chrome_driver(headless=False)
    try:
        driver.get("https://www.facebook.com/")
        print("Please log in manually if needed and solve any CAPTCHAs.")
        print("Waiting for search box to appear (indicating successful login)...")
        
        # Wait up to 5 minutes for manual login
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search Facebook']"))
        )
        
        cookie_file = os.path.join(BASE_DIR, "fb_cookies.pkl")
        with open(cookie_file, "wb") as f:
            pickle.dump(driver.get_cookies(), f)
        print(f"Facebook cookies saved to {cookie_file}")
    except Exception as e:
        print(f"Failed to generate Facebook cookies: {e}")
    finally:
        driver.quit()

def generate_instagram_cookies():
    print("\n--- Generating Instagram Cookies ---")
    load_dotenv()
    username = os.getenv("IG_USERNAME") or os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("IG_PASSWORD") or os.getenv("INSTAGRAM_PASSWORD")
    
    if not username or not password:
        print("IG_USERNAME and IG_PASSWORD must be in .env")
        return

    driver = make_chrome_driver(headless=False)
    try:
        driver.get("https://www.instagram.com/accounts/login/")
        print("Please log in manually if needed and solve any CAPTCHAs.")
        print("Waiting for navigation bar to appear (indicating successful login)...")
        
        # Wait up to 5 minutes for manual login
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.TAG_NAME, "nav"))
        )
        
        cookie_file = os.path.join(BASE_DIR, "ig_cookies.pkl")
        with open(cookie_file, "wb") as f:
            pickle.dump(driver.get_cookies(), f)
        print(f"Instagram cookies saved to {cookie_file}")
    except Exception as e:
        print(f"Failed to generate Instagram cookies: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    print("This script will open a visible browser for you to log in.")
    print("Once logged in, it will save cookies to .pkl files.")
    print("You can then upload these .pkl files to Railway.")
    
    choice = input("\nWhich cookies to generate? (fb/ig/both): ").lower()
    if choice in ["fb", "both"]:
        generate_facebook_cookies()
    if choice in ["ig", "both"]:
        generate_instagram_cookies()
