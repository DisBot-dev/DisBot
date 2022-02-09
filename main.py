import os
import datetime
import discord
from discord.ext import commands
from discord.ui import View
token = os.environ['DISCORD_BOT_SECRET']

bot = commands.Bot(command_prefix = "%",
    activity = discord.Activity(
      name= "%help for the commands!",
      type = discord.ActivityType.watching
      ),
      status = discord.Status.online)
bot.remove_command("help")

class DropDownMenu(View):
    @discord.ui.select(placeholder="Choose a category!", min_values=1, max_values=1, options=[
        discord.SelectOption(label="Games", description="We all need some fun!", emoji="🎈"),
        discord.SelectOption(label="Moderation", description="For managing your servers!", emoji="🤖"),
        discord.SelectOption(label="Utility", description="Setting up your bot! Change the prefix, clear messages and more!", emoji="🔨"),
        discord.SelectOption(label="Online Working", description="Now there is a bot for working using discord!", emoji="💻")
    ])
    async def callback(self, select, interaction: discord.Interaction):
      if select.values[0] == "Games":
        embed = discord.Embed(
          title="Games!",
          description="This is the page for the games!",
          color=discord.Color.blue(),
          timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url="https://th.bing.com/th/id/OIP.HP26kTFgP6H83IDyu4wwxAHaE8?pid=ImgDet&rs=1")
        embed.add_field(name="TicTacToe", value="Play Tic Tac Toe with a friend!", inline=False)
        embed.add_field(name="Snake", value="Play Snake (only one player)!", inline=False)
        embed.set_footer(text="The bot isn't finished yet! But there is only two commands in the game page.")
        await interaction.response.edit_message(embed=embed)
      if select.values[0] == "Moderation":
        embed = discord.Embed(
          title="Moderation!",
          description="This is the page for the moderation commands!",
          color=discord.Color.red(),
          timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url="https://th.bing.com/th/id/OIP.wReEPRJcYG7fd6NaS9cGIwHaER?w=294&h=180&c=7&r=0&o=5&dpr=1.5&pid=1.7")
        embed.add_field(name="kick", value="Kick a member of your server. (Permissions: kick members)", inline=False)
        embed.add_field(name="ban", value="Ban a member of your server. (Permissions: ban members)!", inline=False)
        embed.set_footer(text="The bot isn't finished yet!")
        await interaction.response.edit_message(embed=embed)
      if select.values[0] == "Utility":
        embed = discord.Embed(
          title="Utility!",
          description="This is the page for the utility commands!",
          color=discord.Color.green(),
          timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url="https://www.alistdaily.com/wp-content/uploads/2017/06/Discord-2-1024x410.jpg")
        embed.add_field(name="clear `amount`", value="Clear an unlimited amount of messages. (Permissions: manage messages)", inline=False)
        embed.add_field(name="setprefix `new_prefix`", value="Change the prefix of your server. (Permissions: manage messages)!", inline=False)
        embed.set_footer(text="The bot isn't finished yet!")
        await interaction.response.edit_message(embed=embed)
      if select.values[0] == "Online Working":
        embed = discord.Embed(
          title="Working using Discord!",
          description="This is the page for the working commands!",
          color=discord.Color.dark_purple(),
          timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url="https://th.bing.com/th/id/OIP.lZD7ka_IXX7lJxkS6zOAMQAAAA?pid=ImgDet&rs=1")
        embed.set_footer(text="The bot isn't finished yet!")
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label='Info and Credits', style=discord.ButtonStyle.primary, emoji='💡')
    async def button_callback(self, button, interaction):
      embed = discord.Embed(
        title=f"__What is {bot.user.name}?__",
        description=f"DisBot is a 50% English 50% French and [open source](https://github.com/DisBot-dev) discord bot for working online, it has professional, utility, moderation and game commands (**{bot.command_prefix}help** for the help command.")
      embed.add_field(name="__Credits__", value="Down below", inline=False)
      embed.add_field(name="Idea", value="Faxe", inline=False)
      embed.add_field(name="Dashboard", value="CodeElevator(also known as NomCustom), Erwinn and Raphael5916raph", inline=False)
      embed.add_field(name="Bot code", value="CodeElevator(also known as NomCustom), Faxe and Starfit.", inline=False)
      await interaction.response.send_message(embed=embed)
@bot.event
async def on_ready():
  print(f"pret {bot.user}")

@bot.event
async def on_command_error(ctx, error):
  print("Une erreur est survenue!")
  print(error)
  channel = bot.get_channel(938847126752997396)
  embed = discord.Embed(title="Une erreur est survenue!", color=discord.Color.blue(), description= f'```{error}```')
  await channel.send(embed=embed)

@bot.command(name="help", description="The help command.")
async def help(ctx):
  links = ["https://github.com/DisBot-dev/DisBot","https://discord.gg/9wmB5CMS","https://top.gg/bot/939154180759773194"]
  embed = discord.Embed(
    title=f"Welcome to {bot.user.name}!",
    description=f"**Hello {ctx.author.mention}!**\nWelcome to {bot.user.name}, for the list of commands please choose a category down below.\nMake sure to join the [Discord server]({links[1]}).\nThe bot is open source, check out on [Github]({links[0]})!\nYou can also check the top.gg page!(Not added yet)\nWork well while using the bot!"
  )
  dropdowns=DropDownMenu()
  await ctx.send(embed=embed, view=dropdowns)

@bot.slash_command(name="help", description="The help command!")
async def help_slash(ctx):
  links = ["https://github.com/DisBot-dev/DisBot","https://discord.gg/9wmB5CMS","https://top.gg/bot/939154180759773194"]
  embed = discord.Embed(
    title=f"Welcome to {bot.user.name}!",
    description=f"**Hello {ctx.author.mention}!**\nWelcome to {bot.user.name}, for the list of commands please choose a category down below.\nMake sure to join the [Discord server]({links[1]}).\nThe bot is open source, check out on [Github]({links[0]})!\nYou can also check the top.gg page!(Not added yet)\nWork well while using the bot!"
  )
  dropdowns=DropDownMenu()
  await ctx.send(embed=embed, view=dropdowns)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(token)
