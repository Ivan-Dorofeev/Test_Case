import datetime
from pprint import pprint

from data import example_data


def __count_referrals(client, referrals_dict):
    """
    Рекурсивно собирает информацию о рефералах клиента.
    Возвращает список с рефералами, у которых 2+ приглашения
    """

    refferals_with_2_reffs = []
    for ref in referrals_dict[client]['referrals_ids']:
        if referrals_dict.get(ref) and len(referrals_dict[ref]['referrals_ids']) >= 2:
            refferals_with_2_reffs.append(ref)
            refferals_with_2_reffs += __count_referrals(ref, referrals_dict)
    return refferals_with_2_reffs


def users_with_bonus(data):
    """Возвращает список пользователей, получивших бонус и их рефералов
        user_id, [referrals]
    """

    one_month_ago_date = datetime.date.today() - datetime.timedelta(days=30)

    # собираем данные под условия для 1 уровня
    inviters_with_data_1_level = {}
    for user_id, user_data in data.items():
        # условие по дате
        if user_data['purchase_date'] >= one_month_ago_date:
            # условие по цене
            if user_data['package'] >= 1500:
                if not user_data['inviter'] in inviters_with_data_1_level:
                    inviters_with_data_1_level[user_data['inviter']] = {'referrals_ids':[user_id] }
                else:
                    if not user_id in inviters_with_data_1_level[user_data['inviter']]['referrals_ids']:
                        inviters_with_data_1_level[user_data['inviter']]['referrals_ids'].append(user_id)

    # рекурсивно проходимся по рефералам
    res_dict = {}
    for user_id, inviters in inviters_with_data_1_level.items():
        # отсеиваем, где < 2 рефералов
        if len(inviters['referrals_ids']) >= 2:
            res_dict[user_id] = []
            res_dict[user_id] += __count_referrals(user_id,inviters_with_data_1_level)

    # отсеиваем тех, кто не попал под условия
    res_dict = dict(filter(lambda x: len(x) >= 2, res_dict.items()))

    # вывод в консоль
    for user_id, inviters in res_dict.items():
        if len(inviters) >= 2:
            print(f'{user_id} : {inviters}')




if __name__ == '__main__':
    users_with_bonus(example_data)
