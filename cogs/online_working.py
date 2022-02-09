import discord
from discord.ext import commands

#Add later
#record voice meeting
#stop recording
#create meeting
#meeting reminder
#etc..
class Professional(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
  bot.add_cog(Professional(bot))
