import pandas as pd
import os

file_name="C:/Users/hp/OneDrive/Desktop/Free/Lead_Generation_Automation/Data/business_leads.xlsx"
def save_to_excel(leads, file=file_name):
    if not leads:
        print("No data scraped.")
        return
    
    new_df = pd.DataFrame(leads)

    print("Total Scraped Leads:", len(new_df))

    #----------File Exists- Append-------------
    if os.path.exists(file):
        try:
            old_df = pd.read_excel(file)
            df = pd.concat([old_df, new_df], ignore_index=True)
        except:
            print("File exists but is corrupted/empty. Creating new file.")
            df = new_df
    else:
        #-----------File doesn't exits, creating new file---------
        print("File not found. Creating new file.")
        df = new_df    

    #-----------Svaing main file--------------------------
    df.to_excel(file, index=False)
    print(f"\nMain data saved to file {file}")

    #---------------CLEAN DATA----------------
    df_clean = df.copy()

    #Removing Duplicates
    df_clean.drop_duplicates(subset=["Phone"], inplace=True)
    clean_path = file.replace(".xlsx","_cleaned.xlsx")
    df_clean.to_excel(clean_path, index=False)
    print(f"\nClean data saved to {clean_path}")

    #--------------high-quality data------------
    high_quality_df = df_clean[
        (df_clean["Email"] != "Not Available") &
        (df_clean["Website"] != "Not Available") &
        (df_clean["Phone"] != "Not Available")
    ].copy()

    try:
        high_quality_df["Rating"] = high_quality_df["Rating"].astype(float)
        high_quality_df= high_quality_df[high_quality_df["Rating"] >= 3.5]
    except:
        pass

    high_quality_path = file.replace(".xlsx","_high_quality.xlsx")

    #---------------Append High Quality data-------------
    if os.path.exists(high_quality_path):
        try:
            old_hq = pd.read_excel(high_quality_path)
            high_quality_df = pd.concat([old_hq,high_quality_df],ignore_index=True)
            high_quality_df.drop_duplicates(subset=["Phone"],inplace=True)
        except:
            print("High quality file corrupted. Recreating")

    high_quality_df.to_excel(high_quality_path, index=False)
    print(f"High quality leads saved to- {high_quality_path}")

    #------------------Website only data------------------
    df_clean["Website"]=df_clean["Website"].astype(str).str.strip()

    website_df = df_clean[
        (df_clean["Website"] != "Not Available")
    ].copy()

    website_path = file.replace(".xlsx","_with_website.xlsx")

    if os.path.exists(website_path):
        try:
            old_web = pd.read_excel(website_path)
            website_df = pd.concat([old_web, website_df], ignore_index=True)
            website_df.drop_duplicates(subset=["Phone"],inplace=True)
        except:
            print("Website file corrupted. Recreating.")
        
    website_df.to_excel(website_path, index=False)
    print(f"Website leads saved to: {website_path}")