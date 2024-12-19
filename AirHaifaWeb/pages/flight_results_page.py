from time import sleep

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from AirHaifaWeb.utils import WebsiteUtils


class flight_results_page:
    def __init__(self, driver):
        self.driver = driver
        self.flight_outbound_button_locator = "flightItem_titleBtn"
        self.fare_container_locator = "li.flight-class__box"
        self.fare_button_locator = "flightClass_btn"
        self.cart_button_locator = "cartButton"
        self.close_cart_locator = "btnOk"
        self.continue_button_locator = "fr_continue_btn"

    def select_outbound_flight(self, index):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, self.flight_outbound_button_locator))
        )
        flight_outbound_button = self.driver.find_elements(By.CLASS_NAME, self.flight_outbound_button_locator)
        if len(flight_outbound_button) > 0:
            self.driver.execute_script("arguments[0].click();", flight_outbound_button[index])
            print(f"Outbound flight is selected: {index}")

    def select_outbound_flight_fare(self, child_index):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
        fare_containers = self.driver.find_elements(By.CSS_SELECTOR, self.fare_container_locator)
        sleep(3)
        if child_index < 0 or child_index >= len(fare_containers):
            raise ValueError(f"Invalid child index {child_index}. Must be between 0 and {len(fare_containers) - 1}.")

        fare_container = fare_containers[child_index]
        self.driver.execute_script(
            "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", fare_container
        )

        # Retrieve the data-flightid from the selected fare container
        fare_flight_id = fare_container.get_attribute("data-flightid")
        fare_id = fare_container.get_attribute("data-fareid")

        # Click the button inside the selected container to choose the fare
        fare_button = fare_container.find_element(By.CLASS_NAME, self.fare_button_locator)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(fare_button)).click()
        print(f"Fare button clicked successfully at child index {child_index}.")
        sleep(3)

        print(f"Selected flight with Flight ID: {fare_flight_id} and Fare ID: {fare_id}")
        return fare_flight_id

    def view_cart(self, fare_flight_id):
        cart_button = self.driver.find_element(By.CLASS_NAME, self.cart_button_locator)
        cart_button.click()
        print("Navigated to the cart")

        cart_flight_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".grayRow"))
        )
        cart_flight_id = cart_flight_element.get_attribute("data-flightid")

        assert cart_flight_id == fare_flight_id, (
            f"Mismatch in data-flightid. Expected: {fare_flight_id}, Found: {cart_flight_id}"
        )
        print(f"Flight in cart matches selected flight: data-flightid = {fare_flight_id}")

        close_cart_button = self.driver.find_element(By.CLASS_NAME, self.close_cart_locator)
        close_cart_button.click()
        print("Cart closed successfully")
        sleep(3)

    def submit_flight_selection(self):
        continue_button = self.driver.find_element(By.ID, self.continue_button_locator)
        continue_button.click()
        print("Continue button is pressed")
        sleep(10)
        WebsiteUtils.wait_for_page_to_load(self.driver)  # Log URL after redirection
