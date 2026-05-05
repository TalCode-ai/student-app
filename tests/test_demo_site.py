import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_open_parabank_homepage(driver):
    driver.get("https://parabank.parasoft.com/parabank/index.htm")

    assert "ParaBank" in driver.title


def test_register_new_user(driver):
    username = f"amir_test_{int(time.time())}"
    password = "123456"

    driver.get("https://parabank.parasoft.com/parabank/register.htm")

    driver.find_element(By.ID, "customer.firstName").send_keys("Amir")
    driver.find_element(By.ID, "customer.lastName").send_keys("Schwartz")
    driver.find_element(By.ID, "customer.address.street").send_keys("Herzel 10")
    driver.find_element(By.ID, "customer.address.city").send_keys("Raanana")
    driver.find_element(By.ID, "customer.address.state").send_keys("Israel")
    driver.find_element(By.ID, "customer.address.zipCode").send_keys("12345")
    driver.find_element(By.ID, "customer.phoneNumber").send_keys("0501234567")
    driver.find_element(By.ID, "customer.ssn").send_keys("123456789")

    driver.find_element(By.ID, "customer.username").send_keys(username)
    driver.find_element(By.ID, "customer.password").send_keys(password)
    driver.find_element(By.ID, "repeatedPassword").send_keys(password)

    driver.find_element(By.CSS_SELECTOR, "input[value='Register']").click()

    assert "Your account was created successfully" in driver.page_source


def test_login_with_new_registered_user(driver):
    username = f"amir_login_{int(time.time())}"
    password = "123456"

    driver.get("https://parabank.parasoft.com/parabank/register.htm")

    driver.find_element(By.ID, "customer.firstName").send_keys("Amir")
    driver.find_element(By.ID, "customer.lastName").send_keys("Schwartz")
    driver.find_element(By.ID, "customer.address.street").send_keys("Herzel 10")
    driver.find_element(By.ID, "customer.address.city").send_keys("Raanana")
    driver.find_element(By.ID, "customer.address.state").send_keys("Israel")
    driver.find_element(By.ID, "customer.address.zipCode").send_keys("12345")
    driver.find_element(By.ID, "customer.phoneNumber").send_keys("0501234567")
    driver.find_element(By.ID, "customer.ssn").send_keys("123456789")

    driver.find_element(By.ID, "customer.username").send_keys(username)
    driver.find_element(By.ID, "customer.password").send_keys(password)
    driver.find_element(By.ID, "repeatedPassword").send_keys(password)

    driver.find_element(By.CSS_SELECTOR, "input[value='Register']").click()

    assert "Your account was created successfully" in driver.page_source

    driver.find_element(By.LINK_TEXT, "Log Out").click()

    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "input[value='Log In']").click()

    assert "Accounts Overview" in driver.page_source


def test_login_with_invalid_user(driver):
    driver.get("https://parabank.parasoft.com/parabank/index.htm")

    driver.find_element(By.NAME, "username").send_keys("invalid_user_123")
    driver.find_element(By.NAME, "password").send_keys("wrong_password")
    driver.find_element(By.CSS_SELECTOR, "input[value='Log In']").click()

    assert "The username and password could not be verified" in driver.page_source
