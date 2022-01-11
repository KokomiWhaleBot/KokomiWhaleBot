import discord
from discord.ext import commands
import os
import random
import json
from datetime import datetime
import threading
from emoji_game import EmojiGame
from shop import Shop
from replit import db
from datetime import datetime

intents = discord.Intents.default()
# intents.members = True

client = discord.Client(intents=intents)

PREFIX = "k!"

def checkIfUserExists(author):
  try:
    db[str(author)]
  except:
    db[str(author)] = {
      "mora": 0,
      "items": [],
      "health": 100,
      "damage": 10, # ILL BRB - DARK
      "game_cooldown": None
    } # Set up account

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
`{PREFIX}balance`: View Mora balance.
`{PREFIX}inv`: View current items and foods.

> Tip: You can shorten the function name for easier access!
""") # im going to remove the ``` for now.

  if MSG.startswith(f"{PREFIX}daily"):
    await msg.channel.send("This command is currently under construction!");

  if MSG.startswith(f"{PREFIX}game"):
    checkIfUserExists(msg.author.id)
    game_choice = random.randint(1, 2)
    if game_choice == 1 or game_choice == 2: # Change this when there are more games
      game = EmojiGame(msg,   client)
      await game.run_game()
      isCorrectEmoji = game.get_info()
      if game.is_done():
        if isCorrectEmoji:
          await msg.channel.send("You had the correct emoji! You got 100 Mora!")
          db[str(msg.author.id)]["mora"] += 100
        else:
          await msg.channel.send("You had the wrong emoji!")
        game.reset() # Resets all of the variables for cleanup and easy memory destruction
    

  if MSG.startswith(f"{PREFIX}search"):
    random_coin = random.randint(750, 2750)
    all_count = random.randint(1, 7)
    items2 = [f"{random_coin} Mora", f"{all_count} wood", f"{all_count} apples", f"{all_count} mushrooms", f"{all_count} eggs", f"{all_count} sunsettia"]
    item2 = random.choice(items2)

    db[str(msg.author.id)]["items"].append(item2)

    await msg.channel.send("You got " + item2 + "!")
  
  if MSG.startswith(f"{PREFIX}shop"):
    shop = Shop(msg)
    await shop.printShop()
    
  if MSG.startswith(f"{PREFIX}bal") or MSG.startswith(f"{PREFIX}balance") or MSG.startswith(f"{PREFIX}mora"):
    checkIfUserExists(msg.author.id)
    await msg.channel.send("You have " + str(db[str(msg.author.id)]["mora"]) + " Mora!")

  if MSG.startswith(f"{PREFIX}inv") or MSG.startswith(f"{PREFIX}inventory"):
    checkIfUserExists(msg.author.id)
    # rn items = []
    item = ""
    for i in db[str(msg.author.id)]["items"]:
      item += i
    if item == "" or len(db[str(msg.author.id)]["items"]) == 0:
      await msg.channel.send("You have no items!")
    else:
      await msg.channel.send("You have " + item + " items!")

  if MSG.startswith(f"{PREFIX}stats") or MSG.startswith(f"{PREFIX}st"):
    checkIfUserExists(msg.author.id)
    await msg.channel.send("Health: " + str(db[str(msg.author.id)]["health"]) + "\nDamage: " + str(db[str(msg.author.id)]["damage"]))

client.run(os.environ["TOKEN"])