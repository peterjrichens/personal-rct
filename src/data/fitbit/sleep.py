import glob2
import pandas as pd
from datetime import datetime, timedelta, time

date_format = "%Y-%m-%d"
datetime_format = "%Y-%m-%dT%H:%M:%S.000"


def filter_main_sleep(df):
    return df[df.mainSleep == True]


def add_treatment_date(df):
    df["treatment_date"] = pd.to_datetime(df.dateOfSleep).dt.date - timedelta(days=1)
    return df


def add_sleep_start_time(df):
    """timedelta in minutes between sleep start time and
    expected sleep start time"""

    def _start_expected_delta(row):
        start_time = datetime.strptime(row["startTime"], datetime_format)
        date = row["treatment_date"]
        expected_time = time(23, 0, 0)
        expected_start_time = datetime.combine(row["treatment_date"], expected_time)
        return (start_time - expected_start_time).total_seconds() / 60

    df["sleep_start_time"] = df.apply(_start_expected_delta, axis=1)
    return df


def add_total_sleep_duration(df):
    df["total_sleep_duration"] = df.minutesAsleep
    return df


def add_stage_duration(df):
    def _minutes_by_stage(data, stage):
        summary = data["summary"]
        if stage in summary:
            return summary[stage]["minutes"]
        return 0

    df["deep_sleep_duration"] = df.levels.apply(lambda x: _minutes_by_stage(x, "deep"))
    df["rem_sleep_duration"] = df.levels.apply(lambda x: _minutes_by_stage(x, "rem"))
    return df


def select_columns(df):
    return df[
        [
            "treatment_date",
            "total_sleep_duration",
            "deep_sleep_duration",
            "rem_sleep_duration",
            "sleep_start_time",
        ]
    ].drop_duplicates()


def filter_sleep_score(df):
    df["treatment_date"] = pd.to_datetime(df.timestamp).dt.date - timedelta(days=1)
    df["composite_sleep_score"] = df.overall_score * 1.0
    return df[["treatment_date", "composite_sleep_score"]]
