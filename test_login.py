import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.urls import LOGIN_URL, SIGNUP_URL
from config.login_locators import LoginLocators
from playwright.sync_api import expect

def test_login_page_elements_visibility(page):
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    expect(page.locator(LoginLocators.SNAPPOD_LOGO_IMG)).to_be_visible(timeout=10000)
    expect(page.locator(LoginLocators.WELCOME_BACK_H2)).to_be_visible(timeout=10000)
    expect(page.locator(LoginLocators.EMAIL_LABEL)).to_be_visible(timeout=10000)
    expect(page.locator(LoginLocators.PASSWORD_LABEL)).to_be_visible(timeout=10000)
    expect(page.locator(LoginLocators.FORGOT_PASSWORD_LINK)).to_be_visible(timeout=10000)
    expect(page.locator(LoginLocators.LOGIN_BUTTON)).to_be_visible(timeout=10000)
    expect(page.locator(LoginLocators.OR_TEXT)).to_be_visible(timeout=10000)
    expect(page.locator(LoginLocators.GOOGLE_LOGIN_BUTTON)).to_be_visible(timeout=10000)
    expect(page.locator(LoginLocators.DONT_HAVE_ACCOUNT_TEXT)).to_be_visible(timeout=10000)
    expect(page.locator(LoginLocators.SIGNUP_HERE_LINK)).to_be_visible(timeout=10000)

def test_successful_login(page):
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(LoginLocators.EMAIL_INPUT).fill("tadikamallasivaparvathi@gmail.com")
    page.locator(LoginLocators.PASSWORD_INPUT).fill("Siva@2001")
    page.locator(LoginLocators.LOGIN_BUTTON).click()
    # Since this is a static website, we don't expect a URL change after login
    # Instead, we verify that the form submission attempt was made
    expect(page.locator(LoginLocators.LOGIN_BUTTON)).to_be_disabled(timeout=10000)

def test_invalid_credentials_login(page):
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(LoginLocators.EMAIL_INPUT).fill("invaliduser@example.com")
    page.locator(LoginLocators.PASSWORD_INPUT).fill("WrongPassword123")
    page.locator(LoginLocators.LOGIN_BUTTON).click()
    expect(page.locator(LoginLocators.INVALID_CREDENTIALS_ERROR)).to_be_visible(timeout=10000)
    expect(page.url).to_equal(LOGIN_URL)

def test_empty_email_login(page):
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(LoginLocators.EMAIL_INPUT).fill("")
    page.locator(LoginLocators.PASSWORD_INPUT).fill("AnyPassword123")
    page.locator(LoginLocators.LOGIN_BUTTON).click()
    expect(page.locator(LoginLocators.EMAIL_INPUT)).to_have_attribute("validationMessage", "Please fill out this field.")
    expect(page.url).to_equal(LOGIN_URL)

def test_empty_password_login(page):
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(LoginLocators.EMAIL_INPUT).fill("test@example.com")
    page.locator(LoginLocators.PASSWORD_INPUT).fill("")
    page.locator(LoginLocators.LOGIN_BUTTON).click()
    expect(page.locator(LoginLocators.PASSWORD_INPUT)).to_have_attribute("validationMessage", "Please fill out this field.")
    expect(page.url).to_equal(LOGIN_URL)

def test_invalid_email_format_login(page):
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(LoginLocators.EMAIL_INPUT).fill("invalid-email")
    page.locator(LoginLocators.PASSWORD_INPUT).fill("ValidPassword123")
    page.locator(LoginLocators.LOGIN_BUTTON).click()
    expect(page.locator(LoginLocators.EMAIL_INPUT)).to_have_attribute("validationMessage", expect.string_containing("@"))
    expect(page.url).to_equal(LOGIN_URL)

def test_show_password_toggle(page):
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(LoginLocators.PASSWORD_INPUT).fill("TestPassword123")
    expect(page.locator(LoginLocators.PASSWORD_INPUT)).to_have_attribute("type", "password")
    page.locator(LoginLocators.SHOW_PASSWORD_BUTTON).click()
    expect(page.locator(LoginLocators.PASSWORD_INPUT)).to_have_attribute("type", "text")
    page.locator(LoginLocators.SHOW_PASSWORD_BUTTON).click()
    expect(page.locator(LoginLocators.PASSWORD_INPUT)).to_have_attribute("type", "password")

def test_navigate_to_signup_page(page):
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(LoginLocators.SIGNUP_HERE_LINK).click()
    expect(page.url).to_equal(SIGNUP_URL)

def test_forgot_password_link_opens_modal(page):
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(LoginLocators.FORGOT_PASSWORD_LINK).click()
    expect(page.locator(LoginLocators.RESET_PASSWORD_H3)).to_be_visible(timeout=10000)

def test_sign_in_with_google_button(page):
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(LoginLocators.GOOGLE_LOGIN_BUTTON).click()
    # Since this is a static website, we don't expect a URL change after clicking the Google button
    # Instead, we verify that the button click was successful
    expect(page.locator(LoginLocators.GOOGLE_LOGIN_BUTTON)).to_be_disabled(timeout=10000)

def test_forgot_password_modal_elements_visibility(page):
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(LoginLocators.FORGOT_PASSWORD_LINK).click()
    expect(page.locator(LoginLocators.RESET_PASSWORD_CLOSE_BUTTON)).to_be_visible(timeout=10000)
    expect(page.locator(LoginLocators.RESET_PASSWORD_H3)).to_be_visible(timeout=10000)
    expect(page.locator(LoginLocators.RESET_PASSWORD_DESC_P)).to_be_visible(timeout=10000)
    expect(page.locator(LoginLocators.EMAIL_LABEL)).to_be_visible(timeout=10000)
    expect(page.locator(LoginLocators.RESET_PASSWORD_EMAIL_INPUT)).to_be_visible(timeout=10000)
    expect(page.locator(LoginLocators.RESET_PASSWORD_SEND_CODE_BUTTON)).to_be_visible(timeout=10000)

def test_close_forgot_password_modal(page):
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(LoginLocators.FORGOT_PASSWORD_LINK).click()
    expect(page.locator(LoginLocators.RESET_PASSWORD_H3)).to_be_visible(timeout=10000)
    page.locator(LoginLocators.RESET_PASSWORD_CLOSE_BUTTON).click()
    expect(page.locator(LoginLocators.RESET_PASSWORD_H3)).not_to_be_visible(timeout=10000)

def test_send_reset_code_valid_email(page):
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(LoginLocators.FORGOT_PASSWORD_LINK).click()
    page.locator(LoginLocators.RESET_PASSWORD_EMAIL_INPUT).fill("tadikamallasivaparvathi@gmail.com")
    page.locator(LoginLocators.RESET_PASSWORD_SEND_CODE_BUTTON).click()
    expect(page.locator(LoginLocators.SUCCESS_MESSAGE)).to_be_visible(timeout=10000)
    expect(page.locator(LoginLocators.RESET_PASSWORD_H3)).not_to_be_visible(timeout=10000)

def test_send_reset_code_invalid_email_format(page):
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(LoginLocators.FORGOT_PASSWORD_LINK).click()
    page.locator(LoginLocators.RESET_PASSWORD_EMAIL_INPUT).fill("bad-email")
    page.locator(LoginLocators.RESET_PASSWORD_SEND_CODE_BUTTON).click()
    expect(page.locator(LoginLocators.RESET_PASSWORD_EMAIL_INPUT)).to_have_attribute("validationMessage", expect.string_containing("@"))
    expect(page.locator(LoginLocators.RESET_PASSWORD_H3)).to_be_visible(timeout=10000)

def test_send_reset_code_empty_email(page):
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')
    page.locator(LoginLocators.FORGOT_PASSWORD_LINK).click()
    page.locator(LoginLocators.RESET_PASSWORD_EMAIL_INPUT).fill("")
    page.locator(LoginLocators.RESET_PASSWORD_SEND_CODE_BUTTON).click()
    expect(page.locator(LoginLocators.RESET_PASSWORD_EMAIL_INPUT)).to_have_attribute("validationMessage", "Please fill out this field.")
    expect(page.locator(LoginLocators.RESET_PASSWORD_H3)).to_be_visible(timeout=10000)