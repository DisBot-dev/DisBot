import os
from app import keep_alive
from typing import List
import sqlite3
import aiosqlite
import datetime
import requests
import inspect
from cogs.utils import dev, paginate
from discord.ui import View
import discord
from discord.ext import commands
from discord import ui
from discord import Interaction
token = os.environ['DISCORD_BOT_SECRET']

__version__ = "1.0"
class Bot(commands.Bot):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)



bot = Bot(debug_guilds=[938846833667620914], command_prefix = "$", application_id = 939154180759773194)
bot.remove_command("help")

async def warninit():
	await bot.wait_until_ready()
	warndb = await aiosqlite.connect("./data/db/warnData.sqlite")
	await warndb.execute("CREATE TABLE IF NOT EXISTS warningsData (guild_id INT, admin_id INT, user_id INT, reason TEXT)")
	await warndb.commit()

class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        # A label is required, but we don't need one so a zero-width space is used
        # The row parameter tells the View which row to place the button under.
        # A View can only contain up to 5 rows -- each row can only have 5 buttons.
        # Since a Tic Tac Toe grid is 3x3 that means we have 3 rows and 3 columns.
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed
    # This is part of the "meat" of the game logic
    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.primary
            self.label = "X"
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        self.disabled = True
        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X won!"
            elif winner == view.O:
                content = "O won!"
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


# This is our actual board View
class TicTacToe(discord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == -3:
                return self.X

            elif value == 3:
                return self.O
        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == -3:
            return self.X

        elif diag == 3:
            return self.O
        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


class DropDownMenu(ui.View):
    @discord.ui.select(placeholder="Choose a category!", min_values=1, max_values=1, options=[
        discord.SelectOption(label="Games", description="We all need some fun!", emoji="🎈"),
        discord.SelectOption(label="Moderation", description="For managing your servers!", emoji="🤖"),
        discord.SelectOption(label="Utility", description="Setting up your bot! Change the prefix, clear messages and more!", emoji="🔨"),
        discord.SelectOption(label="Online Working", description="Now there is a bot for working using discord!", emoji="💻")
    ])
    async def callback(self, select, interaction: discord.Interaction):
      if select.values[0] == "Music":
        embed = discord.Embed(
          title="Music",
          description="This is the page for the music!",
          color=discord.Color.blue(),
          timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url="https://th.bing.com/th/id/OIP.HP26kTFgP6H83IDyu4wwxAHaE8?pid=ImgDet&rs=1")
        embed.add_field(name="Play", value="Play a song! `%`!", inline=False)
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
        embed.add_field(name="kick `<member>`", value="Kick a member of your server. (Permissions: kick members)", inline=False)
        embed.add_field(name="ban `<member>`", value="Ban a member of your server. (Permissions: ban members)!", inline=False)
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
        embed.add_field(name="clear `<amount>`", value="Clear an unlimited amount of messages. (Permissions: manage messages)", inline=False)
        embed.add_field(name="setprefix `<new_prefix>`", value="Change the prefix of your server. (Permissions: manage messages)!", inline=False)
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
        description=f"DisBot is a 50% English 50% French and [open source](https://github.com/DisBot-dev) discord bot for working online, it has professional, utility, moderation and game commands (**{bot.command_prefix}help** for the help command).")
      embed.add_field(name="__Credits__", value="Down below", inline=False)
      embed.add_field(name="Idea", value="Faxe", inline=False)
      embed.add_field(name="Website", value="CodeElevator(also known as NomCustom), Erwinn and Raphael5916raph", inline=False)
      embed.add_field(name="Bot code", value="CodeElevator(also known as NomCustom), Faxe and Starfit.", inline=False)
      await interaction.response.send_message(embed=embed)

@bot.event
async def on_ready():
  activity = discord.Game(name=f"/help. On {len(bot.guilds)} servers.", type=3)
  await bot.change_presence(status=discord.Game, activity=activity)
  print(f"pret {bot.user}")

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CheckFailure):
    await ctx.send("Sorry but only the developers (bot code on credits) can do this command.")
  print("Une erreur est survenue!")
  print(error)
  channel = bot.get_channel(938847126752997396)
  embed = discord.Embed(title="An error is raised!", color=discord.Color.blue(), description= f'```{error}```')
  await channel.send(embed=embed)


@bot.slash_command(name="help", description="The help command!")
async def help_slash(ctx: commands.Context):
  links = ["https://github.com/DisBot-dev/DisBot","https://discord.gg/FdfGvhGY","https://top.gg/bot/939154180759773194"]
  embed = discord.Embed(
    title=f"Welcome to {bot.user.name}!",
    description=f"**Hello {ctx.author.mention}!**\nWelcome to {bot.user.name}, for the list of commands please choose a category down below.\nMake sure to join the [Discord server]({links[1]}).\nThe bot is open source, check out on [Github]({links[0]})!\nYou can also check the top.gg page!(Not added yet)\nWork well while using the bot! (tip: use the {bot.command_prefix}bonus for playing a game with yourself)"
  )
  dropdowns=DropDownMenu()
  await ctx.respond(embed=embed, view=dropdowns)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and not filename in ['utils.py']:
        bot.load_extension(f"cogs.{filename[:-3]}")

@bot.slash_command(name="bonus", description="Play a bonus game with yourself (tictactoe)")
async def bonus_slash(ctx: commands.Context):
    await ctx.respond("Tic Tac Toe: X goes first", view=TicTacToe())

keep_alive()
bot.run(token)
discord.ext.tasks.loop(warninit)
