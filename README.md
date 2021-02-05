# Boteki
Simple versatile Discord bot to automate dOrg tweets through emoji votes.


# Get started

1. Python 3.8 or higher is needed `python3 --version`
1. clone the repo 
1. set your `.env` file with these variables
```
DISCORD_TOKEN=yourdiscordtoken
DISCORD_GUILD=name of your server

TWITTER_SECRET=twitterapi
TWITTER_CLIENT=twitterkey

ATLAS=database
MONGO_DB_NAME=collection  
```
2. run the bot with `python3 bot.py` and install necessary dependencies.

Once the bot is running you can call the following commands:
 - `!tweet` : Set up an emoji vote poll of the tweett and log it in a database
 - `!validate` looks up all the tweets logged on the database, updates the score if possible, and tweets or schedules the tweet.

## Variables
Set up variables on the config.py file, also create a .env with discord, modgo atlas and twitter keys.

## Process:

- [x] Connect Discord bot through official API.
- [x] Receinve `!tweet` specific commands on Discord #Twitter channel.
- [x] Log tweets to a MongoAtlas cloud server. 
- [x] Query database for received tweets.
- [ ] Created basic `mongo.py` to interact with the cloud server
- [x] Create a function to nuke the database if needed `mogo.nukeDB()`
- [ ] Update data on tweets with the `!validate` command


**Next step:**
- [ ] Connect to Twitter through Tweepy
- [ ] Create a queue of tweets to post
- [ ] Add tweets to queue when `!validate` is called
- [ ] Try to link to hubspot profiles and ethereum addresses
- [ ] Confirm tweet length and other error handling
- [ ] Make this reproducible witha docker container

1. AUTO-Tweet
 - Cronjob to check backlog of tweets
 - If tweet _id has enough votes and has not been tweeted,