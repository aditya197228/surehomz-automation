"""
base_page.py — Core Base Page
==============================
Parent class inherited by every page class across all modules.
Wraps all Selenium actions with waits, logging, and auto-screenshot on failure.

Current scope : CP (Broker) module
Future scope  : Developer, Admin modules
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from colorama import Fore, init
import os

init(autoreset=True)

DEFAULT_TIMEOUT = 10  # matches implicitly_wait(10) in browser.py


class BasePage:
    """
    All page classes inherit from this.

    Usage:
        class LoginPage(BasePage):
            def __init__(self, driver):
                super().__init__(driver)
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)


    # ─────────────────────────────────────────────────────────
    # NAVIGATION
    # ─────────────────────────────────────────────────────────

    def go_to(self, url):
        """Navigate to a URL."""
        print(Fore.CYAN + f"[NAV] Going to → {url}")
        self.driver.get(url)

    def get_current_url(self):
        """Returns the current browser URL."""
        return self.driver.current_url

    def wait_for_url_contains(self, partial_url, label="page"):
        """
        Wait until URL contains a string — confirms navigation happened.

        Usage:
            self.wait_for_url_contains("dashboard", label="Dashboard")
        """
        try:
            WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
                EC.url_contains(partial_url)
            )
            print(Fore.GREEN + f"[NAV] Reached {label} ✓")
        except TimeoutException:
            print(Fore.RED + f"[NAV ERROR] URL did not contain '{partial_url}' after {DEFAULT_TIMEOUT}s")
            self._take_screenshot(f"nav_fail_{label}")
            raise


    # ─────────────────────────────────────────────────────────
    # ELEMENT ACTIONS
    # ─────────────────────────────────────────────────────────

    def click(self, locator, label="element"):
        """
        Wait for element to be clickable then click.

        Usage:
            self.click((By.ID, "loginBtn"), label="Login Button")
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            print(Fore.GREEN + f"[CLICK] {label} ✓")
        except TimeoutException:
            print(Fore.RED + f"[CLICK ERROR] '{label}' not clickable after {DEFAULT_TIMEOUT}s")
            self._take_screenshot(f"click_fail_{label}")
            raise

    def fill(self, locator, text, label="field"):
        """
        Clear field and type text.

        Usage:
            self.fill((By.ID, "username"), "test@email.com", label="Username")
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(text)
            print(Fore.GREEN + f"[FILL] {label} ✓")
        except TimeoutException:
            print(Fore.RED + f"[FILL ERROR] '{label}' not visible after {DEFAULT_TIMEOUT}s")
            self._take_screenshot(f"fill_fail_{label}")
            raise

    def get_text(self, locator, label="element"):
        """
        Returns visible text of an element.

        Usage:
            msg = self.get_text((By.CLASS_NAME, "toast"), label="Toast Message")
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            text = element.text.strip()
            print(Fore.CYAN + f"[TEXT] {label} → '{text}'")
            return text
        except TimeoutException:
            print(Fore.RED + f"[TEXT ERROR] '{label}' not visible after {DEFAULT_TIMEOUT}s")
            return ""

    def select_dropdown(self, locator, visible_text, label="dropdown"):
        """
        Select option from a <select> dropdown by visible text.
        For jQuery/custom dropdowns use click() instead.

        Usage:
            self.select_dropdown((By.ID, "paymentPlan"), "CLP", label="Payment Plan")
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            Select(element).select_by_visible_text(visible_text)
            print(Fore.GREEN + f"[DROPDOWN] {label} → '{visible_text}' ✓")
        except TimeoutException:
            print(Fore.RED + f"[DROPDOWN ERROR] '{label}' not clickable after {DEFAULT_TIMEOUT}s")
            self._take_screenshot(f"dropdown_fail_{label}")
            raise

    def scroll_to_element(self, locator, label="element"):
        """
        Scroll element into view before interacting.
        Useful for SureHomz long booking forms.

        Usage:
            self.scroll_to_element((By.ID, "submitBtn"), label="Submit")
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            print(Fore.CYAN + f"[SCROLL] Scrolled to {label}")
        except TimeoutException:
            print(Fore.RED + f"[SCROLL ERROR] '{label}' not found")
            raise


    # ─────────────────────────────────────────────────────────
    # CHECKS
    # ─────────────────────────────────────────────────────────

    def is_element_present(self, locator, timeout=5):
        """
        Returns True if element appears within timeout, False otherwise.
        Never raises — safe to use in if conditions.

        Usage:
            if self.is_element_present((By.ID, "errorMsg")):
                print("Login failed")
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_element(self, locator, label="element", timeout=None):
        """
        Wait for element to be visible. Raises if not found.
        Use before reading dynamic content after page transitions.

        Usage:
            self.wait_for_element((By.ID, "dashboard"), label="Dashboard")
        """
        t = timeout or DEFAULT_TIMEOUT
        try:
            WebDriverWait(self.driver, t).until(
                EC.visibility_of_element_located(locator)
            )
            print(Fore.GREEN + f"[WAIT] {label} visible ✓")
        except TimeoutException:
            print(Fore.RED + f"[WAIT ERROR] '{label}' not visible after {t}s")
            self._take_screenshot(f"wait_fail_{label}")
            raise


    # ─────────────────────────────────────────────────────────
    # SCREENSHOT
    # ─────────────────────────────────────────────────────────

    def _take_screenshot(self, name):
        """
        Saves screenshot to screenshots/ folder.
        Called automatically on any failure.
        Can also be called manually from flow scripts.

        Usage:
            self._take_screenshot("after_otp_step")
        """
        try:
            os.makedirs("screenshots", exist_ok=True)
            path = os.path.join("screenshots", f"{name}.png")
            self.driver.save_screenshot(path)
            print(Fore.YELLOW + f"[SCREENSHOT] Saved → {path}")
        except Exception as e:
            print(Fore.RED + f"[SCREENSHOT ERROR] {e}")