import telebot
import random
import requests
from telebot import types
from deep_translator import GoogleTranslator

bot = telebot.TeleBot('1748917306:AAEuzWjBJth-MifLGWvizYY_ubGNpNm4PqI')
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('/start', '/bb', 'weatherInOmsk', '/help')

# 14a869c8e7760d2a4cad67727db6d408 open weather key

@bot.message_handler(commands=['start'])
def start_message(msg):
    bot.send_message(msg.chat.id, 'Здарова, ' + str(msg.from_user.first_name), reply_markup=keyboard1)

@bot.message_handler(commands=['bb'])
def bb_message(msg):
    bot.send_sticker(msg.chat.id, 'CAACAgIAAxkBAAMHYFjJCn-iq2UYNs8vXo9zRXJNwLkAAgMAAzujAhrcYj716LqGIB4E')

@bot.message_handler(commands=['help'])
def help_message(msg):
    bot.send_message(msg.chat.id, 'Ты можешь написать: "скинь настю", "weatherInOmsk", "даня лох" \n "переведи" - для перевода текста')

@bot.message_handler(commands=['translate'])
def translator(msg):
    bot.send_message(msg.chat.id, 'Введи текст')

@bot.message_handler(content_types=['text'])
def nastyaSticker(msg):
    if msg.text.lower() == 'скинь настю':
        if random.randint(1, 2) == 1:
            bot.send_sticker(msg.chat.id, 'CAACAgIAAxkBAAMFYFjIr0Gdf5LLcNteghBLS4BLYdUAAiIMAAIsnCBKT2NOZP27k-AeBA')
        else:
            bot.send_photo(msg.chat.id,
                           'https://sun9-59.userapi.com/impg/i-jDwNz1EkKYXhdDJGaXLMfCzhKkJ4HSMuB6qw/jKaxiOmprAY.jpg?size=2560x1707&quality=96&sign=58516fc8c2e696de3db89c9d58062939&type=album')
    if msg.text.lower() == 'weatherInOmsk':
        weather = requests.get("http://api.openweathermap.org/data/2.5/find",
                               params={'q': "Omsk", 'units': 'metric', 'APPID': '14a869c8e7760d2a4cad67727db6d408'})
        data = weather.json()
        if data['list'][0]['main']['temp'] > 0:
            bot.send_message(msg.chat.id, 'Погода в омске сейчас такая: ' + str(data['list'][0]['main']['temp']) + ' жарко емае')
        else : bot.send_message(msg.chat.id, 'Погода в омске сейчас такая: ' + str(data['list'][0]['main']['temp']) + ' ппц дубачелло')

    if msg.text.lower() == 'даня лох':
        bot.send_photo(msg.chat.id,
                       'https://lh3.googleusercontent.com/Rx-g7XgK5AmTXavIbFsB3kIxuMpW-xxuQH23OIRmXVuaQqrnxrIteHzI5A6L-vFAyIpHaY1cPbYIndOCXK62ahiPIHsyLvnxrmFIPHKzpd27F5Ecdw0ka6ec0ITxcpVQEkCRbW0FgCM31UqSnKg-WA8BU1aiaQe5KyIQH3OI23qV44F0_4rsmxEj1NTlscN5GN4kcfz-lryXyvdb2OUg_1pB3szFnstBZFNr_kLqYTZlcCrHxoVLzds-K8r4-2bGlwBkwUSN0pkBAoza47LFUC56KPHPwSBFHwigbjyzDeW2_3XLBiXdMg_rMAmQB1Nc666Ax9LsDFiI4PNzxJntpHHhpiSlOYOpWoPGngVsxh4F7zpGwyYhRloqnrKGefkE5Us7VTuo4iFqDu7kjpMZi6fsOnCNobpBXgwse5XW1pOucG5Txmv_0q6NlpXIWY2AYa-GuPewdxtQzegzo-bbEY1iXg-qZnPkbuDCxRClUyzmhPMV4x1PdXUnHGUpo_-D7lYHWgCiuAHMSle-fpddUSqG5bMhubJvw_8ERnYpbNmG2CA0HGhvZCqpP6QYLM_cKa050cyJDJgMPjG5GBKzpAWtgti8CZoIs1oWEYnX9MT-pEJrKaJ2fRYSlBiYDFluwky183f3TLUJgn0M5BodszwqQWX_a5kXn3e_CtCoOIOljmNTk9uzGPNo4cDEtAEUmmxISXdXTNNfdS4tFWhYFUQuWw=w714-h951-no?authuser=0')

    if msg.text.lower() == 'переведи':
        keyboard = types.InlineKeyboardMarkup()
        key_trans = types.InlineKeyboardButton(text = 'Translate', callback_data = 'translateIt')
        keyboard.add(key_trans)
        bot.send_message(msg.chat.id, 'Нажми', reply_markup= keyboard)

@bot.callback_query_handler(func = lambda call: True)
def translate(call):
        if call.data == 'translateIt':
            kek = bot.send_message(call.message.chat.id, 'введите текст')
            bot.register_next_step_handler(kek, handle_text1)
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text1(msg):
    translated = GoogleTranslator(source='auto', target='en').translate(msg.text)
    bot.send_message(msg.chat.id, translated)


@bot.message_handler(content_types=['sticker'])
def whatSticker(msg):
    print(msg)

bot.polling()