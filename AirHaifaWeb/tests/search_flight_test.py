from AirHaifaWeb.globals import URL
from AirHaifaWeb.pages.search_flight_page import search_flight_page
from AirHaifaWeb.utils import WebsiteUtils


class search_flight_test:
    utils = WebsiteUtils()
    driver = utils.selenium_init(URL)

    # Run Search Flight Page
    search_flight_object = search_flight_page(driver)
    search_flight_object.cookies_apply()
    search_flight_object.close_alert_msg()
    search_flight_object.ow_type()
    search_flight_object.select_departure(index=0)
    search_flight_object.select_arrival()
    search_flight_object.select_flight_date()
    search_flight_object.start_search()
    utils.selenium_end(driver)
