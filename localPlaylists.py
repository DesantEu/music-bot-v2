import bot_locale as loc
import dcHandler as dc
import cacheHandler as cahe
import os
import json
import player

async def play_playlist(message, name, inst) -> int:
    # handle empty prompts
    if name == '':
        await message.add_reaction(dc.reactions.fyou)
        return -1

    # check if the user is in a vc
    if not dc.isInVC(message.author):
        await dc.send(loc.no_vc, message.channel)
        return -1


    # check if playlist exists
    if not os.path.exists(f'playlists/{name}.lpl'):
        await dc.send(loc.playlist_not_found, message.channel)
        return -1

    # open the playlist
    with open(f'playlists/{name}.lpl', 'r') as file:
        try:
            playlist:dict = json.loads(file.read())
        except:
            await dc.send(loc.playlist_broken, message.channel)
            return -1
            

        # notify the server
        emb = await dc.send_long(loc.playlist_on, name, [['-', i] for i in playlist], message.channel)
        song_available = False
        tried_connecting = False

        # add songs to queue
        for song in playlist:
            ind = list(playlist).index(song)
            # first try the links
            if await cahe.find_link_play(message, playlist[song], inst, silent=True, skipQueueUpdate=True) == 0:
                await dc.edit_long_status(emb, ind, f'{inst.queue.len()}.  ')
                song_available = True
            # if the link fails try to find by name
            else:
                await dc.edit_long_status(emb, ind, 'V')
                if await cahe.find_prompt_play(message, song, inst, silent=True, skipQueueUpdate=True) == 0:
                    await dc.edit_long_status(emb, ind, f'{inst.queue.len()}.  ')
                    song_available = True
                # if everything fails theres nothing we can do really
                else:
                    await dc.edit_long_status(emb, ind, 'X')

            # if nothing is playing we should start playing i guess
            if song_available and not tried_connecting:
                tried_connecting = True
                # check vc again just to be sure
                if not dc.isInVC(message.author):
                    await dc.send(loc.left_vc, message.channel)
                    return -1
                else:
                    await dc.join(message, inst)
                    if not inst.isPlaying:
                        player.play_from_queue(0, inst) # TODO: remove

        # check vc again just for fun
        if not dc.isInVC(message.author):
            await dc.send(loc.left_vc, message.channel)

        # await dc.add_status(emb, loc.playlist_success, dc.reactions.pls_tears)
        await message.add_reaction(dc.reactions.check)
        await inst.update_queue()

        return 0


async def save_playlist(message, name, inst):
    # handle empty prompts
    if name == '' or inst.queue.len() == 0:
        await message.add_reaction(dc.reactions.fyou)
        return -1


    if os.path.exists(f'playlists/{name}.lpl'):
        emb = await dc.send(loc.playlist_rewrite + name, message.channel)
    else:
        emb = await dc.send(loc.playlist_saving + name, message.channel)

    try:
        with open(f'playlists/{name}.lpl', 'w+') as file:
            file.write(inst.queue.toJsonStr())
        await dc.add_status(emb, dc.reactions.thumbs_up, dc.reactions.cold)
    except:
        await dc.add_status(emb, dc.reactions.cross, dc.reactions.hot)


async def list_playlists(message, name):
    path = 'playlists'
    filepath = f'playlists/{name}.lpl'
    # list all files
    if name == '':
        files = [f[:-4] for f in os.listdir(path) if f.endswith('.lpl')]
        await dc.send_long(loc.playlists, '', [['>', i] for i in files], message.channel)
    # list specific playlist
    else:
        # if doesnt exist
        if not os.path.exists(filepath):
            await message.add_reaction(dc.reactions.cross)
            return -1
        # if does exist
        else:
            with open(filepath, 'r', encoding='utf-8') as file:
                try:
                    playlist:dict = json.loads(file.read())
                except:
                    await dc.send(loc.playlist_broken, message.channel)
                    return -1

            await dc.send_long(loc.playlist_content, name, [['>', i] for i in playlist], message.channel)
                # await dc.send_long(str(songs), message.channel, title=f'Плейлист {name}:')
