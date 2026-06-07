from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CreateAccountPAge(BasePage):
    # Локаторы текстовых полей
    FIRSTNAME = (By.CSS_SELECTOR, "#field-firstname")
    LASTNAME = (By.CSS_SELECTOR, "#field-lastname")
    EMAIL = (By.CSS_SELECTOR, "#field-email")
    PASSWORD = (By.CSS_SELECTOR, "#field-password")

    # Локаторы чекбоксов (используем лейблы для надежного клика)
    PRIVACY_LABEL = (By.CSS_SELECTOR,
                     "#customer-form > div > div:nth-child(8) > div.col-md-6.js-input-column > span > label")
    DATA_PRIVACY_LABEL = (By.CSS_SELECTOR,
                          "#customer-form > div > div:nth-child(10) > div.col-md-6.js-input-column > span > label")

    # Кнопка сохранения
    SAVE_BUTTON = (By.CSS_SELECTOR, "#customer-form > footer > button")

    def register_user(self, first_name, last_name, email, password):
        self.input(self.FIRSTNAME, first_name)
        self.input(self.LASTNAME, last_name)
        self.input(self.EMAIL, email)
        self.input(self.PASSWORD, password)


        self.click(self.PRIVACY_LABEL)
        self.click(self.DATA_PRIVACY_LABEL)


        self.click(self.SAVE_BUTTON)