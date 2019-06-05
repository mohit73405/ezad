import urllib.parse

from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime
from controller.instagram.instagramCon import InstgramScrapper

ns_insta = Namespace('Insta', description='Insta Apis')

@ns_insta.route('/addInstagramChannel/<string:instagram_username>/<string:business_email>/<string:youtube_channel_id>')
class Insta_api(Resource):
    def post(self,instagram_username,business_email,youtube_channel_id):
        """add Instagram channel by insta url"""
        instagram_url = 'https://www.instagram.com/' + instagram_username
        modelObj = ConnecsiModel()
        columns = ['channel_id', 'twitter_url', 'country', 'facebook_url', 'insta_url']
        channel_data = modelObj.get__(table_name='youtube_channel_details', columns=columns,WHERE='WHERE'
                                      ,compare_column='channel_id',compare_value=str(youtube_channel_id))

        print('channel data = ',channel_data)

        for item in channel_data:
            print('im inside for')
            youtube_channel_id = item[0]
            country = item[2]
            facebook_url = item[3]
            insta_url = item[4]
            youtube_url = 'https://www.youtube.com/channel/' + youtube_channel_id
            twitter_url = item[1]
            vc_data = ''

            try:
                vc_data = modelObj.get_youtube_categories_by_channel_id(channel_id=youtube_channel_id)
            except Exception as e:
                print(e)
                pass
            video_categories = []
            try:
                for vc_item in vc_data:
                    video_categories.append(vc_item[1])
            except Exception as e:
                print(e)
                pass
            try:
                twitter_url = item[1]
                # output = re.findall('http(.*)', twitter_url)
            except Exception as e:
                print(e)
                pass

            try:
                conObj = InstgramScrapper(url=instagram_url,channel_id=youtube_channel_id,twitter_url=twitter_url,video_categories=video_categories
                                          ,country=country,facebook_url=facebook_url,insta_url=instagram_url,youtube_url=youtube_url,business_email=business_email)
                conObj.set_insta_data()

            except Exception as e:
                print(e)
                pass

