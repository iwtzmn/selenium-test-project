import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from AirHaifaWeb.globals import LAST_NAME, FIRST_NAME, PHONE_NUMBER, EMAIL, PAX_TITLE_OPTIONS, DOB_DATE_FILED, DOB_YEAR_FILED, \
    DOB_MONTH_FILED
from AirHaifaWeb.utils import WebsiteUtils


class passenger_details_page:
    def __init__(self, driver):
        self.driver = driver
        self.pax_title_locator = "title_1"
        self.pax_title_options = "#title_1 option"
        self.input_first_name_selector = "firstname_1"
        self.enter_first_name_selector = "#firstname_1 > input[type=text]"
        self.input_last_name_selector = "lastname_1"
        self.enter_last_name_selector = "#lastname_1 > input[type=text]"
        self.input_phone_number_selector = "phone_1"
        self.enter_phone_number_selector = "#phone_1 > input[type=tel]"
        self.input_email_selector = "email_1"
        self.enter_email_selector = "#email_1 > input[type=email]"
        self.birthday_selector = "birthday_1"
        self.date_field = "#birthday_1 .datepicker_day_prim"
        self.month_field = "#birthday_1 .datepicker_month_prim"
        self.year_field = "#birthday_1 .datepicker_year_prim"
        self.continue_button = "btn_continue"

    def select_pax_title(self, max_retries=3, delay=2):
        retries = 0
        while retries < max_retries:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, self.pax_title_locator))
                )
                self.driver.find_element(By.ID, self.pax_title_locator).click()

                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.pax_title_options))
                )

                all_options = self.driver.find_elements(By.CSS_SELECTOR, self.pax_title_options)
                visible_pax_title_options = [
                    option for option in all_options
                    if option.is_displayed() and option.text.strip() in PAX_TITLE_OPTIONS
                ]

                if not visible_pax_title_options:
                    raise Exception("No visible passenger title options available.")

                random_index = random.randint(0, len(visible_pax_title_options) - 1)
                random_option = visible_pax_title_options[random_index]
                random_option.click()
                sleep(2)

                selected_option_text = random_option.text.strip()
                print(f"Randomly selected visible option: {selected_option_text}")
                return selected_option_text

            except Exception as e:
                retries += 1
                print(f"Attempt {retries} failed: {e}")
                if retries < max_retries:
                    print(f"Retrying in {delay} seconds...")
                    sleep(delay)
                else:
                    print("Max retries reached. Unable to select a passenger title.")
                    raise

    def fill_passenger_details(self):
        enter_first_name = self.driver.find_element(By.CSS_SELECTOR, self.enter_first_name_selector)
        enter_first_name.send_keys(FIRST_NAME)
        print(f"Filled first name: {FIRST_NAME}")
        sleep(3)

        enter_last_name = self.driver.find_element(By.CSS_SELECTOR, self.enter_last_name_selector)
        enter_last_name.send_keys(LAST_NAME)
        print(f"Filled last name: {LAST_NAME}")
        sleep(3)

        enter_phone_number = self.driver.find_element(By.CSS_SELECTOR, self.enter_phone_number_selector)
        enter_phone_number.send_keys(PHONE_NUMBER)
        print(f"Filled first name: {PHONE_NUMBER}")
        sleep(3)

        enter_email = self.driver.find_element(By.CSS_SELECTOR, self.enter_email_selector)
        enter_email.send_keys(EMAIL)
        print(f"Filled first name: {EMAIL}")
        sleep(5)

    def fill_passenger_birthday(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.date_field))
        )
        date_input = self.driver.find_element(By.CSS_SELECTOR, self.date_field)
        random_date = random.randint(DOB_DATE_FILED[0], DOB_DATE_FILED[1])
        self.driver.execute_script("arguments[0].value = arguments[1];", date_input, random_date)
        print(f"Filled date: {random_date}")

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.month_field))
        )
        month_input = self.driver.find_element(By.CSS_SELECTOR, self.month_field)
        random_month = random.randint(DOB_MONTH_FILED[0], DOB_MONTH_FILED[1])
        self.driver.execute_script("arguments[0].value = arguments[1];", month_input, random_month)
        print(f"Filled month: {random_month}")

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.year_field))
        )
        year_input = self.driver.find_element(By.CSS_SELECTOR, self.year_field)
        random_year = random.randint(DOB_YEAR_FILED[0], DOB_YEAR_FILED[1])
        self.driver.execute_script("arguments[0].value = arguments[1];", year_input, random_year)
        print(f"Filled year: {random_year}")

    def submit_passenger_details_section(self):
        continue_button = self.driver.find_element(By.ID, self.continue_button)
        self.driver.execute_script("arguments[0].click();", continue_button)
        print("Continue button is pressed")
        sleep(10)
        WebsiteUtils.wait_for_page_to_load(self.driver)  # Log URL after redirection
