import requests
from bs4 import BeautifulSoup

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
        link = a_tag.get('href')       # link on anime

        ul_des_div = div.find('div', {"class": "kino-inner clearfix"})
        ul_dict = ul_des_div.find('ul')
        genre = ul_dict.find('a').text  # anime`s genre

        if len(ul_dict.find_all('li')) == 5:
            ongoing_status = True
        else:
            ongoing_status = False  # ongoing or not

        ul_raiting = div.find('ul')
        raiting = ul_raiting.find('li').text    # rating / 100

        description = ul_des_div.find('div', {'class':'kino-text'}).find('div').text  # short description

        image = 'http://baza1.animevost.tv' + ul_des_div.find('img')['src']

        return_list.append({
            'name':name,
            'link':link,
            'genre':genre,
            'ongoing_status':ongoing_status,
            'raiting':raiting,
            'description':description,
            'image':image
        })

    return return_list



