import discord
import parser
import bot_locale as loc
from instance import Instance
import dcHandler as dc
import os
import player

if not os.path.exists('testToken.txt'):
    prefix = '//'
    admin_prefix = '>'
else:
    prefix = '..'
    admin_prefix = ','


admins = ['Desant#0148']

instances:dict[int, Instance] = {}


async def handle(message:discord.Message):
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
        await parser.parse(message, instances[gid])


async def handle_voice(member, before, after):
    if not dc.isInVC(member):
        await instances[member.guild.id].on_disconnect()


async def handle_reaction_add(reaction:discord.Reaction, user):
    # check if we want to handle reaction
    if not reaction.message.guild is None and reaction.message.guild.id in instances:
        inst = instances[reaction.message.guild.id]
        # flip pages for long messages
        if reaction.message.id in dc.long_messages:
            if await dc.long_messages[reaction.message.id].parse_reaction(reaction.emoji) >= 0:
                await reaction.message.remove_reaction(reaction, user)
                return
        # instaplay:
        player_reaction = await player.handle_reaction(reaction, inst)
        if player_reaction >= 0:
            await reaction.message.clear_reaction(reaction)
            if player_reaction == 1:
                await reaction.message.add_reaction(dc.reactions.cross)

            return
    else:
        return
