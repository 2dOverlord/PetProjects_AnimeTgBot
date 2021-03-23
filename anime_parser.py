import requests
from bs4 import BeautifulSoup

GENRES = {'Боевые искусства', 'Война', 'Детектив', 'Драма', 'История', 'Киберпанк', 'Комедии', 'Махо-сёдзё',
          'Меха', 'Мистика', 'Музыкальный', 'Пародии', 'Повседневность', 'Приключения', 'Романтика', 'Самураи' 
          'Сёдзё', 'Сёдзё-ай', 'Сёнен', 'Сёнен-ай', 'Спорт', 'Триллер', 'Ужасы', 'Фантастика', 'Фэнтези', 'Школа',
          'Текущие сезоны (Онгоинги)', 'Этти'
          }


def get_request(url):
    """
    Getting request from site

    :param url:string
    :return: request:string
    """
    request = requests.get(url).text
    return request


def parse_site_page(url):
    """
    Parsing animevost site pages

    :param url: string(url of page)
    :return:a_tags: list with a tags
    """

    import re

    url_request = get_request(url)
    soup = BeautifulSoup(url_request, 'html.parser')

    pattern = re.compile(r'entry+')
    div_tags = soup.find_all('div', id=pattern)

    return_list = []
    for div in div_tags:
        a_tag = div.find('a')
        name = a_tag.find('h2').text
        link = a_tag.get('href')   # link on anime

        anime_request = get_request(link)
        anime_soap = BeautifulSoup(anime_request, 'html.parser')  # html of anime page

        description = anime_soap.find('div', {'class': 'kino-desc full-text clearfix noselect'}).text.replace('\n', '')

        anime_ul = anime_soap.find('ul', {'class': 'kino-lines ignore-select'})
        ul_links = anime_ul.find_all('a')
        genre = ' '.join(a.text for a in ul_links if a.text in GENRES)

        rating = anime_soap.find('ul', {'class': 'unit-rating'}).find('li').text

        image_url = 'http://baza1.animevost.tv/' + anime_soap.find('a', {'class': 'highslide'}).find('img').get('src')

        return_list.append({
            'name': name,
            'link': link,
            'genre': genre,
            'rating': rating,
            'description': description,
            'image': image_url
        })

    return return_list
