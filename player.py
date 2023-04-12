from instance import Instance
import discord
import ytHandler as yt
import dcHandler as dc
import bot_locale as loc
import playlists

async def play(bot:discord.Client, message:discord.Message, prompt:str, inst:Instance):
    # handle empty prompts
    if prompt == '' and not inst.isPaused:
        await dc.send(loc.no_prompt, message.channel)
        return

    

    # handle links
    if prompt.startswith('https://'):
        # handle playlists
        if 'list=' in prompt:
            await playlists.play_playlist(bot, message, prompt, inst)
        # handle a single song
        else:
            await yt.play_link(bot, message, prompt, inst)
    else:
        await yt.play_prompt(bot, message, prompt, inst)
            
        
    

async def resume(inst:Instance) -> bool:
    inst.isPlaying = True
    inst.isStopped = False
    inst.isPaused = False
    return True

async def pause(inst:Instance) -> bool:
    inst.isPlaying = False
    inst.isStopped = False
    inst.isPaused = True
    return True

