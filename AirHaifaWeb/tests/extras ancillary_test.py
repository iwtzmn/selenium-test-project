from AirHaifaWeb.globals import URL
from AirHaifaWeb.pages.extras_ancillary_page import extras_ancillary_page
from AirHaifaWeb.pages.search_flight_page import search_flight_page
from AirHaifaWeb.pages.flight_results_page import flight_results_page
from AirHaifaWeb.pages.passenger_details_page import passenger_details_page
from AirHaifaWeb.utils import WebsiteUtils


class extras_ancillary_test:
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

    # Run Flight Results Page
    flight_results_object = flight_results_page(driver)
    flight_results_object.select_outbound_flight(index=0)
    fare_flight_id = flight_results_object.select_outbound_flight_fare(child_index=0)
    flight_results_object.view_cart(fare_flight_id=fare_flight_id)
    flight_results_object.submit_flight_selection()

    # Run Passenger Details Page
    passenger_details_object = passenger_details_page(driver)
    passenger_details_object.select_pax_title()
    passenger_details_object.fill_passenger_details()
    passenger_details_object.fill_passenger_birthday()
    passenger_details_object.submit_passenger_details_section()

    # Run Extras Ancillary Page
    extras_ancillary_object = extras_ancillary_page(driver)
    ancillary_id = extras_ancillary_object.select_extra_ancillary(child_index=0)
    extras_ancillary_object.view_cart(ancillary_id=ancillary_id)
    extras_ancillary_object.submit_extra_ancillary_selection()
    utils.selenium_end(driver)
