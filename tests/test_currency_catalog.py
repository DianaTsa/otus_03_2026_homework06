from pages.catalog_page import CatalogPage


def test_currency_changes_on_product_card(driver, base_url):
    page = CatalogPage(driver, base_url)
    page.open("/3-clothes")


    price_before = page.get_price()
    page.change_currency()
    price_after = page.get_price()
    assert price_before != price_after, "Цена на карточке товара не изменилась после переключения валюты"
    assert "$" in price_after, "После переключения валюта не стала USD"