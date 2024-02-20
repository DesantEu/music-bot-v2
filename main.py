import discord
import handler
import os
import atexit
import cacheHandler as cahe

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.reactions = True
intents.members = True


client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Game(name='//help'))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    await handler.handle(message, client)

@client.event
async def on_voice_state_update(member, before, after):
    if member == client.user:
        await handler.handle_voice(member, before, after)

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return

    await handler.handle_reaction_add(reaction, user)


def on_exit():
    handler.instances.clear()
    cahe.save_cache()
    

atexit.register(on_exit)


# yes, you need to make a token.txt
if os.path.exists('testToken.txt'):
    with open('testToken.txt', 'r') as token:
        client.run(token.read())
else:
    with open('token.txt', 'r') as token:
        client.run(token.read())
