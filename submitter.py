import praw
import argparse
import random
import time
import praw.exceptions
import copy
import prawcore.exceptions
parser = argparse.ArgumentParser()
parser.add_argument('botname')
args = parser.parse_args()

reddit = praw.Reddit(args.botname,user_agent = 'cs40')



our_subreddit = reddit.subreddit("BotTown")
posts = list(reddit.subreddit('Liberal').top("all"))
posts += list(reddit.subreddit('politics').top("all"))
posts += list(reddit.subreddit('Libertarian').top("all"))

while len(posts)>0:
    try:
            
            sub = random.choice(posts)
            if sub.is_self:
                our_subreddit.submit(sub.title,selftext = sub.selftext)
            else:
                our_subreddit.submit(sub.url)
                print('working')
            posts.remove(sub)

    except praw.exceptions.RedditAPIException as err:
        for subexception in err.items:
            if 'looks like you' in subexception.error_message.lower():
                important = subexception.error_message.split('\"')[1]
                minutes = int(''.join(filter(str.isdigit,important)))
                print(args.botname+'sleeping!')
                time.sleep(minutes*60)
            else:
                print(args.botname+"error!"+subexception.error_message)  
    except prawcore.exceptions.TooManyRequests as err:
        print("errororororor")
        print(err)
        if 'please wait at least' in err.message:
                important = err.message.split('\"')[1]
                minutes = int(''.join(filter(str.isdigit,important)))
                print(args.botname+'sleeping!')
                time.sleep(minutes)
        else:
            print(args.botname+"error!"+err.message)  
        