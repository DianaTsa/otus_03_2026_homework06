from selenium.webdriver.common.by import By
from pages.base_page import BasePage

def test_catalog_page(driver, base_url):
    page = BasePage(driver, base_url)
    page.open("/brand/2-graphic-corner")

    page.wait_visible((By.XPATH, "//*[@id='wrapper']/div/nav/ol/li[1]/a/span"))
    page.wait_visible((By.CSS_SELECTOR, "#_desktop_user_info"))
    page.wait_visible((By.ID, "_desktop_cart"))
    page.wait_visible((By.CSS_SELECTOR, "#search_widget"))
    page.wait_visible((By.CSS_SELECTOR, "#js-product-list-top"))
    products = page.wait_all_visible((By.CSS_SELECTOR, "#js-product-list .product-miniature"))

    assert len(products) > 0