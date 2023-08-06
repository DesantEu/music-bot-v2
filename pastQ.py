import discord
import bot_locale as loc
import dcHandler as dc
import instance

def add_rmlist(inst: instance.Instance, song_name: str):
    inst.rmlist.append(song_name)
    if len(inst.rmlist) > 50:
        inst.rmlist.pop(0)

async def send_rmlist(inst: instance.Instance, message: discord.Message):
    if len(inst.rmlist) == 0:
        await message.add_reaction(dc.reactions.fyou)
        return

    content = []

    for i in inst.rmlist:
        content.append(['>', i])
    
    await dc.send_long(loc.rmlist_title, loc.rmlist_smaller_title, content, message.channel)


async def send_past_queues():
    pass

async def play_past_queue():
    pass
