import cprint
from bs4 import BeautifulSoup
import re
import requests

url1 = 'https://www.wildberries.ru/catalog/obuv/muzhskaya'
url2 = 'https://www.wildberries.ru/catalog/obuv/zhenskaya/baletki-i-cheshk'
url3 = 'https://www.wildberries.ru/catalog/dom-i-dacha/bakaleya/konfety'


def goods(page):
    """Получаем с сайта артикул, описание, наименование товара"""
    goods_dict = {}
    counter = 0
    soup = page.find_all(class_="ref_goods_n_p j-open-full-product-card")
    for goods in soup:
        counter += 1
        good = goods.find_all(class_='l_class')
        good_soup = re.findall(r'\w+', str(good))
        article = good_soup[4][1::]
        name = good_soup[8]
        descrition = good_soup[7]
        goods_dict[article] = [name, descrition]
    print(goods_dict)
    return goods_dict


def category(page):
    """Получаем с сайта Категорию товаров"""
    soup = page.find(class_="catalog-title")
    category_soup = re.split(r'[><]', str(soup))
    category_good = category_soup[-3]
    print('Категория товара: ', category_good)
    return category


def parser(url):
    """Проверяем страницу и запускаем парсер"""
    response = requests.get(url1)
    if response.status_code == 200:
        html_page = BeautifulSoup(response.text, 'html.parser')
        category(html_page)
        goods(html_page)
    else:
        print(f'Oops, ошибка запроса на сайт - {response.status_code}')


if __name__ == '__main__':
    parser(url1)