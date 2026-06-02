from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class ProductPage(BasePage):
    CONTENT = (By.CSS_SELECTOR, "#content")
    SIZE_SELECT = (By.ID, "group_1")
    CURRENT_PRICE = (By.CLASS_NAME, "current-price-value")
    COMMENTS_HEADER = (By.CSS_SELECTOR, "#product-comments-list-header")
    CURRENCY_DROPDOWN =  (By.CSS_SELECTOR, ".currency-selector .expand-more, #_desktop_currency_selector .expand-more")
    USD_OPTION = (By.LINK_TEXT, "USD $")
    PRICE = (By.CSS_SELECTOR, ".price, .current-price span")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "button[data-button-action='add-to-cart']")

    def  change_currency(self):
        self.click(self.CURRENCY_DROPDOWN)
        self.click(self.USD_OPTION)

    def get_price(self):
        return self.wait_visible(self.PRICE).text

    def wait_page_loaded(self):
        self.wait_visible(self.CONTENT)

    def check_product_elements(self):
        self.wait_visible(self.SIZE_SELECT)
        self.wait_visible(self.CURRENT_PRICE)
        self.wait_visible(self.ADD_TO_CART_BTN)
        self.wait_visible(self.COMMENTS_HEADER)





