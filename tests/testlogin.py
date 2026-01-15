import time
import subprocess
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import os

BASE_URL = "http://127.0.0.1:8000"

# Jalankan PHP built-in server sebagai stub
@pytest.fixture(scope="session", autouse=True)
def run_php_server():
    proc = subprocess.Popen(["php", "-S", "127.0.0.1:8000", "-t", "."])
    time.sleep(3)
    yield
    proc.terminate()


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


def open_login(driver):
    driver.get(f"{BASE_URL}/login.php")
    time.sleep(0.5)


# FT005 – Login dengan kredensial benar
def test_FT005_login_valid(driver):
    open_login(driver)

    driver.find_element(By.NAME, "username").send_keys("user01")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(1)
    assert "index.php" in driver.current_url


# FT006 – Login dengan username tidak terdaftar
def test_FT006_login_user_not_found(driver):
    open_login(driver)

    driver.find_element(By.NAME, "username").send_keys("user_tidak_ada")
    driver.find_element(By.NAME, "password").send_keys("abc123")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(1)
    assert "Username tidak ditemukan" in driver.page_source or "login.php" in driver.current_url


# FT007 – Login dengan password salah
def test_FT007_login_wrong_password(driver):
    open_login(driver)

    driver.find_element(By.NAME, "username").send_keys("user01")
    driver.find_element(By.NAME, "password").send_keys("salah123")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(1)
    assert "Password salah" in driver.page_source or "login.php" in driver.current_url


# FT008 – Login dengan field kosong
def test_FT008_login_empty_fields(driver):
    open_login(driver)

    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)

    assert "Data tidak boleh kosong" in driver.page_source or "login.php" in driver.current_url

