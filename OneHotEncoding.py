import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder

calls = pd.read_csv("preprocessed/calls_prep.csv")

cityCounts = calls.groupby('CityName').count()["callreportnum"]
cityCounts = cityCounts.sort_values(ascending=False)
calls["NewCityName"] = np.where(cityCounts[calls["CityName"]] < 500, 'Other', calls["CityName"])

plt.plot(cityCounts.index, cityCounts.values, 'k-')
plt.xticks([], [])
plt.savefig("figures/CityCounts.png")

# print(cityCounts.values)
# print(cityCounts)
# print(calls[["CityName", "NewCityName"]])
# print(cityCounts["Winnipeg"])


# One hot encode city names
OHE = OneHotEncoder(sparse_output=False)


OHE.fit(calls["NewCityName"].to_numpy().reshape(-1, 1))
OHE_CityNames = pd.DataFrame(OHE.transform(calls["NewCityName"].to_numpy().reshape(-1, 1)), columns=OHE.get_feature_names_out(), dtype=int)

OHE.fit(calls["ContactMethod"].to_numpy().reshape(-1, 1))
OHE_ContactMethods = pd.DataFrame(OHE.transform(calls["ContactMethod"].to_numpy().reshape(-1, 1)), columns=OHE.get_feature_names_out(), dtype=int)

# print(OHE_CityNames)
# print(OHE_ContactMethods)

calls.drop(["Unnamed: 0", "callreportnum", "DateTimeStart", "CityName", "NewCityName", "ContactMethod"], axis=1, inplace=True)
calls = pd.concat([calls, OHE_CityNames, OHE_ContactMethods], axis=1)

# print(calls)

calls.to_csv('preprocessed/calls_OHE.csv')