import discord

class Shop:
  def __init__(self, msg):
    self.msg = msg 
    builder = discord.Embed(title="Kokomi's Whale Shop!", description="A place to shop for your desires!", color=0x00ff00)
    builder.add_field(name = "🍎 Apple - 200 Mora", value = "Simple item that heals you during battles", inline = False)
    builder.add_field(name = "🍑 Sunsettia - 200 Mora", value = "Simple item that heals you during battles", inline = False)
    # builder.add_field(name = "⚗️ Potion of Life - 10k Mora", value = "Powerful item that completely restores your heal [CANNOT BE USED IN BATTLE]", inline = False)
    self.shop_msg = builder

  async def printShop(self):
    await self.msg.channel.send(embed = self.shop_msg)
    await self.msg.channel.send("Use `k!buy <item>` to buy something!")