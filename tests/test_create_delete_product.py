from pathlib import Path
import pytest
import time
from pages.admin_page import AdminPage
from pages.admin_products_page import AdminProductsPage


@pytest.fixture
def product_image_path():
    current_dir = Path(__file__).parent
    image_path = current_dir / "test_data" /"product.png"

    assert image_path.exists(), f"изображение не найдено: {image_path}"
    return str(image_path)

description = "Описание товара"


def test_create_and_delete_product(driver, base_url, product_image_path):
    admin = AdminPage(driver, base_url)
    admin.open("/administration")
    admin.login("admin@example.com", "Admin123!")

    products = AdminProductsPage(driver, base_url)
    products.go_to_products_list()
    assert "sell/catalog/products" in driver.current_url

    product_name = f"TestProduct_{int(time.time())}"

    products.start_adding_standard_product()
    products.set_name(product_name)
    products.upload_product_image(product_image_path)
    products.set_description(description)
    products.save_product()

    assert products.is_success_alert_visible(), "Уведомление об успешном сохранении не появилось"

    products.go_to_products_list()
    products.search_product_by_name(product_name)
    assert products.is_product_present(product_name), f"Продукт '{product_name}' не найден"

    products.delete_product_by_name(product_name)
    name, message = products.delete()
    assert "success" in message.lower() or "успеш" in message.lower(), f"Нет сообщения об успешном удалении: {message!r}"

    products.search_product_by_name(product_name)
    assert not products.is_product_present(product_name), f"Товар '{product_name}' всё ещё присутствует"