from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure


class HomePage(BasePage):
    PRODUCT_MINIATURES = (By.CSS_SELECTOR, "#content .product-miniature")
    LINK = (By.CSS_SELECTOR, ".product-title a")
    ADD_TO_CART = (
        By.CSS_SELECTOR,
        "#add-to-cart-or-refresh > div.product-add-to-cart.js-product-add-to-cart > div > div.add > button",
    )
    MODAL_CLOSE = (By.CSS_SELECTOR, "#blockcart-modal")
    DESKTOP_LOGO = (By.CSS_SELECTOR, "#_desktop_logo")
    SEARCH_WIDGET = (By.CSS_SELECTOR, "#search_widget")
    CONTENT = (By.CSS_SELECTOR, "#content")
    CATEGORY_9 = (By.CSS_SELECTOR, "#category-9")
    FIRST_SECTION_LINK = (By.XPATH, "//*[@id='content']/section[1]/a")
    CURRENCY_DROPDOWN_BTN = (By.CSS_SELECTOR, "#_desktop_currency_selector > div > button")
    CURRENCY_DROPDOWN_MENU = (By.CSS_SELECTOR, "#_desktop_currency_selector .dropdown-menu")
    CURRENT_CURRENCY_LABEL = (By.CSS_SELECTOR, "#_desktop_currency_selector .expand-more")

    @allure.step("Получить список всех товаров на главной")
    def get_all_products(self):
        self.logger.info("Получение списка миниатюр товаров на главной странице")
        products = self.wait_all_visible(self.PRODUCT_MINIATURES)
        self.logger.info(f"Найдено товаров на главной: {len(products)}")
        return products

    @allure.step("Кликнуть по товару и получить его название")
    def click_product(self, product_element):
        link = product_element.find_element(*self.LINK)
        name = link.text.strip()
        self.logger.info(f"Переход на карточку товара: «{name}»")
        link.click()
        return name

    @allure.step("Закрыть модальное окно корзины")
    def close_modal(self):
        self.logger.info("Закрываем модальное окно «Товар добавлен в корзину»")
        self.click(self.MODAL_CLOSE)

    @allure.step("Добавить товар в корзину")
    def add_to_cart(self):
        self.logger.info("Нажимаем кнопку «Добавить в корзину»")
        self.click(self.ADD_TO_CART)

    @allure.step("Проверить отображение основных элементов главной страницы")
    def check_home_page_elements(self):
        self.logger.info("Проверка отображения ключевых элементов главной страницы")
        self.logger.debug("Проверяем виджет поиска")
        self.wait_visible(self.SEARCH_WIDGET)
        self.logger.debug("Проверяем основной контентный блок")
        self.wait_visible(self.CONTENT)
        self.logger.debug("Проверяем блок категории #category-9")
        self.wait_visible(self.CATEGORY_9)
        self.logger.debug("Проверяем ссылку первой секции контента")
        self.wait_visible(self.FIRST_SECTION_LINK)
        self.logger.info("Все ключевые элементы главной страницы отображаются корректно")

    @allure.step("Получить список товаров главной страницы")
    def get_product_list(self):
        self.logger.info("Получение списка товаров главной страницы")
        products = self.wait_all_visible(self.PRODUCT_MINIATURES)
        self.logger.info(f"Получено товаров: {len(products)}")
        return products

    def _currency_option(self, code: str):
        return (
            By.XPATH,
            f"//div[@id='_desktop_currency_selector']"
            f"//a[contains(@class,'dropdown-item') and starts-with(normalize-space(.), '{code}')]",
        )

    @allure.step("Открыть меню выбора валюты")
    def open_currency_menu(self):
        self.logger.info("Открытие выпадающего меню выбора валюты")
        btn = self._wait().until(EC.element_to_be_clickable(self.CURRENCY_DROPDOWN_BTN))
        try:
            btn.click()
        except ElementClickInterceptedException:
            self.logger.warning("Клик по кнопке валюты перехвачен — используем JS-клик")
            self._js_click(btn)
        self._wait().until(
            EC.visibility_of_element_located(self.CURRENCY_DROPDOWN_MENU)
        )
        self.logger.debug("Меню выбора валюты открыто")

    @allure.step("Выбрать валюту: {code}")
    def select_currency(self, code: str):
        self.logger.info(f"Смена валюты на: {code}")
        self.open_currency_menu()
        option = self._wait().until(EC.element_to_be_clickable(self._currency_option(code)))
        old_label = self.driver.find_element(*self.CURRENT_CURRENCY_LABEL).text.strip()
        self.logger.debug(f"Текущая валюта до смены: «{old_label}»")
        self._js_click(option)
        self._wait().until(
            lambda d: d.find_element(*self.CURRENT_CURRENCY_LABEL).text.strip() != old_label
        )
        new_label = self.driver.find_element(*self.CURRENT_CURRENCY_LABEL).text.strip()
        self.logger.info(f"Валюта успешно изменена: «{old_label}» → «{new_label}»")

    @allure.step("Получить текущую валюту сайта")
    def get_current_currency(self) -> str:
        el = self._wait().until(EC.visibility_of_element_located(self.CURRENT_CURRENCY_LABEL))
        current = el.text.strip()
        self.logger.info(f"Текущая валюта на сайте: «{current}»")
        return current