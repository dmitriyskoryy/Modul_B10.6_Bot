import telebot


from config import TOKEN, keys
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start', 'help'])
def send_start_help(message):
    bot.send_message(message.chat.id, f"Введите через пробел валюту цену которой хотите узнать,\n"
                                      f"валюту в которой надо узнать цену первой валюты,\n"
                                      f"и колличество первой валюты. Например: рубль доллар 12\n"
                                      f"Доступные виды валют, введите команду: /values")


@bot.message_handler(commands=['values', ])
def send_values(message):
    s = ', '.join([s for s in keys])
    bot.send_message(message.chat.id, f"Доступные валюты: {s}")



@bot.message_handler(content_types=['text', ])
def repeat(message: telebot.types.Message):

    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise APIException('Много введено параметров.')

        base, quote, amount = value

        total = CryptoConverter.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду:\n{e}")
    else:
        bot.send_message(message.chat.id, total)

bot.polling(none_stop=True)




