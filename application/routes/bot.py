import os

import discord
class Bot:
    def __new__(cls):
        client = discord.Client()
        @client.event
        async def on_ready():
            print("{0.user} is now online!".format(client))

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return
            if message.content.startswith('>'):
                await message.channel.send('Cuzão')
            if message.content.startswith('>lol'):
                await message.channel.send('Noob')
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
