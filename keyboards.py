from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class StartKeyboard:
    serials_btn = KeyboardButton('Аниме сериалы')
    films_btn = KeyboardButton('Аниме фильмы')
    anons_btn = KeyboardButton('Анонсы')

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(anons_btn, serials_btn, films_btn)


class FilmsKeyboard:
    random_btn = KeyboardButton('Случайный фильм')
    back = KeyboardButton('⬅ Назад')

    genre_button = KeyboardButton('Фильмы по жанрам')
    top_btn = KeyboardButton('Топ фильмов')

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(back, random_btn).row(top_btn, genre_button)


class FilmsGenresKeyboard:
    back_to_serials = KeyboardButton('Назад к аниме фильмам')

    arts = KeyboardButton('Боевые искусства')
    war = KeyboardButton('Война')

    detectiv = KeyboardButton('Детектив')
    drama = KeyboardButton('Драма')

    cyber_punk = KeyboardButton('Киберпанк')
    meha = KeyboardButton('Меха')

    fantastic = KeyboardButton('Фантастика')
    fantasy = KeyboardButton('Фэнтези')

    everydaying = KeyboardButton('Повседневность')
    musicial = KeyboardButton('Музыкальный')

    romantic = KeyboardButton('Романтика')
    comedy = KeyboardButton('Комедии')

    sport = KeyboardButton('Спорт')
    advanture = KeyboardButton('Приключения')

    triller = KeyboardButton('Триллер')
    hrrbls = KeyboardButton('Ужасы')

    history = KeyboardButton('История')

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(back_to_serials) \
        .row(arts, war).row(detectiv, drama) \
        .row(cyber_punk, meha).row(fantastic, fantasy) \
        .row(everydaying, musicial) \
        .row(romantic, comedy).row(sport, advanture) \
        .row(triller, hrrbls).row(history)

class SerialsKeyboard:
    random_btn = KeyboardButton('Случайный сериал')
    back = KeyboardButton('⬅ Назад')

    genre_button = KeyboardButton('Сериалы по жанрам')
    ongoings = KeyboardButton('Онгоинги')

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(back, random_btn).row(ongoings, genre_button)

class SerialsGenresKeyboard:
    back_to_serials = KeyboardButton('Назад к аниме сериалам')

    seinen = KeyboardButton('Сёнен') # no in films
    school = KeyboardButton('Школа')  # no in films

    arts = KeyboardButton('Боевые искусства')
    war = KeyboardButton('Война')

    detectiv = KeyboardButton('Детектив')
    drama = KeyboardButton('Драма')

    cyber_punk = KeyboardButton('Киберпанк')
    meha = KeyboardButton('Меха')

    fantastic = KeyboardButton('Фантастика')
    history = KeyboardButton('История')

    mystic = KeyboardButton('Мистика') # no in films
    fantasy = KeyboardButton('Фэнтези')

    everydaying = KeyboardButton('Повседневность')
    musicial = KeyboardButton('Музыкальный')

    romantic = KeyboardButton('Романтика')
    comedy = KeyboardButton('Комедии')

    sport = KeyboardButton('Спорт')
    advanture = KeyboardButton('Приключения')

    triller = KeyboardButton('Триллер')
    hrrbls = KeyboardButton('Ужасы')


    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(back_to_serials).row(school, seinen) \
                                                        .row(arts, war).row(detectiv, drama)\
                                                        .row(cyber_punk, meha).row(fantastic, history)\
                                                        .row(mystic, fantasy).row(everydaying, musicial)\
                                                        .row(romantic, comedy).row(sport, advanture)\
                                                        .row(triller, hrrbls)

