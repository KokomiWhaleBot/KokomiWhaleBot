import discord
from discord.ext import commands
import os
import random
import json
from datetime import datetime
import threading
from emoji_game import EmojiGame
from shop import Shop
from memory_game import MemoryGame
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
      "health": 100,
      "damage": 10,
      "game_cooldown": None,
      "items": {}
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
    builder = discord.Embed(title = "Help options", name = "Help", description = f"""`{PREFIX}help`: Helps with bot commands.
`{PREFIX}daily`: Recieve daily rewards. (Currently unavailable)
`{PREFIX}game`: Play a game to recieve rewards.
`{PREFIX}si`: Search to get items.
`{PREFIX}balance`: View Mora balance.
`{PREFIX}sm`: Search to get Mora.
`{PREFIX}battle`: Battle monsters to get Mora and rewards. (Currently unavailable)
`{PREFIX}shop`: View shop to get items.
`{PREFIX}buy <item>`: Buy item from the shop.
`{PREFIX}stats`: View health and damage stats.
`{PREFIX}inv`: View current items and foods.""")
    await msg.channel.send(embed = builder)
    await msg.channel.send("> Tip: You can shorten the function name for easier access!")

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
        await game.emj_msg.clear_reactions()
        if isCorrectEmoji:
          await game.emj_msg.edit(content = f"{msg.author.mention}, you had the correct emoji! You got 1000 Mora!")
          db[str(msg.author.id)]["mora"] += 1000
        else:
          await game.emj_msg.edit(content = f"{msg.author.mention}, you had the wrong emoji!")
        game.reset() # Resets all of the variables for cleanup and easy memory destruction
    

  if MSG.startswith(f"{PREFIX}si"):
    checkIfUserExists(msg.author.id)
    
    all_count = random.randint(1, 7)
    items2 = ["apple", "wood", "egg", "sunsettia"]
    item2 = random.choice(items2)
    def has(item):
      hasItem = False
      for key in db[str(msg.author.id)]["items"].keys():
        if key == item:
          hasItem = True
      return hasItem
    # print(item2)
    if item2 == "apple":
      if has("apple"):
        db[str(msg.author.id)]["items"]["apple"]["count"] += all_count
      else:
        db[str(msg.author.id)]["items"]["apple"] = {
          "count": all_count, 
          "name": "Apples"
        } # code go brrrrr
    if item2 == "egg":
      if has("egg"):
        db[str(msg.author.id)]["items"]["egg"]["count"] += all_count
      else:
        db[str(msg.author.id)]["items"]["egg"] = {
          "count": all_count,
          "name": "Eggs"
        }
    if item2 == "sunsettia":
      if has("sunsettia"):
        db[str(msg.author.id)]["items"]["sunsettia"]["count"] += all_count
      else:
        db[str(msg.author.id)]["items"]["sunsettia"] = {
          "count": all_count,
          "name": "Sunsettias"
        } 
    if item2 == "wood":
      if has("wood"):
        db[str(msg.author.id)]["items"]["wood"]["count"] += all_count
      else:
        db[str(msg.author.id)]["items"]["wood"] = {
          "count": all_count,
          "name": "Wood"
        }
    await msg.channel.send("You got " + str(all_count) + " " + item2 + "!") # well make it better later

  if MSG.startswith(f"{PREFIX}sm"): # search money
    money_count = random.randint(500, 3750)

    db[str(msg.author.id)]["mora"] += money_count

    await msg.channel.send("You got " + str(money_count) + " Mora!")
  
  if MSG.startswith(f"{PREFIX}shop"):
    shop = Shop(msg)
    await shop.printShop()

  if MSG.startswith(f"{PREFIX}buy"):
    pass
    
  if MSG.startswith(f"{PREFIX}bal") or MSG.startswith(f"{PREFIX}balance") or MSG.startswith(f"{PREFIX}mora"):
    checkIfUserExists(msg.author.id)
    await msg.channel.send("You have " + str(db[str(msg.author.id)]["mora"]) + " Mora!")

  if MSG.startswith(f"{PREFIX}inv") or MSG.startswith(f"{PREFIX}inventory"):
    checkIfUserExists(msg.author.id)
    await msg.channel.send(f"{msg.author.mention}") # for notif
    builder = discord.Embed(title = "Inventory", name = "Inventory")
    items = db[str(msg.author.id)]["items"]

    for i in items.keys():
      text = f"You have {str(items[i]['count'])} {str(items[i]['name'])}!"
      builder.add_field(name = items[i]['name'], value = text)
    await msg.channel.send(embed = builder)

  if MSG.startswith(f"{PREFIX}stats") or MSG.startswith(f"{PREFIX}st"):
    checkIfUserExists(msg.author.id)
    await msg.channel.send("Health: " + str(db[str(msg.author.id)]["health"]) + "\nDamage: " + str(db[str(msg.author.id)]["damage"]))

#   if MSG.startswith(f"{PREFIX}battle"):
  #   boss = random.choice([""])

client.run(os.environ["TOKEN"])