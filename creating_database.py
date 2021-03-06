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
                     Column('tag', String),
                     Column('link', String),
                     Column('genre', String),
                     Column('rating', Integer),
                     Column('description', String),
                     Column('image_url', String))

films_table = Table('FILMS', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('name', String),
                     Column('tag', String),
                     Column('link', String),
                     Column('genre', String),
                     Column('rating', Integer),
                     Column('description', String),
                     Column('image_url', String))

anons_table = Table('ANONS', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('name', String),
                     Column('tag', String),
                     Column('link', String),
                     Column('genre', String),
                     Column('rating', Integer),
                     Column('description', String),
                     Column('image_url', String))

metadata.create_all(engine)

def filling_serials_table():
    insert_serials_stmt = serials_table.insert(bind = engine)
    for i in range(1, 72):  # How many pages on site
        link = f'http://baza.animevost.tv/anime-tv/page/{i}/'
        for serial in parse_site_page(link):
            insert_serials_stmt.execute(name = serial['name'],
                                        tag = 's',
                                        link = serial['link'],
                                        genre = serial['genre'],
                                        rating = int(serial['rating']),
                                        description = serial['description'],
                                        image_url = serial['image'])
    for i in range(1, 6):
        link = f'http://baza.animevost.tv/ongoing/page/{i}/'
        for serial in parse_site_page(link):
            insert_serials_stmt.execute(name=serial['name'],
                                        tag='s',
                                        link=serial['link'],
                                        genre=serial['genre'],
                                        rating=int(serial['rating']),
                                        description=serial['description'],
                                        image_url = serial['image'])
    for i in range(1, 109):
        link = f'http://baza.animevost.tv/zavershennye/page/{i}/'
        for serial in parse_site_page(link):
            insert_serials_stmt.execute(name=serial['name'],
                                        tag='s',
                                        link=serial['link'],
                                        genre=serial['genre'],
                                        rating=int(serial['rating']),
                                        description=serial['description'],
                                        image_url=serial['image'])

def filling_films_table():
    insert_films_stmt = films_table.insert(bind = engine)
    for i in range(1, 24):
        link = f'http://baza.animevost.tv/polnometrazhnyj/page/{i}/'
        for film in parse_site_page(link):
            insert_films_stmt.execute(name = film['name'],
                                      tag = 'f',
                                      link = film['link'],
                                      genre = film['genre'],
                                      rating = int(film['rating']),
                                      description = film['description'],
                                      image_url = film['image'])

def filling_anons_table():
    insert_serials_stmt = anons_table.insert(bind = engine)
    for i in range(1, 8):  # How many pages on site
        link = f'http://baza.animevost.tv/anonsy/page/{i}/'
        for serial in parse_site_page(link):
            insert_serials_stmt.execute(name = serial['name'],
                                        tag = 'a',
                                        link = serial['link'],
                                        genre = serial['genre'],
                                        rating = int(serial['rating']),
                                        description = serial['description'],
                                        image_url = serial['image'])


if __name__ == '__main__':
    filling_serials_table()
    filling_films_table()
    filling_anons_table()