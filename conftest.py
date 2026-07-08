import os
import pytest
import logging
import allure
from selenium import webdriver
from pages.admin_products_page import AdminProductsPage
from pages.admin_page import AdminPage
from pages.home_page import HomePage

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--browser_version", action="store", default="128.0")
    parser.addoption("--base-url", action="store", default=None)
    parser.addoption("--executor", action="store", default="local")

@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url") or os.getenv("BASE_URL", "http://localhost:8081/")

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    version = request.config.getoption("--browser_version")
    executor = request.config.getoption("--executor")
    base_url = request.config.getoption("--base-url") or os.getenv("BASE_URL", "http://localhost:8081/")

    logger.info(f"Запуск браузера {browser} (версия: {version}) на исполнителе {executor}")
    logger.info(f"BASE_URL: {base_url}")

    if browser == "chrome":
        options = webdriver.ChromeOptions()
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
    elif browser == "edge":
        options = webdriver.EdgeOptions()
    else:
        raise ValueError(f"Браузер '{browser}' не поддерживается.")

    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if executor == "local":
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        logger.info("Запущен локальный Chrome")
    elif executor == "selenoid" or executor.startswith("http"):
        if executor == "selenoid":
            executor_url = "http://selenoid:4444/wd/hub"
        else:
            executor_url = executor

        options.set_capability("browserName", browser)
        options.set_capability("browserVersion", version)

        selenoid_options = {
            "enableVNC": True,
            "enableVideo": False,
            "enableLog": True,
            "sessionTimeout": "5m"
        }

        options.set_capability("selenoid:options", selenoid_options)

        logger.info(f"Подключение к Selenoid: {executor_url}")
        driver = webdriver.Remote(command_executor=executor_url, options=options)
    elif executor == "remote":
        selenium_url = os.getenv("SELENIUM_URL", "http://selenium:4444/wd/hub")
        options.set_capability("browserName", browser)
        options.set_capability("browserVersion", version)
        logger.info(f"Подключение к удаленному Selenium: {selenium_url}")
        driver = webdriver.Remote(command_executor=selenium_url, options=options)
    else:
        executor_url = f"http://{executor}:4444/wd/hub"
        options.set_capability("browserName", browser)
        options.set_capability("browserVersion", version)
        selenoid_options = {"enableVNC": True, "enableVideo": False}
        options.set_capability("selenoid:options", selenoid_options)
        logger.info(f"Подключение к кастомному исполнителю: {executor_url}")
        driver = webdriver.Remote(command_executor=executor_url, options=options)

    driver.maximize_window()
    yield driver
    logger.info("Закрытие браузера")
    try:
        driver.quit()
    except Exception as e:
        logger.error(f"Ошибка при закрытии драйвера: {e}")

@pytest.fixture
def admin_products_page(driver, base_url):
    logger.info("Логинимся в админку")
    admin = AdminPage(driver, base_url)
    admin.open("/administration")
    admin.login("admin@example.com", "Admin123!")
    return AdminProductsPage(driver, base_url)

@pytest.fixture
def home_page(driver, base_url):
    return HomePage(driver, base_url)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        try:
            if "driver" in item.fixturenames:
                web_driver = item.funcargs["driver"]
                screenshot = web_driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="screenshot_on_failure",
                    attachment_type=allure.attachment_type.PNG,
                )
                logger.error(f"Тест упал. Скриншот прикреплен к отчету Allure. Тест: {item.nodeid}")
        except Exception as e:
            logger.error(f"Не удалось сделать скриншот: {e}")