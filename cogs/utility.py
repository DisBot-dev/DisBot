import discord
from discord.ext import commands
import datetime
from discord.ui import InputText, Modal
import discord
from discord.ext import commands
from discord.commands import (
  slash_command, Option
)
from .utils import get_status_code

class SuggestModal(Modal):
    def __init__(self, bot) -> None:
        super().__init__(title="New suggestion:")
        self.bot = bot
        self.add_item(InputText(label="Username", placeholder="e.g: Wumpus#0000"))
        self.add_item(
            InputText(
                label="Your suggestion",
                placeholder="What should we do for the bot?",
                style=discord.InputTextStyle.long,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        channel = self.bot.get_channel(938847118603477102)
        embed1 = discord.Embed(title="Results", color=discord.Color.blue())
        embed1.add_field(name="Username", value=self.children[0].value, inline=False)
        embed1.add_field(name="Suggestion", value=self.children[1].value, inline=False)
        await channel.respond("New suggestion!",embed=embed1)

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.time = datetime.datetime.now()
        self.today_time = self.time.strftime(" • Today at %I:%M %p")
    
    @slash_command(name="suggest", description="Send a suggestion!")
    async def suggestion(self, ctx):
      suggest = SuggestModal(self.bot)
      await ctx.interaction.response.send_modal(suggest)

    @slash_command(name="clear", description="clear an amount of messages")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount:Option(int, description="the amount of messages.", required=True)):
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
        await ctx.respond(embed=my_embed, delete_after=7)

def setup(bot):
    bot.add_cog(Utilities(bot))
