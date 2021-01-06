import time
import datetime
from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
import numpy as np
import pandas as pd
from pandas import ExcelWriter

roll_list = pd.read_csv("...NonResidential Roll Numbers.csv")

roll_list.columns = ['Roll' for i in roll_list.columns]

chrome_options = webdriver.ChromeOptions()

driver = webdriver.Chrome(executable_path=r"c:/users/31463/Downloads/chromedriver_win32 (1)/chromedriver.exe")


def main():

    # Open Edmonton Tribunals website
    driver.get("https://arb.edmonton.ca/Default.aspx?PossePresentation=SearchForARBDecisions")

    # ***** Enter the roll number
    for roll in roll_list:
        taxRoll = driver.find_element_by_id("TaxRollAccount_1505072_S0")
        taxRoll.clear()            # clear the field
        taxRoll.send_keys(str(roll))

        # Hit the search button
        driver.find_element_by_id("ctl00_cphBottomFunctionBand_ctl03_PerformSearch").click()

        time.sleep(5)

        # ******* Downloads the pdfs
        links = driver.find_elements_by_css_selector("a[href*='Download']")

        for element in links:
            element.click()
            time.sleep(5)
        # *******
        driver.back()


if __name__ == "__main__":
    main()

