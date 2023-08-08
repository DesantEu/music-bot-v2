import discord
from instance import Instance
import player
import localPlaylists as lpl
import bot_locale as loc
import pastQ as past
import playlists
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
        prompts = args[1].split('\n')
        if len(prompts) > 1:
            await playlists.play_bulk(prompts, inst, message)
        else:
            await player.play(message, args[1], inst)

    elif args[0] in ['s', 'skip']:
        if not inst.hasVC():
            await message.add_reaction(dc.reactions.fyou)
            return
        if player.skip(inst, num=args[1]) == 0:
            await message.add_reaction(dc.reactions.check)
        else:
            await message.add_reaction(dc.reactions.cross)

    elif args[0] in ['next', 'n']:
        if not inst.hasVC():
            await message.add_reaction(dc.reactions.fyou)
            return
        if player.skip(inst, num='') == 0:
            await message.add_reaction(dc.reactions.check)
        else:
            await message.add_reaction(dc.reactions.cross)

    elif args[0] in ['back', 'b']:
        if not inst.hasVC():
            await message.add_reaction(dc.reactions.fyou)
            return
        if player.skip(inst, num=str(inst.queue.len()-1)) == 0:
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

        removes = args[1].split(' ')
        success = False
        warns = 0
        max = inst.queue.len()

        # do unreasonable transformations so you can bulk remove better
        # get deletion indeces from whatever garbage the user gives
        indeces = []

        for i in removes:
            # ignore negatives from spawn
            if i.startswith('-'):
                continue

            # handle ranges
            if '-' in i:
                start = -1
                end = -1

                splits = i.split('-')

                # safety measures
                # idk how that could happen but anyway
                if len(splits) == 1:
                    warns += 1
                    continue
                # only pick (1-25)-123
                elif len(splits) > 2:
                    warns += 1
                try:
                    start = int(splits[0])
                    end = int(splits[1])
                    if end > max:
                        end = max
                        warns += 1
                # if letters are thrown in the sequence
                except:
                    warns += 1
                    continue

                # yea this would happen somehow
                if end < start:
                    warns += 1
                    continue

                for ind in range(start, end+1):
                    if ind > max:
                        warns += 1
                        continue

                    if not ind in indeces:
                        indeces.append(ind)

            # handle single numbers
            else:
                # parse int of course
                try:
                    ind = int(i)
                    if ind > max:
                        warns += 1
                        continue

                    if not i in indeces:
                        indeces.append(ind)
                # letters detected here
                except:
                    warns += 1
                    continue

        print('warns: ' + str(warns))

        # my honest reaction:
        if warns >= 3:
            print('reaction triggered')
            await message.channel.send(loc.warn_reaction)



        # reverse and delete from end cuz indeces change and shit
        indeces = sorted(indeces, reverse=True)

        for i in indeces:
            res = inst.queue.pop(str(i))
            if not res == '':
                past.add_rmlist(inst, res)
                # await inst.update_queue()
                if inst.queue.len() == 0:
                    player.stop(inst)
                success = True

        await inst.update_queue()


        if success:
            if warns > 0:
                await message.add_reaction(dc.reactions.warn)
            else:
                await message.add_reaction(dc.reactions.check)
        else:
            await message.add_reaction(dc.reactions.cross)

    elif args[0] in ['rmlist']:
        await past.send_rmlist(inst, message)

    elif args[0] in ['cc', 'clear', 'clean']:
        if not inst.hasVC() or inst.queue.len() == 0:
            await message.add_reaction(dc.reactions.fyou)
            return

        if player.stop(inst):
            await inst.update_queue()
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

    elif args[0] in ['qq']:
        if len(inst.past_queues) == 0:
            await message.add_reaction(dc.reactions.fyou)
            return

        if args[1] == '':
            await past.send_past_queues(inst, message)
        else:
            index = -1
            try:
                index = int(args[1])
                if index < 1 or index > len(inst.past_queues):
                    await message.add_reaction(dc.reactions.cross)
                    return
            except:
                await message.add_reaction(dc.reactions.cross)
                return
            await past.play_past_queue(index-1, inst, message)


    # elif args[0] in ['np']:
    #     await np.send_np(message.channel, inst)

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

    elif args[0] in ['fix']:
        # check if we in vc
        print("fixing...")
        g = message.guild
        if not g is None:
            print("found guild")
            mem = g.get_member_named("Thwew#0618")
            if not mem is None:
                print("found bot user")
                if not mem.voice is None:
                    print("found voice")
                    await dc.leave(inst)
                    await dc.join(message, inst)
                    await message.add_reaction(dc.reactions.check)

        # if not disconnect
                else:
                    print("voice not found, leaving")
                    if player.stop(inst) and await dc.leave(inst) == 0:
                        await message.add_reaction(dc.reactions.wave)
                    else:
                        await message.add_reaction(dc.reactions.cross)

                    

        # if yes reset socket

    elif args[0] in ['test']:
        await dc.send_long('asd', 'asd', [['asd', 'asd']], message.channel)
        await inst.bot.change_presence(activity=discord.Game(name='//help'))
        

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
    elif args[0] == 'help':
        await help(message.channel)
#

async def help(chan, admin=False):
    commands = []
    descriptions = []
    if admin:
        path = 'help_admin.txt'
    else:
        path = 'help.txt'

    with open(path, 'r', encoding="utf-8") as file:
        for i in file.readlines():
            if i.startswith("#"):
                continue
            temp = i.split(" - ")
            commands.append(temp[0])
            descriptions.append(temp[1])
    emb = discord.Embed()
    # emb.color = discord.Color.green()
    emb.color = discord.Color.from_rgb(252, 108, 133)
    # prefix = bot.prefix if not admin else bot.admin_prefix
    prefix = '//'
    for i in range(len(commands)):
        emb.add_field(
            name=prefix + f' {prefix}'.join(commands[i].split(", ")), value=descriptions[i], inline=False)
    await chan.send(embed=emb)
