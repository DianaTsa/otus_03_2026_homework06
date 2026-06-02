from pages.auth_page import AuthPage

def test_user_auth_page_elements(driver, base_url):
    page = AuthPage(driver, base_url)
    page.open("/login")

    page.check_auth_elements()