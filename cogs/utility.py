import discord
from discord.ext import commands
import datetime
#import json (adding that later)


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.time = datetime.datetime.now()
        self.today_time = self.time.strftime(" • Aujourd'hui a %I:%M %p")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount:int):
        mention = ctx.author.mention
        await ctx.channel.purge(limit=amount+1)
        my_embed = discord.Embed(
            title=f'{amount} messages deleted',
            description=f'\n\n **The messages are deleted ✅**'
            f'\n\n **🖱️ By :** {mention}',
            colour=0x87FF00)
        my_embed.set_thumbnail(url=ctx.author.avatar)
        my_embed.set_footer(text=f"\n\n{ctx.author.name}{self.today_time} ",
                            icon_url=ctx.author.avatar)
        await ctx.send(embed=my_embed, delete_after=7)

def setup(bot):
    bot.add_cog(Utilities(bot))
