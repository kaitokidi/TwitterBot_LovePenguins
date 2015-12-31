#!/usr/bin/python
from twython import Twython
import json

frases = ["I love Penguins!", "Penguins are awesome!", "I like penguins : )", "Penguins are the best", "Penguins FTW", "Penguins <3", "Oh, Penguins!", "so you are thinking about penguins too ^^", "I love Penguins!"]
def pick():
    n = random().randint(0, len(frases))
    return frases[n]
def auth():
    with open("access.json", 'r') as f:
        db = json.load(f)
    return Twython(db["API_Key"], db["API_Secret"], db["Access_Token"],db["Access_Token_Secret"])

def load():
    with open("queue.json",'r') as f:
        queue = json.load(f)
    with open("info.json", 'r') as fi:
        info = json.load(fi)
    return queue, info

def respond(twitter, top_tweet):
    name = top_tweet["user"]["screen_name"]
    if name != "Penguin___Lover":
        twitter.update_status(status="@%s, I love Penguins!" %(name)+pick(), in_reply_to_status_id=top_tweet["id"]) 
    
def dump(queue, info):
    with open("queue.json", 'w') as f:
        json.dump(queue, f)
    with open("info.json", 'w') as fi:
        json.dump(info, fi)
    
def main():
    twitter = auth()
    queue, info = load()
    tweets = twitter.search(q="penguins", result_type="recent", since_id=info["sinceid"], count='100')
    info["sinceid"] = tweets["search_metadata"]["max_id"]
    triggers = ("Penguins","penguins","Penguin","penguin")
    to_add = [tweet for tweet in tweets["statuses"] if not tweet["retweeted"] and not tweet.has_key("retweeted_status")]

    #to_add = [tweet for tweet in to_add if (tweet["text"].__contains__(triggers[0]) or tweet["text"].__contains__(triggers[1]) or tweet["text"].__contains__(triggers[2]) or tweet["text"].__contains__(triggers[3]))]

    #TOTEST

    totaltext = tweet["text"]
    print totaltext

    tt = [x for x in totaltext.split() if x[0] != '@']
    #print tt
    t = ' '.join(tt)
    #print t
    #    [y for y in x if y != 2]
    to_add = [tweet for tweet in to_add if ( (triggers[0] in t) or (triggers[1] in t) or (triggers[2] in t) or (triggers[3] in t) )]
    #TOTEST


    queue = list(queue) + to_add
    mx = max(len(to_add), 20)
    if len(queue) > mx:
        queue = queue[-mx:]
    if len(queue) > 0:
        respond(twitter, queue.pop())
    dump(queue,info)
    
#it would have to run on cron every n minutes, it would be nice not to get banned for spam T.T
if __name__ == "__main__":
    main()
