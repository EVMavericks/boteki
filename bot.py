import asyncio
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
async def twitterPoll(ctx):

    # This line should turn into an explanatory 
    response = f"""\n
    :fire: **Vote Started**
    React with :+1:  or :-1: to publish or skip the tweet.
    Tweets with a net socre of {config.required_score} points within {config.approval_window} days will be published automatically.
    ```markdown

    {ctx.message.content[7:]}
    ```
    """
    print("Incomming command: ", ctx.message.content)
    print("Setting up discord vote.")
    tweetBot = bot.get_channel(806923512270422016)

    print(" ~ Sending Message")
    poll = await tweetBot.send(response)

    print(" ~ Adding Reactions")
    emojis = ["👍", "👎"]

    for emoji in emojis:
        await poll.add_reaction(emoji)
    
    print(poll)
    print(f"{poll.id=}")
    
    ## Now there must be a vote emoticon set for easy votes
    print(" ~ About to sleep and check reactions")
    asyncio.sleep(10)
    vote_results = await tweetBot.fetch_message(poll.id)
    print(f"{vote_results=}")
    print(f"{vote_results.reactions=}")



    # def check(reaction, user):
    #     return user == poll.author and str(reaction.emoji) == '👍'

    # try:
    #     reaction, user = await tweetBot.wait_for('reaction_add', timeout=5.0, check=check)
    # except asyncio.TimeoutError:
    #     await tweetBot.send('👎')
    # else:
    #     await tweetBot.send('👍')


bot.run(TOKEN)