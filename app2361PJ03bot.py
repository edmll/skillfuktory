import telebot
import requests
import json

from config import TOKEN, API_KEY, keys

bot = telebot.TeleBot(TOKEN)
akey = API_KEY


class APIException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'Ошибка API: {self.message}'


class API:
    @staticmethod
    def get_price(base, quote, amount):
        base = keys.get(base.lower())
        quote = keys.get(quote.lower())
        


        if base is None or quote is None:
            raise APIException('Неподдерживаемая валюта')

        url = f'https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}&api_key={akey}'
        response = requests.get(url)
        data = json.loads(response.content)

        if 'Response' in data and data['Response'] == 'Error':
            raise APIException(f'Ошибка при получении данных: {data["Message"]}')

        if quote not in data:
            raise APIException(f'Неподдерживаемая валюта: {quote}')

        price = round(data[quote] * amount, 2)
        return price







@bot.message_handler(commands=['start', 'help'])
def help(message):
    text = 'Привет! Я бот для получения цены на валюту. ' \
           'Для получения цены, отправь мне сообщение в формате: <валюта1> <валюта2> <количество>. ' \
           'Например: биткоин рубль 0.5 или доллар евро 10'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message):
    available_currencies = list(keys.keys())
    text = 'Доступные валюты:\n\n' + '\n'.join(available_currencies)
    bot.reply_to(message, text)


@bot.message_handler(func=lambda message: True)
def convert(message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неверный формат запроса. Используйте формат: <валюта1> <валюта2> <количество>')
        currency1 = values[0]
        currency2 = values[1]
        amount = float(values[2])

        price = API.get_price(currency1, currency2, amount)

        result = f'Цена {amount} {currency1} в {currency2}: {price}'
        bot.reply_to(message, result)
    except ValueError:
        bot.reply_to(message, 'Неправильно введено число')
    except APIException as e:
        bot.reply_to(message, str(e))


bot.polling()
