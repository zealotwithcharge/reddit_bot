from re import sub
import praw
import time
from textblob import TextBlob
import praw.exceptions
from praw.reddit import Comment
import prawcore.exceptions

reddit = praw.Reddit('bot7', user_agent='cs40')
subreddit = reddit.subreddit("BotTown")
botname = 'bot7'
voted = 0
def vote(submission):
    global voted
    if submission.selftext != '':
        text = TextBlob(submission.selftext)
    else:
        text = TextBlob(submission.title)
    submission = reddit.submission(id = submission.id)
    if text.sentiment.polarity >= 0:
        submission.downvote()
        print("downvoted! sub")
        
    else:
        
        submission.upvote()
        print("upvoted! sub")
    print(submission.permalink)
    voted += 1
    print('subs: ',voted)

submissions = list(subreddit.top('all',limit = None))
print('subs: ',len(submissions))
for submission in submissions:
    
    if "trump" in submission.selftext.lower() or "trump" in submission.title.lower():
        try:    
            vote(submission)
        except praw.exceptions.RedditAPIException as err:
                for subexception in err.items:
                    if 'looks like you' in subexception.error_message.lower():
                        important = subexception.error_message.split('\"')[1]
                        minutes = int(''.join(filter(str.isdigit,important)))
                        print(botname+'sleeping!')
                        time.sleep(minutes*60)
                    else:
                        print(botname+"error!"+subexception.error_message)  
        except prawcore.exceptions.TooManyRequests as err:
            print("errororororor")
            print(err)
            if 'please wait at least' in err.message:
                    important = err.message.split('\"')[1]
                    minutes = int(''.join(filter(str.isdigit,important)))
                    print(botname+'sleeping!')
                    time.sleep(minutes)
            else:
                print(botname+"error!"+err.message)  

for submission in subreddit.stream.submissions():
    if "trump" in submission.selftext.lower() or "trump" in submission.title.lower():
        try:
            vote(submission)
        except praw.exceptions.RedditAPIException as err:
                for subexception in err.items:
                    if 'looks like you' in subexception.error_message.lower():
                        important = subexception.error_message.split('\"')[1]
                        minutes = int(''.join(filter(str.isdigit,important)))
                        print(botname+'sleeping!')
                        time.sleep(minutes*60)
                    else:
                        print(botname+"error!"+subexception.error_message)  
        except prawcore.exceptions.TooManyRequests as err:
            print("errororororor")
            print(err)
            if 'please wait at least' in err.message:
                    important = err.message.split('\"')[1]
                    minutes = int(''.join(filter(str.isdigit,important)))
                    print(botname+'sleeping!')
                    time.sleep(minutes)
            else:
                print(botname+"error!"+err.message)  