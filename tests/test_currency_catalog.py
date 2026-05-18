from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_currency_changes_on_product_card(driver, base_url):
    wait = WebDriverWait(driver, 10)
    driver.get(base_url + "3-clothes")

    price_locator = (By.CSS_SELECTOR, ".price, .current-price span")
    currency_dropdown = (By.CSS_SELECTOR, ".currency-selector .expand-more, #_desktop_currency_selector .expand-more")
    euro_option = (By.LINK_TEXT, "USD $")

    price_before = wait.until(EC.visibility_of_element_located(price_locator)).text.strip()

    wait.until(EC.element_to_be_clickable(currency_dropdown)).click()

    wait.until(EC.element_to_be_clickable(euro_option)).click()

    price_after = wait.until(EC.visibility_of_element_located(price_locator)).text.strip()

    assert price_before != price_after, "Цена на карточке товара не изменилась после переключения валюты"
    assert "$" in price_after, "После переключения валюта не стала USD"