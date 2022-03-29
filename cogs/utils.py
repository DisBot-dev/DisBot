import asyncio
import json
import discord
from discord.ext import commands
from discord.ext.buttons import Paginator

def paginate(text: str):
	'''Simple generator that paginates text.'''
	last = 0
	pages = []
	for curr in range(0, len(text)):
		if curr % 1980 == 0:
			pages.append(text[last:curr])
			last = curr
			appd_index = curr
	if appd_index != len(text) - 1:
		pages.append(text[last:curr])
		return list(filter(lambda a: a != '', pages))

def dev():
    def wrapper(ctx):
        with open('data/devs.json') as f:
            devs = json.load(f)
        if ctx.author.id in devs:
            return True
        raise commands.CheckFailure()
    return commands.check(wrapper)

def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content
