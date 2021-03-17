# Task 2:
# В нашей школе мы не можем разглашать персональные данные пользователей, но чтобы преподаватель и ученик смогли
# объяснить нашей поддержке, кого они имеют в виду (у преподавателей, например, часто учится несколько Саш), мы
# генерируем пользователям уникальные и легко произносимые имена. Имя у нас состоит из прилагательного, имени животного
# и двузначной цифры. В итоге получается, например, "Перламутровый лосось 77". Для генерации таких имен мы и решали
# следующую задачу:
# Получить с русской википедии список всех животных (Категория:Животные по алфавиту) и вывести количество животных на
# каждую букву алфавита. Результат должен получиться в следующем виде:
#  А: 642
# Б: 412
# В:....

from collections import Counter
from urllib.parse import urljoin

from lxml import *
import requests
from bs4 import BeautifulSoup

first = 'https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'

animals = []


def parsing_animals(url):
    """Находим имена животных на сайте"""

    response = requests.get(url)
    if response.status_code == 200:
        html_doc = BeautifulSoup(response.text, 'lxml')
        links = html_doc.find_all('a')
        write_to_list = False
        for link in links:
            if 'Следующая страница' in link.text:
                if not write_to_list:
                    write_to_list = True
                else:
                    write_to_list = False
            if write_to_list and 'Следующая страница' and 'Предыдущая страница' not in link.text:
                if 'Aaaaba' in link.text:
                    return False
                animals.append(link.text[0:1])
    else:
        print('Ooooooooooooooops', response.status_code)
    return True


def parsing_next_page(url):
    """Находим следующщую страницу на сайте"""

    response = requests.get(url)
    if response.status_code == 200:
        html_doc = BeautifulSoup(response.text, 'html.parser')
        links = html_doc.find_all('a')
        for link in links:
            if 'Следующая страница' in link.text:
                return str(link.attrs['href'])


count = 0
parsing_animals(first)
while True:
    count += 1
    new_url = urljoin('https://ru.wikipedia.org', parsing_next_page(first))
    if parsing_animals(new_url) is False:
        break
    first = new_url
    print('step', count)
counter_animals = Counter(animals)
sort_counter_animal = sorted(counter_animals)
list_keys = list(counter_animals.keys())
list_keys.sort()
for word in list_keys:
    print(word, ':', counter_animals[word])
