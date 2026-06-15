from pathlib import Path
import pytest
import time
from pages.admin_page import AdminPage
from pages.admin_products_page import AdminProductsPage
import allure


@pytest.fixture
def product_image_path():
    current_dir = Path(__file__).parent
    image_path = current_dir / "test_data" /"product.png"

    assert image_path.exists(), f"изображение не найдено: {image_path}"
    return str(image_path)

DESCRIPTION = "Описание товара"

@allure.epic("Административная панель")
@allure.feature("Управление товарами")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_and_delete_product(driver, base_url, product_image_path):
    admin = AdminPage(driver, base_url)

    with allure.step("Открыть страницу админки"):
        admin.open("/administration")

    with allure.step("Выполнить вход в админку"):
        admin.login("admin@example.com", "Admin123!")

    products = AdminProductsPage(driver, base_url)

    with allure.step("Перейти в список товаров"):
        products.go_to_products_list()

    with allure.step("Проверить, что открыта страница управления товарами"):
        assert "sell/catalog/products" in driver.current_url

    product_name = f"TestProduct_{int(time.time())}"
    allure.attach(product_name, name="generated_product_name", attachment_type=allure.attachment_type.TEXT)

    with allure.step(f"Начать создание нового товара с названием '{product_name}'"):
        products.start_adding_standard_product()

    with allure.step("Заполнить название товара"):
        products.set_name(product_name)

    with allure.step("Загрузить изображение товара"):
        products.upload_product_image(product_image_path)
        allure.attach(product_image_path, name="image_path", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Заполнить описание товара"):
        products.set_description(DESCRIPTION)
        allure.attach(DESCRIPTION, name="product_description", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Сохранить созданный товар"):
        products.save_product()

    with allure.step("Проверить появление уведомления об успешном сохранении"):
        assert products.is_success_alert_visible(), "Уведомление об успешном сохранении не появилось"
        allure.attach(
            driver.get_screenshot_as_png(),
            name="product_saved_success",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step("Вернуться к списку товаров"):
        products.go_to_products_list()

    with allure.step(f"Выполнить поиск созданного товара по имени '{product_name}'"):
        products.search_product_by_name(product_name)

    with allure.step("Проверить, что товар отображается в списке"):
        assert products.is_product_present(product_name), f"Продукт '{product_name}' не найден"
        allure.attach(
            driver.get_screenshot_as_png(),
            name="product_found_in_list",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step(f"Удалить товар '{product_name}'"):
        products.delete_product_by_name(product_name)
        name, message = products.delete()
        allure.attach(message, name="delete_message", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверить успешность удаления"):
        assert "success" in message.lower() or "успеш" in message.lower(), \
            f"Нет сообщения об успешном удалении: {message!r}"

    with allure.step(f"Проверить, что товар '{product_name}' больше не отображается в списке"):
        products.search_product_by_name(product_name)
        assert not products.is_product_present(product_name), \
            f"Товар '{product_name}' всё ещё присутствует после удаления"
        allure.attach(
            driver.get_screenshot_as_png(),
            name="product_deleted_success",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step("Завершение теста: товар успешно создан и удален"):
        allure.attach(
            f"Товар '{product_name}' был создан и успешно удален",
            name="test_result",
            attachment_type=allure.attachment_type.TEXT
        )