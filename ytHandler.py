import yt_dlp as yt
# import json
import dcHandler as dc
import bot_locale as loc
# from datetime import datetime
import re, os

options = {
    'max_downloads' : 1
}
_dl = yt.YoutubeDL(options)


async def get_title(link:str):
    try:
        res = _dl.extract_info(link, download=False)
    except:
        return -1

    if res:
        if 'ytsearch' in link:
            try:
                return res['entries'][0]['title']
            except:
                return -1
        try:
            return res['title']
        except:
            return -1
    else:
        return -1


async def play_link(message, link, inst, silent=False) -> int:
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
            inst.queue.append(link, title)
            await inst.update_queue()
            return 0
        else:
            if not silent: await dc.edit_status(emb, st, loc.download_fail)
            return -1

    # local search success
    else:
        if not silent: await dc.edit_status(emb, st, loc.search_local_success)
        inst.queue.append(link, title)
        await inst.update_queue()
        return 0

async def play_prompt(message, prompt, inst, silent=False):
    return await play_link(message, f'ytsearch1:{prompt}', inst, silent)


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

