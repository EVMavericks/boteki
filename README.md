# boteki

Simple Discord bot to automate dOrg tweets through emoji votes.


## Variables
Set up variables on the config.py file

## Process:

- [x]. Connect Discord bot through official API.
- [x] Connect to Twitter through Tweepy

- [x] Receinve `!tweet` specific commands on Discord #Twitter channel.
- [x] Record votes after X time
  
Next step:

Log entries

```
 tweet: {
     'author': 
        builder: {
            'discord_user_id':'',
            'eth_address':'',
         },
     'content':'',
     'discord_message_id':'',
     'score': ,
     'result': ['pending', 'passed', 'rejected']
 }
```

- [ ] User handle
- Tweet text (Emoji compliant)
- Message permalink / _id
- Confirm tweet length.

1. AUTO-Tweet
 - Cronjob to check backlog of tweets
 - If tweet _id has enough votes and has not been tweeted,