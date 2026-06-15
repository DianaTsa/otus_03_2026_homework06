import logging
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    DEFAULT_TIMEOUT = 10

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.logger = logging.getLogger(self.__class__.__name__)

    @allure.step("Открыть страницу {path}")
    def open(self, path="/"):
        url = self.base_url.rstrip("/") + path
        self.logger.info(f"лОткрытие URL: {url}")
        self.driver.get(url)

    def wait_visible(self, locator, timeout=10):
        self.logger.debug(f"ожидание видимости {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_all_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_all_elements_located(locator)
        )

    def wait_clickable(self, locator, timeout=10):
        self.logger.debug(f"Ожидание кликабельности {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    @allure.step("Клик по элементу {locator}")
    def click(self, locator):
        self.logger.info(f"Клик по {locator}")
        self.wait_clickable(locator).click()

    @allure.step("Ввод текста в {locator}")
    def input(self, locator, text):
        self.logger.info(f"Ввод текста {locator}")
        element = self.wait_visible(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Клик по элементу {locator_or_element}")
    def _js_click(self, locator_or_element):
        if isinstance(locator_or_element, tuple):
            element = self._wait().until(
                EC.presence_of_element_located(locator_or_element)
            )
        else:
            element = locator_or_element

        self.driver.execute_script("arguments[0].click();", element)

    def _wait(self, timeout=None):
        return WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT)