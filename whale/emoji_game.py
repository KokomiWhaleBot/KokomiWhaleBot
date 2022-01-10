import random
import discord
import asyncio

# TODO: Make it so only the author of the message that called k!game can interact with the guessing

class EmojiGame:
  def __init__(self, msg: discord.message.Message, bot):
    self.msg = msg
    self.bot = bot
    self.didGo = False 
    self.isCorrectEmoji = False
    self.isInEmojis = False
    self.delay = 1 # 1.5 is also a good delay

  def is_done(self):
    return self.didGo
  
  def get_info(self):
    return self.isCorrectEmoji

  def reset(self):
    self.didGo = False 
    self.isCorrectEmoji = False
    self.isInEmojis = False

  async def run_game(self):
    msg = self.msg
    bot = self.bot
    # 1 is emoji game
    emojis = ["👋", "😀", "🤣", "🤓", "😏", "🙁", "🤑", "🤨", "😑", "😬", "🤥", "🥶", "🤠", "😳"]
    emoji = random.choice(emojis)
    emj_msg = await msg.channel.send("Remember this emoji: " + str(emoji))
    await asyncio.sleep(self.delay) # 1.5 second delay

    # Set reactions
    await emj_msg.edit(content = "What was the emoji?")
    for i in emojis:
      await emj_msg.add_reaction(i)

    # Emoji callback  
    def check(reaction, user):
      if str(user) == "Kokomi's whale#8624":
        return False # Needed so bot doesn't listen to own reactions
      self.isInEmojis = reaction.emoji in emojis
      if self.isInEmojis:
        isCorrectEmoji = reaction.emoji == emoji
        self.didGo = True 
        self.isCorrectEmoji = isCorrectEmoji
      return self.isInEmojis
    await bot.wait_for('reaction_add', check = check) # Wait for user to add reaction 