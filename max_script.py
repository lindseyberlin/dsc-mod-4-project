import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("zillow_data.csv")

for i in range(df.shape[0]):
    first_region_info = df[df.iloc[i].index[:7]].iloc[i]
    first_dates = df[df.iloc[i].index[7:]].iloc[i]
    plt.figure(figsize=(16,8))
    plt.title(str(first_region_info))
    plt.plot(first_dates)
    plt.xticks(first_dates.index[::10], rotation=90)
    plt.xlabel("Date")
    plt.ylabel("Average Cost of a House?")
plt.show()