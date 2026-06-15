import allure
from pages.catalog_page import CatalogPage


@allure.epic("Каталог")
@allure.feature("Просмотр")
@allure.story("Отображение страницы каталога")
@allure.severity(allure.severity_level.NORMAL)
def test_catalog_page(driver, base_url):
    page = CatalogPage(driver, base_url)

    with allure.step("Открыть страницу каталога"):
        page.open("/brand/2-graphic-corner")
        allure.attach(
            driver.get_screenshot_as_png(),
            name="catalog_page_opened",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step("проверка элементов страницы"):
        page.check_elements()
        allure.attach(
            driver.get_screenshot_as_png(),
            name="elements_checked",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step("Получить список товаров в каталоге"):
        products = page.get_product_list()

    with allure.step(f"Проверить, что в каталоге есть хотя бы один товар (найдено: {len(products)})"):
        assert len(products) > 0
        allure.attach(driver.get_screenshot_as_png(),
                      attachment_type=allure.attachment_type.PNG)