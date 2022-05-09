
from dotenv import load_dotenv
import os
import mongo
import asyncio
import time
import requests
from tweepy import OAuth1UserHandler, API
load_dotenv()

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')

Auth = OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET,  callback="oob") #oob is needed for pin authorization

def tweet_send(msg, guild):
    
    Auth.set_access_token(*mongo.get_tokens(guild))
    TwitterBot = API(Auth)

    return TwitterBot.update_status(msg)

def get_authorization_url():
    return Auth.get_authorization_url()

def get_token(pin):
    access_token, access_token_secret = Auth.get_access_token(pin)

    Auth.set_access_token(access_token, access_token_secret)
    api = API(Auth)
    
    user = api.verify_credentials()
    if(user.name is not None or user.name != ""):
        return True, user.name, Auth.access_token, Auth.access_token_secret

    return False