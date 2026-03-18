"""
flow_login.py — Full Login Flow
=================================
The only file you run for login.
Also imported by every direct booking flow as Step 1.

Run standalone:
    python login/flow_login.py

Import in booking flows:
    from login.flow_login import run_login
    run_login(driver=driver)
"""

from core.browser import create_driver, get_base_url, get_credentials, close_driver
from login.login_page import LoginPage
from colorama import Fore, init

init(autoreset=True)


def run_login(driver=None):
    """
    Runs full login flow end to end.

    Two ways to call:
        1. Standalone — no driver passed, creates its own
           run_login()

        2. From booking flow — pass existing driver, browser stays open
           run_login(driver=driver)

    Returns driver so booking flow can continue on same session.
    """

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

        # Step 3 — Manual captcha pause
        login.solve_captcha()

        # Step 4 — Click login button
        login.submit()

        # Step 5 — Confirm dashboard loaded
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