"""
All things bot can do are here
"""

from sqlalchemy import create_engine
from sqlalchemy.sql import text

class AnimeBot:
    def __init__(self, database = 'sqlite:///animeTgBot.db'):
        """

        :param database: link on database(sqlite:///animeTgBot.db in my case)
        """
        self.engine = create_engine(database)
        self.connection = self.engine.connect()

    def choose_random(self, media):
        """
        This function choose one random serial or film

        :param media: table name in sql database(SERIALS or FILMS in my case)
        :return: set of serial or film values(name, link, genre, rating, description)
        """

        sql_content_query = text(f'SELECT * FROM \'{media}\''
                               f'ORDER BY RANDOM() LIMIT 1')     # sql query to choose random film or serial

        content = self.connection.execute(sql_content_query).fetchone()

        return content

    def choose_top10(self, media):
        """
        This function choose top 10 serials or films
        :param media: table name in sql database(SERIALS or FILMS in my case)
        :return: list of sets
        """
        sql_top10_text = text(f'SELECT * FROM {media} ' \
                              f'ORDER BY rating DESC')
        top10_list = self.connection.execute(sql_top10_text).fetchmany(10)
        return top10_list

    def choose_random_by_genre(self, media, genre='Комедии'):
        """
        Same as choose_random, but you can also enter your genre
        """
        from random import choice as random_choice

        sql_max_text = text(f'SELECT * FROM {media} '
                            f'WHERE genre = \'{genre}\'')

        random_list = self.connection.execute(sql_max_text).fetchall()
        serial = random_choice(random_list)

        return serial

    def choose_top10_by_genre(self, media, genre='Драма'):
        """
        Save as choose_top10, but you can also enter your genre
        """
        sql_max_text = text(f'SELECT * FROM {media} '
                            f'WHERE genre = \'{genre}\''
                            f'ORDER BY rating DESC')

        rating_list = self.connection.execute(sql_max_text).fetchmany(10)
        return rating_list

    def find_by_name(self, media, name):
        """
        Finding film or serial, which title is close to given parametr name
        :param name: Name of anime, string
        """
        sql_find_text = text(f'SELECT * FROM {media} '
                             f'WHERE UPPER(name) LIKE UPPER(\'%{name}%\')')

        serial = self.connection.execute(sql_find_text).fetchall()
        return serial

    def select_ongoins(self):
        sql_find_text = text(f'SELECT * FROM SERIALS '
                             f'WHERE genre is \'Текущие сезоны (Онгоинги)\'')
        serials = self.connection.execute(sql_find_text).fetchall()
        return serials
