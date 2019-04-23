import urllib.parse

from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime
from controller.twitter_module.TwitterApiController import TwitterApiController

ns_twitter = Namespace('Twitter', description='Twitter Apis')

@ns_twitter.route('/addTwitterChannel/<string:channel_id>/<string:business_email>/<string:youtube_channel_id>')
class Twitter(Resource):
    def post(self,channel_id,business_email,youtube_channel_id):
        '''add twitter_module channel by channel_id'''
        modelObj = ConnecsiModel()
        columns = ['channel_id', 'twitter_url', 'country', 'facebook_url', 'insta_url']
        channel_data = modelObj.get__(table_name='youtube_channel_details', columns=columns,WHERE='WHERE'
                                      ,compare_column='channel_id',compare_value=str(youtube_channel_id))
        # print(channel_data)
        # exit()
        # ratelimit_counter = 0
        for item in channel_data:
            youtube_channel_id = item[0]
            country = item[2]
            facebook_url = item[3]
            insta_url = item[4]
            youtube_url = 'https://www.youtube.com/channel/' + youtube_channel_id

            vc_data = ''
            screen_name = ''
            output = ''
            try:
                print('twitter_module url',item[1])
                vc_data = modelObj.get_youtube_categories_by_channel_id(channel_id=youtube_channel_id)
                print(vc_data)
            except:
                pass
            video_categories = []
            try:
                for vc_item in vc_data:
                    video_categories.append(vc_item[1])
            except:
                pass
            try:
                twitter_url = item[1]
                # output = re.findall('http(.*)', twitter_url)
            except:
                pass
            try:
                parsed = urllib.parse.urlsplit(twitter_url)
                path = parsed.path
                output = path.rsplit('/', 3)
            except:
                pass
            try:
                screen_name = output[1]
                print(screen_name)
            except:
                pass

            try:
                conObj = TwitterApiController()
                conObj.get_data_by_screen_name(channel_id=youtube_channel_id, twitter_url=twitter_url,
                                               screen_name=screen_name, video_categories=video_categories
                                               , country=country, facebook_url=facebook_url, insta_url=insta_url,
                                               youtube_url=youtube_url)
            except:
                pass

