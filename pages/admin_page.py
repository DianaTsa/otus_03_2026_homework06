from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class AdminPage(BasePage):
    EMAIL_INPUT = (By.CSS_SELECTOR, "#email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#passwd")
    LOGIN_BUTTON = (By.ID, "submit_login")
    AVATAR = (By.CSS_SELECTOR, "#employee_infos")
    LOGOUT_LINK = (By.ID, "header_logout")
    FGT_PWRD = (By.CSS_SELECTOR, "#forgot-password-link")
    LGGD_IN = (By.CSS_SELECTOR, "#remind-me > label")

    def login(self, email, password):
        self.input(self.EMAIL_INPUT, email)
        self.input(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def logout(self):
        self.click(self.AVATAR)
        self.click(self.LOGOUT_LINK)

    def check_admin_elements(self):
        self.wait_visible(self.EMAIL_INPUT)
        self.wait_visible(self.PASSWORD_INPUT)
        self.wait_visible(self.LOGIN_BUTTON)
        self.wait_visible(self.FGT_PWRD)
        self.wait_visible(self.LGGD_IN)


