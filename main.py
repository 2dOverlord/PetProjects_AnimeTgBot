from aiogram import Bot, Dispatcher, executor
import keyboards
from bot_functions import AnimeBot, content_to_html

TOKEN = '1410462743:AAHmabWssHSalBRNIQhQeGpFRqGX6aw7jWo'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

BOT_FUNCTIONS = AnimeBot()


class IsSerial:
    # Check user choice - Serials or Films
    bol = True


@dp.message_handler(commands=['start'])
async def send_welcome(message,
                       message_text='Привет \n' \
                                    'Я телеграм бот, который поможет тебе с выбором аниме))\n\n' \
                                    'Если нужна будет помощь, напиши /help'):
    """
    Welcome function
    :param message_text: This text will be in bot`s message
    :param message: message like in commands
    """
    chat_id = message.from_user.id
    await bot.send_message(chat_id=chat_id, text=message_text, reply_markup=keyboards.StartKeyboard.keyboard)


@dp.message_handler(lambda message: message.text == f'⬅ Назад')
async def back_to_start(message):
    """
    Returns user to the start keyboard
    """
    message_text = 'Хорошо'
    await send_welcome(message, message_text)


@dp.message_handler(lambda message: message.text in ['Аниме сериалы', 'Аниме фильмы'])
async def choose_media(message):
    """
    Choosing media function
    :param message:
    :return:
    """
    message_text = 'Хорошо, но что именно ты хочешь?'
    chat_id = message.from_user.id

    if message.text == 'Аниме сериалы':
        IsSerial.bol = True
        reply_markup = keyboards.SerialsKeyboard.keyboard
    else:
        IsSerial.bol = False
        reply_markup = keyboards.FilmsKeyboard.keyboard

    await bot.send_message(chat_id=chat_id, text=message_text, reply_markup=reply_markup)


@dp.message_handler(lambda message: message.text in ['Случайный фильм', 'Случайный сериал'])
async def random_anime(message):
    # Send random anime to user
    chat_id = message.from_user.id

    if message.text == 'Случайный сериал':
        content = BOT_FUNCTIONS.choose_random('SERIALS')
    else:
        content = BOT_FUNCTIONS.choose_random('FILMS')

    message_text = content_to_html(content)

    await bot.send_message(chat_id=chat_id, text=message_text, parse_mode='html', disable_web_page_preview=False)


@dp.message_handler(lambda message: message.text in ['Сериалы по жанрам', 'Фильмы по жанрам'])
async def media_genres_keyboard(message):
    # Reply genre keyboard

    message_text = 'Отлично, какой жанр ты предпочитаешь?'
    chat_id = message.from_user.id

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


@dp.message_handler(lambda message: message.text in ['Боевые искусства', 'Война', 'Детектив', 'Драма', 'Сёдзё',
                                                     'Сёнен', 'Киберпанк', 'Меха', 'Фантастика', 'История',
                                                     'Мистика', 'Фэнтези', 'Повседневность', 'Музыкальный',
                                                     'Романтика', 'Комедии', 'Спорт', 'Приключения',
                                                     'Триллер', 'Ужасы', 'Школа'])
async def random_genre(message):
    # Reply random serial, but user choose genre
    chat_id = message.from_user.id
    if IsSerial.bol:
        content = BOT_FUNCTIONS.choose_random_by_genre(media='SERIALS', genre=message.text)
    else:
        content = BOT_FUNCTIONS.choose_random_by_genre(media='FILMS', genre=message.text)

    message_text = '👇Вот случайный тайтл этого жанра👇\n'
    message_text += content_to_html(content)

    await bot.send_message(chat_id=chat_id, text=message_text, parse_mode='markdown', disable_web_page_preview=False)


@dp.message_handler(lambda message: message.text in ['Топ фильмов', 'Топ сериалов'])
async def top_media(message):
    # Need refactoring
    chat_id = message.from_user.id

    if message.text == 'Топ фильмов':
        content = BOT_FUNCTIONS.choose_top10('FILMS')
    else:
        content = BOT_FUNCTIONS.choose_top10('SERIALS')

    message_text = ''
    for anime in content:
        message_text += f'<a href=\'{anime["link"]}\'>{anime["name"]}</a>\n'

    await bot.send_message(chat_id=chat_id, text=message_text, parse_mode='html', disable_web_page_preview=True)


@dp.message_handler(lambda message: message.text == 'Онгоинги')
async def ongoins(message):
    # Need refactoring
    chat_id = message.from_user.id
    content = BOT_FUNCTIONS.select_ongoins()
    message_text = ''
    for anime in content:
        message_text += f'<a href=\'{anime["link"]}\'>{anime["name"]}</a>\n'
    await bot.send_message(chat_id=chat_id ,text=message_text, parse_mode='html', disable_web_page_preview=True)

@dp.message_handler()
async def other_text_to_search(message):
    #Need refactoring

    chat_id = message.from_user.id
    content = BOT_FUNCTIONS.find_by_name(message.text)

    if isinstance(content, list):
        message_text = ''
        for anime in content:
            message_text += f'<a href=\'{anime["link"]}\'>{anime["name"]}</a>\n'
    else:
        message_text = content

    await bot.send_message(chat_id=chat_id, text=message_text, parse_mode='html', disable_web_page_preview=True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
