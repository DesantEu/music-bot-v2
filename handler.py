import discord
import parser
import bot_locale as loc
from instance import Instance
import dcHandler as dc
import os

if not os.path.exists('testToken.txt'):
    prefix = '//'
    admin_prefix = '>'
else:
    prefix = '..'
    admin_prefix = ','


admins = ['Desant#0148']

instances:dict[int, Instance] = {}


async def handle(bot:discord.Client, message:discord.Message):
    # PM handler
    if not message.guild:
        await message.channel.send(loc.pm_reply)
        return

    # add new instance if needed
    gid = message.guild.id
    if not gid in instances.keys():
        instances[gid] = Instance(gid, prefix)

    # parse regular commands
    if message.content.startswith(prefix):
        await parser.parse(bot, message, instances[gid])


async def handle_voice(member, before, after):
    if not dc.isInVC(member):
        await instances[member.guild.id].on_disconnect()
