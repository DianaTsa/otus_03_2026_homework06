from pages.auth_page import AuthPage
import allure


@allure.epic("Магазин")
@allure.feature("Авторизация пользователя")
@allure.story("Страница авторизации")
@allure.severity(allure.severity_level.CRITICAL)
def test_user_auth_page_elements(driver, base_url):
    page = AuthPage(driver, base_url)

    with allure.step("Открыть страницу авторизации '/login'"):
        page.open("/login")
        allure.attach(
            driver.get_screenshot_as_png(),
            name="auth_page_opened",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step("Проверить наличие всех обязательных элементов на странице авторизации"):
        page.check_auth_elements()
        allure.attach(
            driver.get_screenshot_as_png(),
            name="auth_elements_checked",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step("Завершение теста: все элементы страницы авторизации отображаются корректно"):
        allure.attach(
            "Страница авторизации успешно проверена, все элементы присутствуют",
            name="test_result",
            attachment_type=allure.attachment_type.TEXT
        )
