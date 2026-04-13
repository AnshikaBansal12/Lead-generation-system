def analyzer_data(df):
    summary = {}

    #Business Type
    summary["business_type"]= df["Business Type"].iloc[0]

    #Basic Matrics
    summary["total_leads"] = len(df)
    summary["cities"]=df["City"].nunique()
    summary["avg_rating"]= df["Rating"].mean()

    summary["website_count"]=(df["Website"] != "Not Available").sum()
    summary["email_count"]=(df["Email"] != "Not Available").sum()

    #city-wise Analysis
    city_analysis = df.groupby("City").agg({
        "Company": "count",
        "Rating": "mean"
    }).rename(columns={"Company": "Total Leads"})

    summary["city_analysis"] = city_analysis

    #Top Companies
    top_companies = df[df["Rating"] >= 4].sort_values(by="Rating", ascending= False)
    summary["top_companies"] = top_companies

    return summary