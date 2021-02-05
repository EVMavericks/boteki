import asyncio
import os
import datetime
import discord
import tweepy
import config
from dotenv import load_dotenv
import mongo

from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='tweet')
async def twitterPoll(ctx):
    # Define tweet contents
    tweetText = ctx.message.content[7:]
    messageObject = ctx.message

    # What will the Bot answer through Discord:
    response = f"""\n
    :fire: **Vote Started**
    React with :+1:  or :-1: to publish or skip the tweet.
    Tweets with a net socre of {config.required_score} points within {config.approval_window} days will be published automatically.
    ```markdown
    {tweetText}
    ```
    """

    # Format data and upload to database
    tweetObject = mongo.newTweetObject(tweetText, messageObject)
    mongo.submit_tweet(tweetObject)

    print(">> Incomming command: ", ctx.message.content)
    print(" ~ Setting up discord vote.")
    tweetBot = bot.get_channel(806923512270422016)

    print(" ~ Sending Voting Message")
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

@bot.command(name='validate')
async def validateTweets(ctx):
    """
    Async conjob that queries all tweets logged on the database.
    Filters tweets that are 'pending', and calculates scores.
    Approved tweets will trigger a tweet and update db function.
    """

    print(" ~ Sending Verification Message")
    tweetBot = bot.get_channel(806923512270422016)
    await tweetBot.send("""Alright . . . Checking the tweets proposed. Currently received ## tweets total""")

    for tweet in mongo.db.tweets.find():
        print(f"{tweet=}")
        print(f"{tweet['_id']}")
        await tweetBot.fetch_message(tweet['_id'])            

    # def check(reaction, user):
    #     return user == poll.author and str(reaction.emoji) == '👍'

    # try:
    #     reaction, user = await tweetBot.wait_for('reaction_add', timeout=5.0, check=check)
    # except asyncio.TimeoutError:
    #     await tweetBot.send('👎')
    # else:
    #     await tweetBot.send('👍')

bot.run(TOKEN)