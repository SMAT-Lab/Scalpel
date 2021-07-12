import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
try:
    xrange
except NameError:
    xrange = range
from __future__ import print_function
dataset = pd.read_csv("csv/enjoy_baseball/result.csv")
dataset.head()
def ip_to_real(x):
    #最初の４文字を取り出せば、年になる
    return float(eval(x))
dataset["HOME_K/9"] = dataset["HOME_K"] * 9 / dataset["HOME_IP"].apply(ip_to_real)
dataset["HOME_BB/9"] = dataset["HOME_BB"] * 9 / dataset["HOME_IP"].apply(ip_to_real)
dataset["HOME_K/BB"] = dataset["HOME_K"] / dataset["HOME_BB"]
dataset["VISITOR_K/9"] = dataset["VISITOR_K"] * 9 / dataset["VISITOR_IP"].apply(ip_to_real)
dataset["VISITOR_BB/9"] = dataset["VISITOR_BB"] * 9 / dataset["VISITOR_IP"].apply(ip_to_real)
dataset["VISITOR_K/BB"] = dataset["VISITOR_K"] / dataset["VISITOR_BB"]
dataset["HOME_K/BB / VISITOR_K/BB"] = dataset["HOME_K/BB"] / dataset["VISITOR_K/BB"]
dataset[dataset["HOME_K/BB / VISITOR_K/BB"] < 1].sort_values(by=["Team", "Year"], ascending=True)
dataset[dataset["Team"] == 'Fighters'][["Year" ,"Team", "HOME_K/BB", "VISITOR_K/BB", "HOME_K/BB / VISITOR_K/BB"]]
dataset[dataset["HOME_K/BB / VISITOR_K/BB"] > 1.2].sort_values(by=["Team", "Year"], ascending=True)
dataset[["Year", "Team", "HOME_K/BB"]].sort_values(by=["HOME_K/BB"], ascending=False)