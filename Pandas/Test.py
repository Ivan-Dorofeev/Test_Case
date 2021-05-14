import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dates = pd.date_range(datetime.datetime.today(), periods=7)
# print(dates)

df = pd.DataFrame(np.random.randint(1, 10, None, int), index=dates, columns=list('ABCD'))
# print(df)
# print(df.to_numpy())
# print(df.describe())
# print(df.T)
# df["E"] = [1, 2, 3, 4, 5, 6, 7]
# print(df[df["E"].isin([2, 3, 4])])
plt.close("all")

df2 = pd.Series(np.random.randint(0, 100, len(dates)), index=dates)
df2 = df2.cumsum()
df2.plot()
