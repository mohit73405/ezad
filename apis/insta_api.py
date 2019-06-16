import re
import urllib.parse
from random import choice
import json
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime
from controller.instagram.instagramCon import InstgramScrapper

ns_insta = Namespace('Insta', description='Insta Apis')
USER_AGENTS = ["Mozilla/5.0 (Windows NT 5.1; rv:41.0) Gecko/20100101 Firefox/41.0",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
                   "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
                   ]

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
                modelObj.update_insta_url_in_youtube_channel_details(insta_url=instagram_url,youtube_channel_id=youtube_channel_id)
            except Exception as e:
                print(e)
                pass

@ns_insta.route('/getInstagramChannel/<string:instagram_username>')
class Insta_api(Resource):
    def get(self,instagram_username):
        """get Instagram channel by insta url"""

        instagram_url = 'https://www.instagram.com/' + instagram_username
        self.url = instagram_url
        self.user_agents = None
        try:
            insta_data_dict = self.get_insta_data()
            # print(insta_data_dict)
            return insta_data_dict
        except Exception as e:
            print(e)
            pass
            return {'error':e}


    def get_insta_data(self):
        insta_data_list = []
        insta_data={}
        page_data = {}
        post_list = []
        page_metrics = self.page_metrics()
        # for key, value in page_metrics.items():
        #     print(key, ':', value)
        page_data.update({'insta_id':page_metrics['id']})
        page_data.update({'username':page_metrics['username']})
        page_data.update({'title':page_metrics['full_name']})
        page_data.update({'business_category_name':page_metrics['business_category_name']})
        page_data.update({'channel_img':page_metrics['profile_pic_url_hd']})
        page_data.update({'description':page_metrics['biography']})
        page_data.update({'no_of_followers':page_metrics['edge_followed_by']['count']})

        for item in page_metrics['edge_owner_to_timeline_media']['edges']:
            post_data = {}
            post_data.update({'insta_id':page_metrics['id']})
            post_data.update({'post_id':item['node']['id']})
            post_data.update({'post_time':datetime.datetime.fromtimestamp(item['node']['taken_at_timestamp']).strftime('%Y-%m-%d %H:%M:%S')})
            hastag_list = []
            for text in item['node']['edge_media_to_caption']['edges']:
                 for tag in re.findall(r'[#@][^\s#@]+', text['node']['text']):
                     hastag_list.append(tag)
            hashtag_string = ','.join(hastag_list)
            # print(item)
            # print('string = ',hashtag_string)
            post_data.update({'insta_hashtags':hashtag_string})
            post_data.update({'no_of_post_likes':item['node']['edge_liked_by']['count']})
            post_data.update({'no_of_post_comments':item['node']['edge_media_to_comment']['count']})
            post_list.append(post_data)
            # self.insert_insta_post_data(post_data=post_data)
        insta_data.update({'page_data':page_data})
        insta_data.update({'post_data': post_list})
        insta_data_list.append(insta_data)
        return insta_data_list
        # self.insert_insta_data(data=self.insta_data)

    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(USER_AGENTS)

    def __request_url(self):
        try:
            response = requests.get(
                self.url,
                headers={'User-Agent': self.__random_agent()})
            response.raise_for_status()
        except requests.HTTPError:
            raise requests.HTTPError('Received non-200 status code.')
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response.text

    @staticmethod
    def extract_json(html):
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
        return json.loads(raw_string)

    def page_metrics1(self):
        results = {}
        try:
            response = self.__request_url()
            json_data = self.extract_json(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
        except Exception as e:
            raise e
        else:
            for key, value in metrics.items():
                if key != 'edge_owner_to_timeline_media':
                    if value and isinstance(value, dict):
                        value = value['count']
                        results[key] = value
        return results


    def page_metrics(self):
        metrics=''
        try:
            response = self.__request_url()
            json_data = self.extract_json(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
        except Exception as e:
            print(e)
            pass
        return metrics


    def post_metrics(self):
        results = []
        try:
            response = self.__request_url()
            json_data = self.extract_json(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media'][
                'edges']
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node, dict):
                    results.append(node)
        return results