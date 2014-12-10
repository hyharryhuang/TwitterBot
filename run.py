#!/usr/bin/env python
#coding: utf8 
 
import tweepy, time, sys, re, json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#API KEYS - Fill these in from Twitter. 
CONSUMER_KEY = '1234' 
CONSUMER_SECRET = '1234'
ACCESS_KEY = '1234'
ACCESS_SECRET = '1234'
USER_HANDLE = "@sample"

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self):
        self.wait = 0
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        self.api = tweepy.API(self.auth)
        self.lastTweeted = ""
        self.lastTweetedCount = 0

    def on_status(self, status):
        try:
            tweetText = re.split(regex, status.text.encode('ascii','ignore'))

            #sort out any white spaces left over from splitting
            #account for if username is at the start of a tweet/in the middle/at the end
            if(tweetText[0] != ''):
                tweetText[0] = tweetText[0].rstrip(' ')
            else:
                tweetText[1] = tweetText[1].lstrip(' ')

            textTweetWithoutSpaces = ''.join(tweetText)

            #do not reply to retweets
            if "RT:" in overallInput: 
                return

            postMsg = '@' + status.author.screen_name + " " + textTweetWithoutSpaces

            #prevent bot loops - if we tweet the same person more than 10 times then start ignoring. 
            if(status.author.screen_name == self.lastTweeted):
                self.lastTweetedCount += 1
            else:
                self.lastTweeted = status.author.screen_name
                self.lastTweetedCount = 0

            if(self.lastTweetedCount > 10):
                return

            #rate limiting - if attempts is greater than 10, give up
            try:
                if(self.wait > 10):
                    return
                elif(self.wait > 0):
                    time.sleep(self.wait)

                self.api.update_status(postMsg, status.id)
                self.wait = 0
            except Exception, a:
                self.wait += 1
                return

        except Exception, e:
            return

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()

    stream = Stream(l.auth, l)

    #start listening to userstream
    stream.userstream()