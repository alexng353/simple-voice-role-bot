import discord
import json

def main():
  f = open("config.json", "r")
  config = json.load(f)
  f.close()
  
  def save():
    f = open("config.json", "w")
    json.dump(config, f)
    f.close()

  class Client(discord.Client):
    async def on_ready(self):
      print(f'Logged on as {self.user}!')

    async def on_message(self, message):
      if message.author == self.user:
        return

      if message.content.startswith('!'):

        command = message.content.split(' ')[0][1:]
        args = message.content.split(' ')[1:]

        if message.author.guild_permissions.administrator is False:
          await message.channel.send("You do not have permission to use this bot.")
          return
        match command.lower():
          case 'setchannel':
            if message.author.guild_permissions.administrator:
              if not args:
                await message.channel.send('Please specify a channel.')
                return
              if args[0] == 'all':
                config["settings"]["channels"] = ["all"]
                save()
                await message.channel.send('All channels are now enabled.')
                return
              if args[0] == 'none':
                config["settings"]["channels"] = []
                save()
                await message.channel.send('All channels are now disabled.')
                return
              if args[0] == 'list':
                await message.channel.send(config["settings"]["channels"])
                return
              if args[0] == 'add':
                if not args[1]:
                  await message.channel.send('Please specify a channel.')
                  return
                if args[1] in config["settings"]["channels"]:
                  await message.channel.send('Channel already enabled.')
                  return
                config["settings"]["channels"].append(args[1])
                save()
                await message.channel.send('Channel added.')
                return
              if args[0] == 'remove':
                if not args[1]:
                  await message.channel.send('Please specify a channel.')
                  return
                if args[1] not in config["settings"]["channels"]:
                  await message.channel.send('Channel already disabled.')
                  return
                config["settings"]["channels"].remove(args[1])
                await message.channel.send('Channel removed.')
                return
              if args[0] == 'help':
                await message.channel.send('```setchannel [all|none|list|add|remove] [channel_id]```')
                return
              else:
                await message.channel.send('Invalid command.')
                return

            else:
              await message.channel.send('You do not have permission to use this command.')
              return
          case 'setvoicerole':
            # try:
            try:
              role = discord.utils.get(message.guild.roles, id=int(args[0]))
              config["settings"]["roles"]["voice"] = int(args[0])

              f = open("config.json", "w")
              json.dump(config, f)
              f.close()

              await message.channel.send(f'Voice role set to "{role.name}".')
            except:
              await message.channel.send('Usage: !setvoicerole <role id>')
            return
          case 'help':
            await message.channel.send("\n".join(config['help']))
            return
          case _:
            if command != '':
              await message.channel.send(f'Unknown command: {command}')
            return

    async def on_voice_state_update(self, member, before, after):
      if member.id == self.user.id:
        return

      role = discord.utils.get(member.guild.roles, id=config["settings"]["roles"]["voice"])

      if after.channel is None:
        if role in member.roles:
          await member.remove_roles(role)
        return
      elif "all" in config["settings"]["channels"]:
        if role not in member.roles:
          await member.add_roles(role)
        return
      elif after.channel.id in config["settings"]["channels"]:
        if role not in member.roles:
          await member.add_roles(role)
        else:
          return
      else:
        if role in member.roles:
          await member.remove_roles(role)
        return

      if after.channel is None:
        await member.remove_roles(role)
        print(f'{member.name} left {after.channel} | role "{role.name}" removed')
        return
      elif "all" in config["settings"]["channels"]:
        await member.add_roles(role)
        print(f'{member.name} joined {after.channel.name} | role "{role.name}" added')
        return
      elif after.channel.id in config["settings"]["channels"]:
        await member.add_roles(role)
        print(f'{member.name} joined {after.channel.name} | role "{role.name}" added')
        return
      else:
        await member.remove_roles(role)
        print(f'{member.name} joined {after.channel.name} | role "{role.name}" removed')
        return

  client = Client()
  client.run(config["token"])

if __name__ == '__main__':
  main()