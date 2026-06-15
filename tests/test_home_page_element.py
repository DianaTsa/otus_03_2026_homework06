from pages.home_page import HomePage
import allure


@allure.epic("Магазин")
@allure.feature("Главная страница")
@allure.story("Отображение элементов главной страницы")
@allure.severity(allure.severity_level.CRITICAL)
def test_home_page_elements(driver, base_url):
    page = HomePage(driver, base_url)

    with allure.step("Открыть главную страницу магазина"):
        page.open("/")
        allure.attach(
            driver.get_screenshot_as_png(),
            name="home_page_opened",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step("Проверить наличие всех обязательных элементов на главной странице"):
        page.check_home_page_elements()
        allure.attach(
            driver.get_screenshot_as_png(),
            name="home_page_elements_checked",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step("Получить список товаров на главной странице"):
        products = page.get_product_list()
        allure.attach(
            str(len(products)),
            name="products_count",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step(f"Проверить, что список товаров не пуст (найдено товаров: {len(products)})"):
        assert len(products) > 0, f'Список товаров пуст. Ожидалось хотя бы 1 товар, получено: {len(products)}'
        allure.attach(
            driver.get_screenshot_as_png(),
            name="products_displayed",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step("Завершение теста: главная страница отображается корректно"):
        allure.attach(
            f"На главной странице отображается {len(products)} товаров",
            name="test_result",
            attachment_type=allure.attachment_type.TEXT
        )