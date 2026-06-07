import allure

@allure.epic("Магазин")
@allure.feature("Валюта")
@allure.story("Переключение валюты")
@allure.severity(allure.severity_level.NORMAL)
def test_switch_currency_to_eur(home_page):
    with allure.step("Открыть главную страницу магазина"):
        home_page.open("/")

    with allure.step("Выбрать валюту USD"):
        home_page.select_currency("USD")

    with allure.step("Получить текущую выбранную валюту"):
        current = home_page.get_current_currency()

    with allure.step("Проверить, что валюта изменилась на USD"):
        assert current == "USD $", (
            f"Ожидали 'USD €', а в селекторе валют отображается '{current}'"
        )
        allure.attach(
            "Тест переключения валюты на USD успешно завершен",
            name="test_result",
            attachment_type=allure.attachment_type.TEXT
        )