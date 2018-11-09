import twitter
import csv
import re
import os
import requests
from configparser import ConfigParser
from bs4 import BeautifulSoup
from model.ConnecsiModel import ConnecsiModel

class TwitterApiController:
    def __init__(self):
        self.channelId = ''
        config = ConfigParser()
        config.read('config.ini')
        self.consumer_key = config.get('auth', 'consumer_key')
        self.consumer_secret = config.get('auth','consumer_secret')
        self.access_token = config.get('auth', 'access_token')
        self.access_token_secret = config.get('auth', 'access_token_secret')
        self.api = twitter.Api(consumer_key=self.consumer_key,
                      consumer_secret=self.consumer_secret,
                      access_token_key=self.access_token,
                      access_token_secret=self.access_token_secret)
        self.api.VerifyCredentials()



    def get_Json_data_Request_Lib(self, url):
        r = requests.get(url=url)
        json_data = r.json()
        return json_data

    def get_data(self):
        user_data = self.api.GetUser(screen_name='msigaming_pl')
        user_timeline = self.api.GetUserTimeline(screen_name='msigaming_pl',count=100)
        for key, value in user_data.__dict__.items():
            print(key,':',value)
        # print(user_timeline)
        for item in user_timeline:
            print(item)
            for key, value in item.__dict__.items():
                print(key, ':', value)
        print(len(user_timeline))

    def get_data_by_screen_name(self,screen_name='Cristiano'):
        title=''
        no_of_followers=''
        business_email=''
        website=''
        no_of_views=0
        no_of_likes=0
        no_of_comments=0
        no_of_retweets=0
        hashtagsList=[]
        user_data = self.api.GetUser(screen_name=screen_name)
        user_data_dict = user_data.AsDict()
        print(user_data_dict)
        title=user_data_dict['name']
        no_of_followers = user_data_dict['followers_count']
        website = user_data_dict['url']
        print('title =',title)
        print('no of followers = ',no_of_followers)
        print('website = ',website)

        # for key, value in user_data.__dict__.items():
        #     print(key, ':', value)

        user_timeline = self.api.GetUserTimeline(screen_name=screen_name, count=7)

        # print(user_timeline)
        for item in user_timeline:
            status_dict = item.AsDict()
            # for key, value in item.__dict__.items():
            #     print(key, ':', value)
            status_id = status_dict['id']
            no_of_likes  += status_dict['favorite_count']
            no_of_retweets += status_dict['retweet_count']
            # no_of_comments = status_dict['user_mentions']
            # print('user mentions = ',no_of_comments)
            hashtags=status_dict['hashtags']
            for hashtag in hashtags:
                # print(hashtag['text'])
                hashtagsList.append(hashtag['text'])
        print('no of likes = ',no_of_likes)
        print('no of retweets',no_of_retweets)
        # print('hashtags = ',hashtagsList)
        hashtagsList_string=','.join(hashtagsList)
        print(hashtagsList_string)
        no_of_comments_url='https://twitter.com/'+screen_name+'/with_replies'
        print(no_of_comments_url)
        page = requests.get(url=no_of_comments_url).content
        soup = BeautifulSoup(page, "html.parser")
        # print(soup)
        # find a list of all span elements
        spans = soup.find_all('span', {'class': 'ProfileTweet-actionCount'})
        print(spans)
        # create a list of lines corresponding to element texts
        lines = [span.get_text() for span in spans]
        print(lines)



    def get_content_categories(self):
        url = 'https://ads-api.twitter.com/4/content_categories'
        content_categories = self.get_Json_data_Request_Lib(url=url)
        print(content_categories)

    def get_user_categories(self):
        user_categories = self.api.GetUserSuggestionCategories()
        print(user_categories)
        for category in user_categories:
            print(category)
            self.get_users_by_category(category=category)
    def get_users_by_category(self,category):
        users = self.api.GetUserSuggestion(category=category)
        # print(users)
        for user in users:
            print(user)
        # exit()

    def search_users(self):
        results = self.api.GetSearch(raw_query="q=Entertainment & Pop Culture%20&result_type=recent&since=2014-07-19&count=100")
        for item in results:
            print(item)
            # [q = "to:$tweeterusername", sinceId = $tweetId]

    # def get_reply_count(self,screen_name,tweet_id):
    #     query = "to:"+screen_name+"&sinceId="+str(tweet_id)
    #     results = self.api.GetSearch(raw_query=query)
    #     for item in results:
    #         print(item)