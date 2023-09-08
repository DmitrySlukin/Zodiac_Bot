"""Телеграмм бот для получения астрологического прогноза на день.
    В качестве датасета используется датасет гороскопов с сайта https://horoscopes.rambler.ru """

from datetime import date
import pandas as pd
import telebot
from telebot import types

# В переменную zodiac_bot передаем токен нашего бота из botFather
#                             \/\/
zodiac_bot = telebot.TeleBot('****')


# Создаем кнопки для ввода знаков зодиака

@zodiac_bot.message_handler(commands=['start'])  # декоратор в который передаем отслеживаемые команды
def start(message):  # Декорируемая функция, принимает сообщение от пользователя
    mess = f'Привет, {message.from_user.first_name}!'
    zodiac_bot.send_message(message.chat.id, mess, parse_mode='html')  # Отправляем сообщение в чат по id чата.
    #                              ^^^^^^^   ^^^^^^      ^^^^^
    #                          Обязательные параметры  Необязательный (Без него будет просто текст без html-тегов)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    aries = types.KeyboardButton("Овен")
    taurus = types.KeyboardButton("Телец")
    gemini = types.KeyboardButton("Близнецы")
    cancer = types.KeyboardButton("Рак")
    leo = types.KeyboardButton("Лев")
    virgo = types.KeyboardButton("Дева")
    libra = types.KeyboardButton("Весы")
    scorpio = types.KeyboardButton("Скорпион")
    sagittarius = types.KeyboardButton("Стрелец")
    capricorn = types.KeyboardButton("Козерог")
    aquarius = types.KeyboardButton("Водолей")
    pisces = types.KeyboardButton("Рыбы")
    markup.add(aries, taurus, gemini, cancer, leo, virgo, libra, scorpio, sagittarius, capricorn, aquarius, pisces)
    zodiac_bot.send_message(message.chat.id, 'Выбери свой знак зодиака!', reply_markup=markup)


# Выводим фразу из файла в качестве ответного сообщения

@zodiac_bot.message_handler(content_types=['text'])
def get_user_text(message):
    zodiac_list = ["овен", "телец", "близнецы",
                   "рак", "лев", "дева",
                   "весы", "скорпион", "стрелец",
                   "козерог", "водолей", "рыбы"]
    if message.text.lower() in zodiac_list:
        current_date = str(date.today())
        pd_df = pd.read_csv(f'{message.text}.csv', encoding='utf-8', sep='^', dtype=str, usecols=['date', 'text'])
        pd_df = pd_df[pd_df['date'].str.contains(current_date[5::])].sample(n=1)
        response = pd_df['text'].tolist()
        response = ''.join(response)
        current_date = date.today().strftime("%d.%m.%Y")
        zodiac_bot.send_message(message.chat.id, f"Астрологический прогноз на сегодня <b><u>{current_date}</u></b>, \n"
                                                  f"для знака зодиака <b><u>{message.text}</u></b>: \n"
                                                  f"{response}", parse_mode='html')

    else:
        zodiac_bot.send_message(message.chat.id, f"Прости, но я не знаю такого знака зодиака.")


if __name__ == '__main__':
    zodiac_bot.polling(none_stop=True)  # Запускает постоянное выполнение бота
