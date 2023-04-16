import discord

# TODO: 

messages:dict[int, discord.Message] = {}

async def send(msg:str, channel, color=discord.Color.from_rgb(255, 166, 201)):
    if msg == '':
        emb = discord.Embed()
    else:
        emb = discord.Embed(title=msg)
    emb.color = color
    message = await channel.send(embed=emb)
    messages[message.id] = message
    print(f"sent message with id {message.id}")
    return message.id

async def edit(id, title:str, body:dict[str,str]={}, color=discord.Color.from_rgb(255, 166, 201)):
    if id in messages:
        emb = discord.Embed(title=title)
        if not body == {}:
            for i in body:
                emb.add_field(name=i, value=body[i])

        emb.color = color
                
        messages[id] = await messages[id].edit(embed=emb)

# adds a field to an embed
async def add_status(id, name, value) -> int:
    if not id in messages or len(messages[id].embeds) == 0:
        return -1

    print("adding field")
    emb = messages[id].embeds[0].add_field(name=name, value=value)
    messages[id] = await messages[id].edit(embed=emb)

    return len(messages[id].embeds[0].fields) - 1


async def edit_status(id, ind, value) -> int:
    if not id in messages or len(messages[id].embeds) == 0 or ind > len(messages[id].embeds[0].fields) - 1:
        return -1

    name = messages[id].embeds[0].fields[ind].name

    # emb = messages[id].embeds[0].remove_field(ind).insert_field_at(ind, name=name, value=value)
    emb = messages[id].embeds[0].set_field_at(ind, name=name, value=value)
    messages[id] = await messages[id].edit(embed=emb)
    return 0


def isInVC(author):
    return type(author) == discord.Member and not author.voice is None


async def join(message, inst) -> int:
    print('trying to join vc')
    try:
        # connect if not yet connected
        if not inst.hasVC():
            print('im not in a vc')
            inst.vc = await message.author.voice.channel.connect()
            print('connected to vc')
            return 0
        print('im in vc')
        # move to other channel maybe
        if not inst.vc.channel == message.author.voice.channel:
            print('trying to move to another vc')
            await inst.vc.move_to(message.author.voice.channel)
            print('moved')
        return 0
    except Exception as e:
        print(f"exception caught: {e}")
        return -1

async def leave(inst) -> int:
    try:
        if not inst.hasVC:
            print('cant leave vc: not in a vc')
            return 1

        await inst.vc.disconnect()
        del(inst.vc)
        print('left vc')

        return 0
    except Exception as e:
        print(f'exception leaving: {e}')

        return -1


class reactions:
    check = '✅'
    cross = '❌'
    fyou = '🖕'
    wave = '👋'
    thumbs_up = '👍'
   
    cold = '🥶'
    hot = '🥵'

    pls ='🥺'
    pls_tears = '🥹'
    

# async def edit_title(id, title):
#     if not id in messages or len(messages[id].embeds) == 0:
#         return -1
#     
#     old_emb = messages[id].embeds[0]
#     emb = discord.Embed(title=title, color=old_emb.color)
#     for i in old_emb.fields:
#         emb.add_field(name=i.name, value=i.value)
#
#     messages[id] = await messages[id].edit(embed=emb)
#
#

