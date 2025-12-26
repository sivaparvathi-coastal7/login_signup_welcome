import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.urls import SIGNUP_URL
from config.signup_locators import SignupLocators
from playwright.sync_api import expect

def test_sign_up_page_elements_visibility(page):
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    expect(page.locator(SignupLocators.SNAPPOD_LOGO_IMG)).to_be_visible(timeout=10000)
    expect(page.locator(SignupLocators.START_CREATING_H1)).to_be_visible(timeout=10000)
    expect(page.locator(SignupLocators.ALREADY_HAVE_ACCOUNT_P)).to_be_visible(timeout=10000)
    expect(page.locator(SignupLocators.SIGNIN_HERE_LINK)).to_be_visible(timeout=10000)
    expect(page.locator(SignupLocators.GOOGLE_SIGNUP_BUTTON)).to_be_visible(timeout=10000)
    expect(page.locator(SignupLocators.FACEBOOK_SIGNUP_BUTTON)).to_be_visible(timeout=10000)
    expect(page.locator(SignupLocators.FIRST_NAME_INPUT)).to_be_visible(timeout=10000)
    expect(page.locator(SignupLocators.LAST_NAME_INPUT)).to_be_visible(timeout=10000)
    expect(page.locator(SignupLocators.PHONE_INPUT)).to_be_visible(timeout=10000)
    expect(page.locator(SignupLocators.EMAIL_INPUT)).to_be_visible(timeout=10000)
    expect(page.locator(SignupLocators.PASSWORD_INPUT)).to_be_visible(timeout=10000)
    expect(page.locator(SignupLocators.CONFIRM_PASSWORD_INPUT)).to_be_visible(timeout=10000)
    expect(page.locator(SignupLocators.SIGNUP_BUTTON)).to_be_visible(timeout=10000)

def test_successful_sign_up(page):
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(SignupLocators.FIRST_NAME_INPUT).fill("John")
    page.locator(SignupLocators.LAST_NAME_INPUT).fill("Doe")
    page.locator(SignupLocators.PHONE_INPUT).fill("1234567890")
    page.locator(SignupLocators.EMAIL_INPUT).fill("sivaparvathiCS4-G3@coastalseven.com")
    page.locator(SignupLocators.PASSWORD_INPUT).fill("Coastal@123")
    page.locator(SignupLocators.CONFIRM_PASSWORD_INPUT).fill("Coastal@123")
    page.locator(SignupLocators.SIGNUP_BUTTON).click()

def test_sign_up_missing_first_name(page):
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(SignupLocators.LAST_NAME_INPUT).fill("Doe")
    page.locator(SignupLocators.EMAIL_INPUT).fill("test@example.com")
    page.locator(SignupLocators.PASSWORD_INPUT).fill("SecurePassword123!")
    page.locator(SignupLocators.CONFIRM_PASSWORD_INPUT).fill("SecurePassword123!")
    page.locator(SignupLocators.SIGNUP_BUTTON).click()
    expect(page.locator(SignupLocators.FIRST_NAME_INPUT)).to_have_attribute("validationMessage", "Please fill out this field.")

def test_sign_up_missing_last_name(page):
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(SignupLocators.FIRST_NAME_INPUT).fill("John")
    page.locator(SignupLocators.EMAIL_INPUT).fill("test@example.com")
    page.locator(SignupLocators.PASSWORD_INPUT).fill("SecurePassword123!")
    page.locator(SignupLocators.CONFIRM_PASSWORD_INPUT).fill("SecurePassword123!")
    page.locator(SignupLocators.SIGNUP_BUTTON).click()
    expect(page.locator(SignupLocators.LAST_NAME_INPUT)).to_have_attribute("validationMessage", "Please fill out this field.")

def test_sign_up_missing_email(page):
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(SignupLocators.FIRST_NAME_INPUT).fill("John")
    page.locator(SignupLocators.LAST_NAME_INPUT).fill("Doe")
    page.locator(SignupLocators.PASSWORD_INPUT).fill("SecurePassword123!")
    page.locator(SignupLocators.CONFIRM_PASSWORD_INPUT).fill("SecurePassword123!")
    page.locator(SignupLocators.SIGNUP_BUTTON).click()
    expect(page.locator(SignupLocators.EMAIL_INPUT)).to_have_attribute("validationMessage", "Please fill out this field.")

def test_sign_up_missing_password(page):
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(SignupLocators.FIRST_NAME_INPUT).fill("John")
    page.locator(SignupLocators.LAST_NAME_INPUT).fill("Doe")
    page.locator(SignupLocators.EMAIL_INPUT).fill("test@example.com")
    page.locator(SignupLocators.CONFIRM_PASSWORD_INPUT).fill("SecurePassword123!")
    page.locator(SignupLocators.SIGNUP_BUTTON).click()
    expect(page.locator(SignupLocators.PASSWORD_INPUT)).to_have_attribute("validationMessage", "Please fill out this field.")

def test_sign_up_missing_re_enter_password(page):
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(SignupLocators.FIRST_NAME_INPUT).fill("John")
    page.locator(SignupLocators.LAST_NAME_INPUT).fill("Doe")
    page.locator(SignupLocators.EMAIL_INPUT).fill("test@example.com")
    page.locator(SignupLocators.PASSWORD_INPUT).fill("SecurePassword123!")
    page.locator(SignupLocators.SIGNUP_BUTTON).click()
    expect(page.locator(SignupLocators.CONFIRM_PASSWORD_INPUT)).to_have_attribute("validationMessage", "Please fill out this field.")

def test_sign_up_invalid_email_format(page):
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(SignupLocators.FIRST_NAME_INPUT).fill("John")
    page.locator(SignupLocators.LAST_NAME_INPUT).fill("Doe")
    page.locator(SignupLocators.EMAIL_INPUT).fill("invalid-email")
    page.locator(SignupLocators.PASSWORD_INPUT).fill("SecurePassword123!")
    page.locator(SignupLocators.CONFIRM_PASSWORD_INPUT).fill("SecurePassword123!")
    page.locator(SignupLocators.SIGNUP_BUTTON).click()
    expect(page.locator(SignupLocators.EMAIL_INPUT)).to_have_attribute("validationMessage", expect.string_containing("@"))

def test_sign_up_mismatched_passwords(page):
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(SignupLocators.FIRST_NAME_INPUT).fill("John")
    page.locator(SignupLocators.LAST_NAME_INPUT).fill("Doe")
    page.locator(SignupLocators.EMAIL_INPUT).fill("test@example.com")
    page.locator(SignupLocators.PASSWORD_INPUT).fill("SecurePassword123!")
    page.locator(SignupLocators.CONFIRM_PASSWORD_INPUT).fill("MismatchPassword123")
    page.locator(SignupLocators.SIGNUP_BUTTON).click()
    expect(page.locator(SignupLocators.PASSWORD_MISMATCH_ERROR)).to_be_visible()

def test_sign_up_short_password(page):
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(SignupLocators.FIRST_NAME_INPUT).fill("John")
    page.locator(SignupLocators.LAST_NAME_INPUT).fill("Doe")
    page.locator(SignupLocators.EMAIL_INPUT).fill("shortpass@example.com")
    page.locator(SignupLocators.PASSWORD_INPUT).fill("short")
    page.locator(SignupLocators.CONFIRM_PASSWORD_INPUT).fill("short")
    page.locator(SignupLocators.SIGNUP_BUTTON).click()
    expect(page.locator(SignupLocators.PASSWORD_LENGTH_ERROR)).to_be_visible()

def test_sign_up_invalid_phone_number_format(page):
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(SignupLocators.FIRST_NAME_INPUT).fill("John")
    page.locator(SignupLocators.LAST_NAME_INPUT).fill("Doe")
    page.locator(SignupLocators.PHONE_INPUT).fill("123")
    page.locator(SignupLocators.EMAIL_INPUT).fill("phone@example.com")
    page.locator(SignupLocators.PASSWORD_INPUT).fill("SecurePassword123!")
    page.locator(SignupLocators.CONFIRM_PASSWORD_INPUT).fill("SecurePassword123!")
    page.locator(SignupLocators.SIGNUP_BUTTON).click()
    expect(page.locator(SignupLocators.PHONE_FORMAT_ERROR)).to_be_visible()

def test_navigate_to_login_page_from_sign_up(page):
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(SignupLocators.SIGNIN_HERE_LINK).click()
    expect(page).to_have_url("https://dev.vox.snappod.ai/login")

def test_sign_up_with_google_button(page):
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(SignupLocators.GOOGLE_SIGNUP_BUTTON).click()
    page.wait_for_url("https://accounts.google.com/*")

def test_sign_up_with_facebook_button(page):
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(SignupLocators.FACEBOOK_SIGNUP_BUTTON).click()
    page.wait_for_url("https://www.facebook.com/*")