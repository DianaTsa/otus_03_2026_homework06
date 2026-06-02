from pages.catalog_page import CatalogPage


def test_catalog_page(driver, base_url):
    page = CatalogPage(driver, base_url)
    page.open("/brand/2-graphic-corner")

    page.check_elements()
    products = page.get_product_list()

    assert len(products) > 0