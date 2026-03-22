"""
locators.py — Login Page Locators
===================================
All element locators for the login page in one place.
If SureHomz ever changes an element, update here only — nothing else breaks.
"""

from selenium.webdriver.common.by import By


class LoginLocators:
    USERNAME      = (By.ID, "UserName")
    PASSWORD      = (By.ID, "Password")
    LOGIN_BTN     = (By.ID, "btnlogin")
    CAPTCHA_INPUT = (By.ID, "CaptchaResult")   # ← added
    ERROR_MSG     = (By.CLASS_NAME, "validation-summary-errors")