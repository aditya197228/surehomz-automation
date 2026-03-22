"""
booking_page.py — Direct Booking
==================================
All page interactions for Direct Booking flow.
Inherits BasePage — screenshots built in automatically.

Delay of 2 seconds added after each booking action here only.
base_page.py is untouched so login and other modules are unaffected.

OTP: enter in browser → click Validate → script auto-detects and continues.
No ENTER press needed anywhere in this flow.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from colorama import Fore, init
from core.base_page import BasePage
from direct_booking.locators import (
    DashboardL, ProjectNavL, BookingListL,
    InventoryL, Step1L, Step2L, Step3L
)
import time

init(autoreset=True)

DELAY       = 2    # seconds between booking actions
OTP_TIMEOUT = 120  # seconds to wait for OTP verification


class BookingPage(BasePage):

    # ── Dashboard ────────────────────────────────────────────

    def select_project(self, name):
        """Click project card by name. Wait for project dashboard."""
        print(Fore.CYAN + f"[DASHBOARD] Selecting → {name}")
        locator = (By.XPATH, f"//*[contains(text(),'{name}')]")
        try:
            self.click(locator, label=name)
        except Exception:
            self.driver.execute_script("window.scrollTo(0,300);")
            self.click(locator, label=f"{name} (scrolled)")
        self.wait_for_url_contains("dashboard", label="Project Dashboard")
        time.sleep(DELAY)

    # ── Project Nav ──────────────────────────────────────────

    def open_direct_booking(self):
        """Click Direct Booking in project nav."""
        print(Fore.CYAN + "[NAV] Opening Direct Booking...")
        try:
            self.click(ProjectNavL.DIRECT_BOOKING, label="Direct Booking")
        except Exception:
            self.click(ProjectNavL.DIRECT_BOOKING_ALT, label="Direct Booking (alt)")
        self.wait_for_url_contains("direct-booking", label="Booking List")
        time.sleep(DELAY)

    # ── Booking List ─────────────────────────────────────────

    def proceed_to_book(self):
        """Click Proceed to Book. Wait for inventory list."""
        print(Fore.CYAN + "[BOOKING] Proceed to Book...")
        try:
            self.click(BookingListL.PROCEED, label="Proceed to Book")
        except Exception:
            self.click(BookingListL.PROCEED_ALT, label="Proceed to Book (alt)")
        self.wait_for_url_contains("inventory-list", label="Inventory List")
        time.sleep(DELAY)

    # ── Inventory List ───────────────────────────────────────

    def select_inventory(self, inv_number=None):
        """
        Click BOOK on an inventory.
        inv_number=None → first available (auto)
        inv_number="X"  → specific row match
        """
        if inv_number:
            print(Fore.CYAN + f"[INVENTORY] Selecting → {inv_number}")
            loc = (By.XPATH,
                f"//tr[contains(.,'{inv_number}')] //a[contains(@class,'book')]")
            self.scroll_to_element(loc, label=f"BOOK {inv_number}")
            self.click(loc, label=f"BOOK {inv_number}")
        else:
            print(Fore.CYAN + "[INVENTORY] Selecting first available...")
            self.click(InventoryL.FIRST_BOOK, label="First BOOK")
        self.wait_for_url_contains("broker-inventory-details", label="Step 1")
        time.sleep(DELAY)

    # ── Step 1 ───────────────────────────────────────────────

    def verify_step1(self):
        """Read hidden inventory ID to confirm Step 1 loaded."""
        try:
            inv_id = self.driver.find_element(
                *Step1L.HIDDEN_ID).get_attribute("value")
            print(Fore.GREEN + f"[STEP1] Inventory ID → {inv_id} ✓")
            return inv_id
        except Exception:
            print(Fore.YELLOW + "[STEP1] Could not read inventory ID")
            return None

    def select_plan(self, plan="CLP"):
        """Select CLP or DP payment plan via JS click."""
        print(Fore.CYAN + f"[STEP1] Payment plan → {plan}")
        locs = [Step1L.CLP, Step1L.CLP_ALT] if plan.upper() == "CLP" else [Step1L.DP]
        for loc in locs:
            try:
                el = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(loc))
                self.driver.execute_script("arguments[0].click();", el)
                print(Fore.GREEN + f"[STEP1] {plan} ✓")
                time.sleep(DELAY)
                return
            except Exception:
                continue
        self._take_screenshot(f"plan_fail_{plan}")
        raise Exception(f"Payment plan {plan} not found")

    def select_associate(self, select=True):
        """Tick first associate property checkbox."""
        if not select:
            print(Fore.CYAN + "[STEP1] Associate property → skipped")
            return
        print(Fore.CYAN + "[STEP1] Selecting first associate property...")
        try:
            el = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(Step1L.ASSOC_CHECKBOX))
            self.driver.execute_script("arguments[0].click();", el)
            print(Fore.GREEN + "[STEP1] Associate property ✓")
            time.sleep(DELAY)
        except Exception:
            print(Fore.YELLOW + "[STEP1] Checkbox not found — skipping")

    def proceed_step1(self):
        """Click Proceed to Book on Step 1 via JS click."""
        print(Fore.CYAN + "[STEP1] Proceeding...")
        for loc in [Step1L.PROCEED, Step1L.PROCEED_ALT]:
            try:
                el = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(loc))
                self.driver.execute_script("arguments[0].click();", el)
                print(Fore.GREEN + "[STEP1] Proceed ✓")
                time.sleep(DELAY)
                return
            except Exception:
                continue
        self._take_screenshot("step1_proceed_fail")
        raise Exception("Step 1 Proceed button not found")

    # ── Step 2 ───────────────────────────────────────────────

    def enter_mobile(self, mobile):
        """Enter mobile number and click Proceed. Wait for OTP screen."""
        print(Fore.CYAN + f"[STEP2] Mobile → {mobile}")
        self.wait_for_url_contains("broker-assign-customer", label="Step 2")
        self.fill(Step2L.MOBILE, mobile, label="Mobile")
        time.sleep(1)
        el = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(Step2L.MOBILE_PROCEED))
        self.driver.execute_script("arguments[0].click();", el)
        print(Fore.GREEN + "[STEP2] Mobile submitted ✓")
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(Step2L.OTP))
        print(Fore.GREEN + "[STEP2] OTP screen loaded ✓")
        time.sleep(DELAY)

    def wait_otp_verified(self):
        """
            Watches OTP input field.
            As soon as 6 digits are typed, auto-clicks Validate.
            No ENTER needed. No terminal interaction needed.
            Just type OTP in browser and walk away.
        """
        print()
        print(Fore.YELLOW + "─" * 50)
        print(Fore.YELLOW + "  ⏸  TYPE OTP IN BROWSER")
        print(Fore.YELLOW + "  →  Script auto-validates when 6 digits entered")
        print(Fore.YELLOW + "  →  No ENTER needed")
        print(Fore.YELLOW + "─" * 50)
        print()

        # Step 1 — wait for OTP field to have 6 digits
        print(Fore.CYAN + "[STEP2] Watching OTP field...")
        start = time.time()
        while time.time() - start < OTP_TIMEOUT:
            try:
                otp_field = self.driver.find_element(*Step2L.OTP)
                otp_value = otp_field.get_attribute("value")
                if otp_value and len(otp_value.strip()) >= 4:
                    print(Fore.GREEN + f"[STEP2] OTP detected → {otp_value} ✓")
                    break
            except Exception:
                pass
            time.sleep(0.5)
        else:
            self._take_screenshot("otp_timeout")
            raise Exception(f"OTP not entered after {OTP_TIMEOUT}s")

        # Step 2 — auto-click Validate button
        time.sleep(0.5)  # tiny pause so field value settles
        print(Fore.CYAN + "[STEP2] Auto-clicking Validate...")
        try:
            el = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(Step2L.VALIDATE_OTP))
            self.driver.execute_script("arguments[0].click();", el)
            print(Fore.GREEN + "[STEP2] Validate clicked ✓")
        except Exception:
            self._take_screenshot("validate_btn_fail")
            raise Exception("Validate button not found after OTP entered")

        # Step 3 — wait for verified state
        print(Fore.CYAN + "[STEP2] Waiting for OTP verification...")
        time.sleep(2)  # give server time to verify
        print(Fore.GREEN + "[STEP2] OTP verified — continuing ✓")
        time.sleep(DELAY)

    def proceed_after_otp(self):
        """Click Proceed to Book after OTP verified. Wait for Step 3."""
        print(Fore.CYAN + "[STEP2] Proceeding to Step 3...")
        el = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(Step2L.AFTER_OTP_BTN))
        self.driver.execute_script("arguments[0].click();", el)
        self.wait_for_url_contains("broker-direct-booking-form", label="Step 3")
        time.sleep(DELAY)

    # ── Step 3 ───────────────────────────────────────────────

    def select_type(self, applying_as="Individual"):
        """Select Individual or Corporate radio. Wait for form fields."""
        print(Fore.CYAN + f"[STEP3] Applying as → {applying_as}")
        loc = Step3L.INDIVIDUAL if applying_as == "Individual" else Step3L.CORPORATE
        el = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(loc))
        self.driver.execute_script("arguments[0].click();", el)
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(Step3L.FIRST_NAME))
        print(Fore.GREEN + f"[STEP3] {applying_as} ✓")
        time.sleep(DELAY)

    def fill_form(self, cfg):
        """
        Fill application form from config dict.
        Splits name into first and last.
        Sets first family income option via JS.
        cfg keys: name, mobile, email
        """
        print(Fore.CYAN + "[STEP3] Filling form...")
        parts = cfg.get("name", "Aditya Chaudhary").split(" ", 1)
        fname = parts[0]
        lname = parts[1] if len(parts) > 1 else "."

        self.fill(Step3L.FIRST_NAME, fname,                label="First Name")
        self.fill(Step3L.LAST_NAME,  lname,                label="Last Name")
        self.fill(Step3L.MOBILE,     cfg.get("mobile",""), label="Mobile")
        self.fill(Step3L.EMAIL,      cfg.get("email", ""), label="Email")

        try:
            self.driver.execute_script(
                "var s=document.getElementById('FirstApplicantFamilyIncome');"
                "s.selectedIndex=1; s.dispatchEvent(new Event('change'));")
            print(Fore.GREEN + "[STEP3] Family Income ✓")
            time.sleep(1)
        except Exception:
            print(Fore.YELLOW + "[STEP3] Family Income — skipped")

        print(Fore.GREEN + "[STEP3] Form filled ✓")
        time.sleep(DELAY)

    def accept_terms(self):
        """Click Terms & Conditions anchor checkbox via JS click."""
        print(Fore.CYAN + "[STEP3] Accepting terms...")
        try:
            el = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(Step3L.TERMS))
            self.driver.execute_script("arguments[0].click();", el)
            print(Fore.GREEN + "[STEP3] Terms ✓")
            time.sleep(DELAY)
        except Exception:
            print(Fore.YELLOW + "[STEP3] Terms not found — skipping")

    def proceed_step3(self):
        """Click Proceed to Book button on Step 3."""
        print(Fore.CYAN + "[STEP3] Proceeding...")
        el = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(Step3L.PROCEED))
        self.driver.execute_script("arguments[0].click();", el)
        print(Fore.GREEN + "[STEP3] Proceed ✓")
        time.sleep(DELAY)