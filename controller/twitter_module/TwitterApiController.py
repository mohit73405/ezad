import twitter
import csv
import re
import os
import requests
from configparser import ConfigParser
from bs4 import BeautifulSoup
from datetime import datetime
import time

from model.ConnecsiModel import ConnecsiModel

class TwitterApiController:
    def __init__(self):
        self.channelId = ''
        config = ConfigParser()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config.read(dir_path + '/config.ini')
        # config.read('config.ini')
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

    def get_data_by_screen_name(self,channel_id,twitter_url,screen_name,video_categories,country,facebook_url,insta_url,youtube_url,business_email=''):
        twitter_id = ''
        title=''
        description=''
        location=''
        no_of_followers=0
        business_email=business_email
        website=''
        no_of_views=0
        no_of_likes=0
        no_of_comments=0
        no_of_retweets=0
        hashtagsList=[]
        channel_img=''
        rate_limit_get_user = self.api.rate_limit.get_limit(url='/users/show')
        rate_limit_user_timeline = self.api.rate_limit.get_limit(url='/statuses/user_timeline')
        print('get user limit remaining = ',rate_limit_get_user.remaining)
        print('statuses user timeline limit remaining = ', rate_limit_user_timeline.remaining)
        # print(type(rate_limit_user_timeline))
        if rate_limit_get_user.remaining != 0 and rate_limit_user_timeline.remaining != 0 :
            user_data = self.api.GetUser(screen_name=screen_name)
            user_data_dict = user_data.AsDict()
            # print(user_data_dict)
            # exit()
            try:
                twitter_id = user_data_dict['id_str']
            except Exception as e:
                print(e)
                pass
            try:
                title=user_data_dict['name']
            except Exception as e:
                print(e)
                pass
            try:
                description = user_data_dict['description']
            except Exception as e:
                print(e)
                pass
            try:
                location = user_data_dict['location']
            except Exception as e:
                print(e)
                pass
            try:
                no_of_followers = user_data_dict['followers_count']
            except Exception as e:
                print(e)
                pass
            try:
                website = user_data_dict['url']
            except Exception as e:
                print(e)
                pass
            try:
                channel_img = user_data_dict['profile_image_url']
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
            print('profile img = ',channel_img)

            # for key, value in user_data.__dict__.items():
            #     print(key, ':', value)

            user_timeline = self.api.GetUserTimeline(screen_name=screen_name, count=100)

            # print(user_timeline)
            for item in user_timeline:
                status_dict = item.AsDict()
                # for key, value in item.__dict__.items():
                #     print(key, ':', value)
                hashtags=[]
                try:
                    status_id = status_dict['id']
                except Exception as e:
                    print(e)
                    pass
                try:
                    no_of_likes  += status_dict['favorite_count']
                    # print(no_of_likes)
                except Exception as e:
                    print(e)
                    pass
                try:
                    no_of_retweets += status_dict['retweet_count']
                except Exception as e:
                    print(e)
                    pass
                    # no_of_comments = status_dict['user_mentions']
                    # print('user mentions = ',no_of_comments)
                try:
                    hashtags=status_dict['hashtags']
                except Exception as e:
                    print(e)
                    pass
                try:
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

            # columns = ['twitter_id','screen_name','title','description','location','no_of_followers','no_of_likes_recent100',
            # 'no_of_retweets_recent100','website','twitter_url','hashtags','facebook_url','insta_url','youtube_url','country','channel_img','business_email']

            data = [twitter_id,screen_name,title,description,location,no_of_followers,no_of_likes,no_of_retweets
                ,website,twitter_url,hashtagsList_string,facebook_url,insta_url,youtube_url,country,channel_img,business_email]
            connecsiObj= ConnecsiModel()
            try:
                connecsiObj.insert_update_twitter_details(data=data)
            except Exception as e:
                print(e)
                pass
            try:
                history_columns = ['twitter_id', 'no_of_followers', 'no_of_likes_recent100', 'no_of_retweets_recent100']
                history_data=[twitter_id,no_of_followers,no_of_likes,no_of_retweets]
                connecsiObj.insert__(table_name='twitter_channels_history',columns=history_columns,data=history_data)
            except Exception as e:
                print(e)
                pass
            try:
                if business_email:
                    confirmed='true'
                else:
                    confirmed='false'
                # connecsiObj.insert__(table_name='channels_mapper',columns=['youtube_channel_id','twitter_channel_id','confirmed'],data=[channel_id,twitter_id,confirmed])
                connecsiObj.insert_into_channels_mapper(youtube_channel_id=channel_id,twitter_channel_id=twitter_id,confirmed=confirmed)
            except Exception as e:
                print(e)
                pass
            for category_id in video_categories:
                try:
                    # connecsiObj.insert__(table_name='twitter_id_category_id',columns=['twitter_id','category_id'],data=[twitter_id,category_id])
                    connecsiObj.insert_categories_to_twitter_channel(twitter_id=twitter_id,category_id=category_id)
                except Exception as e:
                    print(e)
                    pass
        else: time.sleep(30)

    def get_content_categories(self):
        url = 'https://ads-api.twitter_module.com/4/content_categories'
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