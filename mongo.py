# %% 
from pymongo import MongoClient, ReturnDocument 

from dotenv import load_dotenv
import os
load_dotenv()

ATLAS_CONNECTIONSTRING = os.getenv('ATLAS_CONNECTIONSTRING')
def connect():
    print("connecting")
    client = MongoClient(ATLAS_CONNECTIONSTRING)
    db = client.test
    print("Connected")
    return db

db = connect()

#%%

def newTweetObject(tweetText, messageObject, poll):

    # Get Author
    # Get Tweet Text
    # Get Score

    tweetObject =  {
        '_id': int(messageObject.id),
        'channel': messageObject.channel.id,
        'poll': int(poll.id),
        'author': f'{messageObject.author}',
        'content': f'{tweetText}',
        'reactions': f'{messageObject.reactions}',
        'created_at': f'{messageObject.created_at}',
        'status': 'pending',
    }
    return tweetObject

def submit_tweet(tweetObject):
    post_id = db.tweets.insert_one(tweetObject).inserted_id
    print(post_id)    
    return post_id

def confirm_tweet(_id, response):
    """
    Update a object in the database after tweeting it
    """
    new_object = db.tweets.find_one_and_update({'_id': _id},
                                { '$set': { "status" : "tweeted",
                                            "response": response} },  
                                #TODO: This database should keep the URL of the tweet sent 
                                )
    return new_object

# %%
def count_submissions():
    return db.tweets.count_documents({})
# %%
def nukeDB():
    cursor = db.tweets.find({})

    for element in cursor:
        print(element)
        db.tweets.delete_many( {'_id': element['_id']} )

    print(' ~ Deleted all tweets on database')