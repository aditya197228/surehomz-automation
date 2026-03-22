"""
flow_login.py — Full Login Flow
=================================
The only file you run for login.
Also imported by every direct booking flow as Step 1.

Run standalone:   python -m login.flow_login
Import in flows:  from login.flow_login import run_login
"""

from core.browser import create_driver, get_base_url, get_credentials, close_driver
from login.login_page import LoginPage
from colorama import Fore, init

init(autoreset=True)


def run_login(driver=None):
    if driver is None:
        driver = create_driver()

    try:
        print(Fore.CYAN + "\n[FLOW] ── Login Flow Started ──")

        url                = get_base_url(role="cp")
        username, password = get_credentials(role="cp")
        login              = LoginPage(driver)

        # Step 1 — Open login page
        login.open(url)

        # Step 2 — Fill username and password
        login.enter_credentials(username, password)

        # Step 3 — Watch captcha field, auto-clicks Sign In when answered
        login.solve_captcha()

        # Step 4 — Confirm dashboard loaded
        login.verify_success()

        print(Fore.GREEN + "[FLOW] ── Login Flow Completed ✓ ──\n")
        return driver

    except Exception as e:
        print(Fore.RED + f"[FLOW ERROR] Login failed → {e}")
        close_driver(driver)
        raise


if __name__ == "__main__":
    driver = run_login()
    input("Press ENTER to close browser...")
    close_driver(driver)