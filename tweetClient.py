from dotenv import load_dotenv
import os
import mongo
import asyncio
import time
import requests
from tweepy import OAuthHandler, API
load_dotenv()

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')

Auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
Auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
TwitterBot = API(Auth)

def tweet_send(msg):
    return TwitterBot.update_status(msg)


def tweet_format(json):
    msg = f"""Ethereum Gas Monitor 👽 
        [Block No. {json["blockNum"]}]

        Slow: {int(json["safeLow"])/10} gwei
        Average: {int(json["average"])/10} gwei
        Fast: {int(json["fast"])/10} gwei
        
        $ETH #EthereumMainnet"""

    return msg

async def gas_price_delayed(sleep):
    print("Sleeping for {0} seconds...".format(sleep))
    await asyncio.sleep(sleep)
    sleep = sleep*2
    gas_price(sleep)

def gas_price(sleep=15):
    try:
        url = "https://ethgasstation.info/api/ethgasAPI.json"
        response = requests.get(url, timeout=3)
        data = response.json()
        return data
    except Exception as e:
        print(e)
        gas_price_delayed(sleep)

def unix_now():
    return round(time.time())

# class Bot:
#     def __init__(self):
#         self.last = 0
#         self.wait = 5*60 # Check every 5 minutes
#         self.threshold = 50 # Gwei threshold
#         self.delay = 60*60  # Use 24*60*60 to tweet only every 24 hours

#     def check(self):
#         json = gas_price()
#         gwei = int(json["average"])/10
#         if gwei < self.threshold:
#             if unix_now()-self.last >= self.delay:
#                 msg = tweet_format(json)
#                 print(unix_now())
#                 print(msg)
#                 tweet_send(msg)
#                 self.last = unix_now()

#     async def start(self):
#         while True:
#             self.check()
#             await asyncio.sleep(self.wait)

# b = Bot()
# b.start()
