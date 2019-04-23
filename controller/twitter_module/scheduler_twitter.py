import re
import urllib.parse

import schedule #pip install schedule
import time
# import sys
# sys.path.append('/cryto_trading/CryptoMasterMindsApi/controller')
from controller.twitter_module.TwitterApiController import TwitterApiController
from model.ConnecsiModel import ConnecsiModel

def get_data():
    conObj = TwitterApiController()
    conObj.get_data()

def get_data_by_screen_name():
    modelObj = ConnecsiModel()
    columns=['channel_id','twitter_url','country','facebook_url','insta_url']
    channel_data=modelObj.get__(table_name='youtube_channel_details',columns=columns)
    # print(channel_data)
    # exit()
    # ratelimit_counter = 0
    for item in channel_data:
        channel_id = item[0]
        country = item[2]
        facebook_url = item[3]
        insta_url= item[4]
        youtube_url = 'https://www.youtube.com/channel/'+channel_id
        if item[1]:
            vc_data=''
            screen_name = ''
            output=''
            try:

                print(item[1])
                vc_data = modelObj.get_youtube_categories_by_channel_id(channel_id=channel_id)
                print(vc_data)
            except:pass
            video_categories=[]
            try:
                for vc_item in vc_data:
                    video_categories.append(vc_item[1])
            except:pass
            try:
                twitter_url = item[1]
                # output = re.findall('http(.*)', twitter_url)
            except:pass
            try:
                parsed = urllib.parse.urlsplit(twitter_url)
                path=parsed.path
                output=path.rsplit('/', 3)
            except:pass
            try:
                screen_name = output[1]
                print(screen_name)
            except:pass

            try:
                conObj = TwitterApiController()
                conObj.get_data_by_screen_name(channel_id=channel_id,twitter_url=twitter_url,screen_name=screen_name,video_categories=video_categories
                                                   ,country=country,facebook_url=facebook_url,insta_url=insta_url,youtube_url=youtube_url)
            except:pass

        else:
            try:
                data = [channel_id, 'false']
                modelObj.insert__(table_name='channels_mapper',columns=['youtube_channel_id','confirmed'],data=data)
            except:pass

def get_content_categories():
    conObj = TwitterApiController()
    conObj.get_user_categories()

def search_users():
    conObj = TwitterApiController()
    conObj.search_users()
# search_users()
# get_content_categories()
# get_data()
get_data_by_screen_name()

############change parameter for required periodic tasks###################
#default is 1 minute it can be changed as per requirement
#schedule.every(1).minutes.do(getCoinDetails,'coinmarketcap.com')
# schedule.every().day.at("07:00").do(del_and_update_events)
# schedule.every().day.at("05:00").do(get_fiat_daily_data)
#schedule.every(5).minutes.do(getDailyData_records,'coinmarketcap.com')
#schedule.every(1).minutes.do(getDailyData,'coinmarketcap.com')

#schedule.every().hour.do(periodic_task)
#schedule.every().day.at("10:30").do(getCoinDetails,'coinmarketcap.com')
#schedule.every(5).to(10).minutes.do(periodic_task)
#schedule.every().monday.do(periodic_task)
#schedule.every().wednesday.at("13:15").do(periodic_task)
#schedule.cancel_job(periodic_task())
###########################################################################
# while True:
#
#     schedule.run_pending()
#     time.sleep(1)


