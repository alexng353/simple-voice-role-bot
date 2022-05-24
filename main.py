import discord
import json
# token is in token.json

f = open("token.json", "r")
token = json.load(f)
f.close()


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()
client.run(token["token"])
