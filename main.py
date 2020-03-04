import praw
import json
import os
import slack
import requests

#Retrieve username and password from json
keys = {}
with open("pwd.json","r") as f:
    keys = json.loads(f.read())

client = keys['client']
secret = keys['secret']
username = keys['username']
userpwd = keys['userpwd']
wekbook_url = keys['url']
reddit = praw.Reddit(client_id=client, client_secret=secret, password=userpwd, username=username, user_agent='fetch_script')

reqs = ["usa-ny", "atx", "rx570", "rx 570"]

for post in reddit.subreddit("hardwareswap").stream.submissions():
    post_t = post.title.lower();
    buyorsell = post.link_flair_text;
    for req in reqs:
        if req in post_t:
            data = {
                "blocks": [
                    { "type": "divider"},
                    { "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": post.title
                        }
                    },
                    { "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "https://www.reddit.com" + post.permalink
                        }
                    },
                    { "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Type of post: " + buyorsell
                        }
                    },
                    { "type": "divider"},
                ]
            }
            response = requests.post(wekbook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
            print(post.title)
            break
