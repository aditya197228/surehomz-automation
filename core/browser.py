"""
browser.py — Core Browser Setup
================================
Responsible for Chrome driver initialization and credential management.
Used by every flow script across all modules.

Current scope : CP (Broker) module
Future scope  : Developer, Admin modules (add to .env when needed)
"""

import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from colorama import Fore, init

# Initialize colorama for colored terminal output
init(autoreset=True)

# Load .env file into environment
load_dotenv()


# ─────────────────────────────────────────────────────────────
# ENVIRONMENT
# ─────────────────────────────────────────────────────────────

def get_base_url(role="cp"):
    """
    Returns base URL for the given role.

    Roles:
        cp    → Channel Partner / Broker  (active)
        dev   → Developer module          (future)
        admin → Admin module              (future)

    Usage:
        url = get_base_url()              # defaults to cp
        url = get_base_url(role="dev")    # future use
    """
    urls = {
        "cp":    os.getenv("CP_URL"),
        "dev":   os.getenv("DEV_URL"),
        "admin": os.getenv("ADMIN_URL"),
    }

    url = urls.get(role)

    if not url:
        print(Fore.RED + f"[ENV ERROR] No URL configured for role '{role}'. Check .env file.")
        raise ValueError(f"URL not configured for role: {role}")

    print(Fore.CYAN + f"[ENV] Role: {role.upper()} → {url}")
    return url


def get_credentials(role="cp"):
    """
    Returns (username, password) for the given role.

    Roles:
        cp    → Channel Partner / Broker  (active)
        dev   → Developer module          (future)
        admin → Admin module              (future)

    Usage:
        username, password = get_credentials()
        username, password = get_credentials(role="dev")
    """
    credentials = {
        "cp":    (os.getenv("CP_USERNAME"),    os.getenv("CP_PASSWORD")),
        "dev":   (os.getenv("DEV_USERNAME"),   os.getenv("DEV_PASSWORD")),
        "admin": (os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD")),
    }

    username, password = credentials.get(role, (None, None))

    if not username or not password:
        print(Fore.RED + f"[CREDENTIALS ERROR] No credentials configured for role '{role}'. Check .env file.")
        raise ValueError(f"Credentials not configured for role: {role}")

    print(Fore.CYAN + f"[CREDENTIALS] Loaded → {username}")
    return username, password


# ─────────────────────────────────────────────────────────────
# BROWSER
# ─────────────────────────────────────────────────────────────

def create_driver():
    """
    Launches Chrome in full visual mode with performance optimizations.
    Uses Selenium Manager — no manual ChromeDriver setup ever needed.
    Returns driver instance ready to use.

    Usage:
        driver = create_driver()
    """
    print(Fore.YELLOW + "[BROWSER] Setting up Chrome...")

    options = Options()

    # ── Visual ────────────────────────────────────────────────
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # ── Performance ───────────────────────────────────────────
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")

    # Disable save password and autofill popups
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "autofill.profile_enabled": False
    })

    # ── Driver ────────────────────────────────────────────────
    # Selenium Manager auto detects and downloads correct ChromeDriver
    driver = webdriver.Chrome(options=options)

    # ── Timeouts ──────────────────────────────────────────────
    driver.set_page_load_timeout(30)   # fail if page takes over 30s
    driver.implicitly_wait(10)          # wait up to 10s for elements

    print(Fore.GREEN + "[BROWSER] Chrome launched successfully ✓")
    return driver


def close_driver(driver):
    """
    Safely closes Chrome at end of any flow.
    Safe to call even if browser already crashed.

    Usage:
        close_driver(driver)
    """
    try:
        driver.quit()
        print(Fore.YELLOW + "[BROWSER] Chrome closed ✓")
    except Exception:
        pass

