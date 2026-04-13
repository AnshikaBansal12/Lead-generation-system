from selenium.webdriver.common.by import By
from Scraper.driver import setup_driver
import time

def get_phone(item,driver):
    phone = ""

    try:
        phone = item.find_element(By.CLASS_NAME, "callcontent").text

        if phone and "Show Number" not in phone:
            return phone.strip()
    except:
        pass

    try:
       driver.execute_script("arguments[0].click();",item)
       time.sleep(3)

       try:
           btn = driver.find_element(By.ID, "header_shownumber")

           driver.execute_script("argumnets[0].scrollIntoView();",btn)
           time.sleep(1)

           driver.execute_script("arguments[0].click();",btn)
           time.sleep(2)
       except:
           pass
       try:
           phone_elem = driver.find_element(By.XPATH, '//a[contains(@href,"tel:")]')
           phone = phone_elem.text.strip()
       except:
           pass
       
       driver.back()
       time.sleep(2)

       if phone:
           return phone
    except:
        pass

    try:
        tel = item.find_element(By.XPATH,'.//a[contains(@href,"tel:")]')
        phone = tel.get_attribute("href").replace("tel:","")

        if phone:
            return phone.strip()
    except:
        pass

    return "Not Available"