import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

calls = pd.read_csv("preprocessed/calls_OHE.csv")

X = calls.drop(["Unnamed: 0", "CallLength"], axis=1)
y = calls["CallLength"]

X_train, X_test, y_train, y_test = train_test_split(X, y)

model = make_pipeline(
    StandardScaler(),
    MLPRegressor()
)

print("Fitting model...")
model.fit(X_train, y_train)

print("Model score:")
print(model.score(X_test, y_test))