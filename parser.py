import discord
from instance import Instance
import player
import localPlaylists as lpl
import bot_locale as loc
# import nowPlaying as np

import dcHandler as dc

non_vc_commands = [f'//help', f'>help']
async def parse(message:discord.Message, inst:Instance):
    msg = message.content[len(inst.prefix):]

    args = msg.split(" ", 1)
    args[0] = args[0].lower()
    if len(args) == 1:
        args.append('')

    if args[0] in ['p', 'play']:
        await player.play(message, args[1], inst)

    elif args[0] in ['s', 'skip']:
        if not inst.hasVC():
            await message.add_reaction(dc.reactions.fyou)
            return
        if player.skip(inst, num=args[1]) == 0:
            await message.add_reaction(dc.reactions.check)
        else:
            await message.add_reaction(dc.reactions.cross)

    elif args[0] in ['stop']:
        if not inst.hasVC():
            await message.add_reaction(dc.reactions.fyou)
            return
        if player.stop(inst) and await dc.leave(inst) == 0:
            await message.add_reaction(dc.reactions.wave)
        else:
            await message.add_reaction(dc.reactions.cross)

    elif args[0] in ['rm', 'remove']:
        if inst.queue.len() == 0 or not inst.hasVC():
            await message.add_reaction(dc.reactions.fyou)
            return
        if inst.queue.pop(args[1]):
            await inst.update_queue()
            if inst.queue.len() == 0:
                player.stop(inst)
            await message.add_reaction(dc.reactions.check)
        else:
            await message.add_reaction(dc.reactions.cross)

    elif args[0] in ['cc', 'clear']:
        if not inst.hasVC() or inst.queue.len() == 0:
            await message.add_reaction(dc.reactions.fyou)
            return

        if player.stop(inst):
            await message.add_reaction(dc.reactions.check)
        else:
            await message.add_reaction(dc.reactions.cross)
            

    elif args[0] in ['q', 'queue']:
        if inst.queue.len() == 0 or not inst.hasVC():
            await message.add_reaction(dc.reactions.fyou)
            return

        content = inst.queue.toContent()
        emb = await dc.send_long(loc.queue, loc.now_playing + '...', content, message.channel)
        inst.queue_messages.append(emb)

    elif args[0] in ['save', 'ss']:
        await lpl.save_playlist(message, args[1], inst)

    elif args[0] in ['pp']:
        await lpl.play_playlist(message, args[1], inst)

    elif args[0] in ['pl']:
        await lpl.list_playlists(message, args[1])
    

    elif args[0] in ['join']:
        if not dc.isInVC(message.author):
            await message.add_reaction(dc.reactions.fyou)
            return

        if await dc.join(message, inst) == 0:
            await message.add_reaction(dc.reactions.check)
        else:
            await message.add_reaction(dc.reactions.cross)

    elif args[0] in ['test']:
        await dc.send_long('asd', 'asd', [['asd', 'asd']], message.channel)
        

    #
    # elif args[0] in ['leave']:
    #     await dc.leave(inst)

#     if args[0] in ['p', "play"]:
#         await mplayer.play(bot, args[1], message)
#     elif args[0] in ['pt', "playtop"]:
#         await mplayer.play(bot, args[1], message, play_top=True)
#
#     elif args[0] in ['clean', 'clear', 'cc']:
#         await mplayer.clear_queue(message)
#
#     elif args[0] == 'stop':
#         await mplayer.stop(bot, message)
#
#     elif args[0] in ['s', 'skip']:
#         await mplayer.skip(num=args[1], message=message)
#
#     elif args[0] in ['n', 'next']:
#         await mplayer.next(message)
#
#     elif args[0] in ['b', 'back']:
#         await mplayer.back(message)
#
#     elif args[0] == 'pause':
#         await mplayer.pause(message)
#
#     elif args[0] in ['q', 'queue']:
#         await mplayer.print_queue(message)
#     elif args[0] in ['np', 'now']:
#         await mplayer.now_playing(message)
#
#     elif args[0] in ['rm', 'remove']:
#         await mplayer.remove(args[1], message)
#
#     elif args[0] in ['save', 'ss']:
#         await mplayer.save_playlist(args[1], message)
#     elif args[0] in ['pp']:
#         await mplayer.play_playlist(args[1], message, bot)
#
#     elif args[0] in ['pl']:
#         await mplayer.list_playlist(args[1], message, bot)
#
#     elif args[0] in ['v', 'volume']:
#         await mplayer.volume_(args[1], message, bot)
#
#     elif args[0] == 'help':
#         await help(bot, chan)
#
#
# async def parse_admin(bot, message):
#     msg = message.content.lower()[1:]
#     chan = message.channel
#
#     args = msg.split(" ", 1)
#     args[0] = args[0].lower()
#     if len(args) == 1:
#         args.append('')
#
#     if args[0] == 'clean':
#         shutil.rmtree('queue')
#         await msender.send('Освободил место', message.channel)
#
#     elif args[0] == 'dj':
#         bot.dj_check = not bot.dj_check
#         await msender.send(f'Проверка на роль: {bot.dj_check}', message.channel)
#
#     elif args[0] == 'debug':
#         bot.debug = not bot.debug
#         await msender.send(f'Можно ломаться: {bot.debug}', message.channel)
#
#     elif args[0] == 'shutdown':
#         await msender.send('Смэрть', chan)
#         exit()
#
#     elif args[0] in ['dpl', 'delpl', 'rmpl']:
#         await mplayer.del_playlist(args[1], message)
#
#     elif args[0] in ['admin', 'adminonly', 'ao']:
#         bot.admin_only = not bot.admin_only
#         await msender.send(f'Админ онли: {bot.admin_only}', message.channel)
#
#     elif args[0] == 'help':
#         await help(bot, chan, admin=True)
#

async def help(bot, chan, admin=False):
    commands = []
    descriptions = []
    if admin:
        path = 'help_admin.txt'
    else:
        path = 'help.txt'

    with open(path, 'r', encoding="utf-8") as file:
        for i in file.readlines():
            temp = i.split(" - ")
            commands.append(temp[0])
            descriptions.append(temp[1])
    emb = discord.Embed()
    emb.color = discord.Color.orange()
    prefix = bot.prefix if not admin else bot.admin_prefix
    for i in range(len(commands)):
        emb.add_field(
            name=prefix + f' {prefix}'.join(commands[i].split(", ")), value=descriptions[i], inline=False)
    await chan.send(embed=emb)
