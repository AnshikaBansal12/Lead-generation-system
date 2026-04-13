from Scraper.scraper import scrape_leads
from Utils.util import save_to_excel
from Processing.data_loader import load_data
from Processing.data_cleaner import clean_data
from Processing.analyzer import analyzer_data
from Processing.report import generate_report
import pandas as pd
import os

print("------------Lead Generator---------------")

def run_pipeline():
    keyword = input("Enter business type: ")
    start_page = int(input("Enter starting page:"))
    pages = int(input("Enter number of pages:"))
    cities = input("Enter Cities (comma separated):").split(",")
    
    all_data = []
    
    for city in cities:
       city = city.strip()
       data = scrape_leads(keyword,city,start_page, pages)
       all_data.extend(data)

#--------Raw Data Saved-----------
    raw_data = "C:/Users/hp/OneDrive/Desktop/Free/Lead_Generation_Automation/Data/business_leads.xlsx"
    os.makedirs(os.path.dirname(raw_data),exist_ok=True)
    save_to_excel(all_data,raw_data)
    print("Data saved successfully")

    print("---------REPORT AUTOMATION------------")
    
#---------Load Data--------------
    report_data = "C:/Users/hp/OneDrive/Desktop/Free/Lead_Generation_Automation/Data/business_leads_with_website.xlsx"
    df_load = load_data(raw_data)

#---------Clean Data------------
    df_clean = clean_data(df_load)

#--------Analyze Data---------------
    summary = analyzer_data(df_clean)

#--------Generate Report------------
    report = generate_report(df_clean,summary)

    print("\nFull Pipeline Completed")

if __name__ == "__main__":
    run_pipeline()