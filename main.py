import discord
import config
import asyncio
import re
from datetime import datetime

class Bot(discord.Client):
    def __init__(self):
        super().__init__()
        
        @self.event
        async def on_message(message: discord.Message):
            if isinstance(message.channel, discord.TextChannel) and not message.author == self.user:
                await message.delete()
                message_to_confirm = await self.send_dm(f'Mensagem a aprovar:\nDatetime: {datetime.now().strftime("%d/%m %H:%M:%S")}\nCanal ID: {message.channel.id}\nGrupo ID: {message.guild.id}\nAutor ID: {message.author.id}\nMensagem: {message.content}', message.guild.owner)
                for emote in ['✔','❌']:
                    await message_to_confirm.add_reaction(emote)
    
        @self.event
        async def on_reaction_add(reaction:discord.Reaction, user:discord.User):
            if not user.bot:
                CHANNEL_ID = int(re.findall(r'Canal ID: ([0-9]+)', reaction.message.content)[0])
                GROUP_ID = int(re.findall(r'Grupo ID: ([0-9]+)', reaction.message.content)[0])
                AUTHOR_ID = int(re.findall(r'Autor ID: ([0-9]+)', reaction.message.content)[0])
                MESSAGE = re.findall(r'Mensagem: (.+)', reaction.message.content)[0]
                DATETIME = re.findall(r'Datetime: ([0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})', reaction.message.content)[0]

                if reaction.emoji == '✔':
                    Group = self.get_guild(GROUP_ID)
                    Author = Group.get_member(AUTHOR_ID)
                    Channel = Group.get_channel(CHANNEL_ID)
                    
                    await Channel.send(f'{DATETIME} {Author.name} : {MESSAGE}')
                    await reaction.message.delete()
                elif reaction.emoji == '❌':
                    await reaction.message.delete()
        
        self.run(config.TOKEN)
    
    async def send_dm(self, text:str, receiver:discord.User):
        DMChannel = await receiver.create_dm() if not receiver.dm_channel else receiver.dm_channel
        return await DMChannel.send(text)

        
Bot()