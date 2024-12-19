from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class WebsiteUtils:
    @staticmethod
    def selenium_init(url):
        print("Test start")
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.implicitly_wait(30)
        driver.get(url)
        print(f"Initial URL: {driver.current_url}")
        return driver

    @staticmethod
    def selenium_end(driver):
        driver.quit()
        print("Test end")

    @staticmethod
    def log_current_url(driver):
        print(f"Current URL: {driver.current_url}")

    @staticmethod
    def wait_for_page_to_load(driver, timeout=10):
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        WebsiteUtils.log_current_url(driver)
