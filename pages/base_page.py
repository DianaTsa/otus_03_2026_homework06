from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    DEFAULT_TIMEOUT = 10
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def open(self, path="/"):
        self.driver.get(self.base_url.rstrip("/") + path)

    def wait_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_all_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_all_elements_located(locator)
        )

    def wait_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def click(self, locator):
        self.wait_clickable(locator).click()

    def input(self, locator, text):
        element = self.wait_visible(locator)
        element.clear()
        element.send_keys(text)

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