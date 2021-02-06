import os, asyncio
import config, mongo, tweetClient
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.command(name='plznuke')
async def validateTweets(ctx):
    mongo.nukeDB()
    await bot.get_channel(806923512270422016).send("reset db done")

@bot.command(name='tweet')
async def twitterPoll(ctx):
    """
    Creates a tweet object in the mongo database.
    Logs the message ID for future evaluation and posts to twitter.
    """

    # Define contents of the tweet that will be voted
    tweetText = ctx.message.content[7:]
    messageObject = ctx.message

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

    print(" ~@ Sending Voting Message")
    poll = await tweetBot.send(response)
    print(poll)

    print(" ~ Adding Reactions")
    emojis = ["👍", "👎"]

    for emoji in emojis:
        await poll.add_reaction(emoji)

    # Format data and upload to database
    tweetObject = mongo.newTweetObject(tweetText, messageObject, poll)
    mongo.submit_tweet(tweetObject)
    
    # ## Now there must be a vote emoticon set for easy votes
    # print(" ~ About to sleep and check reactions")
    # await asyncio.sleep(2)
    # vote_results = await tweetBot.fetch_message(poll.id)
    # print(f"{vote_results=}")
    # print(f"{vote_results.reactions=}")
    # print(f"{vote_results.reactions=}")

    # This sends the tweet through tweepy.
    #print(f" ~ Sending {tweetText=}")
    # tweetClient.tweet_send(tweetText)

@bot.command(name='validate')
async def validateTweets(ctx):
    """
    Async conjob, called on demand, that queries all tweets logged on the database.
    Filters tweets that are 'pending', and calculates scores.
    Approved tweets will trigger a tweet and update db function.
    """

    print(" ~ Sending Verification Message")
    tweetBot = bot.get_channel(806923512270422016)   #TODO: change the channel to be dynamic
    await tweetBot.send(f"""Alright . . . Checking the tweets proposed. Currently received {mongo.count_submissions()} tweets total""")

    for tweet in mongo.db.tweets.find():
        print(f"{tweet=}")
        print(f"{tweet['_id']=}")
        print(f"{type(tweet['_id'])=}")
        print(f"{tweet['reactions']}")

        newstatus = await tweetBot.fetch_message(int(tweet['poll']))            
        print(newstatus.reactions)

    def update_reactions(_id):
        """
        Receive original message _id
        updates the reactions re
        """    

        # Original message ID
        myquery= {"_id" : _id}

        # Poll message
        newvalues = {"poll_id":poll_id}
        pymongo.update_one(myquery, newvalues)

        

bot.run(TOKEN)