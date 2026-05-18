from selenium.webdriver.common.by import By
from pages.base_page import BasePage

def test_user_auth_page_elements(driver, base_url):
    page = BasePage(driver, base_url)
    page.open("/login")

    page.wait_visible((By.CSS_SELECTOR, "button[data-action='show-password']"))
    page.wait_visible((By.CSS_SELECTOR, "#field-email"))
    page.wait_visible((By.CSS_SELECTOR, "#field-password"))
    page.wait_visible((By.CLASS_NAME, "no-account"))
    page.wait_visible((By.CLASS_NAME, "forgot-password"))