"""
All things bot can do are here
"""

from sqlalchemy import create_engine
from sqlalchemy.sql import text


class AnimeBot:
    def __init__(self, database='sqlite:///animeTgBot.db'):
        self.engine = create_engine(database)
        self.connection = self.engine.connect()

    def choose_random(self, media):
        sql_content_query = text(f'SELECT * FROM \'{media}\''
                                 f'ORDER BY RANDOM() LIMIT 1')  # sql query to choose random film or serial

        content = self.connection.execute(sql_content_query).fetchone()
        content_dict = content_to_dict(content)

        return content_dict

    def choose_random_by_genre(self, media, genre='Комедии'):
        sql_random_query = text(f'SELECT * FROM \'{media}\''
                                f'WHERE genre LIKE \'%{genre}%\''
                                f'ORDER BY RANDOM() LIMIT 1')

        content = self.connection.execute(sql_random_query).fetchone()
        content_dict = content_to_dict(content)

        return content_dict

    def choose_top10(self, media, genre = None):
        if genre:
            sql_top_10_query = text(f'SELECT * FROM {media} '
                                    f'WHERE genre LIKE \'%{genre}%\''
                                    f'ORDER BY rating DESC LIMIT 10')
        else:
            sql_top10_query = text(f'SELECT * FROM \'{media}\''
                                   f'ORDER BY rating DESC LIMIT 10')

        top10_content_list = self.connection.execute(sql_top10_query).fetchall()
        content_list = []

        for content_set in top10_content_list:
            content_dict = content_to_dict(content_set)
            content_list.append(content_dict)

        return content_list

    def find_by_name(self, name_to_find):
        sql_search_query = text(f'SELECT * FROM \'SERIALS\' '
                                 f'WHERE UPPER(name) LIKE UPPER(\'%{name_to_find}%\')'
                                 f'UNION '
                                 f'SELECT * FROM \'FILMS\' '
                                 f'WHERE UPPER(name) LIKE UPPER(\'%{name_to_find}%\')')

        content = self.connection.execute(sql_search_query).fetchall()
        if content:
            content_list = []
            for anime in content:
                content_dict = content_to_dict(anime)
                content_list.append(content_dict)
            return content_list
        return 'Извини, не смог найти ничего похожего'

    def select_ongoins(self):
        sql_ongiongs_query = text(f'SELECT * FROM SERIALS '
                                  f'WHERE genre is \'Текущие сезоны (Онгоинги)\'')

        serial = self.connection.execute(sql_ongiongs_query).fetchall()
        serials_list = []
        for ser in serial:
            serials_list.append(content_to_dict(ser))

        return serials_list

    def choose_by_id(self, media, id):
        sql_query = text(f'SELECT * FROM {media} '
                         f'WHERE id = \'{id[4:]}\'')

        content = self.connection.execute(sql_query).fetchone()
        content_dict = content_to_dict(content)

        return content_dict


def content_to_dict(content: set) -> dict:
    content_dict = {'name': content[1],
                    'link': content[2],
                    'genre': content[3],
                    'rating': content[4],
                    'description': content[5],
                    'image_url':content[6],
                    'id':content[0]}

    return content_dict


def content_to_html(content: dict) -> str:
    html_text = f'[⁠]({content["image_url"]})' \
                f'----------------------------\n' \
                f'🎬[{content["name"]}]({content["link"]})\n' \
                f'⭐{content["rating"]}\n' \
                f'📄{content["genre"]}\n' \
                f'-------------------------------\n' \
                f'✍{content["description"][0:350] + "..."}\n'
    return html_text

