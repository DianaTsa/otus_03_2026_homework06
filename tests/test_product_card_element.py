
from pages.product_page import ProductPage

def test_product_card_elements(driver, base_url):
    page = ProductPage(driver, base_url)
    page.open("/women/2-9-brown-bear-printed-sweater.html#/1-size-s")

    page.wait_page_loaded()
    page.check_product_elements()
