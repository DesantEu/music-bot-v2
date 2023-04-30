import discord
import bot_locale as loc

# TODO: 

class LongMessage:
    def __init__(self, title:str, smaller_title:str, content:list[list[str]], page=0):
        self.page:int = page
        self.pages:list[str] = []
        self.title = title
        self.smaller_title = smaller_title
        self.content = content
        self.isMultipage = False

        self.message:discord.Message

        self.regenerate()


    def regenerate(self):
        char_limit = 1024
        # handle multipage
        if len('\n'.join([f'{i[0]} {i[1]}' for i in self.content])) > char_limit:
            self.pages.clear()
            line = 0
            page = 0
            
            # generate pages
            self.pages.append('')
            while line < len(self.content):
                while line < len(self.content) and len(self.pages[page]) + len(f'{self.content[line][0]} {self.content[line][1]}') + 1 < char_limit:
                    newline =  f'{self.content[line][0]} {self.content[line][1]}\n'
                    self.pages[page] += newline
                    line += 1
                page += 1
                self.pages.append('')
            self.isMultipage = True
            self.pages.pop(-1)

        # handle single page
        else:
            self.page = 0
            self.pages.clear()

            self.pages.append('\n'.join([f'{i[0]} {i[1]}' for i in self.content]))

            self.isMultipage = False

    def genEmbed(self, color=discord.Color.from_rgb(255, 166, 201)):
        emb = discord.Embed(title=self.title)
        emb.color = color
        emb.add_field(name=self.smaller_title, value=self.pages[self.page])
        if self.isMultipage:
            emb.set_footer(text=f'{loc.page} {self.page + 1}')

        return emb


    async def edit(self, ind, status='', text=''):
        if not status == '':
            self.content[ind][0] = status

        if not text == '':
            self.content[ind][0] = text

        self.regenerate()

        await self.message.edit(embed=self.genEmbed());


    async def send(self, channel:discord.TextChannel, color=discord.Color.from_rgb(255, 166, 201)):
        self.message = await channel.send(embed=self.genEmbed(color=color))
        if self.isMultipage:
            await self.message.add_reaction(reactions.left_arrow)
            await self.message.add_reaction(reactions.right_arrow)

    async def parse_reaction(self, reaction):
        if not self.isMultipage:
            return 1
        changed = False
        if reaction == reactions.left_arrow:
            if not self.page < 1:
                self.page -= 1
                changed = True
            else:
                return 1

        elif reaction == reactions.right_arrow:
            if not self.page == len(self.pages) - 1:
                self.page += 1
                changed = True
            else:
                return 1

        if changed:
            self.regenerate()
            await self.message.edit(embed=self.genEmbed())
            return 0
        return -1
        
    def setContent(self, content:list[list[str]]):
        self.content = content
        self.regenerate()


        


    def append(self):
        return


    def __str__(self):
        return ''

messages:dict[int, discord.Message] = {}
long_messages:dict[int, LongMessage] = {}

async def send(msg:str, channel, color=discord.Color.from_rgb(255, 166, 201)):
    if msg == '':
        emb = discord.Embed()
    else:
        emb = discord.Embed(title=msg)
    emb.color = color
    message = await channel.send(embed=emb)
    messages[message.id] = message
    return message.id

async def send_long(title:str, smaller_title:str, content:list[list[str]], channel, color=discord.Color.from_rgb(255, 166, 201)):
    global long_messages

    msg = LongMessage(title, smaller_title, content)
    await msg.send(channel, color)
    long_messages[msg.message.id] = msg
    return msg.message.id
    # emb = discord.Embed(title=title)
    # emb.color = color
    # emb_content = '\n'.join([f'{i[0]} {i[1]}' for i in content])
    # emb.add_field(name=smaller_title, value=emb_content)
    # message = await channel.send(embed=emb)
    # messages[message.id] = message
    # return message.id

async def edit_long_status(id, index:int, value:str) -> int:
    await long_messages[id].edit(index, status=value)
    return 0
    # if not id in messages or len(messages[id].embeds) == 0 or len(messages[id].embeds[0].fields) == 0 or messages[id].embeds[0].fields[0].value is None:
    #     return -1
    #
    # emb = messages[id].embeds[0]
    # old_title = str(emb.fields[0].name)
    # old_content = str(emb.fields[0].value).split('\n')
    #
    # new_content = list(old_content[index])
    # new_content[0] = value
    # old_content[index] = ''.join(new_content)
    # emb.clear_fields()
    #
    # emb.add_field(name=old_title, value='\n'.join(old_content))
    #
    #
    # messages[id] = await messages[id].edit(embed=emb)
    #
    # return 0


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
    try:
        # connect if not yet connected
        if not inst.hasVC():
            inst.vc = await message.author.voice.channel.connect()
            return 0
        # move to other channel maybe
        if not inst.vc.channel == message.author.voice.channel:
            await inst.vc.move_to(message.author.voice.channel)
        return 0
    except Exception as e:
        print(f"exception caught: {e}")
        return -1

async def leave(inst) -> int:
    try:
        if not inst.hasVC:
            return 1

        await inst.vc.disconnect()
        del(inst.vc)

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

    black_circle = '⚫'
    green_circle = '🟢'
    yellow_circle = '🟡'
    orange_circle = '🟠'
    red_circle = '🔴'

    left_arrow = '⬅️'
    right_arrow = '➡️'
    

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

