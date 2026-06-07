from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure


class AuthPage(BasePage):
    LOGIN = (By.CSS_SELECTOR, "#submit-login")
    EMAIL = (By.CSS_SELECTOR, "#field-email")
    PSSWRD = (By.CSS_SELECTOR, "#field-password")
    FGT_PSSWRD = (By.CSS_SELECTOR, "#login-form > div > div.forgot-password")
    NO_ACC = (By.CSS_SELECTOR, "#content > div > a")

    @allure.step("Проверить наличие всех элементов формы авторизации")
    def check_auth_elements(self):
        self.logger.info("Проверка отображения элементов формы авторизации")

        self.logger.debug("Проверяем кнопку Войти")
        self.wait_visible(self.LOGIN)

        self.logger.debug("Проверяем поле Email")
        self.wait_visible(self.EMAIL)

        self.logger.debug("Проверяем поле Пароль")
        self.wait_visible(self.PSSWRD)

        self.logger.debug("Проверяем ссылку - Нет аккаунта")
        self.wait_visible(self.NO_ACC)

        self.logger.debug("Проверяем ссылку - Забыли пароль")
        self.wait_visible(self.FGT_PSSWRD)

        self.logger.info("Все элементы формы авторизации отображаются корректно")