import discord
import ytHandler as yt
import dcHandler as dc
import bot_locale as loc
import playlists
import re

async def play(message:discord.Message, prompt:str, inst):
    # handle empty prompts
    if prompt == '' and not inst.isPaused:
        """ await dc.send(loc.no_prompt, message.channel) """
        await message.add_reaction(dc.reactions.fyou)
        return

    # check if the user is in a vc
    if not dc.isInVC(message.author):
        await dc.send(loc.no_vc, message.channel)
        return -1


    isSuccessful = -1

    # handle links
    if prompt.startswith('https://'):
        # handle playlists
        if 'list=' in prompt:
             isSuccessful = await playlists.play_playlist(message, prompt, inst)
        # handle a single song
        else:
            isSuccessful = await yt.play_link(message, prompt, inst)
    # handle text search
    else:
        isSuccessful = await yt.play_prompt(message, prompt, inst)

    if not isSuccessful == 0:
        return -1

    # check vc again just to be sure
    if not dc.isInVC(message.author):
        await dc.send(loc.left_vc, message.channel)
        return -1
    else:
        await dc.join(message, inst)
        if not inst.isPlaying:
            play_from_queue(0, inst) # TODO: remove
    
            
def stop(inst) -> bool:

    # stop and leave vc
    if inst.hasVC():
    # drop play.after
        inst.skipSkip = True
        inst.vc.stop()
    # else:
    #     return False

    inst.isPaused = False
    inst.isPlaying = False
    inst.isStopped = True
    inst.queue.clear()
    return True


def resume(inst) -> bool:
    inst.isPlaying = True
    inst.isStopped = False
    inst.isPaused = False
    return True

def pause(inst) -> bool:
    inst.isPlaying = False
    inst.isStopped = False
    inst.isPaused = True
    return True

def skip(inst, num='', afterSong=False) -> int:
    if not inst.hasVC():
        return -1

    if inst.queue.len() == 0:
        return -1

    # handle numbers:
    if not num == '':
        try:
            num = int(num)
        except:
            return -1

        if num < 0 or num > inst.queue.len():
            return -1
        
        if num == 0:
            next = 0
        else:
            next = num - 1
    # skip no number
    else:
        next = inst.current + 1
        # roll over forward
        if next >= inst.queue.len():
            next = 0

    # drop play.after to avoid recursive skipping
    if inst.vc.is_playing():
        if not afterSong:
            inst.skipSkip = True
        inst.vc.stop()

    play_from_queue(next, inst)
    return 0
    

def play_from_queue(index, inst):
    title = inst.queue[index].title
    file = 'songs/' + re.sub(r'[\|/,:&$#"]', '', title) + '.mp3'

    inst.vc.play(discord.FFmpegPCMAudio(file), after=inst.after_song)
    inst.current = index
    resume(inst)

