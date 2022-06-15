import os
import time

import discord
from discord import Message, VoiceChannel

from routes.audio import create_audio


class Bot:
    def __new__(cls):
        client = discord.Client()
        @client.event
        async def on_ready():
            print("{0.user} is now online!".format(client))

        @client.event
        async def on_message(message: Message):
            if message.author == client.user:
                return

            elif message.content.startswith('>'):
                return await message.channel.send('Cuzão')
            elif message.content.startswith('time'):
                return await message.channel.send('Cuzão',file=discord.File("temp.mp3"))
            if message.content.startswith('!'):
                channel: VoiceChannel = message.author.voice.channel
                voice = await channel.connect()
                await create_audio(message.content[1:],"temp.mp3")
                l = len(message.content)
                voice.play(discord.FFmpegPCMAudio(executable="C:/Users/AzK-v/Documents/dev/ffmpeg/ffmpeg.exe",source='temp.mp3'))
                time.sleep(int(l*0.3)+1)
                voice_client = message.guild.voice_client
                await voice_client.disconnect()
        return client

    def __enter__(self):
        print("Enter")

    def __exit__(self):
        bot.logout()
        bot.close()
        print("Sair")
        exit()
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    bot = Bot()
    bot.run(os.getenv("BOT_TOKEN"))
