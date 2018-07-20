import csv
import re
import requests
from configparser import ConfigParser
from bs4 import BeautifulSoup
from model.ConnecsiModel import ConnecsiModel

class YoutubeApiController:
    def __init__(self):
        self.channelId = ''
        config = ConfigParser()
        config.read('config.ini')
        self.api_key = config.get('auth', 'api_key')
        self.channel_details_url = config.get('instance', 'channel_details_url')
        self.get_channel_ids_url = 'https://www.googleapis.com/youtube/v3/search?part=id&type=channel&key='+self.api_key
        self.latest_video_ids_url= 'https://www.googleapis.com/youtube/v3/search?part=snippet&order=date&type=video&key='+self.api_key
        self.video_details_url = 'https://www.googleapis.com/youtube/v3/videos?key=' + self.api_key + '&part=snippet,statistics&id='
        self.channel_thumbnail=''
        self.channelTitle=''
        self.channel_desc=''
        self.subscriberCount=''
        self.subscriberCount_lost=0
        self.total_100video_views = 0
        self.total_100video_views_unique = 0
        self.total_100video_likes = 0
        self.total_100video_dislikes = 0
        self.total_100video_comments = 0
        self.total_100video_shares = 0
        self.facebook_url = ''
        self.insta_url = ''
        self.twitter_url = ''
        self.business_email = ''



    def get_Json_data_Request_Lib(self, url):
        r = requests.get(url=url)
        json_data = r.json()
        return json_data


    def get_channel_details(self):
        url = self.channel_details_url+self.channelId+'&key='+self.api_key
        print(url)
        channel_data = self.get_Json_data_Request_Lib(url=url)
        print(channel_data)
        # exit()
        try:
            self.channel_thumbnail = channel_data['items'][0]['snippet']['thumbnails']['default']['url']
            # print(self.channel_thumbnail)
            # exit()
            self.channelTitle = channel_data['items'][0]['snippet']['title']
            self.channel_desc = channel_data['items'][0]['snippet']['description']
            # print(self.channel_desc)
            # exit()
            self.subscriberCount = channel_data['items'][0]['statistics']['subscriberCount']
            video_ids = self.get_latest_video_ids(channelId=self.channelId)
            self.get_video_details(video_ids=video_ids)
            self.get_social_media_url(channel_id=self.channelId)
        except Exception as e:
            print(e)
            pass
        # return data

    def get_social_media_url(self,channel_id):
        url = 'https://www.youtube.com/channel/'+channel_id
        print(url)
        page = requests.get(url=url).content
        soup = BeautifulSoup(page,"html.parser")
        # print(soup)
        links = []
        for link in soup.findAll('a', attrs={'href': re.compile("^https://")}):
            links.append(link.get('href'))
        for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
            links.append(link.get('href'))
        links = list(set(links))

        facebook_string = ['facebook']
        facebook_url = [s for s in links if any(xs in s for xs in facebook_string)]
        if facebook_url:
            self.facebook_url=facebook_url

        insta_string = ['instagram']
        insta_url = [s for s in links if any(xs in s for xs in insta_string)]
        if insta_url:
            self.insta_url = insta_url

        twitter_string = ['twitter']
        twitter_url = [s for s in links if any(xs in s for xs in twitter_string)]
        if twitter_url:
            self.twitter_url = twitter_url


    def get_video_details(self,video_ids):
        try:
            size = int(len(video_ids)/2)
            video_ids = [video_ids[x:x + size] for x in range(0, len(video_ids), size)]
        except:pass

        for item in video_ids:
            video_ids_string = ','.join(item)
            url = self.video_details_url + video_ids_string
            # print(url)
            # exit()
            json_video_data = self.get_Json_data_Request_Lib(url=url)
            items = json_video_data['items']
            # twitter_url_list=[]
            # facebook_url_list=[]
            # insta_url_list=[]
            for item in items:
                try:
                    self.total_100video_views += int(item['statistics']['viewCount'])
                    self.total_100video_likes += int(item['statistics']['likeCount'])
                    self.total_100video_dislikes += int(item['statistics']['dislikeCount'])
                    self.total_100video_comments += int(item['statistics']['commentCount'])
                    # self.total_100video_shares += int(item['statistics']['viewCount'])
                    # description = item['snippet']['description']
                    # print(description)
                except:pass

                # facebook_url = re.findall('http://facebook\.*.*',description)
                # if facebook_url:
                #     facebook_url_list.append(facebook_url[0])
                # insta_url = re.findall('http://instagram\.*.*', description)
                # if insta_url:
                #     insta_url_list.append(insta_url[0])
                # twitter_url = re.findall('http://twitter\.*.*', description)
                # if twitter_url:
                #     twitter_url_list.append(twitter_url[0])
                # print(twitter_url_list)
                # self.facebook_url = list(set(facebook_url_list))
                # self.insta_url= list(set(insta_url_list))
                # self.twitter_url = list(set(twitter_url_list))





    def get_latest_video_ids(self,channelId):
        counter = 1
        pageToken = ''
        video_ids = []
        while counter <= 2 :
            url=self.latest_video_ids_url+'&maxResults=50'+'&pageToken='+pageToken+'&channelId='+str(channelId)
            # print(url)
            # exit()
            json_data = self.get_Json_data_Request_Lib(url=url)
            # print(json_data)
            try:
                pageToken = json_data['nextPageToken']
            except:pass
            try:
                items = json_data['items']
                # print(items)
                counter = counter+1
                for item in items:
                    video_ids.append(item['id']['videoId'])
            except:pass
        print(len(video_ids))
        # exit()
        return video_ids

    def get_all_channel_ids(self):
        counter = 1
        pageToken = ''
        channel_ids = []
        while counter <= 2:
            url = self.get_channel_ids_url + '&maxResults=50' + '&pageToken=' + pageToken
            # print(url)
            json_data = self.get_Json_data_Request_Lib(url=url)
            try:
                pageToken = json_data['nextPageToken']
            except:
                pass
            items = json_data['items']
            # print(items)
            # exit()
            counter = counter + 1
            try:
                for item in items:
                    # print(item)
                    # print(item['id'])
                    # print(item['id']['channelId'])
                    channel_id = item['id']['channelId']
                    print(channel_id)
                    channel_ids.append(channel_id)
            except:pass
        # print(len(video_ids))
        # exit()
        connecsiObj = ConnecsiModel()
        connecsiObj.insert__(data=channel_ids,table_name='youtube_channel_ids',columns=['channel_id'],IGNORE='IGNORE')



    def get_data(self):
        obj = ConnecsiModel()
        data = obj.get__(table_name='youtube_channel_ids',STAR='*')
        # print(data)
        channelIds = []
        for item in data:
            # print(item[0])
            channelIds.append(item[0])
        # print(channelIds)
        # exit()
        for channelId in channelIds:
            myList = []
            # self.YoutubeApiController(channelId=channelId)
            try:
                self.channelId=channelId
                self.get_channel_details()
                myList.append(channelId)
                myList.append(self.channelTitle)
                myList.append(self.channel_thumbnail)
                myList.append(self.channel_desc)
                myList.append(self.subscriberCount)
                myList.append(self.subscriberCount_lost)
                myList.append(self.business_email)
                myList.append(self.total_100video_views)
                myList.append(self.total_100video_views_unique)
                myList.append(self.total_100video_likes)
                myList.append(self.total_100video_dislikes)
                myList.append(self.total_100video_comments)
                myList.append(self.total_100video_shares)
                myList.append(self.facebook_url)
                myList.append(self.insta_url)
                myList.append(self.twitter_url)
                print(myList)
                # exit()
                columns = ['channel_id', 'title', 'channel_img', 'desc', 'subscriberCount_gained','subscriberCount_lost', 'business_email',
                           'total_100video_views','total_100video_views_unique','total_100video_likes','total_100video_dislikes','total_100video_comments',
                           'total_100video_shares','facebook_url','insta_url','twitter_url']
                connecsiObj = ConnecsiModel()
                connecsiObj.insert__(table_name='youtube_channel_details',columns=columns,IGNORE='IGNORE',data=myList)
            except:
                print('Channel details failed to insert for channel_id = ',channelId)
                pass

            # with open("output.csv", 'a') as resultFile:
            #     wr = csv.writer(resultFile, dialect='excel')
            #     wr.writerow(myList)





