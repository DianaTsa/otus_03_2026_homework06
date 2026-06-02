import random
from pages.home_page import HomePage

def test_cart_from_home(driver, base_url):
    page = HomePage(driver, base_url)
    page.open("")

    products = page.get_all_products()
    assert products, "нет товаров на главной странице"
    product = random.choice(products)

    product_name = page.click_product(product)

    page.add_to_cart()
    page.close_modal()
    page.open("/cart")

    cart_page_source = driver.page_source
    assert product_name.lower() in cart_page_source.lower(), f"Товар '{product_name}' не найден в корзине"