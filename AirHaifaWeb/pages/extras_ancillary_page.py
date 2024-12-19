import random
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from AirHaifaWeb.utils import WebsiteUtils


class extras_ancillary_page:
    def __init__(self, driver):
        self.driver = driver
        self.flight_extras_all_options_locator = "anc"
        self.add_ancillary_btn_locator = ".button.btn-active.btnModify"
        self.select_box_locator = "div.column"
        self.ancillary_options_locator = "#selectBox option[data-itemid]"
        self.submit_ancillary_options_locator = ".button.addAnc0"
        self.cart_button_locator = "cartButton"
        self.expand_button_locator = "div.column-2 .eSecond > a"
        self.cart_ancillary_element_locator = ".removeFlight.removeAnc"
        self.close_cart_locator = "btnOk"
        self.continue_button_locator = "extrasCountinue"

    def select_extra_ancillary(self, child_index):
        flight_extras_all_options = self.driver.find_elements(By.ID, self.flight_extras_all_options_locator)
        if child_index < 0 or child_index >= len(flight_extras_all_options):
            raise ValueError(
                f"Invalid child index {child_index}. Must be between 0 and {len(flight_extras_all_options) - 1}.")

        ancillary_container = flight_extras_all_options[child_index]
        add_ancillary_btn = ancillary_container.find_element(By.CSS_SELECTOR, self.add_ancillary_btn_locator)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(add_ancillary_btn))
        add_ancillary_btn.click()
        print(f"Add extra ancillary button clicked successfully at child index {child_index}.")
        sleep(3)

        select_box = self.driver.find_elements(By.CSS_SELECTOR, self.select_box_locator)
        select_box[1].click()
        sleep(2)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.ancillary_options_locator))
        )

        all_options = self.driver.find_elements(By.CSS_SELECTOR, self.ancillary_options_locator)
        visible_options = [option for option in all_options if option.is_displayed()]

        random_option = random.choice(visible_options)
        random_option.click()
        sleep(2)
        print(f"Clicked random visible option: {random_option.text} (value: {random_option.get_attribute('value')})")

        submit_ancillary_selected = self.driver.find_element(By.CSS_SELECTOR, self.submit_ancillary_options_locator)
        submit_ancillary_selected.click()
        print("Ancillary has been added to the cart")
        sleep(5)

        ancillary_id = random_option.get_attribute("data-itemid")
        print(f"Selected ancillary with Item ID: {ancillary_id}")
        return ancillary_id

    def view_cart(self, ancillary_id):
        cart_button = self.driver.find_element(By.CLASS_NAME, self.cart_button_locator)
        cart_button.click()
        print("Navigated to the cart")

        expand_button = self.driver.find_element(By.CSS_SELECTOR, self.expand_button_locator)
        expand_button.click()
        print("Expand button is clicked")

        cart_ancillary_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.cart_ancillary_element_locator))
        )
        cart_ancillary_id = cart_ancillary_element.get_attribute("data-itemid")

        assert cart_ancillary_id == ancillary_id, (
            f"Mismatch in data-itemid. Expected: {ancillary_id}, Found: {cart_ancillary_id}"
        )
        print(f"Ancillary in cart matches selected ancillary: data-itemid = {ancillary_id}")

        inv_id = cart_ancillary_element.get_attribute("data-invid")
        booking_id = cart_ancillary_element.get_attribute("data-bookingid")
        print(f"Created inv_id: {inv_id} and booking_id: {booking_id}")

        close_cart_button = self.driver.find_element(By.CLASS_NAME, self.close_cart_locator)
        close_cart_button.click()
        print("Cart closed successfully")
        sleep(3)

    def submit_extra_ancillary_selection(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
        continue_button = self.driver.find_element(By.ID,self.continue_button_locator)
        sleep(3)
        self.driver.execute_script("arguments[0].click();", continue_button)
        print("Continue button is pressed")
        sleep(10)
        WebsiteUtils.wait_for_page_to_load(self.driver)  # Log URL after redirection
