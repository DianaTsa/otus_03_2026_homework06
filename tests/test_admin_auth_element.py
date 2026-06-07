from pages.admin_page import AdminPage

def test_admin_auth_page_elements(driver, base_url):
    page = AdminPage(driver, base_url)
    page.open("/administration")

    page.check_admin_elements()
