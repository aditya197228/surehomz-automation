"""
login_page.py — Login Page Actions
=====================================
Handles all interactions on the SureHomz CP login page.
Inherits from BasePage — uses click(), fill(), wait_for_element() etc.

Current scope : CP (Broker) module
Future scope  : Developer, Admin modules (same login structure)
"""

from core.base_page import BasePage
from login.locators import LoginLocators
from colorama import Fore, init
import time
import re

init(autoreset=True)


class LoginPage(BasePage):

    def open(self, base_url):
        """Navigate to login page. Wait for username field."""
        self.go_to(base_url)
        self.wait_for_element(LoginLocators.USERNAME, label="Username field")
        print(Fore.GREEN + "[LOGIN] Login page loaded ✓")

    def enter_credentials(self, username, password):
        """Fill username and password from .env."""
        self.fill(LoginLocators.USERNAME, username, label="Username")
        self.fill(LoginLocators.PASSWORD, password, label="Password")

    def solve_captcha(self):
        """
        Watches CaptchaResult field every 0.5s.
        You type the answer — script detects digits typed,
        then auto-clicks Sign In. No ENTER needed.
        Same pattern as OTP in booking flow.
        """
        print()
        print(Fore.YELLOW + "─" * 50)
        print(Fore.YELLOW + "  ⏸  SOLVE CAPTCHA IN BROWSER")
        print(Fore.YELLOW + "  →  Type the answer in the field")
        print(Fore.YELLOW + "  →  Script auto-clicks Sign In")
        print(Fore.YELLOW + "─" * 50)
        print()

        print(Fore.CYAN + "[CAPTCHA] Watching answer field...")
        start = time.time()
        while time.time() - start < 120:
            try:
                field = self.driver.find_element(*LoginLocators.CAPTCHA_INPUT)
                value = field.get_attribute("value")
                if value and re.match(r'^\d+$', value.strip()):
                    print(Fore.GREEN + f"[CAPTCHA] Answer detected → {value} ✓")
                    break
            except Exception:
                pass
            time.sleep(0.5)
        else:
            self._take_screenshot("captcha_timeout")
            raise Exception("Captcha not answered within 120s")

        # tiny pause so value settles then auto-click Sign In
        time.sleep(0.5)
        print(Fore.CYAN + "[CAPTCHA] Auto-clicking Sign In...")
        btn = self.driver.find_element(*LoginLocators.LOGIN_BTN)
        self.driver.execute_script("arguments[0].click();", btn)
        print(Fore.GREEN + "[CAPTCHA] Sign In clicked ✓")

    def verify_success(self):
        """Confirm redirect to cp-dashboard after login."""
        self.wait_for_url_contains("cp-dashboard", label="cp-dashboard")
        print(Fore.GREEN + "[LOGIN] Login successful ✓")

    def is_login_failed(self):
        """Returns True if error message visible. Used for graceful failure."""
        return self.is_element_present(LoginLocators.ERROR_MSG, timeout=3)