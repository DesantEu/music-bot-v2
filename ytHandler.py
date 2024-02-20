import json
from urllib.parse import parse_qs, urlparse
import yt_dlp as yt
import cacheHandler as cahe

options = {
    'max_downloads' : 1
}
_dl = yt.YoutubeDL(options)


async def get_title(link:str):
    try:
        res = _dl.extract_info(link, download=False)
        with open("test.txt", "w+") as file:
            file.write(json.dumps(res))
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

def get_cache(prompt, is_link=False) -> cahe.CachedSong | None:
    speciman = {}

    # get video data
    if not is_link:
        res = _dl.extract_info(f"ytsearch1:{prompt}", download=False)
        if res:
            speciman = res["entries"][0]
    else:
        res = _dl.extract_info(prompt, download=False)
        if res:
            speciman = res

    # check that we have data
    if speciman == {}:
        return None

    # profit
    return cahe.CachedSong(speciman['id'],
                           speciman['title'],
                           [speciman['title'].lower()] if is_link 
                           else [prompt, speciman['title'].lower()])


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


def get_id_from_link(link: str) -> str:
    parsed = urlparse(link)

    if parsed.hostname == 'youtu.be':
        return parsed.path[1:]
    if parsed.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed.path == '/watch':
            p = parse_qs(parsed.query)
            return p['v'][0]
        if parsed.path[:7] == '/embed/':
            return parsed.path.split('/')[2]
        if parsed.path[:3] == '/v/':
            return parsed.path.split('/')[2]

    return ''


def remove_playlist_from_link(link: str) -> str:
    return link[:link.find('&list=')]
