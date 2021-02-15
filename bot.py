import os, asyncio
import config, mongo, tweetClient, democratic
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.command(name='plznuke')
async def validateTweets(ctx):
    mongo.nukeDB()
    await  bot.get_channel(ctx.message.channel.id).send("reset db done")

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
    print(messageObject)
    tweetBot = bot.get_channel(messageObject.channel.id)   #TODO: change the channel to be dynamic
    # tweetBot = bot.get_channel(806923512270422016)   

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

    
@bot.command(name='validate')
async def validateTweets(ctx):
    """
    Async function, called on demand. 
    1. Queries all tweets logged on the database.
    2. Filters tweets that are 'pending', and calculates scores.
    Approved tweets will trigger a tweet and update db function.
    """

    print(" ~ Sending Verification Message")
    messageObject = ctx.message

    tweetBot = bot.get_channel(messageObject.channel.id)   #this line makes the command work across channels
    await tweetBot.send(f"""Alright . . . Checking the tweets proposed. Currently received {mongo.count_submissions()} tweets total""")

    for tweet in mongo.db.tweets.find({'status':'pending'}):
        print(f"{tweet=}")
        newstatus = await bot.get_channel(tweet['channel']).fetch_message(int(tweet['poll']))            
        results = democratic.count_votes(f"{newstatus.reactions}")
        net_score = democratic.net_score(results)

        # TODO : Update this function to also check if the tweet is within the correct timeframe (
        # Consider using the datetime module to turn "2021-02-10 21:19:02.795000" strings into timestamp
        print(type(tweet['created_at']))
        tweet['created_at']


        if net_score >= config.required_score: 
            
            await tweetBot.send(f"This tweet has a `net_score` of {net_score}, which is compliant with the minimum publish threshold of {config.required_score} points in favor.")
            await tweetBot.send(f"```\n{tweet['content']}\n```")
            #await tweetBot.send(f"At this point, Boteki publishes the tweet `{tweet['_id']=}` and with the content string:\n```{tweet['content']=}```")
       
            # This sends the tweet through tweepy.
            sent_tweet_url = tweetClient.tweet_send(tweet['content'])
        
            # TODO: change mongo document to {"status":"tweeted"}
            mongo.confirm_tweet(tweet['_id'], sent_tweet_url)
            await tweetBot.send(f"Tweet above has been sent and database object updated.")

        else: print(f"{net_score=}")

        # Turn the net score into a publish or pass action to twitter API.
        # Also, the mongo tweet status must be updated to 'published'
    await tweetBot.send(f"done validating :)")


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