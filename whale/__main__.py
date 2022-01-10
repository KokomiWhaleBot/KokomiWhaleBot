import discord
from discord.ext import commands
import os
import random
import json
from datetime import datetime
import threading
from emoji_game import EmojiGame

intents = discord.Intents.default()
# intents.members = True

client = discord.Client(intents=intents)

PREFIX = "k!"

bot = commands.Bot(command_prefix = PREFIX, intents=intents)
  

@client.event
async def on_ready():
  print(f"Bot logged in as {client.user}")


@client.event
async def on_message(msg):
  if msg.author == client.user:
    return

  MSG = msg.content
  
  if MSG.startswith(f"{PREFIX}help"):
    await msg.channel.send(f"""
`{PREFIX}help`: Helps with bot commands.
`{PREFIX}daily`: Recieve daily rewards. (Currently unavailable)
`{PREFIX}game`: Play a game to recieve rewards.
`{PREFIX}search`: Search to get items or small rewards.
""") # im going to remove the ``` for now.

  if MSG.startswith(f"{PREFIX}daily"):
    await msg.channel.send("This command is currently under construction!");

  if MSG.startswith(f"{PREFIX}game"):
    game_choice = random.randint(0, 2)
    if game_choice == 1 or game_choice == 2: # Change this when there are more games
      game = EmojiGame(msg, client)
      await game.run_game()
      isCorrectEmoji = game.get_info()
      if game.is_done():
        if isCorrectEmoji:
          await msg.channel.send("You had the correct emoji!")
        else:
          await msg.channel.send("You had the wrong emoji!")
        game.reset() # Resets all of the variables for cleanup and easy memory destruction
    

  if MSG.startswith(f"{PREFIX}search"):
    random_coin = random.randint(750, 2750)
    all_count = random.randint(1, 7)
    items = [f"{random_coin} Mora", f"{all_count} wood", f"{all_count} apples", f"{all_count} mushrooms", f"{all_count} eggs", f"{all_count} sunsettia"]
    item = random.choice(items)

    await msg.channel.send("You got " + item + "!")

client.run(os.environ["TOKEN"])