# -*- coding: utf-8 -*-
from Log_Handler import Log_Handler as lh
import  tweepy
import json


logger = lh.log_initializer()
def main():
   try:
       #Section 1
       #getting necessary keys and tokens from config file
       cofig_file = open("config.json").read()
       config_json = json.loads(cofig_file)
       consumer_key = config_json['twitter']['ConsumerKey']
       consumer_secret = config_json['twitter']['ConsumerSecret']
       access_token = config_json['twitter']['AccessToken']
       access_token_secret = config_json['twitter']['AccessTokenSecret']       
       api = IniTwitterApi(consumer_key, consumer_secret, access_token, access_token_secret)

       #1.1 retrieving users unique id
       user_name = input("\nPlease enter the username to fetch its unique id\n")
       logger.debug("Before calling get twitter data| user_name:" + str(user_name))
       user_unique_id = GetTwitterUniqId(api, user_name)
       print("\n\nUnique Id for user name:- " + str(user_name) + " is " + str(user_unique_id))
       
       #1.2 retrieving most pop tweet
       #Excluding the tweets whose authos it NOT CitronResearch
       user_name_citron = 'CitronResearch'
       max_retweet_count,popular_tweet =  GetMostRetwitted(api, user_name_citron)
       print("\nMost popular tweet of user name:- " + user_name_citron + " is \n" + str(popular_tweet) + " \nRetweet count:- " +str(max_retweet_count))
       
       #1.3 Citron Research mentions in Shopifys tweets
       user_name = "Shopify"
       user_mention = "Citron Research"
       shopify_citron_menlist = TweetsMentions(api, user_name, user_mention)
#       print("shopify_citron_menlist" + str(shopify_citron_menlist)) 
       
       #1.4 FTC mentions in Citron Research tweets
       user_name = user_name_citron
       user_mention = "FTC"
       citron_ftc_menlist = TweetsMentions(api, user_name, user_mention)
#       print("citron_ftc_menlist" + str(citron_ftc_menlist))
              
       #1.5 Export tweet lists to csv
       import csv
       with open ('tweets.csv', 'w') as outfile:
           writer = csv.writer(outfile)
           writer.writerow(shopify_citron_menlist)
           writer.writerow(citron_ftc_menlist)
                  
   except Exception as Ex:
       logger.error("Exception occurred in the main method| Exception:" + str(Ex))

def IniTwitterApi(consumer_key, consumer_secret, access_token, access_token_secret):
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)        
        api = tweepy.API(auth)
        return api
    except Exception as Ex:
        logger.error("Exception occurred in the IniTwitterApi method| Exception:" + str(Ex))


def GetTwitterUniqId(api, user_name):
    try:
        user = api.get_user(user_name)
        #id_str is the string version of id in user object 
        print ("Unique Id: " + user.id_str)
#        open("user_profile.txt","w").write(str(user)).close()
        return user.id_str
    except Exception as Ex:
        logger.error("Exception occurred in the GetTwitterUniqId method| Exception:" + str(Ex))

def GetMostRetwitted(api, user_name):
    try:
#        open("home_timeline.txt","w", encoding="utf-8").write(str(user_timeline))
        max_retweet_count = 0
        popular_tweet = ''        
        for tweets in tweepy.Cursor(api.user_timeline, id = user_name).items(): 
            #Chooosing to exclude the tweets whose author is not citron
            if not hasattr(tweets, 'retweeted_status'):  
#                tweet_retweet_author = tweets.retweeted_status.author.id         
#                tweet_author = tweets.author.id               
                tweet_text = tweets.text                             
                tweet_retweet_count = tweets.retweet_count 
                
                if(tweet_retweet_count > max_retweet_count):                    
                    max_retweet_count = tweet_retweet_count
                    popular_tweet =tweet_text
                    
        logger.info("\n\nMost Pop Tweet:" + str(popular_tweet) + "\nRetweet Count:" + str(max_retweet_count))
        return (max_retweet_count,popular_tweet)
            
    except Exception as Ex:
        logger.error("Exception occurred in the GetMostRetwitted method| Exception:" + str(Ex))
  
def TweetsMentions(api, user_name, user_mention):
    try:
        mention_tweet_list = []        
#        file = open("shopify_tweets.txt","a+", encoding="utf-8")
        for tweets in tweepy.Cursor(api.user_timeline, id = user_name, count=200).items():
#            file.write(tweets.text + "\n\n")
            if user_mention in tweets.text:
                 logger.debug("user mention found:" +  tweets.text)
                 mention_tweet_list.append(tweets.text)       
#        file.close()
        return mention_tweet_list
    except Exception as Ex:
        logger.error("Exception occurred in the TweetsMentions method| Exception:" + str(Ex))


if __name__ == "__main__":
    main()
