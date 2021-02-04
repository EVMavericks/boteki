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
    response = f""" I am a custom bot.

    This tweet is now up for vote! React with :+1: or :-1: Tweets will be automatically published when they 
    ```markdown
    {ctx.message.content}
    ```
    """
    print("Incomming command: ", ctx.message.content)
    print("Setting up discord vote.")
    await ctx.send(response)

bot.run(TOKEN)