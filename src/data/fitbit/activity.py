import pandas as pd


def sum_by_treatment_date(df, variable):
    df = df.set_index("dateTime").groupby(pd.Grouper(freq="D")).sum().reset_index()
    df = df.rename(columns={"dateTime": "treatment_date", "value": variable})
    df.treatment_date = df.treatment_date.dt.date
    return df
