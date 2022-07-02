import discord
import gpiozero
import json
import time


class SlowCookerBot(discord.Client):

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        
        #self.servo = gpiozero.Servo(17)
        self.off = 15
        self.low = 30
        self.medium = 45
        self.warm = 60
        
        self.start_time = 0
        self.status = "off"

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.author.id == self.user_id:
            if message.content == "!off":
                if self.start_time == 0:
                    await message.channel.send("Slow cooker is already off")
                else:
                    await message.channel.send("Turned off. Time elapsed: {}".format(formatTime(time.time() - self.start_time)))
                    self.start_time = 0
                    self.status = "off"
                    
            elif message.content == "!low":
                if self.start_time == 0:
                    await message.channel.send("Turned on. Setting temperature to low")
                else:
                    await message.channel.send("Setting temperature to low. Time elapsed: {}".format(formatTime(time.time() - self.start_time)))
                self.start_time = time.time()
                self.status = "low"
                
            elif message.content == "!medium":
                if self.start_time == 0:
                    await message.channel.send("Turned on. Setting temperature to medium")
                else:
                    await message.channel.send("Setting temperature to medium. Time elapsed: {}".format(formatTime(time.time() - self.start_time)))
                self.start_time = time.time()
                self.status = "medium"
                
            elif message.content == "!warm":
                if self.start_time == 0:
                    await message.channel.send("Turned on. Set to keep warm.")
                else:
                    await message.channel.send("Set to keep warm. Time elapsed: {}".format(formatTime(time.time() - self.start_time)))
                self.start_time = time.time()
                self.status = "warm"
                
            elif message.content == "!status":
                await message.channel.send("Current status: {}".format(self.status)) # self.servo.value))
                await message.channel.send("Time elapsed: {}".format(time.time() - self.start_time))
                
        else:
            await message.channel.send("You do not have slowcooker privileges.")


def getConfig():
    f = open('config.json', 'r')
    config = json.load(f)
    f.close()
    return config

def formatTime(diff):
    struct = time.gmtime(diff)
    return "{}hrs {}mins {}secs".format(struct.tm_hour, struct.tm_min, struct.tm_sec)

def main():
    config = getConfig()
    bot = SlowCookerBot(config['user'])
    bot.run(config['token'])


if __name__ == "__main__":
    main()
