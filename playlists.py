import dcHandler as dc
import bot_locale as loc

async def play_playlist(message, link, inst):
    await dc.send(loc.not_available, message.channel)
