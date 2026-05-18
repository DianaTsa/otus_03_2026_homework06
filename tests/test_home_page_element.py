from selenium.webdriver.common.by import By
from pages.base_page import BasePage

def test_home_page_elements(driver, base_url):
    page = BasePage(driver, base_url)
    page.open("/")

    page.wait_visible((By.CSS_SELECTOR, "#_desktop_logo"))
    page.wait_visible((By.CSS_SELECTOR, "#search_widget"))
    page.wait_visible((By.CSS_SELECTOR, "#content"))
    page.wait_visible((By.CSS_SELECTOR, "#category-9"))
    page.wait_visible((By.XPATH, "//*[@id='content']/section[1]/a"))
    products = page.wait_all_visible((By.CSS_SELECTOR, "#content .product-miniature"))

    assert len(products) > 0, 'список товаров пуст'