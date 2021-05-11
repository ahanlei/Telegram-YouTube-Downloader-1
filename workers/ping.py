import os
import telebot
from config import TOKEN, CHAT_ID

bot = telebot.TeleBot(TOKEN)
# tb.send_message(chatid, message)
bot.send_message(CHAT_ID, 'GoGo power ranger')

ip = ["10.5.110.55", "10.5.110.56"]
#ip = ['google.com', 'facebook.com']

for val in ip:
    response = os.system('ping -c 1 ' + val)
    if response == 0:
        print(val + ' is up!')
        bot.send_message(CHAT_ID, val + ' is up')
    else:
        print(val + ' is down!')
        bot.send_message(CHAT_ID, val + ' is down!')
        
bot.sendChatAction(
    chat_id = CHAT_ID,
    action = "typing"
)
