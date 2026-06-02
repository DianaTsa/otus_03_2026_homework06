import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchElementException,
    NoAlertPresentException,
)
from pages.base_page import BasePage


class AdminProductsPage(BasePage):
    DEFAULT_TIMEOUT = 15

    CLOSE_TOOLBAR = (By.CSS_SELECTOR, "a[id^='sfToolbarHideButton']")
    CATALOG_MENU = (By.CSS_SELECTOR, "#subtab-AdminCatalog > a > span")
    PRODUCTS_SUBMENU = (By.CSS_SELECTOR, "#subtab-AdminProducts > a")
    ADD_NEW_PRODUCT_BTN = (By.CSS_SELECTOR, "#page-header-desc-configuration-add")
    MODAL_STANDARD_PRODUCT = (By.ID, "create_product_create")
    FILE_INPUT = (By.CSS_SELECTOR, "#product-images-dropzone input[type='file']")
    DESCRIPTION_IFRAME = (By.CSS_SELECTOR, "#product_description_description_ifr")
    DESCRIPTION_BODY = (By.CSS_SELECTOR, "#tinymce")
    SAVE_BUTTON = (By.CSS_SELECTOR, "#product_footer_save")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert.alert-success")

    GRID_TABLE = (By.CSS_SELECTOR, "#product_grid_table")
    GRID_ROWS = (By.CSS_SELECTOR, "#product_grid_table > tbody > tr")
    PRODUCT_NAME_INPUT = (By.CSS_SELECTOR, "#product_name")
    SEARCH_BUTTON = (
        By.CSS_SELECTOR,
        "#product_grid_table > thead > tr.column-filters > td:nth-child(11) > button",
    )
    GRID_EMPTY_ROW = (
        By.CSS_SELECTOR,
        "#product_grid_table tbody tr.empty_row, "
        "#product_grid_table tbody tr.grid-table-empty-row",
    )
    MODAL_CONFIRM_DELETE = (
        By.CSS_SELECTOR,
        ".modal.show .btn-confirm-submit, "
        "#grid-confirm-modal .btn-confirm-submit, "
        ".modal.show button[type='submit']",
    )
    DELETE_SUCCESS_MESSAGE = (
        By.CSS_SELECTOR,
        "#main-div > div > div.alert.alert-success.d-print-none",
    )

    def _wait(self, timeout=None):
        return WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT)

    def _close_toolbar(self):
        try:
            toolbar = self.driver.find_element(*self.CLOSE_TOOLBAR)
            if toolbar.is_displayed():
                self.driver.execute_script("arguments[0].click();", toolbar)
        except Exception:
            pass

    def _js_click(self, locator_or_element):
        if isinstance(locator_or_element, tuple):
            element = self._wait().until(EC.presence_of_element_located(locator_or_element))
        else:
            element = locator_or_element
        self.driver.execute_script("arguments[0].click();", element)

    def go_to_products_list(self):
        self._close_toolbar()
        self.click(self.CATALOG_MENU)
        self.click(self.PRODUCTS_SUBMENU)
        self._wait().until(EC.url_contains("sell/catalog/products"))
        self._wait().until(EC.presence_of_element_located(self.GRID_TABLE))

    # ---------- добавление товара ----------
    def start_adding_standard_product(self):
        self.click(self.ADD_NEW_PRODUCT_BTN)
        self._js_click(self.MODAL_STANDARD_PRODUCT)
        self._wait().until(EC.presence_of_element_located(self.SAVE_BUTTON))

    def upload_product_image(self, file_path):
        file_input = self._wait().until(EC.presence_of_element_located(self.FILE_INPUT))
        self.driver.execute_script(
            "arguments[0].style.cssText='display:block!important;visibility:visible;opacity:1;';",
            file_input,
        )
        file_input.send_keys(file_path)

    def set_description(self, text):
        iframe = self._wait().until(EC.visibility_of_element_located(self.DESCRIPTION_IFRAME))
        self.driver.switch_to.frame(iframe)
        try:
            body = self._wait().until(EC.visibility_of_element_located(self.DESCRIPTION_BODY))
            body.clear()
            body.send_keys(text)
        finally:
            self.driver.switch_to.default_content()

    def save_product(self):
        self._close_toolbar()
        try:
            self.click(self.SAVE_BUTTON)
        except ElementClickInterceptedException:
            self._js_click(self.SAVE_BUTTON)

    def is_success_alert_visible(self) -> bool:
        try:
            self._wait().until(EC.visibility_of_element_located(self.SUCCESS_ALERT))
            return True
        except TimeoutException:
            return False

    def _get_data_rows(self):
        rows = self.driver.find_elements(*self.GRID_ROWS)
        data_rows = []
        for r in rows:
            cls = r.get_attribute("class") or ""
            if "empty_row" in cls or "grid-table-empty-row" in cls:
                continue
            if "column-filters" in cls or "column-headers" in cls:
                continue
            data_rows.append(r)
        return data_rows

    def pick_random_product(self):

        self._wait().until(EC.presence_of_element_located(self.GRID_TABLE))
        rows = self._get_data_rows()
        assert rows, "В таблице нет товаров для удаления"

        random.shuffle(rows)
        for row in rows:
            try:
                name_el = row.find_element(By.CSS_SELECTOR, "a.text-primary")
            except NoSuchElementException:
                continue
            index = self.driver.execute_script(
                "return Array.from(arguments[0].parentNode.children).indexOf(arguments[0]) + 1;",
                row,
            )
            return index, name_el.text.strip()

        raise AssertionError("Не нашлось ни одной строки с именем товара (a.text-primary)")

    def open_kebab_menu(self, row_index: int):
        kebab = (
            By.CSS_SELECTOR,
            f"#product_grid_table > tbody > tr:nth-child({row_index}) "
            f"> td.action-type.column-actions .dropdown-toggle",
        )
        el = self._wait().until(EC.element_to_be_clickable(kebab))
        try:
            el.click()
        except ElementClickInterceptedException:
            self._js_click(el)

    def click_delete_in_kebab(self, row_index: int):
        delete_link = (
            By.CSS_SELECTOR,
            f"#product_grid_table > tbody > tr:nth-child({row_index}) "
            f"> td.action-type.column-actions .grid-delete-row-link",
        )
        el = self._wait().until(EC.element_to_be_clickable(delete_link))
        self._js_click(el)

    def _accept_js_alert_if_any(self, timeout=2) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
            return True
        except (TimeoutException, NoAlertPresentException):
            return False

    def get_delete_success_message(self) -> str:
        el = self._wait().until(
            EC.visibility_of_element_located(self.DELETE_SUCCESS_MESSAGE)
        )
        return el.text.strip()

    def delete_product_by_name(self, name: str) -> tuple[str, str]:
        self.search_product_by_name(name)
        self.open_kebab_menu(index=0)
        self.click_delete_in_kebab(index=0)
        self.confirm_delete()
        message = self.get_delete_success_message()
        return name, message

    def search_product_by_name(self, name: str):
        self._close_toolbar()
        inp = self._wait().until(EC.visibility_of_element_located(self.PRODUCT_NAME_INPUT))
        inp.clear()
        inp.send_keys(name)
        self._js_click(self.SEARCH_BUTTON)
        self._wait().until(
            lambda d: d.find_elements(*self.GRID_EMPTY_ROW) or self._get_data_rows()
        )

    def is_product_present(self, name: str) -> bool:
        if self.driver.find_elements(*self.GRID_EMPTY_ROW):
            return False
        for row in self._get_data_rows():
            try:
                el = row.find_element(By.CSS_SELECTOR, "a.text-primary")
            except NoSuchElementException:
                continue
            if el.text.strip() == name.strip():
                return True
        return False