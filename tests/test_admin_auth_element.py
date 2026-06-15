import allure
from pages.admin_page import AdminPage


@allure.epic("Админка")
@allure.feature("Авторизация")
@allure.title("Проверка элементов формы входа в админку")
@allure.severity(allure.severity_level.NORMAL)
def test_admin_auth_page_elements(driver, base_url):
    page = AdminPage(driver, base_url)

    with allure.step("Открыть страницу авторизации в админке"):
        page.open("/administration")

    with allure.step("Проверить элементы формы авторизации"):
        page.check_admin_elements()