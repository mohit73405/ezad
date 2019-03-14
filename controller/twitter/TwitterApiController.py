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
                      access_token_secret=self.access_token_secret,
                               sleep_on_rate_limit=True)
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

    def get_data_by_screen_name(self,channel_id,twitter_url,screen_name,video_categories,country,facebook_url,insta_url,youtube_url):
        twitter_id = ''
        title=''
        description=''
        location=''
        no_of_followers=0
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
        try:
            twitter_id = user_data_dict['id_str']
            title=user_data_dict['name']
            description = user_data_dict['description']
            location = user_data_dict['location']
            no_of_followers = user_data_dict['followers_count']
            website = user_data_dict['url']
        except Exception as e:
            print(e)
            pass

        print('twitter id = ',twitter_id)
        print('screen name =',screen_name)
        print('title =',title)
        print('description = ',description)
        print('location = ', location)
        print('no of followers = ',no_of_followers)
        print('website = ',website)
        print('twitter_url = ',twitter_url)

        # for key, value in user_data.__dict__.items():
        #     print(key, ':', value)

        user_timeline = self.api.GetUserTimeline(screen_name=screen_name, count=100)

        # print(user_timeline)
        for item in user_timeline:
            status_dict = item.AsDict()
            # for key, value in item.__dict__.items():
            #     print(key, ':', value)
            try:
                status_id = status_dict['id']
                no_of_likes  += status_dict['favorite_count']
                no_of_retweets += status_dict['retweet_count']
                # no_of_comments = status_dict['user_mentions']
                # print('user mentions = ',no_of_comments)
                hashtags=status_dict['hashtags']
                for hashtag in hashtags:
                    # print(hashtag['text'])
                    hashtagsList.append(hashtag['text'])
            except Exception as e:
                print(e)
                pass
        print('no of likes = ',no_of_likes)
        print('no of retweets',no_of_retweets)
        # print('hashtags = ',hashtagsList)
        hashtagsList_string=','.join(hashtagsList)
        print('hastags = ',hashtagsList_string)

        ###################### no of comments##############################
        # no_of_comments_url='https://twitter.com/'+screen_name+'/with_replies'
        # print(no_of_comments_url)
        # page = requests.get(url=no_of_comments_url).content
        # soup = BeautifulSoup(page, "html.parser")
        # print(soup)
        # find a list of all span elements
        # spans = soup.find_all('span', {'class': 'ProfileTweet-actionCount'})
        # button = soup.find_all('button', {'class': 'ProfileTweet-actionButton js-actionButton js-actionReply'})
        # span = button.find('span', {'class': 'ProfileTweet-actionCount'})
        # replies_count=span.attrs["data-tweet-stat-count"]

        # print(button)
        # print(span)
        # print(replies_count)
        ################################################ no of comments #################

        columns = ['twitter_id','screen_name','title','description','location','no_of_followers','no_of_likes_recent100',
        'no_of_retweets_recent100','website','twitter_url','hashtags','facebook_url','insta_url','youtube_url','country']
        data = [twitter_id,screen_name,title,description,location,no_of_followers,no_of_likes,no_of_retweets
            ,website,twitter_url,hashtagsList_string,facebook_url,insta_url,youtube_url,country]
        connecsiObj= ConnecsiModel()
        try:
            connecsiObj.insert__(table_name='twitter_channel_details',IGNORE='IGNORE',columns=columns,data=data)
        except Exception as e:
            print(e)
            pass
        try:
            connecsiObj.insert__(table_name='channels_mapper',columns=['youtube_channel_id','twitter_channel_id','confirmed'],data=[channel_id,twitter_id,'false'])
        except Exception as e:
            print(e)
            pass
        for category_id in video_categories:
            try:
                connecsiObj.insert__(table_name='twitter_id_category_id',columns=['twitter_id','category_id'],data=[twitter_id,category_id])
            except Exception as e:
                print(e)
                pass


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