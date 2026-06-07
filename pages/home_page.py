from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class HomePage(BasePage):
    PRODUCT_MINIATURES = (By.CSS_SELECTOR, "#content .product-miniature")
    LINK = (By.CSS_SELECTOR, ".product-title a")
    ADD_TO_CART = (By.CSS_SELECTOR, "#add-to-cart-or-refresh > div.product-add-to-cart.js-product-add-to-cart > div > div.add > button")
    MODAL_CLOSE = (By.CSS_SELECTOR, "#blockcart-modal")
    DESKTOP_LOGO = (By.CSS_SELECTOR, "#_desktop_logo")
    SEARCH_WIDGET = (By.CSS_SELECTOR, "#search_widget")
    CONTENT = (By.CSS_SELECTOR, "#content")
    CATEGORY_9 = (By.CSS_SELECTOR, "#category-9")
    FIRST_SECTION_LINK = (By.XPATH, "//*[@id='content']/section[1]/a")
    CURRENCY_DROPDOWN_BTN = (By.CSS_SELECTOR, "#_desktop_currency_selector > div > button")
    CURRENCY_DROPDOWN_MENU = (By.CSS_SELECTOR, "#_desktop_currency_selector .dropdown-menu")
    CURRENT_CURRENCY_LABEL = (By.CSS_SELECTOR, "#_desktop_currency_selector .expand-more")


    def get_all_products(self):
        return self.wait_all_visible(self.PRODUCT_MINIATURES)

    def click_product(self, product_element):
        link = product_element.find_element(*self.LINK)
        name = link.text.strip()
        link.click()
        return name

    def close_modal(self):
        self.click(self.MODAL_CLOSE)

    def add_to_cart(self):
        self.click(self.ADD_TO_CART)

    def check_home_page_elements(self):
        self.wait_visible(self.SEARCH_WIDGET)
        self.wait_visible(self.CONTENT)
        self.wait_visible(self.CATEGORY_9)
        self.wait_visible(self.FIRST_SECTION_LINK)

    def get_product_list(self):
        return self.wait_all_visible(self.PRODUCT_MINIATURES)

    def _currency_option(self, code: str):
        return (
            By.XPATH,
            f"//div[@id='_desktop_currency_selector']"
            f"//a[contains(@class,'dropdown-item') and starts-with(normalize-space(.), '{code}')]",
        )

    def open_currency_menu(self):
        btn = self._wait().until(EC.element_to_be_clickable(self.CURRENCY_DROPDOWN_BTN))
        try:
            btn.click()
        except ElementClickInterceptedException:
            self._js_click(btn)
        self._wait().until(
            EC.visibility_of_element_located(self.CURRENCY_DROPDOWN_MENU)
        )

    def select_currency(self, code: str):
        self.open_currency_menu()
        option = self._wait().until(EC.element_to_be_clickable(self._currency_option(code)))
        old_label = self.driver.find_element(*self.CURRENT_CURRENCY_LABEL).text.strip()
        self._js_click(option)
        self._wait().until(
            lambda d: d.find_element(*self.CURRENT_CURRENCY_LABEL).text.strip() != old_label
        )

    def get_current_currency(self) -> str:
        el = self._wait().until(EC.visibility_of_element_located(self.CURRENT_CURRENCY_LABEL))
        return el.text.strip()

