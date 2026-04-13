import pandas as pd
def clean_data(df):

    df["Rating"] = pd.to_numeric(df["Rating"], errors= "coerce")

    return df