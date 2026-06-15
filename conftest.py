import pytest
from selenium import webdriver
from pages.admin_products_page import AdminProductsPage
from pages.admin_page import AdminPage
from pages.home_page import HomePage
import logging
import allure

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="Supported browsers: chrome, edge")
    parser.addoption(
        "--base-url", action="store", default="http://localhost:8081/", help="Base URL of the application")


def create_driver(browser_name):
    global driver
    browsers = {
        "chrome": (webdriver.ChromeOptions, webdriver.Chrome),
        "edge": (webdriver.EdgeOptions, webdriver.Edge)
    }

    if browser_name not in browsers:
        raise ValueError(f"Браузер '{browser_name}' не поддерживается.")

    options_class, driver_class = browsers[browser_name]
    options = options_class()

    if browser_name == "chrome":
        options.add_argument("--start-maximized")
        driver = driver_class(options=options)

    if browser_name == "edge":
        driver = driver_class(options=options)
        driver.maximize_window()

    return driver


@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url")


@pytest.fixture
def driver(request):
    logger.info("Запуск браузера")
    browser_name = request.config.getoption("--browser").lower()
    driver = create_driver(browser_name)

    yield driver
    logger.info("Закрытие браузера")
    driver.quit()


@pytest.fixture
def admin_products_page(driver, base_url):
    logger.info("логинимся в админку")
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

    if rep.when == 'call' and rep.failed:
        try:
            if 'driver' in item.fixturenames:
                web_driver = item.funcargs['driver']
                allure.attach(
                    web_driver.get_screenshot_as_png(),
                    name="screenshot_on_failure",
                    attachment_type=allure.attachment_type.PNG
                )
                logger.error(f"Тест упал. Скриншот прикреплен к отчету Allure. Тест: {item.nodeid}")
        except Exception as e:
            logger.error(f"Не удалось сделать скриншот: {e}")