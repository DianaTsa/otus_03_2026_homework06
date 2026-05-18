from selenium.webdriver.common.by import By
from pages.base_page import BasePage

def test_product_card_elements(driver, base_url):
    page = BasePage(driver, base_url)
    page.open("/women/2-9-brown-bear-printed-sweater.html#/1-size-s")

    page.wait_visible((By.CSS_SELECTOR, "#content"))
    page.wait_visible((By.ID, "group_1"))
    page.wait_visible((By.XPATH, "//*[contains(normalize-space(.), 'Add to cart')]"))
    page.wait_visible((By.CLASS_NAME, "current-price-value"))
    page.wait_visible((By.CSS_SELECTOR, "#product-comments-list-header"))