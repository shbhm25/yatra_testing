import os
import pdb
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.devtools.v85.debugger import pause
from selenium.webdriver.common.keys import Keys
from base.base_driver import BaseDriver
from pages.search_flights_results_page import SearchFlightResults
from utilities.utils import Utils


class LaunchPage(BaseDriver):
    log = Utils.custom_logger()
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    DEPART_FROM_FIELD = "//p[text()='Departure From']"
    DEPART_FROM_FIELD_KEY = "//input[@id='input-with-icon-adornment']"
    GOING_TO_FIELD = "//p[text()='Going To']"
    GOING_TO_FIELD_KEY = "//input[@id='input-with-icon-adornment']"
    RESULT_LIST = "//div[@class='MuiBox-root css-134xwrj']/ul/div[1]"
    SELECT_DATE_FIELD = "//div[@class='position-relative MuiBox-root css-0']/div[@class='MuiBox-root css-0']"
    ALL_DATES = "//div[@id='monthWrapper']//tbody//td[@class!='inActiveTD']"
    SEARCH_BUTTON = "//input[@value='Search Flights']"
    Month_path= "//span[@class='react-datepicker__current-month']"

    def getDepartFromField(self,field):
        return self.wait_until_element_is_clickable(By.XPATH,field)

    def getGoingToField(self,field):
        return self.wait_until_element_is_clickable(By.XPATH, field)

    def getFromToResults(self):
        return self.wait_for_presence_of_all_elements(By.XPATH, self.RESULT_LIST)

    def getDepatureDateField(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.SELECT_DATE_FIELD)

    def getAllDatesField(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.ALL_DATES)

    def getSearchButton(self):
        return self.driver.find_element(By.XPATH, self.SEARCH_BUTTON)

    def enterDepartFromLocation(self, departlocation):
        try:
            self.getDepartFromField(self.DEPART_FROM_FIELD).click()
            self.getDepartFromField(self.DEPART_FROM_FIELD_KEY).send_keys(departlocation)
            self.log.info("Typed text into depart from field successfully")
            time.sleep(2)
            search_results = self.getFromToResults()
            print(search_results)
            for results in search_results:
                print(results.text)
                if departlocation.lower() in results.text.lower():
                    time.sleep(2)
                    print("Match found")
                    results.click()
                    break

        except:
            print("not able to find goto place")

    def enterGoingToLocation(self, goingtolocation):
        try:
            self.getGoingToField(self.GOING_TO_FIELD).click()
            self.log.info("Clicked on going to")
            time.sleep(2)
            self.getGoingToField(self.GOING_TO_FIELD_KEY).send_keys(goingtolocation)
            self.log.info("Typed text into going to field successfully")
            time.sleep(2)
            search_results = self.getFromToResults()
            print(search_results)
            for results in search_results:
                print(results.text)
                if goingtolocation.lower() in results.text.lower():
                    time.sleep(2)
                    print("Match found")
                    results.click()
                    break
        except:
            print("not able to find goto place")

    # react-datepicker__day react-datepicker__day--0
    def enterDepartureDate(self, departuredate):
        self.getDepatureDateField().click()
        pdb.set_trace()
        current_month = self.driver.find_element(By.XPATH,self.Month_path).text

        all_dates = self.getAllDatesField().find_elements(By.XPATH, self.ALL_DATES)
        for date in all_dates:
            if date.get_attribute("data-date") == departuredate:
                date.click()
                break

    def clickSearchFlightsButton(self):
        self.getSearchButton().click()
        time.sleep(4)

    def searchFlights(self, departlocation, goingtolocation, departuredate):
        self.enterDepartFromLocation(departlocation)
        self.enterGoingToLocation(goingtolocation)
        self.enterDepartureDate(departuredate)
        self.clickSearchFlightsButton()
        search_flights_result = SearchFlightResults(self.driver)
        return search_flights_result
