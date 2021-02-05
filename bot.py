import os, asyncio
import config, mongo
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='tweet')
async def twitterPoll(ctx):
    """
    Creates a tweet object in the mongo database.
    Logs the message ID for future evaluation and posts to twitter.
    """

    # Define contents of the tweet that will be voted
    tweetText = ctx.message.content[7:]
    messageObject = ctx.message

    # Format data and upload to database
    tweetObject = mongo.newTweetObject(tweetText, messageObject)
    mongo.submit_tweet(tweetObject)

    # Bot Responds through Discord and starts the vote:
    response = f"""\n
    :fire: **Vote Started**
    React with :+1:  or :-1: to publish or skip the tweet.
    Tweets with a net socre of {config.required_score} points within {config.approval_window} days will be published automatically.
    ```markdown
    {tweetText}
    ```
    """

    print(">> Incomming command: ", ctx.message.content)
    print(" ~ Setting up discord vote.")
    tweetBot = bot.get_channel(806923512270422016)   #TODO: change the channel to be dynamic

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
    Async conjob, called on demand, that queries all tweets logged on the database.
    Filters tweets that are 'pending', and calculates scores.
    Approved tweets will trigger a tweet and update db function.
    """

    print(" ~ Sending Verification Message")
    tweetBot = bot.get_channel(806923512270422016)   #TODO: change the channel to be dynamic
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