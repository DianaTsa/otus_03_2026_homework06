def test_switch_currency_to_eur(home_page):
    home_page.open("/")
    home_page.select_currency("USD")

    current = home_page.get_current_currency()
    assert current == "USD $", (
        f"Ожидали 'USD €', а в селекторе валют отображается '{current}'"
    )