import re
from random import choice
from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup
import pymysql
import pymysql.cursors
from model.ConnecsiModel import ConnecsiModel

# USER_AGENTS = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36']
USER_AGENTS = ["Mozilla/5.0 (Windows NT 5.1; rv:41.0) Gecko/20100101 Firefox/41.0",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
               "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
               ]

class InstgramScrapper:
    def __init__(self, url,channel_id,twitter_url,video_categories,country,facebook_url,insta_url,youtube_url,user_agents=None):
        self.url = url
        self.user_agents = user_agents
        self.insta_data=[]
        # self.insta_post_data=[]
        self.insta_data.append(youtube_url)
        self.insta_data.append(twitter_url)
        self.insta_data.append(insta_url)
        self.insta_data.append(facebook_url)
        self.insta_data.append(country)
        self.video_categories = video_categories
        self.channel_id = channel_id

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

    def get_insta_data(self):
        return self.insta_data

    def get_insta_post_data(self):
        return self.insta_post_data

    def set_insta_data(self):
        page_metrics = self.page_metrics()
        # for key, value in page_metrics.items():
        #     print(key, ':', value)
        self.insta_data.append(page_metrics['id'])
        self.insta_data.append(page_metrics['username'])
        self.insta_data.append(page_metrics['full_name'])
        self.insta_data.append(page_metrics['business_category_name'])
        self.insta_data.append(page_metrics['profile_pic_url_hd'])
        self.insta_data.append(page_metrics['biography'])
        self.insta_data.append(page_metrics['edge_followed_by']['count'])

        for item in page_metrics['edge_owner_to_timeline_media']['edges']:
            # self.insta_post_data = []
            post_data = []
            post_data.append(page_metrics['id'])
            post_data.append(item['node']['id'])
            post_data.append(datetime.fromtimestamp(item['node']['taken_at_timestamp']).strftime('%Y-%m-%d %H:%M:%S'))
            hastag_list = []
            for text in item['node']['edge_media_to_caption']['edges']:
                 for tag in re.findall(r'[#@][^\s#@]+', text['node']['text']):
                     hastag_list.append(tag)
            hashtag_string = ','.join(hastag_list)
            # print(item)
            # print('string = ',hashtag_string)
            post_data.append(hashtag_string)
            post_data.append(item['node']['edge_liked_by']['count'])
            post_data.append(item['node']['edge_media_to_comment']['count'])
            # self.insta_post_data.append(post_data)
            self.insert_insta_post_data(post_data=post_data)
        self.insert_insta_data(data=self.insta_data)
        insta_history_data=[]
        insta_history_data.append(page_metrics['id'])
        insta_history_data.append(page_metrics['edge_followed_by']['count'])
        self.insert_insta_history_data(data=insta_history_data)

        try:
            connecsiObj = ConnecsiModel()
            # connecsiObj.insert__(table_name='channels_mapper',
            #                      columns=['youtube_channel_id', 'insta_channel_id', 'confirmed'],
            #                      data=[self.channel_id, page_metrics['id'], 'false'])
            connecsiObj.insert_insta_id_into_channels_mapper(youtube_channel_id=self.channel_id,insta_channel_id=page_metrics['id']
                                                             ,confirmed='false')
        except Exception as e:
            print(e)
            pass
        try:
            self.insert_insta_categories(video_categories=self.video_categories,insta_id=page_metrics['id'])
        except Exception as e:
            print(e)
            pass

    def insert_insta_data(self,data):
        modelObj = ConnecsiModel()
        # columns=['youtube_url','twitter_url','insta_url','facebook_url','country',
        #          'insta_id','username','title','business_category_name','channel_img','description','no_of_followers']
        modelObj.insert_update_insta_details(data=data)

    def insert_insta_history_data(self, data):
        modelObj = ConnecsiModel()
        columns = ['insta_id', 'no_of_followers']
        modelObj.insert__(table_name='insta_channels_history', columns=columns, data=data)

    def insert_insta_categories(self,video_categories,insta_id):
        for category_id in video_categories:
            # data = []
            # data.append(insta_id)
            # data.append(category_id)
            # columns=['insta_id','category_id']
            # modelObj.insert__(table_name='insta_id_category_id',columns=columns,data=data)
            modelObj = ConnecsiModel()
            modelObj.insert_categories_to_insta_channel(insta_id=insta_id,category_id=category_id)

    def insert_insta_post_data(self,post_data):
        modelObj = ConnecsiModel()
        # columns=['insta_id','post_id','post_time','insta_hashtags','no_of_post_likes','no_of_post_comments']
        modelObj.insert_update_insta_post_details(data=post_data)

# insta_url='https://www.instagram.com/blowek5'
# instagram = InstgramScrapper(url=insta_url)
# instagram.set_insta_data()



# insta_data = instagram.get_insta_data()
# print(insta_data)
# insta_post_data = instagram.get_insta_post_data()
# print(insta_post_data)

# print(page_metrics)
# print(post_metrics)
# for m in post_metrics:
#     i_id = str(m['id'])
#     i_post_time = datetime.fromtimestamp(m['taken_at_timestamp']).strftime('%Y-%m-%d %H:%M:%S')
#     i_likes = int(m['edge_liked_by']['count'])
#     i_comments = int(m['edge_media_to_comment']['count'])
#     i_media = m['display_url']
#     i_video = bool(m['is_video'])
#     print(i_id,"|",i_post_time,"|",i_likes,"|",i_comments)

