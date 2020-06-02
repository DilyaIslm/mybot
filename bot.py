from glob import glob
import logging

from random import randint, choice

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME , 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')

def talk_to_me(update, context):
    text = update.message.text 
    print(text)
    update.message.reply_text(text) 

def play_random_number(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f"Ваше число {user_number}, а мое число {bot_number}, Вы выиграли"
    elif user_number == bot_number:
        message = f"Ваше число {user_number}, а мое число {bot_number}, ничья"
    else:
        message = f"Ваше число {user_number}, а мое число {bot_number}, Вы проиграли"
    return message        

def guess_number(update, context): 
    print(context.args)
    if context.args:
       try: 
           user_number = int(context.args[0])
           message = play_random_number(user_number)
       except (TypeError, ValueError):
           message = "Введите целое число" 
    else:
        message = "Введите число"
    update.message.reply_text(message)

def send_cat_picture(update, context):
    cat_photo_list = glob("images/cat*.jp*g")
    cat_photo_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_photo_filename, "rb"))


def main():
    mybot = Updater(settings.API_KEY , use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
 
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()
if __name__ == "__main__":
    main()