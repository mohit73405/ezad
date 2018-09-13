import csv
import re
import os
import requests
from configparser import ConfigParser
from bs4 import BeautifulSoup
from model.ConnecsiModel import ConnecsiModel

class FacebookApiController:
    def __init__(self):
        self.channelId = ''
        config = ConfigParser()
        config.read('config.ini')
        self.api_key = config.get('auth', 'api_key')
        self.regionCode_url = 'https://www.googleapis.com/youtube/v3/i18nRegions?part=id,snippet&key='+self.api_key


    def get_Json_data_Request_Lib(self, url):
        r = requests.get(url=url)
        json_data = r.json()
        return json_data


