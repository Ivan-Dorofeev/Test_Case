answer = {
    "displayedName": {
        "displayedName": {
            "value": [
                "Профиль маячковый ПВХ 10 мм L3м"
            ],
            "description": "Полное наименование товара для клиента"
        }
    },
    "stock": {
        "stocks": {
            "34": {
                "2": "35",
                "3": "42",
                "4": "58",
                "5": "57",
                "6": "112",
                "20": "51",
                "22": "78",
                "26": "34",
                "32": "22",
                "35": "358",
                "40": "28",
                "43": "68",
                "45": "58",
                "49": "31",
                "51": "29",
                "56": "42",
                "62": "26",
                "64": "0",
                "65": "57",
                "86": "15",
                "114": "41",
                "117": "46",
                "143": "46",
                "162": "4",
                "171": "0",
                "176": "12"
            }
        }
    }
}

# 1. получить название товара
name = answer["displayedName"]["displayedName"]["value"][0]
print(name)
# 2. получить массив номеров магазинов, в которых есть товары в наличии
stocks_empty = dict(answer["stock"]["stocks"]["34"])
res = []
for score, quantity in stocks_empty.items():
    if int(quantity) > 0:
        res.append(score)
print(res)
# 3. найти максимальное количество товара в регионе, вернуть это количество и номер магазина
max_quantity = 0
name_score = ""
stocks_empty = dict(answer["stock"]["stocks"]["34"])
for score, quantity in stocks_empty.items():
    stocks_empty.update({score: int(quantity)})
    if int(quantity) > max_quantity:
        max_quantity = int(quantity)
        name_score = score
res = f'Магазин - {name_score}, количество {max_quantity}'
print(res)
