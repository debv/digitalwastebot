import sys
import os
import twitter
import time
import random
from twilio.rest import TwilioRestClient
from keys import *

def main():

    api = twitter.Api(
        consumer_key,
        consumer_secret,
        access_key,
        access_secret
    )

    client = TwilioRestClient(twil_sid, twil_auth)

    tweet = 1
    tweetedQuotes = 0
    imagesPath = os.listdir('./images')
    
    # Put quotes into list for random tweeting
    f = open('quotes/all.txt', 'r')
    quotes = f.readlines()
    f.close
   
    # Put images into list for random tweeting 
    images = []
    for image in imagesPath:
        if(image != '.DS_Store'):
            images.append('images/'+image)

    # Keep tweeting while there are things to tweet
    while(len(quotes) > 0): 
        # Tweet one image for every 10 quotes
        if(tweetedQuotes < 10 and quotes is not None):
            if(len(quotes) == 1):
                tweet = quotes[0]
            elif(len(quotes) < 1):
                continue      
            elif(len(quotes) > 1):
                tweet = random.choice(quotes)
            tweetIndex = quotes.index(tweet)
            api.PostUpdate(tweet)
            print("QUOTE")
            print(len(quotes))
            print(tweetIndex)
            del quotes[tweetIndex]
            tweetedQuotes += 1
        elif((tweetedQuotes >= 10 and images is not None) or (quotes is None)):
            tweet = random.choice(images)
            tweetIndex = images.index(tweet)
            api.PostUpdate('',image)
            print("IMAGE")
            print(len(images))
            print(tweetIndex)
            del images[tweetIndex]
            tweetedQuotes = 0

        # Text me if there are 5 images or quotes remaining
        if(len(quotes) == 5 or len(images) == 5):
            stats = ("DigitalWasteBot is running low on content!\n"
                + str(5) 
                + " Quotes Remaining\n" 
                + str(6) 
                + " Images Remaining")
            
            message = client.messages.create(body=stats,
                to="+13059679060",
                from_="+17866614259")

        # Only send out a tweet at 11am EST (1000 GMT) and 6pm EST (1800 GMT)
        if(time.gmtime().tm_hour == 15):
            time.sleep(25200) # Tweet again at 6pm
        elif(time.gmtime().tm_hour == 22):
            time.sleep(61200) # Tweet again at 11am

if __name__ == '__main__':
    main()
