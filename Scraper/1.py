from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from Utils.email_extractor import process_website
from Scraper.driver import setup_driver
from Utils.phone import get_phone


#Main Scraper
def scrape_leads(keyword, city, start_page, pages):
    driver = setup_driver()
    leads = []    

    search_city = city.replace(" ","-")
    keyword = keyword.replace(" ","-")

    for page in range(start_page,pages+1):
        url = f"https://www.justdial.com/{search_city}/{keyword}/page-{page}"
        print(f"Scrapping {city} | Page {page} ")

        driver.get(url)
        #time.sleep(5)

        try:
            WebDriverWait(driver,10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME,"resultbox"))
            )
        except:
            #print("Timeout, continuing.....")
            #time.sleep(random.uniform(5, 10))
            continue
        
        #Scroll (human-like)
        for i in range(5):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(random.uniform(3, 2))

        results = driver.find_elements(By.CLASS_NAME,"resultbox")

        if len(results) == 0:
            print("No results found (may be blocked or wrong selector)")

        print("Business found:",len(results))

        for r in results:
            try:
                name = r.find_element(By.CLASS_NAME,"resultbox_title_anchor").text
            except:
                name = "Not Available"
            
            phone = get_phone(r,driver)
            
            try:
                rating = r.find_element(By.CLASS_NAME, "resultbox_totalrate").text
            except:
                rating = "Not Available"
            
            try:
                link = r.find_element(By.TAG_NAME,"a").get_attribute("href")
            except:
                continue

            #Open in new Tab
            driver.execute_script("window.open(arguments[0]);",link)
            try:
              WebDriverWait(driver, 5).until(lambda d: len(d.window_handles) > 1)
              driver.switch_to.window(driver.window_handles[1])
              time.sleep(3)

              try:
                address = driver.find_element(By.XPATH,"//address[contains(@class,'vendorinfo_address')]").text
              except:
                address = "Not Available"

              try:
                website = driver.find_element(By.XPATH,"//a[contains(@class,'address_link')]").get_attribute("href")
              except:
                website = "Not Available"

              try:
                try:
                    email_btn = WebDriverWait(driver, 5).until(
                       EC.element_to_be_clickable(By.XPATH,"//span[conatains(text(),'Email')]")
                    )
                    email_btn.click()
                    time.sleep(2)
                except:
                    pass

                email_element = driver.find_element(By.XPATH,"//a[contains(@href,'mailto')]")
                email = email_element.get_attribute("href").replace("mailto:", "").strip()
              except:
                email = ""

              emails = process_website(website) if website and website != "Not Available" else []
              final_email = email if email else (", ".join(emails) if emails else "Not Available")
            
              leads.append({
                "Business Type":keyword,
                "Company":name,
                "Phone":phone,
                "Address": address,
                "Rating": rating,
                "City": city,
                "Website": website,
                "Email" : final_email
              })

              print(name,"|", phone, "|", rating, "|", final_email)
            
            finally:
               if len(driver.window_handles)>1:
                  driver.close()
                  driver.switch_to.window(driver.window_handles[0])

            time.sleep(random.uniform(2,4))

    driver.quit()
    return leads    