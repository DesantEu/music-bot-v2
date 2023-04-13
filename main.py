import discord
import handler

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.reactions = True


client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    await handler.handle(client, message)

# yes, you need to make a token.txt
with open('token.txt', 'r') as token:
    client.run(token.read())
