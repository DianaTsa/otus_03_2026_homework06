from selenium.webdriver.common.by import By
from pages.base_page import BasePage

def test_admin_auth_page_elements(driver, base_url):
    page = BasePage(driver, base_url)
    page.open("/administration")

    page.wait_visible((By.ID, "submit_login"))
    page.wait_visible((By.CSS_SELECTOR, "#email"))
    page.wait_visible((By.CSS_SELECTOR, "#passwd"))
    page.wait_visible((By.ID, "stay_logged_in"))
    page.wait_visible((By.ID, "forgot-password-link"))
