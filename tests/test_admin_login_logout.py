from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def test_admin_login_logout(driver, base_url):
    wait = WebDriverWait(driver, 10)
    driver.get(base_url + "administration")


    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#email"))).send_keys("admin@example.com")
    driver.find_element(By.CSS_SELECTOR, "#passwd").send_keys("Admin123!")
    driver.find_element(By.ID, "submit_login").click()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#dashtrends")))

    driver.find_element(By.CSS_SELECTOR, "#employee_infos").click()
    driver.find_element(By.ID, "header_logout").click()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#email")))




