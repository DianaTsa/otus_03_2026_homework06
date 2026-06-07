from pages.product_page import ProductPage
import allure


@allure.epic("Магазин")
@allure.feature("Валюта")
@allure.severity(allure.severity_level.CRITICAL)
def test_currency_changes_on_product_card(driver, base_url):
    page = ProductPage(driver, base_url)

    with allure.step("Открыть главную страницу магазина"):
        page.open("/")

    with allure.step("Перейти к карточке товара и получить цену до переключения валюты"):
        price_before = page.get_price()

    with allure.step("Переключить валюту на другую (USD)"):
        page.change_currency()


    with allure.step("Получить цену товара после переключения валюты"):
        price_after = page.get_price()
        allure.attach(price_after, name="price_after_currency_change", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверить, что цена изменилась после смены валюты"):
        assert price_before != price_after, "Цена на карточке товара не изменилась"

    with allure.step("Проверить, что после переключения отображается валюта USD"):
        assert "$" in price_after, "Валюта не USD"





