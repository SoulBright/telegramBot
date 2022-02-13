import telebot
from constant import TOKEN, currency
from extension import APIException, CurrConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def greetings(messege: telebot.types.Message):
    text = 'Привет! Просто введи:\nИмя валюты, в какую перевести, и колличество. \
\nЧтобы узнать список доступных к расчёту валют введи: /values'
    bot.reply_to(messege, text)


@bot.message_handler(commands=['values'])
def values(messege: telebot.types.Message):
    text = 'К расчёту доступны следующие валюту: '
    for cur in currency.keys():
        text = '\n'.join((text, cur))
    bot.reply_to(messege, text)


@bot.message_handler(content_types='text')
def exchanger(messege: telebot.types.Message):
    try:
        value = messege.text.split(' ')

        if len(value) != 3:
            raise APIException('Введите название валют и колличиство')

        quote, base, amount = value
        quote, base = str(quote).lower(), str(base).lower()
        cur_total = CurrConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(messege, f'Ошибка ввода!\n{e}')
    except Exception as e:
        bot.reply_to(messege, f'Не удалось обработать команду!\n{e}')
    else:
        text = f'{amount} {currency[quote]} = {cur_total} {currency[base]}'
        bot.send_message(messege.chat.id, text)


bot.polling(none_stop=True)
