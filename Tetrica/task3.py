# Task 3:
# Мы сохраняем время присутствия каждого пользователя на уроке  виде интервалов. В функцию передается словарь,
# содержащий три списка с таймстемпами (время в секундах): — lesson – начало и конец урока
# — pupil – интервалы присутствия ученика
# — tutor – интервалы присутствия учителя
# Интервалы устроены следующим образом – это всегда список из четного количества элементов. Под четными индексами
# (начиная с 0) время входа на урок, под нечетными - время выхода с урока.
# Нужно написать функцию, которая получает на вход словарь с интервалами и возвращает время общего присутствия ученика
# и учителя на уроке (в секундах).
# Будет плюсом: Написать WEB API с единственным endpoint’ом для вызова этой функции.

# Ответ #1
'''Ответ одной функцией'''


def appearance(intervals):
    new_dict = {}
    for who, time in intervals.items():
        even = []
        odd = []
        counter = 0
        for number in time:
            if counter % 2 == 0:
                even.append(number)
            else:
                odd.append(number)
            counter += 1
        new_dict[who] = sum(odd) - sum(even)
    res_pupil = new_dict.get('pupil')
    res_tutor = new_dict.get('tutor')
    return f'Учитель:{res_tutor} \b Ученик:{res_pupil}'


# print(appearance({
#     'lesson': [1594663200, 1594666800],
#     'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
#     'tutor': [1594663290, 1594663430, 1594663443, 1594666473]
# }))
# # >> OUT: 31...


# Ответ #2
'''WEB API с единственным endpoint’ом'''

from flask import Flask, request

app = Flask(__name__)


@app.route("/appearance/", methods=["GET"])
def appearance():
    intervals = {'pupil': request.args.get('pupil')[1:-1].split(','),
                 'tutor': str(request.args.get('tutor')[1:-1]).split(',')}
    print(intervals)
    new_dict = {}
    for who, time in intervals.items():
        even = []
        odd = []
        counter = 0
        for number in time:
            if counter % 2 == 0:
                even.append(int(number))
            else:
                odd.append(int(number))
            counter += 1
        new_dict[who] = sum(odd) - sum(even)
    res_pupil = new_dict.get('pupil')
    res_tutor = new_dict.get('tutor')
    return f'Учитель:{res_tutor} сек., Ученик:{res_pupil} сек.'


if __name__ == "__main__":
    app.run(debug=True)
