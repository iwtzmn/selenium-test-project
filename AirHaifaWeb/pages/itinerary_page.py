from time import sleep

from selenium.webdriver.common.by import By

from AirHaifaWeb.utils import WebsiteUtils


class itinerary_page:
    def __init__(self, driver):
        self.driver = driver
        self.checkbox_approval_selector = "#rules"

    def approval_of_the_terms(self):
        checkbox = self.driver.find_element(By.CSS_SELECTOR, self.checkbox_approval_selector)
        sleep(3)
        self.driver.execute_script("arguments[0].click();", checkbox)
        print("Approval of the terms checkbox is checked")
        WebsiteUtils.wait_for_page_to_load(self.driver)  # Log URL after redirection
