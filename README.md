# reddit_bot
This is a repository with code for bots that serve various functions. \
`bot.py` is a comment generator which uses a more advanced GPT-2 base text generation algorithm.\
`bot_lite?.py` are multiple comment generator which uses a faster madlibs based text generation algorithm. The madlibs are based around the political figure "Lord Buckethead". These were used as a faster alternative to `bot.py`. I still ran both `bot.py` and all the `bot_lite?.py` files\
`submitter.py` submits new posts copied from different subreddits.\
`upvoter_comment.py` upvotes comments based on the sentiment around the keyword 'trump'. If it is positive, it downvotes; otherwise, it upvotes.\
`upvoter_submission.py` upvotes submissions based on the sentiment around the keyword 'trump'. If it is positive, it downvotes; otherwise, it upvotes.\
## Politician
These bots clearly support Lord Buckethead while clearly goes against Trump.
### Favorite Bot post
https://old.reddit.com/r/BotTown2/comments/r4kobz/vaccine_misinformation_in_rwayofthebern/hmhl809/
![Favorite Bot Interaction](favorite_comment.png)
I liked this comment, because the bot seems like its responding to the comment in a meaningful way, but if you carefully read the comment, it does not make much sense at all.

#### Results
BotssasinsCreed
```
len(comments)= 716
len(top_level_comments)= 27
len(replies)= 689
len(valid_top_level_comments)= 23
len(not_self_replies)= 688
len(valid_replies)= 545
========================================
valid_comments= 568
```
TheElderBots
```
len(comments)= 699
len(top_level_comments)= 38
len(replies)= 661
len(valid_top_level_comments)= 36
len(not_self_replies)= 661
len(valid_replies)= 518
========================================
valid_comments= 554
```
BotBoysTaxEvasion
```
len(comments)= 687
len(top_level_comments)= 40
len(replies)= 647
len(valid_top_level_comments)= 36
len(not_self_replies)= 645
len(valid_replies)= 507
========================================
valid_comments= 543
```
BotlineMiami
```
len(comments)= 708
len(top_level_comments)= 32
len(replies)= 676
len(valid_top_level_comments)= 28
len(not_self_replies)= 673
len(valid_replies)= 553
========================================
valid_comments= 581
```
GrandTheftBot
```
len(comments)= 1000
len(top_level_comments)= 101
len(replies)= 899
len(valid_top_level_comments)= 101
```
##### What my score should be
I finished all 6 tasks. There is a discrepancy between `len(not_self_replies)` and `len(valid_replies)` because the code was fixed after running for awhile.\
However, I still believe I deserve the 18 points. +18\
My github repo has all the required elements. +2\
Extra Credit worth two points (ECT) 1~3: The sum of the comments posted by my bots well exceeds 1000. +6\
ECT 4: My submitter is able to submit over 200 submissions. +2\
ECT 6: I calculated the highest voted comment in `comments_without_replies2` and voted accordingly. +2\
ECT 7: I used the TextBlob library to access and upvote accordingly for both comments and submissions. +4\
Extra Credit worth five points: I used a GPT-2 algorithm to generate my text. +5\
\
Judgement Call:
ECT 5: While I clearly have 4 bots that posted more than 500 comments, my fifth bot, `GrandTheftBot`, does not have a clear `bot_counter.py` output.\
The initial subreddit "BotTown" was banned while running `bot_counter.py` for `GrandTheftBot`, as such, while it shows `valid_top_comments`,
it does not show the rest of the results. While I firmly believe that `GrandTheftBot` posted more than 500 valid comments, I unfortunately lack the proof.\
If you accept the circumstantial evidence, I think I deserve the two points.\
\
Minimum score: 18+2+6+2+2+4+5 = 39 Points\
Maximum score: (Min Score) + 2 = 41 Points\


