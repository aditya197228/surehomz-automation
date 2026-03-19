"""
flow_clp_new.py — Direct Booking CLP New Customer
===================================================
Full flow: Login → Dashboard → Step 1 → Step 2 → Step 3

OTP is fully automatic:
  Enter OTP in browser → click Validate → script auto-continues.

Run standalone:   python -m direct_booking.flow_clp_new
Run from UI:      python launcher.py
"""

from colorama import Fore, init
from core.browser import create_driver, close_driver
from login.flow_login import run_login
from direct_booking.booking_page import BookingPage

init(autoreset=True)

# ── Default config ─────────────────────────────────────────
# Used when running standalone.
# UI passes its own config dict when calling run_flow().
DEFAULT = {
    "project":   "Eden Banabitan",
    "inventory": None,               # None = first available
    "mobile":    "8617296574",
    "name":      "Aditya Chaudhary",
    "email":     "aditya28chy@gmail.com",
    "plan":      "CLP",
    "assoc":     "yes",              # yes = select first, no = skip
    "type":      "Individual",
}


def run_flow(driver=None, config=None):
    """
    Runs Direct Booking CLP flow end to end.

    driver=None  → creates a new Chrome session
    config=None  → uses DEFAULT config above
    Returns driver on success.
    """
    cfg        = {**DEFAULT, **(config or {})}
    standalone = driver is None
    inventory  = cfg.get("inventory") or None

    if standalone:
        driver = create_driver()

    try:
        page = BookingPage(driver)

        print(Fore.CYAN + "\n[FLOW] ══ Direct Booking — CLP ══")
        print(Fore.CYAN + f"       Project  : {cfg['project']}")
        print(Fore.CYAN + f"       Plan     : {cfg['plan']} | Type: {cfg['type']}")
        print(Fore.CYAN + f"       Mobile   : {cfg['mobile']}\n")

        # 1. Login
        print(Fore.CYAN + "[1/9] Login")
        run_login(driver=driver)

        # 2. Select project
        print(Fore.CYAN + "[2/9] Select Project")
        page.select_project(cfg["project"])

        # 3. Open Direct Booking
        print(Fore.CYAN + "[3/9] Open Direct Booking")
        page.open_direct_booking()

        # 4. Proceed to Book
        print(Fore.CYAN + "[4/9] Proceed to Book")
        page.proceed_to_book()

        # 5. Select inventory
        print(Fore.CYAN + "[5/9] Select Inventory")
        page.select_inventory(inv_number=inventory)

        # 6. Step 1 — payment plan + associate property
        print(Fore.CYAN + "[6/9] Step 1 — Review & Plan")
        page.verify_step1()
        page.select_plan(plan=cfg["plan"])
        page.select_associate(select=cfg.get("assoc", "yes") == "yes")
        page.proceed_step1()

        # 7. Step 2 — mobile + OTP
        print(Fore.CYAN + "[7/9] Step 2 — Customer Details")
        page.enter_mobile(cfg["mobile"])
        page.wait_otp_verified()    # auto-detects OTP verified
        page.proceed_after_otp()

        # 8. Step 3 — application form
        print(Fore.CYAN + "[8/9] Step 3 — Application Form")
        page.select_type(applying_as=cfg["type"])
        page.fill_form(cfg)
        page.accept_terms()
        page.proceed_step3()

        # 9. Done
        print(Fore.GREEN + "\n[9/9] ══ Flow Complete ✓ ══\n")
        return driver

    except Exception as e:
        print(Fore.RED + f"\n[FLOW ERROR] {e}")
        if standalone:
            close_driver(driver)
        raise


if __name__ == "__main__":
    driver = run_flow()
    input("\nPress ENTER to close browser...")
    close_driver(driver)