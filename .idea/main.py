import os
import telegram
import requests

# установка API токена бота
bot = telegram.Bot(token='6007038799:AAF5IVC5U37orf59p4roySyv7aPgARHTLyE')

# определение функции для загрузки видео
def download_video(url):
    r = requests.get(url, stream=True)
    with open('video.mp4', 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

# определение функции для обработки сообщений
def handle_message(update, context):
    message = update.message
    # проверка, что сообщение содержит ссылку на видео
    if message.entities and message.entities[0].type == 'url':
        url = message.text[message.entities[0].offset:message.entities[0].offset+message.entities[0].length]
        download_video(url)
        # отправка видео в ответ на сообщение
        context.bot.send_video(chat_id=message.chat_id, video=open('video.mp4', 'rb'))

# установка обработчика сообщений
updater = telegram.ext.Updater(token='YOUR_TOKEN', use_context=True)
updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))

# запуск бота
updater.start_polling()