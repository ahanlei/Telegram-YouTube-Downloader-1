"""
█████████████████████████████████████████████████████████████████████
█░░░░░░██░░░░░░█░░░░░░░░░░░░░░░░███░░░░░░░░░░░░░░█░░░░░░░░██░░░░░░░░█
█░░▄▀░░██░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀▄▀░░███░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀░░██░░▄▀▄▀░░█
█░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░░░▄▀░░███░░░░░░▄▀░░░░░░█░░░░▄▀░░██░░▄▀░░░░█
█░░▄▀░░██░░▄▀░░█░░▄▀░░████░░▄▀░░███████░░▄▀░░███████░░▄▀▄▀░░▄▀▄▀░░███
█░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░░░▄▀░░███████░░▄▀░░███████░░░░▄▀▄▀▄▀░░░░███
█░░▄▀░░██░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀▄▀░░███████░░▄▀░░█████████░░▄▀▄▀▄▀░░█████
█░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░▄▀░░░░███████░░▄▀░░███████░░░░▄▀▄▀▄▀░░░░███
█░░▄▀▄▀░░▄▀▄▀░░█░░▄▀░░██░░▄▀░░█████████░░▄▀░░███████░░▄▀▄▀░░▄▀▄▀░░███
█░░░░▄▀▄▀▄▀░░░░█░░▄▀░░██░░▄▀░░░░░░█████░░▄▀░░█████░░░░▄▀░░██░░▄▀░░░░█
███░░░░▄▀░░░░███░░▄▀░░██░░▄▀▄▀▄▀░░█████░░▄▀░░█████░░▄▀▄▀░░██░░▄▀▄▀░░█
█████░░░░░░█████░░░░░░██░░░░░░░░░░█████░░░░░░█████░░░░░░░░██░░░░░░░░█
█████████████████████████████████████████████████████████████████████
ʍǟֆȶɛʀʍɨռɖ-ʋʀȶӼ
"""

from datetime import datetime, timedelta
# i am  using the CW4RR10R/pyrogram so don't change anything stupidly
from pyrogram import Client, Filters, InlineKeyboardButton, InlineKeyboardMarkup
from Tg_YtDl import user_time
from config import youtube_next_fetch
from func.ytdlfunc import extractYt, create_buttons
# this import is very import
import wget
import os
from PIL import Image

ytregex = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"


@Client.on_message(Filters.regex(ytregex))
async def ytdl(_, message):
    userLastDownloadTime = user_time.get(message.chat.id)
    try:
        if userLastDownloadTime > datetime.now():
            wait_time = round((userLastDownloadTime - datetime.now()).total_seconds() / 60, 2)
            await message.reply_text(f"`Wait {wait_time} Minutes before next Request`")
            return
    except:
        pass

    url = message.text.strip()
    await message.reply_chat_action("upload_video")
    try:
        title, thumbnail_url, formats = extractYt(url)

        now = datetime.now()
        user_time[message.chat.id] = now + \
                                     timedelta(minutes=youtube_next_fetch)

    except Exception:
        await message.reply_text("Failed To Fetch Youtube Data...😔"
                                 "Wait for {wait_time} or try other link"
                                 "[ʍǟֆȶɛʀʍɨռɖ-ʋʀȶӼ](https://telegra.ph/file/3f287a7ff7bd6d63fbd60.jpg)")
        return
    buttons = InlineKeyboardMarkup(list(create_buttons(formats)))
    sentm = await message.reply_text("Select Audio or Video👇🏻")
    try:
        # Todo add webp image support in thumbnail by default not supported by pyrogram
        # https://www.youtube.com/watch?v=lTTajzrSkCw
        img = wget.download(thumbnail_url)
        im = Image.open(img).convert("RGB")
        output_directory = os.path.join(os.getcwd(), "downloads", str(message.chat.id))
        if not os.path.isdir(output_directory):
            os.makedirs(output_directory)
        thumb_image_path = f"{output_directory}.jpg"
        im.save(thumb_image_path,"jpeg")
        await message.reply_photo(thumb_image_path, caption=title, reply_markup=buttons)
        await sentm.delete()
    except Exception as e:
        print(e)
        try:
            thumbnail_url = "https://telegra.ph/file/3f287a7ff7bd6d63fbd60.jpg"
            await message.reply_photo(thumbnail_url, caption=title, reply_markup=buttons)
        except Exception as e:
            await sentm.edit(
            f"<code>{e}</code> #Error")
