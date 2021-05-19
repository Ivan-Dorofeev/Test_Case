import os
import sys

import pandas as pd

my_path = sys.argv[1]
name_sl = {}
result = {}
no_name_list = []


def update_departmen():
    # записываем в словарь сотрудников департамента из файла
    ex_data = pd.read_excel(os.path.join(my_path, 'name_department.xlsx'))
    names = list(ex_data.to_dict()['name'].values())
    sl = list(ex_data.to_dict()['SL'].values())
    for i in range(0, len(names)):
        name_sl[names[i]] = sl[i]
        result[sl[i]] = 0
    return name_sl


def get_percents():
    #  вычисляем проценты по каждому сотруднику из файлов и записываем с "result"
    for file in os.listdir(my_path):
        if file.startswith('2021'):
            file_pd_data = pd.read_excel(file, header=None)
            pivot_data = pd.pivot_table(file_pd_data, index=0, values=3, aggfunc=sum)
            for i, j in pivot_data.items():
                for key, value in j.items():
                    if key in name_sl.keys():
                        result[name_sl[key]] += value
                    else:
                        if key != 'Owner':
                            no_name_list.append(key)
    sum_value = sum(result.values())
    for keys, value in result.items():
        result[keys] = str(round(value / sum_value * 100, 2)) + ' %'
    result[' '] = ' '
    result['Нет в списке'] = ', '.join(no_name_list)
    return result


def write_to_file():
    # записываем в новый файл
    df = pd.DataFrame(data=result, index=['Проценты']).T
    df.to_excel('department_percents.xlsx', sheet_name='Проценты')
    print(df)



if __name__ == '__main__':
    update_departmen()
    get_percents()
    write_to_file()
