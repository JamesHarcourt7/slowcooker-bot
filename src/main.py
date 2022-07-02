import discord
import json


class SlowCookerBot(discord.Client):

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.author.id == self.user_id:
            if message.content == "!start":
                await message.channel.send("i cant")
            elif message.content == "!stop":
                await message.channel.send("i cant")
        else:
            await message.channel.send("You do not have slowcooker privileges.")


def getConfig():
    f = open('config.json', 'r')
    config = json.load(f)
    f.close()
    return config


if __name__ == "__main__":
    config = getConfig()

    client = SlowCookerBot(config["user"])
    client.run(config["token"])
