import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_cart_from_home(driver, base_url):
    wait = WebDriverWait(driver, 10)
    driver.get(base_url)

    products = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content .product-miniature")))
    assert products, "На главной странице не найдено товаров"

    product = random.choice(products)

    link_locator = (By.CSS_SELECTOR, ".product-title a")
    link_element = product.find_element(*link_locator)
    product_name = link_element.text.strip()

    link_element.click()

    add_to_cart_locator = (By.CSS_SELECTOR, "button[data-button-action='add-to-cart']")
    wait.until(EC.element_to_be_clickable(add_to_cart_locator)).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#blockcart-modal .close"))).click()

    driver.get(base_url + "cart")

    cart_page_source = driver.page_source
    assert product_name.lower() in cart_page_source.lower(), f"Товар '{product_name}' не найден в корзине"