import praw
import time
import praw.exceptions
from praw.reddit import Comment
import prawcore.exceptions
from textblob import TextBlob

reddit = praw.Reddit('bot8', user_agent='cs40')
subreddit = reddit.subreddit("BotTown")
botname = 'bot8'
voted = 0
def vote(comment):
    global voted
    text = TextBlob(comment.body)
    comment = reddit.comment(id = comment.id)
    if text.sentiment.polarity >= 0:
        comment.downvote()
        print("downvoted!")
        
    else:
        
        comment.upvote()
        print("upvoted!")
    print(comment.permalink)
    voted += 1
    print('comments: ',voted)

submissions = list(subreddit.top('all',limit = None))
for submission in submissions:
    
    submission.comments.replace_more(limit=None)

    for comment in submission.comments.list():
        if "trump" in comment.body.lower():
            try:
                
                vote(comment)
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



for comment in subreddit.stream.comments():
    if "trump" in comment.body.lower():
        try:
            vote(comment)
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

