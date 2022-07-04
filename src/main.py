
import discord
import gpiozero
import json
import time
from gpiozero.pins.pigpio import PiGPIOFactory

gpiozero.Device.pin_factory = PiGPIOFactory()

class SlowCookerBot(discord.Client):

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        
        self.servo = gpiozero.AngularServo(13, min_angle=-90, max_angle=90)
        self.off = -54
        self.low = -18
        self.medium = 18
        self.warm = 54
        
        self.start_time = 0
        self.status = "off"
        self.servo.angle = self.off

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
                    self.servo.angle = self.off

            elif message.content == "!low":
                if self.start_time == 0:
                    await message.channel.send("Turned on. Setting temperature to low")
                else:
                    await message.channel.send("Setting temperature to low. Time elapsed: {}".format(formatTime(time.time() - self.start_time)))
                self.start_time = time.time()
                self.status = "low"
                self.servo.angle = self.low
		
            elif message.content == "!medium":
                if self.start_time == 0:
                    await message.channel.send("Turned on. Setting temperature to medium")
                else:
                    await message.channel.send("Setting temperature to medium. Time elapsed: {}".format(formatTime(time.time() - self.start_time)))
                self.start_time = time.time()
                self.status = "medium"
                self.servo.angle = self.medium
                
            elif message.content == "!warm":
                if self.start_time == 0:
                    await message.channel.send("Turned on. Set to keep warm.")
                else:
                    await message.channel.send("Set to keep warm. Time elapsed: {}".format(formatTime(time.time() - self.start_time)))
                self.start_time = time.time()
                self.status = "warm"
                self.servo.angle = self.warm
                
            elif message.content == "!status":
                await message.channel.send("Current status: {}".format(self.status)) # self.servo.value))
                await message.channel.send("Time elapsed: {}".format(time.time() - self.start_time))
                
        else:
            if message.content in ["!low", "!high", "!warm", "!off", "!status"]:
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
