from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class AuthPage(BasePage):
    LOGIN = (By.CSS_SELECTOR, "#submit-login")
    EMAIL = (By.CSS_SELECTOR, "#field-email")
    PSSWRD = (By.CSS_SELECTOR, "#field-password")
    FGT_PSSWRD = (By.CSS_SELECTOR, "#login-form > div > div.forgot-password")
    NO_ACC = (By.CSS_SELECTOR, "#content > div > a")

    def check_auth_elements(self):
        self.wait_visible(self.LOGIN)
        self.wait_visible(self.EMAIL)
        self.wait_visible(self.PSSWRD)
        self.wait_visible(self.NO_ACC)
        self.wait_visible(self.FGT_PSSWRD)