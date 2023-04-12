import yt_dlp as yt
import json
from datetime import datetime

_dl = yt.YoutubeDL()


async def get_title(link:str):
    res = _dl.extract_info(link, download=False)

    if res:
        return res['title']
    else:
        return 1

async def get_link(title:str):
    res = _dl



