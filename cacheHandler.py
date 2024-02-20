import json
import os, re
from typing import Any
import ytHandler as yt
import dcHandler as dc
import bot_locale as loc

class CachedSong:
    def __init__(self, link: str='', title: str='', searches: list[str]=[]):
        self.link = link
        self.title = title
        self.searches = searches

    def toJson(self):
        rJson = {}
        rJson['link'] = self.link
        rJson['title'] = self.title
        rJson['searches'] = self.searches

        return rJson

    def fromJson(self, o: dict[str, Any]):
        self.link = o['link']
        self.title = o['title']
        self.searches = o['searches']

    def __str__(self) -> str:
        return json.dumps(self.toJson())


# short link - song
cache: dict[str, CachedSong]

# search - song
search_cache: dict[str, CachedSong]

async def find_link_play(message, link, inst, silent=False) -> int:
    global cache
    emb = ''
    st = -2

    # extract id from link
    prompt = yt.get_id_from_link(link)

    if prompt == '':
        await dc.send(loc.search_fail, loc.sorry)

    # notify that we are working
    if not silent: emb = await dc.send(loc.loading_track, message.channel)

    if prompt in cache:
        # add song name
        if not silent: st = await dc.add_status(emb, cache[prompt].title, loc.search_local)
        return await play_cached(message, cache[prompt], inst, silent, emb, st)

    else:
        # notify that we are searching
        if not silent: st = await dc.add_status(emb, link, loc.search_yt)

        # get infor from yt
        info = yt.get_cache(prompt, is_link=True)

        if not info == None:
            cache[info.link] = info

            # notify that we have info
            await dc.edit_status_title(emb, st, info.title)
            await dc.edit_status(emb, st, loc.search_local)
            return await play_cached(message, info, inst, silent, emb, st)

        else:
            if not silent: await dc.edit_status(emb, st, loc.search_fail)
            return -1


async def find_prompt_play(message, prompt: str, inst, silent=False) -> int:
    global search_cache, cache
    emb = ''
    st = -2

    prompt = prompt.lower()

    # notify that we are working
    if not silent: emb = await dc.send(loc.loading_track, message.channel)

    if prompt in search_cache:
        # add song name
        if not silent: st = await dc.add_status(emb, search_cache[prompt].title, loc.search_local)
        return await play_cached(message, search_cache[prompt], inst, silent, emb, st)

    else:
        # notify that we are searching
        if not silent: st = await dc.add_status(emb, prompt, loc.search_yt)

        # get infor from yt
        info = yt.get_cache(prompt)

        if not info == None:
            # check if known link
            if info.link in cache:
                cache[info.link].searches.append(prompt)
                search_cache[prompt] = cache[info.link]
            else:
                cache[info.link] = info
                search_cache[prompt] = info

            # notify that we have info
            await dc.edit_status_title(emb, st, info.title)
            await dc.edit_status(emb, st, loc.search_local)
            return await play_cached(message, info, inst, silent, emb, st)

        else:
            if not silent: await dc.edit_status(emb, st, loc.search_fail)
            return -1



async def play_cached(message, song: CachedSong, inst, silent, emb, st) -> int:
    # search for song on disk
    filename = 'songs/' + re.sub(r'[\|/,:&$#"]', '', song.link) + '.mp3'
    full_link = 'https://www.youtube.com/watch?v=' + song.link
    
    if not os.path.exists(filename):
        # notify that we are downloading
        if not silent: await dc.edit_status(emb, st, loc.downloading)
        # download
        dl = await yt.download(full_link, filename)
        # check how that went
        if dl == 0:
            return await on_search_success(message, inst, emb, song.title, full_link, st, silent)
        else:
            if not silent: await dc.edit_status(emb, st, loc.download_fail)
            return -1
    else:

        return await on_search_success(message, inst, emb, song.title, full_link, st, silent)


async def on_search_success(message, inst, emb, title, link, st, silent) -> int:
    if not silent:
        await dc.edit_status(emb, st, loc.search_local_success)
        # add instaplay reaction
        if inst.queue.len() > 0:
            msg = await message.channel.fetch_message(emb)
            await msg.add_reaction(dc.reactions.play)

    inst.queue.append(link, title, emb)
    if not silent: 
        await dc.edit_status_title(emb, st, f"{inst.queue.index_title(title) + 1}. {title}")
    await inst.update_queue()
    return 0



def add_to_cache(song: CachedSong):
    global cache, search_cache
    # add to link cache
    cache[song.link] = song

    # add to search cache
    for s in song.searches:
        search_cache[s] = song

def load_cache():
    global cache, search_cache

    print("loading cache...")
    cache = {}
    search_cache = {}
    
    try:
        with open("saves/cache.json", "r") as file:
            for i in json.loads(file.read()):
                song = CachedSong()
                song.fromJson(i)
                print(song)

                add_to_cache(song)                

    except Exception as e:
        print(f"got exception loading cache:")
        print(e)

    print("loading cache... done")


def save_cache():
    print("saving cache...")

    l = []
    for k in cache.keys():
        l.append(cache[k].toJson())

    with open(f"saves/cache.json", "w+") as file:
        file.write(json.dumps(l))

    print("saving cache... done")

if not os.path.exists("saves/cache.json"):
    cache = {}
    search_cache = {}
else:
    load_cache()
