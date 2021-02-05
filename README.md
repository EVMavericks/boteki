# boteki

Simple Discord bot to automate dOrg tweets through emoji votes.


## Variables
Set up variables on the config.py file, also create a .env with discord, modgo atlas and twitter keys.

## Process:

- [x] Connect Discord bot through official API.
- [x] Receinve `!tweet` specific commands on Discord #Twitter channel.
- [x] Log tweets to a MongoAtlas cloud server. 
- [x] Query database for received tweets.
- [ ] Update data on tweets with the `!validate` command


**Next step:**
- [ ] Connect to Twitter through Tweepy
- [ ] Create a queue of tweets to post
- [ ] Add tweets to queue when `!validate` is called
- [ ] Try to link to hubspot profiles and ethereum addresses
- [ ] Confirm tweet length and other error handling

1. AUTO-Tweet
 - Cronjob to check backlog of tweets
 - If tweet _id has enough votes and has not been tweeted,