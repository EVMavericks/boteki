# boteki

Simple Discord bot to automate dOrg tweets through emoji votes.


## Variables
```
approval_window=7 #days
required_votes=3 #people needed to vote in favor for tweeting

```
## Process:

1. Connect Discord bot through official API.
1. Connect to Twitter through Tweepy

1. Query specific Discord #Twitter channel message history .
- User handle
- Tweet text (Emoji compliant)
- Message permalink / _id
- Confirm tweet length.

1. AUTO-Tweet
 - Cronjob to check backlog of tweets
 - If tweet _id has enough votes and has not been tweeted,