from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure


class CreateAccountPage(BasePage):
    # Локаторы текстовых полей
    FIRSTNAME = (By.CSS_SELECTOR, "#field-firstname")
    LASTNAME = (By.CSS_SELECTOR, "#field-lastname")
    EMAIL = (By.CSS_SELECTOR, "#field-email")
    PASSWORD = (By.CSS_SELECTOR, "#field-password")

    # Локаторы чекбоксов
    PRIVACY_LABEL = (By.CSS_SELECTOR,
                     "#customer-form > div > div:nth-child(8) > div.col-md-6.js-input-column > span > label")
    DATA_PRIVACY_LABEL = (By.CSS_SELECTOR,
                          "#customer-form > div > div:nth-child(10) > div.col-md-6.js-input-column > span > label")

    # Кнопка сохранения
    SAVE_BUTTON = (By.CSS_SELECTOR, "#customer-form > footer > button")

    @allure.step("Зарегистрировать пользователя: {first_name} {last_name}, email={email}")
    def register_user(self, first_name, last_name, email, password):
        self.logger.info(
            f"Регистрация нового пользователя: {first_name} {last_name}, email={email}"
        )

        self.logger.debug("Заполняем поле «Имя»")
        self.input(self.FIRSTNAME, first_name)

        self.logger.debug("Заполняем поле «Фамилия»")
        self.input(self.LASTNAME, last_name)

        self.logger.debug("Заполняем поле «Email»")
        self.input(self.EMAIL, email)

        self.logger.debug("Заполняем поле «Пароль»")
        self.input(self.PASSWORD, password)

        self.logger.debug("Принимаем согласие на обработку персональных данных (Privacy)")
        self.click(self.PRIVACY_LABEL)

        self.logger.debug("Принимаем согласие на политику конфиденциальности (Data Privacy)")
        self.click(self.DATA_PRIVACY_LABEL)

        self.logger.info("Отправка формы регистрации")
        self.click(self.SAVE_BUTTON)

        self.logger.info(f"Форма регистрации отправлена для пользователя: {email}")