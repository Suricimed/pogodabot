# python test.py

import telebot
import os
from flask import Flask, request
import logging
import pyowm

bot = telebot.TeleBot("1273318771:AAHVc_y1C-EvZ33nC6xvcpndWUsZhlBtdjU")
owm = pyowm.OWM('a2796b736dbdd2d94dd087be1702d1da', language = "ru")

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Введите город")

@bot.message_handler(content_types=['text'])
def send_echo(message):
	place = message.text
	if message.text != place:
		bot.send_message(message.chat.id, "ОШИБКА")
	if message.text == place:
		
		observation = owm.weather_at_place(message.text)
		w = observation.get_weather()
		temp = w.get_temperature('celsius')["temp"]

		answer = "В городе " + message.text + " сейчас " + w.get_detailed_status() + '\n'
		answer += "Температура " + str(temp) + "°C" + "\n\n"
		bot.send_message(message.chat.id, answer)

		city = "Введите город" + "\n\n"
		bot.send_message(message.chat.id, city)

# Здесь пишем наши хэндлеры

# Проверим, есть ли переменная окружения Хероку (как ее добавить смотрите ниже)
if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)
    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200
    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://min-gallows.herokuapp.com/bot") # этот url нужно заменить на url вашего Хероку приложения
        return "?", 200
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.  
    # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)