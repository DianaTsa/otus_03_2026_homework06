from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure


class ProductPage(BasePage):
    CONTENT = (By.CSS_SELECTOR, "#content")
    SIZE_SELECT = (By.ID, "group_1")
    CURRENT_PRICE = (By.CLASS_NAME, "current-price-value")
    COMMENTS_HEADER = (By.CSS_SELECTOR, "#product-comments-list-header")
    CURRENCY_DROPDOWN = (
        By.CSS_SELECTOR,
        ".currency-selector .expand-more, #_desktop_currency_selector .expand-more",
    )
    USD_OPTION = (By.LINK_TEXT, "USD $")
    PRICE = (By.CSS_SELECTOR, ".price, .current-price span")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "button[data-button-action='add-to-cart']")

    @allure.step("Сменить валюту на USD")
    def change_currency(self):
        self.logger.info("Смена валюты на странице товара на USD")
        self.logger.debug("Открываем выпадающий список выбора валюты")
        self.click(self.CURRENCY_DROPDOWN)
        self.logger.debug("Выбираем пункт «USD $»")
        self.click(self.USD_OPTION)
        self.logger.info("Валюта переключена на USD")

    @allure.step("Получить цену товара")
    def get_price(self):
        price = self.wait_visible(self.PRICE).text
        self.logger.info(f"Текущая цена товара: «{price}»")
        return price

    @allure.step("Дождаться загрузки страницы товара")
    def wait_page_loaded(self):
        self.logger.info("Ожидание загрузки страницы товара")
        self.wait_visible(self.CONTENT)
        self.logger.debug("Контентный блок страницы товара отображён")

    @allure.step("Проверить отображение основных элементов карточки товара")
    def check_product_elements(self):
        self.logger.info("Проверка ключевых элементов карточки товара")
        self.logger.debug("Проверяем селектор размера")
        self.wait_visible(self.SIZE_SELECT)
        self.logger.debug("Проверяем блок текущей цены")
        self.wait_visible(self.CURRENT_PRICE)
        self.logger.debug("Проверяем кнопку - Добавить в корзину")
        self.wait_visible(self.ADD_TO_CART_BTN)
        self.logger.debug("Проверяем заголовок секции комментариев")
        self.wait_visible(self.COMMENTS_HEADER)
        self.logger.info("Все ключевые элементы карточки товара отображаются корректно")