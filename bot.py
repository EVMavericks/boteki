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
    :fire: **Vote Started**: react with :+1:  or :-1: to publish or skip the tweet.
    Tweets with a net socre of {config.required_score} points will be published when the `!validate` command is called.
    ```markdown
    {tweetText}
    ```
    """

    print(">> Incomming command: ", ctx.message.content)
    print(" ~ Setting up discord vote.")
    print(messageObject)
    tweetBot = bot.get_channel(messageObject.channel.id)  

    # Verify tweet integrity and return error message if needed
    if len(tweetText) >=240:
        error = await tweetBot.send('Your tweet exceeds the maximum character length. Try again. Max 240 characters.')
        return error

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

        if net_score >= config.required_score: 
            
            # This sends the tweet through tweepy.
            try:
                await tweetBot.send(f"This tweet has a `net_score` of {net_score}, which is compliant with the minimum publish threshold of {config.required_score} points in favor.")
                await tweetBot.send(f"```\n{tweet['content']}\n```")
                response = tweetClient.tweet_send(tweet['content'])._json
            except Exception as e:
                await tweetBot.send(f"error occurred when sending tweet:\n{e}")

            # TODO: change mongo document to include the new tweet's URL and also include the new net_score 
            print(f"{response['id']=}")
            
            mongo.confirm_tweet(tweet['_id'], response)
            await tweetBot.send(f"Tweet above has been sent (https://twitter.com/twitter/statuses/{response['id']}) and database object updated.")

        else: print(f" ~ Tweet skipped with a {net_score=}")

    await tweetBot.send(f"done validating :)")
        
bot.run(TOKEN)