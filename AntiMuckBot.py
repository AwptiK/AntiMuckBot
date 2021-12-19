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
               "mcku", "cmku", "kmcu", "mkcu", "ckmu", "kcmu", "kcum", "ckum", "ukcm", "kucm", "cukm", "uckm"]
logfileName = "AlreadyRepliedToComments.txt"
characterWhitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')


# Add the comment ID to a text file just in case it somehow wants to reply to it again. Which should NEVER happen
def AddCommentIDToList(comment_id):
    file = open(logfileName, "a")
    file.write(comment_id)
    file.write("\n")
    file.close()

# Shut whoever is trying to Muck Chain up
def TryToShutMucker():
    reddit = praw.Reddit(           ####################
        client_id=clientID,
        client_secret=clientSecret, #Connect to Reddit#
        password=password,
        user_agent=userAgent,      ####################
        username=username,
    )
    print(Fore.YELLOW + reddit.user.me().__str__()) # Print your username to verify the connections

    desiredSub = reddit.subreddit(subName) # Choose the sub you want to destroy

    print(Fore.LIGHTBLUE_EX + "We online bois") # more verification
    print(Fore.LIGHTBLUE_EX + "Connected to subreddit of name: " + Fore.YELLOW + desiredSub.display_name) # even more verification

    for comment in desiredSub.stream.comments(skip_existing=True):
        # Check if comment is already replied to. Helps when testing, not in actual use
        with open(logfileName) as logFile:
            if comment.id in logFile.read():
                print(Fore.YELLOW + "Comment has already been replied to")
                continue

        # convert all text to lower case for ease of use
        commentBody = comment.body.lower()
        # remove any symbols and weird shit
        commentBodyLettersOnly = ''.join(filter(characterWhitelist.__contains__, commentBody))
        # Loop over every muck variation and check if the comment contains one of them
        for muckVariation in bannedWords:
            if muckVariation in commentBodyLettersOnly:
                comment.reply(muckReply + replyBody)
                AddCommentIDToList(comment.id)
                print(Fore.GREEN + "Mucker has been shut up")

# Constantly run this shit
while True:
    # Try to shut a mucker up
    try:
        TryToShutMucker()

    # If the user presses Control and C, exit the program/stop the bot
    except KeyboardInterrupt:  # Ctrl + C exits
        print(Fore.RED + "Exiting...")
        break

    # if error, tell error
    except Exception as error:  # What did you do idiot?
        print(Fore.RED + "Well...fuck, something done fucked up")
        print(Fore.RED + "Error is: " + error.__str__())
        print(Fore.RED + "Trying to restart...")
