import random
from time import sleep

from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from AirHaifaWeb.utils import WebsiteUtils


class search_flight_page:
    def __init__(self, driver):
        self.driver = driver
        self.cookies_button_locator = "cookieButton"
        self.close_button_locator = "material-symbols-outlined"
        self.ow_selection_locator = "radio-inline"
        self.departure_locator = "flightFrom"
        self.departure_list_locator = ".easy-autocomplete-container ul li"
        self.arrival_locator = "flightTo"
        self.arrival_list_locator = ".easy-autocomplete-container ul li"
        self.all_dates_locator = "ul.dateFrame_calendar li a"
        self.search_button_locator = "flightSubmit"

    def cookies_apply(self):
        cookies_button = self.driver.find_element(By.ID, self.cookies_button_locator)
        cookies_button.click()
        print("Cookies are applied")

    def close_alert_msg(self):
        close_button = self.driver.find_element(By.CLASS_NAME, self.close_button_locator)
        close_button.click()
        print("Top alert msg have been closed")

    def ow_type(self):
        ow_selection = self.driver.find_elements(By.CLASS_NAME, self.ow_selection_locator)
        ow_selection[1].click()
        print("One Way type is selected")

    def select_departure(self, index):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, self.departure_locator))
        )
        departure = self.driver.find_element(By.ID, self.departure_locator)
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", departure)
        sleep(5)
        departure.click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.departure_list_locator))
        )
        departure_list = self.driver.find_elements(By.CSS_SELECTOR, self.departure_list_locator)
        if len(departure_list) > 0:
            departure_list[index].click()
            print(f"Departure flight from is selected,index is {index}")
        sleep(5)

    def select_arrival(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, self.arrival_locator))
        )
        arrival = self.driver.find_element(By.ID, self.arrival_locator)
        self.driver.execute_script("arguments[0].click();", arrival)
        sleep(2)
        arrival.send_keys(Keys.ARROW_DOWN)
        arrival.send_keys(Keys.ENTER)
        print(f"Arrival flight from is selected")
        sleep(5)

    def select_flight_date(self):
        all_dates = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.all_dates_locator))
        )
        valid_dates = [date for date in all_dates if "disabled" not in date.get_attribute("class")]

        if not valid_dates:
            print("No valid dates available.")
            return

        random_date = random.choice(valid_dates)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", random_date)
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(random_date))
        self.driver.execute_script("arguments[0].click();", random_date)

        print(f"Randomly selected date: {random_date.get_attribute('data-daynumber')} "
              f"{random_date.get_attribute('data-monthnumber')} "
              f"{random_date.get_attribute('data-year')}")

    def start_search(self):
        search_button = self.driver.find_element(By.CLASS_NAME, self.search_button_locator)
        search_button.click()
        print("Continue button is pressed")
        sleep(10)
        WebsiteUtils.wait_for_page_to_load(self.driver)  # Log URL after redirection
