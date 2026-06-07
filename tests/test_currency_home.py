from pages.product_page import ProductPage

def test_currency_changes_on_product_card(driver, base_url):
    page = ProductPage(driver, base_url)
    page.open("/")

    price_before = page.get_price()

    page.change_currency()

    price_after = page.get_price()

    assert price_before != price_after, "Цена на карточке товара не изменилась"
    assert "$" in price_after, "Валюта не USD"





