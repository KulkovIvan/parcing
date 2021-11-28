# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы
# получаем должность) с сайтов HH(обязательно) и/или Superjob(по желанию).
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# -Наименование вакансии.
# -Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# -Ссылку на саму вакансию.
# -Сайт, откуда собрана вакансия.


import requests
from bs4 import BeautifulSoup
from pprint import pprint

page = 0
id = 0
running = True
while running:
    url = 'https://hh.ru/'
    params = {'text': 'python', 'page': page}
    headers = {'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    try:
        next = dom.find('div', {'class': ['pager']}).find('a', {'class': ['bloko-botton']}).get('href')
    except:
        running = False


    vacancies = dom.find_all('div', {'vacancy-serp-item'})

    list_of_vacancies = []

    for vacancy in vacancies:
        vacancy_data = {}
        name = vacancy.find('a').text
        link = vacancy.find('a', {'class': ['bloko-link']}).get('href')
        try:
            price = vacancy.find('div', {'class': 'vacancy-serp-item_sidebar'}).find('span').text.replace('\u202f', ' ')
            price_str = int(price[-4:])
            price = int(price[:-4])
            if '-' in price:
                price_list = price.split('-')
                price_min = int(price_list[0])
                price_max = int(price_list[1])
            else:
                price_min = int(price)
                price_max = None
        except:
            price = None
            price_str = None
            price_min = None
            price_max = None

        id += 1

        vacancy_data['name'] = name
        vacancy_data['price_min'] = price_min
        vacancy_data['price_max'] = price_max
        vacancy_data['price_str'] = price_str
        vacancy_data['link'] = link
        vacancy_data['base'] = url
        vacancy_data['id'] = id

        list_of_vacancies.append(vacancy_data)
    pprint(list_of_vacancies)
    page +=1


