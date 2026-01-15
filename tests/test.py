import time
import subprocess
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
try:
    try:
        from webdriver_manager.chrome import ChromeDriverManager  # type: ignore
        from webdriver_manager.firefox import GeckoDriverManager  # type: ignore
    except ImportError:
        raise ImportError("webdriver_manager is not installed. Please run 'pip install webdriver-manager' to install it.")
except ImportError:
    raise ImportError("webdriver_manager is not installed. Please run 'pip install webdriver-manager' to install it.")

BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture(scope="session", autouse=True)
def run_php_server():
    proc = subprocess.Popen(["php", "-S", "127.0.0.1:8000", "-t", "."])
    time.sleep(3)
    yield
    proc.terminate()


import os

@pytest.fixture
def driver():
    browser = os.environ.get("BROWSER", "chrome").lower()
    if browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
    else:
        options = ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
    yield driver
    driver.quit()


def open_register(driver):
    driver.get(f"{BASE_URL}/register.php")
    time.sleep(0.5)


def fill_common_fields(driver, name="Tester", email="tester@test.com"):
    driver.find_element(By.NAME, "name").send_keys(name)
    driver.find_element(By.NAME, "email").send_keys(email)


# FT001: Register valid
def test_FT001_register_valid(driver):
    open_register(driver)
    fill_common_fields(driver)

    driver.find_element(By.NAME, "username").send_keys("user01")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "repassword").send_keys("password123")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(1)
    assert "index.php" in driver.current_url


# FT002: Username kosong, password diisi
def test_FT002_register_username_empty(driver):
    open_register(driver)
    fill_common_fields(driver)

    # username dikosongkan
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "repassword").send_keys("password123")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(1)
    assert "register.php" in driver.current_url or "Data tidak boleh kosong" in driver.page_source


# FT003: Username diisi, password kosong
def test_FT003_register_password_empty(driver):
    open_register(driver)
    fill_common_fields(driver)

    driver.find_element(By.NAME, "username").send_keys("user02")
    # password & repassword dikosongkan
    driver.find_element(By.NAME, "submit").click()

    time.sleep(1)
    assert "register.php" in driver.current_url or "Data tidak boleh kosong" in driver.page_source


# FT004: Username duplikat (user01) + password baru
def test_FT004_register_duplicate_username(driver):
    open_register(driver)
    fill_common_fields(driver, name="Tester2", email="tester2@test.com")

    driver.find_element(By.NAME, "username").send_keys("user01")
    driver.find_element(By.NAME, "password").send_keys("passwordBARU")
    driver.find_element(By.NAME, "repassword").send_keys("passwordBARU")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(1)
    assert "Username sudah terdaftar" in driver.page_source or "register.php" in driver.current_url
