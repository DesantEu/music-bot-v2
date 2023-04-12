import yt_dlp as yt
import json
import dcHandler as dc
import bot_locale as loc
from datetime import datetime
import re, os
# options = {
#     'format': 'bestaudio/best',
#     'keepvideo': False,
#     'outtmpl': filename,
# }
_dl = yt.YoutubeDL()


async def get_title(link:str):
    res = _dl.extract_info(link, download=False)

    if res:
        return res['title']
    else:
        return -1

async def get_link(title:str):
    res = _dl


async def play_link(bot, message, link, inst, silent=False) -> int:
    emb = ''
    st = -2
    
    # get title
    if not silent: emb = await dc.send(loc.loading_track, message.channel)
    title = await get_title(link)
    if title == -1:
        if not silent: await dc.add_status(emb, loc.search_fail, loc.sorry)
        return -1

    # download if needed
    if not silent: st = await dc.add_status(emb, title, loc.search_local)
    # local search
    filename = 'songs/' + re.sub(r'[\|/,:&$#"]', '', title) + '.mp3'
    if not os.path.exists(filename):
        # start downloading
        if not silent: await dc.edit_status(emb, st, loc.downloading)
        dl = await download(link, filename)
        
        if dl == 0:
            if not silent: await dc.edit_status(emb, st, loc.search_local_success)
            return 0
        else:
            if not silent: await dc.edit_status(emb, st, loc.download_fail)
            return -1

    # local search success
    else:
        if not silent: await dc.edit_status(emb, st, loc.search_local_success)
        return 0




        

async def play_prompt(bot, message, prompt, inst, silent=False):
    pass

async def download(link, filename):
    #TODO: this is probably dumb

    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filename
    }
    
    try:
        with(yt.YoutubeDL(options)) as ydl:
            ydl.download([link])
    except:
        return -1

    return 0

