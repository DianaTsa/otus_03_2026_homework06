import pytest
from selenium import webdriver
from pages.admin_products_page import AdminProductsPage
from pages.admin_page import AdminPage
from pages.home_page import HomePage


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Supported browsers: chrome, edge")
    parser.addoption("--base-url", action="store", default="http://localhost:8081/", help="Base URL of the application")


def create_driver(browser_name):
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
        driver.maximize_window()

    return driver


@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url")


@pytest.fixture
def driver(request):
    browser_name = request.config.getoption("--browser").lower()
    driver = create_driver(browser_name)

    yield driver

    driver.quit()

@pytest.fixture
def admin_products_page(driver, base_url):
    # логинимся в админку
    admin = AdminPage(driver, base_url)
    admin.open("/administration")
    admin.login("admin@example.com", "Admin123!")

    # возвращаем готовую страницу товаров
    return AdminProductsPage(driver, base_url)

@pytest.fixture
def home_page(driver, base_url):
    return HomePage(driver, base_url)