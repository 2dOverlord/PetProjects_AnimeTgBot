import logging
from aiogram import Bot, Dispatcher, executor, types
import keyboards
from bot_functions import AnimeBot

TOKEN = '1410462743:AAHmabWssHSalBRNIQhQeGpFRqGX6aw7jWo'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

BOT_FUNCTIONS = AnimeBot()

class IsSerial:
    bol = True


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message, text = 'Привет \nЯ телеграм бот, который поможет тебе с выбором аниме'):
    await bot.send_message(chat_id=message.from_user.id, \
                           text= text, \
                           reply_markup=keyboards.StartKeyboard().keyboard)


@dp.message_handler(lambda message: message.text == f'⬅ Назад')
async def back_to_start(message):
    await send_welcome(message, text='Хорошо')



@dp.message_handler(lambda message: message.text in ['Аниме сериалы', 'Аниме фильмы'])
async def anime_choose(message):
    bot_message = 'Хорошо, но что именно ты хочешь?'
    if message.text == 'Аниме сериалы':
        IsSerial.bol = True
        reply_markup = keyboards.SerialsKeyboard.keyboard
    else:
        IsSerial.bol = False
        reply_markup = keyboards.FilmsKeyboard.keyboard

    await bot.send_message(chat_id=message.from_user.id, text=bot_message, \
                           reply_markup=reply_markup)



@dp.message_handler(lambda message: message.text in ['Случайный фильм', 'Случайный сериал'])
async def random_anime(message):
    if message.text == 'Случайный сериал':
        link = BOT_FUNCTIONS.choose_random('SERIALS')[2]
    else:
        link = BOT_FUNCTIONS.choose_random('FILMS')[2]

    await bot.send_message(chat_id=message.from_user.id, text=link)


@dp.message_handler(lambda message: message.text in ['Сериалы по жанрам', 'Фильмы по жанрам'])
async def serials_genre(message):
    if message.text == 'Сериалы по жанрам':
        reply = keyboards.SerialsGenresKeyboard.keyboard
    else:
        reply = keyboards.FilmsGenresKeyboard.keyboard
    await bot.send_message(chat_id=message.from_user.id,\
                           text='Отлично, какой жанр ты предпочитаешь?', \
                           reply_markup=reply)

@dp.message_handler(lambda message: message.text in ['Назад к аниме сериалам', 'Назад к аниме фильмам'])
async def back_to_serials(message):
    if message.text == 'Назад к аниме сериалам':
        reply_markup = keyboards.SerialsKeyboard.keyboard
    else:
        reply_markup = keyboards.FilmsKeyboard.keyboard
    await bot.send_message(message.from_user.id, text='Ok', reply_markup=reply_markup)


@dp.message_handler(lambda message: message.text in ['Боевые искусства', 'Война', 'Детектив', 'Драма', 'Сёдзё',
                                                     'Сёнен', 'Киберпанк', 'Меха', 'Фантастика', 'История',
                                                     'Мистика', 'Фэнтези', 'Повседневность', 'Музыкальный',
                                                     'Романтика', 'Комедии', 'Спорт', 'Приключения',
                                                     'Триллер', 'Ужасы', 'Школа'])
async def random_genre(message):
    if IsSerial.bol == True:
        link = BOT_FUNCTIONS.choose_random_by_genre(media='SERIALS', genre=message.text)[2]
    else:
        link = BOT_FUNCTIONS.choose_random_by_genre(media='FILMS', genre=message.text)[2]
    await bot.send_message(message.from_user.id, text=link)


@dp.message_handler(lambda message: message.text in ['Топ фильмов', 'Топ сериалов'])
async def top_media(message):
    if message.text == 'Топ фильмов':
        links = BOT_FUNCTIONS.choose_top10('FILMS')
    else:
        links = BOT_FUNCTIONS.choose_top10('SERIALS')
    text = ""
    for anime in links:
        text += f"<a href=\'{anime[2]}\'>{anime[1]}</a>\n"
    await bot.send_message(text=text, chat_id=message.from_user.id, parse_mode="html", disable_web_page_preview=True)

@dp.message_handler(lambda message: message.text == 'Онгоинги')
async def ongoins(message):
    links =BOT_FUNCTIONS.select_ongoins()
    text = ""
    for anime in links:
        text += f"<a href=\'{anime[2]}\'>{anime[1]}</a>\n"
    await bot.send_message(text=text, chat_id=message.from_user.id, parse_mode="html", disable_web_page_preview=True)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)