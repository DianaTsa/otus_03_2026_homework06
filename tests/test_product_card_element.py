from pages.product_page import ProductPage
import allure


@allure.epic("Магазин")
@allure.feature("Карточка товара")
@allure.story("Отображение элементов карточки товара")
@allure.severity(allure.severity_level.CRITICAL)
def test_product_card_elements(driver, base_url):
    page = ProductPage(driver, base_url)

    with allure.step("Открыть страницу товара '/women/2-9-brown-bear-printed-sweater.html#/1-size-s'"):
        page.open("/women/2-9-brown-bear-printed-sweater.html#/1-size-s")
        allure.attach(
            driver.get_screenshot_as_png(),
            name="product_page_opened",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step("Дождаться полной загрузки страницы"):
        page.wait_page_loaded()
        allure.attach(
            driver.get_screenshot_as_png(),
            name="page_loaded",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step("Проверить наличие всех обязательных элементов на карточке товара"):
        page.check_product_elements()
        allure.attach(
            driver.get_screenshot_as_png(),
            name="all_elements_checked",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step("Завершение теста: все элементы карточки товара отображаются корректно"):
        allure.attach(
            "Карточка товара успешно проверена, все элементы присутствуют",
            name="test_result",
            attachment_type=allure.attachment_type.TEXT
        )