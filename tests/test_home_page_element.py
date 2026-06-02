from pages.home_page import HomePage


def test_home_page_elements(driver, base_url):
    page = HomePage(driver, base_url)

    page.open("/")

    page.check_home_page_elements()
    products = page.get_product_list()

    assert len(products) > 0, 'список товаров пуст'