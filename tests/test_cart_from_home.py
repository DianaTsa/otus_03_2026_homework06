import random

import allure

from pages.home_page import HomePage

@allure.epic('Каталог')
@allure.feature("Корзина")

@allure.title("Добавление случайного товара в корзину с главной страницы")
@allure.severity(allure.severity_level.CRITICAL)
def test_cart_from_home(driver, base_url):
    page = HomePage(driver, base_url)

    with allure.step("Открыть главную страницу"):
        page.open("")

    with allure.step("Получить список товаров на главной странице"):
        products = page.get_all_products()
        assert products, "нет товаров на главной странице"

    with allure.step("Выбрать случайный товар"):
        product = random.choice(products)
        product_name = page.click_product(product)

    with allure.step("Добавить товар в корзину"):
        page.add_to_cart()

    with allure.step("Закрыть модальное окно"):
        page.close_modal()

    with allure.step("Проверить наличие товара в корзине"):
        page.open("/cart")

    cart_page_source = driver.page_source
    assert product_name.lower() in cart_page_source.lower(), f"Товар '{product_name}' не найден в корзине"