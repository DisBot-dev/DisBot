import discord
from discord.ext import commands
#add later
#kick
#ban
#If someone have an idea please put them here
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
  bot.add_cog(Moderation(bot))
