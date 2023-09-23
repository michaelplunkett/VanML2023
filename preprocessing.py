import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


calls = pd.read_csv("data/calls.csv", parse_dates=["DateStart", "TimeStart"])

calls = calls[["callreportnum","DateStart","TimeStart","CityName","ContactMethod","CallLength"]]
calls['TimeStart'] = calls['TimeStart'].dt.time
calls.loc[calls["CityName"].isna(),"CityName"] = "Unknown"
calls["year"] = pd.to_datetime(calls["DateStart"]).dt.strftime("%Y")

print(calls)

calls.to_csv('preprocessed/calls_prep.csv')