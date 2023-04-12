from instance import Instance
import discord
import ytHandler as yt
import dcHandler as dc
import bot_locale as loc
import playlists
import re

async def play(bot:discord.Client, message:discord.Message, prompt:str, inst:Instance):
    # handle empty prompts
    if prompt == '' and not inst.isPaused:
        await dc.send(loc.no_prompt, message.channel)
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
             isSuccessful = await playlists.play_playlist(bot, message, prompt, inst)
        # handle a single song
        else:
            isSuccessful = await yt.play_link(bot, message, prompt, inst)
    # handle text search
    else:
        isSuccessful = await yt.play_prompt(bot, message, prompt, inst)

    if not isSuccessful == 0:
        return -1

    # check vc again just to be sure
    if not dc.isInVC(message.author):
        await dc.send(loc.left_vc, message.channel)
        return -1
    else:
        await dc.join(message, inst)
        await play_file(inst.queue[0].title, inst) # TODO: remove
    
            
def stop(inst:Instance) -> bool:
    inst.isPaused = False
    inst.isPlaying = False
    inst.isStopped = True
    inst.queue.clear()
    return True


def resume(inst:Instance) -> bool:
    inst.isPlaying = True
    inst.isStopped = False
    inst.isPaused = False
    return True

def pause(inst:Instance) -> bool:
    inst.isPlaying = False
    inst.isStopped = False
    inst.isPaused = True
    return True

async def play_file(title, inst:Instance):
    file = 'songs/' + re.sub(r'[\|/,:&$#"]', '', title) + '.mp3'

    inst.vc.play(discord.FFmpegPCMAudio(file), after=inst.skip)

    discord.VoiceClient.play

class After(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)
    # def __init__(self, message, inst:Instance):
    #     self.message = message
    #     self.inst = inst


