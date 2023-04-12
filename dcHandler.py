import discord

# TODO: 

messages:dict[int, discord.Message] = {}

async def send(msg:str, channel, color=discord.Color.from_rgb(255, 166, 201)):
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
                
        await messages[id].edit(embed=emb)

# adds a field to an embed
async def add_status(id, name, value) -> int:
    if not id in messages or len(messages[id].embeds) == 0:
        return -1

    print("adding field")
    emb = messages[id].embeds[0].add_field(name=name, value=value)
    await messages[id].edit(embed=emb)

    return len(messages[id].embeds[0].fields) - 1


async def edit_status(id, ind, value):
    if not id in messages or len(messages[id].embeds) == 0 or ind > len(messages[id].embeds[0].fields) - 1:
        return -1

    name = messages[id].embeds[0].fields[ind].name

    # emb = messages[id].embeds[0].remove_field(ind).insert_field_at(ind, name=name, value=value)
    emb = messages[id].embeds[0].set_field_at(ind, name=name, value=value)
    await messages[id].edit(embed=emb)

async def edit_title(id, title):
    if not id in messages or len(messages[id].embeds) == 0:
        return -1
    
    old_emb = messages[id].embeds[0]
    emb = discord.Embed(title=title, color=old_emb.color)
    for i in old_emb.fields:
        emb.add_field(name=i.name, value=i.value)

    await messages[id].edit(embed=emb)



