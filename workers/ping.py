import os
import telebot
import config

bot = telebot.TeleBot(TOKEN)
# tb.send_message(chatid, message)
bot.send_message(chat.id, 'GoGo power ranger')

ip = ["10.5.110.55", "10.5.110.56"]
#ip = ['google.com', 'facebook.com']

for val in ip:
    response = os.system('ping -c 1 ' + val)
    if response == 0:
        print(val + ' is up!')
        bot.send_message(chat.id, val + ' is up')
    else:
        print(val + ' is down!')
        bot.send_message(chat.id, val + ' is down!')
        
bot.sendChatAction(
    chat_id = chat.id,
    action = "typing"
)
