"""
login_page.py — Login Page Actions
=====================================
Handles all interactions on the SureHomz CP login page.
Inherits from BasePage — uses click(), fill(), wait_for_element() etc.

Current scope : CP (Broker) module
Future scope  : Developer, Admin modules (same login structure)
"""

from core.base_page import BasePage
from core.manual_pause import manual_pause
from login.locators import LoginLocators
from colorama import Fore, init

init(autoreset=True)


class LoginPage(BasePage):
    """
    Handles all login page interactions.

    Usage:
        login = LoginPage(driver)
        login.open(base_url)
        login.enter_credentials(username, password)
        login.solve_captcha()
        login.submit()
        login.verify_success()
    """

    def open(self, base_url):
        """
        Navigate to login page and confirm it loaded.
        Waits for username field to be visible before proceeding.
        """
        self.go_to(base_url)
        self.wait_for_element(LoginLocators.USERNAME, label="Username field")
        print(Fore.GREEN + "[LOGIN] Login page loaded ✓")


    def enter_credentials(self, username, password):
        """
        Fill username and password from .env credentials.
        Fields are cleared before typing to avoid leftover values.
        """
        self.fill(LoginLocators.USERNAME, username, label="Username")
        self.fill(LoginLocators.PASSWORD, password, label="Password")


    def solve_captcha(self):
        """
        Pauses script for human to solve captcha manually.
        Script resumes only after ENTER is pressed.
        """
        manual_pause("Solve the captcha in the browser then press ENTER")


    def submit(self):
        """Click the login button to submit the form."""
        self.click(LoginLocators.LOGIN_BTN, label="Login Button")


    def verify_success(self):
        """
        Confirms login was successful by checking URL contains 'dashboard'.
        Raises exception if dashboard is not reached — flow stops immediately.
        """
        self.wait_for_url_contains("cp-dashboard", label="cp-dashboard")
        print(Fore.GREEN + "[LOGIN] Login successful ✓")


    def is_login_failed(self):
        """
        Returns True if error message is visible after submit.
        Use to handle wrong credentials gracefully.

        Usage:
            if login.is_login_failed():
                excel.write_result(1, "FAIL", "Invalid credentials")
        """
        return self.is_element_present(LoginLocators.ERROR_MSG, timeout=3)