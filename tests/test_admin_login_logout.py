from pages.admin_page import AdminPage
from selenium.webdriver.common.by import By
import allure


@allure.epic("Административная панель")
@allure.feature("Авторизация")
@allure.story("Логин и выход из системы")
@allure.title("Проверка успешного логина и логаута администратора")
@allure.severity(allure.severity_level.BLOCKER)

def test_admin_login_logout(driver, base_url):
    with allure.step("Открыть страницу административной панели"):
        admin_page = AdminPage(driver, base_url)
        admin_page.open("/administration")

    with allure.step("Выполнить вход с логином 'admin@example.com'"):
        admin_page.login("admin@example.com", "Admin123!")

    with allure.step("Проверить, что дашборд отображается после входа"):
        dashboard_visible = admin_page.wait_visible((By.CSS_SELECTOR, "#dashtrends"))
        assert dashboard_visible, "Дашборд не отображается после авторизации"
        allure.attach(
            driver.get_screenshot_as_png(),
            name="dashboard_after_login",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step("Выполнить выход из системы"):
        admin_page.logout()

    with allure.step("Проверить, что открыта страница входа после логаута"):
        login_form_visible = admin_page.wait_visible(admin_page.EMAIL_INPUT)
        assert login_form_visible, "Форма входа не отображается после выхода"
        allure.attach(
            driver.get_screenshot_as_png(),
            name="login_form_after_logout",
            attachment_type=allure.attachment_type.PNG
        )