from pages.product_page import ProductPage
from selenium.webdriver.common.by import By
import allure


class CatalogPage(ProductPage):
    BREADCRUMB_HOME = (By.XPATH, "//*[@id='wrapper']/div/nav/ol/li[1]/a/span")
    DESKTOP_USER_INFO = (By.CSS_SELECTOR, "#_desktop_user_info")
    DESKTOP_CART = (By.ID, "_desktop_cart")
    SEARCH_WIDGET = (By.CSS_SELECTOR, "#search_widget")
    PRODUCT_LIST_TOP = (By.CSS_SELECTOR, "#js-product-list-top")
    PRODUCT_MINIATURES = (By.CSS_SELECTOR, "#js-product-list .product-miniature")

    @allure.step("Проверить наличие основных элементов страницы каталога")
    def check_elements(self):
        self.logger.info("Проверка отображения элементов страницы каталога")

        self.logger.debug("Проверяем хлебные крошки (Home)")
        self.wait_visible(self.BREADCRUMB_HOME)

        self.logger.debug("Проверяем иконку корзины")
        self.wait_visible(self.DESKTOP_CART)

        self.logger.debug("Проверяем блок информации о пользователе")
        self.wait_visible(self.DESKTOP_USER_INFO)

        self.logger.debug("Проверяем виджет поиска")
        self.wait_visible(self.SEARCH_WIDGET)

        self.logger.debug("Проверяем верхнюю панель списка товаров")
        self.wait_visible(self.PRODUCT_LIST_TOP)

        self.logger.debug("Проверяем миниатюры товаров")
        self.wait_visible(self.PRODUCT_MINIATURES)

        self.logger.info("Все основные элементы каталога отображаются корректно")

    @allure.step("Получить список товаров каталога")
    def get_product_list(self):
        self.logger.info("Получение списка миниатюр товаров на странице каталога")
        products = self.wait_all_visible(self.PRODUCT_MINIATURES)
        self.logger.info(f"Найдено товаров на странице: {len(products)}")
        return products