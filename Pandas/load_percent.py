import datetime
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = os.path.join('task')
name_department_list = []


def update_name_department():
    name_department = pd.read_excel('task/2021_3.xlsx')
    print(name_department)


update_name_department()
