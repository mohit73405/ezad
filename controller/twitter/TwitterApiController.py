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
        followers = self.api.GetUser(screen_name='CodeWisdom')
        for key, value in followers.__dict__.items():
            print(key,':',value)

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
