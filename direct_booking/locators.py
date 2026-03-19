"""
locators.py — Direct Booking
==============================
All element locators confirmed from Chrome Inspector.
✓ = confirmed   ⚠ = fallback used, update when ID confirmed

One change here fixes all flows automatically.
"""

from selenium.webdriver.common.by import By


class DashboardL:
    """CP Dashboard — /cp-dashboard"""
    PROJECT = (By.XPATH, "//*[contains(text(),'{}')]")


class ProjectNavL:
    """Project nav — /dashboard"""
    # ✓ confirmed from screenshot
    DIRECT_BOOKING     = (By.XPATH, "//a[contains(text(),'Direct Booking')]")
    DIRECT_BOOKING_ALT = (By.LINK_TEXT, "Direct Booking")


class BookingListL:
    """Direct Booking List — /direct-booking-list"""
    # ✓ confirmed: class="linkBtnC" href="/inventory-list"
    PROCEED     = (By.CLASS_NAME, "linkBtnC")
    PROCEED_ALT = (By.XPATH, "//a[@href='/inventory-list']")


class InventoryL:
    """Inventory List — /inventory-list"""
    # ✓ confirmed: class="linkBtn3 book"
    FIRST_BOOK  = (By.XPATH, "(//a[contains(@class,'book')])[1]")
    BOOK_BY_INV = (By.XPATH, "//tr[contains(.,'{}')] //a[contains(@class,'book')]")
    INV_CELLS   = (By.XPATH, "//table//tbody//tr//td[1]")


class Step1L:
    """Step 1 — /broker-inventory-details"""
    # ✓ confirmed
    HIDDEN_ID       = (By.ID, "hidmaininventoryid")
    CLP             = (By.ID, "clp")
    CLP_ALT         = (By.XPATH, "//input[@name='paymentType' and @value='1']")
    DP              = (By.XPATH, "//input[@name='paymentType' and @value='2']")
    # ✓ confirmed: first checkbox in aapListHolder
    ASSOC_CHECKBOX  = (By.XPATH, "//div[contains(@class,'aapListHolder')]//input[@type='checkbox'][1]")
    # ✓ confirmed: class="linkBtnC" type="button" value="PROCEED TO BOOK"
    PROCEED         = (By.CSS_SELECTOR, "input.linkBtnC[value='PROCEED TO BOOK']")
    PROCEED_ALT     = (By.CSS_SELECTOR, "input.linkBtnC")


class Step2L:
    """Step 2 — /broker-assign-customer"""
    # ✓ all confirmed from inspector screenshots
    MOBILE          = (By.ID, "mobileno")
    MOBILE_PROCEED  = (By.CSS_SELECTOR, "input.linkBtnC.btn1")
    OTP             = (By.ID, "otpval")
    VALIDATE_OTP    = (By.CSS_SELECTOR, "input.linkBtnC.validateotp")
    AFTER_OTP_BTN   = (By.CSS_SELECTOR, "input.linkBtnC.prc")
    # Verified message — any of these appearing means OTP success
    VERIFIED        = (By.XPATH, "//*[contains(text(),'verified') or contains(text(),'Find customer')]")


class Step3L:
    """Step 3 — /broker-direct-booking-form"""
    # ✓ all confirmed from inspector screenshots
    INDIVIDUAL      = (By.CSS_SELECTOR, "input[id='ApplicationKit_GroupFor'][value='Individual']")
    CORPORATE       = (By.CSS_SELECTOR, "input[id='ApplicationKit_GroupFor'][value='Corporate']")
    FIRST_NAME      = (By.ID, "FirstApplicantFirstName")
    LAST_NAME       = (By.ID, "FirstApplicantLastName")
    MOBILE          = (By.ID, "FA_MobileNumber")
    EMAIL           = (By.ID, "FA_EmailID")
    PAN             = (By.ID, "FA_PAN")
    AADHAR          = (By.ID, "FA_AADHARNo")
    FAMILY_INCOME   = (By.ID, "FirstApplicantFamilyIncome")
    TERMS           = (By.CSS_SELECTOR, "a.applyFrom_gtc.cboxElement")
    PROCEED         = (By.CSS_SELECTOR, "button.linkBtnC")
