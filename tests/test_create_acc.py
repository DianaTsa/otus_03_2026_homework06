import uuid
from pages.create_account_page import CreateAccountPAge


def test_successful_registration(driver, base_url):
    registration_page = CreateAccountPAge(driver, base_url)
    registration_page.open("/registration")

    unique_email = f"test_user_{uuid.uuid4().hex[:8]}@example.com"

    registration_page.register_user(
        first_name="Petr",
        last_name="Ivanov",
        email=unique_email,
        password="Passsssword123!."
    )

    expected_url = base_url.rstrip("/") + "/"

    from selenium.webdriver.support.ui import WebDriverWait
    WebDriverWait(driver, 10).until(lambda d: d.current_url == expected_url)

    assert driver.current_url == expected_url, \
        f"Регистрация не удалась. Текущий URL: {driver.current_url}, ожидался: {expected_url}"