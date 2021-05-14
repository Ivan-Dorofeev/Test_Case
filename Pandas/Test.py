import datetime

import pandas as pd
import numpy as np

dates = pd.date_range(datetime.datetime.today(), periods=7)
# print(dates)

df = pd.DataFrame(np.random.randn(7, 4), index=dates, columns=list('ABCD'))
print(df)
print(df.to_numpy())
print(df.describe())
print(df.T)
