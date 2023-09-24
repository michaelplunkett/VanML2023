import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt


calls = pd.read_csv("data/calls.csv", parse_dates=["DateStart", "TimeStart"])

calls = calls[["callreportnum","DateStart","TimeStart","CityName","ContactMethod","CallLength"]]

# Convert Timestamp to Datetime
calls['DateStart'] = pd.to_datetime(calls['DateStart']).dt.date
calls['TimeofDay'] = pd.to_datetime(calls['TimeStart']).dt.time

# Create time columns
calls['DateTimeStart'] = calls.apply(lambda x: dt.datetime.combine(x.DateStart, x.TimeofDay), axis=1)
calls['AbsoluteTime'] = calls['DateTimeStart'].apply(lambda x: x.timestamp())
calls['TimeofYear'] = calls['DateTimeStart'].apply(lambda x: x.timestamp() - dt.datetime(x.year, 1, 1).timestamp())

calls = calls.drop(['DateStart', 'TimeStart'], axis=1)


# Resolve NA city names
calls.loc[calls["CityName"].isna(),"CityName"] = "Unknown"

# calls['month'] = calls['DateTimeStart'].apply(lambda x: x.month)
# calls['day'] = calls['DateTimeStart'].apply(lambda x: x.day)
# print(calls[calls['month'] + calls['day'] == 2][['DateTimeStart', 'TimeofYear']])


print(calls.dtypes)
print(calls)

calls.to_csv('preprocessed/calls_prep.csv')