"""
All things bot can do are here
"""

from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy import exc

class AnimeBot:
    def __init__(self, database='sqlite:///animeTgBot.db'):
        self.engine = create_engine(database)
        self.connection = self.engine.connect()

    def select_random_anime(self, media):
        sql_content_query = text(f"""
                                 SELECT * FROM {media}
                                 ORDER BY RANDOM() LIMIT 1
                                 """)

        content = self.connection.execute(sql_content_query).fetchone()

        return content_to_dict(content)

    def select_random_by_genre(self, media, genre='Комедии'):
        sql_content_query = text(f"""
                                 SELECT * FROM {media}
                                 WHERE genre LIKE '%{genre}%'
                                 ORDER BY RANDOM() LIMIT 1
                                  """)

        content = self.connection.execute(sql_content_query).fetchone()

        return content_to_dict(content)

    def select_top10_anime(self, media):
        sql_content_query = text(f"""
                               SELECT * FROM {media}
                               ORDER BY rating DESC LIMIT 10
                               """)

        top10_content_list = self.connection.execute(sql_content_query).fetchall()
        content_list = [content_to_dict(content_set) for content_set in top10_content_list]

        return content_list

    def select_by_name(self, name_to_find):
        try:
            sql_search_serials = text(f"""
                                       SELECT * FROM SERIALS
                                       WHERE upper(name) LIKE upper('%{name_to_find}%')
                                       """)

            sql_search_films = text(f"""
                                    SELECT * FROM FILMS
                                    WHERE upper(name) LIKE upper('%{name_to_find}%')
                                    """)

            content_serials = self.connection.execute(sql_search_serials).fetchmany(10)
            content_films = self.connection.execute(sql_search_films).fetchmany(10)

            if content_serials or content_films:
                return content_serials + content_films
            return None

        except exc.OperationalError:
            return None

    def select_ongoings(self):
        sql_content_query = text(f"""
                                 SELECT * FROM SERIALS
                                 WHERE genre is 'Текущие сезоны (Онгоинги)'
                                 """)
        content = self.connection.execute(sql_content_query).fetchmany(10)

        return [content_to_dict(anime) for anime in content]

    def select_by_id(self, media, id):
        sql_content_query = text(f"""
                                 SELECT * FROM {media}
                                 WHERE id = '{id[4:]}'
                                 """)
        content = self.connection.execute(sql_content_query).fetchone()

        return content_to_dict(content)

    def select_anons(self):
        sql_content_query = text(f"""SELECT * FROM ANONS""")
        content = self.connection.execute(sql_content_query).fetchall()

        return [content_to_dict(anime) for anime in content]


def content_to_dict(content: set) -> dict:
    content_dict = {'name': content[1],
                    'tag':content[2],
                    'link': content[3],
                    'genre': content[4],
                    'rating': content[5],
                    'description': content[6],
                    'image_url':content[7],
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

def content_to_html_short(anime):
    return f'▶{anime["name"]}(/{anime["tag"]}id{anime["id"]}) - {anime["rating"]}⭐\n'
