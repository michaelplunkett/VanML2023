import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt


calls = pd.read_csv("data/calls.csv", parse_dates=["DateStart", "TimeStart"])

calls = calls[["callreportnum", "DateStart", "TimeStart",
               "CityName", "ContactMethod", "CallLength"]]


# add code to each city
calls.loc[calls["CityName"].isna(), "CityName"] = "Unknown"
city_to_code = pd.DataFrame(calls["CityName"].unique())
city_to_code["code"] = pd.Series(range(0, 514))
city_to_code.columns = ["CityName", "code"]
calls["CityNameCode"] = calls["CityName"].map(
    lambda x: city_to_code.loc[city_to_code["CityName"] == x, "code"].iloc[0])

# turn contact methods into code
# convert na IN contactMethod to "Unknown"
calls.loc[calls["ContactMethod"].isna(), "ContactMethod"] = "Unknown"
contactMethod_to_code = pd.DataFrame(calls["ContactMethod"].unique())

contactMethod_to_code["code"] = pd.Series(range(0, 8))
contactMethod_to_code.columns = ["ContactMethod", "code"]
calls["ContactMethod_code"] = calls["ContactMethod"].map(
    lambda x: contactMethod_to_code.loc[contactMethod_to_code["ContactMethod"] == x, "code"].iloc[0])


# Convert Timestamp to Datetime
calls['DateStart'] = pd.to_datetime(calls['DateStart']).dt.date
calls['TimeStart'] = pd.to_datetime(calls['TimeStart']).dt.time

# Create time columns
calls['DateTimeStart'] = calls.apply(
    lambda x: dt.datetime.combine(x.DateStart, x.TimeStart), axis=1)
calls['AbsoluteTime'] = calls['DateTimeStart'].apply(lambda x: x.timestamp())
calls['TimeofYear'] = calls['DateTimeStart'].apply(
    lambda x: x.timestamp() - dt.datetime(x.year, 1, 1).timestamp())
calls['TimeofDay'] = calls['DateTimeStart'].apply(
    lambda x: x.timestamp() - dt.datetime(x.year, x.month, x.day).timestamp())


calls = calls.drop(['DateStart', 'TimeStart'], axis=1)

# Resolve NA city names
calls.loc[calls["CityName"].isna(), "CityName"] = "Unknown"

# calls['month'] = calls['DateTimeStart'].apply(lambda x: x.month)
# calls['day'] = calls['DateTimeStart'].apply(lambda x: x.day)
# print(calls[calls['month'] + calls['day'] == 2][['DateTimeStart', 'TimeofYear']])

print(calls.dtypes)
print(calls)

calls.to_csv('preprocessed/calls_prep.csv')
