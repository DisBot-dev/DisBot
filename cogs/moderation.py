import discord
from discord.ext import commands
from discord.commands import slash_command, Option, SlashCommandGroup
import aiosqlite
#a ajouter
#kick
#ban

class warn(commands.Cog, name="Warn", description="Warn commands"):
    def __init__(self, bot):
        self.bot = bot
    warns = SlashCommandGroup(
      "warnings", "Commands related to warns"
                                 )
    @warns.command(name="warn", description="Warn a member", hidden=False)
    @commands.has_permissions(kick_members=True)
    async def warn(
      self, ctx, member: Option(discord.Member, "The member you want to warn", required=True), *, reason: Option(str, "The reason of the warn.", required=False)
    ):

        warndb = await aiosqlite.connect("./data/db/warnData.sqlite")

        if member == ctx.author:
            emb = discord.Embed(title='Error',description = "You can't warn yourself !", color=discord.Color.red())
            await ctx.respond(embed = emb)
            return

        else:
            await warndb.execute('INSERT OR IGNORE INTO warningsData (guild_id, admin_id, user_id, reason) VALUES (?,?,?,?)', (ctx.guild.id, ctx.author.id, member.id, reason))
            await warndb.commit()

            em = discord.Embed(title="Warn",color=discord.Color.random())
            em.add_field(name='Staff:',value=ctx. author.mention,inline=False)
            em.add_field(name='Member:',value=member.mention,inline=False)
            em.add_field(name='Reason:',value=reason,inline=False)
            await ctx.respond(embed = em)

    @warns.command(name="clear",description="Remove warns from a member.", hidden=False)
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def removewarn(self, ctx, member:Option(discord.Member, "The member.")):

        warndb = await aiosqlite.connect("./data/db/warnData.sqlite")

        if member == ctx.author:
            emb = discord.Embed(title='Error',description = "You can't clear your warns !", color=discord.Color.red())
            await ctx.respond(embed = emb)
            return

        else:
            await warndb.execute("DELETE FROM warningsData WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, member.id))
            await warndb.commit()
            emb = discord.Embed(title="ALL WARNS ARE GONE !",color=discord.Color.random())
            emb.add_field(name='Staff:',value=ctx.author.mention,inline=False)
            emb.add_field(name='Member:',value=member.mention,inline=False)
            await ctx.respond(embed = emb)
            
    @warns.command(hidden=False,description="Show the warnings of a member", name="warns")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def warnings(self, ctx, member:Option(discord.Member, "The member for showing the warnings.")):
        warndb = await aiosqlite.connect("./data/db/warnData.sqlite")
        index = 0
        embed=discord.Embed(title=f"Warns of {member.name}", description="", color=0x000000)
        embed.set_thumbnail(url=member.avatar)
        msg = await ctx.send(embed=embed)
        async with warndb.execute('SELECT admin_id, reason FROM warningsData WHERE guild_id = ? AND user_id = ?', (ctx.guild.id, member.id,)) as cursor:
            if cursor == None:
              embed.description += "This member doesn't have any warns."
            async for entry in cursor:
                index += 1
                admin_id, reason = entry
                embed.description += f"Number of warns: {index} | Staff: {ctx.guild.get_member(admin_id)} | Reason: {reason}\n"
            await msg.edit(embed=embed)

    @warns.command(hidden=False,description="Show your warnings.", name="mywarns")
    @commands.guild_only()
    async def mywarnings(self, ctx):
        member = ctx.author
        index = 0
        embed=discord.Embed(title=f"Warns of {member.name}", description="", color=0x000000)
        embed.set_thumbnail(url=member.avatar)
        msg = await ctx.send(embed=embed)
        warndb = await aiosqlite.connect("./data/db/warnData.sqlite")
        async with warndb.execute('SELECT admin_id, reason FROM warningsData WHERE guild_id = ? AND user_id = ?', (ctx.guild.id, member.id,)) as cursor:
          if cursor == None:
            embed.description += "This member doesn't have any warns."  
          async for entry in cursor:
                index += 1
                admin_id, reason = entry
                admin_name = ctx.guild.get_member(admin_id)
                embed.description += f"Warn: {index} | Staff: {admin_name} | Reasons: {reason}\n"
          await msg.edit(embed=embed)


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
  bot.add_cog(Moderation(bot))
  bot.add_cog(warn(bot))
