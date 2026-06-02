from pages.product_page import ProductPage
from selenium.webdriver.common.by import By

class CatalogPage(ProductPage):
    BREADCRUMB_HOME = (By.XPATH, "//*[@id='wrapper']/div/nav/ol/li[1]/a/span")
    DESKTOP_USER_INFO = (By.CSS_SELECTOR, "#_desktop_user_info")
    DESKTOP_CART = (By.ID, "_desktop_cart")
    SEARCH_WIDGET = (By.CSS_SELECTOR, "#search_widget")
    PRODUCT_LIST_TOP = (By.CSS_SELECTOR, "#js-product-list-top")
    PRODUCT_MINIATURES = (By.CSS_SELECTOR, "#js-product-list .product-miniature")

    def check_elements(self):
        self.wait_visible(self.BREADCRUMB_HOME)
        self.wait_visible(self.DESKTOP_CART)
        self.wait_visible(self.DESKTOP_USER_INFO)
        self.wait_visible(self.SEARCH_WIDGET)
        self.wait_visible(self.PRODUCT_LIST_TOP)
        self.wait_visible(self.PRODUCT_MINIATURES)

    def get_product_list(self):
        return self.wait_all_visible(self.PRODUCT_MINIATURES)