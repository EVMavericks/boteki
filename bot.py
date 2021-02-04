import os
import datetime
import discord
import tweepy
from dotenv import load_dotenv

from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='tweet')
async def nine_nine(ctx):

    # This line should turn into an explanatory 
    response = 'I\'m a bot and i will eb able to tweet'
    await ctx.send(response)

bot.run(TOKEN)