import telebot
from cfg import TOKEN, keys
from utils import ConvertionException, Converter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = "Здравствуйте! Моя задача - конвертация валют.\nЧтобы начать работу, отправьте сообщение в следующем формате:\n<имя валюты> \
 <в какую валюту перевести> \
 <количество переводимой валюты>\nПример: доллар рубль 100\nУвидеть список всех доступных валют: /values\nЕсли что-то забыли, то вам поможет команда /help"
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу, отправьте сообщение в следующем формате:\n<имя валюты> \
     <в какую валюту перевести> \
     <количество переводимой валюты>\nПример: доллар рубль 100\nУвидеть список всех доступных валют: /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    if len(values) != 3:
        raise ConvertionException('Слишком много параметров.')

    quote, base, amount = values
    total_base = Converter.convert(quote, base, amount)
    text = f'Цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)

bot.polling()