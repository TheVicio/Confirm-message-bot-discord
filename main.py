import discord
import config
import asyncio

class Bot(discord.Client):
    def __init__(self):
        super().__init__()
        
        async def on_message(message: discord.Message):
            pass
        
        self.run(config.TOKEN)
        
Bot()