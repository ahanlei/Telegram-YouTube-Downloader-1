"""
|---------------------------------------------------_____________$$$
|---------------------------------------------------_____________$$$$
|---------------------------------------------------_____________$$$$
|---------------------------------------------------_____________$$$$$
|---------------------------------------------------_____________$$$$$$
|---------------------------------------------------_____________$$$$$$$
|---------------------------------------------------_____________$$$$$$$$
|---------------------------------------------------_____________$$$$$$$$$
|---------------------------------------------------____________$$$__$$$$$$
|---------------------------------------------------____________$$$___$$$$$$
|---------------------------------------------------____________$$$____$$$$$
|---------------------------------------------------____________$$$_____$$$$$
|---------------------------------------------------____________$$$______$$$$
|---------------------------------------------------____________$$$_______$$$$
|---------------------------------------------------____________$$$_______$$$$
|---------------------------------------------------____________$$$________$$$
|---------------------------------------------------____________$$$________$$$
|---------------------------------------------------____________$$$________$$$
|---------------------------------------------------____________$$$________$$
|---------------------------------------------------____________$$________$$$
|---------------------------------------------------____________$$_______$$$
|---------------------------------------------------____________$$______$$$
|---------------------------------------------------_____$$$$$$$$$_____$$$
|---------------------------------------------------___$$$$$$$$$$$___$$$
|---------------------------------------------------_$$$$$$$$$$$$$__$$$
|---------------------------------------------------$$$$$$$$$$$$$$$$$
|---------------------------------------------------$$$$$$$$$$$$$
|---------------------------------------------------$$$$$$$$$$$$
|---------------------------------------------------_$$$$$$$$$
|---------------------------------------------------___$$$$

ʍǟֆȶɛʀʍɨռɖ-ʋʀȶӼ
"""
from __future__ import unicode_literals
from pyrogram import Client, Filters, StopPropagation, InlineKeyboardButton, InlineKeyboardMarkup
import youtube_dl
from humaner.hooli import humanbytes
import asyncio


def buttonmap(item):
    quality = item['format']
    if "audio" in quality:
        return [InlineKeyboardButton(f"{quality} 🎵 {humanbytes(item['filesize'])}",
                                     callback_data=f"ytdata||audio||{item['format_id']}||{item['yturl']}")]
    else:
        return [InlineKeyboardButton(f"{quality} 📹 {humanbytes(item['filesize'])}",
                                     callback_data=f"ytdata||video||{item['format_id']}||{item['yturl']}")]

# Return a array of Buttons
def create_buttons(quailitylist):
    return map(buttonmap, quailitylist)


# extract Youtube info
def extractYt(yturl):
    ydl = youtube_dl.YoutubeDL()
    with ydl:
        qualityList = []
        r = ydl.extract_info(yturl, download=False)
        for format in r['formats']:
            # Filter dash video(without audio)
            if not "dash" in str(format['format']).lower():
                qualityList.append(
                {"format": format['format'], "filesize": format['filesize'], "format_id": format['format_id'],
                 "yturl": yturl})

        return r['title'], r['thumbnail'], qualityList


#  Need to work 

def downloadyt(url, fmid, custom_progress):
     ydl_opts = {
         'format': f"{fmid}+bestaudio",
         "outtmpl": "test+.%(ext)s",
         'noplaylist': True,
         'progress_hooks': [custom_progress],
     }
     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
         ydl.download([url])


# check https://github.com/SpEcHiDe/AnyDLBot
"""
docvideo is under construction 
"""
async def downloadvideocli(command_to_exec):
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE, )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    print(e_response)
    filename = t_response.split("Merging formats into")[-1].split('"')[1]
    
    return filename


async def downloadaudiocli(command_to_exec):
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE, )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    print("Download error:", e_response)

    return t_response.split("Destination")[-1].split("Deleting")[0].split(":")[-1].strip()
