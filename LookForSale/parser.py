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
    base_url = page.find('base').get('href')
    counter = 0
    soup = page.find_all(class_="ref_goods_n_p j-open-full-product-card")
    for goods in soup:
        counter += 1
        href = goods.get('href')
        # заходим на страницу товара
        good_page = base_url + href[1::]
        if requests.get(good_page).status_code == 200:
            good_page_soup = BeautifulSoup(requests.get(good_page).text, 'html.parser')
            # находим наименование товара
            good_soup = good_page_soup.find_all(class_="brand-and-name j-product-title")
            good_soup_re = re.split(r'[><]', str(good_soup))
            name = good_soup_re[4] + " " + good_soup_re[8]
            # находим артикул товара
            article_soup = good_page_soup.find_all(class_="article")
            article_soup_re = re.split(r'[><]', str(article_soup))
            article = article_soup_re[4]
            # находим описание товара
            description_soup = good_page_soup.find_all("p", {'data-link': "text{:productCard.description}"})
            description_soup_re = re.split(r'[><]', str(description_soup))
            description = description_soup_re[2]
            goods_dict[counter] = [name, article, description]
        else:
            print('Opps, нет такой страницы ТОВАРА')
    for k, v in goods_dict.items():
        print(f'Место {k}: {v}')
    return goods_dict


def category(page):
    """Получаем с сайта Категорию товаров"""
    soup = page.find(class_="catalog-title")
    category_soup = re.split(r'[><]', str(soup))
    category_good = category_soup[-3]
    print('Категория товара: ', category_good)
    print('')
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
