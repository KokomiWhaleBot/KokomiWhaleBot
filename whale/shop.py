import discord

class Shop:
  def __init__(self, msg):
    self.msg = msg 
    builder = discord.Embed(title="Whale Shop!", description="A place to shop for your desires!", color=0x00ff00)
    builder.add_field(name = "🍎 Apple - 100 Mora", value = "Simple item that makes you less hungry!", inline = False)
    self.shop_msg = builder

  async def printShop(self):
    await self.msg.channel.send(embed = self.shop_msg)