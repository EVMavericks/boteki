# boteki
Discord bot to automate dOrg tweets through emoji votes

Process:

1. QUERY DISCORD TWITTER CHANNEL 
- Connect with Boteki account.

2. QUERY ALL MESSAGES IN LAST WEEK
- User handle
- Tweet text (Emoji compliant)
- Message permalink / _id
- Confirm tweet length.

3. AUTO-Tweet
 - Cronjob to check backlog of tweets
 - If tweet _id has enough votes and has not been tweeted,