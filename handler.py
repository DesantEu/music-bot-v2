import discord
import parser
from instance import Instance


prefix = '//'
admin_prefix = '>'

admins = ['Desant#0148']

instances = {}


async def handle(bot:discord.Client, message:discord.Message):
    # PM handler
    if not message.guild:
        return

    # add new instance if needed
    gid = message.guild.id
    if not gid in instances.keys():
        instances[gid] = Instance(gid, prefix)

    # parse regular commands
    if message.content.startswith(prefix):
        await parser.parse(bot, message, instances[gid])
