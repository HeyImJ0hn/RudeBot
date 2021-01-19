import tweepy
import time
import random

print('Bot Starting...')

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def get_insults(file_name):
    f = open(file_name, 'r')
    insults = f.read().split('\n')
    return insults

def pick_insult():
    insults = get_insults('insults.txt')
    insult = random.choice(insults)
    return insult

def reply():
    insult = pick_insult()

    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id)

    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        print('Replying to tweet - ' + str(mention.id) + ' by @' + mention.user.screen_name)
        api.update_status('@' + mention.user.screen_name + ' ' + insult, in_reply_to_status_id = mention.id)
        print('Replied - ' + '@' + mention.user.screen_name + ' ' + insult)

print('Bot Started.')

while True:
    print('Waiting for Tweets...')
    reply()
    time.sleep(10)
    
