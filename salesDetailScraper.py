__author__ = 'Eli'

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from datetime import date, datetime, timedelta
from itertools import islice
#from selenium.common.exceptions import NoSuchElementException
driver = webdriver.Chrome(executable_path=r".../chromedriver_win32/chromedriver.exe")

def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

def main():
    wait = WebDriverWait(driver,3)
    # Open Edmonton Tribunals website
    driver.get("http://www.gettelnetwork.com/")

    driver.find_element_by_id("signin_modal").click()

    time.sleep(7)

    username = driver.find_element_by_id("username_input")
    username.send_keys('1509')

    password = driver.find_element_by_id("user_password_input")
    password.send_keys('altustax')

    driver.find_element_by_id("signin_submit").click()

    sale_date_from = driver.find_element_by_name("asrch_sale_fromdate")
    sale_date_from.clear()
    sale_date_from.send_keys("05/01/2017")

    sale_date_to = driver.find_element_by_name("asrch_sale_todate")
    sale_date_to.clear()

    today_date = date.today()
    sale_date_to.send_keys(today_date.strftime('%m/%d/%Y'))

    time.sleep(2.2)
    property_type = driver.find_element_by_name("asrch_prop_type")
    property_type.click()
    property_type.send_keys('a')
    property_type.send_keys(Keys.RETURN)

    time.sleep(2.5)
    driver.find_element_by_name("doSearch").click()

    time.sleep(5)

    file_data = []
    while True:
        view_buttons = driver.find_elements_by_xpath("//input[@type='submit' and @value='View']")

        nameList = []

        for i in view_buttons:
            name = i.get_attribute('name')
            nameList.append(name)
        if driver.find_element_by_name("next").is_enabled():
            for name in nameList:
                driver.find_element_by_name(name).click()

                time.sleep(2)

                table1 = driver.find_element_by_xpath("//*[@id='bodycol']/table[2]")
                body1 = table1.find_element_by_tag_name('tbody')
                body_rows1 = body1.find_elements_by_tag_name('tr')

                for row in body_rows1:
                    data = row.find_elements_by_tag_name('td')
                    file_row = []
                    for datum in data:
                        datum_text = datum.text.encode('utf8')
                        file_row.append(datum_text)
                    file_data.append(b",".join(file_row))

                table2 = driver.find_element_by_xpath("//*[@id='bodycol']/table[1]")
                body2 = table2.find_element_by_tag_name('tbody')
                body_rows2 = body2.find_elements_by_tag_name('tr')

                for row in body_rows2:
                    data2 = row.find_elements_by_tag_name('td')
                    file_row2 = []
                    for datum in data2:
                        datum_text2 = datum.text.encode('utf8')
                        file_row2.append(datum_text2)
                    file_data.append(b",".join(file_row2))

                driver.execute_script("window.history.go(-1)")
                time.sleep(2)
            driver.find_element_by_name("next").click()
            time.sleep(3)
        else:
            break

    print(file_data)


if __name__ == "__main__":
    main()
 