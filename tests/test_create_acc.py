import uuid
from pages.create_account_page import CreateAccountPage
import allure
from selenium.webdriver.support.ui import WebDriverWait


@allure.epic("Пользовательский аккаунт")
@allure.feature("Регистрация")
@allure.severity(allure.severity_level.CRITICAL)
def test_successful_registration(driver, base_url):
    registration_page = CreateAccountPage(driver, base_url)

    with allure.step("Открыть страницу регистрации /registration"):
        registration_page.open("/registration")

    with allure.step("Сгенерировать уникальный email для регистрации"):
        unique_email = f"test_user_{uuid.uuid4().hex[:8]}@example.com"
        allure.attach(unique_email, name="generated_email", attachment_type=allure.attachment_type.TEXT)

    with allure.step(f"Заполнить форму регистрации с email: {unique_email}"):
        registration_page.register_user(
            first_name="Petr",
            last_name="Ivanov",
            email=unique_email,
            password="Passsssword123!."
        )
        allure.attach(
            driver.get_screenshot_as_png(),
            name="form_filled",
            attachment_type=allure.attachment_type.PNG
        )
    with allure.step("Дождаться перенаправления на главную страницу"):
        expected_url = base_url.rstrip("/") + "/"
        WebDriverWait(driver, 10).until(lambda d: d.current_url == expected_url)

    assert driver.current_url == expected_url, \
        f"Регистрация не удалась. Текущий URL: {driver.current_url}, ожидался: {expected_url}"

    with allure.step("Завершение теста: пользователь успешно зарегистрирован"):
        allure.attach(
            f"Пользователь {unique_email} успешно зарегистрирован",
            name="test_result",
            attachment_type=allure.attachment_type.TEXT
        )