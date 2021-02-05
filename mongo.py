# %% 
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

ATLAS = os.getenv('ATLAS')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')

def connect():
    print("connecting")
    client = MongoClient(f"mongodb+srv://rihp:{ATLAS}@messenger-api.lq6n5.mongodb.net/{MONGO_DB_NAME}?retryWrites=true&w=majority")
    db = client.test
    print("Connected")
    return db

db = connect()

#%%

tweet =  {
     'author':'discord_user_id',
     'content':'',
     'discord_message_id':'',
     'score': 0,
     'result': ['pending', 'passed', 'rejected']
 }

def submit_tweet(tweet):
    db.tw
    post_id = db.tweets.insert_one(tweet).inserted_id
    print(post_id)    
    return post_id

submit_tweet(tweet)
# %%
db.list_collection_names()

# %%

db.tweets.find_one()

# %%
