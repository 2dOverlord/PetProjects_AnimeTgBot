# CREATING SQLITE DATABASE

import sqlalchemy
from anime_parser import *

from sqlalchemy import create_engine
engine = create_engine('sqlite:///animeTgBot.db', echo=True)

from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()


serials_table = Table('SERIALS', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('name', String),
                     Column('link', String),
                     Column('genre', String),
                     Column('rating', Integer),
                     Column('description', String))

films_table = Table('FILMS', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('name', String),
                     Column('link', String),
                     Column('genre', String),
                     Column('rating', Integer),
                     Column('description', String))

metadata.create_all(engine)

def filling_serials_table():
    insert_serials_stmt = serials_table.insert(bind = engine)
    for i in range(1, 72):  # How many pages on site
        link = f'http://baza.animevost.tv/anime-tv/page/{i}/'
        for serial in parse_site_page(link):
            insert_serials_stmt.execute(name = serial['name'],
                                        link = serial['link'],
                                        genre = serial['genre'],
                                        rating = int(serial['raiting']),
                                        description = serial['description'])

def filling_films_table():
    insert_films_stmt = films_table.insert(bind = engine)
    for i in range(1, 24):
        link = f'http://baza.animevost.tv/polnometrazhnyj/page/{i}/'
        for film in parse_site_page(link):
            insert_films_stmt.execute(name = film['name'],
                                      link = film['link'],
                                      genre = film['genre'],
                                      rating = int(film['raiting']),
                                      description = film['description'])

def filling_ongoings():
    insert_serials_stmt = serials_table.insert(bind=engine)
    for i in range(1, 6):
        link = f'http://baza.animevost.tv/ongoing/page/{i}/'
        for serial in parse_site_page(link):
            insert_serials_stmt.execute(name=serial['name'],
                                        link=serial['link'],
                                        genre=serial['genre'],
                                        rating=int(serial['raiting']),
                                        description=serial['description'])


if __name__ == '__main__':
    filling_serials_table()
    filling_films_table()
    filling_ongoings()