from pages.admin_page import AdminPage
from selenium.webdriver.common.by import By

def test_admin_login_logout(driver, base_url):
    admin_page = AdminPage(driver, base_url)
    admin_page.open("/administration")

    admin_page.login("admin@example.com", "Admin123!")

    assert admin_page.wait_visible((By.CSS_SELECTOR, "#dashtrends"))

    admin_page.logout()

    assert admin_page.wait_visible(admin_page.EMAIL_INPUT)


