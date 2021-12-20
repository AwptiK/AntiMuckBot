#!/usr/bin/python3
import praw
from colorama import Fore
import topSecretInfo

# Variables. Don't forget to change before publishing!!!
clientID = topSecretInfo.clientID
clientSecret = topSecretInfo.clientSecret
username = topSecretInfo.username
password = topSecretInfo.password
subName = topSecretInfo.subName
userAgent = topSecretInfo.userAgent

# Message Replies
muckReply = "Will you please shut the fuck up?"
goodBotReply = "Thanks!"
badBotReply = "F. Can you tell me what i did wrong?"
replyBody = "\n\n ^(I'm just a stupid bot (also a real person but idk)) ^(trying to fix some of this sub's problems. [Here is my source code](https://github.com/AwptiK/AntiMuckBot))"

# Stuff...
bannedWords = ["muck", "umck," "cmuk", "mcuk," "ucmk", "cumk", "kumc", "ukmc", "mkuc", "kmuc", "umkc", "mukc",
               "mcku", "cmku", "kmcu", "mkcu", "ckmu", "kcmu", "kcum", "ckum", "ukcm", "kucm", "cukm", "uckm",
               "not giving a shit"]
logfileName = "AlreadyRepliedToComments.txt"
characterWhitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')


# Add the comment ID to a text file just in case it somehow wants to reply to it again. Which should NEVER happen
def AddCommentIDToList(comment_id):
    file = open(logfileName, "a")
    file.write(comment_id)
    file.write("\n")
    file.close()


def process_comment(_comment, depth=0):
    """Generate comment bodies and depths."""
    yield _comment.body, depth
    for _reply in _comment.replies:
        # depth += 1
        if depth == 2:
            _reply.reply("Shut the fuck up")
            print("Mucker has been shut up")
            break
        yield from process_comment(_reply, depth + 1)


def get_post_comments(post, more_limit=32):
    """Get a list of (body, depth) pairs for the comments in the post."""
    _comments = []
    post.comments.replace_more(limit=more_limit)
    for top_level in post.comments:
        _comments.extend(process_comment(top_level))
    return _comments


# Constantly run this shit
while True:
    # Try to shut a mucker up
    try:
        # TryToShutMucker()
        # TryToShutChain()
        reddit = praw.Reddit(
            client_id=clientID,
            client_secret=clientSecret,  # Connect to Reddit #
            password=password,
            user_agent=userAgent,
            username=username,
        )

        subreddit = reddit.subreddit(subName)

        print(Fore.YELLOW + reddit.user.me().__str__())
        print(Fore.LIGHTBLUE_EX + "Connected to subreddit of name: " + Fore.YELLOW + subreddit.display_name)

        # for submission in subreddit.stream.submissions():
        #     for comment in submission.comments:
        #         comment.replies.replace_more(limit=4)
        #         if comment.replies[1] is not None:
        #             reply = comment.replies[1]
        #             reply.reply("Shut the fuck up please")
        #             print("Mucker has been shut up")
        #             break
        #         else:
        #             break

        for submission in subreddit.stream.submissions():
            comments = get_post_comments(post=submission, more_limit=10)
            print(comments)
            # for comment in comments:
            #     if comment == ('muck', 3):
            #         print("Mucker has been shut up")

    # If the user presses Control and C, exit the program/stop the bot
    except KeyboardInterrupt:  # Ctrl + C exits
        print(Fore.RED + "Exiting...")
        break

    # if error, tell error
    except Exception as error:  # What did you do idiot?
        print(Fore.RED + "Well...fuck, something done fucked up")
        print(Fore.RED + "Error is: " + error.__str__())
        print(Fore.RED + "Trying to restart...")
