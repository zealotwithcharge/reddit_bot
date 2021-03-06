import praw
import praw.exceptions
import random
import datetime
from aitextgen import aitextgen
import argparse
import time

import prawcore.exceptions
import tensorflow as tf
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer


# parser = argparse.ArgumentParser()
# parser.add_argument('botname')
# args = parser.parse_args()

botname = 'bot2'
# Without any parameters, aitextgen() will download, cache, and load the 124M GPT-2 "small" model
tester = False


tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# add the EOS token as PAD token to avoid warnings
model = TFGPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)
# Without any parameters, aitextgen() will download, cache, and load the 124M GPT-2 "small" model
ai = aitextgen()



# FIXME:
# copy your generate_comment functions from the madlibs assignment here
def generate_comment(key_word):

    tf.random.set_seed(0)

# set top_k = 50 and set top_p = 0.95 and num_return_sequences = 3
    input_ids = tokenizer.encode(key_word, return_tensors='tf')
    if len(key_word)>100:
        output = model.generate(
        input_ids,
        do_sample=True, 
        max_length=len(key_word)*2, 
        top_k=50, 
        top_p=0.95,
        )
        return tokenizer.decode(output[0], skip_special_tokens=True)[len(key_word):]
    else:
        output = model.generate(
        input_ids,
        do_sample=True, 
        max_length=150, 
        top_k=50, 
        top_p=0.95, 
        )
        return tokenizer.decode(output[0], skip_special_tokens=True)[len(key_word):]
# connect to reddit 
reddit = praw.Reddit(botname,user_agent = 'cs40')
my_bot_name = reddit.user.me().name
# connect to the debate thread
reddit_debate_url = 'https://www.reddit.com/r/BotTown2/comments/r0yi9l/main_discussion_thread/'
# 'https://old.reddit.com/r/BotTown/comments/qqmr8l/main_discussion_thread/'
submission = reddit.submission(url=reddit_debate_url)

redditor = reddit.redditor(name = my_bot_name)
my_bots_comments = list(redditor.comments.new(limit=None))

my_top_level_comments = []
my_replies = []
for comment in my_bots_comments:
    try:
        if type(comment.parent()) is praw.models.Submission:
            my_top_level_comments.append(comment)
        else:
            my_replies.append(comment)
    except AttributeError:
        pass

my_parents = []
for comment in my_replies:
    my_parents.append(comment.parent().id)
# each iteration of this loop will post a single comment;
# since this loop runs forever, your bot will continue posting comments forever;
# (this is what makes it a deamon);
# recall that you can press CTRL-C in the terminal to stop your bot
#
# HINT:
# while you are writing and debugging your code, 
# you probably don't want it to run in an infinite loop;
# you can change this while loop to an if statement to make the code run only once
while True:
    try:
        
    # printing the current time will help make the output messages more informative
    # since things on reddit vary with time
        print()
        print(botname+": "+my_bot_name)
        print('new iteration at:',datetime.datetime.now())
        print('submission.title=',submission.title)
        print('submission.url=',submission.url)

        # FIXME (task 0): get a list of all of the comments in the submission
        # HINT: this requires using the .list() and the .replace_more() functions
        all_comments = []
        if not tester:
            submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            all_comments.append(comment)
        # HINT: 
        # we need to make sure that our code is working correctly,
        # and you should not move on from one task to the next until you are 100% sure that 
        # the previous task is working;
        # in general, the way to check if a task is working is to print out information 
        # about the results of that task, 
        # and manually inspect that information to ensure it is correct; 
        # in this specific case, you should check the length of the all_comments variable,
        # and manually ensure that the printed length is the same as the length displayed on reddit;
        # if it's not, then there are some comments that you are not correctly identifying,
        # and you need to figure out which comments those are and how to include them.
        print('len(all_comments)=',len(all_comments))

        # FIXME (task 1): filter all_comments to remove comments that were generated by your bot
        # HINT: 
        # use a for loop to loop over each comment in all_comments,
        # and an if statement to check whether the comment is authored by you or not
        not_my_comments = []
        my_comments = []
        if len(all_comments) >0:
            for i,comment in enumerate(all_comments):
                if tester and type(comment) == praw.models.MoreComments:
                    continue
                if comment.author != None and comment.author.name != my_bot_name:
                    not_my_comments.append(comment)
                elif comment.author!= None and comment.author.name == my_bot_name:
                    my_comments.append(comment)
                else:
                    not_my_comments.append(comment)

        

        # HINT:
        # checking if this code is working is a bit more complicated than in the previous tasks;
        # reddit does not directly provide the number of comments in a submission
        # that were not gerenated by your bot,
        # but you can still check this number manually by subtracting the number
        # of comments you know you've posted from the number above;
        # you can use comments that you post manually while logged into your bot to know 
        # how many comments there should be. 
        print('len(not_my_comments)=',len(not_my_comments))
        print('len(my_comments)=',len(my_comments))

        # if the length of your all_comments and not_my_comments lists are the same,
        # then that means you have not posted any comments in the current submission;
        # (your bot may have posted comments in other submissions);
        # your bot will behave differently depending on whether it's posted a comment or not
        has_not_commented = len(not_my_comments) == len(all_comments)

        if has_not_commented:
            # FIXME (task 2)
            # if you have not made any comment in the thread, then post a top level comment
            #
            # HINT:
            # use the generate_comment() function to create the text,
            # and the .reply() function to post it to reddit;
            # a top level comment is created when you reply to a post instead of a message
            if submission.selftext != '':
                if tester:
                    print(submission.selftext)
                    text = generate_comment(submission.selftext)
                    print('this is unshortend from title: \n'+text)
                    print("this is generated: \n" + text[len(submission.selftext):])
                else:
                    submission.reply(generate_comment(submission.selftext))
            else:
                    if tester:
                        print(submission.title)
                        text = generate_comment(submission.title)
                        print('this is unshortend from title: \n'+text)
                        print("this is generated from title: \n" +text[len(submission.title):])
                    else:
                        submission.reply(generate_comment(submission.title))
                
            print("commented!")
        else:
            # FIXME (task 3): filter the not_my_comments list to also remove comments that 
            # you've already replied to
            # HINT:
            # there are many ways to accomplish this, but my solution uses two nested for loops
            # the outer for loop loops over not_my_comments,
            # and the inner for loop loops over all the replies of the current comment from the outer loop,
            # and then an if statement checks whether the comment is authored by you or not
            comments_without_replies = []
            comments_with_replies = []
            comments_without_replies2 = []
            parents = []
            for comment in my_comments:
                parents.append(comment.parent().id)
                
            
            for i,comment in enumerate(not_my_comments):
                flag = True
                for reply in comment.replies:
                    if tester and type(reply) == praw.models.MoreComments:
                        continue
                    if reply.author != None and reply.author.name == my_bot_name:
                        flag = False
                if flag:
                    comments_without_replies.append(comment)
                else:
                    comments_with_replies.append(comment)




            for comment in comments_without_replies:
                try:
                    if comment.id in parents or comment.id in my_parents or comment.author.name == my_bot_name:
                        pass
                    else:
                        comments_without_replies2.append(comment)
                except AttributeError:
                    try:
                        checker = comment.author.name == my_bot_name
                    except AttributeError:
                        comments_without_replies2.append(comment)
            
            
            # HINT:
            # this is the most difficult of the tasks,
            # and so you will have to be careful to check that this code is in fact working correctly
            print('len(comments_with_replies)=',len(comments_with_replies))
            print('len(comments_without_replies)=',len(comments_without_replies))
            print('len(comments_without_replies2)=',len(comments_without_replies2))
            
            # FIXME (task 4): randomly select a comment from the comments_without_replies list,
            # and reply to that comment
            #
            # HINT:
            # use the generate_comment() function to create the text,
            # and the .reply() function to post it to reddit;
            # these will not be top-level comments;
            # so they will not be replies to a post but replies to a message

            #### Random choice of comment code
            # if len(comments_without_replies)>0:
            #     target_comment = random.choice(comments_without_replies)
            
            high = 0
            target_comment = None
            for comment in comments_without_replies2:
                if comment.score > high:
                    high = comment.score
                    target_comment = comment
             
                    
            
            if tester:
                print(target_comment.body)
                print()
                text = generate_comment(target_comment.body)
                print('This is the generation unshortened: '+text+'\n')
                print('This is the generation: '+text[len(target_comment.body):])
            else:
                if target_comment != None:
                    for reply in target_comment.replies:
                        if reply.author != None and reply.author.name == my_bot_name:
                            print('AAAAAAAAAAAAAAAAAAAAAAAAAAAA')
                            break
                    target_comment.reply(generate_comment(target_comment.body))
                    my_parents.append(target_comment.id)
                    print("commented2")
            
        # FIXME (task 5): select a new submission for the next iteration;
        # your newly selected submission should have a 50% chance of being the original submission
        # (url in the reddit_debate_url variable)
        # and a 50% chance of being randomly selected from the top submissions to the csci040 subreddit for the past month
        # HINT: 
        # use random.random() for the 50% chance,
        # if the result is less than 0.5,
        # then create a submission just like is done at the top of this page;
        # otherwise, create a subreddit instance for the csci40 subreddit,
        # use the .top() command with appropriate parameters to get the list of all submissions,
        # then use random.choice to select one of the submissions
        
        hots = list(reddit.subreddit("BotTown2").hot(limit=5))
        
        submission = reddit.submission(id = random.choice(hots).id)



        time.sleep(10)
    except praw.exceptions.RedditAPIException as err:
        print("errororororor")
        print(err)
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
    except IndexError:
        print("nothing to reply to!")
        hots = list(reddit.subreddit("BotTown2").hot(limit=5))
        
        submission = reddit.submission(id = random.choice(hots).id)

        # submission = reddit.submission(id = submission.id)

        # hots = list(reddit.subreddit("BotTown").hot(limit=7))
        # removed_hots = []
        # for hot in hots:
        #     if 'Main Discussion' not in str(hot.title) and 'Practice posting' not in str(hot.title):
        #         removed_hots.append(hot)
        

        # submission = random.choice(removed_hots)

