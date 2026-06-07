from pages.catalog_page import CatalogPage
import allure

@allure.epic("Магазин")
@allure.feature("Валюта")
@allure.story("Отображение цен в карточке товара")
@allure.severity(allure.severity_level.CRITICAL)
def test_currency_changes_on_product_card(driver, base_url):
    page = CatalogPage(driver, base_url)

    with allure.step("Открыть страницу каталога '/3-clothes'"):
        page.open("/3-clothes")

    with allure.step("Получить цену товара до переключения валюты"):
        price_before = page.get_price()
        allure.attach(price_before, name="price_before_currency_change", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Переключить валюту на другую (USD)"):
        page.change_currency()
        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_currency_change",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step("Проверить, что цена изменилась после смены валюты"):
        price_after = page.get_price()

    with allure.step("Проверить, что после переключения отображается валюта USD"):
        assert price_before != price_after, "Цена на карточке товара не изменилась после переключения валюты"

    with allure.step("Завершение теста: валюта в карточке товара корректно изменяется"):
        assert "$" in price_after, "После переключения валюта не стала USD"

