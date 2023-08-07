import dcHandler as dc
import bot_locale as loc
import ytHandler as yt
import player

async def play_bulk(prompts: list[str], inst, message):
    # notify the server
    emb = await dc.send_long(loc.rmlist_title, loc.bulk_smaller_title, [['> ', i] for i in prompts], message.channel)
    song_available = False
    tried_connecting = False

    # add songs to queue
    for pr in prompts:
        ind = prompts.index(pr)
        # indicate works on song
        await dc.edit_long_status(emb, ind, '-')
        # handle words
        if not 'https://' in pr:
            if await yt.play_prompt(message, pr, inst, silent=True) == 0:
                await dc.edit_long_status(emb, ind, f'{inst.queue.len()}.  ')
                await dc.edit_long_text(emb, ind, inst.queue[inst.queue.len()-1].title)
                song_available = True
        # handle links
        else:
            if await yt.play_link(message, pr, inst, silent=True) == 0:
                await dc.edit_long_status(emb, ind, f'{inst.queue.len()}.  ')
                await dc.edit_long_text(emb, ind, inst.queue[inst.queue.len()-1].title)
                song_available = True


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

    await dc.add_status(emb, loc.playlist_success, dc.reactions.pls_tears)


async def play_playlist(message, link, inst, exception=''):
    await dc.send(loc.not_available, message.channel)
