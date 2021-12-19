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


def AddCommentIDToList(comment_id):
    file = open(logfileName, "a")
    file.write(comment_id)
    file.write("\n")
    file.close()


def TryToShutMucker():
    reddit = praw.Reddit(
        client_id=clientID,
        client_secret=clientSecret,
        password=password,
        user_agent=userAgent,
        username=username,
    )
    print(Fore.YELLOW + reddit.user.me().__str__())

    desiredSub = reddit.subreddit(subName)

    print(Fore.LIGHTBLUE_EX + "We online bois")
    print(Fore.LIGHTBLUE_EX + "Connected to subreddit of name: " + Fore.YELLOW + desiredSub.display_name)

    for comment in desiredSub.stream.comments(skip_existing=True):
        with open(logfileName) as logFile:
            if comment.id in logFile.read():
                print(Fore.YELLOW + "Comment has already been replied to")
                continue

        commentBody = comment.body.lower()
        commentBodyLettersOnly = ''.join(filter(characterWhitelist.__contains__, commentBody))
        # if commentBodyLettersOnly.lower().__contains__() in muckVariations:
        #     comment.reply(muckReply + replyBody)
        #     AddCommentIDToList(comment.id)
        #     print(Fore.GREEN + "Mucker has been shut up")
        for muckVariation in bannedWords:
            if muckVariation in commentBodyLettersOnly:
                comment.reply(muckReply + replyBody)
                AddCommentIDToList(comment.id)
                print(Fore.GREEN + "Mucker has been shut up")


while True:
    try:
        TryToShutMucker()

    except KeyboardInterrupt:  # Ctrl + C exits
        print(Fore.RED + "Exiting...")
        break
    except Exception as error:  # What did you do idiot?
        print(Fore.RED + "Well...fuck, something done fucked up")
        print(Fore.RED + "Error is: " + error.__str__())
        print(Fore.RED + "Trying to restart...")
