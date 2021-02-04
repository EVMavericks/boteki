import os
import datetime
import discord
import tweepy
import config
from dotenv import load_dotenv

from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='tweet')
async def nine_nine(ctx):

    # This line should turn into an explanatory 
    response = f"""
    :fire: **Vote Started**
    React with :+1:  or :-1: to publish or skip the tweet.
    Tweets with a net socre of {config.required_score} points within {config.approval_window} days will be published automatically.
    ```markdown
    {ctx.message.content[7:]}
    ```
    """
    print("Incomming command: ", ctx.message.content)
    print("Setting up discord vote.")

    emojis = ["👍", "👎", "📮"]
    tweetBot = bot.get_channel(806923512270422016)

    print(" ~ Sending Message")
    poll = await tweetBot.send(response)

    print(" ~ Adding Reactions")
    for emoji in emojis:
        await poll.add_reaction(emoji)

    ## Now there must be a vote emoticon set for easy votes
    print(poll.message)
    print(poll.message.reactions)

bot.run(TOKEN)