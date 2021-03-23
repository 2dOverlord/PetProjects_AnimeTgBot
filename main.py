from aiogram import Bot, Dispatcher, executor

import keyboards
from bot_functions import AnimeBot, content_to_html, content_to_html_short
from anime_parser import GENRES

TOKEN = '1410462743:AAHmabWssHSalBRNIQhQeGpFRqGX6aw7jWo'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

BOT_FUNCTIONS = AnimeBot()


class IsSerial:
    # Check user choice - Serials or Films
    bol = True


@dp.message_handler(commands=['start'])
async def send_welcome(message,
                       message_text='Ohayo ✌\n'
                                    'Я помогу тебе выборать аниме ✨\n\n' 
                                    'Если хочешь найти его по названию, просто вбей его в чат ✎\n'
                                    'Для вызова команд используй клавиатуру ниже ↡\n'
                                    'Удачки)'):

    chat_id = message.from_user.id

    await bot.send_message(chat_id=chat_id, text=message_text, reply_markup=keyboards.StartKeyboard.keyboard)

@dp.message_handler(lambda message: message.text[0:4] in ['/sid', '/fid', '/aid'])
async def send_anime_by_id(message):
    """
    This function find anime by its id in database
    Id looks like /sid21
    /sid is for serials, /fid is for films
    """
    chat_id = message.from_user.id

    if message.text[0:4] == '/sid':
        content = BOT_FUNCTIONS.select_by_id('SERIALS', message.text)
    elif message.text[0:4] == '/fid':
        content = BOT_FUNCTIONS.select_by_id('FILMS', message.text)
    else:
        content = BOT_FUNCTIONS.select_by_id('ANONS', message.text)

    message_text = content_to_html(content)

    await bot.send_message(chat_id=chat_id, text=message_text, parse_mode='markdown')

@dp.message_handler(lambda message: message.text == f'⬅ Назад')
async def back_to_start_keyboard(message):
    message_text = '🦄 Временно отступаем, senpai'

    await send_welcome(message, message_text)

@dp.message_handler(lambda message: message.text == 'Анонсы')
async def send_anons(message):

    chat_id = message.from_user.id

    content = BOT_FUNCTIONS.select_anons()
    message_text = ''.join(content_to_html_short(anime) for anime in content[:10])

    await bot.send_message(chat_id=chat_id, text=message_text, parse_mode='markdown')

@dp.message_handler(lambda message: message.text in ['Аниме сериалы', 'Аниме фильмы'])
async def choose_media(message):
    """
    This function call when user choose between Serials or Films
    """

    chat_id = message.from_user.id
    message_text = 'Хорошо, давай выбирать дальше🤔'

    if message.text == 'Аниме сериалы':
        IsSerial.bol = True
        reply_markup = keyboards.SerialsKeyboard.keyboard
    else:
        IsSerial.bol = False
        reply_markup = keyboards.FilmsKeyboard.keyboard

    await bot.send_message(chat_id=chat_id, text=message_text, reply_markup=reply_markup)


@dp.message_handler(lambda message: message.text in ['Случайный фильм', 'Случайный сериал'])
async def send_random_anime(message):
    """
    This function sends random anime to user
    """
    chat_id = message.from_user.id

    if message.text == 'Случайный сериал':
        message_text = content_to_html(BOT_FUNCTIONS.select_random_anime('SERIALS'))
    else:
        message_text = content_to_html(BOT_FUNCTIONS.select_random_anime('FILMS'))

    await bot.send_message(chat_id=chat_id, text=message_text, parse_mode='markdown', disable_web_page_preview=False)


@dp.message_handler(lambda message: message.text in ['Сериалы по жанрам', 'Фильмы по жанрам'])
async def media_genres_keyboard(message):
    """
    This function send user keyboard to choose genres
    """

    chat_id = message.from_user.id
    message_text = 'Какой жанр предпочитаешь?'

    if message.text == 'Сериалы по жанрам':
        reply_keyboard = keyboards.SerialsGenresKeyboard.keyboard
    else:
        reply_keyboard = keyboards.FilmsGenresKeyboard.keyboard

    await bot.send_message(chat_id=chat_id, text=message_text, reply_markup=reply_keyboard)


@dp.message_handler(lambda message: message.text in ['Назад к аниме сериалам', 'Назад к аниме фильмам'])
async def back_to_media_keyboard(message):

    chat_id = message.from_user.id
    message_text = '👇Вернулись, что дальше?👇'

    if message.text == 'Назад к аниме сериалам':
        reply_markup = keyboards.SerialsKeyboard.keyboard
    else:
        reply_markup = keyboards.FilmsKeyboard.keyboard

    await bot.send_message(chat_id=chat_id, text=message_text, reply_markup=reply_markup)


@dp.message_handler(lambda message: message.text in GENRES)
async def send_random_by_genre(message):
    """
    Send user media which genre is same as user selected
    """
    chat_id = message.from_user.id

    if IsSerial.bol:
        content = BOT_FUNCTIONS.select_random_by_genre(media='SERIALS', genre=message.text)
    else:
        content = BOT_FUNCTIONS.select_random_by_genre(media='FILMS', genre=message.text)

    message_text = f'👇Вот случайный тайтл этого жанра👇\n{content_to_html(content)}'

    await bot.send_message(chat_id=chat_id, text=message_text, parse_mode='markdown', disable_web_page_preview=False)


@dp.message_handler(lambda message: message.text in ['Топ фильмов', 'Топ сериалов'])
async def send_top10_anime(message):
    """
    Send user top 10 films or serials
    """
    chat_id = message.from_user.id

    if message.text == 'Топ фильмов':
        content = BOT_FUNCTIONS.select_top10_anime('FILMS')
    else:
        content = BOT_FUNCTIONS.select_top10_anime('SERIALS')

    message_text = ''.join(content_to_html_short(anime) for anime in content)

    await bot.send_message(chat_id=chat_id, text=message_text, parse_mode='markdown', disable_web_page_preview=True)


@dp.message_handler(lambda message: message.text == 'Онгоинги')
async def send_ongoings(message):
    chat_id = message.from_user.id

    content = BOT_FUNCTIONS.select_ongoings()
    message_text = ''.join(content_to_html_short(anime) for anime in content)

    await bot.send_message(chat_id=chat_id ,text=message_text, parse_mode='html', disable_web_page_preview=True)

@dp.message_handler()
async def send_anime_by_search(message):
    chat_id = message.from_user.id

    content = BOT_FUNCTIONS.select_by_name(message.text)

    if content:
        message_text = ''.join(content_to_html_short(anime) for anime in content)
    else:
        message_text = 'Извини, не смог найти ничего похожего(('

    await bot.send_message(chat_id=chat_id, text=message_text, parse_mode='markdown', disable_web_page_preview=False)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
