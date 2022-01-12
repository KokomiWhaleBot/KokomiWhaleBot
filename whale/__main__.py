import discord
from discord.ext import commands
import os
import random
import json
from datetime import datetime
from emoji_game import EmojiGame
from shop import Shop
from memory_game import MemoryGame
from replit import db
from datetime import datetime

def has(item, id):
      hasItem = False
      for key in db[str(id)]["items"].keys():
        if key == item:
          hasItem = True
      return hasItem

intents = discord.Intents.default()
# intents.members = True

db["shop_items"] = {
  "apple": 200,
  "sunsettia": 200
}

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
`{PREFIX}inv`: View current items and foods.
`{PREFIX}upgrade`: Spend Mora to upgrade stats (health or damage).""")
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
    # print(item2)
    if item2 == "apple":
      if has("apple", msg.author.id):
        db[str(msg.author.id)]["items"]["apple"]["count"] += all_count
      else:
        db[str(msg.author.id)]["items"]["apple"] = {
          "count": all_count, 
          "name": "Apples"
        } # code go brrrrr
    if item2 == "egg":
      if has("egg", msg.author.id):
        db[str(msg.author.id)]["items"]["egg"]["count"] += all_count
      else:
        db[str(msg.author.id)]["items"]["egg"] = {
          "count": all_count,
          "name": "Eggs"
        }
    if item2 == "sunsettia":
      if has("sunsettia", msg.author.id):
        db[str(msg.author.id)]["items"]["sunsettia"]["count"] += all_count
      else:
        db[str(msg.author.id)]["items"]["sunsettia"] = {
          "count": all_count,
          "name": "Sunsettias"
        } 
    if item2 == "wood":
      if has("wood", msg.author.id):
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
    tokens = MSG.split(" ")
    if len(tokens) != 1:
      multip = 1
      try:
        multip = int(tokens[2])
      except:
        pass # put error here later
      item_to_buy = tokens[1]
      shop_items = db["shop_items"]
      try:
        shop_items[item_to_buy]
      except:
        await msg.channel.send(f"{msg.author.mention}, {item_to_buy} is not an item in the shop. Please use `k!shop` to see a list of items")
      cost = shop_items[item_to_buy] * multip
      user_mora = db[str(msg.author.id)]["mora"]
      if user_mora >= cost:
        db[str(msg.author.id)]["mora"] -= cost
        if has(item_to_buy, msg.author.id):
          db[str(msg.author.id)]["items"][item_to_buy]["count"] += 1 * multip
        else:
          db[str(msg.author.id)]["items"][item_to_buy] = {
            "name": item_to_buy,
            "count": 1 * multip
          }
        await msg.channel.send("You bought " + str(multip) + " " + item_to_buy + " for " + str(cost) + " mora!")
      else:
        await msg.channel.send("You don't have enough mora!")
    else:
      await msg.channel.send("Please specify an item to buy. Use `k!shop` to see a full list of items")

    
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
    builder = discord.Embed(title = "Stats", name = "Stats", description = ":heart: Health: " + str(db[str(msg.author.id)]["health"]) + "\n:crossed_swords: Damage: " + str(db[str(msg.author.id)]["damage"]))
    await msg.channel.send(embed = builder)

  if MSG.startswith(f"{PREFIX}upgrade") or MSG.startswith(f"{PREFIX}u"):
    a = random.choice([True, False])

    if a:
      healthp = random.randint(10, 50)
      db[str(msg.author.id)]["health"] += healthp
      if db[str(msg.author.id)]["mora"] >= 1000:
        db[str(msg.author.id)]["mora"] -= 1000
        builder = discord.Embed(title = "Upgrade", name = "Upgrade", description = ":heart: Health has been increased by " + str(healthp) + "!")
        await msg.channel.send(embed = builder)
      else:
        await msg.channel.send("You do not have enough Mora!")
    else:
      dmgp = random.randint(5, 20)
      db[str(msg.author.id)]["damage"] += dmgp
      if db[str(msg.author.id)]["mora"] >= 1000:
        db[str(msg.author.id)]["mora"] -= 1000
        builder = discord.Embed(title = "Upgrade", name = "Upgrade", description = ":crossed_swords: Damage has been increased by " + str(dmgp) + "!")
        await msg.channel.send(embed = builder)
      else:
        await msg.channel.send("You do not have enough Mora!")

#   if MSG.startswith(f"{PREFIX}battle"):
  #   boss = random.choice([""])

client.run(os.environ["TOKEN"])