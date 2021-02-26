# Boteki
Simple versatile Discord bot to automate dOrg tweets through emoji votes.
You can deploy on your own cloud using docker.

![images/sample.png]

# Get started


1. Get API keys for Twitter
1. Set up bot account and add to your server
1. Create MongoAtlas database and configure connections

1. Clone the repo 
1. Set your `.env` file with these variables, 
```
DISCORD_TOKEN=yourdiscordtoken
DISCORD_GUILD=name of your server

TWITTER_SECRET=twitterapi
TWITTER_CLIENT=twitterkey

ATLAS=database
MONGO_DB_NAME=collection  
```
1. Deploy the Docker container with the command `docker build -t boteki .` and `docker run boteki`, or  this will run the bot with `python3 bot.py` and install necessary dependencies.

Once the bot is running you can call the following commands:
 - `!tweet` : Set up an emoji vote poll of the tweett and log it in a database
 - `!validate`: looks up all the tweets logged on the database, updates the score if possible, and tweets or schedules the tweet.
 - `!plznuke`: resets the existing database. use this if the bot breaks during development. Remove this function from the bot before bringing to production to avoid trouble.
  
## Variables
Set up variables on the config.py file, also create a .env with discord, modgo atlas and twitter keys.

## Functionalities:

- [x] Connect Discord bot through official API.
- [x] Receinve `!tweet` specific commands on Discord #Twitter channel.
- [x] Log tweets to a MongoAtlas cloud server. 
- [x] Query database for received tweets.
- [x] Created basic `mongo.py` to interact with the cloud server
- [x] Create a function to nuke the database if needed `mogo.nukeDB()`
- [x] Update data on tweets with the `!validate` command
- [x] Connect to Twitter through Tweepy
- [x] Add tweets to queue when `!validate` is called () 
- [x] Confirm tweet length and other error handling
- [x] Make this reproducible witha docker container

**Next steps:**
- [ ] Create a queue of tweets to post
- [ ] create a `!preview`command to show the queued tweets before sending them
- [ ] Try to link to hubspot profiles and ethereum addresses
- [ ] Establish versions to the Docker requirements to reproduce correct builds
- [ ] Bash script that builds the docker image and runs it