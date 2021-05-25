import glob2
import pandas as pd
from datetime import datetime, timedelta, time

date_format = "%Y-%m-%d"


def load_data(data_dir, data_path):
    dfs = []
    for f in glob2.iglob(f"{data_dir}/{data_path}"):
        if f.endswith(".json"):
            dfs.append(pd.read_json(f))
        else:
            dfs.append(pd.read_csv(f))
    return pd.concat(dfs)


def get_treatment_df(start_date, end_date, treatment_dict):
    df = pd.date_range(start_date, end_date).to_frame().reset_index()
    df["treatment_date"] = df["index"].dt.date
    treatment_map = {}
    for treatment, date_list in treatment_dict["dates"].items():
        for d in date_list:
            treatment_map[datetime.strptime(d, date_format)] = treatment
    df["treatment"] = df.treatment_date.map(treatment_map)
    exclude = [
        datetime.strptime(d, date_format).date()
        for d in treatment_dict["exclude_dates"]
    ]
    df = df[~df.treatment_date.isin(exclude)]
    experiment_start = df[df.treatment.notnull()].treatment_date.min()
    experiment_end = df[df.treatment.notnull()].treatment_date.max()
    df = df[df.treatment_date <= experiment_end]
    baseline_end = df[df.treatment.isnull()].treatment_date.max()
    assert baseline_end + timedelta(days=1) == experiment_start
    df["experiment_active"] = df.treatment_date >= experiment_start
    assert df[df.experiment_active == True].treatment.notnull().all()
    assert df[df.experiment_active == False].treatment.isnull().all()
    return df[["treatment_date", "experiment_active", "treatment"]]


def add_day_of_week(df):
    df["day_of_week"] = pd.DatetimeIndex(df.treatment_date).day_name()
    return df


def validate(df):
    assert len(df) == df.treatment_date.nunique()
    return df
